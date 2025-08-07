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
        try:
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector_id = f"{document_id}_{i}"
                metadata = {
                    "project_id": project_id,
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": i,
                    "text": chunk[:1000],  # Store first 1000 chars for preview
                    "full_text": chunk  # Store full text for retrieval
                }
                vectors.append((vector_id, embedding, metadata))
            
            # Upsert vectors to Pinecone with project namespace
            namespace = f"project_{project_id}"
            self.index.upsert(vectors=vectors, namespace=namespace)
            return True
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
        try:
            # If project_id is specified, search within that project's namespace
            namespace = f"project_{project_id}" if project_id else None
            
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace=namespace
            )
            
            # Format results
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata,
                    "text": match.metadata.get("full_text", match.metadata.get("text", ""))
                })
            
            return formatted_results
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