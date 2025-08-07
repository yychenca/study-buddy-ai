"""
Test file for Task 2: Embedding Generation
Students can run this to validate their implementation.

Usage: python -m pytest tests/test_task2_embeddings.py -v
"""

import pytest
from backend.services.gemini_service import gemini_service

class TestTask2Embeddings:
    
    def test_document_embedding_implementation(self):
        """Test that document embedding generation is implemented"""
        test_text = "This is a sample document chunk for embedding generation."
        
        try:
            embedding = gemini_service.generate_embedding(test_text)
            
            # Check that placeholder implementation is replaced
            assert embedding != [0.0] * 768, \
                "❌ TASK 2 INCOMPLETE: You need to replace placeholder implementation in generate_embedding method"
            
            # Check embedding properties
            assert isinstance(embedding, list), "❌ Embedding should be a list"
            assert len(embedding) > 0, "❌ Embedding should not be empty"
            assert all(isinstance(x, (int, float)) for x in embedding), "❌ Embedding should contain only numbers"
            
            print(f"✅ Document embedding generated successfully ({len(embedding)} dimensions)")
            
        except AssertionError as e:
            pytest.fail(f"❌ TASK 2 FAILED: {str(e)}")
        except Exception as e:
            pytest.fail(f"❌ TASK 2 FAILED: Error generating embedding - {str(e)}")
    
    def test_query_embedding_implementation(self):
        """Test that query embedding generation is implemented"""
        test_query = "What are the main topics covered in this document?"
        
        try:
            embedding = gemini_service.generate_query_embedding(test_query)
            
            # Check that placeholder implementation is replaced
            assert embedding != [0.0] * 768, \
                "❌ TASK 2 INCOMPLETE: You need to replace placeholder implementation in generate_query_embedding method"
            
            # Check embedding properties
            assert isinstance(embedding, list), "❌ Query embedding should be a list"
            assert len(embedding) > 0, "❌ Query embedding should not be empty"
            assert all(isinstance(x, (int, float)) for x in embedding), "❌ Query embedding should contain only numbers"
            
            print(f"✅ Query embedding generated successfully ({len(embedding)} dimensions)")
            
        except AssertionError as e:
            pytest.fail(f"❌ TASK 2 FAILED: {str(e)}")
        except Exception as e:
            pytest.fail(f"❌ TASK 2 FAILED: Error generating query embedding - {str(e)}")
    
    def test_embedding_consistency(self):
        """Test that same text produces same embedding"""
        test_text = "Consistency test text"
        
        try:
            embedding1 = gemini_service.generate_embedding(test_text)
            embedding2 = gemini_service.generate_embedding(test_text)
            
            # Skip if placeholder implementation
            if embedding1 == [0.0] * 768:
                pytest.skip("Placeholder implementation - implement embedding generation first")
            
            # Embeddings should be identical for same input
            assert embedding1 == embedding2, "❌ Same text should produce identical embeddings"
            
            print("✅ Embedding generation is consistent")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 2 FAILED: Consistency test failed - {str(e)}")
    
    def test_embedding_different_texts(self):
        """Test that different texts produce different embeddings"""
        text1 = "Machine learning is a subset of artificial intelligence."
        text2 = "Natural language processing helps computers understand human language."
        
        try:
            embedding1 = gemini_service.generate_embedding(text1)
            embedding2 = gemini_service.generate_embedding(text2)
            
            # Skip if placeholder implementation
            if embedding1 == [0.0] * 768:
                pytest.skip("Placeholder implementation - implement embedding generation first")
            
            # Different texts should produce different embeddings
            assert embedding1 != embedding2, "❌ Different texts should produce different embeddings"
            
            print("✅ Different texts produce different embeddings")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 2 FAILED: Different text test failed - {str(e)}")
    
    def test_empty_text_handling(self):
        """Test that empty or invalid text is handled properly"""
        try:
            # Test empty string
            with pytest.raises(AssertionError):
                gemini_service.generate_embedding("")
            
            # Test None
            with pytest.raises(AssertionError):
                gemini_service.generate_embedding(None)
            
            # Test whitespace only
            with pytest.raises(AssertionError):
                gemini_service.generate_embedding("   ")
            
            print("✅ Empty/invalid text handling works correctly")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 2 FAILED: Empty text handling failed - {str(e)}")

def run_task2_tests():
    """Helper function to run Task 2 tests with nice output"""
    print("🧪 TESTING TASK 2: Embedding Generation")
    print("=" * 60)
    
    test_class = TestTask2Embeddings()
    
    tests = [
        ("Document embedding", test_class.test_document_embedding_implementation),
        ("Query embedding", test_class.test_query_embedding_implementation),
        ("Embedding consistency", test_class.test_embedding_consistency),
        ("Different texts", test_class.test_embedding_different_texts),
        ("Empty text handling", test_class.test_empty_text_handling),
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
    
    print(f"\n📊 TASK 2 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 TASK 2 COMPLETE! Great job implementing embedding generation!")
    else:
        print("⚠️  Some tests failed. Check the error messages above for guidance.")
        print("\n💡 DEBUGGING TIPS:")
        print("- Make sure you uncommented the template code in gemini_service.py")
        print("- Verify your GEMINI_API_KEY is set correctly in .env file")
        print("- Check that you're using the correct model name and task_type")
        print("- Ensure your API key has proper permissions for embedding generation")

if __name__ == "__main__":
    run_task2_tests()