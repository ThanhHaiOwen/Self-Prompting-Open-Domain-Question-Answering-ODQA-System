// Type definitions for the Self-Prompting ODQA System

export interface SystemStatus {
  system_ready: boolean;
  dataset_stats: {
    total_pairs: number;
    topic_counts: Record<string, number>;
  };
  clustering_stats: {
    n_clusters: number;
    total_qa_pairs: number;
    cluster_sizes: number[];
  };
  components_status: {
    database: boolean;
    gemini_client: boolean;
    clustering: boolean;
    dataset: boolean;
  };
}

export interface QuestionRequest {
  question: string;
  n_demonstrations?: number;
}

export interface QuestionResponse {
  question: string;
  answer: string;
  explanation?: string;
  confidence: number;
  demonstrations_used: number;
  processing_time: number;
  error?: string;
}

export interface DatasetSample {
  topic: string;
  question: string;
  answer: string;
  explanation: string;
}

export interface TopicsConfig {
  topics: Record<string, number>;
  total_topics: number;
  total_target_pairs: number;
}

export interface PreparationProgress {
  total_generated: number;
  total_target: number;
  progress_percentage: number;
  topic_breakdown: Record<string, number>;
}
