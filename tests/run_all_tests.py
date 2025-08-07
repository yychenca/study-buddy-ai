"""
Master test runner for all RAG homework tasks.
Students can run this to test their complete implementation.

Usage: python tests/run_all_tests.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_task1_document_processing import run_task1_tests
from test_task2_embeddings import run_task2_tests
from test_task3_vector_storage import run_task3_tests
from test_task4_retrieval import run_task4_tests
from test_task5_rag_generation import run_task5_tests

def run_all_rag_tests():
    """Run all RAG homework tests in sequence"""
    print("🚀 STUDYBUDDY AI - RAG HOMEWORK TEST SUITE")
    print("=" * 80)
    print("Testing your complete RAG implementation...")
    print("This will test all 5 tasks in the RAG pipeline:")
    print("1. Document Loading & Text Extraction")  
    print("2. Embedding Generation")
    print("3. Vector Storage")
    print("4. Similarity Retrieval")
    print("5. Context-Aware Generation")
    print("=" * 80)
    
    # Track overall results
    all_tasks_passed = True
    
    try:
        # Task 1: Document Processing
        print("\n" + "🔄" * 20)
        run_task1_tests()
        
        # Task 2: Embeddings
        print("\n" + "🔄" * 20)
        run_task2_tests()
        
        # Task 3: Vector Storage  
        print("\n" + "🔄" * 20)
        run_task3_tests()
        
        # Task 4: Retrieval
        print("\n" + "🔄" * 20)
        run_task4_tests()
        
        # Task 5: RAG Generation
        print("\n" + "🔄" * 20)
        run_task5_tests()
        
    except Exception as e:
        print(f"❌ Test suite error: {e}")
        all_tasks_passed = False
    
    # Final results
    print("\n" + "🎯" * 80)
    print("FINAL RESULTS")
    print("🎯" * 80)
    
    if all_tasks_passed:
        print("🎉 CONGRATULATIONS! 🎉")
        print("You have successfully implemented a complete RAG system!")
        print()
        print("Your implementation includes:")
        print("✅ Document processing (PDF, DOCX, TXT)")
        print("✅ Text chunking for optimal embeddings")
        print("✅ Vector embedding generation with Gemini")
        print("✅ Vector storage and indexing with Pinecone")
        print("✅ Semantic similarity search")
        print("✅ Context-aware response generation")
        print()
        print("🚀 Ready to test your RAG system with real documents!")
        print("💡 Try uploading some documents and asking questions about them!")
    else:
        print("⚠️  Some tasks need more work. Don't worry - this is part of learning!")
        print()
        print("📚 Review the test output above for specific guidance.")
        print("💡 Work through the tasks one by one - each builds on the previous.")
        print("🆘 Ask your TA for help if you're stuck on any task!")
    
    print("🎯" * 80)

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 ENVIRONMENT CHECK")
    print("-" * 40)
    
    # Check for required environment variables
    required_env_vars = ["GEMINI_API_KEY", "PINECONE_API_KEY"]
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Make sure your .env file is properly configured")
        return False
    else:
        print("✅ Environment variables configured")
        return True

if __name__ == "__main__":
    # Check environment first
    if not check_environment():
        print("\n⚠️  Please fix environment setup before running tests")
        sys.exit(1)
    
    # Run all tests
    run_all_rag_tests()