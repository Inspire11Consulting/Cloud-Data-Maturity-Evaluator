import React from 'react';
import { 
  BarChart3, 
  Lightbulb, 
  Database, 
  GitBranch, 
  PieChart, 
  X,
  Home,
  Map
} from 'lucide-react';
import { Button } from './ui/button';
import { PageType } from '../App';

interface SidebarProps {
  isOpen: boolean;
  onNavigate: (page: PageType) => void;
  currentPage: PageType;
}

const menuItems = [
  { id: 'dashboard', label: 'Home', icon: Home, color: 'bg-blue-100 text-blue-700 hover:bg-blue-200' },
  { id: 'maturity-tool', label: 'Maturity Tool', icon: BarChart3, color: 'bg-blue-100 text-blue-700 hover:bg-blue-200' },
  { id: 'poc-starter', label: 'PoC Starter Kit', icon: Lightbulb, color: 'bg-green-100 text-green-700 hover:bg-green-200' },
  { id: 'data-model', label: 'Data Model Generator', icon: Database, color: 'bg-purple-100 text-purple-700 hover:bg-purple-200' },
  { id: 'metadata-mapper', label: 'Metadata Driven Mapper', icon: Map, color: 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200' },
  { id: 'pipeline', label: 'Pipeline Generator', icon: GitBranch, color: 'bg-teal-100 text-teal-700 hover:bg-teal-200' },
  { id: 'powerbi', label: 'Power BI Generator', icon: PieChart, color: 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200' },
];

export function Sidebar({ isOpen, onNavigate, currentPage }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-gray-800 bg-opacity-30 z-40 lg:hidden"
          onClick={() => onNavigate(currentPage)}
        />
      )}
      
      {/* Sidebar */}
      <div className={`
        fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 
        transform transition-transform duration-300 ease-in-out pt-16 lg:pt-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="p-4">
          <div className="flex items-center justify-between mb-6 lg:hidden">
            <h3 className="text-lg font-semibold text-gray-900">Menu</h3>
            <Button variant="ghost" size="sm" onClick={() => onNavigate(currentPage)}>
              <X className="h-5 w-5" />
            </Button>
          </div>
          
          <nav className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentPage === item.id;
              
              return (
                <Button
                  key={item.id}
                  variant={isActive ? "default" : "ghost"}
                  className={`w-full justify-start space-x-3 ${
                    isActive ? item.color : 'text-gray-700 hover:bg-gray-100'
                  }`}
                  onClick={() => onNavigate(item.id as PageType)}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Button>
              );
            })}
          </nav>
        </div>
      </div>
    </>
  );
}