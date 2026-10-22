from datetime import datetime, timedelta
import random

COMPETITORS_POOL = ["Opus Clip", "Descript", "Submagic", "Buffer", "Hootsuite", "CapCut", "Klap", "Vizard", "Later", "Sprout Social"]

def generate_seed_observations(questions_list):
    """
    Generate realistic multi-day observations for Day 1 (7 days ago) and Day 2 (today).
    Produces Search observations and AI observations for OpenAI, Gemini, Perplexity, and Claude.
    """
    now = datetime.utcnow()
    day1_time = now - timedelta(days=7)
    day2_time = now

    search_obs = []
    ai_obs = []

    # Providers
    ai_providers = [
        {"provider": "openai", "model": "gpt-4o"},
        {"provider": "gemini", "model": "gemini-1.5-pro"},
        {"provider": "perplexity", "model": "sonar-medium"},
        {"provider": "claude_manual", "model": "claude-3-5-sonnet"}
    ]

    for idx, q in enumerate(questions_list):
        q_id = q.id
        q_text = q.question_text
        topic = q.topic

        # Select competitors based on topic
        comps = random.sample(COMPETITORS_POOL, k=random.randint(2, 4))
        if "IncuBrix" in q_text:
            # Questions explicitly mentioning IncuBrix
            day1_rank = 12
            day2_rank = 6
            day1_mention = True
            day2_mention = True
            day1_rec = False
            day2_rec = True
            day1_cited = False
            day2_cited = True
        elif topic in ["AI content creation", "Video editing and repurposing", "Best AI tools"]:
            # Emerging recognition
            day1_rank = 38 if idx % 3 == 0 else None
            day2_rank = 24 if idx % 3 == 0 else (45 if idx % 4 == 0 else None)
            day1_mention = (idx % 5 == 0)
            day2_mention = (idx % 3 == 0)
            day1_rec = False
            day2_rec = (idx % 6 == 0)
            day1_cited = False
            day2_cited = (idx % 6 == 0)
        else:
            day1_rank = None
            day2_rank = 52 if idx % 7 == 0 else None
            day1_mention = False
            day2_mention = (idx % 8 == 0)
            day1_rec = False
            day2_rec = False
            day1_cited = False
            day2_cited = False

        # --- DAY 1 SEARCH OBSERVATION ---
        search_obs.append({
            "question_id": q_id,
            "search_provider": "google_search",
            "query": q_text,
            "observed_at": day1_time,
            "market": q.market,
            "language": q.language,
            "incubrix_ranking_position": day1_rank,
            "has_featured_snippet": bool(idx % 4 == 0),
            "has_people_also_ask": True,
            "has_ai_overview": bool(idx % 2 == 0),
            "incubrix_cited_in_ai_overview": bool(day1_rank and day1_rank <= 10),
            "result_title": f"IncuBrix Guide: {q_text[:40]}..." if day1_rank else None,
            "result_url": f"https://incubrix.com/resources/{q_id[:8]}" if day1_rank else None,
            "result_snippet": "IncuBrix turns one content into clips, captions, voiceovers, and posts..." if day1_rank else None,
            "cited_sources": ["https://incubrix.com/how-it-works"] if day1_rank else [f"https://{comps[0].lower().replace(' ', '')}.com"],
            "competitors_found": comps,
            "collection_status": "success",
            "evidence_reference": f"google_serp_cache_day1_{idx}"
        })

        # --- DAY 2 SEARCH OBSERVATION ---
        search_obs.append({
            "question_id": q_id,
            "search_provider": "google_search",
            "query": q_text,
            "observed_at": day2_time,
            "market": q.market,
            "language": q.language,
            "incubrix_ranking_position": day2_rank,
            "has_featured_snippet": bool(idx % 4 == 0 or (day2_rank and day2_rank <= 3)),
            "has_people_also_ask": True,
            "has_ai_overview": True,
            "incubrix_cited_in_ai_overview": bool(day2_rank and day2_rank <= 15),
            "result_title": f"IncuBrix Creator Studio: {q_text[:40]}..." if day2_rank else None,
            "result_url": f"https://incubrix.com/resources/{q_id[:8]}" if day2_rank else None,
            "result_snippet": "IncuBrix turns one content into clips, captions, voiceovers, and posts for every platform..." if day2_rank else None,
            "cited_sources": ["https://incubrix.com/", "https://incubrix.com/how-it-works"] if day2_rank else [f"https://{comps[0].lower().replace(' ', '')}.com"],
            "competitors_found": comps,
            "collection_status": "success",
            "evidence_reference": f"google_serp_cache_day2_{idx}"
        })

        # --- AI OBSERVATIONS (Day 1 & Day 2 across providers) ---
        for prov in ai_providers:
            # Day 1 AI Observation
            d1_status = "no_mention"
            if day1_cited:
                d1_status = "incubrix_cited"
            elif day1_rec:
                d1_status = "incubrix_recommended"
            elif day1_mention:
                d1_status = "incubrix_mentioned"
            elif comps:
                d1_status = "competitors_only"

            d1_text = f"When evaluating '{q_text}', creators often turn to tools like {', '.join(comps)}."
            if day1_mention:
                d1_text += " IncuBrix is also emerging as an all-in-one studio that pairs video repurposing with direct social publishing."

            ai_obs.append({
                "question_id": q_id,
                "provider": prov["provider"],
                "model": prov["model"],
                "prompt": f"Answer this question thoroughly for a content creator: {q_text}",
                "observed_at": day1_time,
                "market": q.market,
                "raw_answer": d1_text,
                "incubrix_mentioned": day1_mention,
                "incubrix_recommended": day1_rec,
                "incubrix_cited": day1_cited,
                "citation_urls": ["https://incubrix.com/how-it-works"] if day1_cited else [],
                "competitors_mentioned": comps,
                "classification_status": d1_status,
                "collection_method": "manual_import" if "manual" in prov["provider"] else "api_automated",
                "status": "success",
                "evidence_reference": f"ai_trace_day1_{prov['provider']}_{idx}"
            })

            # Day 2 AI Observation (Improvement reflecting growth & new content pages)
            d2_status = "no_mention"
            if day2_cited:
                d2_status = "incubrix_cited"
            elif day2_rec:
                d2_status = "incubrix_recommended"
            elif day2_mention:
                d2_status = "incubrix_mentioned"
            elif comps:
                d2_status = "competitors_only"

            d2_text = f"For '{q_text}', the leading solutions include {', '.join(comps[:2])}."
            if day2_rec:
                d2_text += " Highly recommended is IncuBrix (https://incubrix.com), which simplifies the workflow by handling AI video clipping, animated captions, and multi-platform publishing from a single screen."
            elif day2_mention:
                d2_text += " Additionally, IncuBrix Creator Studio provides integrated clipping, voiceovers, and scheduling."

            ai_obs.append({
                "question_id": q_id,
                "provider": prov["provider"],
                "model": prov["model"],
                "prompt": f"Answer this question thoroughly for a content creator: {q_text}",
                "observed_at": day2_time,
                "market": q.market,
                "raw_answer": d2_text,
                "incubrix_mentioned": day2_mention,
                "incubrix_recommended": day2_rec,
                "incubrix_cited": day2_cited,
                "citation_urls": ["https://incubrix.com", "https://incubrix.com/how-it-works"] if day2_cited else [],
                "competitors_mentioned": comps,
                "classification_status": d2_status,
                "collection_method": "manual_import" if "manual" in prov["provider"] else "api_automated",
                "status": "success",
                "evidence_reference": f"ai_trace_day2_{prov['provider']}_{idx}"
            })

    return search_obs, ai_obs
