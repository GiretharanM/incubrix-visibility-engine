import uvicorn
import os
import sys

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting IncuBrix FastAPI Backend on http://127.0.0.1:8001...")
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8001, log_level="info")
