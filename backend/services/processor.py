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
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
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
        file_extension = Path(filename).suffix.lower()
        
        try:
            if file_extension == '.pdf':
                return self._extract_pdf_text(file_content)
            elif file_extension == '.docx':
                return self._extract_docx_text(file_content)
            elif file_extension == '.txt':
                return self._extract_txt_text(file_content)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
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