import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.core.database import SessionLocal
from backend.app.services.audit_service import audit_service

def main():
    print("Initiating Live Technical SEO & AEO Audit for https://incubrix.com...")
    db = SessionLocal()
    try:
        audit = audit_service.run_full_audit(db)
        print("Audit Completed Successfully!")
        print(f"Overall Health Score: {audit.score_overall}/100")
        print(f"Crawlability Score:  {audit.score_crawlability}%")
        print(f"Metadata Score:      {audit.score_metadata}%")
        print(f"Structured Data:     {audit.score_structured_data}%")
        print(f"Mobile Score:        {audit.score_mobile}%")
        print(f"llms.txt Status:     {audit.llms_txt_status}")
        print(f"Total Issues Found:  {len(audit.issues)}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
