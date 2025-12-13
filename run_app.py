import subprocess
import time
import sys
import os

def main():
    print("Starting Backend (FastAPI)...")
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"])
    time.sleep(3)
    print("Starting Frontend (Streamlit)...")
    frontend = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    main()
