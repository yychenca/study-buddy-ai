from fastapi import APIRouter, HTTPException
from typing import List
from backend.models import ChatMessage, ChatHistory, SearchQuery, SearchResult
from backend.database import db
from backend.services.gemini_service import gemini_service
from backend.services.pinecone_service import pinecone_service

router = APIRouter(prefix="/api/projects/{project_id}/chat", tags=["chat"])

@router.post("/")
async def chat_with_project(project_id: str, message: ChatMessage):
    """Chat with documents in a specific project"""
    try:
        # Check if project exists
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # TODO: TASK 5 - CONTEXT-AWARE GENERATION
        # Students need to implement RAG-powered chat responses
        # This is the "Generate" step in the RAG pipeline
        
        # TODO: Implement RAG chat pipeline
        # Instructions:
        # 1. Convert user question to embedding for similarity search
        # 2. Search vector database for relevant document chunks
        # 3. Extract text content from search results
        # 4. Combine retrieved context with user question in prompt
        # 5. Generate final answer using LLM with document context
        # 6. Handle cases where no relevant documents are found
        #
        # RAG Generation Pipeline:
        # User Query → Query Embedding → Vector Search → Context Retrieval → LLM Generation
        #
        # Expected behavior:
        # - Input: User's question/message
        # - Output: AI response grounded in uploaded documents
        # - Use retrieved document chunks as context for more accurate answers
        # - Distinguish between document-based answers vs general knowledge
        
        assert message.message and message.message.strip(), "Message cannot be empty"
        
        # TODO: Replace this placeholder implementation
        # Students need to implement the complete RAG pipeline
        query_embedding = None
        relevant_chunks = []
        response = "TODO: Implement RAG-powered chat response"
        
        # Save chat history
        chat_history = ChatHistory.create_new(
            project_id=project_id,
            message=message.message,
            response=response
        )
        await db.create_chat_history(chat_history)
        
        return {
            "message": message.message,
            "response": response,
            "sources_used": len(relevant_chunks),
            "timestamp": chat_history.timestamp
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process chat message: {str(e)}")

@router.get("/history", response_model=List[ChatHistory])
async def get_chat_history(project_id: str, limit: int = 50):
    """Get chat history for a project"""
    try:
        # Check if project exists
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        history = await db.get_chat_history(project_id, limit)
        return history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chat history: {str(e)}")

@router.post("/search", response_model=List[SearchResult])
async def search_in_project(project_id: str, query: SearchQuery):
    """Search within project documents"""
    try:
        # Check if project exists
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if not pinecone_service:
            raise HTTPException(status_code=503, detail="Search service not available")
        
        # Generate query embedding
        query_embedding = gemini_service.generate_query_embedding(query.query)
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to generate query embedding")
        
        # Search in project
        search_results = pinecone_service.search_similar_chunks(
            query_embedding=query_embedding,
            project_id=project_id,
            top_k=10
        )
        
        # Format results
        formatted_results = []
        for result in search_results:
            metadata = result.get("metadata", {})
            formatted_results.append(SearchResult(
                document_id=metadata.get("document_id", ""),
                filename=metadata.get("filename", "Unknown"),
                project_id=metadata.get("project_id", project_id),
                content_snippet=result.get("text", "")[:200] + "..." if len(result.get("text", "")) > 200 else result.get("text", ""),
                relevance_score=result.get("score", 0.0)
            ))
        
        return formatted_results
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search project: {str(e)}")

@router.post("/summarize")
async def summarize_project(project_id: str):
    """Generate a summary of all documents in the project"""
    try:
        # Check if project exists
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get all documents in project
        documents = await db.get_documents_by_project(project_id)
        if not documents:
            raise HTTPException(status_code=404, detail="No documents found in project")
        
        # For now, we'll generate a simple summary
        # In a full implementation, you might want to retrieve document chunks from Pinecone
        summary_prompt = f"""
        Generate a comprehensive summary for the project "{project.name}".
        
        The project contains {len(documents)} documents:
        {', '.join([doc.filename for doc in documents])}
        
        Please provide an overview of what this project might contain based on the document names and project description: {project.description or 'No description provided'}.
        """
        
        summary = await gemini_service.generate_response(summary_prompt)
        
        return {
            "project_name": project.name,
            "document_count": len(documents),
            "summary": summary,
            "documents": [{"filename": doc.filename, "upload_date": doc.upload_date} for doc in documents]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate project summary: {str(e)}")

# Global search across all projects
@router.post("/search/global", response_model=List[SearchResult])  
async def search_across_projects(query: SearchQuery):
    """Search across all projects"""
    try:
        if not pinecone_service:
            raise HTTPException(status_code=503, detail="Search service not available")
        
        # Generate query embedding
        query_embedding = gemini_service.generate_query_embedding(query.query)
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to generate query embedding")
        
        # Search across all projects
        search_results = pinecone_service.search_across_projects(
            query_embedding=query_embedding,
            top_k=15
        )
        
        # Format results
        formatted_results = []
        for result in search_results:
            metadata = result.get("metadata", {})
            formatted_results.append(SearchResult(
                document_id=metadata.get("document_id", ""),
                filename=metadata.get("filename", "Unknown"),
                project_id=metadata.get("project_id", ""),
                content_snippet=result.get("text", "")[:200] + "..." if len(result.get("text", "")) > 200 else result.get("text", ""),
                relevance_score=result.get("score", 0.0)
            ))
        
        return formatted_results
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search across projects: {str(e)}")