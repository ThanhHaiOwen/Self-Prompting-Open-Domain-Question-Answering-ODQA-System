#!/bin/bash

echo "🚀 Pushing Self-Prompting ODQA System to GitHub..."

# Check if repository exists on GitHub
echo "📋 Checking repository status..."

# Try to push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Your repository is now available at:"
    echo "   https://github.com/zafkiel-ltb/self-prompting-odqa"
    echo ""
    echo "📊 Project Summary:"
    echo "   - 137 authentic QA pairs (no formulaic patterns)"
    echo "   - 7 comprehensive topics covered"
    echo "   - FastAPI backend + Next.js frontend"
    echo "   - Professional-grade ODQA system"
    echo ""
    echo "🎉 Ready for deployment and collaboration!"
else
    echo "❌ Failed to push to GitHub."
    echo "📝 Please make sure you have:"
    echo "   1. Created the repository 'self-prompting-odqa' on GitHub"
    echo "   2. Set the repository to public or have proper access"
    echo "   3. Configured your GitHub authentication"
    echo ""
    echo "🔧 To create the repository:"
    echo "   1. Go to https://github.com/zafkiel-ltb"
    echo "   2. Click 'New' or '+' → 'New repository'"
    echo "   3. Name: self-prompting-odqa"
    echo "   4. Description: Self-Prompting ODQA System with Authentic Diverse Dataset"
    echo "   5. Make it Public"
    echo "   6. DON'T add README (we already have one)"
    echo "   7. Click 'Create repository'"
    echo "   8. Run this script again"
fi
