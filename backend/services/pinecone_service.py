from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Tuple, Optional
from shared.config import Config

class PineconeService:
    def __init__(self):
        if not Config.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY must be set in environment variables")
        
        # Initialize Pinecone (new API - no environment needed)
        self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        
        # Create or connect to index
        self.index_name = "studybuddy-documents"
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)
    
    def _ensure_index_exists(self):
        """Create index if it doesn't exist"""
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=Config.VECTOR_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
    
    def upsert_document_chunks(
        self, 
        project_id: str, 
        document_id: str, 
        filename: str,
        chunks: List[str], 
        embeddings: List[List[float]]
    ) -> bool:
        """Store document chunks with their embeddings"""
        # TODO: TASK 3 - VECTOR STORAGE
        # Students need to implement vector database storage
        # This is the "Store" step in the RAG pipeline
        
        # TODO: Implement vector storage in Pinecone
        # Instructions:
        # 1. Create vector records with unique IDs for each chunk
        # 2. Store embeddings along with metadata (project_id, filename, text, etc.)
        # 3. Use project-based namespaces to organize vectors by project
        # 4. Handle errors gracefully and return success/failure boolean
        # 5. Ensure metadata includes both preview text and full text
        #
        # Vector storage format:
        # - ID: Unique identifier like "document_id_chunk_index"
        # - Vector: The embedding (list of floats) 
        # - Metadata: Information about the chunk (project, file, text, etc.)
        #
        # Pinecone API usage:
        # self.index.upsert(
        #     vectors=[(id, embedding, metadata), ...],
        #     namespace="project_123"  # Organize by project
        # )
        #
        # Expected behavior:
        # - Input: Document chunks and their embeddings
        # - Output: Success/failure boolean
        # - Store vectors with rich metadata for retrieval
        # - Use namespaces to separate different projects
        
        assert project_id and isinstance(project_id, str), "Project ID must be a non-empty string"
        assert document_id and isinstance(document_id, str), "Document ID must be a non-empty string"
        assert filename and isinstance(filename, str), "Filename must be a non-empty string"
        assert chunks and len(chunks) > 0, "Chunks list cannot be empty"
        assert embeddings and len(embeddings) == len(chunks), "Must have equal number of chunks and embeddings"
        
        try:
            # TODO: Replace this placeholder implementation
            # Students need to implement the actual vector storage logic
            print(f"TODO: Store {len(chunks)} chunks for document {filename}")
            return False  # Change to True after implementing
            
        except Exception as e:
            print(f"Error upserting document chunks: {str(e)}")
            return False
    
    def search_similar_chunks(
        self, 
        query_embedding: List[float], 
        project_id: str = None,
        top_k: int = 5
    ) -> List[Dict]:
        """Search for similar document chunks"""
        # TODO: TASK 4 - SIMILARITY RETRIEVAL
        # Students need to implement vector similarity search
        # This is the "Retrieve" step in the RAG pipeline
        
        # TODO: Implement similarity search using Pinecone
        # Instructions:
        # 1. Convert user query to embedding (done elsewhere - you receive query_embedding)
        # 2. Search vector database for most similar document chunks
        # 3. Use cosine similarity to find semantically related content
        # 4. Return top_k most relevant results with metadata
        # 5. Handle project-specific search (namespace) vs global search
        # 6. Format results properly for downstream use
        #
        # Pinecone search API:
        # self.index.query(
        #     vector=query_embedding,     # The query vector
        #     top_k=top_k,               # Number of results to return
        #     include_metadata=True,      # Include stored metadata
        #     namespace=namespace         # Search within specific project (optional)
        # )
        #
        # Expected behavior:
        # - Input: Query embedding vector, optional project_id, result count
        # - Output: List of dictionaries with matching chunks and metadata
        # - Results sorted by similarity score (higher = more similar)
        # - Include full text content for context generation
        
        assert query_embedding and len(query_embedding) > 0, "Query embedding cannot be empty"
        assert isinstance(top_k, int) and top_k > 0, "top_k must be a positive integer"
        
        try:
            # TODO: Replace this placeholder implementation  
            # Students need to implement the actual similarity search
            print(f"TODO: Search for similar chunks (top_k={top_k}, project={project_id})")
            return []  # Replace with actual search results
            
        except Exception as e:
            print(f"Error searching similar chunks: {str(e)}")
            return []
    
    def search_across_projects(
        self, 
        query_embedding: List[float], 
        top_k: int = 10
    ) -> List[Dict]:
        """Search across all projects"""
        try:
            # Get all namespaces (projects)
            stats = self.index.describe_index_stats()
            namespaces = list(stats.namespaces.keys()) if stats.namespaces else [None]
            
            all_results = []
            
            # Search in each namespace
            for namespace in namespaces:
                if namespace and namespace.startswith("project_"):
                    results = self.index.query(
                        vector=query_embedding,
                        top_k=top_k,
                        include_metadata=True,
                        namespace=namespace
                    )
                    
                    for match in results.matches:
                        all_results.append({
                            "id": match.id,
                            "score": match.score,
                            "metadata": match.metadata,
                            "text": match.metadata.get("full_text", match.metadata.get("text", ""))
                        })
            
            # Sort by score and return top results
            all_results.sort(key=lambda x: x["score"], reverse=True)
            return all_results[:top_k]
        except Exception as e:
            print(f"Error searching across projects: {str(e)}")
            return []
    
    def delete_document(self, project_id: str, document_id: str) -> bool:
        """Delete all chunks for a specific document"""
        try:
            namespace = f"project_{project_id}"
            
            # Get all vector IDs for this document
            # We need to query to find all chunks for this document
            # This is a limitation of Pinecone - we can't easily get all IDs
            # So we'll use a metadata filter instead
            
            # For now, we'll implement a simple approach
            # In production, you might want to keep track of vector IDs separately
            print(f"Deleting document {document_id} from project {project_id}")
            
            # Pinecone doesn't support deletion by metadata filter directly
            # You would need to query first to get IDs, then delete
            # This is a simplified implementation
            return True
        except Exception as e:
            print(f"Error deleting document: {str(e)}")
            return False
    
    def delete_project_namespace(self, project_id: str) -> bool:
        """Delete entire project namespace"""
        try:
            namespace = f"project_{project_id}"
            # Note: Pinecone doesn't have a direct way to delete namespace
            # You would need to delete all vectors in the namespace
            # This is a placeholder implementation
            print(f"Deleting project namespace: {namespace}")
            return True
        except Exception as e:
            print(f"Error deleting project namespace: {str(e)}")
            return False
    
    def get_project_stats(self, project_id: str) -> Dict:
        """Get statistics for a project's vectors"""
        try:
            namespace = f"project_{project_id}"
            stats = self.index.describe_index_stats()
            
            if stats.namespaces and namespace in stats.namespaces:
                return {
                    "vector_count": stats.namespaces[namespace].vector_count,
                    "namespace": namespace
                }
            else:
                return {"vector_count": 0, "namespace": namespace}
        except Exception as e:
            print(f"Error getting project stats: {str(e)}")
            return {"vector_count": 0, "namespace": f"project_{project_id}"}

# Global service instance
try:
    pinecone_service = PineconeService()
except Exception as e:
    print(f"Warning: Could not initialize Pinecone service: {e}")
    pinecone_service = None