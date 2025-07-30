#!/usr/bin/env python3
"""
System runner for Self-Prompting ODQA System
Provides easy commands to run and test the system
"""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path
import requests

def run_command(command, cwd=None, background=False):
    """Run a command"""
    print(f"Running: {command}")
    if background:
        return subprocess.Popen(command, shell=True, cwd=cwd)
    else:
        return subprocess.run(command, shell=True, cwd=cwd)

def check_backend_ready(max_attempts=30):
    """Check if backend is ready"""
    print("Waiting for backend to be ready...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✓ Backend is ready")
                return True
        except:
            pass
        
        time.sleep(1)
        if attempt % 5 == 0:
            print(f"Still waiting... (attempt {attempt + 1}/{max_attempts})")
    
    print("⚠ Backend not responding")
    return False

def start_backend():
    """Start the backend server"""
    print("Starting backend server...")
    
    backend_dir = Path("backend")
    
    # Determine Python executable in venv
    if os.name == 'nt':  # Windows
        python_path = backend_dir / "venv" / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        python_path = backend_dir / "venv" / "bin" / "python"
    
    if not python_path.exists():
        print("Error: Virtual environment not found. Run setup.py first.")
        sys.exit(1)
    
    # Start backend
    process = run_command(
        f"{python_path} main.py",
        cwd=backend_dir,
        background=True
    )
    
    return process

def start_frontend():
    """Start the frontend server"""
    print("Starting frontend server...")
    
    frontend_dir = Path("frontend")
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("Error: Frontend dependencies not installed. Run setup.py first.")
        sys.exit(1)
    
    # Start frontend
    process = run_command(
        "npm run dev",
        cwd=frontend_dir,
        background=True
    )
    
    return process

def run_full_system():
    """Run the complete system (backend + frontend)"""
    print("Starting Self-Prompting ODQA System...")
    print("="*40)
    
    # Start backend
    backend_process = start_backend()
    
    # Wait for backend to be ready
    if not check_backend_ready():
        print("Failed to start backend")
        backend_process.terminate()
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    
    print("\n" + "="*40)
    print("🚀 System is running!")
    print("="*40)
    print("Frontend: http://localhost:3000")
    print("Backend API: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both servers")
    
    try:
        # Wait for processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("Backend process stopped")
                break
            if frontend_process.poll() is not None:
                print("Frontend process stopped")
                break
                
    except KeyboardInterrupt:
        print("\nShutting down...")
        
    finally:
        # Clean up processes
        try:
            backend_process.terminate()
            frontend_process.terminate()
            
            # Wait a bit for graceful shutdown
            time.sleep(2)
            
            # Force kill if still running
            if backend_process.poll() is None:
                backend_process.kill()
            if frontend_process.poll() is None:
                frontend_process.kill()
                
        except:
            pass
        
        print("System stopped")

def test_system():
    """Test the system with sample questions"""
    print("Testing Self-Prompting ODQA System...")
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("Backend not responding. Please start the system first.")
            sys.exit(1)
    except:
        print("Backend not accessible. Please start the system first.")
        sys.exit(1)
    
    # Test questions
    test_questions = [
        "Who was the first person to walk on the moon?",
        "What is the capital of France?",
        "When was the Declaration of Independence signed?",
        "Who wrote Romeo and Juliet?",
        "What is the largest planet in our solar system?"
    ]
    
    print(f"\nTesting with {len(test_questions)} sample questions...")
    print("="*50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        
        try:
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": question, "n_demonstrations": 5},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Answer: {result['answer']}")
                print(f"   Confidence: {result['confidence']:.2f}")
                print(f"   Time: {result['processing_time']:.2f}s")
                if result.get('explanation'):
                    print(f"   Explanation: {result['explanation'][:100]}...")
            else:
                print(f"   Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n" + "="*50)
    print("Testing complete!")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Self-Prompting ODQA System Runner")
    parser.add_argument(
        "command",
        choices=["run", "backend", "frontend", "test"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    if args.command == "run":
        run_full_system()
    elif args.command == "backend":
        backend_process = start_backend()
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            backend_process.terminate()
    elif args.command == "frontend":
        frontend_process = start_frontend()
        try:
            frontend_process.wait()
        except KeyboardInterrupt:
            frontend_process.terminate()
    elif args.command == "test":
        test_system()

if __name__ == "__main__":
    main()
