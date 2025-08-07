from fastapi import APIRouter, HTTPException
from typing import List
from backend.models import Project, ProjectCreate, ProjectStats
from backend.database import db

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/", response_model=Project)
async def create_project(project_data: ProjectCreate):
    """Create a new project"""
    try:
        project = Project.create_new(
            name=project_data.name,
            description=project_data.description
        )
        created_project = await db.create_project(project)
        return created_project
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@router.get("/", response_model=List[Project])
async def get_all_projects():
    """Get all projects"""
    try:
        projects = await db.get_all_projects()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {str(e)}")

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """Get a specific project"""
    try:
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch project: {str(e)}")

@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: str, project_data: ProjectCreate):
    """Update a project"""
    try:
        # Check if project exists
        existing_project = await db.get_project(project_id)
        if not existing_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        updated_project = await db.update_project(
            project_id=project_id,
            name=project_data.name,
            description=project_data.description
        )
        
        if not updated_project:
            raise HTTPException(status_code=500, detail="Failed to update project")
        
        return updated_project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Delete a project and all its documents"""
    try:
        # Check if project exists
        existing_project = await db.get_project(project_id)
        if not existing_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Delete from database (cascades to documents and chat history)
        success = await db.delete_project(project_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete project")
        
        # TODO: Also delete from Pinecone (namespace cleanup)
        # pinecone_service.delete_project_namespace(project_id)
        
        return {"message": "Project deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")

@router.get("/{project_id}/stats", response_model=ProjectStats)
async def get_project_stats(project_id: str):
    """Get project statistics"""
    try:
        # Check if project exists
        existing_project = await db.get_project(project_id)
        if not existing_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        stats = await db.get_project_stats(project_id)
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch project stats: {str(e)}")