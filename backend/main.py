"""
FastAPI server for Self-Prompting ODQA System
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import asyncio
from contextlib import asynccontextmanager

from qa_engine import QAEngine, QAResult
from config import TOPICS_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global QA engine instance
qa_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global qa_engine
    logger.info("Starting Self-Prompting ODQA System...")
    
    # Initialize QA engine
    qa_engine = QAEngine()
    
    yield
    
    logger.info("Shutting down Self-Prompting ODQA System...")

# Create FastAPI app
app = FastAPI(
    title="Self-Prompting ODQA System",
    description="A complete implementation of Self-Prompting Large Language Models for Zero-Shot Open-Domain QA",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class QuestionRequest(BaseModel):
    question: str
    n_demonstrations: Optional[int] = 10

class QuestionResponse(BaseModel):
    question: str
    answer: str
    explanation: Optional[str] = None
    confidence: float
    demonstrations_used: int
    processing_time: float
    error: Optional[str] = None

class SystemStatus(BaseModel):
    system_ready: bool
    dataset_stats: Dict[str, Any]
    clustering_stats: Dict[str, Any]
    components_status: Dict[str, bool]

class PreparationRequest(BaseModel):
    force_regenerate: Optional[bool] = False

class DatasetSampleRequest(BaseModel):
    topic: Optional[str] = None
    limit: Optional[int] = 5

# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Self-Prompting ODQA System",
        "description": "A complete implementation of the research paper",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "system_ready": qa_engine.system_ready if qa_engine else False}

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get current system status"""
    if not qa_engine:
        raise HTTPException(status_code=500, detail="QA Engine not initialized")
    
    status = qa_engine.check_system_status()
    return SystemStatus(**status)

@app.post("/prepare")
async def prepare_system(request: PreparationRequest, background_tasks: BackgroundTasks):
    """Prepare the system (generate dataset and clustering)"""
    if not qa_engine:
        raise HTTPException(status_code=500, detail="QA Engine not initialized")
    
    # Run preparation in background
    background_tasks.add_task(
        run_system_preparation, 
        request.force_regenerate
    )
    
    return {
        "message": "System preparation started in background",
        "force_regenerate": request.force_regenerate
    }

async def run_system_preparation(force_regenerate: bool = False):
    """Run system preparation in background"""
    try:
        logger.info(f"Starting system preparation (force_regenerate={force_regenerate})")
        result = qa_engine.prepare_system(force_regenerate=force_regenerate)
        logger.info(f"System preparation completed: {result}")
    except Exception as e:
        logger.error(f"System preparation failed: {e}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer"""
    if not qa_engine:
        raise HTTPException(status_code=500, detail="QA Engine not initialized")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Answer the question
    result = qa_engine.answer_question(
        question=request.question,
        n_demonstrations=request.n_demonstrations
    )
    
    return QuestionResponse(
        question=result.question,
        answer=result.answer,
        explanation=result.explanation,
        confidence=result.confidence,
        demonstrations_used=result.demonstrations_used,
        processing_time=result.processing_time,
        error=result.error
    )

@app.get("/topics")
async def get_topics():
    """Get available topics and their target counts"""
    return {
        "topics": TOPICS_CONFIG,
        "total_topics": len(TOPICS_CONFIG),
        "total_target_pairs": sum(TOPICS_CONFIG.values())
    }

@app.get("/sample-questions")
async def get_sample_questions():
    """Get sample questions from the dataset"""
    if not qa_engine:
        raise HTTPException(status_code=500, detail="QA Engine not initialized")
    
    try:
        questions = qa_engine.get_sample_questions()
        return {"sample_questions": questions}
    except Exception as e:
        logger.error(f"Error getting sample questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get sample questions")

@app.post("/dataset-sample")
async def get_dataset_sample(request: DatasetSampleRequest):
    """Get a sample of the generated dataset"""
    if not qa_engine:
        raise HTTPException(status_code=500, detail="QA Engine not initialized")
    
    try:
        sample = qa_engine.get_dataset_sample(
            topic=request.topic,
            limit=request.limit
        )
        return {
            "sample": sample,
            "topic": request.topic,
            "count": len(sample)
        }
    except Exception as e:
        logger.error(f"Error getting dataset sample: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dataset sample")

@app.get("/preparation-progress")
async def get_preparation_progress():
    """Get current preparation progress"""
    if not qa_engine:
        raise HTTPException(status_code=500, detail="QA Engine not initialized")
    
    try:
        progress = qa_engine.dataset_generator.get_generation_progress()
        return progress
    except Exception as e:
        logger.error(f"Error getting preparation progress: {e}")
        raise HTTPException(status_code=500, detail="Failed to get preparation progress")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
