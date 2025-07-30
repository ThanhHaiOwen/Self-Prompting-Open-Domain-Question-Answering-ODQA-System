'use client';

import React, { useState, useEffect } from 'react';
import { Database, Eye, RefreshCw, Filter } from 'lucide-react';
import { DatasetSample, TopicsConfig, SystemStatus } from '@/types';
import { apiClient, handleApiError } from '@/lib/api';
import { truncateText } from '@/lib/utils';

export default function DatasetViewer() {
  const [samples, setSamples] = useState<DatasetSample[]>([]);
  const [topics, setTopics] = useState<TopicsConfig | null>(null);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [selectedTopic, setSelectedTopic] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [limit, setLimit] = useState(10);

  const fetchTopics = async () => {
    try {
      const [topicsData, statusData] = await Promise.all([
        apiClient.getTopics(),
        apiClient.getSystemStatus()
      ]);
      setTopics(topicsData);
      setSystemStatus(statusData);
    } catch (err) {
      console.error('Error fetching topics:', err);
    }
  };

  const fetchSamples = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const samplesData = await apiClient.getDatasetSample(
        selectedTopic || undefined,
        limit
      );
      setSamples(samplesData);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTopics();
  }, []);

  useEffect(() => {
    fetchSamples();
  }, [selectedTopic, limit]);

  // Only show topics that have actual data (count > 0)
  const topicOptions = systemStatus?.dataset_stats?.topic_counts
    ? Object.keys(systemStatus.dataset_stats.topic_counts)
        .filter(topic => systemStatus.dataset_stats.topic_counts[topic] > 0)
        .sort()
    : [];

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold flex items-center">
            <Database className="w-5 h-5 mr-2" />
            Dataset Viewer
          </h2>
          
          <button
            onClick={fetchSamples}
            disabled={loading}
            className="btn-secondary"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-4 mb-4">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <label htmlFor="topic-filter" className="text-sm font-medium text-gray-700">
              Topic:
            </label>
            <select
              id="topic-filter"
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="input-field w-48"
              disabled={loading}
            >
              <option value="">All Topics</option>
              {topicOptions.map(topic => (
                <option key={topic} value={topic}>
                  {topic} ({systemStatus?.dataset_stats?.topic_counts[topic] || 0})
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <label htmlFor="limit-filter" className="text-sm font-medium text-gray-700">
              Limit:
            </label>
            <select
              id="limit-filter"
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="input-field w-20"
              disabled={loading}
            >
              {[5, 10, 20, 50].map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Dataset Stats */}
        {systemStatus && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
            <div>
              <span className="text-sm text-gray-600">Total Topics:</span>
              <span className="ml-2 font-medium">{topicOptions.length}</span>
            </div>
            <div>
              <span className="text-sm text-gray-600">Total QA Pairs:</span>
              <span className="ml-2 font-medium">{systemStatus.dataset_stats?.total_pairs || 0}</span>
            </div>
            <div>
              <span className="text-sm text-gray-600">Showing:</span>
              <span className="ml-2 font-medium">{samples.length} samples</span>
            </div>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="card border-red-200 bg-red-50">
          <div className="flex items-center space-x-2 text-red-700">
            <Eye className="w-5 h-5" />
            <span>Error loading dataset: {error}</span>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="card">
          <div className="flex items-center justify-center py-8">
            <RefreshCw className="w-6 h-6 animate-spin mr-2" />
            <span>Loading dataset samples...</span>
          </div>
        </div>
      )}

      {/* Dataset Samples */}
      {!loading && samples.length > 0 && (
        <div className="space-y-4">
          {samples.map((sample, index) => (
            <div key={index} className="card">
              <div className="flex items-center justify-between mb-3">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                  {sample.topic}
                </span>
              </div>

              <div className="space-y-3">
                {/* Question */}
                <div>
                  <span className="text-sm font-medium text-gray-600">Question:</span>
                  <p className="mt-1 text-gray-900">{sample.question}</p>
                </div>

                {/* Answer */}
                <div>
                  <span className="text-sm font-medium text-gray-600">Answer:</span>
                  <p className="mt-1 font-medium text-primary-700">{sample.answer}</p>
                </div>

                {/* Explanation */}
                <div>
                  <span className="text-sm font-medium text-gray-600">Explanation:</span>
                  <p className="mt-1 text-gray-700 text-sm">{sample.explanation}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && samples.length === 0 && !error && (
        <div className="card">
          <div className="text-center py-8">
            <Database className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No samples found</h3>
            <p className="text-gray-600">
              {selectedTopic 
                ? `No samples found for topic "${selectedTopic}". Try selecting a different topic.`
                : 'No dataset samples available. Make sure the system is prepared first.'
              }
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
