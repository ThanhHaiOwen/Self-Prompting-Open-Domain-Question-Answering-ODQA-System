'use client';

import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, Clock, RefreshCw } from 'lucide-react';
import { SystemStatus as SystemStatusType } from '@/types';
import { api, handleApiError } from '@/lib/api';
import { formatNumber } from '@/lib/utils';

export default function SystemStatus() {
  const [status, setStatus] = useState<SystemStatusType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [preparing, setPreparing] = useState(false);

  const fetchStatus = async () => {
    try {
      setLoading(true);
      const response = await api.getStatus();
      setStatus(response.data);
      setError(null);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const handlePrepareSystem = async (forceRegenerate: boolean = false) => {
    try {
      setPreparing(true);
      await api.prepareSystem(forceRegenerate);
      
      // Poll for status updates
      const pollInterval = setInterval(async () => {
        try {
          const response = await api.getStatus();
          setStatus(response.data);
          
          if (response.data.system_ready) {
            clearInterval(pollInterval);
            setPreparing(false);
          }
        } catch (err) {
          console.error('Error polling status:', err);
        }
      }, 5000);

      // Stop polling after 10 minutes
      setTimeout(() => {
        clearInterval(pollInterval);
        setPreparing(false);
      }, 600000);
      
    } catch (err) {
      setError(handleApiError(err));
      setPreparing(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  if (loading && !status) {
    return (
      <div className="card">
        <div className="flex items-center space-x-2">
          <RefreshCw className="w-5 h-5 animate-spin" />
          <span>Loading system status...</span>
        </div>
      </div>
    );
  }

  if (error && !status) {
    return (
      <div className="card border-red-200 bg-red-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-red-700">
            <XCircle className="w-5 h-5" />
            <span>Error loading system status: {error}</span>
          </div>
          <button onClick={fetchStatus} className="btn-secondary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  const getStatusIndicator = (ready: boolean) => {
    if (preparing) {
      return <span className="status-preparing">Preparing</span>;
    }
    return ready ? (
      <span className="status-ready">Ready</span>
    ) : (
      <span className="status-not-ready">Not Ready</span>
    );
  };

  return (
    <div className="space-y-4">
      {/* Main Status */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            {status?.system_ready ? (
              <CheckCircle className="w-6 h-6 text-green-600" />
            ) : (
              <Clock className="w-6 h-6 text-yellow-600" />
            )}
            <div>
              <h2 className="text-lg font-semibold">System Status</h2>
              {getStatusIndicator(status?.system_ready || false)}
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={fetchStatus}
              disabled={loading}
              className="btn-secondary"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            
            {!status?.system_ready && (
              <button
                onClick={() => handlePrepareSystem(false)}
                disabled={preparing}
                className="btn-primary"
              >
                {preparing ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    Preparing...
                  </>
                ) : (
                  'Prepare System'
                )}
              </button>
            )}
          </div>
        </div>

        {/* Component Status */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          {status?.components_status && Object.entries(status.components_status).map(([component, ready]) => (
            <div key={component} className="flex items-center space-x-2">
              {ready ? (
                <CheckCircle className="w-4 h-4 text-green-600" />
              ) : (
                <XCircle className="w-4 h-4 text-red-600" />
              )}
              <span className="text-sm capitalize">{component.replace('_', ' ')}</span>
            </div>
          ))}
        </div>

        {/* Dataset Stats */}
        {status?.dataset_stats && (
          <div className="border-t pt-4">
            <h3 className="font-medium mb-2">Dataset Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Total QA Pairs:</span>
                <span className="ml-2 font-medium">{formatNumber(status.dataset_stats.total_pairs)}</span>
              </div>
              <div>
                <span className="text-gray-600">Topics:</span>
                <span className="ml-2 font-medium">{Object.keys(status.dataset_stats.topic_counts).length}</span>
              </div>
              <div>
                <span className="text-gray-600">Clusters:</span>
                <span className="ml-2 font-medium">{status.clustering_stats.n_clusters}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Advanced Options */}
      {status?.system_ready && (
        <div className="card border-yellow-200 bg-yellow-50">
          <h3 className="font-medium mb-2 text-yellow-800">Advanced Options</h3>
          <p className="text-sm text-yellow-700 mb-3">
            Regenerate the entire dataset and clustering. This will take several minutes.
          </p>
          <button
            onClick={() => handlePrepareSystem(true)}
            disabled={preparing}
            className="btn-secondary"
          >
            {preparing ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                Regenerating...
              </>
            ) : (
              'Regenerate Dataset'
            )}
          </button>
        </div>
      )}
    </div>
  );
}
