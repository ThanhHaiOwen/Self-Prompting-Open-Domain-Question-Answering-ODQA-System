#!/usr/bin/env python3
"""
Prepare clustering system for existing dataset
"""

import sys
import os
sys.path.append('backend')

from backend.database import DatabaseManager
from backend.clustering_retrieval import ClusteringRetrieval

def prepare_clustering():
    """Prepare clustering system for the existing dataset"""
    print("Preparing clustering system...")
    
    # Initialize components
    db = DatabaseManager()
    clustering = ClusteringRetrieval(db)
    
    # Check current dataset
    stats = db.get_dataset_stats()
    print(f"Current dataset: {stats}")
    
    if stats['total_pairs'] == 0:
        print("No QA pairs found in database. Please run create_sample_dataset.py first.")
        return False
    
    # Prepare clustering
    try:
        result = clustering.prepare_system()
        print(f"Clustering preparation result: {result}")
        
        if result.get('system_ready'):
            print("✅ Clustering system is ready!")
            return True
        else:
            print("❌ Clustering system preparation failed")
            return False
            
    except Exception as e:
        print(f"Error preparing clustering: {e}")
        return False

if __name__ == "__main__":
    success = prepare_clustering()
    sys.exit(0 if success else 1)
