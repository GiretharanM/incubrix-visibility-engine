import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.main import app
from backend.app.core.database import SessionLocal
from backend.app.models.models import Question, MeasurementRun, SearchObservation, AIObservation, ContentPage, TechnicalIssue, CitationOpportunity, GrowthPlanTask

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()

def test_measurement_run_normal_and_records(db):
    # Pick 2 existing questions
    questions = db.query(Question).limit(2).all()
    assert len(questions) == 2
    q_ids = [q.id for q in questions]

    payload = {
        "run_name": "Automated Test Run Normal",
        "market": "US",
        "search_provider": "mock",
        "ai_providers": ["openai", "gemini"],
        "question_ids": q_ids
    }
    resp = client.post("/api/runs", json=payload)
    assert resp.status_code == 200
    run_data = resp.json()
    assert run_data["run_name"] == "Automated Test Run Normal"
    assert run_data["status"] in ["completed", "partial"]
    assert run_data["questions_count"] == 2
    assert run_data["successful_measurements"] > 0
    assert run_data["estimated_cost_usd"] > 0

    # Verify search and AI observations were created in DB
    run_id = run_data["id"]
    s_obs = db.query(SearchObservation).filter(SearchObservation.measurement_run_id == run_id).all()
    assert len(s_obs) == 2
    ai_obs = db.query(AIObservation).filter(AIObservation.measurement_run_id == run_id).all()
    assert len(ai_obs) == 4 # 2 questions * 2 providers

def test_provider_failure_resilience_and_recovery(db):
    """
    Test that when an underlying provider fails/raises an error,
    the measurement runner recovers, logs the error, and completes without crashing.
    """
    questions = db.query(Question).limit(1).all()
    q_id = questions[0].id

    # Simulate SearchProviderAdapter raising an exception
    with patch("backend.app.services.search_provider.SearchProviderAdapter.search_query") as mock_search:
        mock_search.side_effect = RuntimeError("Simulated rate limit 429 from Google Serp API")

        payload = {
            "run_name": "Resilience Failure Test Run",
            "market": "US",
            "search_provider": "mock",
            "ai_providers": ["openai"],
            "question_ids": [q_id]
        }
        resp = client.post("/api/runs", json=payload)
        assert resp.status_code == 200
        run_data = resp.json()
        assert run_data["status"] in ["partial", "completed", "failed"]
        assert run_data["failed_measurements"] >= 1
        assert run_data["successful_measurements"] >= 1 # AI query still succeeded!

def test_content_page_lifecycle_and_versioning(db):
    # 1. Create content page
    unique_slug = "how-to-repurpose-webinars-2026-test"
    # Ensure slug doesn't exist
    existing = db.query(ContentPage).filter(ContentPage.slug == unique_slug).first()
    if existing:
        db.delete(existing)
        db.commit()

    create_payload = {
        "slug": unique_slug,
        "title": "How to Repurpose Webinars for Social Media in 2026",
        "topic": "Video editing and repurposing",
        "target_keyword": "repurpose webinars to reels",
        "search_intent": "informational",
        "page_type": "how_to",
        "markdown_content": "# How to Repurpose Webinars\n\nIncuBrix transforms long-form webinars into reels.",
        "direct_answer": "IncuBrix automatically identifies high-engagement moments in webinar recordings and generates vertical clips.",
        "meta_title": "Webinar Repurposing Guide | IncuBrix",
        "meta_description": "Convert hours of webinars into shorts with IncuBrix AI.",
        "canonical_url": f"https://incubrix.com/resources/{unique_slug}",
        "schema_type": "HowTo",
        "status": "draft"
    }
    res_create = client.post("/api/content/pages", json=create_payload)
    assert res_create.status_code == 200
    page_data = res_create.json()
    assert page_data["version"] == 1
    page_id = page_data["id"]

    # 2. Update content -> verify version increments to 2
    update_payload = {
        "markdown_content": "# Updated Webinar Repurposing Guide\n\nUpdated steps with IncuBrix multi-speaker AI tracking.",
        "status": "review"
    }
    res_update = client.put(f"/api/content/pages/{page_id}", json=update_payload)
    assert res_update.status_code == 200
    updated_data = res_update.json()
    assert updated_data["version"] == 2
    assert updated_data["status"] == "review"

    # 3. Export markdown
    res_export = client.get(f"/api/content/pages/{page_id}/export-markdown")
    assert res_export.status_code == 200
    assert "Updated Webinar Repurposing Guide" in res_export.text

    # Clean up
    db.delete(db.query(ContentPage).filter(ContentPage.id == page_id).first())
    db.commit()

def test_citation_opportunity_management(db):
    citations = client.get("/api/citations").json()
    assert len(citations) >= 30
    target_cit = citations[0]
    cit_id = target_cit["id"]

    # Update status to pitch_sent
    res_patch = client.patch(f"/api/citations/{cit_id}", json={"outreach_status": "pitch_sent"})
    assert res_patch.status_code == 200
    assert res_patch.json()["outreach_status"] == "pitch_sent"

    # Revert back
    client.patch(f"/api/citations/{cit_id}", json={"outreach_status": target_cit["outreach_status"]})

def test_growth_plan_management(db):
    tasks = client.get("/api/growth-plan").json()
    assert len(tasks) >= 12
    task = tasks[0]
    task_id = task["id"]

    # Update task status and actual metric
    res_patch = client.patch(f"/api/growth-plan/{task_id}", json={"status": "in_progress", "actual_metric": "50% audit completed"})
    assert res_patch.status_code == 200
    assert res_patch.json()["status"] == "in_progress"
    assert res_patch.json()["actual_metric"] == "50% audit completed"

    # Revert back
    client.patch(f"/api/growth-plan/{task_id}", json={"status": task["status"], "actual_metric": task["actual_metric"]})

def test_weekly_reports_and_html_export():
    res_list = client.get("/api/reports/weekly")
    assert res_list.status_code == 200
    reports = res_list.json()
    assert len(reports) >= 1

    res_latest = client.get("/api/reports/weekly/latest")
    assert res_latest.status_code == 200
    assert res_latest.json()["report_week"] == "2026-W42"

    res_html = client.get("/api/reports/weekly/download-html")
    assert res_html.status_code == 200
    assert "<!DOCTYPE html>" in res_html.text
    assert "IncuBrix" in res_html.text

def test_evidence_artifacts_endpoint():
    res = client.get("/api/evidence-artifacts")
    assert res.status_code == 200
    artifacts = res.json()
    assert len(artifacts) >= 5
    first = artifacts[0]
    assert "artifact_type" in first
    assert "reference_id" in first
    assert "source_url" in first
    assert "raw_content" in first

def test_settings_endpoint():
    res = client.get("/api/settings")
    assert res.status_code == 200
    data = res.json()
    assert "target_website" in data
    assert data["target_website"] == "https://incubrix.com"
