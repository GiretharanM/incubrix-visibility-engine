import React, { useEffect, useState } from "react";
import {
  Wrench, CheckCircle, AlertTriangle, Copy, Check, Filter,
  ExternalLink, ChevronDown, ChevronUp, Code
} from "lucide-react";
import { api } from "@/lib/api";

export default function SEOFixesPage() {
  const [issues, setIssues] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedSeverity, setSelectedSeverity] = useState("all");
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const loadIssues = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (selectedCategory !== "all") params.category = selectedCategory;
      if (selectedSeverity !== "all") params.severity = selectedSeverity;
      const data = await api.getAuditIssues(params);
      setIssues(data);
    } catch (err: any) {
      alert("Failed to load issues: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIssues();
  }, [selectedCategory, selectedSeverity]);

  const handleStatusChange = async (id: string, newStatus: string) => {
    try {
      await api.updateIssueStatus(id, newStatus);
      setIssues((prev) =>
        prev.map((item) => (item.id === id ? { ...item, validation_status: newStatus } : item))
      );
    } catch (err: any) {
      alert("Failed to update status: " + err.message);
    }
  };

  const handleCopyCode = (id: string, code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case "critical":
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-800 uppercase">Critical</span>;
      case "high":
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-100 text-orange-800 uppercase">High</span>;
      case "medium":
        return <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-100 text-amber-800 uppercase">Medium</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700 uppercase">Low</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="pb-2 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight">Prioritized SEO & AEO Fixes</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          20 evidence-backed technical recommendations with ready-to-paste code and validation methods.
        </p>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <Filter size={13} />
            <span>Category:</span>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-700 font-medium focus:outline-none"
            >
              <option value="all">All Categories</option>
              <option value="crawlability">Crawlability & AEO</option>
              <option value="structured_data">Structured Data (JSON-LD)</option>
              <option value="metadata">Metadata & Social</option>
              <option value="content">Content & Alt Tags</option>
              <option value="performance">Performance & Hints</option>
              <option value="security">Security Headers</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <span>Severity:</span>
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-700 font-medium focus:outline-none"
            >
              <option value="all">All Severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>

        <div className="text-xs text-slate-500">
          Total Recommendations: <strong className="text-slate-800">{issues.length}</strong>
        </div>
      </div>

      {/* Issues List */}
      <div className="space-y-4">
        {issues.map((issue, idx) => (
          <div key={issue.id} className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-3.5">
            {/* Top row */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-400">#{idx + 1}</span>
                {getSeverityBadge(issue.severity)}
                <span className="text-[11px] font-medium bg-slate-100 text-slate-600 px-2 py-0.5 rounded capitalize">
                  {issue.category.replace("_", " ")}
                </span>
                <span className="text-xs text-blue-600 font-mono truncate max-w-xs">{issue.affected_url}</span>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-500">Validation Status:</span>
                <select
                  value={issue.validation_status}
                  onChange={(e) => handleStatusChange(issue.id, e.target.value)}
                  className={`text-xs font-semibold px-2 py-1 rounded border focus:outline-none ${
                    issue.validation_status === "verified"
                      ? "bg-emerald-50 text-emerald-700 border-emerald-300"
                      : issue.validation_status === "in_progress"
                      ? "bg-amber-50 text-amber-700 border-amber-300"
                      : "bg-slate-50 text-slate-700 border-slate-300"
                  }`}
                >
                  <option value="open">Open</option>
                  <option value="in_progress">In Progress</option>
                  <option value="fixed">Fixed</option>
                  <option value="verified">Verified</option>
                </select>
              </div>
            </div>

            {/* Title & Observed problem */}
            <div>
              <h3 className="text-sm font-bold text-slate-900">{issue.issue_title}</h3>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">{issue.observed_problem}</p>
            </div>

            {/* Evidence & Solution */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-slate-50 p-3 rounded-lg border border-slate-200/80">
              <div>
                <strong className="text-slate-700">Observed Evidence:</strong>
                <p className="text-slate-500 mt-0.5">{issue.evidence}</p>
              </div>
              <div>
                <strong className="text-slate-700">Recommended Solution:</strong>
                <p className="text-slate-500 mt-0.5">{issue.recommended_solution}</p>
              </div>
            </div>

            {/* Ready to paste code */}
            {issue.ready_to_paste_code && (
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-slate-700 flex items-center gap-1">
                    <Code size={13} /> Ready-to-Paste Code / Text
                  </span>
                  <button
                    onClick={() => handleCopyCode(issue.id, issue.ready_to_paste_code)}
                    className="px-2 py-0.5 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-medium flex items-center gap-1 transition-colors"
                  >
                    {copiedId === issue.id ? <Check size={11} className="text-emerald-600" /> : <Copy size={11} />}
                    {copiedId === issue.id ? "Copied!" : "Copy Code"}
                  </button>
                </div>
                <pre className="p-3 bg-slate-900 text-slate-100 rounded-lg text-xs font-mono overflow-x-auto max-h-48 leading-relaxed">
                  {issue.ready_to_paste_code}
                </pre>
              </div>
            )}

            {/* Validation Method */}
            <div className="text-[11px] text-slate-400">
              <strong>Validation Method:</strong> {issue.validation_method}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
