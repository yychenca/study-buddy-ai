import streamlit as st
import requests
from datetime import datetime
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

def show_chat_page(project_id: str):
    """Show chat interface for a project"""
    
    # Initialize chat history in session state
    chat_key = f"chat_history_{project_id}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
        # Load existing chat history from backend
        load_chat_history(project_id)
    
    # Chat header
    st.markdown("### 💬 Chat with Your Documents")
    st.markdown("Ask questions about the documents in this project. The AI will search through your documents to provide relevant answers.")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if st.session_state[chat_key]:
            for i, chat in enumerate(st.session_state[chat_key]):
                # User message
                with st.chat_message("user"):
                    st.write(chat["message"])
                
                # AI response
                with st.chat_message("assistant"):
                    st.write(chat["response"])
                    
                    # Show metadata if available
                    if chat.get("sources_used", 0) > 0:
                        st.caption(f"📄 Referenced {chat['sources_used']} document sections")
                    
                    if chat.get("timestamp"):
                        timestamp = datetime.fromisoformat(chat['timestamp'].replace('Z', '+00:00'))
                        st.caption(f"⏰ {timestamp.strftime('%H:%M:%S')}")
        else:
            st.info("👋 Start a conversation! Ask me anything about your documents.")
    
    # Chat input
    if prompt := st.chat_input("Ask about your documents..."):
        # Add user message to display immediately
        st.session_state[chat_key].append({
            "message": prompt,
            "response": "🤔 Thinking...",
            "sources_used": 0,
            "timestamp": datetime.now().isoformat()
        })
        
        # Rerun to show user message immediately
        st.rerun()
    
    # Process the latest message if it's still "thinking"
    if (st.session_state[chat_key] and 
        st.session_state[chat_key][-1]["response"] == "🤔 Thinking..."):
        
        latest_message = st.session_state[chat_key][-1]["message"]
        
        # Show thinking indicator
        with st.spinner("AI is analyzing your documents..."):
            # Make API request
            response = make_api_request(
                f"/api/projects/{project_id}/chat",
                method="POST",
                data={"message": latest_message, "project_id": project_id}
            )
        
        if response:
            # Update the last message with the real response
            st.session_state[chat_key][-1] = {
                "message": latest_message,
                "response": response["response"],
                "sources_used": response.get("sources_used", 0),
                "timestamp": response.get("timestamp", datetime.now().isoformat())
            }
        else:
            # Update with error message
            st.session_state[chat_key][-1] = {
                "message": latest_message,
                "response": "❌ Sorry, I couldn't process your request. Please try again.",
                "sources_used": 0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Rerun to show the response
        st.rerun()
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state[chat_key] = []
            st.rerun()
    
    with col2:
        if st.button("📄 Generate Summary"):
            generate_project_summary(project_id)
    
    with col3:
        if st.button("📥 Load History"):
            load_chat_history(project_id)
            st.success("Chat history refreshed!")
            st.rerun()

def load_chat_history(project_id: str):
    """Load chat history from backend"""
    history = make_api_request(f"/api/projects/{project_id}/chat/history")
    if history:
        chat_key = f"chat_history_{project_id}"
        st.session_state[chat_key] = [
            {
                "message": chat["message"],
                "response": chat["response"],
                "sources_used": 0,  # Not stored in backend currently
                "timestamp": chat["timestamp"]
            }
            for chat in history
        ]

def generate_project_summary(project_id: str):
    """Generate and display project summary"""
    with st.spinner("Generating project summary..."):
        summary = make_api_request(
            f"/api/projects/{project_id}/chat/summarize",
            method="POST"
        )
    
    if summary:
        st.success("📋 Project Summary Generated!")
        
        # Create expandable summary section
        with st.expander("📊 Project Summary", expanded=True):
            st.markdown(f"**Project:** {summary['project_name']}")
            st.markdown(f"**Documents:** {summary['document_count']}")
            
            st.markdown("### Summary")
            st.markdown(summary['summary'])
            
            if summary.get('documents'):
                st.markdown("### Documents in Project")
                for doc in summary['documents']:
                    upload_date = datetime.fromisoformat(doc['upload_date'].replace('Z', '+00:00'))
                    st.markdown(f"- **{doc['filename']}** *(uploaded {upload_date.strftime('%Y-%m-%d')})*")

# Sample questions to help users get started
def show_sample_questions():
    """Show sample questions users can ask"""
    st.markdown("### 💡 Sample Questions")
    
    sample_questions = [
        "What are the main topics covered in these documents?",
        "Can you summarize the key findings?",
        "What are the most important concepts I should know?",
        "Are there any conclusions or recommendations?",
        "How do these documents relate to each other?",
        "What questions should I ask based on this content?"
    ]
    
    for question in sample_questions:
        if st.button(f"❓ {question}", key=f"sample_{hash(question)}"):
            # Add to chat input (this would need to be implemented differently in Streamlit)
            st.info(f"Click in the chat input and type: {question}")

# Call sample questions if chat is empty
def show_chat_page(project_id: str):
    """Enhanced show_chat_page with sample questions"""
    
    # Initialize chat history in session state
    chat_key = f"chat_history_{project_id}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
        # Load existing chat history from backend
        load_chat_history(project_id)
    
    # Chat header
    st.markdown("### 💬 Chat with Your Documents")
    st.markdown("Ask questions about the documents in this project. The AI will search through your documents to provide relevant answers.")
    
    # Show sample questions if no chat history
    if not st.session_state[chat_key]:
        with st.expander("💡 Sample Questions to Get Started", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Content Analysis:**")
                st.markdown("• What are the main topics?")
                st.markdown("• Can you summarize the key points?")
                st.markdown("• What are the important concepts?")
            
            with col2:
                st.markdown("**Specific Queries:**")
                st.markdown("• Are there any conclusions?")
                st.markdown("• How do these documents relate?")
                st.markdown("• What should I focus on studying?")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if st.session_state[chat_key]:
            for i, chat in enumerate(st.session_state[chat_key]):
                # User message
                with st.chat_message("user"):
                    st.write(chat["message"])
                
                # AI response
                with st.chat_message("assistant"):
                    st.write(chat["response"])
                    
                    # Show metadata if available
                    if chat.get("sources_used", 0) > 0:
                        st.caption(f"📄 Referenced {chat['sources_used']} document sections")
                    
                    if chat.get("timestamp"):
                        timestamp = datetime.fromisoformat(chat['timestamp'].replace('Z', '+00:00'))
                        st.caption(f"⏰ {timestamp.strftime('%H:%M:%S')}")
        else:
            st.info("👋 Start a conversation! Ask me anything about your documents.")
    
    # Chat input
    if prompt := st.chat_input("Ask about your documents..."):
        # Add user message to display immediately
        st.session_state[chat_key].append({
            "message": prompt,
            "response": "🤔 Thinking...",
            "sources_used": 0,
            "timestamp": datetime.now().isoformat()
        })
        
        # Rerun to show user message immediately
        st.rerun()
    
    # Process the latest message if it's still "thinking"
    if (st.session_state[chat_key] and 
        st.session_state[chat_key][-1]["response"] == "🤔 Thinking..."):
        
        latest_message = st.session_state[chat_key][-1]["message"]
        
        # Show thinking indicator
        with st.spinner("AI is analyzing your documents..."):
            # Make API request
            response = make_api_request(
                f"/api/projects/{project_id}/chat",
                method="POST",
                data={"message": latest_message, "project_id": project_id}
            )
        
        if response:
            # Update the last message with the real response
            st.session_state[chat_key][-1] = {
                "message": latest_message,
                "response": response["response"],
                "sources_used": response.get("sources_used", 0),
                "timestamp": response.get("timestamp", datetime.now().isoformat())
            }
        else:
            # Update with error message
            st.session_state[chat_key][-1] = {
                "message": latest_message,
                "response": "❌ Sorry, I couldn't process your request. Please try again.",
                "sources_used": 0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Rerun to show the response
        st.rerun()
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state[chat_key] = []
            st.rerun()
    
    with col2:
        if st.button("📄 Generate Summary"):
            generate_project_summary(project_id)
    
    with col3:
        if st.button("📥 Load History"):
            load_chat_history(project_id)
            st.success("Chat history refreshed!")
            st.rerun()