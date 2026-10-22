import csv
import io
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.core.database import get_db
from backend.app.core.config import settings
from backend.app.models.models import (
    Question, SearchObservation, AIObservation, TechnicalAudit,
    TechnicalIssue, ContentPage, ContentRevision, CitationOpportunity,
    GrowthPlanTask, WeeklyReport, MeasurementRun, EvidenceArtifact, JobLog
)
from backend.app.models.schemas import (
    QuestionCreate, QuestionUpdate, QuestionResponse,
    SearchObservationCreate, SearchObservationResponse,
    AIObservationCreate, AIObservationResponse,
    TechnicalAuditResponse, TechnicalIssueResponse, TechnicalIssueUpdate,
    ContentPageCreate, ContentPageUpdate, ContentPageResponse,
    CitationOpportunityCreate, CitationOpportunityUpdate, CitationOpportunityResponse,
    MeasurementRunCreate, MeasurementRunResponse,
    GrowthPlanTaskUpdate, GrowthPlanTaskResponse,
    WeeklyReportResponse, AnalyticsOverviewResponse,
    ProviderSettingsResponse, ReproducibilityAuditResponse
)
from backend.app.services.analytics_service import analytics_service
from backend.app.services.audit_service import audit_service
from backend.app.services.search_provider import SearchProviderAdapter
from backend.app.services.ai_provider import ai_provider_service
from backend.app.services.measurement_runner import measurement_runner
from backend.app.services.report_generator import report_generator
from backend.app.services.content_generator import content_generator
from backend.app.services.reproducibility_service import reproducibility_service

router = APIRouter()

# --- Health Check ---
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "target_website": settings.TARGET_WEBSITE,
        "timestamp": datetime.utcnow().isoformat()
    }

# --- Analytics Overview ---
@router.get("/analytics/overview", response_model=AnalyticsOverviewResponse)
def get_analytics_overview(db: Session = Depends(get_db)):
    return analytics_service.get_overview_metrics(db)

# --- Questions Endpoints ---
@router.get("/questions", response_model=List[QuestionResponse])
def get_questions(
    topic: Optional[str] = None,
    intent: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 150,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    if topic:
        query = query.filter(Question.topic == topic)
    if intent:
        query = query.filter(Question.intent == intent)
    if status:
        query = query.filter(Question.verification_status == status)
    if search:
        query = query.filter(Question.question_text.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@router.post("/questions", response_model=QuestionResponse)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    existing = db.query(Question).filter(Question.question_text == payload.question_text).first()
    if existing:
        raise HTTPException(status_code=400, detail="A question with this exact text already exists.")
    q = Question(**payload.model_dump())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(question_id: str, payload: QuestionUpdate, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(q, k, v)
    q.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(q)
    return q

@router.delete("/questions/{question_id}")
def delete_question(question_id: str, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(q)
    db.commit()
    return {"message": "Question deleted successfully"}

@router.post("/questions/import-csv")
async def import_questions_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    try:
        decoded = contents.decode("utf-8")
    except UnicodeDecodeError:
        decoded = contents.decode("latin-1")
    
    reader = csv.DictReader(io.StringIO(decoded))
    imported = 0
    duplicates = 0
    for row in reader:
        q_text = row.get("question_text") or row.get("question")
        if not q_text:
            continue
        q_text = q_text.strip()
        if db.query(Question).filter(Question.question_text == q_text).first():
            duplicates += 1
            continue
        
        q = Question(
            question_text=q_text,
            topic=row.get("topic", "AI content creation"),
            intent=row.get("intent", "informational"),
            source_url=row.get("source_url"),
            source_type=row.get("source_type", "csv_import"),
            language=row.get("language", "en"),
            market=row.get("market", "US"),
            collection_method="csv_import",
            verification_status="verified",
            evidence_reference=row.get("evidence_reference", "csv_batch_import")
        )
        db.add(q)
        imported += 1
    
    db.commit()
    return {"imported": imported, "duplicates_skipped": duplicates}

# --- Search Visibility Endpoints ---
@router.get("/search-observations", response_model=List[SearchObservationResponse])
def get_search_observations(
    question_id: Optional[str] = None,
    limit: int = 150,
    db: Session = Depends(get_db)
):
    query = db.query(SearchObservation).order_by(SearchObservation.observed_at.desc())
    if question_id:
        query = query.filter(SearchObservation.question_id == question_id)
    return query.limit(limit).all()

@router.post("/search-observations/run-check", response_model=SearchObservationResponse)
def run_search_check(question_id: str, search_provider: str = "mock", db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    adapter = SearchProviderAdapter(provider_name=search_provider)
    result = adapter.search_query(q.question_text, market=q.market, language=q.language)
    
    obs = SearchObservation(
        question_id=q.id,
        search_provider=search_provider,
        query=q.question_text,
        market=q.market,
        language=q.language,
        incubrix_ranking_position=result.get("incubrix_ranking_position"),
        has_featured_snippet=result.get("has_featured_snippet", False),
        has_people_also_ask=result.get("has_people_also_ask", False),
        has_ai_overview=result.get("has_ai_overview", False),
        incubrix_cited_in_ai_overview=result.get("incubrix_cited_in_ai_overview", False),
        result_title=result.get("result_title"),
        result_url=result.get("result_url"),
        result_snippet=result.get("result_snippet"),
        cited_sources=result.get("cited_sources", []),
        competitors_found=result.get("competitors_found", []),
        raw_response=result.get("raw_response", {}),
        collection_status=result.get("collection_status", "success"),
        error_message=result.get("error_message"),
        evidence_reference=f"ad_hoc_search_{datetime.utcnow().timestamp()}"
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs

# --- AI Visibility Endpoints ---
@router.get("/ai-observations", response_model=List[AIObservationResponse])
def get_ai_observations(
    provider: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 150,
    db: Session = Depends(get_db)
):
    query = db.query(AIObservation).order_by(AIObservation.observed_at.desc())
    if provider:
        query = query.filter(AIObservation.provider == provider)
    if status:
        query = query.filter(AIObservation.classification_status == status)
    return query.limit(limit).all()

@router.post("/ai-observations/manual-import", response_model=AIObservationResponse)
def manual_ai_observation_import(payload: AIObservationCreate, db: Session = Depends(get_db)):
    classified = ai_provider_service.classify_response(
        provider=payload.provider,
        model=payload.model,
        prompt=payload.prompt,
        raw_text=payload.raw_answer,
        collection_method="manual_import"
    )
    obs = AIObservation(
        question_id=payload.question_id,
        provider=payload.provider,
        model=payload.model,
        prompt=payload.prompt,
        market=payload.market,
        raw_answer=payload.raw_answer,
        incubrix_mentioned=classified["incubrix_mentioned"],
        incubrix_recommended=classified["incubrix_recommended"],
        incubrix_cited=classified["incubrix_cited"],
        citation_urls=classified["citation_urls"],
        competitors_mentioned=classified["competitors_mentioned"],
        classification_status=classified["classification_status"],
        collection_method="manual_import",
        status="success",
        evidence_reference=payload.evidence_reference or f"manual_import_{datetime.utcnow().timestamp()}"
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs

# --- Technical SEO Audit Endpoints ---
@router.get("/audit/latest", response_model=TechnicalAuditResponse)
def get_latest_audit(db: Session = Depends(get_db)):
    audit = db.query(TechnicalAudit).order_by(TechnicalAudit.started_at.desc()).first()
    if not audit:
        raise HTTPException(status_code=404, detail="No audit found")
    return audit

@router.post("/audit/run", response_model=TechnicalAuditResponse)
def trigger_audit(db: Session = Depends(get_db)):
    return audit_service.run_full_audit(db)

@router.get("/audit/issues", response_model=List[TechnicalIssueResponse])
def get_audit_issues(
    category: Optional[str] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TechnicalIssue)
    if category:
        query = query.filter(TechnicalIssue.category == category)
    if severity:
        query = query.filter(TechnicalIssue.severity == severity)
    if status:
        query = query.filter(TechnicalIssue.validation_status == status)
    return query.all()

@router.patch("/audit/issues/{issue_id}", response_model=TechnicalIssueResponse)
def update_issue_status(issue_id: str, payload: TechnicalIssueUpdate, db: Session = Depends(get_db)):
    issue = db.query(TechnicalIssue).filter(TechnicalIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    issue.validation_status = payload.validation_status
    db.commit()
    db.refresh(issue)
    return issue

# --- Content Studio Endpoints ---
@router.get("/content/pages", response_model=List[ContentPageResponse])
def get_content_pages(db: Session = Depends(get_db)):
    return db.query(ContentPage).order_by(ContentPage.created_at.desc()).all()

@router.get("/content/pages/{page_id}", response_model=ContentPageResponse)
def get_content_page(page_id: str, db: Session = Depends(get_db)):
    page = db.query(ContentPage).filter(ContentPage.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Content page not found")
    return page

@router.post("/content/pages", response_model=ContentPageResponse)
def create_content_page(payload: ContentPageCreate, db: Session = Depends(get_db)):
    existing = db.query(ContentPage).filter(ContentPage.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Page slug already exists")
    cp = ContentPage(**payload.model_dump())
    db.add(cp)
    db.flush()
    rev = ContentRevision(page_id=cp.id, version=1, markdown_content=cp.markdown_content, change_summary="Initial Creation")
    db.add(rev)
    db.commit()
    db.refresh(cp)
    return cp

@router.put("/content/pages/{page_id}", response_model=ContentPageResponse)
def update_content_page(page_id: str, payload: ContentPageUpdate, db: Session = Depends(get_db)):
    cp = db.query(ContentPage).filter(ContentPage.id == page_id).first()
    if not cp:
        raise HTTPException(status_code=404, detail="Content page not found")
    update_data = payload.model_dump(exclude_unset=True)
    content_changed = "markdown_content" in update_data and update_data["markdown_content"] != cp.markdown_content

    for k, v in update_data.items():
        setattr(cp, k, v)

    if content_changed:
        cp.version += 1
        rev = ContentRevision(page_id=cp.id, version=cp.version, markdown_content=cp.markdown_content, change_summary="Editor update")
        db.add(rev)

    cp.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(cp)
    return cp

@router.post("/content/generate-draft")
def generate_draft(topic: str, keyword: str, page_type: str = "how_to"):
    return content_generator.generate_draft(topic, keyword, page_type)

@router.get("/content/pages/{page_id}/export-markdown")
def export_page_markdown(page_id: str, db: Session = Depends(get_db)):
    cp = db.query(ContentPage).filter(ContentPage.id == page_id).first()
    if not cp:
        raise HTTPException(status_code=404, detail="Page not found")
    return PlainTextResponse(content=cp.markdown_content, media_type="text/markdown", headers={"Content-Disposition": f"attachment; filename={cp.slug}.md"})

# --- Citation Opportunities Endpoints ---
@router.get("/citations", response_model=List[CitationOpportunityResponse])
def get_citation_opportunities(
    category: Optional[str] = None,
    outreach_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CitationOpportunity).order_by(CitationOpportunity.priority_score.desc())
    if category:
        query = query.filter(CitationOpportunity.source_category == category)
    if outreach_status:
        query = query.filter(CitationOpportunity.outreach_status == outreach_status)
    return query.all()

@router.patch("/citations/{citation_id}", response_model=CitationOpportunityResponse)
def update_citation_opportunity(citation_id: str, payload: CitationOpportunityUpdate, db: Session = Depends(get_db)):
    co = db.query(CitationOpportunity).filter(CitationOpportunity.id == citation_id).first()
    if not co:
        raise HTTPException(status_code=404, detail="Citation opportunity not found")
    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(co, k, v)
    db.commit()
    db.refresh(co)
    return co

# --- Growth Plan Endpoints ---
@router.get("/growth-plan", response_model=List[GrowthPlanTaskResponse])
def get_growth_plan(db: Session = Depends(get_db)):
    return db.query(GrowthPlanTask).order_by(GrowthPlanTask.week_number.asc()).all()

@router.patch("/growth-plan/{task_id}", response_model=GrowthPlanTaskResponse)
def update_growth_plan_task(task_id: str, payload: GrowthPlanTaskUpdate, db: Session = Depends(get_db)):
    task = db.query(GrowthPlanTask).filter(GrowthPlanTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task

# --- Measurement Runs Endpoints ---
@router.get("/runs", response_model=List[MeasurementRunResponse])
def get_measurement_runs(db: Session = Depends(get_db)):
    return db.query(MeasurementRun).order_by(MeasurementRun.start_time.desc()).all()

@router.post("/runs", response_model=MeasurementRunResponse)
def trigger_measurement_run(payload: MeasurementRunCreate, db: Session = Depends(get_db)):
    return measurement_runner.execute_measurement_run(
        db=db,
        run_name=payload.run_name,
        market=payload.market or "US",
        search_provider=payload.search_provider or "mock",
        ai_providers=payload.ai_providers,
        question_ids=payload.question_ids
    )

# --- Weekly Reports Endpoints ---
@router.get("/reports/weekly", response_model=List[WeeklyReportResponse])
def get_weekly_reports(db: Session = Depends(get_db)):
    return db.query(WeeklyReport).order_by(WeeklyReport.created_at.desc()).all()

@router.get("/reports/weekly/latest", response_model=WeeklyReportResponse)
def get_latest_weekly_report(db: Session = Depends(get_db)):
    rep = db.query(WeeklyReport).order_by(WeeklyReport.created_at.desc()).first()
    if not rep:
        raise HTTPException(status_code=404, detail="No weekly report found")
    return rep

@router.get("/reports/weekly/download-html", response_class=HTMLResponse)
def download_weekly_report_html(db: Session = Depends(get_db)):
    return report_generator.generate_weekly_report_html(db)

# --- Exports Endpoints ---
@router.get("/exports/visibility-csv")
def export_visibility_csv(db: Session = Depends(get_db)):
    csv_content = report_generator.generate_visibility_csv(db)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=visibility.csv"}
    )

@router.get("/exports/submission-workbook-csv")
def export_submission_workbook_csv(db: Session = Depends(get_db)):
    csv_content = report_generator.generate_submission_workbook_csv(db)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=submission_workbook.csv"}
    )

# --- Reproducibility Audit & Evidence ---
@router.get("/reproducibility-audit", response_model=ReproducibilityAuditResponse)
def run_reproducibility_audit(db: Session = Depends(get_db)):
    return reproducibility_service.audit_sampled_records(db, sample_size=20)

@router.get("/evidence-artifacts")
def get_evidence_artifacts(db: Session = Depends(get_db)):
    return db.query(EvidenceArtifact).order_by(EvidenceArtifact.created_at.desc()).all()

# --- Settings Endpoints ---
@router.get("/settings", response_model=ProviderSettingsResponse)
def get_settings():
    return {
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "perplexity_configured": bool(settings.PERPLEXITY_API_KEY),
        "search_api_configured": bool(settings.SEARCH_API_KEY),
        "pagespeed_configured": bool(settings.PAGESPEED_API_KEY),
        "target_website": settings.TARGET_WEBSITE,
        "app_version": settings.APP_VERSION
    }
