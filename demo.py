#!/usr/bin/env python3
"""
Interactive Demo for Self-Prompting ODQA System
Demonstrates the complete system functionality
"""

import sys
import os
import time
import json
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from qa_engine import QAEngine
from config import TOPICS_CONFIG

def print_header():
    """Print demo header"""
    print("=" * 60)
    print("🧠 Self-Prompting ODQA System - Interactive Demo")
    print("=" * 60)
    print("Implementation of 'Self-Prompting Large Language Models")
    print("for Zero-Shot Open-Domain QA' using Google Gemini API")
    print("=" * 60)
    print()

def print_system_info():
    """Print system information"""
    print("📊 System Configuration:")
    print(f"   • Topics: {len(TOPICS_CONFIG)} categories")
    print(f"   • Target QA Pairs: {sum(TOPICS_CONFIG.values()):,}")
    print(f"   • AI Model: Google Gemini Pro")
    print(f"   • Methodology: Faithful paper implementation")
    print()

def check_system_status(engine):
    """Check and display system status"""
    print("🔍 Checking System Status...")
    status = engine.check_system_status()
    
    print(f"   • System Ready: {'✅' if status['system_ready'] else '❌'}")
    print(f"   • Dataset: {status['dataset_stats']['total_pairs']:,} QA pairs")
    print(f"   • Clusters: {status['clustering_stats']['n_clusters']}")
    print(f"   • Components: {sum(status['components_status'].values())}/4 ready")
    print()
    
    return status['system_ready']

def prepare_system_interactive(engine):
    """Interactive system preparation"""
    print("🚀 System Preparation Required")
    print("This will generate the pseudo QA dataset and prepare clustering.")
    print("⏱️  Estimated time: 10-30 minutes (depending on API limits)")
    print()
    
    choice = input("Proceed with system preparation? (y/N): ").strip().lower()
    if choice != 'y':
        print("System preparation cancelled. Demo cannot continue without preparation.")
        return False
    
    print("\n🔄 Starting system preparation...")
    print("This process includes:")
    print("   1. Generating Wikipedia-style passages for 29 topics")
    print("   2. Extracting named entities from passages")
    print("   3. Creating questions for extracted entities")
    print("   4. Generating explanations for QA pairs")
    print("   5. Computing embeddings and clustering")
    print()
    
    start_time = time.time()
    
    try:
        result = engine.prepare_system()
        
        if result['success']:
            elapsed = time.time() - start_time
            print(f"✅ System preparation completed in {elapsed:.1f} seconds!")
            print(f"   • Generated: {result['final_stats']['dataset_stats']['total_pairs']:,} QA pairs")
            print(f"   • Clusters: {result['final_stats']['clustering_stats']['n_clusters']}")
            print()
            return True
        else:
            print(f"❌ System preparation failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ System preparation failed: {e}")
        return False

def demo_question_answering(engine):
    """Demonstrate question answering capabilities"""
    print("💬 Question Answering Demo")
    print("Ask any open-domain question and see the Self-Prompting system in action!")
    print()
    
    # Sample questions from different domains
    sample_questions = [
        "Who was the first person to walk on the moon?",
        "What is the capital of France?",
        "When was the Declaration of Independence signed?",
        "Who wrote Romeo and Juliet?",
        "What is the largest planet in our solar system?",
        "Who painted the Mona Lisa?",
        "What year did World War II end?",
        "Who invented the telephone?",
        "What is the highest mountain in the world?",
        "Who was the first President of the United States?"
    ]
    
    print("📝 Sample questions you can try:")
    for i, q in enumerate(sample_questions[:5], 1):
        print(f"   {i}. {q}")
    print("   ... or ask your own question!")
    print()
    
    while True:
        print("-" * 50)
        question = input("🤔 Your question (or 'quit' to exit): ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if not question:
            continue
        
        print(f"\n🔍 Processing: {question}")
        print("   • Selecting relevant demonstrations...")
        print("   • Applying clustering-based retrieval...")
        print("   • Generating answer with in-context learning...")
        
        start_time = time.time()
        
        try:
            result = engine.answer_question(question)
            elapsed = time.time() - start_time
            
            if result.error:
                print(f"❌ Error: {result.error}")
                continue
            
            print(f"\n✅ Answer generated in {elapsed:.2f} seconds")
            print("=" * 50)
            print(f"❓ Question: {result.question}")
            print(f"💡 Answer: {result.answer}")
            
            if result.explanation:
                print(f"📖 Explanation: {result.explanation}")
            
            print(f"🎯 Confidence: {result.confidence:.1%}")
            print(f"📊 Demonstrations used: {result.demonstrations_used}")
            print(f"⏱️  Processing time: {result.processing_time:.2f}s")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
        
        print()

def show_dataset_sample(engine):
    """Show sample of generated dataset"""
    print("📚 Generated Dataset Sample")
    print("Here are some examples of the automatically generated QA pairs:")
    print()
    
    try:
        samples = engine.get_dataset_sample(limit=3)
        
        for i, sample in enumerate(samples, 1):
            print(f"Example {i}:")
            print(f"   Topic: {sample['topic']}")
            print(f"   Question: {sample['question']}")
            print(f"   Answer: {sample['answer']}")
            print(f"   Explanation: {sample['explanation'][:100]}...")
            print()
            
    except Exception as e:
        print(f"Error retrieving dataset sample: {e}")

def show_methodology_info():
    """Show information about the methodology"""
    print("🔬 Methodology Information")
    print("This system implements the exact methodology from the research paper:")
    print()
    print("📋 Preparation Stage (4 steps):")
    print("   1. Passage Generation - Create Wikipedia-style passages")
    print("   2. Named Entity Recognition - Extract entities using LLM")
    print("   3. Question Generation - Create questions for entities")
    print("   4. Explanation Generation - Add explanations for QA pairs")
    print()
    print("🎯 Inference Stage:")
    print("   1. Clustering-based Retrieval - Select diverse demonstrations")
    print("   2. In-context Learning - Use demonstrations for final answer")
    print()
    print("🔧 Key Features:")
    print("   • Zero-shot learning (no training data required)")
    print("   • Explainable answers with confidence estimation")
    print("   • Dynamic demonstration selection")
    print("   • Faithful implementation of paper methodology")
    print()

def main():
    """Main demo function"""
    print_header()
    print_system_info()
    show_methodology_info()
    
    # Initialize QA engine
    print("🔧 Initializing QA Engine...")
    try:
        engine = QAEngine()
        print("✅ QA Engine initialized successfully")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize QA Engine: {e}")
        print("Please check your configuration and API key.")
        return
    
    # Check system status
    system_ready = check_system_status(engine)
    
    # Prepare system if needed
    if not system_ready:
        if not prepare_system_interactive(engine):
            return
    
    # Show dataset sample
    show_dataset_sample(engine)
    
    # Main demo loop
    demo_question_answering(engine)
    
    print("\n🎉 Demo completed!")
    print("Thank you for trying the Self-Prompting ODQA System!")
    print("For more information, see the research paper:")
    print("https://arxiv.org/abs/2212.08029")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check your configuration and try again.")
