#!/usr/bin/env python3
"""
Simple setup checker that doesn't require dependencies
"""

import os
import sys
from pathlib import Path

def check_file_structure():
    """Check if all required files exist"""
    print("📁 Checking File Structure...")
    
    required_files = [
        # Backend files
        'backend/main.py',
        'backend/qa_engine.py', 
        'backend/gemini_client.py',
        'backend/dataset_generator.py',
        'backend/clustering_retrieval.py',
        'backend/database.py',
        'backend/config.py',
        'backend/requirements.txt',
        'backend/.env.example',
        
        # Frontend files
        'frontend/package.json',
        'frontend/app/page.tsx',
        'frontend/components/QuestionAnswering.tsx',
        'frontend/components/SystemStatus.tsx',
        'frontend/components/DatasetViewer.tsx',
        
        # Root files
        'README.md',
        'setup.py',
        'run_system.py',
        'demo.py',
        'test_system.py',
        'docker-compose.yml',
        'Dockerfile',
        '.gitignore'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_config_files():
    """Check configuration files"""
    print("\n⚙️  Checking Configuration...")
    
    # Check backend config
    config_file = Path('backend/config.py')
    if config_file.exists():
        with open(config_file) as f:
            content = f.read()
            
        # Check for required configurations
        checks = [
            ('TOPICS_CONFIG', 'Topic configuration'),
            ('PROMPT_TEMPLATES', 'Prompt templates'),
            ('GEMINI_API_KEY', 'API key configuration'),
            ('29', 'Expected number of topics')
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}")
    
    # Check environment setup
    env_example = Path('backend/.env.example')
    if env_example.exists():
        print("✅ Environment template exists")
    else:
        print("❌ Environment template missing")

def check_documentation():
    """Check documentation files"""
    print("\n📚 Checking Documentation...")
    
    doc_files = [
        'README.md',
        'GETTING_STARTED.md', 
        'PROJECT_SUMMARY.md',
        'docs/SYSTEM_ARCHITECTURE.md',
        'docs/DEPLOYMENT_GUIDE.md'
    ]
    
    for doc_file in doc_files:
        if Path(doc_file).exists():
            print(f"✅ {doc_file}")
        else:
            print(f"❌ {doc_file}")

def check_python_version():
    """Check Python version"""
    print("\n🐍 Checking Python Version...")
    
    version = sys.version_info
    if version >= (3, 8):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        return False

def check_directories():
    """Check required directories"""
    print("\n📂 Checking Directories...")
    
    required_dirs = [
        'backend',
        'frontend', 
        'frontend/app',
        'frontend/components',
        'frontend/lib',
        'frontend/types',
        'docs'
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists() and Path(dir_path).is_dir():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/")

def main():
    """Main check function"""
    print("🔍 Self-Prompting ODQA System - Setup Check")
    print("=" * 50)
    print("Verifying system files and configuration...")
    print()
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("File Structure", check_file_structure),
        ("Directories", check_directories),
        ("Configuration", check_config_files),
        ("Documentation", check_documentation)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
            results.append((check_name, False))
        print()
    
    # Summary
    print("=" * 50)
    print("📊 Setup Check Summary:")
    
    passed = 0
    for check_name, result in results:
        if result is True:
            print(f"✅ {check_name}: PASS")
            passed += 1
        elif result is False:
            print(f"❌ {check_name}: FAIL")
        else:
            print(f"ℹ️  {check_name}: CHECKED")
            passed += 1
    
    total = len([r for r in results if r[1] is not None])
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Setup check complete! System appears ready.")
        print("\nNext steps:")
        print("1. Install dependencies: python setup.py")
        print("2. Configure API key in backend/.env")
        print("3. Start system: python run_system.py run")
    else:
        print("\n⚠️  Some issues found. Please review above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
