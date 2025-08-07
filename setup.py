#!/usr/bin/env python3
"""
StudyBuddy AI Setup Script

This script helps set up the StudyBuddy AI application.
"""

import os
import sys
import subprocess
from pathlib import Path

def create_virtual_environment():
    """Create a virtual environment"""
    print("🐍 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = Path("venv/Scripts/pip")
    else:  # macOS/Linux
        pip_path = Path("venv/bin/pip")
    
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment_file():
    """Set up the environment file"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created")
            print("💡 Please edit .env file and add your API keys")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ .env.example file not found")
        return False

def initialize_database():
    """Initialize the database"""
    print("🗄️  Initializing database...")
    
    # Determine the correct python path
    if os.name == 'nt':  # Windows
        python_path = Path("venv/Scripts/python")
    else:  # macOS/Linux
        python_path = Path("venv/bin/python")
    
    try:
        subprocess.run([str(python_path), "scripts/init_db.py"], check=True)
        print("✅ Database initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Edit the .env file and add your API keys:")
    print("   - GEMINI_API_KEY=your_gemini_key_here")
    print("   - PINECONE_API_KEY=your_pinecone_key_here")
    print("   - PINECONE_ENV=your_pinecone_environment_here")
    print("\n2. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # macOS/Linux
        print("   source venv/bin/activate")
    print("\n3. Start the application:")
    print("   python start_backend.py    # In first terminal")
    print("   python start_frontend.py   # In second terminal")
    print("\n4. Open your browser and go to:")
    print("   http://localhost:8501")
    print("\n📚 Happy studying with StudyBuddy AI!")

def main():
    """Main setup function"""
    print("🎯 StudyBuddy AI Setup")
    print("=" * 30)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        sys.exit(1)
    
    # Initialize database
    # Note: This might fail if API keys aren't set up yet, but that's okay
    initialize_database()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()