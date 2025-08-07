import streamlit as st
import requests
from datetime import datetime
from typing import List, Dict

API_BASE_URL = "http://localhost:8000"

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
        elif method == "DELETE":
            response = requests.delete(url)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def show_document_page(project_id: str):
    """Show document management interface"""
    
    st.markdown("### 📄 Document Management")
    st.markdown("Upload and manage documents for this project. Supported formats: PDF, DOCX, TXT (max 50MB each, up to 20 files per project).")
    
    # Document upload section
    st.markdown("#### 📤 Upload Documents")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Select one or more documents to upload to this project"
    )
    
    if uploaded_files:
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📤 Upload Files", type="primary"):
                upload_documents(project_id, uploaded_files)
        with col2:
            st.info(f"Ready to upload {len(uploaded_files)} file(s)")
    
    st.markdown("---")
    
    # Document list section
    st.markdown("#### 📚 Project Documents")
    
    # Refresh button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Get and display documents
    documents = get_project_documents(project_id)
    
    if documents:
        st.success(f"Found {len(documents)} document(s) in this project")
        
        # Display documents in a nice format
        for i, doc in enumerate(documents):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    # File icon based on type
                    icon = get_file_icon(doc['file_type'])
                    st.markdown(f"{icon} **{doc['filename']}**")
                    
                    # File details
                    upload_date = datetime.fromisoformat(doc['upload_date'].replace('Z', '+00:00'))
                    file_size_mb = doc['file_size'] / (1024 * 1024)
                    st.caption(f"Uploaded: {upload_date.strftime('%Y-%m-%d %H:%M')} • Size: {file_size_mb:.1f} MB")
                
                with col2:
                    st.markdown(f"**{doc['file_type'].upper()}**")
                
                with col3:
                    # Preview button (placeholder for now)
                    if st.button("👁️ Preview", key=f"preview_{doc['id']}", disabled=True):
                        st.info("Preview feature coming soon!")
                
                with col4:
                    # Delete button
                    if st.button("🗑️ Delete", key=f"delete_{doc['id']}", type="secondary"):
                        delete_document(project_id, doc['id'], doc['filename'])
                
                st.markdown("---")
        
        # Show storage usage
        total_size = sum(doc['file_size'] for doc in documents)
        total_size_mb = total_size / (1024 * 1024)
        max_files = 20  # From config
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Storage Used", f"{total_size_mb:.1f} MB")
        with col2:
            st.metric("📁 Files", f"{len(documents)}/{max_files}")
        
        # Progress bar for file count
        progress = len(documents) / max_files
        st.progress(progress)
        if progress > 0.8:
            st.warning(f"You're using {len(documents)} out of {max_files} available file slots.")
    
    else:
        st.info("📋 No documents uploaded yet. Use the upload section above to add your first documents!")
        
        # Show helpful tips
        with st.expander("💡 Tips for Document Upload", expanded=True):
            st.markdown("""
            **Supported File Types:**
            - 📄 **PDF**: Research papers, reports, articles
            - 📝 **DOCX**: Word documents, essays, notes
            - 📄 **TXT**: Plain text files, code, transcripts
            
            **Best Practices:**
            - Upload related documents to the same project
            - Use descriptive filenames
            - Keep file sizes reasonable (under 50MB)
            - Text-based documents work better than image-heavy files
            
            **Processing:**
            - Documents are automatically processed and indexed
            - Text is extracted and made searchable
            - AI can reference content across all uploaded documents
            """)

def get_project_documents(project_id: str):
    """Get documents for a project"""
    return make_api_request(f"/api/projects/{project_id}/documents")

def upload_documents(project_id: str, uploaded_files):
    """Upload documents to the project"""
    if len(uploaded_files) == 1:
        # Single file upload
        file = uploaded_files[0]
        with st.spinner(f"Uploading {file.name}..."):
            files = {"file": (file.name, file.getvalue(), file.type)}
            result = make_api_request(
                f"/api/projects/{project_id}/documents/upload",
                method="POST",
                files=files
            )
            
            if result:
                st.success(f"✅ Successfully uploaded {file.name}")
                st.rerun()
            else:
                st.error(f"❌ Failed to upload {file.name}")
    
    else:
        # Multiple file upload
        with st.spinner(f"Uploading {len(uploaded_files)} files..."):
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            
            # For bulk upload, we need to handle it differently
            # For now, upload one by one
            success_count = 0
            for file in uploaded_files:
                files = {"file": (file.name, file.getvalue(), file.type)}
                result = make_api_request(
                    f"/api/projects/{project_id}/documents/upload",
                    method="POST",
                    files=files
                )
                if result:
                    success_count += 1
            
            if success_count == len(uploaded_files):
                st.success(f"✅ Successfully uploaded all {success_count} files!")
            elif success_count > 0:
                st.warning(f"⚠️ Uploaded {success_count} out of {len(uploaded_files)} files")
            else:
                st.error("❌ Failed to upload any files")
            
            st.rerun()

def delete_document(project_id: str, document_id: str, filename: str):
    """Delete a document"""
    # Confirmation dialog
    if st.session_state.get(f"confirm_delete_{document_id}"):
        with st.spinner(f"Deleting {filename}..."):
            result = make_api_request(
                f"/api/projects/{project_id}/documents/{document_id}",
                method="DELETE"
            )
            
            if result:
                st.success(f"✅ Successfully deleted {filename}")
                # Clear confirmation state
                if f"confirm_delete_{document_id}" in st.session_state:
                    del st.session_state[f"confirm_delete_{document_id}"]
                st.rerun()
            else:
                st.error(f"❌ Failed to delete {filename}")
    else:
        # Show confirmation
        st.warning(f"Are you sure you want to delete '{filename}'? This action cannot be undone.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete", key=f"confirm_yes_{document_id}"):
                st.session_state[f"confirm_delete_{document_id}"] = True
                st.rerun()
        with col2:
            if st.button("❌ Cancel", key=f"confirm_no_{document_id}"):
                pass  # Do nothing

def get_file_icon(file_type: str) -> str:
    """Get icon for file type"""
    icons = {
        'pdf': '📄',
        'docx': '📝',
        'txt': '📄',
        'doc': '📝'
    }
    return icons.get(file_type.lower(), '📄')

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"