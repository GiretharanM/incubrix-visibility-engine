from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.models import Question, SearchObservation, AIObservation

class ReproducibilityAuditService:
    """
    Inspects 20 sampled records across Questions, Search observations, and AI observations.
    Calculates the exact reproducibility percentage based on complete evidence metadata,
    source URLs, query traces, and verifiable collection references.
    """

    def audit_sampled_records(self, db: Session, sample_size: int = 20) -> Dict[str, Any]:
        # Sample 10 search observations and 10 AI observations
        search_samples = (
            db.query(SearchObservation)
            .filter(SearchObservation.collection_status == "success")
            .limit(10)
            .all()
        )
        ai_samples = (
            db.query(AIObservation)
            .filter(AIObservation.status == "success")
            .limit(10)
            .all()
        )

        audit_samples = []
        valid_evidence_count = 0

        # Check Search Observations
        for s in search_samples:
            q = db.query(Question).filter(Question.id == s.question_id).first()
            q_text = q.question_text if q else s.query
            has_source = bool(q and q.source_url)
            has_evidence = bool(s.evidence_reference)
            has_raw = bool(s.raw_response)
            is_reproducible = has_source and has_evidence and (s.incubrix_ranking_position is not None or len(s.competitors_found) > 0)

            if is_reproducible:
                valid_evidence_count += 1

            audit_samples.append({
                "record_type": "search_observation",
                "id": s.id,
                "query": q_text,
                "provider": s.search_provider,
                "observed_at": s.observed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "evidence_reference": s.evidence_reference,
                "source_url": q.source_url if q else None,
                "is_reproducible": is_reproducible,
                "evidence_notes": f"Rank: {s.incubrix_ranking_position or 'Unranked'}; Features: Snippet={s.has_featured_snippet}, AIO={s.has_ai_overview}"
            })

        # Check AI Observations
        for a in ai_samples:
            q = db.query(Question).filter(Question.id == a.question_id).first()
            q_text = q.question_text if q else a.prompt
            has_prompt = bool(a.prompt)
            has_raw_answer = bool(a.raw_answer and len(a.raw_answer) > 20)
            has_evidence = bool(a.evidence_reference)
            is_reproducible = has_prompt and has_raw_answer and has_evidence

            if is_reproducible:
                valid_evidence_count += 1

            audit_samples.append({
                "record_type": "ai_observation",
                "id": a.id,
                "query": q_text,
                "provider": f"{a.provider} ({a.model})",
                "observed_at": a.observed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "evidence_reference": a.evidence_reference,
                "source_url": q.source_url if q else None,
                "is_reproducible": is_reproducible,
                "evidence_notes": f"Classification: {a.classification_status}; Mentioned: {a.incubrix_mentioned}; Cited: {a.incubrix_cited}"
            })

        total_sampled = len(audit_samples)
        percentage = round((valid_evidence_count / total_sampled * 100), 1) if total_sampled > 0 else 0.0

        return {
            "sampled_records_count": total_sampled,
            "records_with_complete_evidence": valid_evidence_count,
            "reproducibility_percentage": percentage,
            "meets_target": percentage >= 85.0,
            "audit_samples": audit_samples
        }

reproducibility_service = ReproducibilityAuditService()
