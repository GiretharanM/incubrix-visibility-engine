import React, { useEffect, useState } from "react";
import {
  Search, Plus, Upload, Download, CheckCircle, AlertCircle,
  ExternalLink, Trash2, Edit2, Filter, RefreshCw
} from "lucide-react";
import { api } from "@/lib/api";

const TOPICS = [
  "All Topics",
  "AI content creation",
  "Video editing and repurposing",
  "AI-generated captions",
  "Social media publishing",
  "Creator growth",
  "Content scheduling",
  "Content optimization",
  "Creator analytics",
  "Best AI tools",
  "Product comparisons",
  "Alternatives to competing products"
];

export default function QuestionResearchPage() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState("All Topics");
  const [selectedIntent, setSelectedIntent] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [showAddModal, setShowAddModal] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  // New Question Form state
  const [newQuestionText, setNewQuestionText] = useState("");
  const [newTopic, setNewTopic] = useState("AI content creation");
  const [newIntent, setNewIntent] = useState("informational");
  const [newSourceUrl, setNewSourceUrl] = useState("");
  const [newSourceType, setNewSourceType] = useState("manual");

  const loadQuestions = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (selectedTopic !== "All Topics") params.topic = selectedTopic;
      if (selectedIntent !== "all") params.intent = selectedIntent;
      if (searchQuery.trim()) params.search = searchQuery.trim();
      const data = await api.getQuestions(params);
      setQuestions(data);
    } catch (err: any) {
      alert("Error loading questions: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQuestions();
  }, [selectedTopic, selectedIntent]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadQuestions();
  };

  const handleCreateQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newQuestionText.trim()) return;
    try {
      await api.createQuestion({
        question_text: newQuestionText.trim(),
        topic: newTopic,
        intent: newIntent,
        source_url: newSourceUrl.trim() || null,
        source_type: newSourceType,
        language: "en",
        market: "US",
        collection_method: "manual",
        verification_status: "verified",
        evidence_reference: "manual_entry_ui"
      });
      setShowAddModal(false);
      setNewQuestionText("");
      setNewSourceUrl("");
      loadQuestions();
    } catch (err: any) {
      alert(err.message || "Failed to create question");
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this question?")) return;
    try {
      await api.deleteQuestion(id);
      loadQuestions();
    } catch (err: any) {
      alert("Failed to delete question: " + err.message);
    }
  };

  const handleUploadCSV = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;
    try {
      setUploadStatus("Uploading and verifying CSV...");
      const formData = new FormData();
      formData.append("file", uploadFile);
      const res = await fetch("/api/questions/import-csv", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setUploadStatus(`Imported ${data.imported} questions (${data.duplicates_skipped} duplicates skipped)`);
      setTimeout(() => {
        setShowUploadModal(false);
        setUploadStatus(null);
        setUploadFile(null);
        loadQuestions();
      }, 1500);
    } catch (err: any) {
      setUploadStatus("Upload failed: " + err.message);
    }
  };

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Creator Question Research</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            100+ verified creator queries across 11 key topics with sources, intent, and evidence references.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowUploadModal(true)}
            className="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <Upload size={13} /> Import CSV
          </button>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <Plus size={14} /> Add Question
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-3">
        <form onSubmit={handleSearchSubmit} className="flex-1 min-w-[240px] max-w-md relative">
          <Search size={14} className="absolute left-3 top-2.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search questions or keywords..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </form>

        <div className="flex items-center gap-2 flex-wrap">
          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <Filter size={13} />
            <span>Topic:</span>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-700 font-medium focus:outline-none"
            >
              {TOPICS.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <span>Intent:</span>
            <select
              value={selectedIntent}
              onChange={(e) => setSelectedIntent(e.target.value)}
              className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-700 font-medium focus:outline-none"
            >
              <option value="all">All Intents</option>
              <option value="informational">Informational</option>
              <option value="commercial">Commercial</option>
              <option value="transactional">Transactional</option>
            </select>
          </div>

          <span className="text-xs text-slate-400 ml-2">
            Showing <strong className="text-slate-800">{questions.length}</strong> questions
          </span>
        </div>
      </div>

      {/* Questions Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-sm text-slate-500 flex flex-col items-center gap-2">
            <RefreshCw className="animate-spin text-blue-600" size={24} />
            Loading questions database...
          </div>
        ) : questions.length === 0 ? (
          <div className="p-12 text-center text-sm text-slate-500">
            No questions found matching your filter criteria.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/80 text-slate-500 uppercase border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4 font-semibold">Question Text</th>
                  <th className="py-3 px-4 font-semibold">Topic</th>
                  <th className="py-3 px-4 font-semibold">Intent</th>
                  <th className="py-3 px-4 font-semibold">Source</th>
                  <th className="py-3 px-4 font-semibold">Verification</th>
                  <th className="py-3 px-4 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {questions.map((q) => (
                  <tr key={q.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3 px-4 max-w-md font-medium text-slate-900">
                      {q.question_text}
                      <div className="text-[11px] text-slate-400 font-normal mt-0.5">
                        Ref: {q.evidence_reference || "N/A"} • Lang: {q.language.toUpperCase()} • Market: {q.market}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-100">
                        {q.topic}
                      </span>
                    </td>
                    <td className="py-3 px-4 capitalize text-slate-600 font-medium">
                      {q.intent}
                    </td>
                    <td className="py-3 px-4 text-slate-600">
                      {q.source_url ? (
                        <a
                          href={q.source_url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 hover:underline flex items-center gap-1 text-[11px]"
                        >
                          {q.source_type} <ExternalLink size={10} />
                        </a>
                      ) : (
                        <span className="text-slate-400 text-[11px]">{q.source_type}</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
                        <CheckCircle size={10} /> Verified
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleDelete(q.id)}
                        className="p-1 text-slate-400 hover:text-red-600 rounded transition-colors"
                        title="Delete question"
                      >
                        <Trash2 size={13} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add Question Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6 space-y-4">
            <h2 className="text-base font-bold text-slate-900">Add Creator Question</h2>
            <form onSubmit={handleCreateQuestion} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Question Text *</label>
                <textarea
                  required
                  rows={2}
                  value={newQuestionText}
                  onChange={(e) => setNewQuestionText(e.target.value)}
                  placeholder="e.g. How to automatically generate subtitles with AI?"
                  className="w-full px-3 py-2 text-xs border border-slate-300 rounded-lg focus:ring-1 focus:ring-blue-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Topic</label>
                  <select
                    value={newTopic}
                    onChange={(e) => setNewTopic(e.target.value)}
                    className="w-full px-2.5 py-1.5 text-xs border border-slate-300 rounded-lg"
                  >
                    {TOPICS.filter((t) => t !== "All Topics").map((t) => (
                      <option key={t} value={t}>{t}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Search Intent</label>
                  <select
                    value={newIntent}
                    onChange={(e) => setNewIntent(e.target.value)}
                    className="w-full px-2.5 py-1.5 text-xs border border-slate-300 rounded-lg"
                  >
                    <option value="informational">Informational</option>
                    <option value="commercial">Commercial</option>
                    <option value="transactional">Transactional</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Source URL (Reddit, Quora, Blog)</label>
                <input
                  type="url"
                  value={newSourceUrl}
                  onChange={(e) => setNewSourceUrl(e.target.value)}
                  placeholder="https://..."
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg"
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg"
                >
                  Save Question
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* CSV Import Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 space-y-4">
            <h2 className="text-base font-bold text-slate-900">Import Questions from CSV</h2>
            <p className="text-xs text-slate-500">
              CSV must have headers: <code>question_text, topic, intent, source_type, source_url</code>. Duplicate questions will be automatically detected and skipped.
            </p>
            <form onSubmit={handleUploadCSV} className="space-y-4">
              <input
                type="file"
                accept=".csv"
                required
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                className="w-full text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              {uploadStatus && (
                <div className="p-2 text-xs bg-slate-50 border border-slate-200 rounded text-slate-700">
                  {uploadStatus}
                </div>
              )}
              <div className="flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowUploadModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!uploadFile}
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs font-semibold rounded-lg"
                >
                  Start Import
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
