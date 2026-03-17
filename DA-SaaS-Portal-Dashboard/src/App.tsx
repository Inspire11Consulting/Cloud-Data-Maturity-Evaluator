import React, { useState } from 'react';
import { Dashboard } from './components/Dashboard';
import { MaturityTool } from './components/features/MaturityTool';
import { PocStarterKit } from './components/features/PocStarterKit';
import { DataModelGenerator } from './components/features/DataModelGenerator';
import { MetadataMapper } from './components/features/MetadataMapper';
import { PipelineGenerator } from './components/features/PipelineGenerator';
import { PowerBIGenerator } from './components/features/PowerBIGenerator';
import { Navigation } from './components/Navigation';
import { Sidebar } from './components/Sidebar';

export type PageType = 'dashboard' | 'maturity-tool' | 'poc-starter' | 'data-model' | 'metadata-mapper' | 'pipeline' | 'powerbi';

export default function App() {
  const [currentPage, setCurrentPage] = useState<PageType>('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const renderPage = () => {
    switch (currentPage) {
      case 'maturity-tool':
        return <MaturityTool onNavigateBack={() => setCurrentPage('dashboard')} />;
      case 'poc-starter':
        return <PocStarterKit onNavigateBack={() => setCurrentPage('dashboard')} />;
      case 'data-model':
        return <DataModelGenerator onNavigateBack={() => setCurrentPage('dashboard')} />;
      case 'metadata-mapper':
        return <MetadataMapper onNavigateBack={() => setCurrentPage('dashboard')} />;
      case 'pipeline':
        return <PipelineGenerator onNavigateBack={() => setCurrentPage('dashboard')} />;
      case 'powerbi':
        return <PowerBIGenerator onNavigateBack={() => setCurrentPage('dashboard')} />;
      default:
        return <Dashboard onNavigate={setCurrentPage} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation 
        onMenuClick={() => setSidebarOpen(!sidebarOpen)}
        onNavigate={setCurrentPage}
      />
      
      <div className="flex">
        <Sidebar 
          isOpen={sidebarOpen}
          onNavigate={setCurrentPage}
          currentPage={currentPage}
        />
        
        <main className="flex-1 transition-all duration-300">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}