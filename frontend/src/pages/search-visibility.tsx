import React, { useEffect, useState } from "react";
import {
  Search, Globe, CheckCircle, XCircle, AlertTriangle, ExternalLink,
  RefreshCw, Play, Filter, Eye
} from "lucide-react";
import { api } from "@/lib/api";

export default function SearchVisibilityPage() {
  const [observations, setObservations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedRawResponse, setSelectedRawResponse] = useState<any | null>(null);
  const [testingQuestionId, setTestingQuestionId] = useState<string | null>(null);
  const [searchFilter, setSearchFilter] = useState("");

  const loadObservations = async () => {
    try {
      setLoading(true);
      const data = await api.getSearchObservations({ limit: 150 });
      setObservations(data);
    } catch (err: any) {
      alert("Failed to load search observations: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadObservations();
  }, []);

  const handleRunSearchCheck = async (qId: string) => {
    try {
      setTestingQuestionId(qId);
      await api.runSearchCheck(qId, "mock");
      await loadObservations();
    } catch (err: any) {
      alert("Search check error: " + err.message);
    } finally {
      setTestingQuestionId(null);
    }
  };

  const filteredObservations = observations.filter((o) =>
    o.query.toLowerCase().includes(searchFilter.toLowerCase())
  );

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Google Search Visibility Tracker</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Observing rankings, Featured Snippets, People Also Ask (PAA), and Google AI Overviews for IncuBrix.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={loadObservations}
            className="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <RefreshCw size={13} /> Refresh Tracker
          </button>
        </div>
      </div>

      {/* Filter */}
      <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between gap-4">
        <div className="relative flex-1 max-w-md">
          <Search size={14} className="absolute left-3 top-2.5 text-slate-400" />
          <input
            type="text"
            placeholder="Filter search queries..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>
        <div className="text-xs text-slate-500">
          Total Observations: <strong className="text-slate-800">{filteredObservations.length}</strong>
        </div>
      </div>

      {/* Observations Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-sm text-slate-500 flex flex-col items-center gap-2">
            <RefreshCw className="animate-spin text-blue-600" size={24} />
            Loading search observation records...
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/80 text-slate-500 uppercase border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4 font-semibold">Query</th>
                  <th className="py-3 px-4 font-semibold">IncuBrix Ranking</th>
                  <th className="py-3 px-4 font-semibold">SERP Features</th>
                  <th className="py-3 px-4 font-semibold">AI Overview</th>
                  <th className="py-3 px-4 font-semibold">Competitors Seen</th>
                  <th className="py-3 px-4 font-semibold">Observed At</th>
                  <th className="py-3 px-4 font-semibold text-right">Raw / Test</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredObservations.map((obs) => (
                  <tr key={obs.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3 px-4 max-w-sm">
                      <div className="font-semibold text-slate-900">{obs.query}</div>
                      {obs.result_title && (
                        <div className="text-[11px] text-blue-600 truncate mt-0.5">
                          {obs.result_title}
                        </div>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      {obs.incubrix_ranking_position ? (
                        <span className={`inline-flex items-center gap-1 font-bold text-xs px-2 py-0.5 rounded ${
                          obs.incubrix_ranking_position <= 3
                            ? "bg-emerald-100 text-emerald-800"
                            : obs.incubrix_ranking_position <= 10
                            ? "bg-blue-100 text-blue-800"
                            : "bg-slate-100 text-slate-700"
                        }`}>
                          #{obs.incubrix_ranking_position}
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px] italic">Unranked (&gt;100)</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex flex-wrap gap-1">
                        {obs.has_featured_snippet && (
                          <span className="px-1.5 py-0.5 bg-amber-50 text-amber-700 border border-amber-200 rounded text-[10px] font-semibold">
                            Snippet
                          </span>
                        )}
                        {obs.has_people_also_ask && (
                          <span className="px-1.5 py-0.5 bg-indigo-50 text-indigo-700 border border-indigo-200 rounded text-[10px] font-semibold">
                            PAA
                          </span>
                        )}
                        {!obs.has_featured_snippet && !obs.has_people_also_ask && (
                          <span className="text-slate-400 text-[10px]">Standard</span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      {obs.has_ai_overview ? (
                        <span className={`inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full ${
                          obs.incubrix_cited_in_ai_overview
                            ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                            : "bg-slate-100 text-slate-600"
                        }`}>
                          <CheckCircle size={10} /> {obs.incubrix_cited_in_ai_overview ? "IncuBrix Cited" : "AIO Active"}
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px]">No AIO</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-slate-600 text-[11px]">
                      {obs.competitors_found && obs.competitors_found.length > 0 ? (
                        obs.competitors_found.slice(0, 3).join(", ")
                      ) : (
                        <span className="text-slate-400">-</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-[11px] text-slate-500 whitespace-nowrap">
                      {new Date(obs.observed_at).toLocaleDateString()} {new Date(obs.observed_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </td>
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => setSelectedRawResponse(obs.raw_response)}
                          className="p-1 text-slate-500 hover:text-blue-600 rounded"
                          title="View Raw Response"
                        >
                          <Eye size={13} />
                        </button>
                        <button
                          onClick={() => handleRunSearchCheck(obs.question_id)}
                          disabled={testingQuestionId === obs.question_id}
                          className="px-2 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-[11px] font-medium flex items-center gap-1"
                          title="Run Ad-Hoc Check"
                        >
                          {testingQuestionId === obs.question_id ? <RefreshCw size={11} className="animate-spin" /> : <Play size={10} fill="currentColor" />}
                          Check
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Raw Response Modal */}
      {selectedRawResponse && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6 space-y-3 max-h-[80vh] flex flex-col">
            <div className="flex justify-between items-center pb-2 border-b border-slate-200">
              <h3 className="text-sm font-bold text-slate-900">Raw Provider Response JSON</h3>
              <button
                onClick={() => setSelectedRawResponse(null)}
                className="text-xs text-slate-500 hover:text-slate-800 font-semibold"
              >
                Close
              </button>
            </div>
            <pre className="flex-1 overflow-y-auto bg-slate-900 text-slate-200 p-3 rounded-lg text-xs font-mono">
              {JSON.stringify(selectedRawResponse, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
