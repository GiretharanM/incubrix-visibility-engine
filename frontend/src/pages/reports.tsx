import React, { useEffect, useState } from "react";
import {
  FileBarChart, Download, CheckCircle, TrendingUp,
  AlertTriangle, Globe, Bot, Award, ExternalLink, Calendar
} from "lucide-react";
import { api } from "@/lib/api";

export default function WeeklyReportsPage() {
  const [report, setReport] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getLatestWeeklyReport().then((res) => {
      setReport(res);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-sm text-slate-500">Loading weekly reports...</div>;
  }

  if (!report) {
    return <div className="p-12 text-center text-sm text-slate-500">No report generated yet.</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">{report.title}</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Week: <span className="font-semibold text-slate-800">{report.report_week}</span> • Period:{" "}
            {new Date(report.period_start).toLocaleDateString()} – {new Date(report.period_end).toLocaleDateString()}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <a
            href="/api/reports/weekly/download-html"
            target="_blank"
            rel="noreferrer"
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <Download size={13} /> Printable HTML Report
          </a>
          <a
            href="/api/exports/submission-workbook-csv"
            download="submission_workbook.csv"
            className="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-lg shadow-xs"
          >
            Submission Workbook (.csv)
          </a>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium">Google Organic Coverage</div>
          <div className="mt-2 text-2xl font-extrabold text-blue-600">{report.google_organic_coverage_pct}%</div>
          <div className="text-[11px] text-slate-400 mt-1">Avg rank: #{report.google_avg_position}</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium">AI Brand Mention Rate</div>
          <div className="mt-2 text-2xl font-extrabold text-purple-600">{report.ai_mention_rate_pct}%</div>
          <div className="text-[11px] text-emerald-600 font-medium mt-1">+6.8% delta</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium">AI Recommendation Rate</div>
          <div className="mt-2 text-2xl font-extrabold text-emerald-600">{report.ai_recommendation_rate_pct}%</div>
          <div className="text-[11px] text-slate-400 mt-1">Direct endorsement</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium">AI URL Citation Rate</div>
          <div className="mt-2 text-2xl font-extrabold text-indigo-600">{report.ai_citation_rate_pct}%</div>
          <div className="text-[11px] text-slate-400 mt-1">Backlink in answer</div>
        </div>
      </div>

      {/* Report Content Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-2">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-2">Executive Summary</h3>
          <p className="text-xs text-slate-700 leading-relaxed">{report.executive_summary}</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-2">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-2">Technical SEO & AEO Health</h3>
          <p className="text-xs text-slate-700 leading-relaxed">{report.technical_health_summary}</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-2">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-2">Content Studio Production</h3>
          <p className="text-xs text-slate-700 leading-relaxed">{report.content_production_status}</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-2">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-2">Citation Opportunities</h3>
          <p className="text-xs text-slate-700 leading-relaxed">{report.citation_opportunities_summary}</p>
        </div>
      </div>

      {/* Recommended Next Actions */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
        <h3 className="text-sm font-bold text-slate-900">Recommended Strategic Actions for IncuBrix</h3>
        <div className="space-y-2">
          {report.recommended_next_actions?.map((act: string, idx: number) => (
            <div key={idx} className="flex items-start gap-2.5 text-xs text-slate-800 bg-slate-50 p-3 rounded-lg border border-slate-100">
              <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-700 font-bold flex items-center justify-center text-[10px] flex-shrink-0 mt-0.5">
                {idx + 1}
              </span>
              <span className="leading-relaxed">{act}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
