# Getting Started with Self-Prompting ODQA System

This guide will help you set up and run the Self-Prompting ODQA System in just a few minutes.

## 🚀 Quick Start (5 minutes)

### Step 1: Get Your API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (keep it secure!)

### Step 2: Setup the System
```bash
# Clone or navigate to the project directory
cd NLP

# Run the automated setup
python setup.py
```

### Step 3: Configure API Key
```bash
# Edit the environment file
# Windows:
notepad backend\.env

# Mac/Linux:
nano backend/.env

# Add your API key:
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 4: Start the System
```bash
# Start both backend and frontend
python run_system.py run
```

### Step 5: Use the System
1. Open your browser to http://localhost:3000
2. Click "Prepare System" (first time only - takes 10-30 minutes)
3. Start asking questions!

## 📋 Detailed Setup Guide

### Prerequisites Check
```bash
# Check Python version (need 3.8+)
python --version

# Check Node.js version (need 18+)
node --version

# If missing, install from:
# Python: https://python.org
# Node.js: https://nodejs.org
```

### Manual Installation

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Start Backend
```bash
cd backend
# Make sure virtual environment is activated
python main.py
```

## 🐳 Docker Setup (Alternative)

If you prefer Docker:

```bash
# Create environment file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Start with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## 🔧 System Preparation

### First Time Setup
1. **Access the Web Interface**: http://localhost:3000
2. **Check System Status**: Go to "System Status" tab
3. **Prepare System**: Click "Prepare System" button
4. **Wait for Completion**: This generates ~2,900 QA pairs (10-30 minutes)
5. **Start Using**: Once ready, go to "Question Answering" tab

### What Happens During Preparation
The system will:
1. Generate Wikipedia-style passages for 29 topics
2. Extract named entities from passages
3. Create questions for extracted entities
4. Generate explanations for QA pairs
5. Compute embeddings and perform clustering

## 💬 Using the System

### Question Answering Interface
1. **Enter Your Question**: Type any open-domain question
2. **Adjust Settings**: Choose number of demonstrations (5-15)
3. **Get Answer**: Click "Ask Question"
4. **View Results**: See answer, explanation, and confidence

### Sample Questions to Try
- "Who was the first person to walk on the moon?"
- "What is the capital of France?"
- "When was the Declaration of Independence signed?"
- "Who wrote Romeo and Juliet?"
- "What is the largest planet in our solar system?"

### System Status Monitoring
- **Dataset Stats**: View generated QA pairs by topic
- **Clustering Info**: See how data is organized
- **Component Status**: Check system health
- **Regeneration**: Force regenerate dataset if needed

### Dataset Exploration
- **Browse QA Pairs**: See examples of generated questions
- **Filter by Topic**: Explore specific categories
- **Quality Assessment**: Review explanations and answers

## 🛠️ Troubleshooting

### Common Issues

#### "API Key Error"
```bash
# Check if API key is set
cat backend/.env | grep GEMINI_API_KEY

# Test API access
python -c "
import sys; sys.path.append('backend')
from gemini_client import GeminiClient
print(GeminiClient().generate_text('Hello'))
"
```

#### "Port Already in Use"
```bash
# Check what's using the ports
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Kill processes or use different ports
python run_system.py run --backend-port 8001 --frontend-port 3001
```

#### "System Not Ready"
1. Check if preparation completed successfully
2. Look at system status for error messages
3. Try regenerating the dataset
4. Check logs for detailed error information

#### "Slow Performance"
1. Reduce number of demonstrations (try 5-8)
2. Check internet connection (API calls)
3. Ensure sufficient RAM (4GB+ recommended)
4. Close other applications

### Getting Help

1. **Check Logs**: Look at console output for errors
2. **System Status**: Use the web interface status page
3. **Test Components**: Run `python test_system.py`
4. **Validate Setup**: Run `python validate_implementation.py`

## 📊 Understanding the Results

### Answer Quality Indicators
- **Confidence**: 80%+ is high confidence
- **Processing Time**: 2-5 seconds is normal
- **Demonstrations**: More demonstrations usually = better answers

### Explanation Types
- **Direct Facts**: Simple factual answers
- **Contextual**: Answers requiring reasoning
- **Historical**: Time-based information
- **Comparative**: Relative information

## 🎯 Best Practices

### For Best Results
1. **Ask Clear Questions**: Specific, well-formed questions work best
2. **Use Natural Language**: Write questions as you would ask a person
3. **Be Patient**: First-time setup takes time but is worth it
4. **Explore Topics**: Try questions from different domains

### System Maintenance
1. **Regular Backups**: Backup your data directory
2. **Monitor Performance**: Check system status regularly
3. **Update Dependencies**: Keep packages up to date
4. **API Limits**: Be aware of Gemini API quotas

## 🚀 Next Steps

### Once Running
1. **Try the Interactive Demo**: `python demo.py`
2. **Explore the API**: Visit http://localhost:8000/docs
3. **Read the Documentation**: Check docs/ folder
4. **Experiment**: Try different question types and topics

### For Developers
1. **Study the Code**: Understand the implementation
2. **Run Tests**: Execute the test suite
3. **Modify Topics**: Add your own topic categories
4. **Extend Functionality**: Build on the existing system

## 📚 Additional Resources

- **Research Paper**: https://arxiv.org/abs/2212.08029
- **System Architecture**: docs/SYSTEM_ARCHITECTURE.md
- **Deployment Guide**: docs/DEPLOYMENT_GUIDE.md
- **Project Summary**: PROJECT_SUMMARY.md

## 🎉 Success!

If you've followed this guide, you now have a fully functional Self-Prompting ODQA system that can answer questions without any training data, just like the research paper describes!

The system demonstrates the power of self-prompting and in-context learning, providing explainable answers with confidence estimation across a wide range of topics.
