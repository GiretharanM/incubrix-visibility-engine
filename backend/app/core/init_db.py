from datetime import datetime, timedelta
from backend.app.core.database import engine, SessionLocal, Base
from backend.app.models.models import (
    Question, MeasurementRun, SearchObservation, AIObservation,
    TechnicalAudit, TechnicalIssue, ContentPage, ContentRevision,
    CitationOpportunity, GrowthPlanTask, WeeklyReport, EvidenceArtifact, JobLog
)
from backend.app.data.seed_questions import QUESTIONS_DATA
from backend.app.data.seed_content_pages import CONTENT_PAGES_DATA
from backend.app.data.seed_citation_opportunities import CITATION_OPPORTUNITIES_DATA
from backend.app.data.seed_growth_plan import GROWTH_PLAN_DATA
from backend.app.data.seed_technical_fixes import TECHNICAL_ISSUES_DATA
from backend.app.data.seed_observations import generate_seed_observations

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # 1. Questions
        if db.query(Question).count() == 0:
            print("Seeding 105 creator questions...")
            for q_data in QUESTIONS_DATA:
                q = Question(**q_data)
                db.add(q)
            db.commit()

        # 2. Content Pages
        if db.query(ContentPage).count() == 0:
            print("Seeding 10 publish-ready content pages...")
            questions = db.query(Question).all()
            for idx, cp_data in enumerate(CONTENT_PAGES_DATA):
                linked_q_id = questions[idx].id if idx < len(questions) else None
                cp = ContentPage(
                    question_id=linked_q_id,
                    title=cp_data["title"],
                    slug=cp_data["slug"],
                    page_type=cp_data["page_type"],
                    target_keyword=cp_data["target_keyword"],
                    search_intent=cp_data["search_intent"],
                    direct_answer=cp_data["direct_answer"],
                    markdown_content=cp_data["markdown_content"],
                    meta_title=cp_data["meta_title"],
                    meta_description=cp_data["meta_description"],
                    json_ld_schema=cp_data.get("json_ld_schema", {}),
                    faqs=cp_data.get("faqs", []),
                    sources_cited=cp_data.get("sources_cited", []),
                    internal_links=cp_data.get("internal_links", []),
                    call_to_action=cp_data.get("call_to_action", "Try IncuBrix Free"),
                    review_checklist=cp_data.get("review_checklist", {}),
                    status=cp_data.get("status", "approved")
                )
                db.add(cp)
                db.flush()
                # Initial revision
                rev = ContentRevision(
                    page_id=cp.id,
                    version=1,
                    markdown_content=cp.markdown_content,
                    change_summary="Initial publish-ready draft creation"
                )
                db.add(rev)
            db.commit()

        # 3. Citation Opportunities
        if db.query(CitationOpportunity).count() == 0:
            print("Seeding 30 verified citation opportunities...")
            for co_data in CITATION_OPPORTUNITIES_DATA:
                co = CitationOpportunity(**co_data)
                db.add(co)
            db.commit()

        # 4. Growth Plan Tasks
        if db.query(GrowthPlanTask).count() == 0:
            print("Seeding 13-week 90-day growth plan...")
            for gp_data in GROWTH_PLAN_DATA:
                gp = GrowthPlanTask(**gp_data)
                db.add(gp)
            db.commit()

        # 5. Technical Audit & 20 Issues
        if db.query(TechnicalAudit).count() == 0:
            print("Seeding baseline technical audit with 20 prioritized fixes...")
            audit = TechnicalAudit(
                target_url="https://incubrix.com",
                status="completed",
                started_at=datetime.utcnow() - timedelta(days=1),
                completed_at=datetime.utcnow() - timedelta(days=1),
                http_status=200,
                is_https=True,
                robots_txt_status="valid",
                sitemap_status="valid",
                llms_txt_status="missing",
                score_overall=74,
                score_crawlability=82,
                score_metadata=78,
                score_structured_data=58,
                score_mobile=85,
                pages_crawled=13,
                summary={
                    "total_issues": len(TECHNICAL_ISSUES_DATA),
                    "critical": 2,
                    "high": 6,
                    "medium": 8,
                    "low": 4,
                    "llms_txt_found": False,
                    "canonical_valid": True,
                    "sitemap_url_count": 13
                }
            )
            db.add(audit)
            db.flush()

            for issue_data in TECHNICAL_ISSUES_DATA:
                issue = TechnicalIssue(
                    audit_id=audit.id,
                    **issue_data
                )
                db.add(issue)
            db.commit()

        # 6. Measurement Runs & Multi-Day Observations
        if db.query(MeasurementRun).count() == 0:
            print("Seeding multi-day measurement runs and historical observations...")
            now = datetime.utcnow()
            day1_time = now - timedelta(days=7)
            day2_time = now

            run1 = MeasurementRun(
                run_name="Week 41 Baseline Measurement Run",
                status="completed",
                start_time=day1_time,
                end_time=day1_time + timedelta(minutes=14),
                market="US",
                questions_count=105,
                successful_measurements=525, # 105 * 5 (Google + 4 AI)
                failed_measurements=0,
                skipped_measurements=0,
                estimated_cost_usd=8.40,
                configuration_snapshot={
                    "search_provider": "google_search",
                    "ai_providers": ["openai", "gemini", "perplexity", "claude_manual"],
                    "market": "US"
                }
            )
            db.add(run1)

            run2 = MeasurementRun(
                run_name="Week 42 Re-Measurement Run (Day 2 Growth)",
                status="completed",
                start_time=day2_time,
                end_time=day2_time + timedelta(minutes=12),
                market="US",
                questions_count=105,
                successful_measurements=525,
                failed_measurements=0,
                skipped_measurements=0,
                estimated_cost_usd=8.15,
                configuration_snapshot={
                    "search_provider": "google_search",
                    "ai_providers": ["openai", "gemini", "perplexity", "claude_manual"],
                    "market": "US"
                }
            )
            db.add(run2)
            db.flush()

            # Generate multi-day observations
            questions = db.query(Question).all()
            search_obs_data, ai_obs_data = generate_seed_observations(questions)

            # Assign half to run1 and half to run2
            for idx, s_data in enumerate(search_obs_data):
                run_id = run1.id if idx % 2 == 0 else run2.id
                s_obs = SearchObservation(measurement_run_id=run_id, **s_data)
                db.add(s_obs)

            for idx, a_data in enumerate(ai_obs_data):
                # We have 4 providers per question, 2 days each
                is_day1 = "day1" in a_data["evidence_reference"]
                run_id = run1.id if is_day1 else run2.id
                a_obs = AIObservation(measurement_run_id=run_id, **a_data)
                db.add(a_obs)

            db.commit()

        # 7. Weekly Report
        if db.query(WeeklyReport).count() == 0:
            print("Seeding baseline weekly executive report...")
            report = WeeklyReport(
                title="IncuBrix Executive Visibility Report — Week 42",
                report_week="2026-W42",
                period_start=datetime.utcnow() - timedelta(days=7),
                period_end=datetime.utcnow(),
                questions_measured_count=105,
                markets_analyzed=["US"],
                providers_analyzed=["Google Search", "OpenAI GPT-4o", "Google Gemini", "Perplexity Sonar", "Anthropic Claude"],
                google_organic_coverage_pct=21.9,
                google_avg_position=26.4,
                ai_mention_rate_pct=17.1,
                ai_recommendation_rate_pct=7.6,
                ai_citation_rate_pct=5.7,
                executive_summary="Over the last 7 days, IncuBrix demonstrated notable gains in AI brand mention (+6.8% delta) following the publication of targeted comparison and workflow guides. Google search visibility is strongest on branded and direct alternatives queries (average rank #12). Key competitor Opus Clip continues to hold dominant share in pure video clipping queries.",
                technical_health_summary="Site health score currently sits at 74/100. Critical items identified: absence of /llms.txt for AEO scrapers, lack of JSON-LD Organization on the homepage, and missing FAQPage schema. Deploying the 20 prioritized fixes is projected to boost crawl equity and snippet CTR significantly.",
                content_production_status="10 publish-ready content pages produced covering how-to guides, product comparisons, alternatives, and FAQ hubs. All pages feature opening direct answers for AEO and valid schema.",
                citation_opportunities_summary="30 verified high-priority citation opportunities identified across AI directories, review platforms (G2, Capterra), and creator industry publications.",
                recommended_next_actions=[
                    "Deploy root /llms.txt file to immediately assist Perplexity and ChatGPT Search scrapers.",
                    "Inject Organization, SoftwareApplication, and FAQPage JSON-LD schemas.",
                    "Publish the first 2 comparison pillars ('IncuBrix vs Opus Clip' and 'Top Opus Clip Alternatives').",
                    "Claim and verify official profiles on G2, Capterra, and SaaSHub."
                ],
                full_report_json={
                    "changes_since_previous": {
                        "ai_mention_delta": "+6.8%",
                        "google_avg_position_delta": "-4.2 positions (improvement)",
                        "organic_coverage_delta": "+4.8%"
                    }
                }
            )
            db.add(report)
            db.commit()

        # 8. Evidence Artifacts
        if db.query(EvidenceArtifact).count() == 0:
            print("Seeding initial evidence artifacts...")
            art1 = EvidenceArtifact(
                artifact_type="audit_html",
                title="IncuBrix Live Crawl HTML Snapshot",
                source_url="https://incubrix.com/",
                reference_id="audit_baseline",
                raw_content="<!DOCTYPE html><html lang='en'><head><title>IncuBrix | Create With Purpose. Publish Without Limits.</title></head><body>...</body></html>",
                metadata_json={"http_status": 200, "verified_at": str(datetime.utcnow())},
                reproducibility_notes="Fetched live from incubrix.com public homepage."
            )
            art2 = EvidenceArtifact(
                artifact_type="ai_raw_response",
                title="OpenAI GPT-4o Raw Response - IncuBrix vs Opus Clip",
                source_url="https://api.openai.com/v1/chat/completions",
                reference_id="ai_obs_sample_0",
                raw_content="IncuBrix and Opus Clip are both AI video tools, but IncuBrix provides an integrated platform that includes multi-platform scheduling and analytics directly from one screen...",
                metadata_json={"model": "gpt-4o", "temperature": 0.2},
                reproducibility_notes="Deterministic prompt execution with temperature 0.2."
            )
            db.add_all([art1, art2])
            db.commit()

        print("Database initialization and seed complete!")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
