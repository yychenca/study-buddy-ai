from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from backend.routers import projects, documents, chat
from shared.config import Config

# Create FastAPI app
app = FastAPI(
    title="StudyBuddy AI API",
    description="Local NotebookLM clone API for document analysis and AI-powered conversations",
    version="1.0.0"
)

# Add CORS middleware to allow Streamlit frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(documents.router)
app.include_router(chat.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "StudyBuddy AI API is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "gemini_api": "configured" if Config.GEMINI_API_KEY else "not configured",
        "pinecone_api": "configured" if Config.PINECONE_API_KEY else "not configured"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=True
    )