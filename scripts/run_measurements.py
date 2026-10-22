import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.core.database import SessionLocal
from backend.app.services.measurement_runner import measurement_runner

def main():
    print("Executing Automated Measurement Run...")
    db = SessionLocal()
    try:
        run = measurement_runner.execute_measurement_run(
            db=db,
            run_name="Automated Script Measurement Run",
            market="US",
            search_provider="mock",
            ai_providers=["openai", "gemini", "perplexity", "claude_manual"]
        )
        print("Measurement Run Completed!")
        print(f"Run ID:        {run.id}")
        print(f"Status:        {run.status}")
        print(f"Questions:     {run.questions_count}")
        print(f"Success Count: {run.successful_measurements}")
        print(f"Est Cost:      ${run.estimated_cost_usd} USD")
    finally:
        db.close()

if __name__ == "__main__":
    main()
