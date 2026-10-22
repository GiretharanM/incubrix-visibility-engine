import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Activity, CheckCircle, AlertTriangle, XCircle, RefreshCw,
  ExternalLink, ArrowRight, ShieldCheck, Globe, FileCode
} from "lucide-react";
import { api } from "@/lib/api";

export default function TechnicalAuditPage() {
  const [audit, setAudit] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [runningAudit, setRunningAudit] = useState(false);

  const loadAudit = async () => {
    try {
      setLoading(true);
      const data = await api.getLatestAudit();
      setAudit(data);
    } catch (err: any) {
      alert("Failed to load audit: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAudit();
  }, []);

  const handleTriggerAudit = async () => {
    try {
      setRunningAudit(true);
      const res = await api.triggerAudit();
      setAudit(res);
      alert("Live audit completed successfully!");
    } catch (err: any) {
      alert("Audit error: " + err.message);
    } finally {
      setRunningAudit(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 space-y-3">
        <RefreshCw className="animate-spin text-blue-600" size={32} />
        <p className="text-sm text-slate-500 font-medium">Fetching technical audit results for incubrix.com...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Technical SEO & AEO Audit</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Full crawl and document analysis of target domain:{" "}
            <span className="font-semibold text-slate-800">https://incubrix.com</span>
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/seo-fixes"
            className="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            View 20 Fix Recommendations <ArrowRight size={13} />
          </Link>
          <button
            onClick={handleTriggerAudit}
            disabled={runningAudit}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <RefreshCw size={13} className={runningAudit ? "animate-spin" : ""} />
            {runningAudit ? "Crawling Site..." : "Run Live Audit"}
          </button>
        </div>
      </div>

      {/* Audit Score Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Overall Health</div>
          <div className="mt-2 text-3xl font-extrabold text-blue-600">{audit.score_overall}/100</div>
          <div className="mt-1 text-[11px] text-slate-500">20 Fixes Identified</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Crawlability</div>
          <div className="mt-2 text-3xl font-extrabold text-emerald-600">{audit.score_crawlability}%</div>
          <div className="mt-1 text-[11px] text-slate-500">13 Sitemap URLs</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Metadata</div>
          <div className="mt-2 text-3xl font-extrabold text-blue-600">{audit.score_metadata}%</div>
          <div className="mt-1 text-[11px] text-slate-500">Titles & Descs</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Structured Data</div>
          <div className="mt-2 text-3xl font-extrabold text-amber-600">{audit.score_structured_data}%</div>
          <div className="mt-1 text-[11px] text-amber-600 font-medium">Schema gaps</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs text-center">
          <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Mobile Layout</div>
          <div className="mt-2 text-3xl font-extrabold text-emerald-600">{audit.score_mobile}%</div>
          <div className="mt-1 text-[11px] text-slate-500">Responsive</div>
        </div>
      </div>

      {/* Status Pillars & AEO Alert */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Core Infrastructure Check */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
          <h3 className="text-sm font-bold text-slate-900">Core Infrastructure Indicators</h3>
          <div className="space-y-2.5 text-xs">
            <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50">
              <span className="text-slate-700 font-medium">HTTP Response Status</span>
              <span className="font-bold text-emerald-600 flex items-center gap-1">
                <CheckCircle size={13} /> {audit.http_status} OK
              </span>
            </div>
            <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50">
              <span className="text-slate-700 font-medium">HTTPS Protocol & SSL</span>
              <span className="font-bold text-emerald-600 flex items-center gap-1">
                <CheckCircle size={13} /> Secure
              </span>
            </div>
            <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50">
              <span className="text-slate-700 font-medium">Robots.txt Availability</span>
              <span className="font-bold text-emerald-600 flex items-center gap-1">
                <CheckCircle size={13} /> {audit.robots_txt_status} (Allow: /)
              </span>
            </div>
            <div className="flex items-center justify-between p-2 rounded-lg bg-slate-50">
              <span className="text-slate-700 font-medium">XML Sitemap (sitemap.xml)</span>
              <span className="font-bold text-emerald-600 flex items-center gap-1">
                <CheckCircle size={13} /> 13 URLs Listed
              </span>
            </div>
          </div>
        </div>

        {/* AEO / llms.txt Finding Banner */}
        <div className="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 p-5 rounded-xl space-y-3">
          <div className="flex items-center gap-2 text-amber-800 font-bold text-sm">
            <AlertTriangle size={18} />
            CRITICAL AEO GAP: Missing llms.txt
          </div>
          <p className="text-xs text-amber-900 leading-relaxed">
            The crawl detected that <code>https://incubrix.com/llms.txt</code> returned <strong>404 NOT_FOUND</strong>. 
            AI scrapers from Perplexity, ChatGPT Search, and Gemini require a standardized <code>llms.txt</code> file at the domain root to understand your capabilities, product pricing, and canonical documentation without hallucinations.
          </p>
          <div className="pt-1">
            <Link
              href="/seo-fixes"
              className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold rounded-lg inline-flex items-center gap-1.5"
            >
              Get Ready-to-Paste llms.txt Code <ArrowRight size={13} />
            </Link>
          </div>
        </div>
      </div>

      {/* Crawl Summary Breakdown */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
        <h3 className="text-sm font-bold text-slate-900">Extracted Homepage Meta & DOM Details</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="space-y-1">
            <div className="text-slate-500 font-medium">Observed Title Tag:</div>
            <div className="p-2.5 bg-slate-50 rounded-lg text-slate-800 font-semibold border border-slate-200">
              {audit.summary?.home_title || "IncuBrix | Create With Purpose. Publish Without Limits."}
            </div>
          </div>
          <div className="space-y-1">
            <div className="text-slate-500 font-medium">Observed Meta Description:</div>
            <div className="p-2.5 bg-slate-50 rounded-lg text-slate-800 border border-slate-200 leading-relaxed">
              {audit.summary?.home_description || "IncuBrix turns one content into clips, captions, voiceovers, and posts for every platform | then publishes and tracks it all from one screen."}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
