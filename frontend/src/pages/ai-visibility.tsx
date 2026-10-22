import React, { useEffect, useState } from "react";
import {
  Bot, CheckCircle, AlertCircle, ExternalLink, Plus, Filter,
  RefreshCw, Eye, MessageSquare, Award, Link2
} from "lucide-react";
import { api } from "@/lib/api";

export default function AIVisibilityPage() {
  const [observations, setObservations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedProvider, setSelectedProvider] = useState("all");
  const [selectedStatus, setSelectedStatus] = useState("all");
  const [selectedAnswer, setSelectedAnswer] = useState<any | null>(null);
  const [showImportModal, setShowImportModal] = useState(false);
  const [questions, setQuestions] = useState<any[]>([]);

  // Manual import state
  const [importQuestionId, setImportQuestionId] = useState("");
  const [importProvider, setImportProvider] = useState("claude_manual");
  const [importModel, setImportModel] = useState("claude-3-5-sonnet");
  const [importRawAnswer, setImportRawAnswer] = useState("");

  const loadObservations = async () => {
    try {
      setLoading(true);
      const params: any = { limit: 150 };
      if (selectedProvider !== "all") params.provider = selectedProvider;
      if (selectedStatus !== "all") params.status = selectedStatus;
      const data = await api.getAIObservations(params);
      setObservations(data);
    } catch (err: any) {
      alert("Failed to load AI observations: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadObservations();
    api.getQuestions({ limit: 100 }).then((res) => {
      setQuestions(res);
      if (res.length > 0) setImportQuestionId(res[0].id);
    });
  }, [selectedProvider, selectedStatus]);

  const handleManualImport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!importRawAnswer.trim() || !importQuestionId) return;
    try {
      const q = questions.find((item) => item.id === importQuestionId);
      await api.importManualAI({
        question_id: importQuestionId,
        provider: importProvider,
        model: importModel,
        prompt: q?.question_text || "Manual Query",
        raw_answer: importRawAnswer.trim(),
        evidence_reference: "manual_paste_import"
      });
      setShowImportModal(false);
      setImportRawAnswer("");
      loadObservations();
    } catch (err: any) {
      alert("Import failed: " + err.message);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "incubrix_cited":
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800">
            <Link2 size={11} /> Cited with URL
          </span>
        );
      case "incubrix_recommended":
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-blue-100 text-blue-800">
            <Award size={11} /> Recommended
          </span>
        );
      case "incubrix_mentioned":
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-purple-100 text-purple-800">
            <Bot size={11} /> Mentioned
          </span>
        );
      case "competitors_only":
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">
            Competitors Only
          </span>
        );
      default:
        return (
          <span className="text-slate-400 text-[11px] italic">No Mention</span>
        );
    }
  };

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">AI Assistant Visibility Engine</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Tracking ChatGPT (OpenAI), Google Gemini, Perplexity, and Claude for IncuBrix mentions and citations.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowImportModal(true)}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <Plus size={13} /> Manual Answer Import
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <Filter size={13} />
            <span>Provider:</span>
            <select
              value={selectedProvider}
              onChange={(e) => setSelectedProvider(e.target.value)}
              className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-700 font-medium focus:outline-none"
            >
              <option value="all">All Providers</option>
              <option value="openai">OpenAI (GPT-4o)</option>
              <option value="gemini">Google Gemini</option>
              <option value="perplexity">Perplexity (Sonar)</option>
              <option value="claude_manual">Claude (Manual)</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <span>Classification:</span>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-700 font-medium focus:outline-none"
            >
              <option value="all">All Statuses</option>
              <option value="incubrix_cited">IncuBrix Cited</option>
              <option value="incubrix_recommended">IncuBrix Recommended</option>
              <option value="incubrix_mentioned">IncuBrix Mentioned</option>
              <option value="competitors_only">Competitors Only</option>
              <option value="no_mention">No Mention</option>
            </select>
          </div>
        </div>

        <div className="text-xs text-slate-500">
          Showing <strong className="text-slate-800">{observations.length}</strong> observations
        </div>
      </div>

      {/* Observations Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-sm text-slate-500 flex flex-col items-center gap-2">
            <RefreshCw className="animate-spin text-blue-600" size={24} />
            Loading AI assistant observations...
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/80 text-slate-500 uppercase border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4 font-semibold">Prompt / Query</th>
                  <th className="py-3 px-4 font-semibold">Assistant</th>
                  <th className="py-3 px-4 font-semibold">Classification</th>
                  <th className="py-3 px-4 font-semibold">Competitors Mentioned</th>
                  <th className="py-3 px-4 font-semibold">Citations</th>
                  <th className="py-3 px-4 font-semibold">Observed At</th>
                  <th className="py-3 px-4 font-semibold text-right">View Answer</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {observations.map((obs) => (
                  <tr key={obs.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3 px-4 max-w-sm font-medium text-slate-900">
                      {obs.prompt.replace("Answer this question thoroughly for a content creator: ", "")}
                    </td>
                    <td className="py-3 px-4">
                      <div className="font-semibold text-slate-800 capitalize">{obs.provider.replace("_", " ")}</div>
                      <div className="text-[11px] text-slate-400">{obs.model}</div>
                    </td>
                    <td className="py-3 px-4">
                      {getStatusBadge(obs.classification_status)}
                    </td>
                    <td className="py-3 px-4 text-slate-600 text-[11px]">
                      {obs.competitors_mentioned && obs.competitors_mentioned.length > 0 ? (
                        obs.competitors_mentioned.slice(0, 3).join(", ")
                      ) : (
                        <span className="text-slate-400">None</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      {obs.citation_urls && obs.citation_urls.length > 0 ? (
                        <span className="text-blue-600 font-medium text-[11px] underline">
                          {obs.citation_urls.length} URL(s)
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px]">None</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-[11px] text-slate-500 whitespace-nowrap">
                      {new Date(obs.observed_at).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => setSelectedAnswer(obs)}
                        className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-[11px] font-medium inline-flex items-center gap-1"
                      >
                        <Eye size={12} /> Read
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Answer View Modal */}
      {selectedAnswer && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6 space-y-4 max-h-[85vh] flex flex-col">
            <div className="flex justify-between items-start pb-3 border-b border-slate-200">
              <div>
                <div className="text-xs text-blue-600 font-bold uppercase">{selectedAnswer.provider} • {selectedAnswer.model}</div>
                <h3 className="text-sm font-bold text-slate-900 mt-0.5">{selectedAnswer.prompt}</h3>
              </div>
              <button
                onClick={() => setSelectedAnswer(null)}
                className="text-xs text-slate-500 hover:text-slate-800 font-semibold"
              >
                Close
              </button>
            </div>
            <div className="flex items-center gap-2 text-xs">
              <span>Status:</span> {getStatusBadge(selectedAnswer.classification_status)}
            </div>
            <div className="flex-1 overflow-y-auto bg-slate-50 border border-slate-200 rounded-lg p-4 text-xs leading-relaxed text-slate-800 whitespace-pre-wrap">
              {selectedAnswer.raw_answer}
            </div>
          </div>
        </div>
      )}

      {/* Manual Import Modal */}
      {showImportModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6 space-y-4">
            <h2 className="text-base font-bold text-slate-900">Import Assistant Response (Claude, Copilot, etc.)</h2>
            <p className="text-xs text-slate-500">
              Paste the verbatim answer generated by a consumer assistant. The engine will automatically classify brand mentions, recommendations, citations, and competitors.
            </p>
            <form onSubmit={handleManualImport} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Target Question *</label>
                <select
                  value={importQuestionId}
                  onChange={(e) => setImportQuestionId(e.target.value)}
                  className="w-full px-2.5 py-1.5 text-xs border border-slate-300 rounded-lg"
                >
                  {questions.map((q) => (
                    <option key={q.id} value={q.id}>{q.question_text}</option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Provider</label>
                  <select
                    value={importProvider}
                    onChange={(e) => setImportProvider(e.target.value)}
                    className="w-full px-2.5 py-1.5 text-xs border border-slate-300 rounded-lg"
                  >
                    <option value="claude_manual">Anthropic Claude</option>
                    <option value="copilot_manual">Microsoft Copilot</option>
                    <option value="deepseek_manual">DeepSeek</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Model Version</label>
                  <input
                    type="text"
                    value={importModel}
                    onChange={(e) => setImportModel(e.target.value)}
                    placeholder="claude-3-5-sonnet"
                    className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Raw Assistant Output *</label>
                <textarea
                  required
                  rows={6}
                  value={importRawAnswer}
                  onChange={(e) => setImportRawAnswer(e.target.value)}
                  placeholder="Paste the assistant's full response here..."
                  className="w-full px-3 py-2 text-xs border border-slate-300 rounded-lg"
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowImportModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg"
                >
                  Save & Classify
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
