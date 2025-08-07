import sqlite3
import aiosqlite
from typing import List, Optional
from datetime import datetime
from backend.models import Project, Document, ChatHistory, ProjectStats
from shared.config import Config

class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
    
    async def get_connection(self):
        """Get async database connection"""
        return await aiosqlite.connect(self.db_path)
    
    # Project CRUD operations
    async def create_project(self, project: Project) -> Project:
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute(
                "INSERT INTO projects (id, name, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (project.id, project.name, project.description, project.created_at, project.updated_at)
            )
            await conn.commit()
            return project
    
    async def get_project(self, project_id: str) -> Optional[Project]:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT id, name, description, created_at, updated_at FROM projects WHERE id = ?",
                (project_id,)
            )
            row = await cursor.fetchone()
            if row:
                return Project(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    created_at=datetime.fromisoformat(row[3]),
                    updated_at=datetime.fromisoformat(row[4])
                )
            return None
    
    async def get_all_projects(self) -> List[Project]:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT id, name, description, created_at, updated_at FROM projects ORDER BY updated_at DESC"
            )
            rows = await cursor.fetchall()
            return [
                Project(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    created_at=datetime.fromisoformat(row[3]),
                    updated_at=datetime.fromisoformat(row[4])
                )
                for row in rows
            ]
    
    async def update_project(self, project_id: str, name: str = None, description: str = None) -> Optional[Project]:
        async with aiosqlite.connect(self.db_path) as conn:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            
            if updates:
                updates.append("updated_at = ?")
                params.append(datetime.now().isoformat())
                params.append(project_id)
                
                await conn.execute(
                    f"UPDATE projects SET {', '.join(updates)} WHERE id = ?",
                    params
                )
                await conn.commit()
            
            return await self.get_project(project_id)
    
    async def delete_project(self, project_id: str) -> bool:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            await conn.commit()
            return cursor.rowcount > 0
    
    # Document CRUD operations
    async def create_document(self, document: Document) -> Document:
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute(
                "INSERT INTO documents (id, project_id, filename, file_type, file_size, upload_date) VALUES (?, ?, ?, ?, ?, ?)",
                (document.id, document.project_id, document.filename, document.file_type, document.file_size, document.upload_date)
            )
            await conn.commit()
            return document
    
    async def get_documents_by_project(self, project_id: str) -> List[Document]:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT id, project_id, filename, file_type, file_size, upload_date FROM documents WHERE project_id = ? ORDER BY upload_date DESC",
                (project_id,)
            )
            rows = await cursor.fetchall()
            return [
                Document(
                    id=row[0],
                    project_id=row[1],
                    filename=row[2],
                    file_type=row[3],
                    file_size=row[4],
                    upload_date=datetime.fromisoformat(row[5])
                )
                for row in rows
            ]
    
    async def get_document(self, document_id: str) -> Optional[Document]:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT id, project_id, filename, file_type, file_size, upload_date FROM documents WHERE id = ?",
                (document_id,)
            )
            row = await cursor.fetchone()
            if row:
                return Document(
                    id=row[0],
                    project_id=row[1],
                    filename=row[2],
                    file_type=row[3],
                    file_size=row[4],
                    upload_date=datetime.fromisoformat(row[5])
                )
            return None
    
    async def delete_document(self, document_id: str) -> bool:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))
            await conn.commit()
            return cursor.rowcount > 0
    
    # Chat history CRUD operations
    async def create_chat_history(self, chat: ChatHistory) -> ChatHistory:
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute(
                "INSERT INTO chat_history (id, project_id, message, response, timestamp) VALUES (?, ?, ?, ?, ?)",
                (chat.id, chat.project_id, chat.message, chat.response, chat.timestamp)
            )
            await conn.commit()
            return chat
    
    async def get_chat_history(self, project_id: str, limit: int = 50) -> List[ChatHistory]:
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT id, project_id, message, response, timestamp FROM chat_history WHERE project_id = ? ORDER BY timestamp DESC LIMIT ?",
                (project_id, limit)
            )
            rows = await cursor.fetchall()
            return [
                ChatHistory(
                    id=row[0],
                    project_id=row[1],
                    message=row[2],
                    response=row[3],
                    timestamp=datetime.fromisoformat(row[4])
                )
                for row in reversed(rows)  # Reverse to get chronological order
            ]
    
    async def get_project_stats(self, project_id: str) -> ProjectStats:
        async with aiosqlite.connect(self.db_path) as conn:
            # Get document count
            doc_cursor = await conn.execute(
                "SELECT COUNT(*) FROM documents WHERE project_id = ?",
                (project_id,)
            )
            doc_count = (await doc_cursor.fetchone())[0]
            
            # Get chat count
            chat_cursor = await conn.execute(
                "SELECT COUNT(*) FROM chat_history WHERE project_id = ?",
                (project_id,)
            )
            chat_count = (await chat_cursor.fetchone())[0]
            
            # Get last activity
            activity_cursor = await conn.execute(
                """
                SELECT MAX(timestamp) FROM (
                    SELECT upload_date as timestamp FROM documents WHERE project_id = ?
                    UNION ALL
                    SELECT timestamp FROM chat_history WHERE project_id = ?
                )
                """,
                (project_id, project_id)
            )
            last_activity_str = (await activity_cursor.fetchone())[0]
            last_activity = datetime.fromisoformat(last_activity_str) if last_activity_str else None
            
            return ProjectStats(
                document_count=doc_count,
                chat_count=chat_count,
                last_activity=last_activity
            )

# Global database instance
db = Database()