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

StudyBuddy AI consists of two components that need to run simultaneously:
- **Backend**: FastAPI server that handles API requests and AI processing
- **Frontend**: Streamlit web interface that users interact with

#### Option 1: Using Startup Scripts (Recommended)

**Step 1: Activate your environment**
```bash
# If using conda:
conda activate studybuddy

# If using venv:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**Step 2: Start the backend server**

Open your first terminal/command prompt and run:
```bash
python start_backend.py
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
```

**Step 3: Start the frontend (in a NEW terminal)**

Open a **second** terminal/command prompt, activate your environment again, and run:
```bash
# Activate environment first
conda activate studybuddy  # or source venv/bin/activate

# Start frontend
python start_frontend.py
```

You should see output like:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.xxx:8501
```

**Step 4: Access the application**
- The frontend will automatically open in your browser at `http://localhost:8501`
- If it doesn't open automatically, manually navigate to `http://localhost:8501`
- Keep both terminals running while using the application

#### Option 2: Manual Start (Advanced)

If the startup scripts don't work, you can start each component manually:

**Step 1: Initialize database (first time only)**
```bash
conda activate studybuddy  # Activate your environment
python scripts/init_db.py
```

**Step 2: Start FastAPI backend**
```bash
# In terminal 1:
conda activate studybuddy
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Step 3: Start Streamlit frontend**
```bash
# In terminal 2:
conda activate studybuddy
streamlit run frontend/app.py --server.port 8501
```

#### Troubleshooting Startup Issues

**"Port already in use" error:**
```bash
# Check what's using the ports:
# Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# macOS/Linux:
lsof -i :8000
lsof -i :8501

# Kill processes if needed (use PID from above commands):
# Windows:
taskkill /PID <process_id> /F

# macOS/Linux:
kill -9 <process_id>
```

**Backend won't start:**
- Verify your `.env` file has valid API keys
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're in the project root directory

**Frontend can't connect to backend:**
- Verify backend is running on `http://localhost:8000`
- Check `http://localhost:8000/docs` to confirm API is accessible
- Ensure no firewall is blocking the connection

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

## 🚀 Deployment

### Free Hosting Options

You can deploy StudyBuddy AI to various free hosting platforms. Here are the most popular options:

#### Option 1: Streamlit Community Cloud (Recommended for Frontend)

**Best for**: Quick deployment of Streamlit apps
**Limitations**: Backend needs separate hosting

1. **Prepare your repository:**
   ```bash
   # Add streamlit-specific requirements
   echo "streamlit" >> requirements.txt
   
   # Create streamlit config (optional)
   mkdir -p .streamlit
   cat > .streamlit/config.toml << EOF
   [server]
   headless = true
   port = 8501
   
   [theme]
   base = "light"
   EOF
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `frontend/app.py`
   - Add your environment variables (API keys) in the secrets section

**Note**: You'll need to modify the app to work without a separate backend or use a hosted backend service.

#### Option 2: Railway (Full-Stack Deployment)

**Best for**: Complete full-stack deployment
**Free tier**: 500 hours/month, $5 credit

1. **Prepare for Railway:**
   ```bash
   # Create railway.json
   cat > railway.json << EOF
   {
     "\$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python start_backend.py & python start_frontend.py",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   EOF
   
   # Create Procfile for process management
   cat > Procfile << EOF
   web: python start_backend.py & streamlit run frontend/app.py --server.port \$PORT --server.address 0.0.0.0
   EOF
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Connect GitHub account
   - Deploy your repository
   - Add environment variables in Railway dashboard
   - Railway will automatically detect Python and install dependencies

#### Option 3: Render (Separate Services)

**Best for**: Professional deployment with separate backend/frontend
**Free tier**: 750 hours/month per service

1. **Backend deployment on Render:**
   - Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: studybuddy-backend
       env: python
       buildCommand: "pip install -r requirements.txt"
       startCommand: "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
       envVars:
         - key: GEMINI_API_KEY
           sync: false
         - key: PINECONE_API_KEY
           sync: false
   ```

2. **Frontend deployment on Render:**
   - Create separate service for Streamlit
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0`

#### Option 4: Heroku (Legacy Free Tier Alternative)

**Note**: Heroku discontinued free tier, but still popular for paid hosting

1. **Create Heroku configuration:**
   ```bash
   # Create Procfile
   echo "web: python start_backend.py & streamlit run frontend/app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile
   
   # Create runtime.txt
   echo "python-3.9.18" > runtime.txt
   ```

#### Option 5: Fly.io (Recommended Alternative)

**Best for**: Docker-based deployment
**Free tier**: Generous allowances for small apps

1. **Install Fly CLI and setup:**
   ```bash
   # Install Fly CLI (visit fly.io for instructions)
   
   # Create Dockerfile
   cat > Dockerfile << EOF
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000 8501
   
   CMD ["sh", "-c", "python start_backend.py & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]
   EOF
   
   # Initialize fly app
   fly launch
   ```

### Deployment Preparation Checklist

Before deploying to any platform:

1. **Environment Variables:**
   - Set `GEMINI_API_KEY` in hosting platform's environment settings
   - Set `PINECONE_API_KEY` in hosting platform's environment settings
   - Never commit API keys to your repository

2. **Database Setup:**
   - For production, consider using hosted SQLite or PostgreSQL
   - Update `DATABASE_PATH` environment variable if needed

3. **CORS Configuration:**
   - Update FastAPI CORS settings for your domain
   - Modify `backend/main.py` if needed

4. **Port Configuration:**
   - Ensure your app can use dynamic ports (`$PORT` environment variable)
   - Most platforms assign ports dynamically

5. **Dependencies:**
   - Ensure `requirements.txt` is up to date
   - Test installation locally: `pip install -r requirements.txt`

### Production Considerations

**Security:**
- Use HTTPS in production
- Set up proper environment variable management
- Consider using secrets management services

**Performance:**
- Use gunicorn for FastAPI in production
- Set up proper logging
- Consider using Redis for caching
- Monitor API rate limits (Gemini/Pinecone)

**Scaling:**
- Most free tiers have limitations
- Plan for paid tiers if you expect high usage
- Consider database scaling needs

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