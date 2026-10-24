import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from datetime import datetime
from backend.app.core.database import SessionLocal
from backend.app.models.models import (
    Question, SearchObservation, AIObservation, TechnicalAudit, TechnicalIssue,
    ContentPage, CitationOpportunity, GrowthPlanTask, WeeklyReport,
    EvidenceArtifact, MeasurementRun
)
from backend.app.services.analytics_service import analytics_service

def serialize_model(obj):
    if obj is None:
        return None
    d = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        if isinstance(val, datetime):
            d[col.name] = val.isoformat()
        else:
            d[col.name] = val
    return d

def export_static_data():
    out_dir = os.path.join("frontend", "public", "data")
    os.makedirs(out_dir, exist_ok=True)
    db = SessionLocal()
    try:
        print("Exporting overview metrics...")
        overview = analytics_service.get_overview_metrics(db)
        with open(os.path.join(out_dir, "overview.json"), "w", encoding="utf-8") as f:
            json.dump(overview, f, indent=2)

        print("Exporting questions...")
        questions = [serialize_model(q) for q in db.query(Question).all()]
        with open(os.path.join(out_dir, "questions.json"), "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2)

        print("Exporting search observations...")
        search_obs = [serialize_model(s) for s in db.query(SearchObservation).order_by(SearchObservation.observed_at.desc()).limit(150).all()]
        with open(os.path.join(out_dir, "search_observations.json"), "w", encoding="utf-8") as f:
            json.dump(search_obs, f, indent=2)

        print("Exporting AI observations...")
        ai_obs = [serialize_model(a) for a in db.query(AIObservation).order_by(AIObservation.observed_at.desc()).limit(150).all()]
        with open(os.path.join(out_dir, "ai_observations.json"), "w", encoding="utf-8") as f:
            json.dump(ai_obs, f, indent=2)

        print("Exporting audit & issues...")
        audit = db.query(TechnicalAudit).order_by(TechnicalAudit.started_at.desc()).first()
        audit_data = serialize_model(audit) if audit else {}
        issues = [serialize_model(i) for i in db.query(TechnicalIssue).all()]
        if audit_data:
            audit_data["issues"] = issues
        with open(os.path.join(out_dir, "audit.json"), "w", encoding="utf-8") as f:
            json.dump(audit_data, f, indent=2)
        with open(os.path.join(out_dir, "issues.json"), "w", encoding="utf-8") as f:
            json.dump(issues, f, indent=2)

        print("Exporting content pages...")
        content_pages = [serialize_model(c) for c in db.query(ContentPage).all()]
        with open(os.path.join(out_dir, "content_pages.json"), "w", encoding="utf-8") as f:
            json.dump(content_pages, f, indent=2)

        print("Exporting citation opportunities...")
        citations = [serialize_model(c) for c in db.query(CitationOpportunity).order_by(CitationOpportunity.priority_score.desc()).all()]
        with open(os.path.join(out_dir, "citations.json"), "w", encoding="utf-8") as f:
            json.dump(citations, f, indent=2)

        print("Exporting growth plan tasks...")
        growth_plan = [serialize_model(g) for g in db.query(GrowthPlanTask).order_by(GrowthPlanTask.week_number.asc()).all()]
        with open(os.path.join(out_dir, "growth_plan.json"), "w", encoding="utf-8") as f:
            json.dump(growth_plan, f, indent=2)

        print("Exporting reports...")
        reports = [serialize_model(r) for r in db.query(WeeklyReport).order_by(WeeklyReport.created_at.desc()).all()]
        with open(os.path.join(out_dir, "reports.json"), "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=2)

        print("Exporting measurement runs...")
        runs = [serialize_model(r) for r in db.query(MeasurementRun).order_by(MeasurementRun.start_time.desc()).all()]
        with open(os.path.join(out_dir, "runs.json"), "w", encoding="utf-8") as f:
            json.dump(runs, f, indent=2)

        print("Exporting evidence artifacts...")
        evidence = [serialize_model(e) for e in db.query(EvidenceArtifact).all()]
        with open(os.path.join(out_dir, "evidence_artifacts.json"), "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

        print("Exporting settings...")
        settings_data = {
            "openai_configured": True,
            "gemini_configured": True,
            "perplexity_configured": True,
            "search_api_configured": True,
            "pagespeed_configured": True,
            "target_website": "https://incubrix.com",
            "app_version": "1.0.0 (GitHub Pages Live Static Edition)"
        }
        with open(os.path.join(out_dir, "settings.json"), "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=2)

        print("Static JSON data export complete in frontend/public/data/!")
    finally:
        db.close()

if __name__ == "__main__":
    export_static_data()
