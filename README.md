# IncuBrix AEO, SEO & GEO Visibility Engine

> **Assessment Submission**: Growth Engineer Assessment — Option 3: AEO, SEO & GEO Visibility Engine  
> **Target Website**: [https://incubrix.com](https://incubrix.com)  
> **Status**: Complete, Fully Functional End-to-End Application  
> **🌐 Live Hosted Website (GitHub Pages)**: [https://giretharanm.github.io/incubrix-visibility-engine/](https://giretharanm.github.io/incubrix-visibility-engine/)  
> **📦 Official Submission Workbook**: [`submission/workbook/submission_workbook.xlsx`](submission/workbook/submission_workbook.xlsx)  


---

## 🌟 Executive Overview

The **IncuBrix AEO, SEO & GEO Visibility Engine** is an enterprise-grade full-stack visibility intelligence platform designed specifically for IncuBrix. It enables growth engineers and marketing teams to:

1. **Track Google Search Visibility**: Monitor organic rankings, Featured Snippets, People Also Ask (PAA) questions, and Google AI Overviews across 100+ verified creator queries.
2. **Measure AI Assistant Visibility (AEO/GEO)**: Evaluate brand mentions, explicit recommendations, and URL citations across OpenAI (GPT-4o), Google Gemini, Perplexity, and Claude.
3. **Analyze Competitor Share of Voice**: Quantify relative presence against Opus Clip, Descript, Submagic, Buffer, and Hootsuite.
4. **Conduct Technical SEO Audits**: Automatically crawl `https://incubrix.com` to inspect robots.txt, sitemaps, metadata, Open Graph, mobile indicators, and identify AEO gaps such as missing `llms.txt`.
5. **Execute 20 Prioritized Fixes**: Implement ready-to-paste code and JSON-LD structured data with validation workflows.
6. **Author & Publish Content**: Manage 10 publish-ready draft pages featuring opening direct answers for AEO, valid schemas, and Markdown export.
7. **Discover Citation Opportunities**: Target 30 verified third-party directories, review sites, and publications with customized editorial angles.
8. **Automate Repeatable Measurement**: Execute multi-day runs, compare historical trends, and export `visibility.csv` and weekly reports.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js 15 (TypeScript, React 19), Tailwind CSS, Lucide Icons, Recharts |
| **Backend** | Python FastAPI, Pydantic v2, SQLAlchemy 2.0 |
| **Database** | PostgreSQL (Production / Docker) & SQLite (Zero-config local fallback) |
| **Crawling & Auditing** | HTTPX, BeautifulSoup4, SSRF Security Protection |
| **Testing** | Pytest, FastAPI TestClient |
| **Containerization** | Docker, Docker Compose |

---

## 📁 Repository Structure

```
incubrix-visibility-engine/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI REST endpoints
│   │   ├── core/           # Config, database setup, SSRF security, seeder
│   │   ├── data/           # 105 creator questions, 20 fixes, 10 articles, 30 citations
│   │   ├── models/         # SQLAlchemy models and Pydantic schemas
│   │   └── services/       # Search adapter, AI provider, crawler, analytics, exporter
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # Layout, dark navy sidebar, responsive navigation
│   │   ├── lib/            # Unified API client
│   │   ├── pages/          # 14 complete SaaS pages
│   │   └── styles/         # Global Tailwind CSS
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
├── artifacts/
│   ├── visibility.csv      # 19-column CSV export across 105 questions
│   └── assessment_deliverables.md
├── reports/
│   ├── visibility.csv
│   ├── submission_workbook.csv
│   └── weekly_report_week42.html
├── scripts/
│   ├── run_audit.py        # Standalone live crawl & audit script
│   ├── run_measurements.py # Standalone measurement run script
│   └── export_deliverables.py
├── tests/
│   └── test_engine.py      # Automated Pytest suite (11 test modules)
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart Guide

### Run Live Demonstration in 30 Seconds
```bash
# Ensure backend is running
python run_backend.py

# In a separate terminal:
python scripts/demo_walkthrough.py
```

See [DEMO_GUIDE.md](DEMO_GUIDE.md) for full interactive browser walkthrough steps.

### Option 1: Running with Docker Compose (Production Environment)

1. Clone or open the repository:
   ```bash
   cd c_project2
   ```

2. Create your `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Start all services (PostgreSQL, Redis, FastAPI Backend, Next.js Frontend):
   ```bash
   docker compose up --build
   ```

4. Access the applications:
   - **Frontend UI**: [http://localhost:3000](http://localhost:3000)
   - **Backend API & Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 2: Running Locally (Fast Development Mode)

The backend automatically detects when SQLite is used, requiring zero external service setup.

#### 1. Backend Setup:
```bash
# In the workspace root
pip install -r backend/requirements.txt

# Run the database seeder (initializes 105 questions, 20 fixes, 10 articles, 30 citations)
python -m backend.app.core.init_db

# Run database migrations
python -m alembic upgrade head

# Start the FastAPI server (Port 8001)
python run_backend.py
# Or directly via uvicorn:
# python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001
```

#### 2. Frontend Setup:
```bash
# In a separate terminal
cd frontend
npm install
npm run dev
# Or verify production build:
# npm run build
```

Open [http://localhost:3000](http://localhost:3000) in your browser. API requests are automatically proxied to the backend at `http://127.0.0.1:8001`.

---

## 🧪 Running Automated Tests

Run the complete automated test suite (19 test modules covering question CRUD, duplicate detection, CSV import, search adapters, AI mention classification, metrics, SSRF security, technical audit, content generation, version increments, measurement runs, failure resilience, and exports):

```bash
python -m pytest tests/ -v
```

Expected output:
```
tests/test_engine.py::test_health_check PASSED
tests/test_engine.py::test_question_creation_and_duplicate_prevention PASSED
tests/test_engine.py::test_csv_import PASSED
tests/test_engine.py::test_search_provider_adapter PASSED
tests/test_engine.py::test_ai_provider_classification PASSED
tests/test_engine.py::test_analytics_metrics_calculation PASSED
tests/test_engine.py::test_technical_seo_audit_and_issues PASSED
tests/test_engine.py::test_content_generation_and_schema PASSED
tests/test_engine.py::test_reproducibility_audit PASSED
tests/test_engine.py::test_visibility_csv_and_workbook_exports PASSED
tests/test_engine.py::test_ssrf_security_filter PASSED
tests/test_workflows.py::test_measurement_run_normal_and_records PASSED
tests/test_workflows.py::test_provider_failure_resilience_and_recovery PASSED
tests/test_workflows.py::test_content_page_lifecycle_and_versioning PASSED
tests/test_workflows.py::test_citation_opportunity_management PASSED
tests/test_workflows.py::test_growth_plan_management PASSED
tests/test_workflows.py::test_weekly_reports_and_html_export PASSED
tests/test_workflows.py::test_evidence_artifacts_endpoint PASSED
tests/test_workflows.py::test_settings_endpoint PASSED
======================= 19 passed in ~5.7s =======================
```

---

## 📊 The 14 User Interface Pages

1. **Overview Dashboard (`/`)**: Real-time KPI metric cards, Google ranking distribution chart, multi-day historical trend chart, AI provider breakdown table, and competitor share of voice bars.
2. **Question Research (`/questions`)**: 105 verified creator queries across 11 topics, full-text search, CSV import with duplicate detection, manual question creation modal, and export.
3. **Search Visibility (`/search-visibility`)**: Live SERP tracker recording IncuBrix rankings, Featured Snippets, PAA questions, and Google AI Overviews, with raw JSON inspection and ad-hoc query checks.
4. **AI Visibility (`/ai-visibility`)**: Multi-assistant tracking across OpenAI, Gemini, Perplexity, and Claude with mention/recommendation badges, raw answer reader, and manual answer import modal.
5. **Competitor Analysis (`/competitors`)**: Share of voice comparison and vulnerability matrix analyzing Opus Clip, Descript, Submagic, and Buffer.
6. **Technical SEO Audit (`/audit`)**: Health scores (Overall, Crawlability, Metadata, Structured Data, Mobile) with live re-audit trigger for `https://incubrix.com` and AEO `llms.txt` alert.
7. **SEO Fixes (`/seo-fixes`)**: 20 prioritized technical fixes with ready-to-paste code snippets, copy buttons, and validation status controls (`open`, `in_progress`, `fixed`, `verified`).
8. **Content Studio (`/content-studio`)**: 10 publish-ready draft pages with opening 2-sentence direct answers, live Markdown editor, preview mode, JSON-LD schema preview, and draft generator.
9. **Citation Opportunities (`/citations`)**: 30 verified third-party opportunities (AI directories, G2/Capterra review sites, creator marketing blogs) with priority scores and outreach status tracking.
10. **Weekly Reports (`/reports`)**: Executive summary report with download triggers for printable HTML, `visibility.csv`, and `submission_workbook.csv`.
11. **90-Day Growth Plan (`/growth-plan`)**: 13-week execution roadmap with targets, actuals, budgets, owners, and modal editor.
12. **Evidence Explorer (`/evidence`)**: Verifiable reproducibility audit widget sampling 20 records (scoring 100%, exceeding 85% requirement) and raw artifact inspector.
13. **Measurement History (`/runs`)**: Execution logs, configuration snapshots, runtime durations, cost calculations, and run trigger modal.
14. **Integrations & Settings (`/settings`)**: Secure provider configuration status checks and target website configuration.

---

## 🔒 Security & SSRF Protection

- **Zero Hardcoded Secrets**: All API keys are loaded via environment variables; fallback simulators operate safely when keys are not configured.
- **SSRF Prevention**: The URL crawler strictly validates protocols (`http`/`https`) and blocks private IP spaces (`127.0.0.1`, `10.0.0.0/8`, `192.168.0.0/16`, `169.254.169.254`, and cloud metadata endpoints) while permitting standard NAT64 translation.
- **Input Validation**: All API inputs and CSV uploads are validated using Pydantic v2 schemas and sanitization routines.
