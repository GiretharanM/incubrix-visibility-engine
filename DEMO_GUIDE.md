# IncuBrix AEO, SEO & GEO Visibility Engine — Live Demo Guide

This document outlines the step-by-step procedure to execute the live demonstration of the IncuBrix engine, verifying all 9 core assessment workflows.

---

## ⚡ Option A: Automated CLI Demonstration (Instant 30-Second Verification)

You can run the fully automated demonstration script that executes all 9 workflows sequentially against the backend API and outputs step-by-step results with colored passing assertions:

```bash
# Ensure the backend is running (Port 8001)
python run_backend.py

# In another terminal, run the automated walkthrough:
python scripts/demo_walkthrough.py
```

### Script Execution Flow:
1. **Health & Connection**: Verifies backend `HTTP 200` on `/api/health`.
2. **Dashboard Overview**: Fetches live metrics (107 questions, 20.2% organic coverage, 14.4% AI mention rate, competitor share).
3. **Traceability**: Loads a verified question and traces it to its SERP observation and stored evidence reference.
4. **Measurement Run**: Executes an ad-hoc run across 2 questions; logs duration and estimated cost.
5. **Question CRUD & Duplicate Block**: Creates a new creator query and validates that submitting the identical query returns `HTTP 400` duplicate rejection.
6. **SEO Fix Inspection**: Inspects the critical `/llms.txt` finding, displays ready-to-paste code, and patches validation status to `in_progress`.
7. **Content Studio Brief**: Generates an AEO-optimized draft with a 2-sentence opening direct answer and valid `HowTo` schema.
8. **Export Verification**: Downloads and verifies the 19-column `visibility.csv`.
9. **Resilient Recovery**: Verifies error handling and cleans up temporary test records.

---

## 🖥️ Option B: Interactive Browser UI Demonstration

Open **http://localhost:3000** in your web browser.

### Step 1: Start Application
- Backend running on `http://127.0.0.1:8001`
- Frontend running on `http://localhost:3000`

### Step 2: Overview Dashboard (`/`)
- View real-time KPI cards: **107 Total Questions**, **20.2% Google Coverage**, **14.4% AI Brand Mention Rate**.
- Inspect the **Google Ranking Distribution** bar chart and **Multi-Day Historical Trends** chart.
- Review the **AI Provider Breakdown** table and **Competitor Share of Voice** progress bars (Opus Clip, Descript, Submagic, Buffer).

### Step 3: Question Research (`/questions`)
- Filter questions by topic (e.g., `Video editing and repurposing`).
- Click on any question to view its details: intent, source URL, market, and evidence reference.
- Trace the question to its historical SERP and AI observations.

### Step 4: Search Visibility (`/search-visibility`)
- Review SERP positions, Featured Snippet indicators, PAA questions, and Google AI Overview presence.
- Click **"Run Live Check"** to execute an ad-hoc search measurement.

### Step 5: AI Visibility (`/ai-visibility`)
- Filter by provider (`OpenAI GPT-4o`, `Google Gemini`, `Perplexity Sonar`, `Anthropic Claude`).
- View classification status tags: `IncuBrix Recommended`, `IncuBrix Cited`, `Competitors Only`.
- Click **"Import Answer"** to manually submit an AI assistant response with automatic mention extraction.

### Step 6: Technical SEO Audit & Fixes (`/audit` and `/seo-fixes`)
- Navigate to `/audit` to inspect the 74/100 health score for `https://incubrix.com`.
- Note the prominent red alert: **Missing /llms.txt File (AEO Gap)**.
- Navigate to `/seo-fixes` to view all 20 prioritized fixes.
- Copy the ready-to-paste markdown code for `/llms.txt` and change the validation status dropdown to `in_progress`.

### Step 7: Content Studio (`/content-studio`)
- Select article `#2: IncuBrix vs Opus Clip: Detailed Comparison for Multi-Platform Creators`.
- Inspect the opening 2-sentence direct answer designed for Google Featured Snippets and AI Overviews.
- Switch between **Edit Mode** and **Preview Mode** to view formatted Markdown and JSON-LD schema.

### Step 8: Citation Opportunities (`/citations`)
- Browse 30 verified third-party opportunities (Futurepedia, G2, Capterra, Social Media Examiner).
- Filter by category (`ai_directory`, `review_platform`, `industry_publication`).
- Update outreach status from `ready_for_pitch` to `pitch_sent`.

### Step 9: Weekly Reports & Exports (`/reports`)
- Review the executive summary for Week 42.
- Click **"Download HTML Report"** to view the printable executive dashboard.
- Click **"Download visibility.csv"** to save the complete 19-column dataset.
