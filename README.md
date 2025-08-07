# StudyBuddy AI 📚

StudyBuddy AI helps you organize documents, extract insights, and have intelligent conversations about your content using AI.

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

1. **Clone the repository**
   ```bash
   git clone https://github.com/yychenca/study-buddy-ai.git
   cd study-buddy-ai
   ```

2. **Create and activate conda environment**
   
   Create a new conda environment with Python 3.9+:
   ```bash
   conda create -n studybuddy python=3.9
   conda activate studybuddy
   ```
   
   **Alternative: Using existing Python installation**
   If you prefer to use pip and venv instead of conda:
   ```bash
   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux:
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   # On Windows:
   copy NUL .env
   
   # On macOS/Linux:
   touch .env
   ```
   
   Add your API keys to the `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_key_here
   PINECONE_API_KEY=your_pinecone_key_here
   PINECONE_ENV=your_pinecone_environment
   ```

### Getting API Keys

#### Google Gemini API (Detailed Setup)

1. **Create a Google Account** (if you don't have one)
   - Go to [accounts.google.com](https://accounts.google.com) and create an account

2. **Access Google AI Studio**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account

3. **Create API Key**
   - Click on "Get API key" in the left sidebar
   - Click "Create API key in new project" (or select an existing project)
   - Your API key will be generated automatically
   
4. **Copy the API Key**
   - Click the copy button next to your API key
   - **Important**: Store this key securely - you won't be able to see it again
   
5. **Add to Environment File**
   - Open your `.env` file in the project directory
   - Add your key: `GEMINI_API_KEY=your_actual_api_key_here`
   - **Do not** include quotes around the key

6. **Verify API Access**
   - The Gemini API has a generous free tier
   - Check your usage at [AI Studio](https://aistudio.google.com/)
   - Rate limits: 15 requests per minute, 1 million tokens per minute (free tier)

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

StudyBuddy AI provides an intuitive interface for organizing documents and having intelligent conversations about your content. Here's a detailed walkthrough:

### Getting Started

1. **Launch the Application**
   
   After installation, start both the backend and frontend:
   ```bash
   # Terminal 1: Start backend
   conda activate studybuddy  # or activate your environment
   python start_backend.py
   
   # Terminal 2: Start frontend (in a new terminal)
   conda activate studybuddy
   python start_frontend.py
   ```
   
   The application will open in your browser at `http://localhost:8501`

### Step-by-Step Usage

#### 1. Create Your First Project

When you first open StudyBuddy AI, you'll see the main interface with a sidebar on the left.

![Main Interface](screenshots/main-interface.png)
*The main StudyBuddy AI interface with project sidebar*

**To create a new project:**
- Click the "➕ Create New Project" button in the sidebar
- Enter a **Project Name** (e.g., "Machine Learning Course")
- Add a **Description** (e.g., "Notes and papers for CS229")
- Click "Create Project"

![Create Project](screenshots/create-project.png)
*Project creation dialog*

Your new project will appear in the sidebar and be automatically selected.

#### 2. Upload Documents

Once you have a project, you can start adding documents:

**Navigate to Documents:**
- Click on the "📄 Documents" tab in the main area
- You'll see the document upload interface

![Document Upload](screenshots/document-upload.png)
*Document upload interface with drag-and-drop functionality*

**Upload your files:**
- **Drag and drop** files directly onto the upload area, OR
- Click "Browse files" to select files from your computer
- **Supported formats**: PDF, DOCX, TXT files
- **File limits**: Up to 20 files per project, maximum 50MB per file

**After upload:**
- Files will be automatically processed and indexed
- You'll see a list of all uploaded documents
- Processing may take a few moments for large files

#### 3. Chat with Your Documents

This is where StudyBuddy AI shines - intelligent conversations about your content:

**Start a conversation:**
- Go to the "💬 Chat" tab
- You'll see a chat interface similar to ChatGPT

![Chat Interface](screenshots/chat-interface.png)
*Chat interface showing conversation with your documents*

**Ask questions about your documents:**
- Type questions in natural language
- Examples:
  - "What are the main concepts covered in these papers?"
  - "Explain the difference between supervised and unsupervised learning"
  - "Summarize the key findings from the research paper"
  - "What examples are given for neural networks?"

**How it works:**
- StudyBuddy AI searches through your uploaded documents
- It finds relevant sections and passages
- Provides answers with context from your specific documents
- You can have follow-up conversations to dive deeper

#### 4. Smart Search Across Projects

Use the semantic search feature to find specific information:

**Access Search:**
- Click on the "🔍 Search" tab
- Enter your search query

![Search Interface](screenshots/search-interface.png)
*Search interface with semantic search results*

**Search options:**
- **Current Project**: Search only within the currently selected project
- **All Projects**: Search across all your projects simultaneously

**Search capabilities:**
- **Semantic search**: Finds content by meaning, not just exact keywords
- **Context-aware**: Understands the context of your query
- **Ranked results**: Shows most relevant content first

#### 5. Managing Projects

**Switch between projects:**
- Use the project selector in the sidebar
- Each project maintains its own documents and chat history

![Project Sidebar](screenshots/project-sidebar.png)
*Project sidebar showing multiple organized projects*

**Project organization tips:**
- Create separate projects for different subjects or topics
- Use descriptive names and descriptions
- Keep related documents together in the same project

### Best Practices

1. **Document Organization**
   - Group related documents in the same project
   - Use clear, descriptive project names
   - Keep file names meaningful

2. **Effective Querying**
   - Be specific in your questions
   - Ask follow-up questions to get more detailed answers
   - Use the chat history to build on previous conversations

3. **File Management**
   - Ensure documents are high-quality scans or text-based PDFs for best results
   - Break up very large documents into smaller sections if needed
   - Remove any documents you no longer need to keep projects organized

### Troubleshooting Common Issues

**Documents not processing:**
- Check file format (PDF, DOCX, TXT only)
- Ensure file size is under 50MB
- Verify you haven't reached the 20-file limit per project

**Chat responses seem inaccurate:**
- Make sure your documents contain the information you're asking about
- Try rephrasing your question
- Check that the right project is selected

**Application not loading:**
- Ensure both backend and frontend are running
- Check that no other applications are using ports 8000 or 8501
- Verify your API keys are correctly set in the `.env` file

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