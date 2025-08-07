import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    
    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./studybuddy.db")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # API Settings
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # File Upload Settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_FILES_PER_PROJECT = 20
    ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}
    
    # Vector Database Settings
    VECTOR_DIMENSION = 768  # Gemini embedding dimension
    
    # Text Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200