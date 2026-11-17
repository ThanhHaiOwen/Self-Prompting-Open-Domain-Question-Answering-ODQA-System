import axios, { AxiosError } from 'axios';
import { QuestionResponse, SystemStatus, TopicsConfig } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 120s to allow Render free tier cold-start
});

export const api = {
  // Ask a question
  askQuestion: (question: string, nDemonstrations: number = 10) => {
    return client.post<QuestionResponse>('/ask', {
      question,
      n_demonstrations: nDemonstrations,
    });
  },

  // Get current system status
  getStatus: () => {
    return client.get<SystemStatus>('/status');
  },

  // Get topic configuration
  getTopics: () => {
    return client.get<TopicsConfig>('/topics');
  },

  // Get sample questions
  getSampleQuestions: () => {
    return client.get<{ sample_questions: string[] }>('/sample-questions');
  },

  // Get dataset sample
  getDataset: (limit: number = 10, topic?: string) => {
    return client.post('/dataset-sample', {
      topic: topic || null,
      limit,
    });
  },

  // Trigger system preparation
  prepareSystem: (forceRegenerate: boolean = false) => {
    return client.post('/prepare', {
      force_regenerate: forceRegenerate,
    });
  },

  // Health check
  getHealth: () => {
    return client.get('/health');
  },
};

export function handleApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: string; error?: string }>;
    if (axiosError.response?.data?.detail) {
      return axiosError.response.data.detail;
    }
    if (axiosError.response?.data?.error) {
      return axiosError.response.data.error;
    }
    if (axiosError.message) {
      return axiosError.message;
    }
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected error occurred while communicating with the API.';
}
