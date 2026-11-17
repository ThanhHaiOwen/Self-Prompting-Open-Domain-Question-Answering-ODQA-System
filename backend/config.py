"""
Configuration module for Self-Prompting ODQA System
Based on the research paper's specifications
"""

import os
from typing import Dict, List
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "../data/self_prompting.db")

# System Configuration
MAX_DEMONSTRATIONS = int(os.getenv("MAX_DEMONSTRATIONS", "10"))
DEFAULT_CLUSTERS = int(os.getenv("DEFAULT_CLUSTERS", "10"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))

# Generation Configuration
TOTAL_EXAMPLES_PER_TOPIC = int(os.getenv("TOTAL_EXAMPLES_PER_TOPIC", "100"))
MAX_QA_PAIRS_PER_PASSAGE = int(os.getenv("MAX_QA_PAIRS_PER_PASSAGE", "10"))

# Topic definitions from the paper (Table 9 in Appendix B)
TOPICS_CONFIG: Dict[str, int] = {
    "politician": 100,
    "athlete": 40,
    "sportsteam": 40,
    "sportsevent": 40,
    "country": 40,
    "city": 60,
    "historicalfigure": 50,
    "historicalevent": 50,
    "war": 40,
    "religion": 20,
    "singer": 50,
    "song": 50,
    "actororactress": 50,
    "movieorTVseries": 50,
    "writer": 30,
    "book": 30,
    "painter": 30,
    "painting": 30,
    "composer": 30,
    "classicalmusic": 30,
    "touristattraction": 100,
    "scientist": 40,
    "scientificterm": 40,
    "videogame": 40,
    "company": 40,
    "invention": 30,
    "food": 30,
    "animal": 30,
    "plant": 30
}

# High-level theme categorization
THEME_CATEGORIES = {
    "politics": ["politician"],
    "sports": ["athlete", "sportsteam", "sportsevent"],
    "geography": ["country", "city", "touristattraction"],
    "history": ["historicalfigure", "historicalevent", "war"],
    "religion": ["religion"],
    "entertainment": ["singer", "song", "actororactress", "movieorTVseries"],
    "literature": ["writer", "book"],
    "art": ["painter", "painting", "composer", "classicalmusic"],
    "science": ["scientist", "scientificterm"],
    "technology": ["videogame", "company", "invention"],
    "nature": ["food", "animal", "plant"]
}

# Prompt templates based on the paper's methodology
PROMPT_TEMPLATES = {
    "list_examples": "List some {topic}:",
    "generate_passage": "This is a passage from Wikipedia about the {topic}, {example}:",
    "extract_entities": "Here is a passage: {passage} Extract the named entities in it:",
    "generate_question": "{passage} {entity} is the answer to the question:",
    "double_check": "Based on this passage: {passage}\nQuestion: {question}\nWhat is the answer?",
    "generate_explanation": "Passage: {passage} Question: {question} Answer: {answer} You can refer to the passage and write a short explanation to this Question-Answer pair:",
    "final_qa": "Question: {question}\nAnswer: {answer}\nExplanation: {explanation}"
}

# Sentence transformer model for embeddings (using all-MiniLM-L6-v2 for lightweight memory < 200MB)
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

# Filtering criteria
MAX_ANSWER_WORDS = 5
BANNED_PRONOUNS = ["they", "he", "she", "it", "them", "him", "her"]
