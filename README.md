# StudyBuddy AI 📚

A local NotebookLM clone built with Python! StudyBuddy AI helps you organize documents, extract insights, and have intelligent conversations about your content using AI.

## ✨ Features

- **📁 Project Management**: Organize documents into projects
- **📄 Document Upload**: Support for PDF, DOCX, and TXT files (up to 20 per project)
- **🤖 AI Chat**: Ask questions about your documents using Google Gemini
- **🔍 Smart Search**: Semantic search across projects using Pinecone
- **📊 Summaries**: Get automatic document summaries
- **💾 Local Storage**: All data stored locally in SQLite

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Pure Python UI!)
- **Backend**: FastAPI
- **AI**: Google Gemini API
- **Vector Database**: Pinecone
- **Database**: SQLite
- **Document Processing**: PyPDF2, python-docx, LangChain

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key
- Pinecone account (free tier available)

### Installation

1. **Clone or download this project**
   ```bash
   cd studybuddy-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API keys:
   # GEMINI_API_KEY=your_gemini_key_here
   # PINECONE_API_KEY=your_pinecone_key_here
   ```

### Getting API Keys

#### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

#### Pinecone
1. Sign up at [Pinecone](https://www.pinecone.io/)
2. Create a new project
3. Get your API key from the dashboard
4. Copy to your `.env` file

### Running the Application

#### Option 1: Using Startup Scripts (Recommended)

1. **Start the backend:**
   ```bash
   python start_backend.py
   ```

2. **In a new terminal, start the frontend:**
   ```bash
   python start_frontend.py
   ```

#### Option 2: Manual Start

1. **Initialize database:**
   ```bash
   python scripts/init_db.py
   ```

2. **Start FastAPI backend:**
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

3. **Start Streamlit frontend:**
   ```bash
   streamlit run frontend/app.py
   ```

### Access the Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage Guide

### 1. Create a Project
- Open the app in your browser
- Click "➕ Create New Project" in the sidebar
- Give your project a name and description

### 2. Upload Documents
- Go to the "📄 Documents" tab
- Drag and drop or select files to upload
- Supported formats: PDF, DOCX, TXT (max 50MB each)

### 3. Chat with Your Documents
- Go to the "💬 Chat" tab
- Ask questions about your documents
- The AI will search through your content and provide relevant answers

### 4. Search Across Projects
- Use the "🔍 Search" tab
- Search within current project or across all projects
- Find relevant content using semantic search

## 📁 Project Structure

```
studybuddy-ai/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── models.py               # Data models
│   ├── database.py             # SQLite operations
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
│   └── pages/
│       ├── chat_interface.py   # Chat UI
│       ├── document_manager.py # Document UI
│       └── search_page.py      # Search UI
├── shared/
│   └── config.py               # Shared configuration
├── scripts/
│   └── init_db.py             # Database initialization
├── start_backend.py            # Backend startup script
├── start_frontend.py           # Frontend startup script
└── requirements.txt
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `PINECONE_API_KEY` | Pinecone API key | Yes |
| `PINECONE_ENV` | Pinecone environment | Yes |
| `DATABASE_PATH` | SQLite database path | No (default: ./studybuddy.db) |
| `API_HOST` | API host | No (default: localhost) |
| `API_PORT` | API port | No (default: 8000) |

### File Limits

- **Max files per project**: 20
- **Max file size**: 50MB
- **Supported formats**: PDF, DOCX, TXT

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'backend'"**
   - Make sure you're running from the project root directory
   - Check that your virtual environment is activated

2. **"Failed to connect to API"**
   - Ensure the backend is running on port 8000
   - Check that there are no firewall issues

3. **"Invalid API key"**
   - Verify your API keys in the `.env` file
   - Make sure there are no extra spaces or quotes

4. **Document upload fails**
   - Check file size (max 50MB)
   - Ensure file format is supported (PDF, DOCX, TXT)
   - Verify you haven't exceeded the 20 file limit per project

### Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Verify your `.env` file is properly configured
3. Make sure all dependencies are installed
4. Try restarting both backend and frontend

## 🚀 Development

### Adding New Features

1. **Backend**: Add new endpoints in `backend/routers/`
2. **Frontend**: Add new pages in `frontend/pages/`
3. **Models**: Update data models in `backend/models.py`
4. **Database**: Modify schema in `scripts/init_db.py`

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the UI
- Powered by [FastAPI](https://fastapi.tiangolo.com/) for the backend
- Uses [Google Gemini](https://ai.google.dev/) for AI capabilities
- Vector search powered by [Pinecone](https://www.pinecone.io/)

---

**Happy studying with StudyBuddy AI! 📚✨**