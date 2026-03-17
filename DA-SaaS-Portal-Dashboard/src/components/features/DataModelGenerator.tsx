import React, { useState } from 'react';
import { ArrowLeft, Database, Download, Eye } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Label } from '../ui/label';
import { Checkbox } from '../ui/checkbox';
import { Separator } from '../ui/separator';
import { Badge } from '../ui/badge';

interface DataModelGeneratorProps {
  onNavigateBack: () => void;
}

const industries = [
  'Healthcare', 'Financial Services', 'Retail & E-commerce', 'Manufacturing',
  'Technology', 'Energy & Utilities', 'Transportation', 'Education'
];

const industryKPIs = {
  'Healthcare': [
    'Patient Satisfaction Score', 'Average Treatment Time', 'Readmission Rate',
    'Staff Utilization Rate', 'Medical Error Rate', 'Cost per Patient'
  ],
  'Financial Services': [
    'Customer Acquisition Cost', 'Net Interest Margin', 'Loan Default Rate',
    'Processing Time', 'Compliance Score', 'Customer Lifetime Value'
  ],
  'Retail & E-commerce': [
    'Conversion Rate', 'Average Order Value', 'Customer Churn Rate',
    'Inventory Turnover', 'Cart Abandonment Rate', 'Return Rate'
  ],
  'Manufacturing': [
    'Overall Equipment Effectiveness', 'Defect Rate', 'Production Throughput',
    'Downtime Percentage', 'Cost per Unit', 'On-time Delivery Rate'
  ]
};

const mockSchemaElements = [
  { table: 'customers', type: 'Dimension', fields: ['customer_id', 'name', 'email', 'registration_date'] },
  { table: 'products', type: 'Dimension', fields: ['product_id', 'name', 'category', 'price'] },
  { table: 'orders', type: 'Fact', fields: ['order_id', 'customer_id', 'product_id', 'quantity', 'total_amount', 'order_date'] },
  { table: 'sales_metrics', type: 'Aggregate', fields: ['metric_id', 'date', 'revenue', 'units_sold', 'avg_order_value'] }
];

export function DataModelGenerator({ onNavigateBack }: DataModelGeneratorProps) {
  const [selectedIndustry, setSelectedIndustry] = useState<string>('');
  const [selectedKPIs, setSelectedKPIs] = useState<string[]>([]);

  const handleKPIToggle = (kpi: string) => {
    setSelectedKPIs(prev => 
      prev.includes(kpi) 
        ? prev.filter(k => k !== kpi)
        : [...prev, kpi]
    );
  };

  const availableKPIs = selectedIndustry ? industryKPIs[selectedIndustry as keyof typeof industryKPIs] || [] : [];

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
          <div className="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center">
            <Database className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Data Model Generator</h1>
            <p className="text-gray-600">Generate comprehensive data models and schemas</p>
          </div>
        </div>
      </div>

      <Separator className="mb-8" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Configuration Section */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Industry & KPI Selection</CardTitle>
              <CardDescription>
                Select your industry and relevant KPIs to generate a tailored data model
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="industry">Industry</Label>
                <Select value={selectedIndustry} onValueChange={setSelectedIndustry}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select your industry" />
                  </SelectTrigger>
                  <SelectContent>
                    {industries.map(industry => (
                      <SelectItem key={industry} value={industry}>
                        {industry}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {selectedIndustry && (
                <div>
                  <Label>Key Performance Indicators</Label>
                  <div className="mt-3 space-y-3 max-h-64 overflow-y-auto">
                    {availableKPIs.map(kpi => (
                      <div key={kpi} className="flex items-center space-x-2">
                        <Checkbox
                          id={kpi}
                          checked={selectedKPIs.includes(kpi)}
                          onCheckedChange={() => handleKPIToggle(kpi)}
                        />
                        <Label htmlFor={kpi} className="text-sm cursor-pointer">
                          {kpi}
                        </Label>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4">
            <Button 
              className="bg-purple-600 hover:bg-purple-700"
              disabled={!selectedIndustry || selectedKPIs.length === 0}
            >
              <Database className="h-4 w-4 mr-2" />
              Generate Data Model
            </Button>
            
            <Button variant="outline">
              <Eye className="h-4 w-4 mr-2" />
              View Schema Diagram
            </Button>
            
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Download Model
            </Button>
          </div>

          {/* Selected KPIs Summary */}
          {selectedKPIs.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Selected KPIs ({selectedKPIs.length})</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {selectedKPIs.map(kpi => (
                    <Badge key={kpi} variant="secondary">
                      {kpi}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Generated Schema Preview */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Generated Schema Preview</CardTitle>
              <CardDescription>
                Data model structure based on your selected KPIs
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockSchemaElements.map((element, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-medium text-gray-900">{element.table}</h4>
                      <Badge 
                        variant={element.type === 'Fact' ? 'default' : element.type === 'Dimension' ? 'secondary' : 'outline'}
                      >
                        {element.type}
                      </Badge>
                    </div>
                    <div className="space-y-1">
                      {element.fields.map(field => (
                        <div key={field} className="text-sm text-gray-600 font-mono">
                          • {field}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Relationships</CardTitle>
              <CardDescription>
                Key relationships in your data model
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="text-sm">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded">customers.customer_id</span>
                  <span className="mx-2">→</span>
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded">orders.customer_id</span>
                </div>
                <div className="text-sm">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded">products.product_id</span>
                  <span className="mx-2">→</span>
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded">orders.product_id</span>
                </div>
                <div className="text-sm">
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded">orders.order_date</span>
                  <span className="mx-2">→</span>
                  <span className="font-mono bg-gray-100 px-2 py-1 rounded">sales_metrics.date</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Export Options</CardTitle>
              <CardDescription>
                Available formats for your data model
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-3">
                <Button variant="outline" size="sm">SQL Schema</Button>
                <Button variant="outline" size="sm">JSON Model</Button>
                <Button variant="outline" size="sm">ERD Diagram</Button>
                <Button variant="outline" size="sm">Documentation</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}