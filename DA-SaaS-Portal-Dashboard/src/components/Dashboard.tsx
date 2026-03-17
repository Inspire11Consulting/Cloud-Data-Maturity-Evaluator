import React from 'react';
import { 
  BarChart3, 
  Lightbulb, 
  Database, 
  GitBranch, 
  PieChart, 
  ArrowRight,
  Map // Added for Metadata Mapper icon
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { PageType } from '../App';
import { ImageWithFallback } from './figma/ImageWithFallback';
import inspire11Icon from 'figma:asset/7e5b805c87957be58174764ffc55dd585d5a4ead.png';

interface DashboardProps {
  onNavigate: (page: PageType) => void;
}

const features = [
  {
    id: 'maturity-tool',
    title: 'Data & AI Maturity Tool',
    description: 'Assess your organization\'s data and AI readiness with our comprehensive maturity assessment tool. Input client profiles and get AI-generated recommendations.',
    icon: BarChart3,
    color: 'bg-blue-500',
    buttonColor: 'bg-blue-600 hover:bg-blue-700',
  },
  {
    id: 'poc-starter',
    title: 'Inspire11 PoC Starter Kit',
    description: 'Accelerate your proof of concept development with our intelligent starter kit. Provide your pain points and KPIs to generate tailored solutions.',
    icon: Lightbulb,
    color: 'bg-green-500',
    buttonColor: 'bg-green-600 hover:bg-green-700',
  },
  {
    id: 'data-model',
    title: 'Data Model Generator',
    description: 'Generate comprehensive data models and schema diagrams based on industry-specific KPIs and requirements.',
    icon: Database,
    color: 'bg-purple-500',
    buttonColor: 'bg-purple-600 hover:bg-purple-700',
  },
  {
    id: 'metadata-mapper',
    title: 'Metadata Driven Mapper',
    description: 'Map source columns to target schema with AI-powered suggestions and transformation rules.',
    icon: Map,
    color: 'bg-indigo-500',
    buttonColor: 'bg-indigo-600 hover:bg-indigo-700',
  },
  {
    id: 'pipeline',
    title: 'Pipeline Generator',
    description: 'Build robust Azure Fabric data pipelines with bronze-silver-gold architecture from your data models.',
    icon: GitBranch,
    color: 'bg-teal-500',
    buttonColor: 'bg-teal-600 hover:bg-teal-700',
  },
  {
    id: 'powerbi',
    title: 'Power BI Report Generator',
    description: 'Create professional Power BI dashboards and reports from your semantic models with AI assistance.',
    icon: PieChart,
    color: 'bg-yellow-500',
    buttonColor: 'bg-yellow-600 hover:bg-yellow-700',
  },
];

export function Dashboard({ onNavigate }: DashboardProps) {
  return (
    <div className="p-6 lg:p-8">
      {/* Header Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Data & AI SaaS Platform Portal
        </h1>
        <p className="text-lg text-gray-600">
          Accelerate your data and AI initiatives with our comprehensive suite of tools
        </p>
      </div>

      {/* Feature Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {features.map((feature) => {
          const Icon = feature.icon;
          
          return (
            <Card key={feature.id} className="hover:shadow-lg transition-shadow duration-200 flex flex-col">
              <CardHeader>
                <div className="flex items-center space-x-3 mb-2">
                  <div className={`w-10 h-10 ${feature.color} rounded-lg flex items-center justify-center`}>
                    {feature.image ? (
                      <ImageWithFallback 
                        src={feature.image} 
                        alt="Inspire11 Icon"
                        className="h-6 w-6 rounded object-cover"
                      />
                    ) : (
                      <Icon className="h-6 w-6 text-white" />
                    )}
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </div>
                <CardDescription className="text-gray-600 leading-relaxed">
                  {feature.description}
                </CardDescription>
              </CardHeader>
              
              <CardContent className="mt-auto">
                <Button 
                  className={`w-full ${feature.buttonColor} text-white`}
                  onClick={() => onNavigate(feature.id as PageType)}
                >
                  Launch
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Stats Section */}
      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-2xl font-bold text-blue-600">500+</CardTitle>
            <CardDescription>Organizations Served</CardDescription>
          </CardHeader>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-2xl font-bold text-green-600">1,200+</CardTitle>
            <CardDescription>Data Models Generated</CardDescription>
          </CardHeader>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-2xl font-bold text-purple-600">95%</CardTitle>
            <CardDescription>Customer Satisfaction</CardDescription>
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}