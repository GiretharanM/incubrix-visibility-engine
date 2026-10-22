from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.models.models import Question, SearchObservation, AIObservation, MeasurementRun

class AnalyticsService:
    """
    Calculates visibility, AEO, and SEO analytics using verified database records.
    Ensures correct denominators by excluding failed measurements from negative rates.
    """

    def get_overview_metrics(self, db: Session) -> Dict[str, Any]:
        total_questions = db.query(Question).count()
        verified_questions = db.query(Question).filter(Question.verification_status == "verified").count()

        # Google Search Observations (latest successful)
        successful_search = db.query(SearchObservation).filter(SearchObservation.collection_status == "success").all()
        total_search_success = len(successful_search)

        ranked_positions = [s.incubrix_ranking_position for s in successful_search if s.incubrix_ranking_position is not None]
        google_ranking_coverage_pct = round((len(ranked_positions) / total_search_success * 100), 1) if total_search_success > 0 else 0.0
        google_average_position = round(sum(ranked_positions) / len(ranked_positions), 1) if ranked_positions else 0.0

        top3_count = sum(1 for p in ranked_positions if p <= 3)
        top10_count = sum(1 for p in ranked_positions if p <= 10)
        top30_count = sum(1 for p in ranked_positions if p <= 30)
        unranked_count = total_search_success - len(ranked_positions)

        ai_overview_count = sum(1 for s in successful_search if s.has_ai_overview)
        google_ai_overview_presence_pct = round((ai_overview_count / total_search_success * 100), 1) if total_search_success > 0 else 0.0

        # AI Assistant Observations (latest successful)
        successful_ai = db.query(AIObservation).filter(AIObservation.status == "success").all()
        total_ai_success = len(successful_ai)

        ai_mentions = sum(1 for a in successful_ai if a.incubrix_mentioned)
        ai_recommendations = sum(1 for a in successful_ai if a.incubrix_recommended)
        ai_citations = sum(1 for a in successful_ai if a.incubrix_cited)

        ai_brand_mention_rate_pct = round((ai_mentions / total_ai_success * 100), 1) if total_ai_success > 0 else 0.0
        ai_recommendation_rate_pct = round((ai_recommendations / total_ai_success * 100), 1) if total_ai_success > 0 else 0.0
        ai_citation_rate_pct = round((ai_citations / total_ai_success * 100), 1) if total_ai_success > 0 else 0.0

        # Total measurements success vs failed
        all_ai = db.query(AIObservation).count()
        all_search = db.query(SearchObservation).count()
        total_measurements = all_ai + all_search
        total_success = total_search_success + total_ai_success
        measurement_success_rate_pct = round((total_success / total_measurements * 100), 1) if total_measurements > 0 else 100.0

        # Evidence completeness (proportion of observations with non-null evidence_reference)
        search_with_evidence = sum(1 for s in successful_search if s.evidence_reference)
        ai_with_evidence = sum(1 for a in successful_ai if a.evidence_reference)
        evidence_completeness_pct = round(((search_with_evidence + ai_with_evidence) / total_success * 100), 1) if total_success > 0 else 100.0

        # Ranking distribution chart data
        ranking_distribution = [
            {"tier": "Positions 1 - 3", "count": top3_count, "fill": "#10b981"},
            {"tier": "Positions 4 - 10", "count": top10_count - top3_count, "fill": "#3b82f6"},
            {"tier": "Positions 11 - 30", "count": top30_count - top10_count, "fill": "#8b5cf6"},
            {"tier": "Positions 31 - 100", "count": len(ranked_positions) - top30_count, "fill": "#f59e0b"},
            {"tier": "Unranked (>100)", "count": unranked_count, "fill": "#6b7280"}
        ]

        # Multi-day historical trends
        historical_trends = self._get_historical_trends(db)

        # Provider Breakdown
        provider_breakdown = self._get_provider_breakdown(db)

        # Competitor Share
        competitor_share = self._get_competitor_share(db)

        # Topic Breakdown
        topic_visibility = self._get_topic_visibility(db)

        # Market Breakdown
        market_visibility = self._get_market_visibility(db)

        return {
            "total_questions": total_questions,
            "verified_questions": verified_questions,
            "google_ranking_coverage_pct": google_ranking_coverage_pct,
            "google_average_position": google_average_position,
            "google_top3_count": top3_count,
            "google_top10_count": top10_count,
            "google_top30_count": top30_count,
            "google_ai_overview_presence_pct": google_ai_overview_presence_pct,
            "ai_brand_mention_rate_pct": ai_brand_mention_rate_pct,
            "ai_recommendation_rate_pct": ai_recommendation_rate_pct,
            "ai_citation_rate_pct": ai_citation_rate_pct,
            "measurement_success_rate_pct": measurement_success_rate_pct,
            "evidence_completeness_pct": evidence_completeness_pct,
            "ranking_distribution": ranking_distribution,
            "historical_trends": historical_trends,
            "provider_breakdown": provider_breakdown,
            "competitor_share": competitor_share,
            "topic_visibility": topic_visibility,
            "market_visibility": market_visibility
        }

    def _get_historical_trends(self, db: Session) -> List[Dict[str, Any]]:
        runs = db.query(MeasurementRun).order_by(MeasurementRun.start_time.asc()).all()
        trends = []
        for r in runs:
            ai_obs = db.query(AIObservation).filter(AIObservation.measurement_run_id == r.id, AIObservation.status == "success").all()
            search_obs = db.query(SearchObservation).filter(SearchObservation.measurement_run_id == r.id, SearchObservation.collection_status == "success").all()

            total_ai = len(ai_obs)
            mentions = sum(1 for a in ai_obs if a.incubrix_mentioned)
            recs = sum(1 for a in ai_obs if a.incubrix_recommended)
            cites = sum(1 for a in ai_obs if a.incubrix_cited)

            ranked = [s.incubrix_ranking_position for s in search_obs if s.incubrix_ranking_position is not None]
            avg_rank = round(sum(ranked) / len(ranked), 1) if ranked else None

            trends.append({
                "run_name": r.run_name,
                "date": r.start_time.strftime("%b %d, %Y"),
                "mention_rate": round((mentions / total_ai * 100), 1) if total_ai else 0.0,
                "recommendation_rate": round((recs / total_ai * 100), 1) if total_ai else 0.0,
                "citation_rate": round((cites / total_ai * 100), 1) if total_ai else 0.0,
                "avg_ranking_position": avg_rank or 50.0
            })
        return trends

    def _get_provider_breakdown(self, db: Session) -> List[Dict[str, Any]]:
        providers = ["openai", "gemini", "perplexity", "claude_manual"]
        breakdown = []
        for p in providers:
            obs = db.query(AIObservation).filter(AIObservation.provider == p, AIObservation.status == "success").all()
            total = len(obs)
            mentions = sum(1 for a in obs if a.incubrix_mentioned)
            recs = sum(1 for a in obs if a.incubrix_recommended)
            cites = sum(1 for a in obs if a.incubrix_cited)

            breakdown.append({
                "provider": p.replace("_", " ").title(),
                "total_queries": total,
                "mention_rate": round((mentions / total * 100), 1) if total else 0.0,
                "recommendation_rate": round((recs / total * 100), 1) if total else 0.0,
                "citation_rate": round((cites / total * 100), 1) if total else 0.0
            })
        return breakdown

    def _get_competitor_share(self, db: Session) -> List[Dict[str, Any]]:
        obs = db.query(AIObservation).filter(AIObservation.status == "success").all()
        comp_counts: Dict[str, int] = {}
        total_mentions = 0
        for o in obs:
            if o.incubrix_mentioned:
                comp_counts["IncuBrix"] = comp_counts.get("IncuBrix", 0) + 1
                total_mentions += 1
            for comp in (o.competitors_mentioned or []):
                comp_counts[comp] = comp_counts.get(comp, 0) + 1
                total_mentions += 1

        results = []
        for name, count in sorted(comp_counts.items(), key=lambda x: x[1], reverse=True)[:8]:
            share = round((count / total_mentions * 100), 1) if total_mentions else 0.0
            results.append({
                "name": name,
                "mentions": count,
                "share_pct": share
            })
        return results

    def _get_topic_visibility(self, db: Session) -> List[Dict[str, Any]]:
        topics = db.query(Question.topic).distinct().all()
        results = []
        for (topic,) in topics:
            q_ids = [q.id for q in db.query(Question.id).filter(Question.topic == topic).all()]
            ai_obs = db.query(AIObservation).filter(AIObservation.question_id.in_(q_ids), AIObservation.status == "success").all()
            search_obs = db.query(SearchObservation).filter(SearchObservation.question_id.in_(q_ids), SearchObservation.collection_status == "success").all()

            ai_total = len(ai_obs)
            ai_mentions = sum(1 for a in ai_obs if a.incubrix_mentioned)
            ranked = [s.incubrix_ranking_position for s in search_obs if s.incubrix_ranking_position is not None]

            results.append({
                "topic": topic,
                "questions_count": len(q_ids),
                "ai_mention_rate": round((ai_mentions / ai_total * 100), 1) if ai_total else 0.0,
                "google_coverage": round((len(ranked) / len(search_obs) * 100), 1) if search_obs else 0.0
            })
        return results

    def _get_market_visibility(self, db: Session) -> List[Dict[str, Any]]:
        markets = db.query(Question.market).distinct().all()
        results = []
        for (market,) in markets:
            q_ids = [q.id for q in db.query(Question.id).filter(Question.market == market).all()]
            ai_obs = db.query(AIObservation).filter(AIObservation.question_id.in_(q_ids), AIObservation.status == "success").all()
            search_obs = db.query(SearchObservation).filter(SearchObservation.question_id.in_(q_ids), SearchObservation.collection_status == "success").all()

            ai_total = len(ai_obs)
            ai_mentions = sum(1 for a in ai_obs if a.incubrix_mentioned)
            ranked = [s.incubrix_ranking_position for s in search_obs if s.incubrix_ranking_position is not None]

            results.append({
                "market": market,
                "questions_count": len(q_ids),
                "ai_mention_rate": round((ai_mentions / ai_total * 100), 1) if ai_total else 0.0,
                "google_coverage": round((len(ranked) / len(search_obs) * 100), 1) if search_obs else 0.0,
                "average_rank": round(sum(ranked)/len(ranked), 1) if ranked else 0.0
            })
        return results

analytics_service = AnalyticsService()
