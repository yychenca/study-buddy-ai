#!/usr/bin/env python3
"""
StudyBuddy AI Backend Startup Script

This script initializes the database and starts the FastAPI backend server.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to Python path and change working directory
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Load environment variables explicitly
from dotenv import load_dotenv
load_dotenv()

def check_environment():
    """Check if required environment variables are set"""
    # Debug: Check current working directory and .env file
    print(f"🔍 Current working directory: {os.getcwd()}")
    env_file = Path(".env")
    print(f"🔍 .env file exists: {env_file.exists()}")
    if env_file.exists():
        print(f"🔍 .env file path: {env_file.absolute()}")
    
    required_vars = ['GEMINI_API_KEY', 'PINECONE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Show first few characters for debugging (don't show full key)
            print(f"✅ {var}: {value[:10]}...")
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please check your .env file and make sure it's in the correct location")
        return False
    
    print("✅ Environment variables configured")
    return True

def initialize_database():
    """Initialize the SQLite database"""
    print("🗄️  Initializing database...")
    try:
        from scripts.init_db import init_database
        init_database()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI backend server...")
    try:
        import uvicorn
        
        uvicorn.run(
            "backend.main:app",
            host="localhost",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main startup function"""
    print("🎯 StudyBuddy AI Backend Startup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()