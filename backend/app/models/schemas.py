from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Questions ---
class QuestionBase(BaseModel):
    question_text: str
    topic: str
    intent: str
    source_url: Optional[str] = None
    source_type: str
    language: Optional[str] = "en"
    market: Optional[str] = "US"
    collection_method: Optional[str] = "manual"
    verification_status: Optional[str] = "verified"
    evidence_reference: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    topic: Optional[str] = None
    intent: Optional[str] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None
    language: Optional[str] = None
    market: Optional[str] = None
    verification_status: Optional[str] = None
    evidence_reference: Optional[str] = None

class QuestionResponse(QuestionBase):
    id: str
    collection_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Search Observations ---
class SearchObservationBase(BaseModel):
    question_id: str
    search_provider: str
    query: str
    market: Optional[str] = "US"
    language: Optional[str] = "en"
    incubrix_ranking_position: Optional[int] = None
    has_featured_snippet: Optional[bool] = False
    has_people_also_ask: Optional[bool] = False
    has_ai_overview: Optional[bool] = False
    incubrix_cited_in_ai_overview: Optional[bool] = False
    result_title: Optional[str] = None
    result_url: Optional[str] = None
    result_snippet: Optional[str] = None
    cited_sources: Optional[List[str]] = []
    competitors_found: Optional[List[str]] = []
    raw_response: Optional[Dict[str, Any]] = {}
    evidence_reference: Optional[str] = None
    collection_status: Optional[str] = "success"
    error_message: Optional[str] = None

class SearchObservationCreate(SearchObservationBase):
    pass

class SearchObservationResponse(SearchObservationBase):
    id: str
    observed_at: datetime
    measurement_run_id: Optional[str] = None

    class Config:
        from_attributes = True

# --- AI Observations ---
class AIObservationBase(BaseModel):
    question_id: str
    provider: str
    model: str
    prompt: str
    market: Optional[str] = "US"
    raw_answer: str
    incubrix_mentioned: Optional[bool] = False
    incubrix_recommended: Optional[bool] = False
    incubrix_cited: Optional[bool] = False
    citation_urls: Optional[List[str]] = []
    competitors_mentioned: Optional[List[str]] = []
    classification_status: Optional[str] = "no_mention"
    evidence_reference: Optional[str] = None
    collection_method: Optional[str] = "api_automated"
    status: Optional[str] = "success"
    error_message: Optional[str] = None

class AIObservationCreate(AIObservationBase):
    pass

class AIObservationResponse(AIObservationBase):
    id: str
    observed_at: datetime
    measurement_run_id: Optional[str] = None

    class Config:
        from_attributes = True

# --- Technical SEO Audits & Issues ---
class TechnicalIssueResponse(BaseModel):
    id: str
    audit_id: str
    affected_url: str
    category: str
    severity: str
    issue_title: str
    observed_problem: str
    evidence: str
    recommended_solution: str
    ready_to_paste_code: Optional[str] = None
    validation_method: str
    validation_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class TechnicalIssueUpdate(BaseModel):
    validation_status: str

class TechnicalAuditResponse(BaseModel):
    id: str
    target_url: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str
    http_status: Optional[int] = None
    is_https: bool
    robots_txt_status: str
    sitemap_status: str
    llms_txt_status: str
    score_overall: int
    score_crawlability: int
    score_metadata: int
    score_structured_data: int
    score_mobile: int
    pages_crawled: int
    summary: Dict[str, Any]
    issues: List[TechnicalIssueResponse] = []

    class Config:
        from_attributes = True

# --- Content Studio ---
class ContentPageBase(BaseModel):
    title: str
    slug: str
    page_type: str
    target_keyword: str
    search_intent: str
    direct_answer: str
    markdown_content: str
    meta_title: str
    meta_description: str
    json_ld_schema: Optional[Dict[str, Any]] = {}
    faqs: Optional[List[Dict[str, str]]] = []
    sources_cited: Optional[List[str]] = []
    internal_links: Optional[List[str]] = []
    call_to_action: Optional[str] = "Try IncuBrix Creator Studio Free"
    review_checklist: Optional[Dict[str, Any]] = {}
    status: Optional[str] = "draft"

class ContentPageCreate(ContentPageBase):
    question_id: Optional[str] = None

class ContentPageUpdate(BaseModel):
    title: Optional[str] = None
    direct_answer: Optional[str] = None
    markdown_content: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    json_ld_schema: Optional[Dict[str, Any]] = None
    faqs: Optional[List[Dict[str, str]]] = None
    status: Optional[str] = None
    review_checklist: Optional[Dict[str, Any]] = None

class ContentPageResponse(ContentPageBase):
    id: str
    question_id: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Citation Opportunities ---
class CitationOpportunityBase(BaseModel):
    page_title: str
    url: str
    domain: str
    source_category: str
    related_target_questions: Optional[List[str]] = []
    evidence_of_relevance: str
    competitors_present: Optional[List[str]] = []
    editorial_angle: str
    incubrix_value_add: str
    suggested_resource_to_create: str
    priority_score: Optional[int] = 80
    verification_status: Optional[str] = "verified"
    outreach_status: Optional[str] = "ready_for_pitch"

class CitationOpportunityCreate(CitationOpportunityBase):
    pass

class CitationOpportunityUpdate(BaseModel):
    outreach_status: Optional[str] = None
    verification_status: Optional[str] = None
    priority_score: Optional[int] = None

class CitationOpportunityResponse(CitationOpportunityBase):
    id: str
    date_discovered: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# --- Measurement Run ---
class MeasurementRunCreate(BaseModel):
    run_name: str
    market: Optional[str] = "US"
    search_provider: Optional[str] = "mock"
    ai_providers: Optional[List[str]] = ["openai", "gemini", "perplexity"]
    question_ids: Optional[List[str]] = None

class MeasurementRunResponse(BaseModel):
    id: str
    run_name: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    market: str
    questions_count: int
    successful_measurements: int
    failed_measurements: int
    skipped_measurements: int
    estimated_cost_usd: float
    configuration_snapshot: Dict[str, Any]
    error_details: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Growth Plan Task ---
class GrowthPlanTaskUpdate(BaseModel):
    status: Optional[str] = None
    actual_metric: Optional[str] = None
    target_metric: Optional[str] = None
    budget_usd: Optional[float] = None
    owner: Optional[str] = None

class GrowthPlanTaskResponse(BaseModel):
    id: str
    week_number: int
    phase_name: str
    priority: str
    task_category: str
    task_title: str
    task_description: str
    owner: str
    tools: str
    dependencies: str
    budget_usd: float
    deliverables: str
    target_metric: str
    actual_metric: str
    risks: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Weekly Reports ---
class WeeklyReportResponse(BaseModel):
    id: str
    title: str
    report_week: str
    period_start: datetime
    period_end: datetime
    questions_measured_count: int
    markets_analyzed: List[str]
    providers_analyzed: List[str]
    google_organic_coverage_pct: float
    google_avg_position: float
    ai_mention_rate_pct: float
    ai_recommendation_rate_pct: float
    ai_citation_rate_pct: float
    executive_summary: str
    technical_health_summary: str
    content_production_status: str
    citation_opportunities_summary: str
    recommended_next_actions: List[str]
    full_report_json: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Analytics Overview ---
class AnalyticsOverviewResponse(BaseModel):
    total_questions: int
    verified_questions: int
    google_ranking_coverage_pct: float
    google_average_position: float
    google_top3_count: int
    google_top10_count: int
    google_top30_count: int
    google_ai_overview_presence_pct: float
    ai_brand_mention_rate_pct: float
    ai_recommendation_rate_pct: float
    ai_citation_rate_pct: float
    measurement_success_rate_pct: float
    evidence_completeness_pct: float
    ranking_distribution: List[Dict[str, Any]]
    historical_trends: List[Dict[str, Any]]
    provider_breakdown: List[Dict[str, Any]]
    competitor_share: List[Dict[str, Any]]
    topic_visibility: List[Dict[str, Any]]
    market_visibility: List[Dict[str, Any]]

# --- Settings ---
class ProviderSettingsResponse(BaseModel):
    openai_configured: bool
    gemini_configured: bool
    perplexity_configured: bool
    search_api_configured: bool
    pagespeed_configured: bool
    target_website: str
    app_version: str

class ReproducibilityAuditResponse(BaseModel):
    sampled_records_count: int
    records_with_complete_evidence: int
    reproducibility_percentage: float
    meets_target: bool
    audit_samples: List[Dict[str, Any]]
