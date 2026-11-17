"""
Main QA Engine for Self-Prompting ODQA System
Orchestrates the complete question-answering process
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

from database import DatabaseManager, QAPair
from gemini_client import GeminiClient
from clustering_retrieval import ClusteringRetrieval
from dataset_generator import DatasetGenerator
from config import MAX_DEMONSTRATIONS
from offline_qa import OfflineQAEngine
from seed_data import auto_seed_if_empty

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QAResult:
    """Represents the result of a question-answering request"""
    question: str
    answer: str
    explanation: Optional[str] = None
    confidence: float = 0.0
    demonstrations_used: int = 0
    processing_time: float = 0.0
    error: Optional[str] = None

class QAEngine:
    """Main engine for the Self-Prompting ODQA system"""
    
    def __init__(self):
        """Initialize the QA engine with all components"""
        self.db = DatabaseManager()
        auto_seed_if_empty(self.db)
        self.gemini = GeminiClient()
        self.clustering = ClusteringRetrieval(self.db)
        self.dataset_generator = DatasetGenerator(self.db, self.gemini)
        self.offline_qa = OfflineQAEngine()

        self.system_ready = True
        logger.info("QA Engine initialized successfully with seed data")
    
    def check_system_status(self) -> Dict[str, Any]:
        """Check the current status of the system"""
        dataset_stats = self.db.get_dataset_stats()
        clustering_stats = self.clustering.get_clustering_stats()
        
        system_ready = (
            dataset_stats["total_pairs"] > 0 and 
            clustering_stats["n_clusters"] > 0
        )
        
        return {
            "system_ready": system_ready,
            "dataset_stats": dataset_stats,
            "clustering_stats": clustering_stats,
            "components_status": {
                "database": True,
                "gemini_client": True,
                "clustering": clustering_stats["n_clusters"] > 0,
                "dataset": dataset_stats["total_pairs"] > 0
            }
        }
    
    def prepare_system(self, force_regenerate: bool = False) -> Dict[str, Any]:
        """Prepare the complete system (dataset generation + clustering)"""
        logger.info("Starting system preparation...")
        start_time = datetime.now()
        
        try:
            # Step 1: Generate dataset if needed
            dataset_stats = self.db.get_dataset_stats()
            
            if dataset_stats["total_pairs"] == 0 or force_regenerate:
                logger.info("Generating pseudo QA dataset...")
                if force_regenerate:
                    self.db.clear_database()
                
                generation_results = self.dataset_generator.generate_full_dataset()
                logger.info(f"Dataset generation completed: {generation_results}")
            else:
                logger.info(f"Using existing dataset with {dataset_stats['total_pairs']} QA pairs")
                generation_results = dataset_stats["topic_counts"]
            
            # Step 2: Prepare clustering system
            logger.info("Preparing clustering system...")
            clustering_results = self.clustering.prepare_system()
            
            # Update system status
            self.system_ready = clustering_results["system_ready"]
            
            end_time = datetime.now()
            preparation_time = (end_time - start_time).total_seconds()
            
            result = {
                "success": True,
                "system_ready": self.system_ready,
                "preparation_time": preparation_time,
                "dataset_generation": generation_results,
                "clustering_results": clustering_results,
                "final_stats": self.check_system_status()
            }
            
            logger.info(f"System preparation completed in {preparation_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"System preparation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "system_ready": False
            }
    
    def answer_question(self, question: str, n_demonstrations: int = MAX_DEMONSTRATIONS) -> QAResult:
        """Answer a question using the Self-Prompting methodology"""
        start_time = datetime.now()
        
        try:
            # Check if system is ready
            if not self.system_ready:
                status = self.check_system_status()
                if not status["system_ready"]:
                    # Try offline QA even if system not fully ready
                    logger.info("System not fully ready, trying offline QA")
                    offline_result = self.offline_qa.answer_question(question, n_demonstrations)

                    if offline_result.get('error'):
                        return QAResult(
                            question=question,
                            answer="",
                            error="System not ready. Please run system preparation first."
                        )

                    # Calculate processing time
                    end_time = datetime.now()
                    processing_time = (end_time - start_time).total_seconds()

                    return QAResult(
                        question=question,
                        answer=offline_result['answer'],
                        explanation=offline_result['explanation'],
                        confidence=offline_result['confidence'],
                        demonstrations_used=offline_result['demonstrations_used'],
                        processing_time=processing_time
                    )
                self.system_ready = True
            
            logger.info(f"Answering question: {question}")
            
            # Step 1: Select demonstrations using clustering-based retrieval
            demonstrations = self.clustering.select_demonstrations(question, n_demonstrations)
            
            if not demonstrations:
                return QAResult(
                    question=question,
                    answer="",
                    error="No suitable demonstrations found."
                )
            
            logger.info(f"Selected {len(demonstrations)} demonstrations")
            
            # Step 2: Format demonstrations for in-context learning
            demo_dicts = []
            for demo in demonstrations:
                demo_dicts.append({
                    "question": demo.question,
                    "answer": demo.answer,
                    "explanation": demo.explanation
                })
            
            # Step 3: Generate answer using Gemini with demonstrations
            answer_response = self.gemini.answer_with_context(question, demo_dicts)

            if not answer_response:
                # Fallback to offline QA when API fails
                logger.info("API failed, falling back to offline QA")
                offline_result = self.offline_qa.answer_question(question, n_demonstrations)

                if offline_result.get('error'):
                    return QAResult(
                        question=question,
                        answer="",
                        error=f"API failed and offline fallback error: {offline_result['error']}"
                    )

                # Calculate processing time
                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()

                return QAResult(
                    question=question,
                    answer=offline_result['answer'],
                    explanation=offline_result['explanation'],
                    confidence=offline_result['confidence'],
                    demonstrations_used=offline_result['demonstrations_used'],
                    processing_time=processing_time
                )
            
            # Parse the response to extract answer and explanation
            answer, explanation = self.parse_answer_response(answer_response)
            
            # Calculate processing time
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            # Create result
            result = QAResult(
                question=question,
                answer=answer,
                explanation=explanation,
                confidence=self.estimate_confidence(demonstrations, answer),
                demonstrations_used=len(demonstrations),
                processing_time=processing_time
            )
            
            logger.info(f"Question answered successfully in {processing_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            return QAResult(
                question=question,
                answer="",
                error=str(e),
                processing_time=processing_time
            )
    
    def parse_answer_response(self, response: str) -> Tuple[str, Optional[str]]:
        """Parse the Gemini response to extract answer and explanation"""
        lines = response.strip().split('\n')
        
        answer = ""
        explanation = None
        
        # Look for explanation in the response
        for i, line in enumerate(lines):
            line = line.strip()
            
            if not answer and line:
                # First non-empty line is likely the answer
                answer = line
            elif line.lower().startswith(('because', 'explanation:', 'since', 'as')):
                # Found explanation
                explanation = line
                break
            elif i > 0 and line and not answer:
                # Second line might be explanation
                explanation = line
                break
        
        # Clean up answer
        if answer.lower().startswith('answer:'):
            answer = answer[7:].strip()
        
        # Clean up explanation
        if explanation and explanation.lower().startswith('explanation:'):
            explanation = explanation[12:].strip()
        
        return answer, explanation
    
    def estimate_confidence(self, demonstrations: List[QAPair], answer: str) -> float:
        """Estimate confidence based on demonstration similarity and answer quality"""
        if not demonstrations or not answer:
            return 0.0
        
        # Simple confidence estimation based on:
        # 1. Number of demonstrations used
        # 2. Answer length (not too short, not too long)
        # 3. Basic quality indicators
        
        confidence = 0.5  # Base confidence
        
        # Boost confidence based on number of demonstrations
        demo_boost = min(len(demonstrations) / MAX_DEMONSTRATIONS, 1.0) * 0.3
        confidence += demo_boost
        
        # Adjust based on answer quality
        answer_words = len(answer.split())
        if 1 <= answer_words <= 10:  # Reasonable length
            confidence += 0.2
        elif answer_words > 20:  # Too long, might be uncertain
            confidence -= 0.1
        
        # Ensure confidence is between 0 and 1
        return max(0.0, min(1.0, confidence))
    
    def get_sample_questions(self) -> List[str]:
        """Get sample questions from the generated dataset"""
        qa_pairs = self.db.get_qa_pairs(limit=10)
        return [qa.question for qa in qa_pairs]
    
    def get_dataset_sample(self, topic: Optional[str] = None, limit: int = 5) -> List[Dict[str, str]]:
        """Get a sample of the generated dataset"""
        qa_pairs = self.db.get_qa_pairs(topic=topic, limit=limit)
        
        return [
            {
                "topic": qa.topic,
                "question": qa.question,
                "answer": qa.answer,
                "explanation": qa.explanation
            }
            for qa in qa_pairs
        ]
