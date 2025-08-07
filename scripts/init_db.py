import sqlite3
import os
from datetime import datetime

def init_database(db_path: str = "studybuddy.db"):
    """Initialize the SQLite database with required tables."""
    
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        )
    """)
    
    # Create chat_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        )
    """)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_documents_project_id ON documents(project_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_history_project_id ON chat_history(project_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_history_timestamp ON chat_history(timestamp)")
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized successfully at: {db_path}")

if __name__ == "__main__":
    init_database()