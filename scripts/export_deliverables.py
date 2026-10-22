import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.core.database import SessionLocal
from backend.app.services.report_generator import report_generator

def main():
    print("Exporting all assessment deliverables...")
    db = SessionLocal()
    os.makedirs("artifacts", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    try:
        # 1. visibility.csv
        vis_csv = report_generator.generate_visibility_csv(db)
        with open("artifacts/visibility.csv", "w", encoding="utf-8") as f:
            f.write(vis_csv)
        with open("reports/visibility.csv", "w", encoding="utf-8") as f:
            f.write(vis_csv)
        print("Exported artifacts/visibility.csv and reports/visibility.csv")

        # 2. submission_workbook.csv
        sub_csv = report_generator.generate_submission_workbook_csv(db)
        with open("reports/submission_workbook.csv", "w", encoding="utf-8") as f:
            f.write(sub_csv)
        print("Exported reports/submission_workbook.csv")

        # 3. Weekly Report HTML
        html_report = report_generator.generate_weekly_report_html(db)
        with open("reports/weekly_report_week42.html", "w", encoding="utf-8") as f:
            f.write(html_report)
        print("Exported reports/weekly_report_week42.html")

        print("All deliverables generated successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
