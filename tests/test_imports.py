"""
Simple test to validate that imports work correctly.
Students can run this to verify their environment is set up properly.

Usage: python tests/test_imports.py
"""

import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 TESTING MODULE IMPORTS")
    print("=" * 40)
    
    try:
        print("📦 Testing backend.services.processor...")
        from backend.services.processor import document_processor
        print("✅ processor imported successfully")
    except ImportError as e:
        print(f"❌ processor import failed: {e}")
        return False
    
    try:
        print("📦 Testing backend.services.gemini_service...")
        from backend.services.gemini_service import gemini_service
        print("✅ gemini_service imported successfully")
    except ImportError as e:
        print(f"❌ gemini_service import failed: {e}")
        return False
    
    try:
        print("📦 Testing backend.services.pinecone_service...")
        from backend.services.pinecone_service import pinecone_service
        print("✅ pinecone_service imported successfully")
    except ImportError as e:
        print(f"❌ pinecone_service import failed: {e}")
        return False
    
    try:
        print("📦 Testing backend.routers.chat...")
        from backend.routers.chat import chat_with_project
        print("✅ chat imported successfully")
    except ImportError as e:
        print(f"❌ chat import failed: {e}")
        return False
    
    try:
        print("📦 Testing backend.models...")
        from backend.models import ChatMessage
        print("✅ models imported successfully")
    except ImportError as e:
        print(f"❌ models import failed: {e}")
        return False
    
    print("\n🎉 ALL IMPORTS SUCCESSFUL!")
    print("Your test environment is properly configured.")
    print("You can now run the individual task tests:")
    print("- python tests/test_task1_document_processing.py")
    print("- python tests/test_task2_embeddings.py") 
    print("- python tests/test_task3_vector_storage.py")
    print("- python tests/test_task4_retrieval.py")
    print("- python tests/test_task5_rag_generation.py")
    print("- python tests/run_all_tests.py")
    
    return True

if __name__ == "__main__":
    success = test_imports()
    if not success:
        print("\n💡 TROUBLESHOOTING:")
        print("- Make sure you're running from the project root directory")
        print("- Check that all backend modules exist in the correct locations")
        print("- Verify your Python environment has all required packages")
        sys.exit(1)