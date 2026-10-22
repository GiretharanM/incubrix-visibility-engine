import React, { useEffect, useState } from "react";
import {
  History, Play, CheckCircle, AlertTriangle, Clock,
  RefreshCw, DollarSign, Database, Settings
} from "lucide-react";
import { api } from "@/lib/api";

export default function MeasurementRunsPage() {
  const [runs, setRuns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showRunModal, setShowRunModal] = useState(false);
  const [running, setRunning] = useState(false);

  // New Run parameters
  const [runName, setRunName] = useState("");
  const [market, setMarket] = useState("US");
  const [searchProvider, setSearchProvider] = useState("mock");
  const [selectedAI, setSelectedAI] = useState<string[]>(["openai", "gemini", "perplexity", "claude_manual"]);

  const loadRuns = async () => {
    try {
      setLoading(true);
      const data = await api.getRuns();
      setRuns(data);
    } catch (err: any) {
      alert("Failed to load runs: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRuns();
  }, []);

  const handleStartRun = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setRunning(true);
      const name = runName.trim() || `Measurement Run (${new Date().toLocaleDateString()})`;
      await api.triggerRun({
        run_name: name,
        market: market,
        search_provider: searchProvider,
        ai_providers: selectedAI
      });
      setShowRunModal(false);
      setRunName("");
      await loadRuns();
      alert("Measurement run executed and results stored in database!");
    } catch (err: any) {
      alert("Run error: " + err.message);
    } finally {
      setRunning(false);
    }
  };

  const toggleAIProvider = (provider: string) => {
    if (selectedAI.includes(provider)) {
      if (selectedAI.length > 1) {
        setSelectedAI(selectedAI.filter((p) => p !== provider));
      }
    } else {
      setSelectedAI([...selectedAI, provider]);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Measurement Run History</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Audit logs, configuration snapshots, runtime durations, and cost estimates across multi-day runs.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowRunModal(true)}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <Play size={13} fill="currentColor" /> Trigger Measurement Run
          </button>
        </div>
      </div>

      {/* Runs Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-sm text-slate-500 flex flex-col items-center gap-2">
            <RefreshCw className="animate-spin text-blue-600" size={24} />
            Loading measurement runs...
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/80 text-slate-500 uppercase border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4 font-semibold">Run Name</th>
                  <th className="py-3 px-4 font-semibold">Status</th>
                  <th className="py-3 px-4 font-semibold">Market</th>
                  <th className="py-3 px-4 font-semibold">Questions</th>
                  <th className="py-3 px-4 font-semibold">Successful Measurements</th>
                  <th className="py-3 px-4 font-semibold">Cost (USD)</th>
                  <th className="py-3 px-4 font-semibold">Executed At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {runs.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3 px-4">
                      <div className="font-bold text-slate-900">{r.run_name}</div>
                      <div className="text-[11px] text-slate-400 font-mono mt-0.5">ID: {r.id.slice(0, 8)}...</div>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full capitalize ${
                        r.status === "completed"
                          ? "bg-emerald-50 text-emerald-800 border border-emerald-200"
                          : r.status === "running"
                          ? "bg-blue-50 text-blue-800 border border-blue-200"
                          : "bg-amber-50 text-amber-800 border border-amber-200"
                      }`}>
                        {r.status === "completed" && <CheckCircle size={10} />}
                        {r.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-700">{r.market}</td>
                    <td className="py-3 px-4 font-medium text-slate-800">{r.questions_count}</td>
                    <td className="py-3 px-4 text-emerald-600 font-bold">
                      {r.successful_measurements}
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-700">
                      ${r.estimated_cost_usd?.toFixed(2) || "0.00"}
                    </td>
                    <td className="py-3 px-4 text-slate-500 text-[11px] whitespace-nowrap">
                      {new Date(r.start_time).toLocaleDateString()} {new Date(r.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Trigger Run Modal */}
      {showRunModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 space-y-4">
            <h2 className="text-base font-bold text-slate-900">Trigger New Measurement Run</h2>
            <p className="text-xs text-slate-500">
              Executes search queries and AI prompts across all verified questions. One failed provider will never cancel unrelated provider jobs.
            </p>
            <form onSubmit={handleStartRun} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Run Name</label>
                <input
                  type="text"
                  placeholder="e.g. Week 43 Growth Measurement Run"
                  value={runName}
                  onChange={(e) => setRunName(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Target Market</label>
                  <select
                    value={market}
                    onChange={(e) => setMarket(e.target.value)}
                    className="w-full px-2.5 py-1.5 text-xs border border-slate-300 rounded-lg"
                  >
                    <option value="US">United States (US)</option>
                    <option value="UK">United Kingdom (UK)</option>
                    <option value="CA">Canada (CA)</option>
                    <option value="IN">India (IN)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Search Provider</label>
                  <select
                    value={searchProvider}
                    onChange={(e) => setSearchProvider(e.target.value)}
                    className="w-full px-2.5 py-1.5 text-xs border border-slate-300 rounded-lg"
                  >
                    <option value="mock">Standard Search Engine</option>
                    <option value="serpapi">SerpAPI (Google)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1.5">AI Assistants to Measure</label>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  {[
                    { id: "openai", name: "OpenAI GPT-4o" },
                    { id: "gemini", name: "Google Gemini" },
                    { id: "perplexity", name: "Perplexity Sonar" },
                    { id: "claude_manual", name: "Anthropic Claude" }
                  ].map((p) => (
                    <label key={p.id} className="flex items-center gap-2 p-2 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50">
                      <input
                        type="checkbox"
                        checked={selectedAI.includes(p.id)}
                        onChange={() => toggleAIProvider(p.id)}
                        className="rounded text-blue-600"
                      />
                      <span className="font-medium text-slate-800">{p.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowRunModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={running}
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5"
                >
                  {running ? <RefreshCw size={12} className="animate-spin" /> : <Play size={11} fill="currentColor" />}
                  {running ? "Processing..." : "Start Run"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
