import React, { useEffect, useState } from "react";
import {
  Link2, CheckCircle, ExternalLink, Filter, Star,
  Send, AlertCircle, ArrowUpRight, RefreshCw
} from "lucide-react";
import { api } from "@/lib/api";

export default function CitationsPage() {
  const [citations, setCitations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedStatus, setSelectedStatus] = useState("all");

  const loadCitations = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (selectedCategory !== "all") params.category = selectedCategory;
      if (selectedStatus !== "all") params.outreach_status = selectedStatus;
      const data = await api.getCitations(params);
      setCitations(data);
    } catch (err: any) {
      alert("Failed to load citations: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCitations();
  }, [selectedCategory, selectedStatus]);

  const handleStatusChange = async (id: string, newStatus: string) => {
    try {
      await api.updateCitation(id, { outreach_status: newStatus });
      setCitations((prev) =>
        prev.map((c) => (c.id === id ? { ...c, outreach_status: newStatus } : c))
      );
    } catch (err: any) {
      alert("Failed to update status: " + err.message);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="pb-2 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight">Editorial Citation Opportunities</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          30 verified third-party pages with real URLs, competitor presence, editorial angles, and pitch resources.
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
              <option value="ai_tool_directory">AI Tool Directory</option>
              <option value="review_site">B2B Review Site (G2/Capterra)</option>
              <option value="editorial">Editorial News / Tech Publication</option>
              <option value="creator_marketing">Creator Marketing Blog</option>
              <option value="comparison_article">Software Comparison</option>
              <option value="community">Community Wiki (Reddit)</option>
              <option value="educational">Educational Resource</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <span>Outreach Status:</span>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-700 font-medium focus:outline-none"
            >
              <option value="all">All Statuses</option>
              <option value="ready_for_pitch">Ready for Pitch</option>
              <option value="identified">Identified</option>
              <option value="pitched">Pitched</option>
              <option value="secured">Secured Citation</option>
            </select>
          </div>
        </div>

        <div className="text-xs text-slate-500">
          Opportunities: <strong className="text-slate-800">{citations.length}</strong>
        </div>
      </div>

      {/* Citations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {citations.map((c) => (
          <div key={c.id} className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-3 flex flex-col justify-between">
            <div className="space-y-2.5">
              {/* Header row */}
              <div className="flex items-center justify-between gap-2">
                <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-700 uppercase tracking-wide">
                  {c.source_category.replace("_", " ")}
                </span>
                <div className="flex items-center gap-1 text-amber-600 font-bold text-xs">
                  <Star size={13} fill="currentColor" /> {c.priority_score}/100 Priority
                </div>
              </div>

              <div>
                <a
                  href={c.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-sm font-bold text-slate-900 hover:text-blue-600 flex items-center gap-1.5 group"
                >
                  {c.page_title}
                  <ExternalLink size={12} className="text-slate-400 group-hover:text-blue-600" />
                </a>
                <div className="text-[11px] text-slate-400 font-mono mt-0.5">{c.domain}</div>
              </div>

              <div className="text-xs text-slate-600 leading-relaxed">
                <strong>Relevance:</strong> {c.evidence_of_relevance}
              </div>

              {/* Competitors & IncuBrix Value */}
              <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200/80 text-xs space-y-1.5">
                <div>
                  <span className="text-slate-500 font-medium">Competitors on Page: </span>
                  <span className="font-semibold text-slate-700">
                    {c.competitors_present?.join(", ") || "None"}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 font-medium">Editorial Angle: </span>
                  <span className="text-slate-700">{c.editorial_angle}</span>
                </div>
                <div className="text-blue-900 font-medium">
                  <span>IncuBrix Value Add: </span>
                  {c.incubrix_value_add}
                </div>
              </div>

              <div className="text-xs text-slate-700">
                <strong>Suggested Deliverable:</strong> {c.suggested_resource_to_create}
              </div>
            </div>

            {/* Footer status selector */}
            <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
              <span className="text-slate-400 text-[11px]">Verification: Verified Link</span>
              <div className="flex items-center gap-2">
                <span className="text-slate-500">Status:</span>
                <select
                  value={c.outreach_status}
                  onChange={(e) => handleStatusChange(c.id, e.target.value)}
                  className={`text-xs font-semibold px-2 py-0.5 rounded border focus:outline-none ${
                    c.outreach_status === "secured"
                      ? "bg-emerald-50 text-emerald-700 border-emerald-300"
                      : "bg-slate-50 text-slate-700 border-slate-300"
                  }`}
                >
                  <option value="ready_for_pitch">Ready for Pitch</option>
                  <option value="identified">Identified</option>
                  <option value="pitched">Pitched</option>
                  <option value="secured">Secured</option>
                </select>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
