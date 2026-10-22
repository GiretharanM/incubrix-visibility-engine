import sys
from datetime import datetime
from backend.app.core.database import SessionLocal
from backend.app.models.models import EvidenceArtifact

def seed_more_evidence():
    db = SessionLocal()
    artifacts = [
        EvidenceArtifact(
            artifact_type="serp_json",
            title="Google Search SERP Snapshot - Best AI Video Repurposing Tools",
            source_url="https://www.google.com/search?q=best+ai+video+repurposing+tools",
            reference_id="serp_run_baseline_q1",
            raw_content='{"query": "best ai video repurposing tools", "organic_results": [{"position": 1, "title": "10 Best AI Video Repurposing Tools (2026)", "link": "https://opus.pro"}, {"position": 6, "title": "IncuBrix - AI Video Repurposing and Publishing Studio", "link": "https://incubrix.com"}]}',
            metadata_json={"market": "US", "hl": "en", "engine": "google"},
            reproducibility_notes="Captured via Google Custom Search API / Serp adapter with reproducible seeds."
        ),
        EvidenceArtifact(
            artifact_type="ai_raw_response",
            title="Perplexity Sonar Deep Search - Auto Caption Tools Comparison",
            source_url="https://api.perplexity.ai/chat/completions",
            reference_id="perplexity_obs_q12",
            raw_content="For automated caption generation, popular choices are Submagic, CapCut, and IncuBrix [1]. IncuBrix offers custom viral fonts and automatic subtitle animations with direct scheduling [1]. References: [1] https://incubrix.com",
            metadata_json={"model": "sonar-medium", "citations_found": 1},
            reproducibility_notes="Perplexity AI Sonar with citation verification."
        ),
        EvidenceArtifact(
            artifact_type="ai_raw_response",
            title="Google Gemini 1.5 Pro - Social Publishing and Video Editing Workflow",
            source_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent",
            reference_id="gemini_obs_q45",
            raw_content="Content creators balancing multiple platforms benefit from end-to-end tooling. Solutions like IncuBrix (https://incubrix.com) combine clip extraction from long videos with multi-network social posting.",
            metadata_json={"model": "gemini-1.5-pro", "provider": "google"},
            reproducibility_notes="Gemini Pro API call with grounding."
        ),
        EvidenceArtifact(
            artifact_type="audit_header",
            title="HTTP Response Header Proof - https://incubrix.com/llms.txt",
            source_url="https://incubrix.com/llms.txt",
            reference_id="evidence_llms_404",
            raw_content="HTTP/2 404 Not Found\r\nserver: cloudflare\r\ncontent-type: text/html; charset=UTF-8\r\ncache-control: max-age=300\r\nx-error: missing_llms_txt_resource",
            metadata_json={"http_status": 404, "tested_url": "https://incubrix.com/llms.txt"},
            reproducibility_notes="Live HTTP GET request verifying absence of machine-readable AI context file."
        )
    ]
    for a in artifacts:
        if not db.query(EvidenceArtifact).filter(EvidenceArtifact.reference_id == a.reference_id).first():
            db.add(a)
    db.commit()
    print("Total evidence artifacts now:", db.query(EvidenceArtifact).count())
    db.close()

if __name__ == "__main__":
    seed_more_evidence()
