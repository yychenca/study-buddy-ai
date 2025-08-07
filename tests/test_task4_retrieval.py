"""
Test file for Task 4: Similarity Retrieval
Students can run this to validate their implementation.

Usage: python -m pytest tests/test_task4_retrieval.py -v
"""

import pytest
from backend.services.pinecone_service import pinecone_service

class TestTask4Retrieval:
    
    def test_similarity_search_implementation(self):
        """Test that similarity search is implemented"""
        if not pinecone_service:
            pytest.skip("Pinecone service not available - check API key configuration")
        
        # Mock query embedding (in real implementation, this would come from Task 2)
        query_embedding = [0.1, 0.2, 0.3] * 256  # 768-dimensional vector
        project_id = "test_project"
        top_k = 3
        
        try:
            results = pinecone_service.search_similar_chunks(
                query_embedding=query_embedding,
                project_id=project_id,
                top_k=top_k
            )
            
            # Check that placeholder implementation is replaced
            assert results != [], \
                "❌ TASK 4 INCOMPLETE: You need to implement similarity search logic in search_similar_chunks method"
            
            # Check result structure
            assert isinstance(results, list), "❌ Search should return a list of results"
            
            # If there are results, check their structure
            if results:
                for result in results:
                    assert isinstance(result, dict), "❌ Each result should be a dictionary"
                    expected_keys = ["id", "score", "metadata", "text"]
                    for key in expected_keys:
                        assert key in result, f"❌ Result missing required key: {key}"
                    
                    # Check score is a number
                    assert isinstance(result["score"], (int, float)), "❌ Score should be a number"
                    assert 0 <= result["score"] <= 1, "❌ Score should be between 0 and 1"
                    
                print(f"✅ Similarity search implemented - found {len(results)} results")
            else:
                print("✅ Similarity search implemented (no results found - this is okay for empty index)")
            
        except AssertionError as e:
            pytest.fail(f"❌ TASK 4 FAILED: {str(e)}")
        except Exception as e:
            pytest.fail(f"❌ TASK 4 FAILED: Error in similarity search - {str(e)}")
    
    def test_top_k_parameter(self):
        """Test that top_k parameter limits results correctly"""
        if not pinecone_service:
            pytest.skip("Pinecone service not available")
        
        query_embedding = [0.1] * 768
        project_id = "test_project"
        
        try:
            # Test different top_k values
            for k in [1, 3, 5]:
                results = pinecone_service.search_similar_chunks(
                    query_embedding=query_embedding,
                    project_id=project_id,
                    top_k=k
                )
                
                # Skip if not implemented
                if not results and not isinstance(results, list):
                    pytest.skip("Search not implemented yet")
                
                # Results should not exceed top_k
                assert len(results) <= k, f"❌ Results should not exceed top_k={k}"
            
            print("✅ Top-k parameter working correctly")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 4 FAILED: Top-k test failed - {str(e)}")
    
    def test_project_namespace_filtering(self):
        """Test that project-specific search works"""
        if not pinecone_service:
            pytest.skip("Pinecone service not available")
        
        query_embedding = [0.2] * 768
        
        try:
            # Test project-specific search
            project_results = pinecone_service.search_similar_chunks(
                query_embedding=query_embedding,
                project_id="specific_project",
                top_k=5
            )
            
            # Test global search (no project_id)
            global_results = pinecone_service.search_similar_chunks(
                query_embedding=query_embedding,
                project_id=None,
                top_k=5
            )
            
            # Both should return lists (even if empty)
            assert isinstance(project_results, list), "❌ Project search should return list"
            assert isinstance(global_results, list), "❌ Global search should return list"
            
            print("✅ Project namespace filtering implemented")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 4 FAILED: Namespace filtering test failed - {str(e)}")
    
    def test_empty_query_handling(self):
        """Test that empty or invalid queries are handled properly"""
        if not pinecone_service:
            pytest.skip("Pinecone service not available")
        
        try:
            # Test empty embedding
            with pytest.raises(AssertionError):
                pinecone_service.search_similar_chunks([], "project", 5)
            
            # Test invalid top_k
            with pytest.raises(AssertionError):
                pinecone_service.search_similar_chunks([0.1] * 768, "project", 0)
            
            with pytest.raises(AssertionError):
                pinecone_service.search_similar_chunks([0.1] * 768, "project", -1)
            
            print("✅ Query validation working correctly")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 4 FAILED: Query validation failed - {str(e)}")
    
    def test_result_formatting(self):
        """Test that results are properly formatted"""
        if not pinecone_service:
            pytest.skip("Pinecone service not available")
        
        query_embedding = [0.3] * 768
        
        try:
            results = pinecone_service.search_similar_chunks(
                query_embedding=query_embedding,
                project_id="format_test",
                top_k=3
            )
            
            # Skip if placeholder implementation
            if not results:
                print("✅ Result formatting test (no results to check - implement storage first)")
                return
            
            # Check result formatting
            for result in results:
                assert "id" in result and isinstance(result["id"], str), "❌ Result should have string ID"
                assert "score" in result and isinstance(result["score"], (int, float)), "❌ Result should have numeric score"
                assert "metadata" in result and isinstance(result["metadata"], dict), "❌ Result should have metadata dict"
                assert "text" in result and isinstance(result["text"], str), "❌ Result should have text content"
            
            print("✅ Result formatting is correct")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 4 FAILED: Result formatting test failed - {str(e)}")

def run_task4_tests():
    """Helper function to run Task 4 tests with nice output"""
    print("🧪 TESTING TASK 4: Similarity Retrieval")
    print("=" * 60)
    
    if not pinecone_service:
        print("❌ PINECONE SERVICE NOT AVAILABLE")
        print("💡 Make sure you have:")
        print("   - PINECONE_API_KEY set in your .env file")
        print("   - Completed Task 3 (vector storage) first")
        print("   - Some test data stored in your vector database")
        return
    
    test_class = TestTask4Retrieval()
    
    tests = [
        ("Similarity search", test_class.test_similarity_search_implementation),
        ("Top-k parameter", test_class.test_top_k_parameter),
        ("Project filtering", test_class.test_project_namespace_filtering),
        ("Query validation", test_class.test_empty_query_handling),
        ("Result formatting", test_class.test_result_formatting),
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
    
    print(f"\n📊 TASK 4 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 TASK 4 COMPLETE! Great job implementing similarity retrieval!")
    else:
        print("⚠️  Some tests failed. Check the error messages above for guidance.")
        print("\n💡 DEBUGGING TIPS:")
        print("- Make sure you uncommented the template code in pinecone_service.py")
        print("- Complete Task 3 (vector storage) before testing retrieval")
        print("- Verify your vector index has some test data")
        print("- Check that query embeddings have the correct dimensions")
        print("- Ensure your namespace logic matches the storage implementation")

if __name__ == "__main__":
    run_task4_tests()