import React, { useState } from 'react';
import { ArrowLeft, Map, Download, Upload, Trash2, Plus } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Separator } from '../ui/separator';
import { Badge } from '../ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';

interface MetadataMapperProps {
  onNavigateBack: () => void;
}

interface ColumnMapping {
  bronzeColumn: string;
  silverColumn: string;
  type: string;
  transformationRule: string;
}

const mockBronzeColumns = [
  'column_a', 'column_b', 'column_c', 'column_d', 
  'date_field_a', 'ndc', 'something_date'
];

const dataTypes = [
  'String', 'Integer', 'Float', 'Date', 'DateTime', 'Boolean', 'Decimal'
];

const transformationRules = [
  'Direct Mapping', 'Cast to Type', 'Format Date', 
  'Trim Whitespace', 'Uppercase', 'Lowercase', 'Custom Rule'
];

export function MetadataMapper({ onNavigateBack }: MetadataMapperProps) {
  const [datasourceName, setDatasourceName] = useState('Sample Dataset');
  const [datasourceCategory, setDatasourceCategory] = useState('Lookup');
  const [datasourceCategoryOther, setDatasourceCategoryOther] = useState('');
  const [isNewClient, setIsNewClient] = useState('True');
  const [clientName, setClientName] = useState('');
  const [sourceType, setSourceType] = useState('ADLS');
  const [loadType, setLoadType] = useState('Full');
  const [isActive, setIsActive] = useState('True');
  const [datasourceNotes, setDatasourceNotes] = useState('');
  const [sourceFile, setSourceFile] = useState('');
  const [targetTable, setTargetTable] = useState('sampletable');
  const [targetCatalog, setTargetCatalog] = useState('pops_catalyist');
  const [targetSchema, setTargetSchema] = useState('bronze');
  const [sourcePath, setSourcePath] = useState('/input/');
  const [sheetName, setSheetName] = useState('');
  const [clientDaysOfData, setClientDaysOfData] = useState('90');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  const [mappings, setMappings] = useState<ColumnMapping[]>([
    { bronzeColumn: 'column_a', silverColumn: 'column_a', type: '', transformationRule: '' },
    { bronzeColumn: 'column_b', silverColumn: 'column_b', type: '', transformationRule: '' },
  ]);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setSourceFile(file.name);
      // Simulate AI mapping suggestion generation
      setTimeout(() => {
        const suggestedMappings = mockBronzeColumns.map(col => ({
          bronzeColumn: col,
          silverColumn: col,
          type: col.includes('date') ? 'Date' : 'String',
          transformationRule: col.includes('date') ? 'Format Date' : 'Direct Mapping'
        }));
        setMappings(suggestedMappings);
      }, 500);
    }
  };

  const addMapping = () => {
    setMappings([...mappings, { 
      bronzeColumn: '', 
      silverColumn: '', 
      type: '', 
      transformationRule: '' 
    }]);
  };

  const removeMapping = (index: number) => {
    setMappings(mappings.filter((_, i) => i !== index));
  };

  const updateMapping = (index: number, field: keyof ColumnMapping, value: string) => {
    const newMappings = [...mappings];
    newMappings[index][field] = value;
    setMappings(newMappings);
  };

  const clearAllMappings = () => {
    setMappings([]);
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
          <div className="w-10 h-10 bg-indigo-500 rounded-lg flex items-center justify-center">
            <Map className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Metadata Driven Mapper</h1>
            <p className="text-gray-600">Map source columns to target schema with AI assistance</p>
          </div>
        </div>
      </div>

      <Separator className="mb-8" />

      <div className="space-y-6">
        {/* Datasource Configuration */}
        <Card>
          <CardHeader>
            <CardTitle>Datasource Configuration</CardTitle>
            <CardDescription>
              Configure your data source settings and metadata
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Row 1 */}
              <div>
                <Label htmlFor="datasourceName">Datasource Name</Label>
                <Input
                  id="datasourceName"
                  value={datasourceName}
                  onChange={(e) => setDatasourceName(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="datasourceCategory">Datasource Category</Label>
                <Select value={datasourceCategory} onValueChange={setDatasourceCategory}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Lookup">Lookup</SelectItem>
                    <SelectItem value="Transactional">Transactional</SelectItem>
                    <SelectItem value="Reference">Reference</SelectItem>
                    <SelectItem value="Master">Master</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="datasourceCategoryOther">Datasource Category (Other)</Label>
                <Input
                  id="datasourceCategoryOther"
                  value={datasourceCategoryOther}
                  onChange={(e) => setDatasourceCategoryOther(e.target.value)}
                  placeholder="Optional"
                />
              </div>

              {/* Row 2 */}
              <div>
                <Label htmlFor="isNewClient">Is New Client</Label>
                <Select value={isNewClient} onValueChange={setIsNewClient}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="True">True</SelectItem>
                    <SelectItem value="False">False</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="clientName">Client Name (if new client flag = True)</Label>
                <Input
                  id="clientName"
                  value={clientName}
                  onChange={(e) => setClientName(e.target.value)}
                  placeholder="Enter client name"
                />
              </div>
              <div>
                <Label htmlFor="datasourceNotes">Datasource Notes</Label>
                <Input
                  id="datasourceNotes"
                  value={datasourceNotes}
                  onChange={(e) => setDatasourceNotes(e.target.value)}
                  placeholder="Optional notes"
                />
              </div>

              {/* Row 3 */}
              <div>
                <Label htmlFor="sourceType">Source Type</Label>
                <Select value={sourceType} onValueChange={setSourceType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ADLS">ADLS</SelectItem>
                    <SelectItem value="SQL">SQL</SelectItem>
                    <SelectItem value="API">API</SelectItem>
                    <SelectItem value="File">File</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="loadType">Load Type</Label>
                <Select value={loadType} onValueChange={setLoadType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Full">Full</SelectItem>
                    <SelectItem value="Incremental">Incremental</SelectItem>
                    <SelectItem value="Delta">Delta</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="isActive">Is Active</Label>
                <Select value={isActive} onValueChange={setIsActive}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="True">True</SelectItem>
                    <SelectItem value="False">False</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Row 4 */}
              <div>
                <Label htmlFor="targetTable">Target Table</Label>
                <Input
                  id="targetTable"
                  value={targetTable}
                  onChange={(e) => setTargetTable(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="targetCatalog">Target Catalog</Label>
                <Input
                  id="targetCatalog"
                  value={targetCatalog}
                  onChange={(e) => setTargetCatalog(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="targetSchema">Target Schema</Label>
                <Input
                  id="targetSchema"
                  value={targetSchema}
                  onChange={(e) => setTargetSchema(e.target.value)}
                />
              </div>

              {/* Row 5 */}
              <div>
                <Label htmlFor="sourcePath">Source Path</Label>
                <Input
                  id="sourcePath"
                  value={sourcePath}
                  onChange={(e) => setSourcePath(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="sheetName">Sheet Name (if XLS)</Label>
                <Input
                  id="sheetName"
                  value={sheetName}
                  onChange={(e) => setSheetName(e.target.value)}
                  placeholder="Optional"
                />
              </div>
              <div>
                <Label htmlFor="clientDaysOfData">Client Days of Data (Dev Only)</Label>
                <Input
                  id="clientDaysOfData"
                  type="number"
                  value={clientDaysOfData}
                  onChange={(e) => setClientDaysOfData(e.target.value)}
                />
              </div>
            </div>

            {/* File Upload Section */}
            <div className="mt-6">
              <Label htmlFor="sourceFile">Source File</Label>
              <div className="flex items-center gap-3 mt-2">
                <Button
                  variant="outline"
                  onClick={() => document.getElementById('fileInput')?.click()}
                  className="bg-blue-600 text-white hover:bg-blue-700"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Select File
                </Button>
                <input
                  id="fileInput"
                  type="file"
                  className="hidden"
                  accept=".csv,.xlsx,.xls,.json"
                  onChange={handleFileSelect}
                />
                {selectedFile && (
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="text-sm">
                      File Selected: {selectedFile.name}
                    </Badge>
                  </div>
                )}
              </div>
              <p className="text-sm text-gray-500 mt-1">
                Upload source metadata file for AI-powered mapping suggestions
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Column Mapping Section */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Column Mapping</CardTitle>
                <CardDescription>
                  Map bronze columns to silver columns with transformation rules
                </CardDescription>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={clearAllMappings}
                  disabled={mappings.length === 0}
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Clear All
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={addMapping}
                  className="bg-indigo-600 text-white hover:bg-indigo-700"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Row
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="border rounded-lg overflow-hidden">
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow className="bg-blue-700 hover:bg-blue-700">
                      <TableHead className="text-white font-semibold">Bronze Column</TableHead>
                      <TableHead className="text-white font-semibold">Silver Column Name</TableHead>
                      <TableHead className="text-white font-semibold">Type</TableHead>
                      <TableHead className="text-white font-semibold">Transformation Rule</TableHead>
                      <TableHead className="text-white font-semibold w-20">Action</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {mappings.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={5} className="text-center text-gray-500 py-8">
                          No mappings defined. Upload a file or add rows manually.
                        </TableCell>
                      </TableRow>
                    ) : (
                      mappings.map((mapping, index) => (
                        <TableRow key={index}>
                          <TableCell>
                            <Select
                              value={mapping.bronzeColumn}
                              onValueChange={(value) => updateMapping(index, 'bronzeColumn', value)}
                            >
                              <SelectTrigger className="w-full">
                                <SelectValue placeholder="Select column" />
                              </SelectTrigger>
                              <SelectContent>
                                {mockBronzeColumns.map(col => (
                                  <SelectItem key={col} value={col}>
                                    {col}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          </TableCell>
                          <TableCell>
                            <Input
                              value={mapping.silverColumn}
                              onChange={(e) => updateMapping(index, 'silverColumn', e.target.value)}
                              placeholder="Silver column name"
                            />
                          </TableCell>
                          <TableCell>
                            <Select
                              value={mapping.type}
                              onValueChange={(value) => updateMapping(index, 'type', value)}
                            >
                              <SelectTrigger className="w-full">
                                <SelectValue placeholder="Select type" />
                              </SelectTrigger>
                              <SelectContent>
                                {dataTypes.map(type => (
                                  <SelectItem key={type} value={type}>
                                    {type}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          </TableCell>
                          <TableCell>
                            <Select
                              value={mapping.transformationRule}
                              onValueChange={(value) => updateMapping(index, 'transformationRule', value)}
                            >
                              <SelectTrigger className="w-full">
                                <SelectValue placeholder="Select rule" />
                              </SelectTrigger>
                              <SelectContent>
                                {transformationRules.map(rule => (
                                  <SelectItem key={rule} value={rule}>
                                    {rule}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          </TableCell>
                          <TableCell>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => removeMapping(index)}
                            >
                              <Trash2 className="h-4 w-4 text-red-500" />
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </div>
            </div>
            
            {selectedFile && mappings.length > 0 && (
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm text-green-800">
                  ✓ AI-powered mapping suggestions generated from uploaded file. Review and adjust as needed.
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4">
          <Button className="bg-indigo-600 hover:bg-indigo-700">
            <Map className="h-4 w-4 mr-2" />
            Generate Mapping
          </Button>
          
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Download JSON
          </Button>
          
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export Configuration
          </Button>
        </div>
      </div>
    </div>
  );
}