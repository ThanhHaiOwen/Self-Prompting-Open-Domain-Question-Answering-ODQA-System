"""
Google Gemini API client for Self-Prompting ODQA System
Replaces GPT-3/InstructGPT while maintaining exact prompting methodology
"""

import google.generativeai as genai
import time
import logging
from typing import List, Optional, Dict, Any
import re

from config import GEMINI_API_KEY, TEMPERATURE, MAX_TOKENS, BANNED_PRONOUNS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        """Initialize Gemini client"""
        genai.configure(api_key=api_key)
        
        # Configure the model
        self.generation_config = {
            "temperature": TEMPERATURE,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": MAX_TOKENS,
        }
        
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        logger.info("Gemini client initialized successfully")
    
    def generate_text(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Generate text using Gemini API with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                
                if response.text:
                    return response.text.strip()
                else:
                    logger.warning(f"Empty response from Gemini API (attempt {attempt + 1})")
                    
            except Exception as e:
                logger.error(f"Error calling Gemini API (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                
        logger.error(f"Failed to get response from Gemini API after {max_retries} attempts")
        return None
    
    def list_examples(self, topic: str, count: int = 10) -> List[str]:
        """Generate examples for a given topic"""
        prompt = f"List {count} specific examples of {topic}. Provide only the names, one per line:"
        
        response = self.generate_text(prompt)
        if not response:
            return []
        
        # Parse the response into individual examples
        examples = []
        for line in response.split('\n'):
            line = line.strip()
            # Remove numbering, bullets, or other formatting
            line = re.sub(r'^\d+\.?\s*', '', line)
            line = re.sub(r'^[-*•]\s*', '', line)
            if line and len(line) > 2:
                examples.append(line)
        
        return examples[:count]
    
    def generate_passage(self, topic: str, example: str) -> Optional[str]:
        """Generate a Wikipedia-style passage for a topic and example"""
        prompt = f"""This is a passage from Wikipedia about the {topic}, {example}:

Write a comprehensive, factual Wikipedia-style paragraph about {example}. Include specific details, dates, and relevant information that would be found in an encyclopedia entry. Make it informative and well-structured."""
        
        response = self.generate_text(prompt)
        return response
    
    def extract_entities(self, passage: str) -> List[str]:
        """Extract named entities from a passage"""
        prompt = f"""Here is a passage: {passage}

Extract the named entities in it. Focus on:
- Person names
- Place names  
- Organization names
- Dates and years
- Specific terms and proper nouns

List only the entities, one per line:"""
        
        response = self.generate_text(prompt)
        if not response:
            return []
        
        # Parse entities
        entities = []
        for line in response.split('\n'):
            line = line.strip()
            # Remove formatting
            line = re.sub(r'^\d+\.?\s*', '', line)
            line = re.sub(r'^[-*•]\s*', '', line)
            if line and len(line) > 1:
                entities.append(line)
        
        return entities
    
    def generate_question(self, passage: str, entity: str) -> Optional[str]:
        """Generate a question for which the entity is the answer"""
        prompt = f"""{passage}

{entity} is the answer to the question:"""
        
        response = self.generate_text(prompt)
        if response:
            # Clean up the question
            question = response.strip()
            if not question.endswith('?'):
                question += '?'
            return question
        return None
    
    def double_check_answer(self, passage: str, question: str) -> Optional[str]:
        """Double-check if the question can be answered from the passage"""
        prompt = f"""Based on this passage: {passage}

Question: {question}
What is the answer?"""
        
        response = self.generate_text(prompt)
        return response.strip() if response else None
    
    def generate_explanation(self, passage: str, question: str, answer: str) -> Optional[str]:
        """Generate an explanation for a QA pair"""
        prompt = f"""Passage: {passage}
Question: {question}
Answer: {answer}

You can refer to the passage and write a short explanation to this Question-Answer pair:"""
        
        response = self.generate_text(prompt)
        return response.strip() if response else None
    
    def answer_with_context(self, question: str, demonstrations: List[Dict[str, str]]) -> Optional[str]:
        """Answer a question using in-context learning with demonstrations"""
        # Build the prompt with demonstrations
        prompt_parts = []
        
        # Add demonstrations in QAE format
        for demo in demonstrations:
            prompt_parts.append(f"Question: {demo['question']}")
            prompt_parts.append(f"Answer: {demo['answer']}")
            prompt_parts.append(f"Explanation: {demo['explanation']}")
            prompt_parts.append("")  # Empty line between demonstrations
        
        # Add the test question
        prompt_parts.append(f"Question: {question}")
        prompt_parts.append("Answer:")
        
        prompt = "\n".join(prompt_parts)
        
        response = self.generate_text(prompt)
        return response.strip() if response else None
    
    def filter_question_quality(self, question: str) -> bool:
        """Filter out low-quality questions based on paper criteria"""
        question_lower = question.lower()
        
        # Check for banned pronouns that make questions ambiguous
        for pronoun in BANNED_PRONOUNS:
            if pronoun.lower() in question_lower:
                return False
        
        # Basic quality checks
        if len(question.split()) < 3:  # Too short
            return False
        
        if not question.strip().endswith('?'):  # Not a proper question
            return False
        
        return True
    
    def normalize_answer(self, answer: str) -> str:
        """Normalize answer format"""
        if not answer:
            return ""
        
        # Remove extra whitespace
        answer = answer.strip()
        
        # Handle multiple entities (take first one as per paper)
        if ',' in answer:
            answer = answer.split(',')[0].strip()
        
        return answer
