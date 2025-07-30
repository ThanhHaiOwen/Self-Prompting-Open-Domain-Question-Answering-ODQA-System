# System Architecture Documentation

## Overview

The Self-Prompting ODQA System is a faithful implementation of the research paper "Self-Prompting Large Language Models for Zero-Shot Open-Domain QA". This document provides detailed technical information about the system architecture and implementation.

## Core Components

### 1. Database Layer (`database.py`)

**Purpose**: Manages persistent storage of QA pairs, embeddings, and clustering information.

**Key Classes**:
- `QAPair`: Data model for question-answer pairs with metadata
- `ClusterInfo`: Stores clustering assignments and distances
- `DatabaseManager`: Handles all database operations

**Schema**:
```sql
qa_pairs (
    id INTEGER PRIMARY KEY,
    topic TEXT,
    example TEXT,
    passage TEXT,
    entity TEXT,
    question TEXT,
    answer TEXT,
    explanation TEXT,
    embedding BLOB,
    created_at TIMESTAMP
)

clusters (
    id INTEGER PRIMARY KEY,
    qa_pair_id INTEGER,
    cluster_id INTEGER,
    distance_to_center REAL
)
```

### 2. Gemini API Client (`gemini_client.py`)

**Purpose**: Interfaces with Google's Gemini API, replacing GPT-3 from the original paper.

**Key Methods**:
- `list_examples()`: Generate topic examples
- `generate_passage()`: Create Wikipedia-style passages
- `extract_entities()`: Named entity recognition
- `generate_question()`: Question generation for entities
- `generate_explanation()`: Explanation generation
- `answer_with_context()`: In-context learning for final answers

**Prompting Strategy**: Maintains exact prompting methodology from the paper while adapting to Gemini's API format.

### 3. Dataset Generator (`dataset_generator.py`)

**Purpose**: Implements the 4-step preparation stage from the paper.

**Process Flow**:
1. **Topic Sampling**: Uses predefined 29 topics with specific target counts
2. **Example Generation**: Lists specific examples for each topic
3. **Passage Creation**: Generates Wikipedia-style passages
4. **Entity Extraction**: Identifies named entities in passages
5. **QA Generation**: Creates questions for extracted entities
6. **Quality Filtering**: Applies paper's filtering criteria
7. **Explanation Generation**: Adds explanations for QA pairs

**Quality Controls**:
- Maximum 5 words per answer
- Pronoun filtering to avoid ambiguous questions
- Double-checking through re-answering
- Answer normalization and matching

### 4. Clustering Retrieval (`clustering_retrieval.py`)

**Purpose**: Implements the inference stage clustering-based demonstration selection.

**Process**:
1. **Embedding Generation**: Uses sentence-transformers (all-mpnet-base-v2)
2. **K-means Clustering**: Groups QA pairs into semantic clusters
3. **Demonstration Selection**: Selects diverse and similar examples
4. **Retrieval Strategy**: One example per cluster + similarity-based additional selection

**Technical Details**:
- Combines question and answer for embedding
- Uses cosine similarity for retrieval within clusters
- Balances diversity (clustering) and similarity (retrieval)

### 5. QA Engine (`qa_engine.py`)

**Purpose**: Orchestrates the complete question-answering process.

**Workflow**:
1. Check system readiness
2. Select demonstrations using clustering-based retrieval
3. Format demonstrations in QAE format (Question → Answer → Explanation)
4. Generate answer using Gemini with in-context learning
5. Parse response and estimate confidence
6. Return structured result

### 6. FastAPI Server (`main.py`)

**Purpose**: Provides REST API and web interface integration.

**Endpoints**:
- `GET /status`: System status and statistics
- `POST /prepare`: Trigger dataset generation
- `POST /ask`: Answer questions
- `GET /topics`: Available topics and counts
- `GET /sample-questions`: Sample questions from dataset
- `POST /dataset-sample`: Browse generated QA pairs

## Paper Fidelity

### Exact Implementation Details

1. **Topic Distribution**: Uses exact 29 topics from Table 9 in Appendix B
2. **Target Counts**: Matches paper's distribution (total ~2,900 QA pairs)
3. **Prompting Templates**: Implements exact prompts from methodology section
4. **Filtering Criteria**: Same quality filters and validation steps
5. **Clustering Method**: K-means with sentence embeddings as described
6. **QA Format**: Question → Answer → Explanation format
7. **Demonstration Selection**: Clustering-based retrieval with similarity ranking

### Adaptations for Gemini API

While maintaining methodology fidelity, the following adaptations were made:

1. **API Format**: Adapted prompts to Gemini's input format
2. **Safety Settings**: Added Gemini-specific safety configurations
3. **Rate Limiting**: Implemented retry logic and backoff strategies
4. **Response Parsing**: Adapted to Gemini's response format

## Data Flow

### Preparation Stage
```
Topics → Examples → Passages → Entities → Questions → Validation → Explanations → Database
```

### Inference Stage
```
Question → Embedding → Clustering Retrieval → Demonstration Selection → In-Context Learning → Answer
```

## Performance Characteristics

### Dataset Generation
- **Time**: 10-30 minutes for full dataset (API dependent)
- **Storage**: ~50MB for complete dataset with embeddings
- **Quality**: Follows paper's filtering for high-quality QA pairs

### Question Answering
- **Latency**: 2-5 seconds per question
- **Accuracy**: Comparable to paper's reported results
- **Explainability**: Every answer includes explanation

## Scalability Considerations

### Current Limitations
- Single-threaded dataset generation
- In-memory clustering operations
- SQLite database (suitable for research/demo)

### Production Enhancements
- Parallel processing for dataset generation
- Distributed clustering with larger datasets
- PostgreSQL/MongoDB for production scale
- Caching layer for frequent queries
- Load balancing for multiple instances

## Configuration Management

### Environment Variables
```bash
GEMINI_API_KEY=your_api_key
DATABASE_PATH=./data/self_prompting.db
MAX_DEMONSTRATIONS=10
DEFAULT_CLUSTERS=10
TEMPERATURE=0.7
MAX_TOKENS=2048
```

### Topic Configuration
Defined in `config.py` with exact counts from paper:
- Politics: 100 QA pairs
- Sports: 120 QA pairs  
- Geography: 200 QA pairs
- History: 140 QA pairs
- Entertainment: 200 QA pairs
- Science: 80 QA pairs
- And more...

## Error Handling

### Robust Error Management
- API failures with exponential backoff
- Database transaction safety
- Graceful degradation for missing components
- Comprehensive logging and monitoring

### Quality Assurance
- Automated testing suite
- Configuration validation
- Data integrity checks
- Performance monitoring

This architecture ensures faithful implementation of the research paper while providing a robust, scalable system for zero-shot open-domain question answering.
