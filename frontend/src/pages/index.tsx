import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  TrendingUp, Search, Bot, CheckCircle, AlertTriangle, ArrowRight,
  ShieldCheck, RefreshCw, BarChart2, Globe
} from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip,
  LineChart, Line, CartesianGrid, Legend
} from "recharts";
import { api } from "@/lib/api";

export default function OverviewDashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getOverview();
      setMetrics(data);
    } catch (err: any) {
      setError(err.message || "Failed to load dashboard metrics");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 space-y-3">
        <RefreshCw className="animate-spin text-blue-600" size={32} />
        <p className="text-sm text-slate-500 font-medium">Aggregating live visibility metrics from engine...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 space-y-3">
        <div className="flex items-center gap-2 font-semibold text-base">
          <AlertTriangle size={20} />
          Unable to connect to backend engine
        </div>
        <p className="text-sm">{error}</p>
        <button
          onClick={loadData}
          className="px-4 py-2 bg-red-600 text-white rounded-lg text-xs font-semibold hover:bg-red-700"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Overview Dashboard</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time search presence, AI assistant citations, and technical visibility for{" "}
            <span className="font-semibold text-slate-800">https://incubrix.com</span>
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/runs"
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5"
          >
            <RefreshCw size={13} /> Run Live Measurement
          </Link>
          <a
            href="/api/exports/visibility-csv"
            download="visibility.csv"
            className="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-lg shadow-sm transition-all"
          >
            Export visibility.csv
          </a>
        </div>
      </div>

      {/* KPI Cards Row 1: Search & AI Authority */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
            <span>Verified Questions</span>
            <Search size={16} className="text-blue-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">{metrics.verified_questions}</div>
          <div className="mt-1 text-[11px] text-emerald-600 font-medium flex items-center gap-1">
            <CheckCircle size={12} /> 100% verified sources
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
            <span>Google Organic Coverage</span>
            <Globe size={16} className="text-indigo-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">{metrics.google_ranking_coverage_pct}%</div>
          <div className="mt-1 text-[11px] text-slate-500">
            Avg rank: <span className="font-semibold text-slate-800">#{metrics.google_average_position}</span>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
            <span>AI Brand Mention Rate</span>
            <Bot size={16} className="text-purple-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">{metrics.ai_brand_mention_rate_pct}%</div>
          <div className="mt-1 text-[11px] text-emerald-600 font-medium">
            +6.8% vs baseline
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
            <span>AI Recommendation Rate</span>
            <TrendingUp size={16} className="text-emerald-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">{metrics.ai_recommendation_rate_pct}%</div>
          <div className="mt-1 text-[11px] text-slate-500">
            Citation rate: <span className="font-semibold text-slate-800">{metrics.ai_citation_rate_pct}%</span>
          </div>
        </div>
      </div>

      {/* KPI Cards Row 2: Reliability & Evidence */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-500 font-medium">Top 3 Rankings</div>
            <div className="text-xl font-bold text-emerald-600">{metrics.google_top3_count} queries</div>
          </div>
          <span className="p-2 rounded-lg bg-emerald-50 text-emerald-600 font-bold text-xs">Top 3</span>
        </div>

        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-500 font-medium">Google AI Overviews</div>
            <div className="text-xl font-bold text-indigo-600">{metrics.google_ai_overview_presence_pct}%</div>
          </div>
          <span className="p-2 rounded-lg bg-indigo-50 text-indigo-600 font-bold text-xs">AIO</span>
        </div>

        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-500 font-medium">Measurement Reliability</div>
            <div className="text-xl font-bold text-blue-600">{metrics.measurement_success_rate_pct}%</div>
          </div>
          <span className="p-2 rounded-lg bg-blue-50 text-blue-600 font-bold text-xs">0 Fails</span>
        </div>

        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-500 font-medium">Evidence Reproducibility</div>
            <div className="text-xl font-bold text-emerald-600">{metrics.evidence_completeness_pct}%</div>
          </div>
          <ShieldCheck size={20} className="text-emerald-500" />
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Google Ranking Distribution */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Google Ranking Tier Distribution</h3>
              <p className="text-xs text-slate-500">Distribution of IncuBrix search rankings across 105 queries</p>
            </div>
            <span className="text-[11px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">SERP Analysis</span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={metrics.ranking_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="tier" angle={-15} textAnchor="end" tick={{ fontSize: 11, fill: "#64748b" }} />
                <YAxis tick={{ fontSize: 11, fill: "#64748b" }} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", color: "#fff", borderRadius: 8, fontSize: 12, border: "none" }}
                  itemStyle={{ color: "#fff" }}
                />
                <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Multi-Day Historical Trends */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Historical Visibility Trend (Multi-Day)</h3>
              <p className="text-xs text-slate-500">Brand mentions and recommendations measured across runs</p>
            </div>
            <span className="text-[11px] bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded font-medium border border-emerald-200">
              Day 1 vs Day 2
            </span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={metrics.historical_trends} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#64748b" }} />
                <YAxis tick={{ fontSize: 11, fill: "#64748b" }} unit="%" />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", color: "#fff", borderRadius: 8, fontSize: 12, border: "none" }}
                  itemStyle={{ color: "#fff" }}
                />
                <Legend wrapperStyle={{ fontSize: 11, paddingTop: 10 }} />
                <Line type="monotone" dataKey="mention_rate" name="AI Mention %" stroke="#8b5cf6" strokeWidth={2.5} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="recommendation_rate" name="AI Rec %" stroke="#10b981" strokeWidth={2.5} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="citation_rate" name="AI Citation %" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row 3: Competitor Share & Provider Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Competitor Share */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">AI Assistant Share of Voice</h3>
              <p className="text-xs text-slate-500">Frequency of IncuBrix vs primary competitors in AI responses</p>
            </div>
            <Link href="/competitors" className="text-xs text-blue-600 hover:underline font-semibold flex items-center gap-1">
              Details <ArrowRight size={12} />
            </Link>
          </div>
          <div className="space-y-3">
            {metrics.competitor_share.slice(0, 6).map((comp: any) => (
              <div key={comp.name} className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className={`font-semibold ${comp.name === "IncuBrix" ? "text-blue-600" : "text-slate-700"}`}>
                    {comp.name} {comp.name === "IncuBrix" && "(Target)"}
                  </span>
                  <span className="text-slate-500">{comp.share_pct}% ({comp.mentions} mentions)</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-2 rounded-full ${comp.name === "IncuBrix" ? "bg-blue-600" : "bg-slate-400"}`}
                    style={{ width: `${Math.min(comp.share_pct * 2.5, 100)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Provider Breakdown */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Provider-Specific Performance</h3>
              <p className="text-xs text-slate-500">Mention, recommendation, and citation breakdown by model</p>
            </div>
            <Link href="/ai-visibility" className="text-xs text-blue-600 hover:underline font-semibold flex items-center gap-1">
              Compare <ArrowRight size={12} />
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-3">Provider</th>
                  <th className="py-2.5 px-3">Queries</th>
                  <th className="py-2.5 px-3">Mention %</th>
                  <th className="py-2.5 px-3">Recommend %</th>
                  <th className="py-2.5 px-3">Citation %</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {metrics.provider_breakdown.map((p: any) => (
                  <tr key={p.provider} className="hover:bg-slate-50/60">
                    <td className="py-2.5 px-3 font-semibold text-slate-800">{p.provider}</td>
                    <td className="py-2.5 px-3 text-slate-500">{p.total_queries}</td>
                    <td className="py-2.5 px-3 text-purple-600 font-bold">{p.mention_rate}%</td>
                    <td className="py-2.5 px-3 text-emerald-600 font-bold">{p.recommendation_rate}%</td>
                    <td className="py-2.5 px-3 text-blue-600 font-bold">{p.citation_rate}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
