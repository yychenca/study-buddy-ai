# Local NotebookLM Clone - Project Requirements

## 🎯 Project Overview

**Project Name:** StudyBuddy AI  
**Description:** A local web application that allows users to create projects, upload documents to them, and have intelligent AI-powered conversations about their content - similar to Google's NotebookLM but running locally.

**Target Developer:** Teenage coder with basic Python knowledge  
**Estimated Development Time:** 3-4 weeks (faster with Python-only stack)

---

## 🚀 Core Features

### MVP (Minimum Viable Product) Features

1. **Project Management**
   - Create, rename, and delete projects
   - Organize documents within projects
   - Switch between projects easily
   - Project-level chat history

2. **Document Upload & Processing**
   - Support for PDF, TXT, and DOCX files
   - Drag-and-drop interface per project
   - Multi-file upload (up to 20 documents per project)
   - Document preview within projects

3. **AI-Powered Analysis**
   - Project-wide document analysis
   - Automatic summarization of all project documents
   - Q&A interface scoped to current project
   - Cross-document insights within a project

4. **Vector Search**
   - Search within current project or across all projects
   - Semantic search with relevance scoring
   - Filter results by document or date

5. **User Interface**
   - Clean, modern Python-based UI
   - Project sidebar navigation
   - Real-time chat interface
   - Dark/light mode toggle

### Future Features (Phase 2)
- Export project as study guide
- Share projects via link
- Audio summaries per project
- Collaborative project editing
- Project templates

---

## 🛠️ Technical Stack (Python-Only!)

### Backend
- **Framework:** FastAPI
- **LLM Integration:** Google Gemini API
- **Vector Database:** Pinecone.io
- **Database:** SQLite (for projects/documents metadata)
- **Document Processing:** 
  - PyPDF2 (for PDFs)
  - python-docx (for Word docs)
  - langchain (for text splitting)

### Frontend
- **Framework:** Streamlit (easiest for beginners!)
- **Alternative Options:**
  - Gradio (for more AI-focused UI)
  - NiceGUI (for more control)
  - FastAPI + Jinja2 templates (traditional approach)

### Why Streamlit?
- Pure Python - no HTML/CSS/JS needed!
- Built-in components for file upload, chat, sidebars
- Hot-reload during development
- Easy deployment options
- Great for data/AI applications

---

## 📋 Detailed Requirements

### 1. Project Structure

```python
# Project Model
class Project:
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    document_count: int
    
# Document Model
class Document:
    id: str
    project_id: str
    filename: str
    file_type: str
    upload_date: datetime
    content_hash: str
    chunk_ids: List[str]  # Pinecone vector IDs
```

### 2. Database Schema (SQLite)

```sql
-- Projects table
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Documents table
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    filename TEXT,
    file_type TEXT,
    file_size INTEGER,
    upload_date TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);

-- Chat history table
CREATE TABLE chat_history (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    message TEXT,
    response TEXT,
    timestamp TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
```

### 3. Streamlit UI Structure

```python
# Main app layout
st.set_page_config(page_title="StudyBuddy AI", layout="wide")

# Sidebar for project management
with st.sidebar:
    st.title("📚 Projects")
    
    # Project selector
    selected_project = st.selectbox(
        "Select Project",
        options=get_all_projects()
    )
    
    # New project button
    if st.button("➕ New Project"):
        show_new_project_dialog()
    
    # Project stats
    st.metric("Documents", get_doc_count(selected_project))
    st.metric("Total Chats", get_chat_count(selected_project))

# Main area
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📄 Documents", "🔍 Search"])

with tab1:
    # Chat interface
    show_chat_interface(selected_project)

with tab2:
    # Document management
    show_document_manager(selected_project)
    
with tab3:
    # Search interface
    show_search_interface(selected_project)
```

### 4. API Structure

```python
# Core API endpoints (FastAPI backend)
@app.post("/api/projects")
async def create_project(project: ProjectCreate)

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str)

@app.post("/api/projects/{project_id}/documents")
async def upload_document(project_id: str, file: UploadFile)

@app.post("/api/projects/{project_id}/chat")
async def chat_in_project(project_id: str, message: ChatMessage)

@app.post("/api/projects/{project_id}/search")
async def search_project(project_id: str, query: SearchQuery)
```

### 5. Pinecone Organization

```python
# Namespace structure in Pinecone
# Each project gets its own namespace
namespace = f"project_{project_id}"

# Metadata structure for vectors
metadata = {
    "project_id": project_id,
    "document_id": document_id,
    "filename": filename,
    "chunk_index": chunk_index,
    "text": chunk_text[:1000],  # First 1000 chars for preview
    "timestamp": upload_timestamp
}
```

---

## 🏗️ System Architecture

```
┌─────────────────────┐
│  Streamlit Frontend │
│  (Pure Python UI)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌─────────────────┐
│  FastAPI Backend    │────▶│   Gemini API    │
│  - Project Logic    │     └─────────────────┘
│  - Document Process │              │
│  - Chat Management  │              ▼
└──────────┬──────────┘     ┌─────────────────┐
           │                 │ Text Embeddings │
           ▼                 └─────────────────┘
┌─────────────────────┐              │
│   SQLite Database   │              ▼
│  - Projects         │     ┌─────────────────┐
│  - Documents        │     │    Pinecone     │
│  - Chat History     │     │ (Namespaced by  │
└─────────────────────┘     │    Project)     │
                            └─────────────────┘
```

---

## 🚦 Getting Started Guide

### Prerequisites
- Python 3.9+ installed
- Basic Python knowledge
- Google Cloud account (for Gemini API)
- Pinecone account (free tier available)

### Step-by-Step Setup

1. **Clone the starter template**
```bash
git clone https://github.com/your-username/studybuddy-python
cd studybuddy-python
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install streamlit fastapi uvicorn
pip install google-generativeai pinecone-client
pip install pypdf2 python-docx langchain
pip install sqlite3 python-multipart
```

4. **Environment setup**
Create `.env` file:
```
GEMINI_API_KEY=your_gemini_key
PINECONE_API_KEY=your_pinecone_key
SECRET_KEY=your_secret_key
DATABASE_PATH=./studybuddy.db
```

5. **Initialize database**
```bash
python scripts/init_db.py
```

6. **Run the application**
```bash
# Terminal 1 - Backend API
uvicorn backend.main:app --reload --port 8000

# Terminal 2 - Streamlit Frontend
streamlit run frontend/app.py
```

---

## 📁 Project Structure

```
studybuddy-python/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── models.py               # Data models
│   ├── database.py             # SQLite connection
│   ├── routers/
│   │   ├── projects.py         # Project endpoints
│   │   ├── documents.py        # Document endpoints
│   │   └── chat.py            # Chat endpoints
│   └── services/
│       ├── gemini_service.py   # Gemini integration
│       ├── pinecone_service.py # Pinecone integration
│       └── processor.py        # Document processing
├── frontend/
│   ├── app.py                  # Main Streamlit app
│   ├── pages/
│   │   ├── project_manager.py  # Project UI
│   │   ├── chat_interface.py   # Chat UI
│   │   └── search_page.py      # Search UI
│   └── components/
│       ├── file_uploader.py    # Upload component
│       └── chat_widget.py      # Chat component
├── shared/
│   └── config.py               # Shared configuration
├── scripts/
│   └── init_db.py             # Database initialization
└── requirements.txt
```

---

## 💻 Sample Code

### Streamlit Chat Interface
```python
# frontend/pages/chat_interface.py
import streamlit as st
import requests

def show_chat_interface(project_id):
    st.header(f"💬 Chat - {get_project_name(project_id)}")
    
    # Initialize chat history in session state
    if f"messages_{project_id}" not in st.session_state:
        st.session_state[f"messages_{project_id}"] = []
    
    # Display chat history
    for message in st.session_state[f"messages_{project_id}"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your documents..."):
        # Add user message
        st.session_state[f"messages_{project_id}"].append(
            {"role": "user", "content": prompt}
        )
        
        # Get AI response
        with st.spinner("Thinking..."):
            response = requests.post(
                f"http://localhost:8000/api/projects/{project_id}/chat",
                json={"message": prompt}
            )
            
        # Add AI response
        if response.ok:
            ai_response = response.json()["response"]
            st.session_state[f"messages_{project_id}"].append(
                {"role": "assistant", "content": ai_response}
            )
            st.rerun()
```

### Document Processing
```python
# backend/services/processor.py
async def process_document(project_id: str, file: UploadFile):
    # Extract text based on file type
    if file.filename.endswith('.pdf'):
        text = extract_pdf_text(file)
    elif file.filename.endswith('.docx'):
        text = extract_docx_text(file)
    else:
        text = await file.read()
    
    # Split into chunks
    chunks = split_text(text, chunk_size=1000)
    
    # Generate embeddings and store in Pinecone
    for i, chunk in enumerate(chunks):
        embedding = gemini_service.generate_embedding(chunk)
        
        pinecone_service.upsert(
            namespace=f"project_{project_id}",
            vectors=[(
                f"{file.filename}_{i}",
                embedding,
                {
                    "project_id": project_id,
                    "filename": file.filename,
                    "chunk_index": i,
                    "text": chunk[:1000]
                }
            )]
        )
```

---

## 🎯 Development Milestones

### Week 1: Foundation
- [ ] Set up project structure
- [ ] Create database schema
- [ ] Basic Streamlit UI with project sidebar
- [ ] FastAPI backend skeleton

### Week 2: Core Features
- [ ] Project CRUD operations
- [ ] Document upload and processing
- [ ] Pinecone integration with namespaces
- [ ] Basic Gemini chat integration

### Week 3: Advanced Features
- [ ] Project-scoped search
- [ ] Chat history persistence
- [ ] Document management UI
- [ ] Cross-document insights

### Week 4: Polish
- [ ] Error handling
- [ ] Loading states
- [ ] UI improvements
- [ ] Deployment setup

---

## 💡 Tips for Teen Developers

### Python-Specific Tips
1. **Use Type Hints**: Makes code clearer
   ```python
   def process_document(file: UploadFile) -> str:
   ```

2. **Streamlit Session State**: Perfect for managing UI state
   ```python
   if "counter" not in st.session_state:
       st.session_state.counter = 0
   ```

3. **Async/Await**: FastAPI uses async functions
   ```python
   async def upload_file(file: UploadFile):
       contents = await file.read()
   ```

4. **Virtual Environments**: Always use them!
   ```bash
   python -m venv venv
   ```

5. **Debug with st.write()**: Streamlit's version of print()
   ```python
   st.write("Debug:", variable)
   ```

---

## 🚀 Deployment Options

### Easiest for Python Apps
1. **Streamlit Cloud**: Free hosting for Streamlit apps
2. **Hugging Face Spaces**: Great for AI apps
3. **Railway**: Simple Python app deployment
4. **Local with ngrok**: For sharing locally

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "frontend/app.py"]
```

---

## 🔒 Security & Performance

### Security
- API key management with environment variables
- File type validation
- Size limits on uploads
- SQL injection prevention (use parameterized queries)
- Rate limiting on API endpoints

### Performance
- Lazy load documents in UI
- Cache Gemini responses
- Batch process embeddings
- Use Streamlit's `@st.cache_data` decorator

---

## 📚 Learning Resources

### Python & Streamlit
1. **Streamlit Documentation**: https://docs.streamlit.io
2. **FastAPI Tutorial**: https://fastapi.tiangolo.com
3. **Real Python**: https://realpython.com
4. **Streamlit Gallery**: https://streamlit.io/gallery

### AI & Vector Databases
1. **Gemini Quickstart**: https://ai.google.dev/tutorials/python_quickstart
2. **Pinecone Python Client**: https://docs.pinecone.io/docs/python-client
3. **LangChain Docs**: https://python.langchain.com

---

## 🎉 Success Criteria

Your StudyBuddy AI is successful when:
- ✅ Users can create and manage multiple projects
- ✅ Documents are organized within projects
- ✅ AI can answer questions about project documents
- ✅ Search works within and across projects
- ✅ The UI is clean and responsive
- ✅ Everything runs in Python!
- ✅ You've built something awesome!

Remember: Python makes everything easier! Start simple, iterate often, and have fun building! 🐍✨