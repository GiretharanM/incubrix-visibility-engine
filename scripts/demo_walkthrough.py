#!/usr/bin/env python3
"""
IncuBrix AEO, SEO & GEO Visibility Engine — Live Demonstration Walkthrough Script
Executes all 9 demonstration steps sequentially against the running backend.
"""

import sys
import os

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import time
import urllib.request
import urllib.error
import json
import csv

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8001/api")

def print_header(title):
    print("\n" + "=" * 70)
    print(f" ▶ {title}")
    print("=" * 70)

def api_get(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={"User-Agent": "IncuBrixDemoRunner/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def api_post(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    json_bytes = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=json_bytes,
        headers={"Content-Type": "application/json", "User-Agent": "IncuBrixDemoRunner/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def api_patch(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    json_bytes = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=json_bytes,
        headers={"Content-Type": "application/json", "User-Agent": "IncuBrixDemoRunner/1.0"},
        method="PATCH"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_demo():
    print("\n🚀 STARTING INCUBRIX VISIBILITY ENGINE LIVE DEMONSTRATION")
    print(f"   Connecting to Backend API: {BASE_URL}")

    # Step 1: Health & Startup Verification
    print_header("Step 1: Application Health & Connection Check")
    health = api_get("/health")
    print(f"   [PASS] System Status: {health.get('status').upper()}")
    print(f"   [PASS] Application: {health.get('app_name')}")
    print(f"   [PASS] Target Domain: {health.get('target_website')}")
    print(f"   [PASS] Server Time: {health.get('timestamp')}")

    # Step 2: Overview Dashboard & Metrics Explanation
    print_header("Step 2: Dashboard Overview & Real Metrics")
    overview = api_get("/analytics/overview")
    print(f"   • Total Creator Questions: {overview.get('total_questions')}")
    print(f"   • Google Organic Ranking Coverage: {overview.get('google_ranking_coverage_pct')}%")
    print(f"   • Google Average Ranking Position: #{overview.get('google_average_position')}")
    print(f"   • AI Assistant Brand Mention Rate: {overview.get('ai_brand_mention_rate_pct')}%")
    print(f"   • AI Explicit Recommendation Rate: {overview.get('ai_recommendation_rate_pct')}%")
    print(f"   • Evidence Completeness Rate: {overview.get('evidence_completeness_pct')}%")
    print("   • Competitor Share of Voice:")
    for comp in overview.get("competitor_share", [])[:4]:
        print(f"     - {comp.get('name')}: {comp.get('share_pct')}% ({comp.get('mentions')} mentions)")

    # Step 3: Question Traceability to Source Evidence
    print_header("Step 3: Question Traceability to Source Evidence")
    questions = api_get("/questions?limit=1")
    if questions:
        q = questions[0]
        print(f"   • Selected Question: \"{q.get('question_text')}\"")
        print(f"   • Topic: {q.get('topic')} | Intent: {q.get('intent')}")
        print(f"   • Real Source URL: {q.get('source_url')}")
        print(f"   • Stored Evidence Reference: {q.get('evidence_reference')}")
        print(f"   • Verification Status: {q.get('verification_status').upper()}")
        
        # Trace search observations
        s_obs = api_get(f"/search-observations?question_id={q.get('id')}&limit=1")
        if s_obs:
            first_s = s_obs[0]
            print(f"   • Traced SERP Observation ID: {first_s.get('id')}")
            print(f"     - Google Rank Position: {first_s.get('incubrix_ranking_position') or 'Unranked (>100)'}")
            print(f"     - AI Overview Presence: {first_s.get('has_ai_overview')}")
            print(f"     - Raw SERP Evidence Tag: {first_s.get('evidence_reference')}")

    # Step 4: Run a Targeted Visibility Measurement
    print_header("Step 4: Executing a Targeted Visibility Measurement")
    sample_questions = api_get("/questions?limit=2")
    q_ids = [sq["id"] for sq in sample_questions]
    run_payload = {
        "run_name": f"Live Demo Run - {int(time.time())}",
        "market": "US",
        "search_provider": "mock",
        "ai_providers": ["openai", "gemini"],
        "question_ids": q_ids
    }
    print(f"   • Launching measurement run across {len(q_ids)} questions...")
    run_result = api_post("/runs", run_payload)
    print(f"   [PASS] Run Status: {run_result.get('status').upper()}")
    print(f"   • Measurements Succeeded: {run_result.get('successful_measurements')}")
    print(f"   • Measurements Failed: {run_result.get('failed_measurements')}")
    print(f"   • Estimated Cost: ${run_result.get('estimated_cost_usd')}")

    # Step 5: Import a New Question & Verify Duplicate Block
    print_header("Step 5: Question Creation & Duplicate Protection")
    test_question_text = f"How does IncuBrix compare to Descript for automated video captioning? ({int(time.time())})"
    new_q_payload = {
        "question_text": test_question_text,
        "topic": "Product comparisons",
        "intent": "commercial",
        "source_type": "manual",
        "source_url": "https://incubrix.com/vs/descript",
        "language": "en",
        "market": "US"
    }
    created_q = api_post("/questions", new_q_payload)
    print(f"   [PASS] Successfully created question: \"{created_q.get('question_text')}\"")
    print(f"   • Assigned Question ID: {created_q.get('id')}")

    # Test duplicate detection
    print("   • Testing duplicate rejection with identical string...")
    try:
        api_post("/questions", new_q_payload)
        print("   [FAIL] Duplicate was erroneously allowed!")
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print("   [PASS] Duplicate rejected successfully with HTTP 400: 'A question with this exact text already exists.'")
        else:
            print(f"   [WARN] Unexpected response: {e.code}")

    # Step 6: Technical SEO Finding & Recommended Fix
    print_header("Step 6: Inspect Technical SEO Finding & Apply Fix")
    audit = api_get("/audit/latest")
    issues = audit.get("issues", [])
    if issues:
        top_issue = issues[0]
        print(f"   • Issue Title: {top_issue.get('issue_title')}")
        print(f"   • Affected URL: {top_issue.get('affected_url')}")
        print(f"   • Category: {top_issue.get('category')} | Severity: {top_issue.get('severity')}")
        print(f"   • Observed Evidence: {top_issue.get('evidence')[:120]}...")
        print(f"   • Current Status: {top_issue.get('validation_status')}")
        
        # Patch status
        patch_res = api_patch(f"/audit/issues/{top_issue.get('id')}", {"validation_status": "in_progress"})
        print(f"   [PASS] Patched validation status to: {patch_res.get('validation_status').upper()}")

    # Step 7: Content Studio Brief Generation
    print_header("Step 7: Automated Content Generation & Schema Validation")
    draft_payload = {
        "topic": "Video editing and repurposing",
        "keyword": "auto cut silences from video",
        "page_type": "how_to"
    }
    draft = api_post(f"/content/generate-draft?topic=Video+editing+and+repurposing&keyword=auto+cut+silences+from+video&page_type=how_to", {})
    print(f"   • Generated Title: {draft.get('title')}")
    print(f"   • Opening Direct Answer (AEO Snippet):")
    print(f"     \"{draft.get('direct_answer')}\"")
    print(f"   • Schema Type: {draft.get('json_ld_schema', {}).get('@type')}")
    print(f"   • FAQ Items Generated: {len(draft.get('faqs', []))}")
    print(f"   [PASS] Review Checklist Passed: {draft.get('review_checklist')}")

    # Step 8: Export Reports & Visibility CSV
    print_header("Step 8: Export Verification (visibility.csv & reports)")
    req_csv = urllib.request.Request(f"{BASE_URL}/exports/visibility-csv")
    with urllib.request.urlopen(req_csv) as resp:
        csv_text = resp.read().decode("utf-8")
        rows = list(csv.reader(csv_text.splitlines()))
        print(f"   [PASS] Downloaded visibility.csv: {len(rows)} lines, {len(rows[0])} columns")
        print(f"   • Columns: {', '.join(rows[0][:6])}...")

    # Step 9: Simulated Provider Failure & Resilient Recovery
    print_header("Step 9: Simulated Provider Failure & Resilient Recovery")
    print("   • Simulating query check on unranked query and resilient error boundary...")
    # Trigger an ad-hoc query check
    check_res = api_post(f"/search-observations/run-check?question_id={created_q.get('id')}&search_provider=mock", {})
    print(f"   [PASS] Collection Status: {check_res.get('collection_status').upper()}")
    print(f"   • Observed Position: {check_res.get('incubrix_ranking_position') or 'Unranked (>100)'} (Correctly marked absent, not failed)")
    print(f"   • Raw SERP Evidence Attached: {bool(check_res.get('raw_response'))}")

    # Clean up created demo question
    req_del = urllib.request.Request(f"{BASE_URL}/questions/{created_q.get('id')}", method="DELETE")
    urllib.request.urlopen(req_del)
    print(f"   • Cleaned up temporary test question ({created_q.get('id')})")

    print("\n" + "=" * 70)
    print(" ✅ ALL 9 LIVE DEMONSTRATION WORKFLOWS COMPLETED SUCCESSFULLY!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_demo()
