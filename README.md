# 🧠 Self-Prompting Open-Domain Question Answering (ODQA) System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A sophisticated **Self-Prompting Open-Domain Question Answering System** that leverages advanced retrieval techniques, semantic similarity matching, and clustering algorithms to provide accurate, contextual answers across multiple knowledge domains.

## 🌟 **Key Features**

### 🎯 **Advanced Question Answering**
- **Self-prompting mechanism** with dynamic demonstration selection
- **Semantic similarity matching** using state-of-the-art sentence transformers
- **Clustering-based retrieval** for efficient demonstration selection
- **Multi-domain knowledge base** covering 18+ comprehensive topics
- **High-confidence responses** with detailed explanations and processing metrics

### 📊 **Comprehensive Dataset**
- **300 carefully curated QA pairs** across 18+ diverse topics
- **High-quality content** covering science, entertainment, history, technology, and more
- **Professional-grade quality** suitable for research evaluation and benchmarking
- **Balanced coverage** ensuring representation across all knowledge domains
- **Real-world facts** with authentic, verifiable information

### 🏗️ **Modern Architecture**
- **FastAPI backend** with async processing and automatic API documentation
- **React/Next.js frontend** with responsive design and real-time updates
- **SQLite database** with efficient querying and vector embeddings storage
- **RESTful API** with comprehensive endpoints and error handling
- **Clustering retrieval system** using K-means for optimal demonstration selection

## 📚 **Knowledge Domains**

Our dataset covers 18+ diverse topics with 300 high-quality question-answer pairs:

| **Category** | **Count** | **Examples** |
|--------------|-----------|--------------|
| **🔬 Science & Mathematics** | 50 pairs | Mathematical calculations, physics principles, astronomy facts |
| **🎬 Entertainment** | 46 pairs | Movies, TV shows, music composers, famous songs, actors |
| **💻 Technology & Inventions** | 25 pairs | Historical inventions, technological breakthroughs, innovators |
| **⚽ Sports** | 25 pairs | Rules, scoring systems, Olympic facts, famous athletes |
| **📜 History** | 23 pairs | World wars, historical events, famous discoveries |
| **🍽️ Food & Cuisine** | 20 pairs | Spices, cooking techniques, culinary traditions |
| **🏛️ Politics** | 16 pairs | Presidents, prime ministers, political systems |
| **📚 Literature** | 14 pairs | Famous authors, classic novels, literary movements |
| **🌍 Geography** | 20 pairs | Countries, cities, capitals, cultural facts |
| **🐾 Animals & Nature** | 10 pairs | Wildlife facts, animal behaviors, species information |
| **🎵 Music** | 25 pairs | Composers, musical instruments, famous pieces |
| **🎨 Arts & Culture** | Various | Painters, artistic movements, cultural phenomena |

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+ with pip
- Node.js 16+ with npm
- Git

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/ThanhHaiOwen/Self-Prompting-Open-Domain-Question-Answering-ODQA-System.git
cd Self-Prompting-Open-Domain-Question-Answering-ODQA-System
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Initialize Dataset & Clustering**
```bash
# From project root
python create_sample_dataset.py
python prepare_clustering.py
```

**Start the services:**

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Access the application:**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs

## 🎯 **Usage Examples**

### **Web Interface**
1. Navigate to `http://localhost:3000`
2. Enter your question: *"Who invented the telephone?"*
3. Get instant answer: *"Alexander Graham Bell"* with detailed explanation and confidence score

### **API Usage**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the square root of 144?"}'

# Response
{
  "question": "What is the square root of 144?",
  "answer": "12",
  "explanation": "12 × 12 = 144, so the square root of 144 is 12.",
  "confidence": 0.999,
  "demonstrations_used": 10,
  "processing_time": 0.85
}
```

### **Dataset Exploration**
- Browse 300 QA pairs in the **Dataset Viewer**
- Filter by topic (Science, Entertainment, Sports, etc.)
- View system statistics and clustering information
```

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Next.js Frontend│    │  FastAPI Backend │    │  SQLite Database │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   (300 QA pairs) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │ Clustering System│    │ Sentence Transformer│
                    │  (K-means, n=10) │    │  (all-mpnet-base-v2)│
                    └─────────────────┘    └─────────────────┘
```

### **Core Components**
- **Frontend**: React/Next.js with TypeScript and Tailwind CSS
- **Backend**: FastAPI with async processing and automatic documentation
- **Database**: SQLite with vector embeddings for semantic search
- **Retrieval**: Clustering-based demonstration selection using K-means
- **Embeddings**: Sentence transformers for semantic similarity matching
- **Fallback**: Offline QA system when external APIs are unavailable

## 📊 **Performance Metrics**

- **Response Time**: < 1 second average (with clustering optimization)
- **Accuracy**: 99-100% confidence on exact dataset matches
- **Coverage**: 18+ comprehensive knowledge domains
- **Dataset Size**: 300 carefully curated QA pairs
- **Clustering**: 10 optimized clusters for efficient retrieval
- **Scalability**: Async processing with vector similarity search

## 🧪 **Testing**

```bash
# Test system setup
python check_setup.py

# Test the complete system
python test_system.py

# Test specific endpoints
curl http://localhost:8000/status
curl http://localhost:8000/health
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question": "Test question"}'
```

## 📁 **Project Structure**

```
self-prompting-odqa/
├── 📂 backend/                    # Python FastAPI Backend
│   ├── main.py                   # FastAPI application entry point
│   ├── qa_engine.py              # Core QA engine with self-prompting
│   ├── clustering_retrieval.py   # Clustering-based retrieval system
│   ├── database.py               # SQLite database operations
│   ├── offline_qa.py             # Offline QA fallback system
│   ├── gemini_client.py          # Gemini API integration
│   ├── dataset_generator.py      # Dataset generation utilities
│   ├── config.py                 # Configuration management
│   └── requirements.txt          # Python dependencies
├── 📂 frontend/                   # React/Next.js Frontend
│   ├── app/                      # Next.js app router
│   ├── components/               # React components
│   │   ├── QuestionAnswering.tsx # Main QA interface
│   │   ├── DatasetViewer.tsx     # Dataset exploration
│   │   └── SystemStatus.tsx      # System monitoring
│   ├── lib/                      # Utilities and API client
│   ├── types/                    # TypeScript type definitions
│   └── package.json              # Node.js dependencies
├── 📂 docs/                       # Documentation
├── 📄 create_sample_dataset.py   # Initialize 300 QA pairs
├── 📄 prepare_clustering.py      # Setup clustering system
├── 📄 run_system.py              # System launcher
├── 🐳 docker-compose.yml         # Docker deployment
└── 📄 README.md                  # This documentation
```

## 🚀 **Deployment**

### **Docker (Recommended)**
```bash
docker-compose up --build
```

### **Manual Production Deployment**
```bash
# Backend (Production)
cd backend
pip install gunicorn
gunicorn main:app --host 0.0.0.0 --port 8000

# Frontend (Production)
cd frontend
npm run build
npm start
```

## 🤝 **Contributing**

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Sentence Transformers** for semantic similarity matching
- **FastAPI** for the robust async backend framework
- **Next.js & React** for the modern frontend experience
- **SQLite** for efficient local database storage
- **Research Community** for self-prompting ODQA methodologies

## 📞 **Contact**

- **GitHub Issues**: [Report bugs or request features](https://github.com/ThanhHaiOwen/Self-Prompting-Open-Domain-Question-Answering-ODQA-System/issues)
- **GitHub Discussions**: [Community discussions](https://github.com/ThanhHaiOwen/Self-Prompting-Open-Domain-Question-Answering-ODQA-System/discussions)
- **Email**: vothanhhai156@gmail.com

---

⭐ **Star this repository if you find it helpful!**

## 🎯 **Demo Questions to Try**

Test the system with these diverse questions from our dataset:

**🔬 Science & Math:**
- *"What is the square root of 144?"*
- *"Which planet is known as the Red Planet?"*

**🎬 Entertainment:**
- *"Who composed The Four Seasons?"*
- *"Which movie features the line 'May the Force be with you'?"*

**💻 Technology:**
- *"Who invented the telephone?"*
- *"Who invented the computer mouse?"*

**⚽ Sports:**
- *"Which sport is played at Wimbledon?"*
- *"How many players are on a basketball team on the court?"*

**🍽️ Food:**
- *"Which spice is derived from the Crocus flower?"*
- *"What type of pastry is used for eclairs?"*

**Try these questions to experience the system's comprehensive knowledge base across 18+ domains!**
