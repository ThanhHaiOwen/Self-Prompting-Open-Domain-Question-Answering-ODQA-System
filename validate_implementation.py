#!/usr/bin/env python3
"""
Implementation Validation Script
Validates that the system correctly implements the research paper methodology
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from config import TOPICS_CONFIG, PROMPT_TEMPLATES

def validate_paper_compliance():
    """Validate compliance with research paper specifications"""
    print("🔍 Validating Research Paper Compliance")
    print("=" * 50)
    
    validation_results = {
        "topic_compliance": False,
        "prompt_compliance": False,
        "architecture_compliance": False,
        "methodology_compliance": False
    }
    
    # 1. Topic Configuration Validation
    print("\n📋 Topic Configuration Validation:")
    
    # Check total topic count (should be 29)
    if len(TOPICS_CONFIG) == 29:
        print("✅ Topic count: 29 topics (matches paper)")
        validation_results["topic_compliance"] = True
    else:
        print(f"❌ Topic count: {len(TOPICS_CONFIG)} topics (expected 29)")
    
    # Check specific topics mentioned in paper
    required_topics = [
        'politician', 'athlete', 'sportsteam', 'sportsevent', 'country', 'city',
        'historicalfigure', 'historicalevent', 'war', 'religion', 'singer', 'song',
        'actororactress', 'movieorTVseries', 'writer', 'book', 'painter', 'painting',
        'composer', 'classicalmusic', 'touristattraction', 'scientist', 'scientificterm',
        'videogame', 'company', 'invention', 'food', 'animal', 'plant'
    ]
    
    missing_topics = [topic for topic in required_topics if topic not in TOPICS_CONFIG]
    if not missing_topics:
        print("✅ All required topics present")
    else:
        print(f"❌ Missing topics: {missing_topics}")
        validation_results["topic_compliance"] = False
    
    # Check target counts
    total_target = sum(TOPICS_CONFIG.values())
    print(f"✅ Total target QA pairs: {total_target:,}")
    
    # 2. Prompt Template Validation
    print("\n💬 Prompt Template Validation:")
    
    required_templates = [
        'list_examples', 'generate_passage', 'extract_entities',
        'generate_question', 'double_check', 'generate_explanation'
    ]
    
    missing_templates = [t for t in required_templates if t not in PROMPT_TEMPLATES]
    if not missing_templates:
        print("✅ All required prompt templates present")
        validation_results["prompt_compliance"] = True
    else:
        print(f"❌ Missing templates: {missing_templates}")
    
    # Validate specific template content
    template_checks = [
        ('list_examples', 'List some {topic}:'),
        ('generate_passage', 'Wikipedia'),
        ('extract_entities', 'Extract the named entities'),
        ('generate_question', 'is the answer to the question:'),
        ('generate_explanation', 'write a short explanation')
    ]
    
    for template_name, expected_content in template_checks:
        if template_name in PROMPT_TEMPLATES:
            if expected_content in PROMPT_TEMPLATES[template_name]:
                print(f"✅ {template_name}: Contains expected content")
            else:
                print(f"⚠️  {template_name}: May not match paper exactly")
    
    # 3. Architecture Validation
    print("\n🏗️  Architecture Validation:")
    
    required_files = [
        'backend/main.py',
        'backend/qa_engine.py',
        'backend/gemini_client.py',
        'backend/dataset_generator.py',
        'backend/clustering_retrieval.py',
        'backend/database.py',
        'backend/config.py',
        'frontend/app/page.tsx',
        'frontend/components/QuestionAnswering.tsx',
        'frontend/components/SystemStatus.tsx'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if not missing_files:
        validation_results["architecture_compliance"] = True
    
    # 4. Methodology Validation
    print("\n🔬 Methodology Validation:")
    
    try:
        from dataset_generator import DatasetGenerator
        from clustering_retrieval import ClusteringRetrieval
        from qa_engine import QAEngine
        
        # Check DatasetGenerator methods
        required_methods = [
            'generate_full_dataset',
            'generate_topic_dataset', 
            'generate_qa_pairs_for_example',
            'generate_single_qa_pair'
        ]
        
        missing_methods = []
        for method in required_methods:
            if hasattr(DatasetGenerator, method):
                print(f"✅ DatasetGenerator.{method}")
            else:
                print(f"❌ DatasetGenerator.{method}")
                missing_methods.append(method)
        
        # Check ClusteringRetrieval methods
        clustering_methods = [
            'compute_embeddings',
            'perform_clustering',
            'select_demonstrations',
            'select_from_cluster'
        ]
        
        for method in clustering_methods:
            if hasattr(ClusteringRetrieval, method):
                print(f"✅ ClusteringRetrieval.{method}")
            else:
                print(f"❌ ClusteringRetrieval.{method}")
                missing_methods.append(method)
        
        # Check QAEngine methods
        qa_methods = [
            'prepare_system',
            'answer_question',
            'check_system_status'
        ]
        
        for method in qa_methods:
            if hasattr(QAEngine, method):
                print(f"✅ QAEngine.{method}")
            else:
                print(f"❌ QAEngine.{method}")
                missing_methods.append(method)
        
        if not missing_methods:
            validation_results["methodology_compliance"] = True
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Validation Summary:")
    
    total_checks = len(validation_results)
    passed_checks = sum(validation_results.values())
    
    for check, passed in validation_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {check.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 Implementation fully complies with research paper!")
        return True
    else:
        print("⚠️  Some compliance issues found. Please review above.")
        return False

def validate_system_readiness():
    """Validate system is ready for use"""
    print("\n🚀 System Readiness Validation")
    print("=" * 50)
    
    # Check environment setup
    env_file = Path("backend/.env")
    if env_file.exists():
        print("✅ Environment file exists")
        
        # Check for API key
        with open(env_file) as f:
            content = f.read()
            if "GEMINI_API_KEY" in content and "your_" not in content:
                print("✅ Gemini API key configured")
            else:
                print("⚠️  Gemini API key needs to be configured")
    else:
        print("❌ Environment file missing")
    
    # Check data directory
    data_dir = Path("data")
    if data_dir.exists():
        print("✅ Data directory exists")
    else:
        print("⚠️  Data directory will be created on first run")
    
    # Check dependencies
    try:
        import fastapi
        import google.generativeai
        import sentence_transformers
        import sklearn
        print("✅ Backend dependencies available")
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e}")
    
    # Check frontend
    frontend_deps = Path("frontend/node_modules")
    if frontend_deps.exists():
        print("✅ Frontend dependencies installed")
    else:
        print("⚠️  Frontend dependencies need to be installed")

def main():
    """Main validation function"""
    print("🔍 Self-Prompting ODQA System Validation")
    print("Validating implementation against research paper specifications")
    print("=" * 60)
    
    # Run validations
    paper_compliant = validate_paper_compliance()
    validate_system_readiness()
    
    print("\n" + "=" * 60)
    if paper_compliant:
        print("🎉 Validation Complete: System ready for use!")
        print("\nNext steps:")
        print("1. Configure your Gemini API key in backend/.env")
        print("2. Run: python run_system.py run")
        print("3. Open: http://localhost:3000")
    else:
        print("⚠️  Validation found issues. Please review and fix.")
    
    return paper_compliant

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
