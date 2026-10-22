import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_text = Column(Text, nullable=False, unique=True, index=True)
    topic = Column(String(100), nullable=False, index=True)
    intent = Column(String(50), nullable=False) # informational, commercial, navigational, transactional
    source_url = Column(Text, nullable=True)
    source_type = Column(String(50), nullable=False) # community, keyword_api, search_suggestion, editorial, manual, csv_import
    collection_date = Column(DateTime, default=datetime.utcnow)
    language = Column(String(10), default="en")
    market = Column(String(10), default="US")
    collection_method = Column(String(50), default="automated_scrape") # manual, automated_scrape, api_pull, candidate_ai
    verification_status = Column(String(30), default="verified") # verified, candidate, rejected
    evidence_reference = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    search_observations = relationship("SearchObservation", back_populates="question", cascade="all, delete-orphan")
    ai_observations = relationship("AIObservation", back_populates="question", cascade="all, delete-orphan")
    content_pages = relationship("ContentPage", back_populates="question")


class MeasurementRun(Base):
    __tablename__ = "measurement_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    run_name = Column(String(150), nullable=False)
    status = Column(String(50), default="pending") # pending, running, completed, partial, failed
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    market = Column(String(20), default="US")
    questions_count = Column(Integer, default=0)
    successful_measurements = Column(Integer, default=0)
    failed_measurements = Column(Integer, default=0)
    skipped_measurements = Column(Integer, default=0)
    estimated_cost_usd = Column(Float, default=0.0)
    configuration_snapshot = Column(JSON, default=dict)
    error_details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    search_observations = relationship("SearchObservation", back_populates="measurement_run")
    ai_observations = relationship("AIObservation", back_populates="measurement_run")
    job_logs = relationship("JobLog", back_populates="measurement_run", cascade="all, delete-orphan")


class SearchObservation(Base):
    __tablename__ = "search_observations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False, index=True)
    measurement_run_id = Column(String(36), ForeignKey("measurement_runs.id"), nullable=True, index=True)
    search_provider = Column(String(50), nullable=False) # serpapi, google_cse, mock, manual
    query = Column(Text, nullable=False)
    observed_at = Column(DateTime, default=datetime.utcnow, index=True)
    market = Column(String(20), default="US")
    language = Column(String(10), default="en")
    
    # Visibility metrics
    incubrix_ranking_position = Column(Integer, nullable=True) # None if not in top 100
    has_featured_snippet = Column(Boolean, default=False)
    has_people_also_ask = Column(Boolean, default=False)
    has_ai_overview = Column(Boolean, default=False)
    incubrix_cited_in_ai_overview = Column(Boolean, default=False)
    
    # Content found
    result_title = Column(Text, nullable=True)
    result_url = Column(Text, nullable=True)
    result_snippet = Column(Text, nullable=True)
    
    # Additional data
    cited_sources = Column(JSON, default=list) # List of URLs cited in SERP/AIO
    competitors_found = Column(JSON, default=list) # List of competitor names/domains
    raw_response = Column(JSON, default=dict)
    evidence_reference = Column(Text, nullable=True)
    collection_status = Column(String(30), default="success") # success, failed, rate_limited, unavailable
    error_message = Column(Text, nullable=True)

    # Relationships
    question = relationship("Question", back_populates="search_observations")
    measurement_run = relationship("MeasurementRun", back_populates="search_observations")


class AIObservation(Base):
    __tablename__ = "ai_observations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False, index=True)
    measurement_run_id = Column(String(36), ForeignKey("measurement_runs.id"), nullable=True, index=True)
    provider = Column(String(50), nullable=False) # openai, gemini, perplexity, claude_manual, copilot_manual
    model = Column(String(50), nullable=False) # gpt-4o, gemini-1.5-pro, sonar, claude-3-5-sonnet
    prompt = Column(Text, nullable=False)
    observed_at = Column(DateTime, default=datetime.utcnow, index=True)
    market = Column(String(20), default="US")
    
    # Answers & Classification
    raw_answer = Column(Text, nullable=False)
    incubrix_mentioned = Column(Boolean, default=False)
    incubrix_recommended = Column(Boolean, default=False)
    incubrix_cited = Column(Boolean, default=False)
    citation_urls = Column(JSON, default=list)
    competitors_mentioned = Column(JSON, default=list)
    classification_status = Column(String(50), default="no_mention") 
    # Statuses: incubrix_mentioned, incubrix_recommended, incubrix_cited, competitors_only, no_mention, unavailable
    
    evidence_reference = Column(Text, nullable=True)
    collection_method = Column(String(50), default="api_automated") # api_automated, manual_import
    status = Column(String(30), default="success") # success, failed, unavailable
    error_message = Column(Text, nullable=True)

    # Relationships
    question = relationship("Question", back_populates="ai_observations")
    measurement_run = relationship("MeasurementRun", back_populates="ai_observations")


class TechnicalAudit(Base):
    __tablename__ = "technical_audits"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    target_url = Column(String(255), default="https://incubrix.com")
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(30), default="pending") # pending, running, completed, failed
    http_status = Column(Integer, nullable=True)
    is_https = Column(Boolean, default=True)
    robots_txt_status = Column(String(30), default="valid")
    sitemap_status = Column(String(30), default="valid")
    llms_txt_status = Column(String(30), default="missing")
    score_overall = Column(Integer, default=0)
    score_crawlability = Column(Integer, default=0)
    score_metadata = Column(Integer, default=0)
    score_structured_data = Column(Integer, default=0)
    score_mobile = Column(Integer, default=0)
    pages_crawled = Column(Integer, default=1)
    summary = Column(JSON, default=dict)
    
    # Relationships
    issues = relationship("TechnicalIssue", back_populates="audit", cascade="all, delete-orphan")


class TechnicalIssue(Base):
    __tablename__ = "technical_issues"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    audit_id = Column(String(36), ForeignKey("technical_audits.id"), nullable=False)
    affected_url = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False) # crawlability, metadata, structured_data, content, mobile, performance, security
    severity = Column(String(20), nullable=False) # critical, high, medium, low, info
    issue_title = Column(String(255), nullable=False)
    observed_problem = Column(Text, nullable=False)
    evidence = Column(Text, nullable=False)
    recommended_solution = Column(Text, nullable=False)
    ready_to_paste_code = Column(Text, nullable=True)
    validation_method = Column(String(100), default="automated_retest")
    validation_status = Column(String(30), default="open") # open, fixed, in_progress, verified
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    audit = relationship("TechnicalAudit", back_populates="issues")


class ContentPage(Base):
    __tablename__ = "content_pages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    page_type = Column(String(50), nullable=False) # how_to, comparison, alternatives, faq_hub, glossary, workflow_guide, landing_page
    target_keyword = Column(String(150), nullable=False)
    search_intent = Column(String(50), default="informational")
    direct_answer = Column(Text, nullable=False)
    markdown_content = Column(Text, nullable=False)
    meta_title = Column(String(150), nullable=False)
    meta_description = Column(String(255), nullable=False)
    json_ld_schema = Column(JSON, default=dict)
    faqs = Column(JSON, default=list) # [{question: "", answer: ""}]
    sources_cited = Column(JSON, default=list)
    internal_links = Column(JSON, default=list)
    call_to_action = Column(String(255), default="Try IncuBrix Creator Studio Free")
    review_checklist = Column(JSON, default=dict) # factual_accuracy, tone, schema_valid, etc.
    status = Column(String(30), default="draft") # draft, reviewed, approved, published
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    question = relationship("Question", back_populates="content_pages")
    revisions = relationship("ContentRevision", back_populates="page", cascade="all, delete-orphan")


class ContentRevision(Base):
    __tablename__ = "content_revisions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    page_id = Column(String(36), ForeignKey("content_pages.id"), nullable=False)
    version = Column(Integer, nullable=False)
    markdown_content = Column(Text, nullable=False)
    change_summary = Column(String(255), default="Edit")
    saved_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    page = relationship("ContentPage", back_populates="revisions")


class CitationOpportunity(Base):
    __tablename__ = "citation_opportunities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    page_title = Column(String(255), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    domain = Column(String(150), nullable=False, index=True)
    source_category = Column(String(50), nullable=False) # ai_tool_directory, comparison_article, editorial, review_site, educational, community, creator_marketing
    date_discovered = Column(DateTime, default=datetime.utcnow)
    related_target_questions = Column(JSON, default=list)
    evidence_of_relevance = Column(Text, nullable=False)
    competitors_present = Column(JSON, default=list)
    editorial_angle = Column(Text, nullable=False)
    incubrix_value_add = Column(Text, nullable=False)
    suggested_resource_to_create = Column(Text, nullable=False)
    priority_score = Column(Integer, default=80) # 1 - 100
    verification_status = Column(String(30), default="verified") # verified, pending_review, archived
    outreach_status = Column(String(30), default="ready_for_pitch") # identified, ready_for_pitch, pitched, secured, rejected
    created_at = Column(DateTime, default=datetime.utcnow)


class GrowthPlanTask(Base):
    __tablename__ = "growth_plan_tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    week_number = Column(Integer, nullable=False, index=True) # 1 - 13
    phase_name = Column(String(100), nullable=False) # Foundation, Scaling, Authority
    priority = Column(String(50), nullable=False) # Critical, High, Medium
    task_category = Column(String(50), nullable=False) # technical_seo, content_publishing, measurement, citation
    task_title = Column(String(255), nullable=False)
    task_description = Column(Text, nullable=False)
    owner = Column(String(100), default="Growth Engineer")
    tools = Column(String(150), default="IncuBrix Engine, Search Console, Ahrefs")
    dependencies = Column(String(255), default="None")
    budget_usd = Column(Float, default=0.0)
    deliverables = Column(Text, nullable=False)
    target_metric = Column(String(255), nullable=False)
    actual_metric = Column(String(255), default="Pending measurement")
    risks = Column(Text, default="API limits or delayed indexing")
    status = Column(String(30), default="planned") # planned, in_progress, completed, blocked
    created_at = Column(DateTime, default=datetime.utcnow)


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    report_week = Column(String(50), nullable=False) # e.g. "2026-W42"
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    questions_measured_count = Column(Integer, default=0)
    markets_analyzed = Column(JSON, default=list)
    providers_analyzed = Column(JSON, default=list)
    
    # Key Metric Snapshots
    google_organic_coverage_pct = Column(Float, default=0.0)
    google_avg_position = Column(Float, default=0.0)
    ai_mention_rate_pct = Column(Float, default=0.0)
    ai_recommendation_rate_pct = Column(Float, default=0.0)
    ai_citation_rate_pct = Column(Float, default=0.0)
    
    executive_summary = Column(Text, nullable=False)
    technical_health_summary = Column(Text, nullable=False)
    content_production_status = Column(Text, nullable=False)
    citation_opportunities_summary = Column(Text, nullable=False)
    recommended_next_actions = Column(JSON, default=list)
    full_report_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class EvidenceArtifact(Base):
    __tablename__ = "evidence_artifacts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    artifact_type = Column(String(50), nullable=False) # search_serp, ai_raw_response, audit_html, citation_screenshot
    title = Column(String(255), nullable=False)
    source_url = Column(Text, nullable=True)
    reference_id = Column(String(100), nullable=False, index=True) # question_id, observation_id, audit_id
    raw_content = Column(Text, nullable=True)
    metadata_json = Column(JSON, default=dict)
    reproducibility_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class JobLog(Base):
    __tablename__ = "job_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    measurement_run_id = Column(String(36), ForeignKey("measurement_runs.id"), nullable=True)
    level = Column(String(20), default="INFO") # INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    context_data = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow)

    measurement_run = relationship("MeasurementRun", back_populates="job_logs")
