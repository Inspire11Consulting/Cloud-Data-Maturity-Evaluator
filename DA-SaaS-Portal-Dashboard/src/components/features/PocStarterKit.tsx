import React, { useState } from 'react';
import { ArrowLeft, Lightbulb, Zap, Database } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Textarea } from '../ui/textarea';
import { Label } from '../ui/label';
import { Separator } from '../ui/separator';
import { Badge } from '../ui/badge';

interface PocStarterKitProps {
  onNavigateBack: () => void;
}

export function PocStarterKit({ onNavigateBack }: PocStarterKitProps) {
  const [formData, setFormData] = useState({
    projectNotes: '',
    painPoints: '',
    existingKPIs: '',
  });

  const mockGeneratedKPIs = [
    { category: 'Operational Efficiency', kpi: 'Process Automation Rate', target: '85%' },
    { category: 'Customer Experience', kpi: 'Customer Satisfaction Score', target: '4.5/5' },
    { category: 'Data Quality', kpi: 'Data Accuracy Rate', target: '99.5%' },
    { category: 'Performance', kpi: 'System Response Time', target: '< 2 seconds' },
  ];

  const mockDataSources = [
    'Customer Transaction Database',
    'Product Inventory System',
    'Marketing Campaign Data',
    'Support Ticket System',
    'Financial Reporting Database',
  ];

  return (
    <div className="p-6 lg:p-8">
      {/* Header */}
      <div className="flex items-center mb-6">
        <Button
          variant="ghost"
          onClick={onNavigateBack}
          className="mr-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>
        
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
            <Lightbulb className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">D&A PoC Starter Kit</h1>
            <p className="text-gray-600">Accelerate your proof of concept development</p>
          </div>
        </div>
      </div>

      <Separator className="mb-8" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Project Requirements</CardTitle>
              <CardDescription>
                Provide details about your PoC requirements and objectives
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="projectNotes">Project Notes & Objectives</Label>
                <Textarea
                  id="projectNotes"
                  value={formData.projectNotes}
                  onChange={(e) => setFormData(prev => ({ ...prev, projectNotes: e.target.value }))}
                  placeholder="Describe your project goals, scope, and key requirements..."
                  rows={4}
                />
              </div>
              
              <div>
                <Label htmlFor="painPoints">Current Pain Points</Label>
                <Textarea
                  id="painPoints"
                  value={formData.painPoints}
                  onChange={(e) => setFormData(prev => ({ ...prev, painPoints: e.target.value }))}
                  placeholder="What challenges are you trying to solve? What processes need improvement?"
                  rows={4}
                />
              </div>
              
              <div>
                <Label htmlFor="existingKPIs">Existing KPIs (Optional)</Label>
                <Textarea
                  id="existingKPIs"
                  value={formData.existingKPIs}
                  onChange={(e) => setFormData(prev => ({ ...prev, existingKPIs: e.target.value }))}
                  placeholder="List any existing KPIs you want to track or improve..."
                  rows={3}
                />
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4">
            <Button className="bg-green-600 hover:bg-green-700">
              <Zap className="h-4 w-4 mr-2" />
              Generate PoC Framework
            </Button>
            
            <Button variant="outline">
              <Database className="h-4 w-4 mr-2" />
              Generate Mock Data
            </Button>
          </div>
        </div>

        {/* Generated Content Section */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>AI-Generated KPIs</CardTitle>
              <CardDescription>
                Recommended KPIs based on your project requirements
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockGeneratedKPIs.map((kpi, index) => (
                  <div key={index} className="border rounded-lg p-4 bg-gray-50">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-medium text-gray-900">{kpi.kpi}</h4>
                      <Badge variant="secondary">{kpi.category}</Badge>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">Target: {kpi.target}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Suggested Data Sources</CardTitle>
              <CardDescription>
                Potential data sources for your PoC based on common patterns
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {mockDataSources.map((source, index) => (
                  <div key={index} className="flex items-center space-x-3 p-2 rounded border">
                    <Database className="h-4 w-4 text-blue-500" />
                    <span className="text-sm">{source}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Implementation Phases</CardTitle>
              <CardDescription>
                Recommended phases for your PoC implementation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-xs font-bold text-blue-600">1</div>
                  <span className="text-sm">Data Discovery & Assessment</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-xs font-bold text-blue-600">2</div>
                  <span className="text-sm">Data Pipeline Development</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-xs font-bold text-blue-600">3</div>
                  <span className="text-sm">Analytics & Visualization</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-xs font-bold text-blue-600">4</div>
                  <span className="text-sm">Testing & Validation</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}