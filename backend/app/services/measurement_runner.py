from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.models import Question, MeasurementRun, SearchObservation, AIObservation, JobLog
from backend.app.services.search_provider import SearchProviderAdapter
from backend.app.services.ai_provider import ai_provider_service

class MeasurementRunnerService:
    """
    Executes automated measurement runs across selected questions, search providers,
    and AI providers. Fully resilient: one failed provider never cancels others.
    """

    def execute_measurement_run(
        self,
        db: Session,
        run_name: str,
        market: str = "US",
        search_provider: str = "mock",
        ai_providers: Optional[List[str]] = None,
        question_ids: Optional[List[str]] = None
    ) -> MeasurementRun:
        if ai_providers is None:
            ai_providers = ["openai", "gemini", "perplexity", "claude_manual"]

        # Select target questions
        query = db.query(Question)
        if question_ids:
            query = query.filter(Question.id.in_(question_ids))
        questions = query.all()

        # Initialize Run record
        run = MeasurementRun(
            run_name=run_name,
            status="running",
            start_time=datetime.utcnow(),
            market=market,
            questions_count=len(questions),
            configuration_snapshot={
                "search_provider": search_provider,
                "ai_providers": ai_providers,
                "market": market,
                "target_questions_count": len(questions)
            }
        )
        db.add(run)
        db.commit()
        db.refresh(run)

        search_adapter = SearchProviderAdapter(provider_name=search_provider)
        successful_count = 0
        failed_count = 0
        skipped_count = 0

        # Execute measurements
        for q in questions:
            # 1. Search measurement
            try:
                s_result = search_adapter.search_query(q.question_text, market=market, language=q.language)
                s_obs = SearchObservation(
                    measurement_run_id=run.id,
                    question_id=q.id,
                    search_provider=search_provider,
                    query=q.question_text,
                    market=market,
                    language=q.language,
                    incubrix_ranking_position=s_result.get("incubrix_ranking_position"),
                    has_featured_snippet=s_result.get("has_featured_snippet", False),
                    has_people_also_ask=s_result.get("has_people_also_ask", False),
                    has_ai_overview=s_result.get("has_ai_overview", False),
                    incubrix_cited_in_ai_overview=s_result.get("incubrix_cited_in_ai_overview", False),
                    result_title=s_result.get("result_title"),
                    result_url=s_result.get("result_url"),
                    result_snippet=s_result.get("result_snippet"),
                    cited_sources=s_result.get("cited_sources", []),
                    competitors_found=s_result.get("competitors_found", []),
                    raw_response=s_result.get("raw_response", {}),
                    collection_status=s_result.get("collection_status", "success"),
                    error_message=s_result.get("error_message"),
                    evidence_reference=f"serp_run_{run.id}_{q.id[:6]}"
                )
                db.add(s_obs)
                if s_result.get("collection_status") == "success":
                    successful_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1
                self._log_job(db, run.id, "ERROR", f"Search failed for '{q.question_text}': {str(e)}")

            # 2. AI provider measurements
            for prov in ai_providers:
                try:
                    ai_result = ai_provider_service.query_provider(
                        provider=prov,
                        prompt=f"Answer this question thoroughly for a content creator: {q.question_text}",
                        market=market
                    )
                    ai_obs = AIObservation(
                        measurement_run_id=run.id,
                        question_id=q.id,
                        provider=prov,
                        model=ai_result.get("model", "default"),
                        prompt=ai_result["prompt"],
                        market=market,
                        raw_answer=ai_result["raw_answer"],
                        incubrix_mentioned=ai_result["incubrix_mentioned"],
                        incubrix_recommended=ai_result["incubrix_recommended"],
                        incubrix_cited=ai_result["incubrix_cited"],
                        citation_urls=ai_result.get("citation_urls", []),
                        competitors_mentioned=ai_result.get("competitors_mentioned", []),
                        classification_status=ai_result["classification_status"],
                        collection_method=ai_result["collection_method"],
                        status=ai_result["status"],
                        error_message=ai_result.get("error_message"),
                        evidence_reference=f"ai_run_{run.id}_{prov}_{q.id[:6]}"
                    )
                    db.add(ai_obs)
                    if ai_result["status"] == "success":
                        successful_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    failed_count += 1
                    self._log_job(db, run.id, "ERROR", f"AI Provider '{prov}' failed for '{q.question_text}': {str(e)}")

        # Complete Run record
        run.end_time = datetime.utcnow()
        run.status = "completed" if failed_count == 0 else ("partial" if successful_count > 0 else "failed")
        run.successful_measurements = successful_count
        run.failed_measurements = failed_count
        run.skipped_measurements = skipped_count
        # Approximate cost calculation ($0.015 per OpenAI query, $0.005 per Serp query)
        run.estimated_cost_usd = round((len(questions) * 0.005) + (len(questions) * len(ai_providers) * 0.015), 2)

        db.commit()
        db.refresh(run)
        return run

    def _log_job(self, db: Session, run_id: str, level: str, message: str):
        log = JobLog(measurement_run_id=run_id, level=level, message=message)
        db.add(log)
        db.commit()

measurement_runner = MeasurementRunnerService()
