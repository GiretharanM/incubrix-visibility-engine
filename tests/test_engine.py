import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.database import SessionLocal, Base, engine
from backend.app.models.models import Question, SearchObservation, AIObservation
from backend.app.services.search_provider import SearchProviderAdapter
from backend.app.services.ai_provider import ai_provider_service
from backend.app.services.analytics_service import analytics_service
from backend.app.services.content_generator import content_generator
from backend.app.services.reproducibility_service import reproducibility_service
from backend.app.services.report_generator import report_generator
from backend.app.core.security import is_safe_url

client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "IncuBrix" in data["app_name"]

def test_question_creation_and_duplicate_prevention(db_session):
    unique_text = f"Test question for solo creators {pytest.__version__}"
    # 1. Create Question
    res1 = client.post("/api/questions", json={
        "question_text": unique_text,
        "topic": "AI content creation",
        "intent": "informational",
        "source_type": "manual",
        "language": "en",
        "market": "US"
    })
    assert res1.status_code == 200
    q_data = res1.json()
    assert q_data["question_text"] == unique_text

    # 2. Duplicate Detection
    res2 = client.post("/api/questions", json={
        "question_text": unique_text,
        "topic": "AI content creation",
        "intent": "informational",
        "source_type": "manual"
    })
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]

    # Clean up
    client.delete(f"/api/questions/{q_data['id']}")

def test_csv_import(db_session):
    csv_payload = (
        "question_text,topic,intent,source_type,source_url\n"
        "How to batch generate captions with IncuBrix?,AI-generated captions,informational,manual,https://example.com/csv\n"
        "Can AI edit multi-cam video?,Video editing and repurposing,informational,community,https://reddit.com/r/video\n"
    )
    files = {"file": ("test.csv", csv_payload, "text/csv")}
    response = client.post("/api/questions/import-csv", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "imported" in data

def test_search_provider_adapter():
    adapter = SearchProviderAdapter(provider_name="mock")
    # Query with IncuBrix
    res_inc = adapter.search_query("incubrix vs opus clip")
    assert res_inc["collection_status"] == "success"
    assert res_inc["incubrix_ranking_position"] is not None
    assert res_inc["has_ai_overview"] is True
    assert len(res_inc["competitors_found"]) > 0

    # Query without IncuBrix
    res_generic = adapter.search_query("general social media trends 2026")
    assert res_generic["collection_status"] == "success"
    assert res_generic["incubrix_ranking_position"] is None # Correctly unranked, not an error

def test_ai_provider_classification():
    # 1. Direct Recommendation & Citation
    raw_text = (
        "We highly recommend IncuBrix (https://incubrix.com) as the best all-in-one tool for video repurposing. "
        "Other notable competitors include Opus Clip and Descript."
    )
    res = ai_provider_service.classify_response(
        provider="openai",
        model="gpt-4o",
        prompt="What is the best video repurposing tool?",
        raw_text=raw_text
    )
    assert res["incubrix_mentioned"] is True
    assert res["incubrix_recommended"] is True
    assert res["incubrix_cited"] is True
    assert "https://incubrix.com" in res["citation_urls"]
    assert "Opus Clip" in res["competitors_mentioned"]
    assert res["classification_status"] == "incubrix_cited"

    # 2. Competitors only
    comp_only_text = "Creators usually prefer Opus Clip and Submagic for auto captions."
    res2 = ai_provider_service.classify_response(
        provider="perplexity",
        model="sonar-medium",
        prompt="Best captions?",
        raw_text=comp_only_text
    )
    assert res2["incubrix_mentioned"] is False
    assert res2["classification_status"] == "competitors_only"

def test_analytics_metrics_calculation(db_session):
    metrics = analytics_service.get_overview_metrics(db_session)
    assert metrics["total_questions"] >= 100
    assert metrics["verified_questions"] >= 100
    assert 0.0 <= metrics["google_ranking_coverage_pct"] <= 100.0
    assert 0.0 <= metrics["ai_brand_mention_rate_pct"] <= 100.0
    assert 0.0 <= metrics["evidence_completeness_pct"] <= 100.0
    assert len(metrics["ranking_distribution"]) == 5
    assert len(metrics["historical_trends"]) >= 2 # Multi-day observations present
    assert len(metrics["provider_breakdown"]) >= 4

def test_technical_seo_audit_and_issues(db_session):
    resp = client.get("/api/audit/latest")
    assert resp.status_code == 200
    audit = resp.json()
    assert audit["target_url"] == "https://incubrix.com"
    assert audit["score_overall"] > 0
    assert len(audit["issues"]) == 20

    # Test patch status on first issue
    issue_id = audit["issues"][0]["id"]
    patch_res = client.patch(f"/api/audit/issues/{issue_id}", json={"validation_status": "in_progress"})
    assert patch_res.status_code == 200
    assert patch_res.json()["validation_status"] == "in_progress"

def test_content_generation_and_schema():
    draft = content_generator.generate_draft(
        topic="Video editing and repurposing",
        keyword="auto cut silences from video",
        page_type="how_to"
    )
    assert "IncuBrix" in draft["direct_answer"]
    assert len(draft["direct_answer"].split(".")) >= 2 # Opening two sentences
    assert "# " in draft["markdown_content"]
    assert "## " in draft["markdown_content"]
    assert "### " in draft["markdown_content"]
    assert draft["json_ld_schema"]["@type"] == "HowTo"
    assert len(draft["faqs"]) >= 2
    assert draft["review_checklist"]["direct_answer_checked"] is True

def test_reproducibility_audit(db_session):
    audit = reproducibility_service.audit_sampled_records(db_session, sample_size=20)
    assert audit["sampled_records_count"] == 20
    assert audit["reproducibility_percentage"] >= 85.0
    assert audit["meets_target"] is True

def test_visibility_csv_and_workbook_exports(db_session):
    vis_csv = report_generator.generate_visibility_csv(db_session)
    assert "question_id" in vis_csv
    assert "google_ranking_position" in vis_csv
    assert "ai_openai_status" in vis_csv

    wb_csv = report_generator.generate_submission_workbook_csv(db_session)
    assert "Assessment Deliverable" in wb_csv
    assert "VERIFIED" in wb_csv

def test_ssrf_security_filter():
    assert is_safe_url("https://incubrix.com") is True
    assert is_safe_url("http://127.0.0.1:8000") is False
    assert is_safe_url("http://localhost:3000") is False
    assert is_safe_url("http://169.254.169.254/latest/meta-data") is False
    assert is_safe_url("file:///etc/passwd") is False
