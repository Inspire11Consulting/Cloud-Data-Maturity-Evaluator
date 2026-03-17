import React, { useState } from 'react';
import { ArrowLeft, PieChart, Eye, Download, BarChart } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Label } from '../ui/label';
import { Checkbox } from '../ui/checkbox';
import { Separator } from '../ui/separator';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';

interface PowerBIGeneratorProps {
  onNavigateBack: () => void;
}

const semanticModels = [
  'Sales Performance Model',
  'Customer Analytics Model',
  'Financial Reporting Model',
  'Operational Metrics Model',
  'Marketing Campaign Model'
];

const visualizationTypes = [
  { id: 'bar-chart', label: 'Bar Chart', icon: BarChart },
  { id: 'line-chart', label: 'Line Chart', icon: BarChart },
  { id: 'pie-chart', label: 'Pie Chart', icon: PieChart },
  { id: 'table', label: 'Table', icon: BarChart },
  { id: 'card', label: 'Card/KPI', icon: BarChart },
  { id: 'gauge', label: 'Gauge', icon: PieChart }
];

const mockReportPages = [
  {
    name: 'Executive Summary',
    description: 'High-level KPIs and trends',
    visuals: ['Revenue Card', 'Sales Trend Line', 'Top Products Table']
  },
  {
    name: 'Sales Analysis',
    description: 'Detailed sales performance',
    visuals: ['Sales by Region Bar', 'Monthly Comparison', 'Sales Rep Performance']
  },
  {
    name: 'Customer Insights',
    description: 'Customer behavior and segmentation',
    visuals: ['Customer Segments Pie', 'Retention Rate Gauge', 'Customer Journey']
  }
];

const mockDashboardElements = [
  { title: 'Total Revenue', value: '$2.4M', change: '+12%', type: 'currency' },
  { title: 'Orders', value: '1,847', change: '+8%', type: 'number' },
  { title: 'Conversion Rate', value: '3.2%', change: '+0.5%', type: 'percentage' },
  { title: 'Avg Order Value', value: '$156', change: '-2%', type: 'currency' }
];

export function PowerBIGenerator({ onNavigateBack }: PowerBIGeneratorProps) {
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [selectedVisuals, setSelectedVisuals] = useState<string[]>([]);

  const handleVisualToggle = (visualId: string) => {
    setSelectedVisuals(prev => 
      prev.includes(visualId) 
        ? prev.filter(v => v !== visualId)
        : [...prev, visualId]
    );
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
          <div className="w-10 h-10 bg-yellow-500 rounded-lg flex items-center justify-center">
            <PieChart className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Power BI Report Generator</h1>
            <p className="text-gray-600">Create professional dashboards from semantic models</p>
          </div>
        </div>
      </div>

      <Separator className="mb-8" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Configuration Section */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Report Configuration</CardTitle>
              <CardDescription>
                Select your semantic model and visualization preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="semanticModel">Semantic Model</Label>
                <Select value={selectedModel} onValueChange={setSelectedModel}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a semantic model" />
                  </SelectTrigger>
                  <SelectContent>
                    {semanticModels.map(model => (
                      <SelectItem key={model} value={model}>
                        {model}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {selectedModel && (
                <div>
                  <Label>Visualization Types</Label>
                  <div className="mt-3 grid grid-cols-2 gap-3">
                    {visualizationTypes.map(visual => {
                      const Icon = visual.icon;
                      return (
                        <div key={visual.id} className="flex items-center space-x-2">
                          <Checkbox
                            id={visual.id}
                            checked={selectedVisuals.includes(visual.id)}
                            onCheckedChange={() => handleVisualToggle(visual.id)}
                          />
                          <Label htmlFor={visual.id} className="text-sm cursor-pointer flex items-center space-x-2">
                            <Icon className="h-4 w-4" />
                            <span>{visual.label}</span>
                          </Label>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4">
            <Button 
              className="bg-yellow-600 hover:bg-yellow-700"
              disabled={!selectedModel || selectedVisuals.length === 0}
            >
              <PieChart className="h-4 w-4 mr-2" />
              Generate Report
            </Button>
            
            <Button variant="outline">
              <Eye className="h-4 w-4 mr-2" />
              Preview Dashboard
            </Button>
            
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Download PBIX
            </Button>
          </div>

          {/* Report Pages Preview */}
          <Card>
            <CardHeader>
              <CardTitle>Generated Report Pages</CardTitle>
              <CardDescription>
                Recommended pages based on your semantic model
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {mockReportPages.map((page, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-900">{page.name}</h4>
                      <Badge variant="secondary">{page.visuals.length} visuals</Badge>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{page.description}</p>
                    <div className="space-y-1">
                      {page.visuals.map((visual, vIndex) => (
                        <div key={vIndex} className="text-xs text-gray-500">
                          • {visual}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Dashboard Preview */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Dashboard Preview</CardTitle>
              <CardDescription>
                Preview of your generated Power BI dashboard
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="overview" className="w-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="overview">Overview</TabsTrigger>
                  <TabsTrigger value="sales">Sales</TabsTrigger>
                  <TabsTrigger value="customers">Customers</TabsTrigger>
                </TabsList>
                
                <TabsContent value="overview" className="mt-4">
                  <div className="space-y-4">
                    {/* KPI Cards */}
                    <div className="grid grid-cols-2 gap-4">
                      {mockDashboardElements.map((element, index) => (
                        <div key={index} className="p-4 border rounded-lg bg-gradient-to-r from-blue-50 to-blue-100">
                          <div className="text-xs text-gray-600 mb-1">{element.title}</div>
                          <div className="text-lg font-bold text-blue-900">{element.value}</div>
                          <div className={`text-xs ${element.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                            {element.change} vs last period
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    {/* Chart Placeholder */}
                    <div className="h-32 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
                      <div className="text-center text-gray-500">
                        <BarChart className="h-8 w-8 mx-auto mb-2" />
                        <div className="text-sm">Sales Trend Chart</div>
                      </div>
                    </div>
                  </div>
                </TabsContent>
                
                <TabsContent value="sales" className="mt-4">
                  <div className="space-y-4">
                    <div className="h-40 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
                      <div className="text-center text-gray-500">
                        <BarChart className="h-8 w-8 mx-auto mb-2" />
                        <div className="text-sm">Sales Analysis Visuals</div>
                      </div>
                    </div>
                  </div>
                </TabsContent>
                
                <TabsContent value="customers" className="mt-4">
                  <div className="space-y-4">
                    <div className="h-40 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
                      <div className="text-center text-gray-500">
                        <PieChart className="h-8 w-8 mx-auto mb-2" />
                        <div className="text-sm">Customer Insights Visuals</div>
                      </div>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Data Connections</CardTitle>
              <CardDescription>
                Connected data sources for your report
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium text-sm">Sales Database</div>
                    <div className="text-xs text-gray-500">SQL Server</div>
                  </div>
                  <Badge variant="default">Connected</Badge>
                </div>
                <div className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium text-sm">Customer Data</div>
                    <div className="text-xs text-gray-500">Azure Data Lake</div>
                  </div>
                  <Badge variant="default">Connected</Badge>
                </div>
                <div className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium text-sm">Product Catalog</div>
                    <div className="text-xs text-gray-500">REST API</div>
                  </div>
                  <Badge variant="secondary">Configured</Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Export Options</CardTitle>
              <CardDescription>
                Available formats for your Power BI report
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-3">
                <Button variant="outline" size="sm">PBIX File</Button>
                <Button variant="outline" size="sm">PDF Report</Button>
                <Button variant="outline" size="sm">Excel Export</Button>
                <Button variant="outline" size="sm">PowerPoint</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}