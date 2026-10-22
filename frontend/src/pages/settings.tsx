import React, { useEffect, useState } from "react";
import {
  Settings, Key, CheckCircle, XCircle, AlertCircle,
  ExternalLink, Shield, RefreshCw
} from "lucide-react";
import { api } from "@/lib/api";

export default function SettingsPage() {
  const [settingsData, setSettingsData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getSettings().then((res) => {
      setSettingsData(res);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-sm text-slate-500">Loading settings...</div>;
  }

  const providers = [
    {
      name: "OpenAI API",
      envVar: "OPENAI_API_KEY",
      configured: settingsData.openai_configured,
      description: "Powers automated visibility checks against GPT-4o models."
    },
    {
      name: "Google Gemini API",
      envVar: "GEMINI_API_KEY",
      configured: settingsData.gemini_configured,
      description: "Powers direct answer and brand mention evaluations on Gemini 1.5 Pro / Flash."
    },
    {
      name: "Perplexity API",
      envVar: "PERPLEXITY_API_KEY",
      configured: settingsData.perplexity_configured,
      description: "Direct real-time conversational search evaluation via Sonar models."
    },
    {
      name: "Search Provider (SerpAPI / Google CSE)",
      envVar: "SEARCH_API_KEY",
      configured: settingsData.search_api_configured,
      description: "Live SERP data scraping for Google rankings, PAA, and AI Overviews."
    },
    {
      name: "Google PageSpeed Insights API",
      envVar: "PAGESPEED_API_KEY",
      configured: settingsData.pagespeed_configured,
      description: "Core Web Vitals and mobile performance score auditing."
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="pb-2 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight">Integrations & API Settings</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Verify connected search and AI providers. All credentials are securely managed via environment variables.
        </p>
      </div>

      {/* Target Website Card */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-2">
        <h3 className="text-sm font-bold text-slate-900">Configured Target Domain</h3>
        <div className="flex items-center gap-3">
          <input
            type="text"
            readOnly
            value={settingsData.target_website}
            className="px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg text-slate-800 font-mono w-72"
          />
          <a
            href={settingsData.target_website}
            target="_blank"
            rel="noreferrer"
            className="text-xs text-blue-600 hover:underline flex items-center gap-1 font-semibold"
          >
            Visit Live Site <ExternalLink size={12} />
          </a>
        </div>
      </div>

      {/* Providers Status List */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <span className="text-xs font-bold text-slate-900 uppercase tracking-wider">
            Provider Configuration Status
          </span>
          <span className="text-xs text-slate-400">Environment Variables Security Check</span>
        </div>
        <div className="divide-y divide-slate-100">
          {providers.map((p) => (
            <div key={p.envVar} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-slate-50/50">
              <div className="space-y-0.5">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-xs text-slate-900">{p.name}</span>
                  <code className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-mono">
                    {p.envVar}
                  </code>
                </div>
                <p className="text-xs text-slate-500">{p.description}</p>
              </div>

              <div>
                {p.configured ? (
                  <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                    <CheckCircle size={12} /> Configured in .env
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-[11px] font-medium text-slate-600 bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200">
                    Simulated / Fallback Mode
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Security Guidance Note */}
      <div className="p-4 rounded-xl bg-blue-50 border border-blue-200 space-y-1.5 text-xs text-blue-900">
        <div className="font-bold flex items-center gap-1.5">
          <Shield size={14} className="text-blue-700" /> Security Notice: Zero Secrets Committed
        </div>
        <p className="leading-relaxed">
          In compliance with Section 14, real API tokens are never saved to source code or git history. 
          To enable live external API calls, supply your keys in the local <code>.env</code> file. When an API key is absent, the engine seamlessly switches to deterministic evaluation adapters so that all workflows, metrics, and exports function uninterrupted.
        </p>
      </div>
    </div>
  );
}
