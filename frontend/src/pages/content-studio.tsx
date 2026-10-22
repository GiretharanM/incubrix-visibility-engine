import React, { useEffect, useState } from "react";
import {
  FileText, Plus, Save, Download, Eye, CheckCircle2,
  Edit3, ArrowLeft, RefreshCw, Sparkles, Code
} from "lucide-react";
import { api } from "@/lib/api";

export default function ContentStudioPage() {
  const [pages, setPages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activePage, setActivePage] = useState<any | null>(null);
  const [editMode, setEditMode] = useState<"edit" | "preview">("edit");
  const [saving, setSaving] = useState(false);
  const [showGenerateModal, setShowGenerateModal] = useState(false);

  // Generate draft inputs
  const [genKeyword, setGenKeyword] = useState("");
  const [genTopic, setGenTopic] = useState("Video editing and repurposing");
  const [genType, setGenType] = useState("how_to");

  const loadPages = async () => {
    try {
      setLoading(true);
      const data = await api.getContentPages();
      setPages(data);
      if (data.length > 0 && !activePage) {
        setActivePage(data[0]);
      }
    } catch (err: any) {
      alert("Failed to load content pages: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPages();
  }, []);

  const handleSavePage = async () => {
    if (!activePage) return;
    try {
      setSaving(true);
      const updated = await api.updateContentPage(activePage.id, {
        title: activePage.title,
        direct_answer: activePage.direct_answer,
        markdown_content: activePage.markdown_content,
        meta_title: activePage.meta_title,
        meta_description: activePage.meta_description,
        status: activePage.status
      });
      setActivePage(updated);
      setPages((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
      alert("Draft saved successfully with version increment!");
    } catch (err: any) {
      alert("Save failed: " + err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleGenerateDraft = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!genKeyword.trim()) return;
    try {
      setSaving(true);
      const draft = await api.generateDraft(genTopic, genKeyword.trim(), genType);
      const created = await api.createContentPage(draft);
      setPages([created, ...pages]);
      setActivePage(created);
      setShowGenerateModal(false);
      setGenKeyword("");
      alert("Generated publish-ready draft successfully!");
    } catch (err: any) {
      alert("Generation failed: " + err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Content Generation & Studio</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            10 publish-ready draft pages with 2-sentence opening direct answers for AEO and structured JSON-LD.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowGenerateModal(true)}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <Sparkles size={13} /> Generate New Page
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Draft Pages List */}
        <div className="lg:col-span-4 bg-white rounded-xl border border-slate-200 shadow-xs p-4 space-y-3">
          <div className="flex justify-between items-center pb-2 border-b border-slate-100">
            <span className="text-xs font-bold text-slate-900 uppercase tracking-wider">Draft Articles ({pages.length})</span>
            <span className="text-[11px] text-slate-400">Select to edit</span>
          </div>

          <div className="space-y-2 overflow-y-auto max-h-[720px] pr-1">
            {pages.map((p) => {
              const selected = activePage?.id === p.id;
              return (
                <div
                  key={p.id}
                  onClick={() => setActivePage(p)}
                  className={`p-3 rounded-lg border text-left cursor-pointer transition-all ${
                    selected
                      ? "bg-blue-50/80 border-blue-400 shadow-xs"
                      : "bg-slate-50/60 border-slate-200 hover:bg-slate-100/60"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase text-blue-600">
                      {p.page_type.replace("_", " ")}
                    </span>
                    <span className={`text-[10px] font-semibold px-1.5 py-0.2 rounded capitalize ${
                      p.status === "approved"
                        ? "bg-emerald-100 text-emerald-800"
                        : "bg-amber-100 text-amber-800"
                    }`}>
                      {p.status} (v{p.version})
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-slate-800 mt-1 line-clamp-2">{p.title}</h4>
                  <div className="text-[11px] text-slate-500 mt-1 line-clamp-2 leading-relaxed">
                    {p.direct_answer}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Active Editor & Details */}
        <div className="lg:col-span-8 space-y-4">
          {activePage ? (
            <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
              {/* Editor Header Bar */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-200">
                <div className="flex items-center gap-2">
                  <div className="inline-flex rounded-lg bg-slate-100 p-0.5 text-xs font-medium">
                    <button
                      onClick={() => setEditMode("edit")}
                      className={`px-3 py-1 rounded-md transition-all ${
                        editMode === "edit" ? "bg-white text-slate-900 shadow-xs font-semibold" : "text-slate-600"
                      }`}
                    >
                      Markdown Editor
                    </button>
                    <button
                      onClick={() => setEditMode("preview")}
                      className={`px-3 py-1 rounded-md transition-all ${
                        editMode === "preview" ? "bg-white text-slate-900 shadow-xs font-semibold" : "text-slate-600"
                      }`}
                    >
                      Live Preview
                    </button>
                  </div>
                  <select
                    value={activePage.status}
                    onChange={(e) => setActivePage({ ...activePage, status: e.target.value })}
                    className="text-xs font-semibold px-2 py-1 rounded border border-slate-300 bg-white"
                  >
                    <option value="draft">Draft</option>
                    <option value="reviewed">Reviewed</option>
                    <option value="approved">Approved</option>
                    <option value="published">Published</option>
                  </select>
                </div>

                <div className="flex items-center gap-2">
                  <a
                    href={`/api/content/pages/${activePage.id}/export-markdown`}
                    className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-lg flex items-center gap-1"
                  >
                    <Download size={12} /> .md
                  </a>
                  <button
                    onClick={handleSavePage}
                    disabled={saving}
                    className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
                  >
                    <Save size={13} /> {saving ? "Saving..." : "Save Draft"}
                  </button>
                </div>
              </div>

              {/* Title & SEO Metadata */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div>
                  <label className="block text-slate-600 font-medium mb-1">Page Title & H1</label>
                  <input
                    type="text"
                    value={activePage.title}
                    onChange={(e) => setActivePage({ ...activePage, title: e.target.value })}
                    className="w-full px-3 py-1.5 border border-slate-300 rounded-lg font-semibold"
                  />
                </div>
                <div>
                  <label className="block text-slate-600 font-medium mb-1">Target Keyword & Intent</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={activePage.target_keyword}
                      disabled
                      className="w-full px-3 py-1.5 border border-slate-200 bg-slate-50 text-slate-600 rounded-lg"
                    />
                    <span className="px-2 py-1 bg-blue-50 text-blue-700 font-bold rounded capitalize">
                      {activePage.search_intent}
                    </span>
                  </div>
                </div>
              </div>

              {/* 2-Sentence Direct Answer (AEO Critical) */}
              <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-lg space-y-1">
                <div className="text-xs font-bold text-amber-900 flex items-center justify-between">
                  <span>AEO Direct Answer (Opening 2 Sentences for AI Engines & Snippets)</span>
                  <span className="text-[10px] bg-amber-200 text-amber-900 px-1.5 py-0.5 rounded font-bold">AEO Hook</span>
                </div>
                <textarea
                  rows={2}
                  value={activePage.direct_answer}
                  onChange={(e) => setActivePage({ ...activePage, direct_answer: e.target.value })}
                  className="w-full p-2 text-xs bg-white border border-amber-300 rounded focus:outline-none focus:ring-1 focus:ring-amber-500 font-medium text-slate-800"
                />
              </div>

              {/* Content Editor vs Preview */}
              {editMode === "edit" ? (
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Markdown Body Content</label>
                  <textarea
                    rows={16}
                    value={activePage.markdown_content}
                    onChange={(e) => setActivePage({ ...activePage, markdown_content: e.target.value })}
                    className="w-full p-3 text-xs font-mono border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 leading-relaxed bg-slate-50/30"
                  />
                </div>
              ) : (
                <div className="border border-slate-200 rounded-lg p-5 min-h-[360px] bg-white text-slate-800 text-xs leading-relaxed space-y-3 prose max-w-none">
                  <div className="p-3 bg-blue-50 border-l-4 border-blue-600 rounded text-xs text-blue-950 font-medium leading-relaxed">
                    {activePage.direct_answer}
                  </div>
                  <div className="whitespace-pre-wrap font-sans text-xs text-slate-700 leading-relaxed">
                    {activePage.markdown_content}
                  </div>
                </div>
              )}

              {/* JSON-LD Schema Preview */}
              {activePage.json_ld_schema && (
                <div className="space-y-1">
                  <span className="text-xs font-semibold text-slate-700 flex items-center gap-1">
                    <Code size={12} /> Validated JSON-LD Structured Data
                  </span>
                  <pre className="p-3 bg-slate-900 text-slate-100 rounded-lg text-[11px] font-mono overflow-x-auto max-h-36">
                    {JSON.stringify(activePage.json_ld_schema, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          ) : (
            <div className="p-12 text-center text-slate-400 bg-white rounded-xl border border-slate-200">
              Select an article from the left to view or edit.
            </div>
          )}
        </div>
      </div>

      {/* Generate Draft Modal */}
      {showGenerateModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 space-y-4">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Sparkles size={16} className="text-blue-600" /> Generate Publish-Ready Page
            </h2>
            <form onSubmit={handleGenerateDraft} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Target Keyword / Topic *</label>
                <input
                  type="text"
                  required
                  value={genKeyword}
                  onChange={(e) => setGenKeyword(e.target.value)}
                  placeholder="e.g. video speech to text accuracy"
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Page Type</label>
                <select
                  value={genType}
                  onChange={(e) => setGenType(e.target.value)}
                  className="w-full px-2.5 py-1.5 text-xs border border-slate-300 rounded-lg"
                >
                  <option value="how_to">How-To Article</option>
                  <option value="comparison">Product Comparison</option>
                  <option value="alternatives">Alternatives Guide</option>
                  <option value="faq_hub">FAQ Hub</option>
                  <option value="glossary">Glossary Page</option>
                  <option value="workflow_guide">Creator Workflow Guide</option>
                </select>
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowGenerateModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg"
                >
                  {saving ? "Generating..." : "Generate Content"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
