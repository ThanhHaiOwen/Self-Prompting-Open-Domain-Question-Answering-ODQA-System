"""
Clustering-based Retrieval System for Self-Prompting ODQA
Implements the inference stage demonstration selection from the research paper
"""

import numpy as np
import logging
from typing import List, Dict, Tuple, Optional
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from config import DEFAULT_CLUSTERS, MAX_DEMONSTRATIONS, SENTENCE_TRANSFORMER_MODEL
from database import DatabaseManager, QAPair, ClusterInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClusteringRetrieval:
    """Handles clustering-based retrieval for demonstration selection"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.sentence_model = None
        self.clusters_computed = False
        self.cluster_centers = None
        self.kmeans_model = None
        
    def initialize_sentence_model(self):
        """Initialize the sentence transformer model"""
        if self.sentence_model is None:
            logger.info(f"Loading sentence transformer model: {SENTENCE_TRANSFORMER_MODEL}")
            self.sentence_model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
            logger.info("Sentence transformer model loaded successfully")
    
    def compute_embeddings(self, force_recompute: bool = False) -> int:
        """Compute embeddings for all QA pairs in the database"""
        self.initialize_sentence_model()
        
        # Get QA pairs without embeddings or all if force recompute
        if force_recompute:
            qa_pairs = self.db.get_qa_pairs()
        else:
            # Get pairs that don't have embeddings yet
            qa_pairs = [qa for qa in self.db.get_qa_pairs() if qa.embedding is None]
        
        if not qa_pairs:
            logger.info("All QA pairs already have embeddings")
            return 0
        
        logger.info(f"Computing embeddings for {len(qa_pairs)} QA pairs")
        
        # Prepare texts for embedding (combine question and answer)
        texts = []
        for qa_pair in qa_pairs:
            # Combine question and answer as per paper methodology
            text = f"{qa_pair.question} {qa_pair.answer}"
            texts.append(text)
        
        # Compute embeddings in batches
        batch_size = 32
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = self.sentence_model.encode(batch_texts)
            embeddings.extend(batch_embeddings)
            
            if (i // batch_size + 1) % 10 == 0:
                logger.info(f"Processed {i + len(batch_texts)} / {len(texts)} embeddings")
        
        # Update database with embeddings
        for qa_pair, embedding in zip(qa_pairs, embeddings):
            self.db.update_embedding(qa_pair.id, embedding.astype(np.float32))
        
        logger.info(f"Successfully computed and saved {len(embeddings)} embeddings")
        return len(embeddings)
    
    def perform_clustering(self, n_clusters: int = DEFAULT_CLUSTERS, force_recompute: bool = False) -> Dict[str, any]:
        """Perform k-means clustering on QA pair embeddings"""
        if self.clusters_computed and not force_recompute:
            logger.info("Clusters already computed")
            return self.get_clustering_stats()
        
        # Get all QA pairs with embeddings
        qa_pairs = [qa for qa in self.db.get_qa_pairs() if qa.embedding is not None]
        
        if len(qa_pairs) < n_clusters:
            logger.warning(f"Not enough QA pairs ({len(qa_pairs)}) for {n_clusters} clusters")
            n_clusters = max(1, len(qa_pairs))
        
        logger.info(f"Performing k-means clustering with {n_clusters} clusters on {len(qa_pairs)} QA pairs")
        
        # Prepare embeddings matrix
        embeddings = np.array([qa.embedding for qa in qa_pairs])
        
        # Perform k-means clustering
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = self.kmeans_model.fit_predict(embeddings)
        self.cluster_centers = self.kmeans_model.cluster_centers_
        
        # Calculate distances to cluster centers
        distances = []
        for i, embedding in enumerate(embeddings):
            cluster_id = cluster_labels[i]
            center = self.cluster_centers[cluster_id]
            distance = np.linalg.norm(embedding - center)
            distances.append(distance)
        
        # Clear existing cluster information
        # Note: In a production system, you might want to version this
        
        # Save cluster information to database
        for qa_pair, cluster_id, distance in zip(qa_pairs, cluster_labels, distances):
            cluster_info = ClusterInfo(
                qa_pair_id=qa_pair.id,
                cluster_id=int(cluster_id),
                distance_to_center=float(distance)
            )
            self.db.save_cluster_info(cluster_info)
        
        self.clusters_computed = True
        
        stats = {
            "n_clusters": n_clusters,
            "total_qa_pairs": len(qa_pairs),
            "cluster_sizes": np.bincount(cluster_labels).tolist()
        }
        
        logger.info(f"Clustering completed: {stats}")
        return stats
    
    def get_clustering_stats(self) -> Dict[str, any]:
        """Get statistics about current clustering"""
        cluster_info = self.db.get_cluster_info()
        
        if not cluster_info:
            return {"n_clusters": 0, "total_qa_pairs": 0, "cluster_sizes": []}
        
        cluster_ids = [info.cluster_id for info in cluster_info]
        n_clusters = max(cluster_ids) + 1 if cluster_ids else 0
        cluster_sizes = np.bincount(cluster_ids).tolist()
        
        return {
            "n_clusters": n_clusters,
            "total_qa_pairs": len(cluster_info),
            "cluster_sizes": cluster_sizes
        }
    
    def select_demonstrations(self, question: str, n_demonstrations: int = MAX_DEMONSTRATIONS) -> List[QAPair]:
        """Select demonstrations using clustering-based retrieval"""
        self.initialize_sentence_model()
        
        # Get clustering stats
        stats = self.get_clustering_stats()
        n_clusters = stats["n_clusters"]
        
        if n_clusters == 0:
            logger.warning("No clusters found. Performing clustering first.")
            self.perform_clustering()
            stats = self.get_clustering_stats()
            n_clusters = stats["n_clusters"]
        
        if n_clusters == 0:
            logger.error("Still no clusters after clustering. Cannot select demonstrations.")
            return []
        
        # Encode the question
        question_embedding = self.sentence_model.encode([question])[0]
        
        # Get one demonstration from each cluster (or as many as requested)
        demonstrations = []
        clusters_to_sample = min(n_demonstrations, n_clusters)
        
        for cluster_id in range(clusters_to_sample):
            demo = self.select_from_cluster(question_embedding, cluster_id)
            if demo:
                demonstrations.append(demo)
        
        # If we need more demonstrations and have fewer clusters, 
        # get additional ones from clusters with most similar examples
        if len(demonstrations) < n_demonstrations:
            additional_needed = n_demonstrations - len(demonstrations)
            additional_demos = self.select_additional_demonstrations(
                question_embedding, demonstrations, additional_needed
            )
            demonstrations.extend(additional_demos)
        
        logger.info(f"Selected {len(demonstrations)} demonstrations for question: {question[:50]}...")
        return demonstrations
    
    def select_from_cluster(self, question_embedding: np.ndarray, cluster_id: int) -> Optional[QAPair]:
        """Select the most similar QA pair from a specific cluster"""
        # Get all QA pairs in this cluster
        cluster_info = self.db.get_cluster_info(cluster_id)
        
        if not cluster_info:
            return None
        
        qa_pair_ids = [info.qa_pair_id for info in cluster_info]
        qa_pairs = []
        
        # Get QA pairs with embeddings
        for qa_pair in self.db.get_qa_pairs():
            if qa_pair.id in qa_pair_ids and qa_pair.embedding is not None:
                qa_pairs.append(qa_pair)
        
        if not qa_pairs:
            return None
        
        # Calculate similarities
        similarities = []
        for qa_pair in qa_pairs:
            similarity = cosine_similarity(
                question_embedding.reshape(1, -1),
                qa_pair.embedding.reshape(1, -1)
            )[0][0]
            similarities.append(similarity)
        
        # Return the most similar QA pair
        best_idx = np.argmax(similarities)
        return qa_pairs[best_idx]
    
    def select_additional_demonstrations(self, question_embedding: np.ndarray, 
                                       existing_demos: List[QAPair], 
                                       n_additional: int) -> List[QAPair]:
        """Select additional demonstrations globally by similarity"""
        # Get all QA pairs with embeddings, excluding already selected ones
        existing_ids = {demo.id for demo in existing_demos}
        all_qa_pairs = [qa for qa in self.db.get_qa_pairs() 
                       if qa.embedding is not None and qa.id not in existing_ids]
        
        if not all_qa_pairs:
            return []
        
        # Calculate similarities
        similarities = []
        for qa_pair in all_qa_pairs:
            similarity = cosine_similarity(
                question_embedding.reshape(1, -1),
                qa_pair.embedding.reshape(1, -1)
            )[0][0]
            similarities.append((similarity, qa_pair))
        
        # Sort by similarity and take top n_additional
        similarities.sort(key=lambda x: x[0], reverse=True)
        additional_demos = [qa_pair for _, qa_pair in similarities[:n_additional]]
        
        return additional_demos
    
    def prepare_system(self) -> Dict[str, any]:
        """Prepare the entire clustering retrieval system"""
        logger.info("Preparing clustering retrieval system...")
        
        # Step 1: Compute embeddings
        embeddings_computed = self.compute_embeddings()
        
        # Step 2: Perform clustering
        clustering_stats = self.perform_clustering()
        
        result = {
            "embeddings_computed": embeddings_computed,
            "clustering_stats": clustering_stats,
            "system_ready": clustering_stats["n_clusters"] > 0
        }
        
        logger.info(f"System preparation complete: {result}")
        return result
