#!/usr/bin/env python3
"""
Offline Question Answering System
Provides answers without requiring API calls by using similarity matching
"""

import sys
sys.path.append('.')
from database import DatabaseManager, QAPair
from clustering_retrieval import ClusteringRetrieval
import numpy as np
from typing import List, Dict, Optional
import logging
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class OfflineQAEngine:
    """Question answering engine that works without API calls"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.clustering = ClusteringRetrieval(self.db)
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            self.model = SentenceTransformer('all-mpnet-base-v2')
            logger.info("Sentence transformer model loaded for offline QA")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer model: {e}")
    
    def find_best_match(self, question: str, top_k: int = 5) -> List[Dict]:
        """Find the best matching QA pairs for a given question"""
        if not self.model:
            return []
        
        # Get all QA pairs
        qa_pairs = self.db.get_qa_pairs()
        if not qa_pairs:
            return []
        
        # Encode the input question
        question_embedding = self.model.encode([question])
        
        # Get embeddings for all QA pairs
        qa_embeddings = []
        valid_qa_pairs = []
        
        for qa_pair in qa_pairs:
            if qa_pair.embedding is not None:
                # Convert bytes back to numpy array
                embedding = np.frombuffer(qa_pair.embedding, dtype=np.float32)
                qa_embeddings.append(embedding)
                valid_qa_pairs.append(qa_pair)
            else:
                # Compute embedding on the fly if missing
                try:
                    embedding = self.model.encode([qa_pair.question])
                    qa_embeddings.append(embedding[0])
                    valid_qa_pairs.append(qa_pair)
                except Exception as e:
                    logger.warning(f"Failed to compute embedding for QA pair {qa_pair.id}: {e}")
        
        if not qa_embeddings:
            return []
        
        # Calculate similarities
        qa_embeddings = np.array(qa_embeddings)
        similarities = cosine_similarity(question_embedding, qa_embeddings)[0]
        
        # Get top-k most similar QA pairs
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            qa_pair = valid_qa_pairs[idx]
            similarity = similarities[idx]
            
            results.append({
                'qa_pair': qa_pair,
                'similarity': float(similarity),
                'confidence': float(similarity)  # Use similarity as confidence
            })
        
        return results
    
    def answer_question(self, question: str, n_demonstrations: int = 5) -> Dict:
        """Answer a question using offline matching"""
        try:
            # Find best matches
            matches = self.find_best_match(question, top_k=n_demonstrations)
            
            if not matches:
                return {
                    'question': question,
                    'answer': '',
                    'explanation': '',
                    'confidence': 0.0,
                    'demonstrations_used': 0,
                    'processing_time': 0.0,
                    'error': 'No matching QA pairs found in database'
                }
            
            # Use the best match as the answer
            best_match = matches[0]
            qa_pair = best_match['qa_pair']
            confidence = best_match['confidence']
            
            # If confidence is high enough, return the answer
            if confidence > 0.5:  # Threshold for accepting an answer
                return {
                    'question': question,
                    'answer': qa_pair.answer,
                    'explanation': qa_pair.explanation,
                    'confidence': confidence,
                    'demonstrations_used': len(matches),
                    'processing_time': 0.1,
                    'error': None,
                    'method': 'offline_similarity_matching',
                    'best_match_question': qa_pair.question,
                    'similarity_score': confidence
                }
            else:
                return {
                    'question': question,
                    'answer': '',
                    'explanation': '',
                    'confidence': 0.0,
                    'demonstrations_used': 0,
                    'processing_time': 0.1,
                    'error': f'No sufficiently similar question found (best similarity: {confidence:.3f})'
                }
                
        except Exception as e:
            logger.error(f"Error in offline question answering: {e}")
            return {
                'question': question,
                'answer': '',
                'explanation': '',
                'confidence': 0.0,
                'demonstrations_used': 0,
                'processing_time': 0.0,
                'error': f'Offline QA error: {str(e)}'
            }
    
    def get_similar_questions(self, question: str, top_k: int = 5) -> List[Dict]:
        """Get similar questions from the database"""
        matches = self.find_best_match(question, top_k=top_k)
        
        similar_questions = []
        for match in matches:
            qa_pair = match['qa_pair']
            similar_questions.append({
                'question': qa_pair.question,
                'answer': qa_pair.answer,
                'similarity': match['similarity'],
                'topic': qa_pair.topic,
                'example': qa_pair.example
            })
        
        return similar_questions

def test_offline_qa():
    """Test the offline QA system"""
    print("Testing Offline QA System...")
    
    offline_qa = OfflineQAEngine()
    
    test_questions = [
        "Who painted the Mona Lisa?",
        "What is the capital of Japan?",
        "Who was the first woman to win a Nobel Prize?",
        "Who invented the World Wide Web?",
        "What is the highest mountain in the world?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        result = offline_qa.answer_question(question)
        
        if result['error']:
            print(f"Error: {result['error']}")
        else:
            print(f"Answer: {result['answer']}")
            print(f"Explanation: {result['explanation']}")
            print(f"Confidence: {result['confidence']:.3f}")
            if 'similarity_score' in result:
                print(f"Similarity: {result['similarity_score']:.3f}")

if __name__ == "__main__":
    test_offline_qa()
