"""
Test file for Task 5: Context-Aware Generation
Students can run this to validate their implementation.

Usage: python -m pytest tests/test_task5_rag_generation.py -v
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from backend.routers.chat import chat_with_project
from backend.models import ChatMessage

class TestTask5RAGGeneration:
    
    @pytest.mark.asyncio
    async def test_rag_pipeline_implementation(self):
        """Test that the complete RAG pipeline is implemented"""
        # Mock the database and services
        with patch('backend.routers.chat.db') as mock_db, \
             patch('backend.routers.chat.gemini_service') as mock_gemini, \
             patch('backend.routers.chat.pinecone_service') as mock_pinecone:
            
            # Setup mocks
            mock_db.get_project.return_value = Mock(id="test_project", name="Test Project")
            mock_db.create_chat_history.return_value = None
            
            # Mock successful embedding generation
            mock_gemini.generate_query_embedding.return_value = [0.1] * 768
            
            # Mock search results
            mock_pinecone.search_similar_chunks.return_value = [
                {
                    "id": "doc1_0",
                    "score": 0.95,
                    "metadata": {"filename": "test.pdf"},
                    "text": "This is relevant content from the document."
                }
            ]
            
            # Mock response generation
            mock_gemini.generate_response.return_value = "Based on the documents, here is the answer."
            
            # Test message
            message = ChatMessage(message="What is the main topic of the documents?")
            
            try:
                result = await chat_with_project("test_project", message)
                
                # Check that response is not the placeholder
                assert result["response"] != "TODO: Implement RAG-powered chat response", \
                    "❌ TASK 5 INCOMPLETE: You need to implement RAG pipeline in chat.py"
                
                # Check result structure
                assert isinstance(result, dict), "❌ Chat should return a dictionary"
                assert "message" in result, "❌ Result should include original message"
                assert "response" in result, "❌ Result should include AI response"
                assert "sources_used" in result, "❌ Result should include number of sources used"
                
                print("✅ RAG pipeline implemented successfully")
                
            except AssertionError as e:
                pytest.fail(f"❌ TASK 5 FAILED: {str(e)}")
            except Exception as e:
                pytest.fail(f"❌ TASK 5 FAILED: Error in RAG pipeline - {str(e)}")
    
    @pytest.mark.asyncio
    async def test_query_embedding_step(self):
        """Test that query embedding step is implemented"""
        with patch('backend.routers.chat.db') as mock_db, \
             patch('backend.routers.chat.gemini_service') as mock_gemini, \
             patch('backend.routers.chat.pinecone_service') as mock_pinecone:
            
            mock_db.get_project.return_value = Mock(id="test_project")
            mock_db.create_chat_history.return_value = None
            
            # Test that query embedding is called
            mock_gemini.generate_query_embedding.return_value = [0.1] * 768
            mock_pinecone.search_similar_chunks.return_value = []
            mock_gemini.generate_response.return_value = "Test response"
            
            message = ChatMessage(message="Test question")
            
            try:
                await chat_with_project("test_project", message)
                
                # Verify that query embedding was called
                mock_gemini.generate_query_embedding.assert_called_once_with("Test question")
                print("✅ Query embedding step implemented")
                
            except AssertionError:
                # This means the implementation is not using the template
                print("❌ Query embedding step not implemented correctly")
                pytest.fail("❌ TASK 5 FAILED: Query embedding step missing")
    
    @pytest.mark.asyncio  
    async def test_context_retrieval_step(self):
        """Test that context retrieval step is implemented"""
        with patch('backend.routers.chat.db') as mock_db, \
             patch('backend.routers.chat.gemini_service') as mock_gemini, \
             patch('backend.routers.chat.pinecone_service') as mock_pinecone:
            
            mock_db.get_project.return_value = Mock(id="test_project")
            mock_db.create_chat_history.return_value = None
            
            query_embedding = [0.1] * 768
            mock_gemini.generate_query_embedding.return_value = query_embedding
            mock_pinecone.search_similar_chunks.return_value = [
                {"text": "Retrieved context"}
            ]
            mock_gemini.generate_response.return_value = "Response with context"
            
            message = ChatMessage(message="Test question")
            
            try:
                await chat_with_project("test_project", message)
                
                # Verify that similarity search was called with correct parameters
                mock_pinecone.search_similar_chunks.assert_called_once_with(
                    query_embedding=query_embedding,
                    project_id="test_project", 
                    top_k=5
                )
                print("✅ Context retrieval step implemented")
                
            except AssertionError:
                print("❌ Context retrieval step not implemented correctly")
                pytest.fail("❌ TASK 5 FAILED: Context retrieval step missing")
    
    @pytest.mark.asyncio
    async def test_context_aware_generation(self):
        """Test that retrieved context is used for generation"""
        with patch('backend.routers.chat.db') as mock_db, \
             patch('backend.routers.chat.gemini_service') as mock_gemini, \
             patch('backend.routers.chat.pinecone_service') as mock_pinecone:
            
            mock_db.get_project.return_value = Mock(id="test_project")
            mock_db.create_chat_history.return_value = None
            
            mock_gemini.generate_query_embedding.return_value = [0.1] * 768
            
            # Mock retrieved context
            retrieved_chunks = ["Context chunk 1", "Context chunk 2"]
            mock_pinecone.search_similar_chunks.return_value = [
                {"text": chunk} for chunk in retrieved_chunks
            ]
            
            mock_gemini.generate_response.return_value = "Context-aware response"
            
            message = ChatMessage(message="Test question")
            
            try:
                await chat_with_project("test_project", message)
                
                # Verify that generate_response was called with context
                mock_gemini.generate_response.assert_called_once_with(
                    prompt="Test question",
                    context=retrieved_chunks
                )
                print("✅ Context-aware generation implemented")
                
            except AssertionError:
                print("❌ Context-aware generation not implemented correctly")
                pytest.fail("❌ TASK 5 FAILED: Context not passed to generation")
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test that errors are handled gracefully"""
        with patch('backend.routers.chat.db') as mock_db:
            # Test project not found
            mock_db.get_project.return_value = None
            
            message = ChatMessage(message="Test question")
            
            try:
                with pytest.raises(Exception):  # Should raise HTTPException
                    await chat_with_project("nonexistent_project", message)
                
                print("✅ Error handling working correctly")
                
            except Exception as e:
                pytest.fail(f"❌ TASK 5 FAILED: Error handling test failed - {str(e)}")
    
    @pytest.mark.asyncio
    async def test_message_validation(self):
        """Test that empty messages are handled"""
        with patch('backend.routers.chat.db') as mock_db:
            mock_db.get_project.return_value = Mock(id="test_project")
            
            # Test empty message
            empty_message = ChatMessage(message="")
            
            try:
                with pytest.raises(AssertionError):
                    await chat_with_project("test_project", empty_message)
                
                print("✅ Message validation working correctly")
                
            except Exception as e:
                pytest.fail(f"❌ TASK 5 FAILED: Message validation failed - {str(e)}")

def run_task5_tests():
    """Helper function to run Task 5 tests with nice output"""
    print("🧪 TESTING TASK 5: Context-Aware Generation")
    print("=" * 60)
    
    test_class = TestTask5RAGGeneration()
    
    tests = [
        ("RAG pipeline", test_class.test_rag_pipeline_implementation),
        ("Query embedding", test_class.test_query_embedding_step),
        ("Context retrieval", test_class.test_context_retrieval_step),
        ("Context generation", test_class.test_context_aware_generation),
        ("Error handling", test_class.test_error_handling),
        ("Message validation", test_class.test_message_validation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n📋 Testing {test_name}...")
            # Run async tests
            if asyncio.iscoroutinefunction(test_func):
                asyncio.run(test_func())
            else:
                test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {test_name} FAILED: {str(e)}")
    
    print(f"\n📊 TASK 5 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 TASK 5 COMPLETE! Great job implementing the full RAG pipeline!")
        print("🎉 ALL TASKS COMPLETE! You've built a complete RAG system!")
    else:
        print("⚠️  Some tests failed. Check the error messages above for guidance.")
        print("\n💡 DEBUGGING TIPS:")
        print("- Make sure you uncommented the template code in chat.py")
        print("- Complete Tasks 1-4 before implementing Task 5")
        print("- Verify that all previous tasks are working correctly")
        print("- Check that your RAG pipeline follows the 5-step process")
        print("- Ensure error handling is implemented for edge cases")

if __name__ == "__main__":
    run_task5_tests()