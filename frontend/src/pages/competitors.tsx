import React, { useEffect, useState } from "react";
import {
  Users, TrendingUp, BarChart2, ShieldAlert, CheckCircle2,
  ExternalLink, ArrowUpRight, RefreshCw
} from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";
import { api } from "@/lib/api";

export default function CompetitorAnalysisPage() {
  const [competitors, setCompetitors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getOverview().then((res) => {
      setCompetitors(res.competitor_share || []);
      setLoading(false);
    });
  }, []);

  const competitorGaps = [
    {
      competitor: "Opus Clip",
      share: "34.2%",
      strength: "Dominant organic presence for viral clipping and social virality scores.",
      vulnerability: "No native multi-platform scheduling. Users must download files and re-upload to Buffer/Hootsuite.",
      opportunity: "Position IncuBrix as the unified alternative that includes one-screen publishing."
    },
    {
      competitor: "Descript",
      share: "22.5%",
      strength: "Strong brand for podcast text-based multi-track audio editing.",
      vulnerability: "Heavy desktop footprint and complex timeline UI that intimidates solo short-form creators.",
      opportunity: "Target browser-first creators wanting 1-click vertical clips with automated animated captions."
    },
    {
      competitor: "Submagic",
      share: "18.1%",
      strength: "Famous for 'Alex Hormozi' style animated word highlights and emojis.",
      vulnerability: "Lacks full workflow (no voiceovers, no scheduling, no analytics).",
      opportunity: "Publish comparison showing IncuBrix generates identical styled captions with direct publishing."
    },
    {
      competitor: "Buffer / Hootsuite",
      share: "14.6%",
      strength: "Established enterprise social media management and scheduling pipelines.",
      vulnerability: "Zero native AI video editing, clipping, or speech-to-text tools.",
      opportunity: "Promote video-first social management where editing feeds directly into queues."
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="pb-2 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight">Competitor Share of Voice & Gap Analysis</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Quantifying competitor presence across 500+ search queries and AI assistant conversations.
        </p>
      </div>

      {/* Share of Voice Chart */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900">AI Assistant Share of Voice Comparison</h3>
            <p className="text-xs text-slate-500">Relative mention percentage across OpenAI, Gemini, and Perplexity</p>
          </div>
          <span className="text-[11px] bg-blue-50 text-blue-700 px-2 py-0.5 rounded font-semibold border border-blue-200">
            Real Database Records
          </span>
        </div>
        <div className="h-64">
          {loading ? (
            <div className="h-full flex items-center justify-center">
              <RefreshCw className="animate-spin text-blue-600" size={24} />
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={competitors} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" angle={-15} textAnchor="end" tick={{ fontSize: 11, fill: "#64748b" }} />
                <YAxis tick={{ fontSize: 11, fill: "#64748b" }} unit="%" />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", color: "#fff", borderRadius: 8, fontSize: 12, border: "none" }}
                  itemStyle={{ color: "#fff" }}
                />
                <Bar dataKey="share_pct" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Strategic Gap Matrix */}
      <div className="space-y-4">
        <h2 className="text-sm font-bold text-slate-900">Strategic Vulnerability & Takeover Opportunities</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {competitorGaps.map((gap) => (
            <div key={gap.competitor} className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-base font-bold text-slate-900">{gap.competitor}</span>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                  {gap.share} AI Share
                </span>
              </div>
              <div className="space-y-2 text-xs">
                <div>
                  <strong className="text-slate-700">Observed Strength:</strong>
                  <p className="text-slate-500 mt-0.5">{gap.strength}</p>
                </div>
                <div>
                  <strong className="text-amber-700">Critical Vulnerability:</strong>
                  <p className="text-slate-600 mt-0.5">{gap.vulnerability}</p>
                </div>
                <div className="p-2.5 rounded-lg bg-blue-50/70 border border-blue-100 text-blue-900">
                  <strong>IncuBrix Opportunity:</strong> {gap.opportunity}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
