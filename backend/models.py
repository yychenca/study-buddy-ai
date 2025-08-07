from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import uuid

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create_new(cls, name: str, description: Optional[str] = None):
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

class DocumentBase(BaseModel):
    filename: str
    file_type: str
    file_size: int

class DocumentCreate(DocumentBase):
    project_id: str

class Document(DocumentBase):
    id: str
    project_id: str
    upload_date: datetime
    
    @classmethod
    def create_new(cls, project_id: str, filename: str, file_type: str, file_size: int):
        return cls(
            id=str(uuid.uuid4()),
            project_id=project_id,
            filename=filename,
            file_type=file_type,
            file_size=file_size,
            upload_date=datetime.now()
        )

class ChatMessageBase(BaseModel):
    message: str

class ChatMessage(ChatMessageBase):
    project_id: str

class ChatHistoryBase(BaseModel):
    message: str
    response: str

class ChatHistory(ChatHistoryBase):
    id: str
    project_id: str
    timestamp: datetime
    
    @classmethod
    def create_new(cls, project_id: str, message: str, response: str):
        return cls(
            id=str(uuid.uuid4()),
            project_id=project_id,
            message=message,
            response=response,
            timestamp=datetime.now()
        )

class SearchQuery(BaseModel):
    query: str
    project_id: Optional[str] = None  # If None, search across all projects

class SearchResult(BaseModel):
    document_id: str
    filename: str
    project_id: str
    content_snippet: str
    relevance_score: float

class ProjectStats(BaseModel):
    document_count: int
    chat_count: int
    last_activity: Optional[datetime] = None