import os
import io
from typing import List, Tuple
from pathlib import Path
import PyPDF2
from docx import Document as DocxDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.services.gemini_service import gemini_service
from backend.services.pinecone_service import pinecone_service
from backend.models import Document
from shared.config import Config

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    async def process_document(
        self, 
        file_content: bytes, 
        filename: str, 
        project_id: str,
        document: Document
    ) -> bool:
        """Process a document: extract text, chunk it, generate embeddings, and store in vector DB"""
        try:
            # Extract text based on file type
            text = self._extract_text(file_content, filename)
            
            if not text.strip():
                print(f"No text extracted from {filename}")
                return False
            
            # TODO: TASK 1 - DOCUMENT SPLITTING/CHUNKING  
            # Students need to implement intelligent text chunking
            # This is the "Split" step in the RAG pipeline
            
            # TODO: Implement smart text chunking
            # Instructions:
            # 1. Split the extracted text into smaller, manageable chunks
            # 2. Use sentence-aware chunking (don't break in middle of sentences)
            # 3. Add overlap between chunks for context continuity
            # 4. Optimize chunk size for embedding models (typically 500-1000 chars)
            # 5. Handle edge cases like very short documents
            #
            # The RecursiveCharacterTextSplitter is already initialized with:
            # - chunk_size: Maximum characters per chunk
            # - chunk_overlap: Characters to overlap between chunks  
            # - separators: Priority order for splitting ["\n\n", "\n", " ", ""]
            #
            # Expected behavior:
            # - Input: Full document text as single string
            # - Output: List of text chunks, each with reasonable size
            # - Each chunk should be semantically meaningful
            # - Chunks should have some overlap to maintain context
            
            assert text and text.strip(), "Text must not be empty for chunking"
            
            # TODO: Replace this placeholder with actual chunking logic
            chunks = ["TODO: Implement chunking logic"]
            
            # Validation check for students
            assert chunks and len(chunks) > 0, "Chunking failed - no chunks were created"
            assert chunks[0] != "TODO: Implement chunking logic", "Students must implement chunking logic"
            
            if not chunks:
                print(f"No chunks created from {filename}")
                return False
            
            # Generate embeddings for chunks
            embeddings = []
            for chunk in chunks:
                embedding = gemini_service.generate_embedding(chunk)
                if embedding:
                    embeddings.append(embedding)
                else:
                    print(f"Failed to generate embedding for chunk in {filename}")
                    return False
            
            # Store in Pinecone
            if pinecone_service:
                success = pinecone_service.upsert_document_chunks(
                    project_id=project_id,
                    document_id=document.id,
                    filename=filename,
                    chunks=chunks,
                    embeddings=embeddings
                )
                
                if not success:
                    print(f"Failed to store chunks in Pinecone for {filename}")
                    return False
            
            print(f"Successfully processed {filename} with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error processing document {filename}: {str(e)}")
            return False
    
    def _extract_text(self, file_content: bytes, filename: str) -> str:
        """Extract text from different file types"""
        # TODO: TASK 1 - DOCUMENT LOADING & TEXT EXTRACTION
        # Students need to implement the text extraction logic for different file types
        # This is the "Load" step in the RAG pipeline
        
        file_extension = Path(filename).suffix.lower()
        
        # TODO: Implement text extraction for PDF, DOCX, and TXT files
        # Instructions:
        # 1. For PDF files: Use PyPDF2 to extract text from all pages
        # 2. For DOCX files: Use python-docx to extract text from all paragraphs  
        # 3. For TXT files: Decode bytes to text with proper encoding handling
        # 4. Handle errors gracefully and return empty string on failure
        # 5. Each method should return a single string with all extracted text
        #
        # Hint: The helper methods _extract_pdf_text, _extract_docx_text, and 
        # _extract_txt_text are already defined below. You need to call them here.
        #
        # Expected behavior:
        # - PDF: Extract text from all pages, join with newlines
        # - DOCX: Extract text from all paragraphs, join with newlines  
        # - TXT: Handle different encodings (utf-8, utf-16, latin-1)
        # - Return empty string if extraction fails
        
        assert file_extension in ['.pdf', '.docx', '.txt'], f"Unsupported file type: {file_extension}"
        
        try:
            # TODO: Add your implementation here
            # Remove this placeholder return and implement the logic
            return "TODO: Implement text extraction logic"
            
        except Exception as e:
            print(f"Error extracting text from {filename}: {str(e)}")
            return ""
    
    def _extract_pdf_text(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            print(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def _extract_docx_text(self, file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docx_file = io.BytesIO(file_content)
            doc = DocxDocument(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
        except Exception as e:
            print(f"Error extracting DOCX text: {str(e)}")
            return ""
    
    def _extract_txt_text(self, file_content: bytes) -> str:
        """Extract text from TXT file"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    return file_content.decode(encoding)
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, use utf-8 with error handling
            return file_content.decode('utf-8', errors='replace')
        except Exception as e:
            print(f"Error extracting TXT text: {str(e)}")
            return ""
    
    def validate_file(self, filename: str, file_size: int) -> Tuple[bool, str]:
        """Validate uploaded file"""
        # Check file extension
        file_extension = Path(filename).suffix.lower()
        if file_extension not in Config.ALLOWED_EXTENSIONS:
            return False, f"File type {file_extension} not allowed. Allowed types: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        
        # Check file size
        if file_size > Config.MAX_FILE_SIZE:
            max_size_mb = Config.MAX_FILE_SIZE / (1024 * 1024)
            return False, f"File size exceeds {max_size_mb}MB limit"
        
        return True, "File is valid"
    
    async def get_document_summary(self, chunks: List[str], filename: str) -> str:
        """Generate a summary of the document"""
        try:
            # Combine first few chunks for summary (to avoid token limits)
            content = "\n\n".join(chunks[:5])  # Use first 5 chunks
            
            summary = await gemini_service.generate_response(
                f"Please provide a brief summary of this document '{filename}':\n\n{content}"
            )
            
            return summary
        except Exception as e:
            return f"Could not generate summary: {str(e)}"

# Global processor instance
document_processor = DocumentProcessor()