#!/usr/bin/env python3
"""
StudyBuddy AI Frontend Startup Script

This script starts the Streamlit frontend application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_backend():
    """Check if backend is running"""
    import requests
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
    except:
        pass
    
    print("⚠️  Backend doesn't seem to be running")
    print("💡 Please start the backend first using: python start_backend.py")
    return False

def start_streamlit():
    """Start the Streamlit frontend"""
    print("🚀 Starting Streamlit frontend...")
    try:
        # Change to project directory
        os.chdir(Path(__file__).parent)
        
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "frontend/app.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main startup function"""
    print("🎯 StudyBuddy AI Frontend Startup")
    print("=" * 40)
    
    # Check if backend is running (optional warning)
    check_backend()
    
    # Start Streamlit
    start_streamlit()

if __name__ == "__main__":
    main()