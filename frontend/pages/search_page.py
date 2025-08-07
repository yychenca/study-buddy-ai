import streamlit as st
import requests
from typing import List, Dict

API_BASE_URL = "http://localhost:8000"

def make_api_request(endpoint: str, method: str = "GET", data: dict = None):
    """Make API request to backend"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def show_search_page(project_id: str):
    """Show search interface"""
    
    st.markdown("### 🔍 Search Documents")
    st.markdown("Search through your documents using semantic search. Find relevant content even if the exact words don't match.")
    
    # Search input
    search_query = st.text_input(
        "Search query",
        placeholder="Enter your search query...",
        help="Use natural language to describe what you're looking for"
    )
    
    # Search scope selection
    search_scope = st.radio(
        "Search scope",
        options=["This project only", "All projects"],
        horizontal=True,
        help="Choose whether to search in this project or across all your projects"
    )
    
    # Search button
    if st.button("🔍 Search", type="primary") and search_query.strip():
        perform_search(project_id if search_scope == "This project only" else None, search_query.strip())
    
    # Show search tips if no query
    if not search_query:
        show_search_tips()
    
    # Display search results if they exist in session state
    search_key = f"search_results_{project_id if search_scope == 'This project only' else 'global'}"
    if search_key in st.session_state and st.session_state[search_key]:
        display_search_results(st.session_state[search_key])

def perform_search(project_id: str, query: str):
    """Perform search and store results"""
    search_key = f"search_results_{project_id if project_id else 'global'}"
    
    with st.spinner("🔍 Searching through documents..."):
        if project_id:
            # Search within project
            results = make_api_request(
                f"/api/projects/{project_id}/chat/search",
                method="POST",
                data={"query": query}
            )
        else:
            # Search across all projects
            results = make_api_request(
                f"/api/projects/any/chat/search/global",  # This endpoint needs to be adjusted in the backend
                method="POST",
                data={"query": query}
            )
    
    if results:
        st.session_state[search_key] = {
            "query": query,
            "results": results,
            "scope": "This project" if project_id else "All projects"
        }
        st.success(f"Found {len(results)} relevant results!")
    else:
        st.warning("No results found. Try different search terms.")
        st.session_state[search_key] = None

def display_search_results(search_data: Dict):
    """Display search results"""
    st.markdown("---")
    st.markdown(f"### 📊 Search Results for '{search_data['query']}'")
    st.caption(f"Scope: {search_data['scope']} • Found {len(search_data['results'])} results")
    
    results = search_data['results']
    
    if not results:
        st.info("No results found.")
        return
    
    # Group results by relevance score
    high_relevance = [r for r in results if r['relevance_score'] > 0.8]
    medium_relevance = [r for r in results if 0.6 <= r['relevance_score'] <= 0.8]
    low_relevance = [r for r in results if r['relevance_score'] < 0.6]
    
    # Display results in sections
    if high_relevance:
        st.markdown("#### 🎯 High Relevance")
        for result in high_relevance:
            display_search_result(result, "high")
    
    if medium_relevance:
        st.markdown("#### 📍 Medium Relevance")
        for result in medium_relevance:
            display_search_result(result, "medium")
    
    if low_relevance:
        with st.expander("📎 Lower Relevance Results"):
            for result in low_relevance:
                display_search_result(result, "low")

def display_search_result(result: Dict, relevance_level: str):
    """Display a single search result"""
    # Determine styling based on relevance
    if relevance_level == "high":
        border_color = "#28a745"  # Green
    elif relevance_level == "medium":
        border_color = "#ffc107"  # Yellow
    else:
        border_color = "#6c757d"  # Gray
    
    with st.container():
        # Create a styled container
        st.markdown(f"""
        <div style="
            border-left: 4px solid {border_color};
            padding: 1rem;
            margin: 0.5rem 0;
            background-color: #f8f9fa;
            border-radius: 0.25rem;
        ">
        </div>
        """, unsafe_allow_html=True)
        
        # Result header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📄 {result['filename']}**")
        with col2:
            score_percentage = result['relevance_score'] * 100
            st.markdown(f"**{score_percentage:.0f}% match**")
        
        # Content snippet
        st.markdown(f"*{result['content_snippet']}*")
        
        # Additional metadata
        col1, col2 = st.columns([1, 1])
        with col1:
            if result.get('project_id'):
                st.caption(f"📁 Project ID: {result['project_id']}")
        with col2:
            if result.get('document_id'):
                st.caption(f"📄 Document ID: {result['document_id'][:8]}...")
        
        st.markdown("---")

def show_search_tips():
    """Show search tips and examples"""
    with st.expander("💡 Search Tips & Examples", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**How to Search Effectively:**")
            st.markdown("• Use natural language queries")
            st.markdown("• Be specific about what you're looking for")
            st.markdown("• Try different phrasings if needed")
            st.markdown("• Use conceptual terms, not just keywords")
        
        with col2:
            st.markdown("**Example Searches:**")
            st.markdown("• *machine learning algorithms*")
            st.markdown("• *project timeline and milestones*")
            st.markdown("• *budget constraints and costs*")
            st.markdown("• *research methodology approach*")
    
    # Quick search buttons for common queries
    st.markdown("#### 🚀 Quick Search")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Data Analysis"):
            st.session_state.quick_search = "data analysis methods and techniques"
    
    with col2:
        if st.button("📈 Results"):
            st.session_state.quick_search = "results findings conclusions"
    
    with col3:
        if st.button("🎯 Objectives"):
            st.session_state.quick_search = "goals objectives purpose aims"
    
    # Handle quick search
    if hasattr(st.session_state, 'quick_search'):
        st.session_state.search_query = st.session_state.quick_search
        del st.session_state.quick_search
        st.rerun()

def show_advanced_search():
    """Show advanced search options (future feature)"""
    with st.expander("🔧 Advanced Search (Coming Soon)"):
        st.markdown("**Future Features:**")
        st.markdown("• Filter by document type")
        st.markdown("• Date range filtering")
        st.markdown("• Exclude specific terms")
        st.markdown("• Search within specific sections")
        st.markdown("• Save and reuse search queries")
        
        # Placeholder controls (disabled)
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Document Type", ["All", "PDF", "DOCX", "TXT"], disabled=True)
            st.date_input("From Date", disabled=True)
        with col2:
            st.multiselect("Tags", ["Research", "Notes", "Reports"], disabled=True)
            st.date_input("To Date", disabled=True)

# Enhanced search page with advanced features
def show_search_page(project_id: str):
    """Enhanced search interface with more features"""
    
    st.markdown("### 🔍 Smart Search")
    st.markdown("Search through your documents using AI-powered semantic search. Find relevant content even when exact words don't match.")
    
    # Search input with better UX
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "What are you looking for?",
            placeholder="e.g., 'budget analysis for Q4' or 'machine learning methodology'",
            help="Use natural language to describe what you're looking for",
            key="main_search_input"
        )
    with col2:
        search_scope = st.selectbox(
            "Scope",
            options=["This project", "All projects"],
            help="Choose search scope"
        )
    
    # Search button
    if st.button("🔍 Search", type="primary") or (search_query and search_query != st.session_state.get('last_search_query', '')):
        if search_query.strip():
            st.session_state['last_search_query'] = search_query
            perform_search(project_id if search_scope == "This project" else None, search_query.strip())
    
    # Show different content based on whether we have results
    search_key = f"search_results_{project_id if search_scope == 'This project' else 'global'}"
    
    if search_key in st.session_state and st.session_state[search_key]:
        display_search_results(st.session_state[search_key])
    else:
        show_search_tips()
        show_advanced_search()