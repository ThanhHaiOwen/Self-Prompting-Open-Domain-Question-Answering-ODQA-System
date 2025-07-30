"""
Pseudo QA Dataset Generator for Self-Prompting ODQA System
Implements the 4-step preparation stage from the research paper
"""

import logging
import time
from typing import List, Dict, Optional, Tuple
import random

from config import TOPICS_CONFIG, MAX_QA_PAIRS_PER_PASSAGE, MAX_ANSWER_WORDS
from database import DatabaseManager, QAPair
from gemini_client import GeminiClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetGenerator:
    """Generates pseudo QA dataset following the paper's methodology"""
    
    def __init__(self, db_manager: DatabaseManager, gemini_client: GeminiClient):
        self.db = db_manager
        self.gemini = gemini_client
        self.generated_count = 0
        self.total_target = sum(TOPICS_CONFIG.values())
        
    def generate_full_dataset(self) -> Dict[str, int]:
        """Generate the complete pseudo QA dataset for all topics"""
        logger.info(f"Starting dataset generation for {len(TOPICS_CONFIG)} topics")
        logger.info(f"Target total: {self.total_target} QA pairs")
        
        results = {}
        
        for topic, target_count in TOPICS_CONFIG.items():
            logger.info(f"Generating {target_count} examples for topic: {topic}")
            
            try:
                generated = self.generate_topic_dataset(topic, target_count)
                results[topic] = generated
                logger.info(f"Successfully generated {generated} QA pairs for {topic}")
                
                # Delay to respect free tier rate limits (15 requests/minute)
                time.sleep(5)  # Wait 5 seconds between topics
                
            except Exception as e:
                logger.error(f"Error generating dataset for topic {topic}: {e}")
                results[topic] = 0
        
        total_generated = sum(results.values())
        logger.info(f"Dataset generation complete. Generated {total_generated} total QA pairs")
        
        return results
    
    def generate_topic_dataset(self, topic: str, target_count: int) -> int:
        """Generate QA pairs for a specific topic"""
        generated_count = 0
        attempts = 0
        max_attempts = target_count * 3  # Allow some failures
        
        while generated_count < target_count and attempts < max_attempts:
            attempts += 1
            
            try:
                # Step 1: Get examples for the topic
                examples = self.gemini.list_examples(topic, count=10)
                if not examples:
                    logger.warning(f"No examples generated for topic {topic}")
                    continue
                
                # Process each example
                for example in examples:
                    if generated_count >= target_count:
                        break
                    
                    qa_pairs = self.generate_qa_pairs_for_example(topic, example)
                    
                    for qa_pair in qa_pairs:
                        if generated_count >= target_count:
                            break
                        
                        # Save to database
                        qa_pair_id = self.db.save_qa_pair(qa_pair)
                        generated_count += 1
                        self.generated_count += 1
                        
                        if generated_count % 10 == 0:
                            logger.info(f"Generated {generated_count}/{target_count} for {topic}")
                
            except Exception as e:
                logger.error(f"Error processing topic {topic}, attempt {attempts}: {e}")
                continue
        
        return generated_count
    
    def generate_qa_pairs_for_example(self, topic: str, example: str) -> List[QAPair]:
        """Generate QA pairs for a specific example following the 4-step process"""
        qa_pairs = []
        
        try:
            # Step 1: Generate Wikipedia-style passage
            passage = self.gemini.generate_passage(topic, example)
            if not passage:
                logger.warning(f"Failed to generate passage for {topic}: {example}")
                return qa_pairs

            # Rate limiting delay
            time.sleep(4)  # 4 seconds between API calls for free tier

            # Step 2: Extract named entities
            entities = self.gemini.extract_entities(passage)
            if not entities:
                logger.warning(f"No entities extracted from passage for {example}")
                return qa_pairs
            
            # Limit entities to avoid too many QA pairs per passage
            entities = entities[:MAX_QA_PAIRS_PER_PASSAGE]
            
            # Step 3 & 4: Generate questions and explanations for each entity
            for entity in entities:
                qa_pair = self.generate_single_qa_pair(topic, example, passage, entity)
                if qa_pair:
                    qa_pairs.append(qa_pair)
            
        except Exception as e:
            logger.error(f"Error generating QA pairs for {example}: {e}")
        
        return qa_pairs
    
    def generate_single_qa_pair(self, topic: str, example: str, passage: str, entity: str) -> Optional[QAPair]:
        """Generate a single QA pair with validation"""
        try:
            # Step 3: Generate question
            question = self.gemini.generate_question(passage, entity)
            if not question:
                return None

            # Rate limiting delay
            time.sleep(4)  # 4 seconds between API calls

            # Filter question quality
            if not self.gemini.filter_question_quality(question):
                return None

            # Check answer length (max 5 words as per paper)
            if len(entity.split()) > MAX_ANSWER_WORDS:
                return None

            # Rate limiting delay
            time.sleep(4)  # 4 seconds between API calls

            # Step 4: Double-check by re-answering
            predicted_answer = self.gemini.double_check_answer(passage, question)
            if not predicted_answer:
                return None
            
            # Normalize answers for comparison
            normalized_entity = self.gemini.normalize_answer(entity)
            normalized_predicted = self.gemini.normalize_answer(predicted_answer)
            
            # Check if answers match (basic string similarity)
            if not self.answers_match(normalized_entity, normalized_predicted):
                logger.debug(f"Answer mismatch: expected '{normalized_entity}', got '{normalized_predicted}'")
                return None
            
            # Rate limiting delay
            time.sleep(4)  # 4 seconds between API calls

            # Step 5: Generate explanation
            explanation = self.gemini.generate_explanation(passage, question, entity)
            if not explanation:
                return None
            
            # Create QA pair
            qa_pair = QAPair(
                topic=topic,
                example=example,
                passage=passage,
                entity=entity,
                question=question,
                answer=entity,
                explanation=explanation
            )
            
            return qa_pair
            
        except Exception as e:
            logger.error(f"Error generating single QA pair: {e}")
            return None
    
    def answers_match(self, answer1: str, answer2: str) -> bool:
        """Check if two answers match (with some tolerance)"""
        if not answer1 or not answer2:
            return False
        
        # Exact match
        if answer1.lower() == answer2.lower():
            return True
        
        # Check if one contains the other
        if answer1.lower() in answer2.lower() or answer2.lower() in answer1.lower():
            return True
        
        # Check for partial matches (for complex entities)
        words1 = set(answer1.lower().split())
        words2 = set(answer2.lower().split())
        
        # If there's significant overlap
        if len(words1.intersection(words2)) >= min(len(words1), len(words2)) * 0.5:
            return True
        
        return False
    
    def get_generation_progress(self) -> Dict[str, any]:
        """Get current generation progress"""
        stats = self.db.get_dataset_stats()
        
        return {
            "total_generated": stats["total_pairs"],
            "total_target": self.total_target,
            "progress_percentage": (stats["total_pairs"] / self.total_target) * 100 if self.total_target > 0 else 0,
            "topic_breakdown": stats["topic_counts"]
        }
    
    def resume_generation(self) -> Dict[str, int]:
        """Resume generation for incomplete topics"""
        current_stats = self.db.get_dataset_stats()
        current_counts = current_stats.get("topic_counts", {})
        
        results = {}
        
        for topic, target_count in TOPICS_CONFIG.items():
            current_count = current_counts.get(topic, 0)
            
            if current_count < target_count:
                remaining = target_count - current_count
                logger.info(f"Resuming generation for {topic}: {remaining} remaining")
                
                generated = self.generate_topic_dataset(topic, remaining)
                results[topic] = current_count + generated
            else:
                results[topic] = current_count
        
        return results
