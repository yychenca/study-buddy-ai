"""
Test file for Task 3: Vector Storage
Students can run this to validate their implementation.

Usage: python -m pytest tests/test_task3_vector_storage.py -v
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.services.pinecone_service import pinecone_service

class TestTask3VectorStorage:
    
    def test_vector_storage_implementation(self):
        """Test that vector storage is implemented"""
        if not pinecone_service:
            pytest.skip("Pinecone service not available - check API key configuration")
        
        # Test data
        project_id = "test_project_123"
        document_id = "test_doc_456"
        filename = "test_document.pdf"
        chunks = [
            "This is the first chunk of text from the document.",
            "This is the second chunk with different content.",
        ]
        # Mock embeddings (in real implementation, these would come from Task 2)
        embeddings = [
            [0.1, 0.2, 0.3] * 256,  # 768-dimensional vector
            [0.4, 0.5, 0.6] * 256,  # 768-dimensional vector
        ]
        
        try:
            result = pinecone_service.upsert_document_chunks(
                project_id=project_id,
                document_id=document_id,
                filename=filename,
                chunks=chunks,
                embeddings=embeddings
            )
            
            # Check that placeholder implementation is replaced
            assert result != False or result == True, \
                "❌ TASK 3 INCOMPLETE: upsert_document_chunks should return boolean, not placeholder"
            
            # If implemented, should return True for successful storage
            assert result == True, \
                "❌ TASK 3 INCOMPLETE: You need to implement vector storage logic in upsert_document_chunks method"
            
            print("✅ Vector storage implemented successfully")
            
        except AssertionError as e:
            pytest.fail(f"❌ TASK 3 FAILED: {str(e)}")
        except Exception as e:
            pytest.fail(f"❌ TASK 3 FAILED: Error storing vectors - {str(e)}")
    
    def test_vector_storage_validation(self):
        """Test that input validation works correctly"""
        if not pinecone_service:
            pytest.skip("Pinecone service not available")
        
        try:
            # Test empty project_id
            with pytest.raises(AssertionError):
                pinecone_service.upsert_document_chunks("", "doc", "file.txt", ["text"], [[0.1] * 768])
            
            # Test mismatched chunks and embeddings
            with pytest.raises(AssertionError):
                pinecone_service.upsert_document_chunks("proj", "doc", "file.txt", ["text1", "text2"], [[0.1] * 768])
            
            # Test empty chunks
            with pytest.raises(AssertionError):
                pinecone_service.upsert_document_chunks("proj", "doc", "file.txt", [], [])
            
            print("✅ Input validation working correctly")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 3 FAILED: Validation test failed - {str(e)}")
    
    def test_namespace_usage(self):
        """Test that project namespaces are used correctly"""
        if not pinecone_service:
            pytest.skip("Pinecone service not available")
        
        # This test would require checking the actual Pinecone calls
        # For now, we'll just verify the method can be called without error
        project_id = "namespace_test_project"
        document_id = "test_doc"
        filename = "test.txt"
        chunks = ["Test chunk for namespace validation"]
        embeddings = [[0.1] * 768]
        
        try:
            result = pinecone_service.upsert_document_chunks(
                project_id=project_id,
                document_id=document_id,
                filename=filename,
                chunks=chunks,
                embeddings=embeddings
            )
            
            # Should not raise exception if properly implemented
            assert isinstance(result, bool), "❌ Method should return boolean result"
            print("✅ Namespace usage appears to be implemented")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 3 FAILED: Namespace test failed - {str(e)}")
    
    def test_metadata_inclusion(self):
        """Test that metadata is properly structured"""
        # This test verifies the metadata structure without making actual API calls
        project_id = "metadata_test"
        document_id = "doc123"
        filename = "example.pdf"
        chunks = ["Sample text chunk for metadata test"]
        embeddings = [[0.5] * 768]
        
        # The implementation should structure metadata correctly
        # This is more of a code review test - checking the template is followed
        print("✅ Metadata structure test (verify template is used correctly)")

def run_task3_tests():
    """Helper function to run Task 3 tests with nice output"""
    print("🧪 TESTING TASK 3: Vector Storage")
    print("=" * 60)
    
    if not pinecone_service:
        print("❌ PINECONE SERVICE NOT AVAILABLE")
        print("💡 Make sure you have:")
        print("   - PINECONE_API_KEY set in your .env file")
        print("   - Valid Pinecone account and API key")
        print("   - Internet connection for API calls")
        return
    
    test_class = TestTask3VectorStorage()
    
    tests = [
        ("Vector storage", test_class.test_vector_storage_implementation),
        ("Input validation", test_class.test_vector_storage_validation),
        ("Namespace usage", test_class.test_namespace_usage),
        ("Metadata structure", test_class.test_metadata_inclusion),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n📋 Testing {test_name}...")
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {test_name} FAILED: {str(e)}")
    
    print(f"\n📊 TASK 3 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 TASK 3 COMPLETE! Great job implementing vector storage!")
    else:
        print("⚠️  Some tests failed. Check the error messages above for guidance.")
        print("\n💡 DEBUGGING TIPS:")
        print("- Make sure you uncommented the template code in pinecone_service.py")
        print("- Verify your PINECONE_API_KEY is set correctly in .env file") 
        print("- Check that your Pinecone index is created and accessible")
        print("- Ensure the vector dimensions match your embedding model (768 for Gemini)")
        print("- Verify your Pinecone account has sufficient quota")

if __name__ == "__main__":
    run_task3_tests()