# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- Git

## 1. Clone Repository
```bash
git clone <your-repo-url>
cd self-prompting-odqa
```

## 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## 3. Frontend Setup
```bash
cd frontend
npm install
```

## 4. Initialize Dataset
```bash
# From project root
python create_sample_dataset.py
python prepare_clustering.py
```

## 5. Run System
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
python main.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

## 6. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Features
- ✅ 300 QA pairs across 18+ topics
- ✅ Advanced clustering retrieval
- ✅ Real-time question answering
- ✅ Dataset viewer with filtering
- ✅ System status monitoring

## Troubleshooting
- Ensure ports 3000 and 8000 are available
- Check Python and Node.js versions
- Verify virtual environment activation
- Run `python check_setup.py` to validate setup
