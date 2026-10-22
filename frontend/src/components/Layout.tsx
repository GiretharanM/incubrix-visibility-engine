import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import {
  LayoutDashboard, HelpCircle, Search, Bot, Users, Activity,
  Wrench, FileText, Link2, FileBarChart, Calendar, Database,
  History, Settings, Menu, X, ExternalLink, Play
} from "lucide-react";

interface LayoutProps {
  children: React.ReactNode;
}

const NAV_ITEMS = [
  { href: "/", label: "Overview Dashboard", icon: LayoutDashboard },
  { href: "/questions", label: "Question Research", icon: HelpCircle },
  { href: "/search-visibility", label: "Search Visibility", icon: Search },
  { href: "/ai-visibility", label: "AI Visibility", icon: Bot },
  { href: "/competitors", label: "Competitor Analysis", icon: Users },
  { href: "/audit", label: "Technical SEO Audit", icon: Activity },
  { href: "/seo-fixes", label: "SEO Fixes", icon: Wrench },
  { href: "/content-studio", label: "Content Studio", icon: FileText },
  { href: "/citations", label: "Citation Opportunities", icon: Link2 },
  { href: "/reports", label: "Weekly Reports", icon: FileBarChart },
  { href: "/growth-plan", label: "90-Day Growth Plan", icon: Calendar },
  { href: "/evidence", label: "Evidence Explorer", icon: Database },
  { href: "/runs", label: "Measurement History", icon: History },
  { href: "/settings", label: "Integrations & Settings", icon: Settings },
];

export default function Layout({ children }: LayoutProps) {
  const router = useRouter();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [market, setMarket] = useState("US");

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 overflow-hidden">
      {/* Sidebar - Desktop */}
      <aside className="hidden lg:flex lg:flex-col w-64 bg-slate-950 text-slate-300 border-r border-slate-800 flex-shrink-0">
        {/* Brand */}
        <div className="p-5 border-b border-slate-800/80">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-black text-lg shadow-md shadow-blue-500/20">
              I
            </div>
            <div>
              <div className="font-bold text-white text-base tracking-tight flex items-center gap-1.5">
                IncuBrix Engine
                <span className="text-[10px] font-semibold bg-blue-500/20 text-blue-400 px-1.5 py-0.5 rounded border border-blue-500/30">v1.0</span>
              </div>
              <a
                href="https://incubrix.com"
                target="_blank"
                rel="noreferrer"
                className="text-xs text-slate-400 hover:text-blue-400 flex items-center gap-1 transition-colors mt-0.5"
              >
                incubrix.com <ExternalLink size={11} />
              </a>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const active = router.pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2 text-xs font-medium rounded-lg transition-all ${
                  active
                    ? "bg-blue-600 text-white shadow-sm shadow-blue-600/30 font-semibold"
                    : "text-slate-300 hover:bg-slate-900 hover:text-white"
                }`}
              >
                <Icon size={16} className={active ? "text-white" : "text-slate-400"} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Footer Quick Action */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-900/40">
          <Link
            href="/runs"
            className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-semibold rounded-lg bg-blue-600/10 text-blue-400 hover:bg-blue-600 hover:text-white border border-blue-500/20 transition-all"
          >
            <Play size={13} fill="currentColor" />
            Run Measurement
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Navbar */}
        <header className="h-14 border-b border-slate-200 bg-white px-5 flex items-center justify-between z-10">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="lg:hidden p-1.5 text-slate-600 hover:bg-slate-100 rounded-md"
            >
              {mobileOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
            <h1 className="text-sm font-semibold text-slate-800 capitalize">
              {NAV_ITEMS.find((n) => n.href === router.pathname)?.label || "Dashboard"}
            </h1>
          </div>

          <div className="flex items-center gap-4">
            {/* Market Selection */}
            <div className="flex items-center gap-1.5 text-xs text-slate-500">
              <span className="hidden sm:inline">Market:</span>
              <select
                value={market}
                onChange={(e) => setMarket(e.target.value)}
                className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs text-slate-700 font-medium focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="US">🇺🇸 United States (US)</option>
                <option value="UK">🇬🇧 United Kingdom (UK)</option>
                <option value="CA">🇨🇦 Canada (CA)</option>
                <option value="IN">🇮🇳 India (IN)</option>
              </select>
            </div>

            {/* Live Status indicator */}
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[11px] font-medium text-emerald-700">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              Live Sync
            </div>
          </div>
        </header>

        {/* Mobile Navigation Drawer */}
        {mobileOpen && (
          <div className="lg:hidden fixed inset-0 z-50 bg-slate-900/70 flex">
            <div className="w-64 bg-slate-950 text-slate-300 h-full p-4 flex flex-col">
              <div className="flex justify-between items-center mb-4 pb-2 border-b border-slate-800">
                <span className="font-bold text-white text-sm">Navigation</span>
                <button onClick={() => setMobileOpen(false)} className="text-slate-400">
                  <X size={18} />
                </button>
              </div>
              <div className="space-y-1 overflow-y-auto flex-1">
                {NAV_ITEMS.map((item) => {
                  const Icon = item.icon;
                  const active = router.pathname === item.href;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setMobileOpen(false)}
                      className={`flex items-center gap-3 px-3 py-2 text-xs font-medium rounded-lg ${
                        active ? "bg-blue-600 text-white" : "text-slate-300 hover:bg-slate-900"
                      }`}
                    >
                      <Icon size={16} />
                      {item.label}
                    </Link>
                  );
                })}
              </div>
            </div>
            <div className="flex-1" onClick={() => setMobileOpen(false)} />
          </div>
        )}

        {/* Page Content Body */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
