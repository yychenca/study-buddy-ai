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
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return []
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embeddings for search queries"""
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
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