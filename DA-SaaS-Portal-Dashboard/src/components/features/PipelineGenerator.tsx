import React, { useState } from 'react';
import { ArrowLeft, GitBranch, Play, Download } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Label } from '../ui/label';
import { Separator } from '../ui/separator';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';

interface PipelineGeneratorProps {
  onNavigateBack: () => void;
}

const dataModels = [
  'Retail Analytics Model',
  'Healthcare Patient Model',
  'Financial Services Model',
  'Manufacturing Operations Model',
  'Customer 360 Model'
];

const pipelineStages = [
  {
    layer: 'Bronze',
    description: 'Raw data ingestion',
    color: 'bg-amber-100 text-amber-800',
    status: 'completed',
    activities: ['Data extraction', 'Raw data storage', 'Schema validation']
  },
  {
    layer: 'Silver',
    description: 'Data cleaning & transformation',
    color: 'bg-gray-100 text-gray-800',
    status: 'in-progress',
    activities: ['Data cleansing', 'Standardization', 'Basic transformations']
  },
  {
    layer: 'Gold',
    description: 'Business-ready analytics',
    color: 'bg-yellow-100 text-yellow-800',
    status: 'pending',
    activities: ['Business logic', 'Aggregations', 'KPI calculations']
  }
];

const mockDataSources = [
  { name: 'Customer Database', type: 'SQL Server', status: 'Connected' },
  { name: 'Transaction Logs', type: 'Azure Blob', status: 'Connected' },
  { name: 'Product Catalog', type: 'REST API', status: 'Configured' },
  { name: 'Marketing Data', type: 'CSV Files', status: 'Pending' }
];

export function PipelineGenerator({ onNavigateBack }: PipelineGeneratorProps) {
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [deploymentProgress, setDeploymentProgress] = useState(0);

  const handleDeployPipeline = () => {
    // Simulate deployment progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setDeploymentProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 500);
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
          <div className="w-10 h-10 bg-teal-500 rounded-lg flex items-center justify-center">
            <GitBranch className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Pipeline Generator</h1>
            <p className="text-gray-600">Build robust Azure Fabric data pipelines</p>
          </div>
        </div>
      </div>

      <Separator className="mb-8" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Configuration Section */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Pipeline Configuration</CardTitle>
              <CardDescription>
                Select a data model and configure your pipeline settings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="dataModel">Data Model</Label>
                <Select value={selectedModel} onValueChange={setSelectedModel}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a data model" />
                  </SelectTrigger>
                  <SelectContent>
                    {dataModels.map(model => (
                      <SelectItem key={model} value={model}>
                        {model}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Data Sources</CardTitle>
              <CardDescription>
                Connected data sources for your pipeline
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {mockDataSources.map((source, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <div className="font-medium text-sm">{source.name}</div>
                      <div className="text-xs text-gray-500">{source.type}</div>
                    </div>
                    <Badge 
                      variant={source.status === 'Connected' ? 'default' : 
                               source.status === 'Configured' ? 'secondary' : 'outline'}
                    >
                      {source.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4">
            <Button 
              className="bg-teal-600 hover:bg-teal-700"
              disabled={!selectedModel}
              onClick={handleDeployPipeline}
            >
              <Play className="h-4 w-4 mr-2" />
              Deploy Pipeline
            </Button>
            
            <Button variant="outline">
              <GitBranch className="h-4 w-4 mr-2" />
              View Pipeline Code
            </Button>
            
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Export Configuration
            </Button>
          </div>

          {/* Deployment Progress */}
          {deploymentProgress > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Deployment Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Progress value={deploymentProgress} className="w-full" />
                  <p className="text-sm text-gray-600">{deploymentProgress}% Complete</p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Pipeline Architecture */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Bronze-Silver-Gold Architecture</CardTitle>
              <CardDescription>
                Multi-layered data processing pipeline structure
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {pipelineStages.map((stage, index) => (
                  <div key={stage.layer} className="relative">
                    <div className="flex items-start space-x-4">
                      <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${stage.color} font-bold`}>
                        {stage.layer}
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium">{stage.layer} Layer</h4>
                          <Badge variant={
                            stage.status === 'completed' ? 'default' :
                            stage.status === 'in-progress' ? 'secondary' : 'outline'
                          }>
                            {stage.status}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-3">{stage.description}</p>
                        
                        <div className="space-y-1">
                          {stage.activities.map((activity, actIndex) => (
                            <div key={actIndex} className="text-xs text-gray-500">
                              • {activity}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                    
                    {index < pipelineStages.length - 1 && (
                      <div className="absolute left-6 top-12 w-0.5 h-8 bg-gray-300" />
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Pipeline Components</CardTitle>
              <CardDescription>
                Azure Fabric components included in your pipeline
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 gap-3">
                <div className="p-3 border rounded-lg">
                  <div className="font-medium text-sm">Data Factory</div>
                  <div className="text-xs text-gray-500">Orchestration and data movement</div>
                </div>
                <div className="p-3 border rounded-lg">
                  <div className="font-medium text-sm">Synapse Analytics</div>
                  <div className="text-xs text-gray-500">Data transformation and analytics</div>
                </div>
                <div className="p-3 border rounded-lg">
                  <div className="font-medium text-sm">Data Lake Storage</div>
                  <div className="text-xs text-gray-500">Scalable data storage</div>
                </div>
                <div className="p-3 border rounded-lg">
                  <div className="font-medium text-sm">Power BI</div>
                  <div className="text-xs text-gray-500">Business intelligence and reporting</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Monitoring & Alerts</CardTitle>
              <CardDescription>
                Pipeline monitoring and notification settings
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Data Quality Monitoring</span>
                  <Badge variant="default">Enabled</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Failure Notifications</span>
                  <Badge variant="default">Enabled</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Performance Alerts</span>
                  <Badge variant="secondary">Configured</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}