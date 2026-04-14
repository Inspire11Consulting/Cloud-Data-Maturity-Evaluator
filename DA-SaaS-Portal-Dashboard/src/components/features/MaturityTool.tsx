import React, { useEffect, useMemo, useState } from 'react';
import { BarChart3, Download, Eye, RefreshCw } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Slider } from '../ui/slider';
import { Separator } from '../ui/separator';

type SchemaResponse = {
  categories_structure: Record<string, string[]>;
  maturity_levels: Record<string, string>;
  scale: { min: number; max: number };
};

type AssessResponse = {
  recommendation_data: Array<{
    category: string;
    raw?: string;
    avg?: number | null;
    show_avg?: boolean;
    error?: string;
    data_normalized?: {
      executive?: Record<string, unknown>;
      technical?: Record<string, unknown>;
    };
  }>;
  category_fragments: Array<{
    category: string;
    focus_8w: string[];
    plan_3y: string[];
  }>;
};

type ConsolidateResponse = {
  consolidated: {
    focus_8w: Record<string, string[]>;
    plan_3y: Record<string, string[]>;
  };
};

export function MaturityTool() {
  const sprintOrder = ['sprint1', 'sprint2', 'sprint3', 'sprint4'];
  const yearOrder = ['year1', 'year2', 'year3'];

  const [clientProfile, setClientProfile] = useState({
    companyName: '',
    industry: '',
    companySize: '',
    description: '',
    itSize: '',
    usesCloud: 'Yes',
    cloudPlatform: 'Azure',
    priorityProjects: '',
  });
  
  const [schema, setSchema] = useState<SchemaResponse | null>(null);
  const [schemaError, setSchemaError] = useState<string | null>(null);

  const [allScores, setAllScores] = useState<Record<string, { sub_capabilities: Record<string, number> }>>({});
  const [categoryInclusion, setCategoryInclusion] = useState<Record<string, boolean>>({});
  const [categoryComments, setCategoryComments] = useState<Record<string, string>>({});

  const [isAssessing, setIsAssessing] = useState(false);
  const [assessError, setAssessError] = useState<string | null>(null);
  const [assessResult, setAssessResult] = useState<AssessResponse | null>(null);

  const [isConsolidating, setIsConsolidating] = useState(false);
  const [consolidateError, setConsolidateError] = useState<string | null>(null);
  const [consolidated, setConsolidated] = useState<ConsolidateResponse['consolidated'] | null>(null);

  const averageScore = useMemo(() => {
    const categories = Object.keys(allScores);
    if (!categories.length) return 0;

    const avgs = categories.map((cat) => {
      const sub = allScores[cat]?.sub_capabilities || {};
      const values = Object.values(sub);
      if (!values.length) return 0;
      const avg = values.reduce((a, b) => a + b, 0) / values.length;
      return avg;
    });
    const overall = avgs.reduce((a, b) => a + b, 0) / avgs.length;
    return Math.round(overall * 10) / 10;
  }, [allScores]);

  const getScoreLabel = (score: number) => {
    const labels = ['Beginner', 'Basic', 'Developing', 'Intermediate', 'Advanced'];
    return labels[score - 1] || 'Unknown';
  };

  const formatPeriodLabel = (period: string) => {
    if (period.toLowerCase().startsWith('sprint')) {
      return period.replace('sprint', 'Sprint ');
    }
    if (period.toLowerCase().startsWith('year')) {
      return period.replace('year', 'Year ');
    }
    return period;
  };

  useEffect(() => {
    let cancelled = false;

    async function loadSchema() {
      setSchemaError(null);
      try {
        const res = await fetch('/api/schema');
        if (!res.ok) throw new Error(`Schema fetch failed: ${res.status}`);
        const json = (await res.json()) as SchemaResponse;
        if (cancelled) return;
        setSchema(json);

        // Initialize scores and inclusion defaults
        const initialScores: Record<string, { sub_capabilities: Record<string, number> }> = {};
        const initialInclusion: Record<string, boolean> = {};
        for (const [category, subs] of Object.entries(json.categories_structure || {})) {
          initialInclusion[category] = true;
          const subScores: Record<string, number> = {};
          for (const sub of subs) subScores[sub] = 3;
          initialScores[category] = { sub_capabilities: subScores };
        }
        setAllScores(initialScores);
        setCategoryInclusion(initialInclusion);
      } catch (e) {
        if (cancelled) return;
        setSchemaError(e instanceof Error ? e.message : String(e));
      }
    }

    loadSchema();
    return () => {
      cancelled = true;
    };
  }, []);

  const handleSubScoreChange = (category: string, subCap: string, value: number[]) => {
    setAllScores((prev) => ({
      ...prev,
      [category]: {
        sub_capabilities: {
          ...(prev[category]?.sub_capabilities || {}),
          [subCap]: value[0],
        },
      },
    }));
  };

  const generateAssessment = async () => {
    setIsAssessing(true);
    setAssessError(null);
    setAssessResult(null);
    setConsolidated(null);
    setConsolidateError(null);

    try {
      const allScoresWithAverages: Record<string, { average: number; sub_capabilities: Record<string, number> }> = {};
      for (const [category, data] of Object.entries(allScores)) {
        const sub = data.sub_capabilities || {};
        const values = Object.values(sub);
        const avg = values.length ? Math.round((values.reduce((a, b) => a + b, 0) / values.length) * 10) / 10 : 0;
        allScoresWithAverages[category] = { average: avg, sub_capabilities: sub };
      }

      const res = await fetch('/api/assess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          industry: clientProfile.industry,
          company_size: clientProfile.companySize,
          it_size: clientProfile.itSize,
          uses_cloud: clientProfile.usesCloud,
          cloud_platform: clientProfile.cloudPlatform,
          priority_projects: clientProfile.priorityProjects,
          overall_context: clientProfile.description,
          seed_scenario_text: '',
          all_scores: allScoresWithAverages,
          category_inclusion: categoryInclusion,
          category_comments: categoryComments,
        }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Assess failed (${res.status}): ${text}`);
      }
      const json = (await res.json()) as AssessResponse;
      setAssessResult(json);
    } catch (e) {
      setAssessError(e instanceof Error ? e.message : String(e));
    } finally {
      setIsAssessing(false);
    }
  };

  const consolidateRoadmap = async () => {
    if (!assessResult?.category_fragments?.length) return;
    setIsConsolidating(true);
    setConsolidateError(null);
    try {
      const res = await fetch('/api/consolidate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category_fragments: assessResult.category_fragments }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Consolidate failed (${res.status}): ${text}`);
      }
      const json = (await res.json()) as ConsolidateResponse;
      setConsolidated(json.consolidated);
    } catch (e) {
      setConsolidateError(e instanceof Error ? e.message : String(e));
    } finally {
      setIsConsolidating(false);
    }
  };

  const downloadPptx = async () => {
    if (!consolidated || !assessResult?.recommendation_data) return;
    try {
      const res = await fetch('/api/export/pptx', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          consolidated,
          recommendation_data: assessResult.recommendation_data,
        }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Export failed (${res.status}): ${text}`);
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Consolidated_Roadmap_and_Cards.pptx';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      setAssessError(e instanceof Error ? e.message : String(e));
    }
  };

  return (
    <div className="p-6 lg:p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6 gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
            <BarChart3 className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Data & AI Maturity Tool</h1>
            <p className="text-gray-600">Assess your organization's data and AI readiness</p>
          </div>
        </div>

        <div className="text-right">
          <div className="text-sm text-gray-600">Overall average</div>
          <div className="text-2xl font-bold text-blue-600">{averageScore}/5</div>
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
              <Label htmlFor="itSize">IT Department Size</Label>
              <Input
                id="itSize"
                value={clientProfile.itSize}
                onChange={(e) => setClientProfile(prev => ({ ...prev, itSize: e.target.value }))}
                placeholder="e.g., 50"
              />
            </div>

            <div>
              <Label htmlFor="cloudPlatform">Cloud Platform(s)</Label>
              <Input
                id="cloudPlatform"
                value={clientProfile.cloudPlatform}
                onChange={(e) => setClientProfile(prev => ({ ...prev, cloudPlatform: e.target.value }))}
                placeholder="e.g., Azure, AWS, GCP"
              />
            </div>

            <div>
              <Label htmlFor="priorityProjects">Priority Projects</Label>
              <Textarea
                id="priorityProjects"
                value={clientProfile.priorityProjects}
                onChange={(e) => setClientProfile(prev => ({ ...prev, priorityProjects: e.target.value }))}
                placeholder="e.g., ERP consolidation, eCommerce upgrade"
                rows={2}
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
              Rate your organization's maturity in each sub-capability (1-5 scale)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {schemaError && (
              <div className="text-sm text-red-600">Failed to load schema: {schemaError}</div>
            )}

            {!schema && !schemaError && (
              <div className="text-sm text-gray-600">Loading assessment schema…</div>
            )}

            {schema &&
              Object.entries(schema.categories_structure).map(([category, subCaps]) => (
                <div key={category} className="space-y-4 rounded-lg border border-gray-200 bg-white p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <Label className="text-sm font-semibold">{category}</Label>
                      <p className="text-xs text-gray-500">{subCaps.length} sub-capabilities</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <label className="text-xs text-gray-600">
                        <input
                          type="checkbox"
                          className="mr-2"
                          checked={categoryInclusion[category] ?? true}
                          onChange={(e) =>
                            setCategoryInclusion((prev) => ({ ...prev, [category]: e.target.checked }))
                          }
                        />
                        Include
                      </label>
                    </div>
                  </div>

                  <div className="space-y-5">
                    {subCaps.map((sub) => {
                      const value = allScores[category]?.sub_capabilities?.[sub] ?? 3;
                      return (
                        <div key={sub} className="space-y-2">
                          <div className="flex items-baseline justify-between gap-4">
                            <div className="text-sm text-gray-800">{sub}</div>
                            <div className="text-xs text-gray-500">
                              {value}/5 • {getScoreLabel(value)}
                            </div>
                          </div>
                          <Slider
                            value={[value]}
                            onValueChange={(v) => handleSubScoreChange(category, sub, v)}
                            max={5}
                            min={1}
                            step={1}
                            className="w-full [&_[data-slot=slider-range]]:bg-blue-600 [&_[data-slot=slider-thumb]]:border-blue-600"
                          />
                        </div>
                      );
                    })}
                  </div>

                  <div className="pt-2">
                    <Label className="text-xs text-gray-600">Comments (optional)</Label>
                    <Textarea
                      value={categoryComments[category] ?? ''}
                      onChange={(e) =>
                        setCategoryComments((prev) => ({ ...prev, [category]: e.target.value }))
                      }
                      placeholder="Context, constraints, or notes for this category"
                      rows={2}
                    />
                  </div>
                </div>
              ))}
          </CardContent>
        </Card>
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex flex-wrap gap-4">
        <Button className="bg-blue-600 hover:bg-blue-700" onClick={generateAssessment} disabled={isAssessing || !!schemaError || !schema}>
          <BarChart3 className="h-4 w-4 mr-2" />
          {isAssessing ? 'Generating…' : 'Generate Assessment'}
        </Button>
        
        <Button variant="outline" onClick={consolidateRoadmap} disabled={isConsolidating || !assessResult?.category_fragments?.length}>
          <Eye className="h-4 w-4 mr-2" />
          {isConsolidating ? 'Consolidating…' : 'View Roadmap'}
        </Button>
        
        <Button variant="outline" onClick={downloadPptx} disabled={!consolidated || !assessResult?.recommendation_data?.length}>
          <Download className="h-4 w-4 mr-2" />
          Download PowerPoint
        </Button>

        <Button
          variant="ghost"
          onClick={() => {
            setClientProfile({
              companyName: '',
              industry: '',
              companySize: '',
              description: '',
              itSize: '',
              usesCloud: 'Yes',
              cloudPlatform: 'Azure',
              priorityProjects: '',
            });
            if (schema) {
              const initialScores: Record<string, { sub_capabilities: Record<string, number> }> = {};
              const initialInclusion: Record<string, boolean> = {};
              for (const [category, subs] of Object.entries(schema.categories_structure || {})) {
                initialInclusion[category] = true;
                const subScores: Record<string, number> = {};
                for (const sub of subs) subScores[sub] = 3;
                initialScores[category] = { sub_capabilities: subScores };
              }
              setAllScores(initialScores);
              setCategoryInclusion(initialInclusion);
              setCategoryComments({});
            }
            setAssessResult(null);
            setConsolidated(null);
            setAssessError(null);
            setConsolidateError(null);
          }}
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Reset
        </Button>
      </div>

      {(assessError || consolidateError) && (
        <div className="mt-4 text-sm text-red-600">
          {assessError ? <div>{assessError}</div> : null}
          {consolidateError ? <div>{consolidateError}</div> : null}
        </div>
      )}

      {/* Results Preview */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Results</CardTitle>
          <CardDescription>
            AI-generated baseball cards and roadmap output
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!assessResult && <div className="text-sm text-gray-600">Run “Generate Assessment” to see results.</div>}

          {assessResult?.recommendation_data?.length ? (
            <div className="space-y-6">
              {assessResult.recommendation_data.map((item) => {
                const exec = (item.data_normalized?.executive || {}) as Record<string, unknown>;
                const tech = (item.data_normalized?.technical || {}) as Record<string, unknown>;
                return (
                  <div key={item.category} className="rounded-lg border border-gray-200 bg-white p-4">
                    <div className="flex items-baseline justify-between gap-4">
                      <div className="text-lg font-semibold text-gray-900">{item.category}</div>
                      {item.show_avg && item.avg != null ? (
                        <div className="text-sm text-gray-600">Avg: {item.avg}</div>
                      ) : null}
                    </div>
                    {item.error ? <div className="mt-2 text-sm text-red-600">{item.error}</div> : null}

                    <div className="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-4">
                      <div className="rounded-md bg-gray-50 p-3">
                        <div className="text-sm font-semibold text-gray-800 mb-2">Executive</div>
                        <div className="text-sm text-gray-700">
                          {typeof exec.summary === 'string' ? exec.summary : '—'}
                        </div>
                      </div>
                      <div className="rounded-md bg-gray-50 p-3">
                        <div className="text-sm font-semibold text-gray-800 mb-2">Technical</div>
                        <div className="text-sm text-gray-700">
                          {typeof tech.summary === 'string' ? tech.summary : '—'}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}

              {consolidated ? (
                <div className="rounded-xl border border-slate-200 bg-slate-50/40 p-5">
                  <div className="mb-5 flex items-start justify-between gap-4">
                    <div>
                      <div className="text-lg font-semibold text-slate-900">Consolidated Roadmap</div>
                      <p className="text-sm text-slate-600">Prioritized initiatives across near-term sprints and long-term outcomes.</p>
                    </div>
                    <div className="rounded-full bg-slate-200 px-3 py-1 text-xs font-medium text-slate-700">
                      Strategy View
                    </div>
                  </div>

                  <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                    <section className="rounded-lg border border-blue-100 bg-white p-4">
                      <div className="mb-3 flex items-center justify-between">
                        <div className="text-sm font-semibold text-blue-900">8-Week Focus</div>
                        <div className="text-xs text-blue-700">Execution Timeline</div>
                      </div>
                      <div className="space-y-3">
                        {sprintOrder.map((sprint) => {
                          const items = consolidated.focus_8w?.[sprint] || [];
                          return (
                            <div key={sprint} className="rounded-md border border-slate-200 bg-slate-50 p-3">
                              <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-700">
                                {formatPeriodLabel(sprint)}
                              </div>
                              {items.length ? (
                                <ul className="space-y-1.5">
                                  {items.map((it, idx) => (
                                    <li key={idx} className="flex gap-2 text-sm leading-relaxed text-slate-700">
                                      <span className="mt-1 h-1.5 w-1.5 rounded-full bg-blue-500" />
                                      <span>{it}</span>
                                    </li>
                                  ))}
                                </ul>
                              ) : (
                                <p className="text-sm text-slate-500">No items available.</p>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    </section>

                    <section className="rounded-lg border border-violet-100 bg-white p-4">
                      <div className="mb-3 flex items-center justify-between">
                        <div className="text-sm font-semibold text-violet-900">3-Year Plan</div>
                        <div className="text-xs text-violet-700">Strategic Horizon</div>
                      </div>
                      <div className="space-y-3">
                        {yearOrder.map((year) => {
                          const items = consolidated.plan_3y?.[year] || [];
                          return (
                            <div key={year} className="rounded-md border border-slate-200 bg-slate-50 p-3">
                              <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-700">
                                {formatPeriodLabel(year)}
                              </div>
                              {items.length ? (
                                <ul className="space-y-1.5">
                                  {items.map((it, idx) => (
                                    <li key={idx} className="flex gap-2 text-sm leading-relaxed text-slate-700">
                                      <span className="mt-1 h-1.5 w-1.5 rounded-full bg-violet-500" />
                                      <span>{it}</span>
                                    </li>
                                  ))}
                                </ul>
                              ) : (
                                <p className="text-sm text-slate-500">No items available.</p>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    </section>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-gray-600">
                  Click “View Roadmap” to generate a consolidated roadmap from the category outputs.
                </div>
              )}
            </div>
          ) : null}
        </CardContent>
      </Card>
    </div>
  );
}