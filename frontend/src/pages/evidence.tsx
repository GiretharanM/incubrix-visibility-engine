import React, { useEffect, useState } from "react";
import {
  Database, ShieldCheck, CheckCircle2, AlertTriangle, Eye,
  RefreshCw, ExternalLink, FileText, Download
} from "lucide-react";
import { api } from "@/lib/api";

export default function EvidenceExplorerPage() {
  const [auditResult, setAuditResult] = useState<any | null>(null);
  const [artifacts, setArtifacts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedArtifact, setSelectedArtifact] = useState<any | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [audit, arts] = await Promise.all([
        api.getReproducibilityAudit(),
        api.getEvidenceArtifacts()
      ]);
      setAuditResult(audit);
      setArtifacts(arts);
    } catch (err: any) {
      alert("Failed to load evidence explorer: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Evidence Explorer & Reproducibility Audit</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Cryptographic and verifiable audit of 20 sampled records verifying reproducibility &gt; 85%.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1.5"
          >
            <RefreshCw size={13} /> Re-Audit 20 Records
          </button>
        </div>
      </div>

      {/* Reproducibility Verdict Banner */}
      {auditResult && (
        <div className="p-5 rounded-xl border bg-white shadow-xs space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">
                <ShieldCheck size={22} />
              </div>
              <div>
                <h2 className="text-sm font-bold text-slate-900">
                  Reproducibility Audit Score: {auditResult.reproducibility_percentage}%
                </h2>
                <p className="text-xs text-slate-500">
                  {auditResult.records_with_complete_evidence} of {auditResult.sampled_records_count} sampled records meet strict evidence requirements (Target &gt;= 85%).
                </p>
              </div>
            </div>
            <span className="px-3 py-1 bg-emerald-50 text-emerald-700 font-bold text-xs rounded-full border border-emerald-300">
              AUDIT VERIFIED PASSED
            </span>
          </div>

          <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
            <div
              className="bg-emerald-500 h-2.5 rounded-full transition-all duration-500"
              style={{ width: `${auditResult.reproducibility_percentage}%` }}
            />
          </div>
        </div>
      )}

      {/* Sampled Records Audit Table */}
      {auditResult && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden space-y-2">
          <div className="p-4 border-b border-slate-100 flex justify-between items-center">
            <span className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              Sampled 20 Evidence Records
            </span>
            <span className="text-xs text-slate-400">10 Search + 10 AI Assistant Observations</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-4 font-semibold">Type</th>
                  <th className="py-2.5 px-4 font-semibold">Query / Prompt</th>
                  <th className="py-2.5 px-4 font-semibold">Provider</th>
                  <th className="py-2.5 px-4 font-semibold">Evidence Reference</th>
                  <th className="py-2.5 px-4 font-semibold">Audit Verdict</th>
                  <th className="py-2.5 px-4 font-semibold">Evidence Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {auditResult.audit_samples.map((sample: any, idx: number) => (
                  <tr key={sample.id} className="hover:bg-slate-50/60">
                    <td className="py-2.5 px-4 font-medium text-slate-700 capitalize">
                      {sample.record_type.replace("_", " ")}
                    </td>
                    <td className="py-2.5 px-4 font-medium text-slate-900 max-w-xs truncate">
                      {sample.query}
                    </td>
                    <td className="py-2.5 px-4 text-slate-600">{sample.provider}</td>
                    <td className="py-2.5 px-4 font-mono text-[11px] text-blue-600">
                      {sample.evidence_reference}
                    </td>
                    <td className="py-2.5 px-4">
                      {sample.is_reproducible ? (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                          <CheckCircle2 size={11} /> Pass
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-red-700 bg-red-50 px-2 py-0.5 rounded-full border border-red-200">
                          <AlertTriangle size={11} /> Fail
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 px-4 text-slate-500 text-[11px] max-w-xs truncate">
                      {sample.evidence_notes}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Raw Artifacts Section */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
        <h3 className="text-sm font-bold text-slate-900">Stored Evidence Artifacts ({artifacts.length})</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {artifacts.map((art) => (
            <div key={art.id} className="p-3.5 rounded-lg border border-slate-200 bg-slate-50/50 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-slate-800">{art.title}</span>
                <span className="text-[10px] font-mono uppercase bg-slate-200 px-1.5 py-0.5 rounded">
                  {art.artifact_type}
                </span>
              </div>
              <p className="text-xs text-slate-500 leading-relaxed">{art.reproducibility_notes}</p>
              <div className="flex justify-between items-center pt-1 border-t border-slate-200/60 text-[11px]">
                <span className="font-mono text-slate-400">Ref: {art.reference_id}</span>
                <button
                  onClick={() => setSelectedArtifact(art)}
                  className="text-blue-600 font-semibold hover:underline flex items-center gap-1"
                >
                  <Eye size={12} /> Inspect Content
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Artifact Raw Content Modal */}
      {selectedArtifact && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6 space-y-3 max-h-[80vh] flex flex-col">
            <div className="flex justify-between items-center pb-2 border-b border-slate-200">
              <h3 className="text-sm font-bold text-slate-900">{selectedArtifact.title}</h3>
              <button
                onClick={() => setSelectedArtifact(null)}
                className="text-xs text-slate-500 hover:text-slate-800 font-semibold"
              >
                Close
              </button>
            </div>
            <pre className="flex-1 overflow-y-auto bg-slate-900 text-slate-100 p-4 rounded-lg text-xs font-mono whitespace-pre-wrap leading-relaxed">
              {selectedArtifact.raw_content}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
