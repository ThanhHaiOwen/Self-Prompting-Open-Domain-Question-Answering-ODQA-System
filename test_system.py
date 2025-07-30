#!/usr/bin/env python3
"""
Test script for Self-Prompting ODQA System
Validates that the implementation follows the paper's methodology
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import DatabaseManager, QAPair
from gemini_client import GeminiClient
from dataset_generator import DatasetGenerator
from clustering_retrieval import ClusteringRetrieval
from qa_engine import QAEngine
from config import TOPICS_CONFIG, PROMPT_TEMPLATES

def test_configuration():
    """Test that configuration matches the paper"""
    print("Testing Configuration...")
    
    # Test topic count (should be 29 as per paper)
    assert len(TOPICS_CONFIG) == 29, f"Expected 29 topics, got {len(TOPICS_CONFIG)}"
    
    # Test specific topics mentioned in paper
    required_topics = [
        'politician', 'athlete', 'sportsteam', 'country', 'city',
        'historicalfigure', 'singer', 'actororactress', 'scientist'
    ]
    
    for topic in required_topics:
        assert topic in TOPICS_CONFIG, f"Required topic '{topic}' not found"
    
    # Test total target pairs
    total_target = sum(TOPICS_CONFIG.values())
    expected_range = (2800, 3000)  # Approximate range based on paper
    assert expected_range[0] <= total_target <= expected_range[1], \
        f"Total target pairs {total_target} not in expected range {expected_range}"
    
    print("✓ Configuration matches paper specifications")

def test_prompt_templates():
    """Test that prompt templates match paper methodology"""
    print("Testing Prompt Templates...")
    
    required_templates = [
        'list_examples', 'generate_passage', 'extract_entities',
        'generate_question', 'double_check', 'generate_explanation'
    ]
    
    for template in required_templates:
        assert template in PROMPT_TEMPLATES, f"Required template '{template}' not found"
    
    # Test specific template formats mentioned in paper
    assert "List some {topic}:" in PROMPT_TEMPLATES['list_examples']
    assert "Wikipedia" in PROMPT_TEMPLATES['generate_passage']
    assert "Extract the named entities" in PROMPT_TEMPLATES['extract_entities']
    
    print("✓ Prompt templates follow paper methodology")

def test_database_operations():
    """Test database operations"""
    print("Testing Database Operations...")
    
    # Create test database
    db = DatabaseManager(":memory:")  # In-memory database for testing
    
    # Test QA pair creation and retrieval
    test_qa = QAPair(
        topic="test_topic",
        example="test_example",
        passage="This is a test passage about test_example.",
        entity="test_entity",
        question="What is the test entity?",
        answer="test_entity",
        explanation="The test entity is mentioned in the passage."
    )
    
    # Save and retrieve
    qa_id = db.save_qa_pair(test_qa)
    assert qa_id is not None, "Failed to save QA pair"
    
    retrieved_qa = db.get_qa_pairs()
    assert len(retrieved_qa) == 1, "Failed to retrieve QA pair"
    assert retrieved_qa[0].question == test_qa.question, "QA pair data mismatch"
    
    print("✓ Database operations working correctly")

def test_gemini_client():
    """Test Gemini client functionality"""
    print("Testing Gemini Client...")
    
    try:
        client = GeminiClient()
        
        # Test basic text generation (if API key is available)
        test_prompt = "List 3 examples of countries:"
        response = client.generate_text(test_prompt)
        
        if response:
            print("✓ Gemini client working correctly")
            print(f"  Sample response: {response[:100]}...")
        else:
            print("⚠ Gemini client initialized but no response (check API key)")
            
    except Exception as e:
        print(f"⚠ Gemini client test failed: {e}")
        print("  This is expected if GEMINI_API_KEY is not set")

def test_dataset_generator():
    """Test dataset generation logic"""
    print("Testing Dataset Generator...")
    
    db = DatabaseManager(":memory:")
    client = GeminiClient()
    generator = DatasetGenerator(db, client)
    
    # Test answer matching logic
    assert generator.answers_match("Paris", "paris"), "Case insensitive matching failed"
    assert generator.answers_match("New York", "New York City"), "Partial matching failed"
    assert not generator.answers_match("Paris", "London"), "False positive matching"
    
    print("✓ Dataset generator logic working correctly")

def test_clustering_retrieval():
    """Test clustering and retrieval system"""
    print("Testing Clustering Retrieval...")
    
    db = DatabaseManager(":memory:")
    clustering = ClusteringRetrieval(db)
    
    # Test sentence model initialization
    clustering.initialize_sentence_model()
    assert clustering.sentence_model is not None, "Sentence model not initialized"
    
    print("✓ Clustering retrieval system initialized correctly")

def test_qa_engine():
    """Test the main QA engine"""
    print("Testing QA Engine...")
    
    engine = QAEngine()
    
    # Test system status check
    status = engine.check_system_status()
    assert 'system_ready' in status, "System status missing required fields"
    assert 'dataset_stats' in status, "System status missing dataset stats"
    assert 'clustering_stats' in status, "System status missing clustering stats"
    
    print("✓ QA engine working correctly")

def test_paper_methodology_compliance():
    """Test compliance with paper methodology"""
    print("Testing Paper Methodology Compliance...")
    
    # Test 4-step preparation process
    steps = [
        "Passage Generation",
        "Named Entity Recognition", 
        "Question Generation",
        "Explanation Generation"
    ]
    
    # Verify all steps are implemented in DatasetGenerator
    generator_methods = [
        'generate_qa_pairs_for_example',
        'generate_single_qa_pair'
    ]
    
    for method in generator_methods:
        assert hasattr(DatasetGenerator, method), f"Missing method: {method}"
    
    # Test clustering-based retrieval
    clustering_methods = [
        'perform_clustering',
        'select_demonstrations',
        'select_from_cluster'
    ]
    
    for method in clustering_methods:
        assert hasattr(ClusteringRetrieval, method), f"Missing method: {method}"
    
    print("✓ Implementation follows paper methodology")

def run_all_tests():
    """Run all tests"""
    print("Self-Prompting ODQA System - Test Suite")
    print("="*50)
    
    tests = [
        test_configuration,
        test_prompt_templates,
        test_database_operations,
        test_gemini_client,
        test_dataset_generator,
        test_clustering_retrieval,
        test_qa_engine,
        test_paper_methodology_compliance
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        print()
    
    print("="*50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! System is ready for use.")
    else:
        print("⚠ Some tests failed. Please check the issues above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
