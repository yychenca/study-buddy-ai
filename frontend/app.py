import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

# Configure the page
st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = "http://localhost:8000"

# Custom CSS for better styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
    }
    .project-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def make_api_request(endpoint: str, method: str = "GET", data: dict = None, files: dict = None):
    """Make API request to backend"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files, data=data)
            else:
                response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def get_all_projects():
    """Fetch all projects"""
    return make_api_request("/api/projects")

def get_project_stats(project_id: str):
    """Get project statistics"""
    return make_api_request(f"/api/projects/{project_id}/stats")

def get_project_documents(project_id: str):
    """Get documents for a project"""
    return make_api_request(f"/api/projects/{project_id}/documents")

def create_project(name: str, description: str = ""):
    """Create a new project"""
    return make_api_request(
        "/api/projects",
        method="POST",
        data={"name": name, "description": description}
    )

# Initialize session state
if 'selected_project_id' not in st.session_state:
    st.session_state.selected_project_id = None
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'refresh_projects' not in st.session_state:
    st.session_state.refresh_projects = True

# Main app
def main():
    # Sidebar for project management
    with st.sidebar:
        st.title("📚 StudyBuddy AI")
        st.markdown("*Your local NotebookLM clone*")
        
        # Refresh projects if needed
        if st.session_state.refresh_projects:
            projects = get_all_projects()
            if projects:
                st.session_state.projects = projects
            st.session_state.refresh_projects = False
        
        # Project selector
        if st.session_state.projects:
            project_options = {proj['name']: proj['id'] for proj in st.session_state.projects}
            project_options["➕ Create New Project"] = "create_new"
            
            selected_name = st.selectbox(
                "Select Project",
                options=list(project_options.keys()),
                index=0 if st.session_state.selected_project_id is None else 
                      list(project_options.values()).index(st.session_state.selected_project_id) 
                      if st.session_state.selected_project_id in project_options.values() else 0
            )
            
            if selected_name == "➕ Create New Project":
                show_create_project_form()
            else:
                st.session_state.selected_project_id = project_options[selected_name]
                selected_project = next(p for p in st.session_state.projects if p['id'] == st.session_state.selected_project_id)
                show_project_info(selected_project)
        else:
            st.info("No projects found. Create your first project!")
            show_create_project_form()
        
        # Refresh button
        if st.button("🔄 Refresh Projects"):
            st.session_state.refresh_projects = True
            st.rerun()
    
    # Main content area
    if st.session_state.selected_project_id and st.session_state.selected_project_id != "create_new":
        show_main_interface()
    else:
        show_welcome_screen()

def show_create_project_form():
    """Show form to create a new project"""
    st.markdown("### Create New Project")
    
    with st.form("create_project_form"):
        name = st.text_input("Project Name", placeholder="My Study Project")
        description = st.text_area("Description (optional)", placeholder="Brief description of your project...")
        
        if st.form_submit_button("Create Project"):
            if name.strip():
                result = create_project(name.strip(), description.strip())
                if result:
                    st.success(f"Project '{name}' created successfully!")
                    st.session_state.refresh_projects = True
                    st.session_state.selected_project_id = result['id']
                    st.rerun()
            else:
                st.error("Project name is required!")

def show_project_info(project):
    """Show project information in sidebar"""
    st.markdown(f"### {project['name']}")
    if project.get('description'):
        st.markdown(f"*{project['description']}*")
    
    # Get and display project stats
    stats = get_project_stats(project['id'])
    if stats:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📄 Documents", stats.get('document_count', 0))
        with col2:
            st.metric("💬 Chats", stats.get('chat_count', 0))
        
        if stats.get('last_activity'):
            last_activity = datetime.fromisoformat(stats['last_activity'].replace('Z', '+00:00'))
            st.caption(f"Last activity: {last_activity.strftime('%Y-%m-%d %H:%M')}")

def show_welcome_screen():
    """Show welcome screen when no project is selected"""
    st.title("Welcome to StudyBuddy AI! 📚")
    st.markdown("""
    ### Your Local NotebookLM Clone
    
    StudyBuddy AI helps you organize documents, extract insights, and have intelligent conversations about your content.
    
    **Features:**
    - 📁 **Project Management**: Organize documents into projects
    - 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
    - 🤖 **AI Chat**: Ask questions about your documents
    - 🔍 **Smart Search**: Find relevant content across projects
    - 📊 **Summaries**: Get automatic document summaries
    
    **Get Started:**
    1. Create a new project in the sidebar
    2. Upload your documents
    3. Start chatting with your AI assistant!
    
    ---
    
    ### Quick Tips:
    - Upload up to 20 documents per project
    - Supported formats: PDF, DOCX, TXT (max 50MB each)
    - Use the chat to ask specific questions about your documents
    - Search across all projects to find relevant information
    """)

def show_main_interface():
    """Show main interface with tabs"""
    project = next(p for p in st.session_state.projects if p['id'] == st.session_state.selected_project_id)
    
    st.title(f"📚 {project['name']}")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📄 Documents", "🔍 Search"])
    
    with tab1:
        show_chat_interface()
    
    with tab2:
        show_document_manager()
    
    with tab3:
        show_search_interface()

def show_chat_interface():
    """Show chat interface"""
    from frontend.pages.chat_interface import show_chat_page
    show_chat_page(st.session_state.selected_project_id)

def show_document_manager():
    """Show document management interface"""
    from frontend.pages.document_manager import show_document_page
    show_document_page(st.session_state.selected_project_id)

def show_search_interface():
    """Show search interface"""
    from frontend.pages.search_page import show_search_page
    show_search_page(st.session_state.selected_project_id)

if __name__ == "__main__":
    main()