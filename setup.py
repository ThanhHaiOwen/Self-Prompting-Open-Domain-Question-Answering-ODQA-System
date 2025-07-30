#!/usr/bin/env python3
"""
Setup script for Self-Prompting ODQA System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and handle errors"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = run_command("node --version", check=False)
        if result.returncode == 0:
            print(f"✓ Node.js detected: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("⚠ Node.js not found. Please install Node.js 18+ for the frontend")
    return False

def setup_backend():
    """Setup the backend environment"""
    print("\n=== Setting up Backend ===")
    
    backend_dir = Path("backend")
    
    # Create virtual environment
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        run_command(f"python -m venv {venv_path}")
    
    # Determine activation script
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix/Linux/Mac
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    # Install requirements
    print("Installing Python dependencies...")
    run_command(f"{pip_path} install --upgrade pip")
    run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir)
    
    # Create .env file if it doesn't exist
    env_file = backend_dir / ".env"
    env_example = backend_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from template...")
        shutil.copy(env_example, env_file)
        print("⚠ Please edit backend/.env and add your GEMINI_API_KEY")
    
    print("✓ Backend setup complete")

def setup_frontend():
    """Setup the frontend environment"""
    print("\n=== Setting up Frontend ===")
    
    if not check_node_version():
        print("Skipping frontend setup - Node.js not available")
        return
    
    frontend_dir = Path("frontend")
    
    # Install npm dependencies
    print("Installing Node.js dependencies...")
    run_command("npm install", cwd=frontend_dir)
    
    print("✓ Frontend setup complete")

def create_data_directory():
    """Create data directory"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("✓ Data directory created")

def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*50)
    print("🎉 Setup Complete!")
    print("="*50)
    
    print("\nNext steps:")
    print("1. Edit backend/.env and add your GEMINI_API_KEY")
    print("   Get your API key from: https://makersuite.google.com/app/apikey")
    
    print("\n2. Start the backend server:")
    if os.name == 'nt':  # Windows
        print("   cd backend")
        print("   venv\\Scripts\\activate")
        print("   python main.py")
    else:  # Unix/Linux/Mac
        print("   cd backend")
        print("   source venv/bin/activate")
        print("   python main.py")
    
    print("\n3. In a new terminal, start the frontend:")
    print("   cd frontend")
    print("   npm run dev")
    
    print("\n4. Open your browser to:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    
    print("\n5. Use the web interface to:")
    print("   - Prepare the system (generate dataset)")
    print("   - Ask questions")
    print("   - Explore the generated dataset")
    
    print("\nFor more information, see README.md")

def main():
    """Main setup function"""
    print("Self-Prompting ODQA System Setup")
    print("="*40)
    
    # Check requirements
    check_python_version()
    
    # Setup components
    create_data_directory()
    setup_backend()
    setup_frontend()
    
    # Show next steps
    display_next_steps()

if __name__ == "__main__":
    main()
