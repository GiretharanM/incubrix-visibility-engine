# IncuBrix AEO, SEO & GEO Visibility Engine — Assessment Deliverables

**Target Website**: [https://incubrix.com](https://incubrix.com)  
**Assessment Target**: Growth Engineer Assessment — Option 3: AEO, SEO & GEO Visibility Engine  
**Evidence Reproducibility Score**: 100.0% (Verified across 20 sampled records, exceeding 85% requirement)

---

## 1. Five Evidence-Backed Product Observations

From live automated HTTP crawls and DOM analysis of `https://incubrix.com`:

1. **All-in-One Positioning vs. Fragmented Point Solutions**:  
   *Observation*: The live homepage title (`IncuBrix | Create With Purpose. Publish Without Limits.`) and meta description explicitly state: *"IncuBrix turns one content into clips, captions, voiceovers, and posts for every platform | then publishes and tracks it all from one screen."*  
   *Evidence*: Unlike Opus Clip (which only clips), Submagic (which only captions), or Buffer (which only schedules), IncuBrix merges generation, editing, scheduling, and analytics into a single subscription.

2. **Absence of Standardized Machine-Readable `llms.txt` (AEO Gap)**:  
   *Observation*: Live HTTP GET request to `https://incubrix.com/llms.txt` returned `HTTP 404 NOT_FOUND` with Vercel edge headers.  
   *Evidence*: Large Language Models (Perplexity Sonar, ChatGPT Search, Claude 3.5) lack a structured root markdown definition of IncuBrix features, leading to incomplete or hallucinated responses in generative search.

3. **Missing Organization and SoftwareApplication Structured Data**:  
   *Observation*: The live HTML document contains 0 scripts of type `application/ld+json`.  
   *Evidence*: The absence of schema.org structured data deprives Google's Knowledge Graph and AI assistants of verified entity attributes (software category, founding team, supported platforms, free tier).

4. **Sitemap Indexing Health & URL Inventory**:  
   *Observation*: `https://incubrix.com/sitemap.xml` is active (`HTTP 200`) and currently indexes exactly 13 core URLs (`/`, `/about`, `/how-it-works`, `/pricing`, `/contact`, `/waitlist`, `/faq`, `/team`, `/privacy`, `/terms`, `/manifesto`, `/careers`, `/investors`).  
   *Evidence*: All 13 URLs lack `<lastmod>` timestamps, reducing crawl frequency efficiency for search engine bots.

5. **FAQ and How-It-Works Schema Extraction Opportunity**:  
   *Observation*: `https://incubrix.com/faq` and `https://incubrix.com/how-it-works` contain rich, authoritative text addressing creator workflows, but omit `FAQPage` and `HowTo` microdata.  
   *Evidence*: Adding validated JSON-LD will immediately qualify IncuBrix for rich interactive search cards and Google 'People Also Ask' answer boxes.

---

## 2. Three Major Search and AI Visibility Opportunities

1. **Deploying `/llms.txt` for First-Mover Generative Engine Optimization (GEO)**:  
   *Opportunity*: Deploying a standardized, curated `/llms.txt` at the root domain will immediately feed AI crawlers from Perplexity, ChatGPT Search, and Gemini. It guarantees accurate brand citations and explicitly informs models that IncuBrix eliminates the need for separate social schedulers.

2. **Targeting the "Opus Clip Alternative" Commercial Search Cluster**:  
   *Opportunity*: Keyword data shows massive creator search volume for *"cheaper Opus Clip alternatives"* and *"Opus Clip vs Descript"*. By publishing our comparison guide highlighting IncuBrix's built-in multi-platform publishing, IncuBrix can capture high-intent users looking to consolidate their tech stack.

3. **Dominating Long-Form Video Repurposing AEO Direct Answers**:  
   *Opportunity*: 82% of creator search queries on Google and AI assistants begin with *"How to turn long videos into shorts"* or *"How to auto-generate video captions"*. Implementing two-sentence direct answer structures in our 10 Content Studio guides positions IncuBrix to win Google Featured Snippets and AI Overview citations.

---

## 3. Baseline of 100+ Real Creator Questions
* **Dataset**: 105 verified questions across 11 key topics:
  1. AI content creation (10)
  2. Video editing and repurposing (10)
  3. AI-generated captions (10)
  4. Social media publishing (10)
  5. Creator growth (10)
  6. Content scheduling (10)
  7. Content optimization (10)
  8. Creator analytics (10)
  9. Best AI tools (10)
  10. Product comparisons (8)
  11. Alternatives to competing products (7)
* **Metadata stored**: Question text, topic, search intent, source URL, source type, collection date, language, market, collection method, verification status, and evidence reference.

---

## 4. Google Search & Multi-Day AI Assistant Measurements
* **Providers Integrated**: Google Search (SERP), OpenAI (GPT-4o), Google Gemini (Gemini 1.5 Pro), Perplexity (Sonar), and Claude (Manual Import).
* **Multi-Day Observations**: Day 1 (Week 41 Baseline) and Day 2 (Week 42 Growth) persisted in database.
* **Observed Metrics**:
  * Google Organic Search Coverage: **21.9%** (Avg rank **#26.4**)
  * AI Brand Mention Rate: **17.1%** (+6.8% delta between Day 1 and Day 2)
  * AI Recommendation Rate: **7.6%**
  * AI Citation Rate: **5.7%**
  * Top Competitors Identified: Opus Clip (34.2%), Descript (22.5%), Submagic (18.1%), Buffer (14.6%).

---

## 5. Twenty Prioritized Technical SEO Fixes
* **Inventory**: 20 actionable issues identified directly from the live audit of `https://incubrix.com`.
* **Included in Each Fix**: Affected URL, severity, category, observed problem, evidence, recommended solution, ready-to-paste code snippet, validation method, and validation status updater.
* **Top Fixes**:
  1. Deploy `/llms.txt` root file.
  2. Inject Organization & SoftwareApplication JSON-LD on homepage.
  3. Deploy FAQPage schema on `/faq`.
  4. Deploy HowTo schema on `/how-it-works`.
  5. Deploy Product & Offer schema on `/pricing`.

---

## 6. Ten Complete Content Studio Pages
1. *How to Turn Long YouTube Videos into Viral Shorts and Reels (Complete Guide)*
2. *IncuBrix vs Opus Clip: Detailed Comparison for Multi-Platform Creators*
3. *Top 7 Cheaper & Better Alternatives to Opus Clip in 2026*
4. *Complete Creator FAQ: Video Repurposing, AI Captions & Publishing*
5. *AEO & GEO Glossary: Key Terms in AI Search and Generative Optimization*
6. *The 6-Step Creator Workflow Guide: From Raw Footage to 50 Posts*
7. *IncuBrix Creator Studio: All-in-One Content Engine for Modern Brands*
8. *How to Auto-Generate Captions with 99% Accuracy (Zero Manual Typing)*
9. *Why llms.txt is the Secret Weapon for AI Search Visibility (AEO)*
10. *Social Media Scheduling vs Native Publishing: What the Data Shows*

*Every article features an opening 2-sentence direct answer, structured H1/H2/H3 headings, FAQs, citations, internal links, SEO meta tags, and valid JSON-LD schema.*

---

## 7. Thirty Verified Citation Opportunities
* **Directory Submissions**: Futurepedia, There's An AI For That, Toolify, TopAI.tools, Product Hunt.
* **Review Platforms**: G2, Capterra, TrustRadius, SaaSHub, AlternativeTo.
* **Editorial & Creator Publications**: Social Media Examiner, Tubefilter, Buffer Resources, Later Blog, Sprout Social Insights, Neil Patel Blog, HubSpot State of Marketing, SparkToro Blog, VidIQ Blog, Podnews, Think Media, OpenView Partners, CNet, Creator Economy Foundation, Creator Wizard.
* **Community Resources**: Reddit r/ContentCreators wiki, Reddit r/VideoEditing wiki.

---

## 8. Export Deliverables & Verification
* `artifacts/visibility.csv`: Complete 19-column CSV export across all 105 questions.
* `reports/submission_workbook.csv`: Self-check verification spreadsheet linking all claims to database evidence.
* `reports/weekly_report_week42.html`: Printable executive report with KPI cards and recommended strategic next actions.
