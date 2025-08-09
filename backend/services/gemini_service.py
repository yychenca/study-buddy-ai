import google.generativeai as genai
from typing import List, Optional
from shared.config import Config

class GeminiService:
    def __init__(self):
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-pro')
            self.embedding_model = genai.GenerativeModel('text-embedding-004')
        else:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    async def generate_response(self, prompt: str, context: List[str] = None) -> str:
        """Generate a response using Gemini model with optional context"""
        try:
            # Build the full prompt with context
            full_prompt = self._build_prompt_with_context(prompt, context)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for the given text"""
        # TODO: TASK 2 - EMBEDDING GENERATION
        # Students need to implement text-to-vector conversion
        # This is the "Embed" step in the RAG pipeline
        
        # TODO: Implement embedding generation using Google's Gemini embedding API
        # Instructions:
        # 1. Use genai.embed_content() to convert text to numerical vectors
        # 2. Use model "models/text-embedding-004" for best performance
        # 3. Set task_type="retrieval_document" for document chunks
        # 4. Handle API errors gracefully (network issues, rate limits, etc.)
        # 5. Return empty list [] on failure
        # 6. Validate that the input text is not empty
        #
        # API Documentation:
        # genai.embed_content(
        #     model="models/text-embedding-004",
        #     content=text,  # The text to embed
        #     task_type="retrieval_document"  # Optimizes for document retrieval
        # )
        #
        # Expected behavior:
        # - Input: Text string (document chunk)
        # - Output: List of floats (vector representation, typically 768 dimensions)
        # - Handle empty/None text inputs
        # - Log errors but don't crash the application
        
        assert text and isinstance(text, str), "Text input must be a non-empty string"
        assert text.strip(), "Text input cannot be just whitespace"
        
        try:
            # TODO: Replace this placeholder with actual embedding generation
            # Remove this line and implement the real logic
            return [0.0] * 768  # Placeholder - replace with real embeddings
            
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return []
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embeddings for search queries"""
        # TODO: TASK 2 - QUERY EMBEDDING GENERATION (Part of embedding task)
        # Students need to implement query-to-vector conversion for search
        # This is used in the "Retrieve" step of the RAG pipeline
        
        # TODO: Implement query embedding generation
        # Instructions:
        # 1. Similar to generate_embedding() but optimized for queries
        # 2. Use same model "models/text-embedding-004"
        # 3. Set task_type="retrieval_query" to optimize for search queries
        # 4. Handle errors gracefully and return empty list on failure
        # 5. Query embeddings should be in same vector space as document embeddings
        #
        # The difference between query and document embeddings:
        # - Document embeddings (task_type="retrieval_document"): For content to be searched
        # - Query embeddings (task_type="retrieval_query"): For search queries
        # - Both should be compatible for similarity search
        
        assert query and isinstance(query, str), "Query input must be a non-empty string"
        assert query.strip(), "Query input cannot be just whitespace"
        
        try:
            # TODO: Replace this placeholder with actual query embedding generation
            return [0.0] * 768  # Placeholder - replace with real embeddings
            
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            return []
    
    def _build_prompt_with_context(self, prompt: str, context: List[str] = None) -> str:
        """Build a prompt with document context"""
        if not context:
            return f"""
You are StudyBuddy AI, an intelligent assistant that helps users understand and analyze their documents.

User Question: {prompt}

Please provide a helpful and accurate response based on the question asked.
"""
        
        context_text = "\n\n".join([f"Document {i+1}:\n{doc}" for i, doc in enumerate(context)])
        
        return f"""
You are StudyBuddy AI, an intelligent assistant that helps users understand and analyze their documents.

Here are the relevant document excerpts for context:

{context_text}

User Question: {prompt}

Please provide a helpful and accurate response based on the provided documents. If the answer cannot be found in the documents, please say so clearly.
"""
    
    async def summarize_documents(self, document_contents: List[str], project_name: str = "this project") -> str:
        """Generate a summary of multiple documents"""
        try:
            # Combine documents with separators
            combined_content = "\n\n---\n\n".join(document_contents)
            
            prompt = f"""
Please provide a comprehensive summary of the documents in {project_name}. 

Documents content:
{combined_content}

Create a summary that includes:
1. Main topics covered
2. Key insights and findings
3. Important concepts or themes
4. Any notable conclusions or recommendations

Keep the summary informative but concise.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

# Global service instance
gemini_service = GeminiService()