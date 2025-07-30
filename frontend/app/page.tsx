'use client';

import React, { useState } from 'react';
import { Brain, Settings, Database, MessageSquare, Github, BookOpen } from 'lucide-react';
import SystemStatus from '@/components/SystemStatus';
import QuestionAnswering from '@/components/QuestionAnswering';
import DatasetViewer from '@/components/DatasetViewer';

type TabType = 'qa' | 'status' | 'dataset';

export default function Home() {
  const [activeTab, setActiveTab] = useState<TabType>('qa');

  const tabs = [
    { id: 'qa' as TabType, label: 'Question Answering', icon: MessageSquare },
    { id: 'status' as TabType, label: 'System Status', icon: Settings },
    { id: 'dataset' as TabType, label: 'Dataset Viewer', icon: Database },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'qa':
        return <QuestionAnswering />;
      case 'status':
        return <SystemStatus />;
      case 'dataset':
        return <DatasetViewer />;
      default:
        return <QuestionAnswering />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Brain className="w-8 h-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Self-Prompting ODQA System
                </h1>
                <p className="text-sm text-gray-600">
                  Zero-Shot Open-Domain Question Answering
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <a
                href="https://arxiv.org/abs/2212.08029"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors"
              >
                <BookOpen className="w-4 h-4" />
                <span className="text-sm">Research Paper</span>
              </a>
              
              <a
                href="https://github.com/lockon-n/self-prompting"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors"
              >
                <Github className="w-4 h-4" />
                <span className="text-sm">Original Code</span>
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Description */}
        <div className="card mb-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Self-Prompting for Zero-Shot ODQA
            </h2>
            <p className="text-gray-600 max-w-3xl mx-auto">
              This system implements the complete Self-Prompting framework from the research paper 
              "Self-Prompting Large Language Models for Zero-Shot Open-Domain QA". It generates 
              pseudo QA datasets automatically and uses clustering-based retrieval for in-context 
              learning, powered by Google's Gemini API.
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="mb-8">
          <nav className="flex space-x-1 bg-white rounded-lg p-1 shadow-sm border">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="min-h-[600px]">
          {renderTabContent()}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">
              Implementation of "Self-Prompting Large Language Models for Zero-Shot Open-Domain QA"
            </p>
            <p className="text-sm">
              Li, J., Wang, J., Zhang, Z., & Zhao, H. (2022) • 
              Powered by Google Gemini API
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
