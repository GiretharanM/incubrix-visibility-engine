import React, { useEffect, useState } from "react";
import {
  Calendar, CheckCircle, Clock, AlertTriangle, User,
  Wrench, DollarSign, Target, Award, Edit2
} from "lucide-react";
import { api } from "@/lib/api";

export default function GrowthPlanPage() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingTask, setEditingTask] = useState<any | null>(null);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const data = await api.getGrowthPlan();
      setTasks(data);
    } catch (err: any) {
      alert("Failed to load growth plan: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleUpdateStatus = async (id: string, newStatus: string) => {
    try {
      await api.updateGrowthPlanTask(id, { status: newStatus });
      setTasks((prev) =>
        prev.map((t) => (t.id === id ? { ...t, status: newStatus } : t))
      );
    } catch (err: any) {
      alert("Status update failed: " + err.message);
    }
  };

  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTask) return;
    try {
      await api.updateGrowthPlanTask(editingTask.id, {
        actual_metric: editingTask.actual_metric,
        target_metric: editingTask.target_metric,
        status: editingTask.status,
        owner: editingTask.owner,
        budget_usd: parseFloat(editingTask.budget_usd) || 0
      });
      setTasks((prev) =>
        prev.map((t) => (t.id === editingTask.id ? editingTask : t))
      );
      setEditingTask(null);
    } catch (err: any) {
      alert("Failed to save changes: " + err.message);
    }
  };

  const getPriorityBadge = (p: string) => {
    switch (p.toLowerCase()) {
      case "critical":
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-800 uppercase">Critical</span>;
      case "high":
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-100 text-orange-800 uppercase">High</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700 uppercase">Medium</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="pb-2 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight">13-Week / 90-Day Growth Plan</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Structured execution plan for IncuBrix across Technical SEO, Content Publishing, AI Visibility, and Citations.
        </p>
      </div>

      {/* Timeline List */}
      <div className="space-y-4">
        {tasks.map((task) => (
          <div key={task.id} className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-3.5">
            {/* Top row */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="w-7 h-7 rounded-lg bg-blue-600 text-white font-extrabold text-xs flex items-center justify-center">
                  W{task.week_number}
                </span>
                <span className="text-xs font-semibold text-slate-500">{task.phase_name}</span>
                {getPriorityBadge(task.priority)}
                <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-blue-50 text-blue-700 uppercase">
                  {task.task_category.replace("_", " ")}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <select
                  value={task.status}
                  onChange={(e) => handleUpdateStatus(task.id, e.target.value)}
                  className={`text-xs font-semibold px-2.5 py-1 rounded border focus:outline-none capitalize ${
                    task.status === "completed"
                      ? "bg-emerald-50 text-emerald-800 border-emerald-300"
                      : task.status === "in_progress"
                      ? "bg-blue-50 text-blue-800 border-blue-300"
                      : "bg-slate-50 text-slate-700 border-slate-300"
                  }`}
                >
                  <option value="planned">Planned</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="blocked">Blocked</option>
                </select>
                <button
                  onClick={() => setEditingTask(task)}
                  className="p-1 text-slate-400 hover:text-blue-600 rounded"
                  title="Edit task targets"
                >
                  <Edit2 size={13} />
                </button>
              </div>
            </div>

            {/* Task Title & Description */}
            <div>
              <h3 className="text-sm font-bold text-slate-900">{task.task_title}</h3>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">{task.task_description}</p>
            </div>

            {/* Deliverables & Targets Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div>
                <strong className="text-slate-700">Deliverables:</strong>
                <p className="text-slate-600 mt-0.5">{task.deliverables}</p>
              </div>
              <div className="space-y-1">
                <div>
                  <strong className="text-slate-700">Target Metric:</strong>
                  <span className="text-blue-700 ml-1 font-semibold">{task.target_metric}</span>
                </div>
                <div>
                  <strong className="text-slate-700">Actual Metric:</strong>
                  <span className={`ml-1 font-semibold ${task.status === "completed" ? "text-emerald-700" : "text-slate-500"}`}>
                    {task.actual_metric}
                  </span>
                </div>
              </div>
            </div>

            {/* Footer Metadata */}
            <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-400 gap-2 pt-1 border-t border-slate-100">
              <div className="flex items-center gap-3">
                <span className="flex items-center gap-1 text-slate-600">
                  <User size={12} /> Owner: <strong>{task.owner}</strong>
                </span>
                <span className="flex items-center gap-1 text-slate-600">
                  <Wrench size={12} /> Tools: {task.tools}
                </span>
              </div>
              <div>Budget: <strong>${task.budget_usd.toFixed(2)} USD</strong></div>
            </div>
          </div>
        ))}
      </div>

      {/* Edit Task Modal */}
      {editingTask && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 space-y-4">
            <h2 className="text-base font-bold text-slate-900">Edit Week {editingTask.week_number} Target & Metrics</h2>
            <form onSubmit={handleSaveEdit} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Target Metric</label>
                <input
                  type="text"
                  value={editingTask.target_metric}
                  onChange={(e) => setEditingTask({ ...editingTask, target_metric: e.target.value })}
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Actual Metric (Measured)</label>
                <input
                  type="text"
                  value={editingTask.actual_metric}
                  onChange={(e) => setEditingTask({ ...editingTask, actual_metric: e.target.value })}
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Owner</label>
                  <input
                    type="text"
                    value={editingTask.owner}
                    onChange={(e) => setEditingTask({ ...editingTask, owner: e.target.value })}
                    className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Budget ($)</label>
                  <input
                    type="number"
                    value={editingTask.budget_usd}
                    onChange={(e) => setEditingTask({ ...editingTask, budget_usd: e.target.value })}
                    className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setEditingTask(null)}
                  className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
