import React, { useState } from 'react';
import { ArrowLeft, BarChart3, Download, Eye } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Slider } from '../ui/slider';
import { Separator } from '../ui/separator';

interface MaturityToolProps {
  onNavigateBack: () => void;
}

const maturityCategories = [
  { id: 'data-governance', label: 'Data Governance', description: 'Policies, standards, and data quality' },
  { id: 'data-architecture', label: 'Data Architecture', description: 'Infrastructure and data integration' },
  { id: 'analytics-capabilities', label: 'Analytics Capabilities', description: 'Reporting, visualization, and insights' },
  { id: 'ai-ml-readiness', label: 'AI/ML Readiness', description: 'Machine learning and AI implementation' },
  { id: 'organizational-culture', label: 'Organizational Culture', description: 'Data-driven culture and skills' },
  { id: 'technology-stack', label: 'Technology Stack', description: 'Tools, platforms, and technical capabilities' },
];

export function MaturityTool({ onNavigateBack }: MaturityToolProps) {
  const [clientProfile, setClientProfile] = useState({
    companyName: '',
    industry: '',
    companySize: '',
    description: '',
  });
  
  const [maturityScores, setMaturityScores] = useState<Record<string, number>>({
    'data-governance': 3,
    'data-architecture': 3,
    'analytics-capabilities': 3,
    'ai-ml-readiness': 3,
    'organizational-culture': 3,
    'technology-stack': 3,
  });

  const handleScoreChange = (categoryId: string, value: number[]) => {
    setMaturityScores(prev => ({
      ...prev,
      [categoryId]: value[0]
    }));
  };

  const getScoreLabel = (score: number) => {
    const labels = ['Beginner', 'Basic', 'Developing', 'Intermediate', 'Advanced'];
    return labels[score - 1] || 'Unknown';
  };

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
          <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
            <BarChart3 className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Data & AI Maturity Tool</h1>
            <p className="text-gray-600">Assess your organization's data and AI readiness</p>
          </div>
        </div>
      </div>

      <Separator className="mb-8" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Client Profile Section */}
        <Card>
          <CardHeader>
            <CardTitle>Client Profile</CardTitle>
            <CardDescription>
              Provide basic information about your organization
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="companyName">Company Name</Label>
              <Input
                id="companyName"
                value={clientProfile.companyName}
                onChange={(e) => setClientProfile(prev => ({ ...prev, companyName: e.target.value }))}
                placeholder="Enter company name"
              />
            </div>
            
            <div>
              <Label htmlFor="industry">Industry</Label>
              <Input
                id="industry"
                value={clientProfile.industry}
                onChange={(e) => setClientProfile(prev => ({ ...prev, industry: e.target.value }))}
                placeholder="e.g., Healthcare, Finance, Manufacturing"
              />
            </div>
            
            <div>
              <Label htmlFor="companySize">Company Size</Label>
              <Input
                id="companySize"
                value={clientProfile.companySize}
                onChange={(e) => setClientProfile(prev => ({ ...prev, companySize: e.target.value }))}
                placeholder="e.g., 100-500 employees"
              />
            </div>
            
            <div>
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={clientProfile.description}
                onChange={(e) => setClientProfile(prev => ({ ...prev, description: e.target.value }))}
                placeholder="Brief description of your organization and data initiatives"
                rows={3}
              />
            </div>
          </CardContent>
        </Card>

        {/* Maturity Assessment */}
        <Card>
          <CardHeader>
            <CardTitle>Maturity Assessment</CardTitle>
            <CardDescription>
              Rate your organization's maturity in each category (1-5 scale)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {maturityCategories.map((category) => (
              <div key={category.id} className="space-y-3">
                <div>
                  <Label className="text-sm font-medium">{category.label}</Label>
                  <p className="text-xs text-gray-500">{category.description}</p>
                </div>
                
                <div className="space-y-2">
                  <Slider
                    value={[maturityScores[category.id]]}
                    onValueChange={(value) => handleScoreChange(category.id, value)}
                    max={5}
                    min={1}
                    step={1}
                    className="w-full [&_[data-slot=slider-range]]:bg-blue-600 [&_[data-slot=slider-thumb]]:border-blue-600"
                  />
                  
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Score: {maturityScores[category.id]}</span>
                    <span>{getScoreLabel(maturityScores[category.id])}</span>
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex flex-wrap gap-4">
        <Button className="bg-blue-600 hover:bg-blue-700">
          <BarChart3 className="h-4 w-4 mr-2" />
          Generate Assessment
        </Button>
        
        <Button variant="outline">
          <Eye className="h-4 w-4 mr-2" />
          View Roadmap
        </Button>
        
        <Button variant="outline">
          <Download className="h-4 w-4 mr-2" />
          Download PowerPoint
        </Button>
      </div>

      {/* Results Preview */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Assessment Results Preview</CardTitle>
          <CardDescription>
            Your organization's data and AI maturity scores will appear here after generation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {maturityCategories.map((category) => (
              <div key={category.id} className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {maturityScores[category.id]}/5
                </div>
                <div className="text-sm text-gray-600 mt-1">
                  {category.label}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}