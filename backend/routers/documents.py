from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List
from backend.models import Document
from backend.database import db
from backend.services.processor import document_processor
from shared.config import Config

router = APIRouter(prefix="/api/projects/{project_id}/documents", tags=["documents"])

@router.post("/upload", response_model=Document)
async def upload_document(project_id: str, file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Check if project exists
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Check file count limit
        existing_docs = await db.get_documents_by_project(project_id)
        if len(existing_docs) >= Config.MAX_FILES_PER_PROJECT:
            raise HTTPException(
                status_code=400, 
                detail=f"Maximum {Config.MAX_FILES_PER_PROJECT} files per project allowed"
            )
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validate file
        is_valid, error_message = document_processor.validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Create document record
        document = Document.create_new(
            project_id=project_id,
            filename=file.filename,
            file_type=file.filename.split('.')[-1].lower(),
            file_size=file_size
        )
        
        # Save to database first
        created_document = await db.create_document(document)
        
        # Process document (extract text, create embeddings, store in vector DB)
        processing_success = await document_processor.process_document(
            file_content=file_content,
            filename=file.filename,
            project_id=project_id,
            document=created_document
        )
        
        if not processing_success:
            # If processing fails, delete the document record
            await db.delete_document(created_document.id)
            raise HTTPException(status_code=500, detail="Failed to process document")
        
        return created_document
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")

@router.get("/", response_model=List[Document])
async def get_project_documents(project_id: str):
    """Get all documents for a project"""
    try:
        # Check if project exists
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        documents = await db.get_documents_by_project(project_id)
        return documents
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")

@router.get("/{document_id}", response_model=Document)
async def get_document(project_id: str, document_id: str):
    """Get a specific document"""
    try:
        document = await db.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Verify document belongs to the project
        if document.project_id != project_id:
            raise HTTPException(status_code=404, detail="Document not found in this project")
        
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch document: {str(e)}")

@router.delete("/{document_id}")
async def delete_document(project_id: str, document_id: str):
    """Delete a document"""
    try:
        # Check if document exists and belongs to project
        document = await db.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if document.project_id != project_id:
            raise HTTPException(status_code=404, detail="Document not found in this project")
        
        # Delete from database
        success = await db.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete document")
        
        # TODO: Delete from Pinecone vector database
        # pinecone_service.delete_document(project_id, document_id)
        
        return {"message": "Document deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@router.post("/bulk-upload")
async def bulk_upload_documents(project_id: str, files: List[UploadFile] = File(...)):
    """Upload multiple documents at once"""
    try:
        # Check if project exists
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Check total file count
        existing_docs = await db.get_documents_by_project(project_id)
        total_files = len(existing_docs) + len(files)
        
        if total_files > Config.MAX_FILES_PER_PROJECT:
            raise HTTPException(
                status_code=400, 
                detail=f"Total files would exceed maximum {Config.MAX_FILES_PER_PROJECT} files per project"
            )
        
        successful_uploads = []
        failed_uploads = []
        
        for file in files:
            try:
                file_content = await file.read()
                file_size = len(file_content)
                
                # Validate file
                is_valid, error_message = document_processor.validate_file(file.filename, file_size)
                if not is_valid:
                    failed_uploads.append({"filename": file.filename, "error": error_message})
                    continue
                
                # Create document record
                document = Document.create_new(
                    project_id=project_id,
                    filename=file.filename,
                    file_type=file.filename.split('.')[-1].lower(),
                    file_size=file_size
                )
                
                # Save to database
                created_document = await db.create_document(document)
                
                # Process document
                processing_success = await document_processor.process_document(
                    file_content=file_content,
                    filename=file.filename,
                    project_id=project_id,
                    document=created_document
                )
                
                if processing_success:
                    successful_uploads.append(created_document)
                else:
                    await db.delete_document(created_document.id)
                    failed_uploads.append({"filename": file.filename, "error": "Processing failed"})
                
            except Exception as e:
                failed_uploads.append({"filename": file.filename, "error": str(e)})
        
        return {
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads,
            "total_successful": len(successful_uploads),
            "total_failed": len(failed_uploads)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to bulk upload documents: {str(e)}")