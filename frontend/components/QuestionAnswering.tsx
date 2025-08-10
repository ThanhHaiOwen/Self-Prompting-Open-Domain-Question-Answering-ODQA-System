'use client';

import React, { useState, useEffect } from 'react';
import { Send, Loader2, HelpCircle, Clock, Target, MessageSquare } from 'lucide-react';
import { QuestionResponse } from '@/types';
import { api, handleApiError } from '@/lib/api';
import { formatTime } from '@/lib/utils';

export default function QuestionAnswering() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QuestionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [sampleQuestions, setSampleQuestions] = useState<string[]>([]);
  const [nDemonstrations, setNDemonstrations] = useState(10);

  const fetchSampleQuestions = async () => {
    try {
      const response = await api.getDataset(5);
      const samples = response.data.sample || response.data.samples || response.data;
      const questions = samples.map((item: any) => item.question);
      setSampleQuestions(questions);
    } catch (err) {
      console.error('Error fetching sample questions:', err);
    }
  };

  useEffect(() => {
    fetchSampleQuestions();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setResult(null);

      const response = await api.askQuestion(question.trim());

      setResult(response.data);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleSampleQuestionClick = (sampleQuestion: string) => {
    setQuestion(sampleQuestion);
    setResult(null);
    setError(null);
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600 bg-green-100';
    if (confidence >= 0.6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div className="space-y-6">
      {/* Question Input */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4 flex items-center">
          <MessageSquare className="w-5 h-5 mr-2" />
          Ask a Question
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
              Your Question
            </label>
            <textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Enter your question here... (e.g., Who was the first person to walk on the moon?)"
              className="input-field h-24 resize-none"
              disabled={loading}
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <label htmlFor="demonstrations" className="text-sm font-medium text-gray-700">
                Demonstrations:
              </label>
              <select
                id="demonstrations"
                value={nDemonstrations}
                onChange={(e) => setNDemonstrations(Number(e.target.value))}
                className="input-field w-20"
                disabled={loading}
              >
                {[5, 8, 10, 12, 15].map(num => (
                  <option key={num} value={num}>{num}</option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="btn-primary"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Ask Question
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Sample Questions */}
      {sampleQuestions.length > 0 && (
        <div className="card">
          <h3 className="font-medium mb-3 flex items-center">
            <HelpCircle className="w-4 h-4 mr-2" />
            Sample Questions
          </h3>
          <div className="space-y-2">
            {sampleQuestions.map((sampleQuestion, index) => (
              <button
                key={index}
                onClick={() => handleSampleQuestionClick(sampleQuestion)}
                className="text-left w-full p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors duration-200"
                disabled={loading}
              >
                <span className="text-sm text-primary-600">{sampleQuestion}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="card border-red-200 bg-red-50">
          <div className="flex items-center space-x-2 text-red-700">
            <HelpCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="card">
          <h3 className="font-semibold mb-4">Answer</h3>
          
          {/* Question */}
          <div className="mb-4 p-3 bg-gray-50 rounded-lg">
            <span className="text-sm font-medium text-gray-600">Question:</span>
            <p className="mt-1">{result.question}</p>
          </div>

          {/* Answer */}
          <div className="mb-4 p-4 bg-primary-50 rounded-lg border border-primary-200">
            <span className="text-sm font-medium text-primary-700">Answer:</span>
            <p className="mt-1 text-lg font-medium text-primary-900">{result.answer}</p>
          </div>

          {/* Explanation */}
          {result.explanation && (
            <div className="mb-4 p-3 bg-blue-50 rounded-lg">
              <span className="text-sm font-medium text-blue-700">Explanation:</span>
              <p className="mt-1 text-blue-900">{result.explanation}</p>
            </div>
          )}

          {/* Metadata */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
            <div className="flex items-center space-x-2">
              <Target className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">Confidence:</span>
              <span className={`text-sm px-2 py-1 rounded-full ${getConfidenceColor(result.confidence)}`}>
                {Math.round(result.confidence * 100)}%
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">Time:</span>
              <span className="text-sm font-medium">{formatTime(result.processing_time)}</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <MessageSquare className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">Demonstrations:</span>
              <span className="text-sm font-medium">{result.demonstrations_used}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
