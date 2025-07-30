#!/bin/bash

# 🚀 Self-Prompting ODQA System - GitHub Setup Script
# This script helps you push your project to GitHub

echo "🧠 Self-Prompting ODQA System - GitHub Setup"
echo "============================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files to git
echo "📝 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "🎉 Initial commit: Self-Prompting ODQA System with 300 authentic QA pairs

Features:
- 🧠 Advanced self-prompting mechanism
- 📊 300 authentic QA pairs across 7 topics
- 🏗️ FastAPI backend + React frontend
- 🎯 98-100% confidence responses
- 🌟 Zero formulaic content

Topics covered:
- Politicians (65 pairs)
- Scientists (60 pairs) 
- Geography (50 pairs)
- Countries (45 pairs)
- Technology (45 pairs)
- Literature (10 pairs)
- Historical Figures (25 pairs)"

echo ""
echo "🎯 Next Steps:"
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: self-prompting-odqa"
echo "   - Description: Advanced Self-Prompting ODQA System with 300 authentic QA pairs"
echo "   - Make it Public"
echo "   - Don't initialize with README (we already have one)"
echo ""
echo "2. Copy the repository URL (e.g., https://github.com/yourusername/self-prompting-odqa.git)"
echo ""
echo "3. Run these commands with your actual repository URL:"
echo "   git remote add origin https://github.com/yourusername/self-prompting-odqa.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "📋 Repository Information:"
echo "   - Total files: $(find . -type f | wc -l) files"
echo "   - Backend: FastAPI with 300 QA pairs"
echo "   - Frontend: React with modern UI"
echo "   - Database: SQLite with authentic content"
echo "   - Documentation: Comprehensive README and guides"
echo ""
echo "🎊 Your Self-Prompting ODQA System is ready for GitHub!"

# Show git status
echo ""
echo "📊 Git Status:"
git status --short
