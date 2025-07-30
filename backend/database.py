"""
Database models and operations for Self-Prompting ODQA System
"""

import sqlite3
import json
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import os

from config import DATABASE_PATH

@dataclass
class QAPair:
    """Represents a Question-Answer pair with metadata"""
    id: Optional[int] = None
    topic: str = ""
    example: str = ""
    passage: str = ""
    entity: str = ""
    question: str = ""
    answer: str = ""
    explanation: str = ""
    embedding: Optional[np.ndarray] = None
    created_at: Optional[datetime] = None

@dataclass
class ClusterInfo:
    """Represents clustering information"""
    id: Optional[int] = None
    qa_pair_id: int = 0
    cluster_id: int = 0
    distance_to_center: float = 0.0

class DatabaseManager:
    """Manages database operations for the Self-Prompting system"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.ensure_data_directory()
        self.init_database()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # QA Pairs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS qa_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    example TEXT NOT NULL,
                    passage TEXT NOT NULL,
                    entity TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    embedding BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Clusters table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clusters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    qa_pair_id INTEGER NOT NULL,
                    cluster_id INTEGER NOT NULL,
                    distance_to_center REAL NOT NULL,
                    FOREIGN KEY (qa_pair_id) REFERENCES qa_pairs (id)
                )
            """)
            
            # System metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def save_qa_pair(self, qa_pair: QAPair) -> int:
        """Save a QA pair to database and return its ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Convert embedding to bytes if present
            embedding_bytes = None
            if qa_pair.embedding is not None:
                embedding_bytes = qa_pair.embedding.tobytes()
            
            cursor.execute("""
                INSERT INTO qa_pairs 
                (topic, example, passage, entity, question, answer, explanation, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                qa_pair.topic, qa_pair.example, qa_pair.passage,
                qa_pair.entity, qa_pair.question, qa_pair.answer,
                qa_pair.explanation, embedding_bytes
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_qa_pairs(self, topic: Optional[str] = None, limit: Optional[int] = None) -> List[QAPair]:
        """Retrieve QA pairs from database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM qa_pairs"
            params = []
            
            if topic:
                query += " WHERE topic = ?"
                params.append(topic)
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            qa_pairs = []
            for row in rows:
                embedding = None
                if row[8]:  # embedding column
                    embedding = np.frombuffer(row[8], dtype=np.float32)
                
                qa_pair = QAPair(
                    id=row[0], topic=row[1], example=row[2], passage=row[3],
                    entity=row[4], question=row[5], answer=row[6],
                    explanation=row[7], embedding=embedding, created_at=row[9]
                )
                qa_pairs.append(qa_pair)
            
            return qa_pairs
    
    def update_embedding(self, qa_pair_id: int, embedding: np.ndarray):
        """Update embedding for a QA pair"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            embedding_bytes = embedding.tobytes()
            
            cursor.execute("""
                UPDATE qa_pairs SET embedding = ? WHERE id = ?
            """, (embedding_bytes, qa_pair_id))
            
            conn.commit()
    
    def save_cluster_info(self, cluster_info: ClusterInfo):
        """Save cluster information"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO clusters 
                (qa_pair_id, cluster_id, distance_to_center)
                VALUES (?, ?, ?)
            """, (cluster_info.qa_pair_id, cluster_info.cluster_id, 
                  cluster_info.distance_to_center))
            
            conn.commit()
    
    def get_cluster_info(self, cluster_id: Optional[int] = None) -> List[ClusterInfo]:
        """Get cluster information"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM clusters"
            params = []
            
            if cluster_id is not None:
                query += " WHERE cluster_id = ?"
                params.append(cluster_id)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [ClusterInfo(id=row[0], qa_pair_id=row[1], 
                               cluster_id=row[2], distance_to_center=row[3])
                    for row in rows]
    
    def get_dataset_stats(self) -> Dict[str, int]:
        """Get statistics about the generated dataset"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total QA pairs
            cursor.execute("SELECT COUNT(*) FROM qa_pairs")
            total_pairs = cursor.fetchone()[0]
            
            # QA pairs by topic
            cursor.execute("SELECT topic, COUNT(*) FROM qa_pairs GROUP BY topic")
            topic_counts = dict(cursor.fetchall())
            
            return {
                "total_pairs": total_pairs,
                "topic_counts": topic_counts
            }
    
    def clear_database(self):
        """Clear all data from database (for testing/reset)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clusters")
            cursor.execute("DELETE FROM qa_pairs")
            cursor.execute("DELETE FROM system_metadata")
            conn.commit()
