#!/usr/bin/env python3
"""
Comprehensive Test Suite for Self-Prompting ODQA System
Tests the system with diverse questions across all topics
"""

import requests
import json
import time
from datetime import datetime

class ODQATestSuite:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    def ask_question(self, question, n_demonstrations=5):
        """Ask a question to the ODQA system"""
        try:
            response = requests.post(
                f"{self.base_url}/ask",
                json={"question": question, "n_demonstrations": n_demonstrations},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def run_test_batch(self, questions, category):
        """Run a batch of test questions"""
        print(f"\n{'='*60}")
        print(f"TESTING CATEGORY: {category.upper()}")
        print(f"{'='*60}")
        
        batch_results = []
        
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] Testing: {question}")
            
            start_time = time.time()
            result = self.ask_question(question)
            end_time = time.time()
            
            test_result = {
                "category": category,
                "question": question,
                "result": result,
                "test_time": end_time - start_time,
                "timestamp": datetime.now().isoformat()
            }
            
            if result.get("error"):
                print(f"❌ ERROR: {result['error']}")
                test_result["status"] = "ERROR"
            else:
                answer = result.get("answer", "")
                confidence = result.get("confidence", 0)
                explanation = result.get("explanation", "")
                
                print(f"✅ Answer: {answer}")
                print(f"📊 Confidence: {confidence:.3f}")
                print(f"💡 Explanation: {explanation[:100]}...")
                
                test_result["status"] = "SUCCESS"
            
            batch_results.append(test_result)
            self.test_results.append(test_result)
            
            # Small delay between questions
            time.sleep(1)
        
        return batch_results
    
    def generate_test_report(self, filename="test_report.txt"):
        """Generate a comprehensive test report"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("COMPREHENSIVE ODQA SYSTEM TEST REPORT\n")
            f.write("="*50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Tests: {len(self.test_results)}\n\n")
            
            # Summary statistics
            successful_tests = [r for r in self.test_results if r["status"] == "SUCCESS"]
            error_tests = [r for r in self.test_results if r["status"] == "ERROR"]
            
            f.write("SUMMARY STATISTICS\n")
            f.write("-" * 20 + "\n")
            f.write(f"Successful Tests: {len(successful_tests)}\n")
            f.write(f"Failed Tests: {len(error_tests)}\n")
            f.write(f"Success Rate: {len(successful_tests)/len(self.test_results)*100:.1f}%\n\n")
            
            if successful_tests:
                avg_confidence = sum(r["result"].get("confidence", 0) for r in successful_tests) / len(successful_tests)
                avg_time = sum(r["result"].get("processing_time", 0) for r in successful_tests) / len(successful_tests)
                f.write(f"Average Confidence: {avg_confidence:.3f}\n")
                f.write(f"Average Processing Time: {avg_time:.2f}s\n\n")
            
            # Detailed results by category
            categories = set(r["category"] for r in self.test_results)
            
            for category in sorted(categories):
                category_results = [r for r in self.test_results if r["category"] == category]
                f.write(f"\n{category.upper()} CATEGORY RESULTS\n")
                f.write("=" * 30 + "\n")
                
                for result in category_results:
                    f.write(f"\nQuestion: {result['question']}\n")
                    if result["status"] == "SUCCESS":
                        r = result["result"]
                        f.write(f"Answer: {r.get('answer', 'N/A')}\n")
                        f.write(f"Confidence: {r.get('confidence', 0):.3f}\n")
                        f.write(f"Explanation: {r.get('explanation', 'N/A')}\n")
                        f.write(f"Processing Time: {r.get('processing_time', 0):.2f}s\n")
                    else:
                        f.write(f"ERROR: {result['result'].get('error', 'Unknown error')}\n")
                    f.write("-" * 40 + "\n")
        
        print(f"\n📄 Test report saved to: {filename}")

def main():
    """Run comprehensive tests"""
    tester = ODQATestSuite()
    
    # Test questions organized by category
    test_categories = {
        "Politicians": [
            "Who is the current President of the United States?",
            "Who was the British Prime Minister during World War II?",
            "Who was the first Black president of South Africa?",
            "Who was the 44th President of the United States?",
            "Which leader served as British PM during WWII?",
            "Who led South Africa after apartheid ended?",
            "What president served before Trump?",
            "Who was Nelson Mandela?",
            "Which Churchill led Britain in war?",
            "Who is Joe Biden?"
        ],
        
        "Scientists": [
            "Who was the first woman to win a Nobel Prize?",
            "Who proposed the theory of evolution through natural selection?",
            "Who formulated the laws of motion and universal gravitation?",
            "Who developed the theory of relativity?",
            "Which scientist studied radioactivity?",
            "Who wrote On the Origin of Species?",
            "Which physicist discovered gravity laws?",
            "Who won Nobel Prizes in both Physics and Chemistry?",
            "Which scientist is known for evolution theory?",
            "Who created the theory of relativity?"
        ],
        
        "Geography": [
            "What is the capital of Japan?",
            "What is the capital of Brazil?",
            "What is the capital of Australia?",
            "What is the capital of France?",
            "What is the highest mountain in the world?",
            "What is the longest river in the world?",
            "Which city is Japan's capital?",
            "Where is the capital of Brazil?",
            "What mountain is the tallest?",
            "Which river is the longest?"
        ],

        "Historical_Figures": [
            "Who painted the Mona Lisa?",
            "Who was the last pharaoh of Ancient Egypt?",
            "Which artist created the Mona Lisa?",
            "Who was Cleopatra?",
            "Which Renaissance artist painted the Last Supper?",
            "Who ruled Ancient Egypt last?",
            "What famous painting did Leonardo create?",
            "Which pharaoh was the last of Egypt?",
            "Who was Leonardo da Vinci?",
            "Which Egyptian queen was famous?"
        ],

        "Literature": [
            "Who wrote Romeo and Juliet?",
            "Which playwright created Hamlet?",
            "Who authored Romeo and Juliet?",
            "Which writer is known for Shakespeare's plays?",
            "Who created the character Romeo?",
            "Which English playwright wrote Macbeth?",
            "Who is the author of Hamlet?",
            "Which writer created Juliet?",
            "Who wrote the play Macbeth?",
            "Which playwright is most famous?"
        ],

        "Technology": [
            "Who invented the World Wide Web?",
            "Which scientist created the internet?",
            "Who developed the WWW?",
            "Which inventor made the web?",
            "Who created the first website?",
            "Which computer scientist invented the web?",
            "Who made the World Wide Web?",
            "Which person invented web browsing?",
            "Who developed web technology?",
            "Which scientist created HTML?"
        ]
    }
    
    # Run tests for each category
    for category, questions in test_categories.items():
        tester.run_test_batch(questions, category)
    
    # Generate comprehensive report
    tester.generate_test_report("comprehensive_test_report.txt")
    
    return tester

if __name__ == "__main__":
    test_suite = main()
