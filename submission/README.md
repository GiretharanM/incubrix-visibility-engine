# IncuBrix AEO, SEO & GEO Visibility Engine — Submission Package

**Candidate**: Senior Full-Stack & Growth Engineer Assessment  
**Option**: Option 3 — AEO, SEO and GEO Visibility Engine  
**Target Domain**: [https://incubrix.com](https://incubrix.com)  

---

## 📂 Submission Directory Structure

```
submission/
├── visibility.csv                 # Complete 19-column CSV export across 105 creator questions
├── research/
│   └── observations_and_opportunities.md  # 5 Product observations & 3 Growth opportunities
├── evidence/                      # Verified raw server captures, headers, and DOM snapshots
│   ├── README.md                  # Evidence artifacts index
│   ├── audit_baseline.html        # Live HTML DOM snapshot of incubrix.com
│   ├── evidence_llms_404.txt      # HTTP 404 response header proof for /llms.txt
│   ├── ai_obs_sample_0.txt        # OpenAI GPT-4o raw comparison response
│   ├── perplexity_obs_q12.txt     # Perplexity Sonar response with citations
│   ├── gemini_obs_q45.txt         # Google Gemini 1.5 Pro workflow evaluation
│   └── serp_run_baseline_q1.json  # Google SERP ranking snapshot
├── seo-fixes/
│   ├── prioritized_fixes.md       # 20 Prioritized technical fixes with ready-to-paste code
│   └── fixes.csv                  # Tabular export of the 20 technical issues
├── content-pages/                 # 10 Complete, publish-ready content drafts
│   ├── README.md                  # Content inventory
│   ├── 01_how-to-turn-long-youtube-videos-into-viral-shorts.md
│   ├── 02_incubrix-vs-opus-clip-comparison.md
│   ├── 03_cheaper-opus-clip-alternatives.md
│   ├── 04_creator-faq-repurposing-captions.md
│   ├── 05_aeo-geo-glossary-ai-search.md
│   ├── 06_creator-workflow-raw-footage-to-posts.md
│   ├── 07_incubrix-creator-studio-overview.md
│   ├── 08_auto-generate-captions-guide.md
│   ├── 09_llms-txt-ai-search-visibility-guide.md
│   └── 10_social-media-scheduling-vs-native-publishing.md
├── citation-plan/
│   ├── citation_opportunities.md  # 30 Verified third-party citation opportunities
│   └── citations.csv              # Machine-readable citations dataset
├── reports/
│   ├── 2026-W42_report.md         # Weekly visibility executive report
│   └── weekly_report_week42.html  # Interactive, printable executive report
├── launch-kit/
│   ├── 90_day_growth_plan.md      # 13-Week strategic execution roadmap
│   └── growth_plan.csv            # Structured tasks, owners, budgets, target metrics
├── workbook/
│   └── submission_workbook.csv    # Assessment self-check matrix
├── self-check.md                  # Comprehensive evidence & completeness audit
└── README.md                      # This submission overview
```

---

## 🚀 Live Demonstration Quickstart

To run the complete live demonstration of the IncuBrix engine:

```bash
# 1. Start the FastAPI Backend (Port 8001)
python run_backend.py

# 2. In a separate terminal, start the Next.js Frontend (Port 3000)
cd frontend
npm run dev
```

Visit **http://localhost:3000** to interact with all 14 pages.

Or execute the 30-second automated walkthrough script:
```bash
python scripts/demo_walkthrough.py
```

See [DEMO_GUIDE.md](../DEMO_GUIDE.md) for full click-by-click instructions.
