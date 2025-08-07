# TA Guide: RAG System Homework

## 📋 Overview

This guide helps TAs effectively support students working on the RAG (Retrieval-Augmented Generation) homework assignment. Students will implement 5 core RAG components over 2-4 hours.

## 🎯 Learning Goals

Students should understand:
- **RAG Pipeline**: The complete flow from document → embeddings → storage → retrieval → generation
- **Vector Embeddings**: How text becomes searchable numerical representations
- **Semantic Search**: How similarity search finds relevant context
- **Context-Aware Generation**: How retrieved information improves LLM responses
- **Production AI Systems**: Real-world implementation challenges and solutions

## 📚 Task Breakdown & Common Issues

### Task 1: Document Loading & Text Extraction (30-45 min)
**File:** `backend/services/processor.py`

**What students implement:**
- Text extraction dispatch logic in `_extract_text()`
- Text chunking by uncommenting `self.text_splitter.split_text(text)`

**Common student mistakes:**
1. **Not uncommenting template code** - Most common issue!
2. **Missing file type handling** - Forgetting to handle PDF, DOCX, TXT
3. **Not returning extracted text** - Forgetting return statements
4. **Chunking confusion** - Not understanding the difference between extraction and chunking

**How to help:**
- Show them the TODO comments and template code
- Explain that helper methods are already implemented
- Demonstrate file type checking with `file_extension`
- Run the test to show specific error messages

**Test command:** `python tests/test_task1_document_processing.py`

**Solution:**
```python
def _extract_text(self, file_content: bytes, filename: str) -> str:
    """Extract text from different file types"""
    file_extension = Path(filename).suffix.lower()
    
    try:
        if file_extension == '.pdf':
            return self._extract_pdf_text(file_content)
        elif file_extension == '.docx':
            return self._extract_docx_text(file_content)
        elif file_extension == '.txt':
            return self._extract_txt_text(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    except Exception as e:
        print(f"Error extracting text from {filename}: {str(e)}")
        return ""
```

And in the `process_document` method, replace the chunking placeholder:
```python
# Replace: chunks = ["TODO: Implement chunking logic"]  
# With:
chunks = self.text_splitter.split_text(text)
```

**Note:** Remove the assert statements in the student template - they're for guidance only.

---

### Task 2: Embedding Generation (20-30 min)
**File:** `backend/services/gemini_service.py`

**What students implement:**
- `genai.embed_content()` calls for documents and queries
- Different `task_type` parameters for optimization

**Common student mistakes:**
1. **API key issues** - Most common blocker
2. **Wrong model name** - Using old model names
3. **Not replacing placeholder** - Leaving `[0.0] * 768`
4. **Incorrect task_type** - Mixing up document vs query types

**How to help:**
- Check `.env` file for valid API keys
- Verify Gemini API access at [aistudio.google.com](https://aistudio.google.com)
- Explain the difference between document and query embeddings
- Show them the API documentation in comments

**Test command:** `python tests/test_task2_embeddings.py`

**Solution:**
```python
def generate_embedding(self, text: str) -> List[float]:
    """Generate embeddings for the given text"""
    assert text and isinstance(text, str), "Text input must be a non-empty string"
    assert text.strip(), "Text input cannot be just whitespace"
    
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return []

def generate_query_embedding(self, query: str) -> List[float]:
    """Generate embeddings for search queries"""
    assert query and isinstance(query, str), "Query input must be a non-empty string"
    assert query.strip(), "Query input cannot be just whitespace"
    
    try:
        result = genai.embed_content(
            model="models/text-embedding-004", 
            content=query,
            task_type="retrieval_query"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating query embedding: {str(e)}")
        return []
```

**API troubleshooting:**
```python
# Test API connection manually
import google.generativeai as genai
genai.configure(api_key="their_api_key")
result = genai.embed_content(model="models/text-embedding-004", content="test")
```

---

### Task 3: Vector Storage (30-45 min)
**File:** `backend/services/pinecone_service.py`

**What students implement:**
- Vector preparation with metadata
- Pinecone `upsert()` calls with namespaces

**Common student mistakes:**
1. **Pinecone API key issues** - Second most common blocker
2. **Vector format confusion** - Not understanding (id, vector, metadata) tuples
3. **Namespace confusion** - Not understanding project organization
4. **Metadata structure** - Missing required fields

**How to help:**
- Verify Pinecone account and API key at [pinecone.io](https://pinecone.io)
- Explain vector tuple format: `(vector_id, embedding, metadata)`
- Show namespace concept: separate projects = separate namespaces
- Walk through metadata structure in template

**Test command:** `python tests/test_task3_vector_storage.py`

**Solution:**
```python
def upsert_document_chunks(
    self, 
    project_id: str, 
    document_id: str, 
    filename: str,
    chunks: List[str], 
    embeddings: List[List[float]]
) -> bool:
    """Store document chunks with their embeddings"""
    assert project_id and isinstance(project_id, str), "Project ID must be a non-empty string"
    assert document_id and isinstance(document_id, str), "Document ID must be a non-empty string"
    assert filename and isinstance(filename, str), "Filename must be a non-empty string"
    assert chunks and len(chunks) > 0, "Chunks list cannot be empty"
    assert embeddings and len(embeddings) == len(chunks), "Must have equal number of chunks and embeddings"
    
    try:
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = f"{document_id}_{i}"
            metadata = {
                "project_id": project_id,
                "document_id": document_id, 
                "filename": filename,
                "chunk_index": i,
                "text": chunk[:1000],  # Preview text (first 1000 chars)
                "full_text": chunk     # Full text for retrieval
            }
            vectors.append((vector_id, embedding, metadata))
        
        # Store vectors in project namespace
        namespace = f"project_{project_id}"
        self.index.upsert(vectors=vectors, namespace=namespace)
        return True
    except Exception as e:
        print(f"Error upserting document chunks: {str(e)}")
        return False
```

**Pinecone troubleshooting:**
```python
# Test Pinecone connection
from pinecone import Pinecone
pc = Pinecone(api_key="their_api_key")
print(pc.list_indexes())  # Should show studybuddy-documents index
```

---

### Task 4: Similarity Retrieval (20-30 min)
**File:** `backend/services/pinecone_service.py`

**What students implement:**
- `index.query()` calls for similarity search
- Result formatting and metadata extraction

**Common student mistakes:**
1. **No data to search** - Task 3 not working first
2. **Wrong query parameters** - Missing `include_metadata=True`
3. **Result formatting** - Not extracting text from metadata
4. **Namespace handling** - Not matching storage namespaces

**How to help:**
- Ensure Task 3 is working first (data must be stored before retrieval)
- Show Pinecone query API documentation
- Explain similarity scores (0-1, higher = more similar)
- Walk through result structure: matches[].metadata

**Test command:** `python tests/test_task4_retrieval.py`

**Solution:**
```python
def search_similar_chunks(
    self, 
    query_embedding: List[float], 
    project_id: str = None,
    top_k: int = 5
) -> List[Dict]:
    """Search for similar document chunks"""
    assert query_embedding and len(query_embedding) > 0, "Query embedding cannot be empty"
    assert isinstance(top_k, int) and top_k > 0, "top_k must be a positive integer"
    
    try:
        # Determine search namespace (project-specific or global)
        namespace = f"project_{project_id}" if project_id else None
        
        # Perform similarity search
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace
        )
        
        # Format results for downstream use
        formatted_results = []
        for match in results.matches:
            formatted_results.append({
                "id": match.id,
                "score": match.score,           # Similarity score (0-1)
                "metadata": match.metadata,     # Document info
                "text": match.metadata.get("full_text", match.metadata.get("text", ""))
            })
        
        return formatted_results
    except Exception as e:
        print(f"Error searching similar chunks: {str(e)}")
        return []
```

---

### Task 5: Context-Aware Generation (30-45 min)
**File:** `backend/routers/chat.py`

**What students implement:**
- Complete RAG pipeline integration
- Query embedding → search → context extraction → generation

**Common student mistakes:**
1. **Pipeline sequence errors** - Wrong order of operations
2. **Context extraction** - Not getting text from search results
3. **Error propagation** - Previous tasks not working
4. **Context formatting** - Not passing context list correctly

**How to help:**
- Emphasize the 5-step sequence: embed → search → extract → generate
- Show context extraction: `[result["text"] for result in search_results]`
- Verify all previous tasks work first
- Demonstrate the difference between context-aware and general responses

**Test command:** `python tests/test_task5_rag_generation.py`

**Solution:**
```python
# In chat_with_project function, replace the TODO section with:

assert message.message and message.message.strip(), "Message cannot be empty"

# Step 1: Generate query embedding
query_embedding = gemini_service.generate_query_embedding(message.message)
if not query_embedding:
    raise HTTPException(status_code=500, detail="Failed to generate query embedding")

# Step 2: Search for relevant document chunks
relevant_chunks = []
if pinecone_service:
    search_results = pinecone_service.search_similar_chunks(
        query_embedding=query_embedding,
        project_id=project_id,
        top_k=5  # Get top 5 most relevant chunks
    )
    
    # Step 3: Extract text content from search results
    relevant_chunks = [result["text"] for result in search_results if result.get("text")]

# Step 4 & 5: Generate response using LLM with retrieved context
response = await gemini_service.generate_response(
    prompt=message.message,
    context=relevant_chunks if relevant_chunks else None
)

# Validation check for students
assert response != "TODO: Implement RAG-powered chat response", "Students must implement RAG chat pipeline"
```

## 🧪 Testing Strategy

### Individual Task Testing
Students should test each task as they complete it:
```bash
python tests/test_task1_document_processing.py
python tests/test_task2_embeddings.py
python tests/test_task3_vector_storage.py
python tests/test_task4_retrieval.py  
python tests/test_task5_rag_generation.py
```

### Full System Testing
Once all tasks are complete:
```bash
python tests/run_all_tests.py
```

### Manual Testing
After implementation, test the full system:
1. Start backend: `python start_backend.py`
2. Start frontend: `python start_frontend.py`
3. Upload a test document
4. Ask questions and verify RAG responses

## 🚨 Common Blockers & Solutions

### 1. API Key Issues (50% of student problems)
**Symptoms:**
- "Authentication failed"
- "API key not found"
- Empty embeddings or search failures

**Solutions:**
- Check `.env` file exists and has valid keys
- Verify no extra quotes/spaces around keys
- Test API access manually
- Ensure students created accounts and got fresh keys

### 2. Environment/Import Issues (20% of problems)
**Symptoms:**
- "Module not found"
- "Cannot import from backend"

**Solutions:**
- Verify working directory is project root
- Check conda/venv activation
- Ensure all dependencies installed: `pip install -r requirements.txt`

### 3. Sequential Dependencies (15% of problems)
**Symptoms:**
- Later tasks fail even when implemented correctly
- "No search results found"

**Solutions:**
- Verify earlier tasks are working
- Tasks 3 & 4 must be completed together (store then retrieve)
- Task 5 requires all previous tasks working

### 4. Placeholder Code Not Replaced (10% of problems)
**Symptoms:**
- Tests fail with "TODO not implemented" messages
- Functions return placeholder values

**Solutions:**
- Show students the commented template code
- Explain they need to uncomment AND modify
- Walk through one example together

## 📊 Assessment Rubric

### Technical Implementation (70%)
- **Task 1 (15%)**: Document processing and chunking
- **Task 2 (15%)**: Embedding generation for docs and queries  
- **Task 3 (15%)**: Vector storage with proper metadata
- **Task 4 (15%)**: Similarity search and result formatting
- **Task 5 (10%)**: RAG pipeline integration

### Code Quality (20%)
- Following provided templates and patterns
- Proper error handling
- Clear variable naming
- Appropriate comments

### Understanding (10%)
- Can explain RAG pipeline steps
- Understands vector embeddings concept
- Recognizes why context improves responses

## 🎓 Office Hours Strategy

### Effective Help Sessions
1. **Start with tests** - Run their tests to see specific failures
2. **One task at a time** - Don't jump ahead if earlier tasks fail
3. **Show, don't tell** - Live debug together
4. **Explain concepts** - Help them understand, not just fix

### Quick Diagnostic Questions
- "Which test is failing?" (shows where they are)
- "Can you show me your .env file?" (API key check)
- "What error message do you see?" (specific debugging)
- "Did you uncomment the template code?" (most common fix)

### Time Management
- **Stuck >10 minutes on API keys?** → Help them debug immediately
- **Confused about concepts?** → Brief explanation, then hands-on
- **Code not working?** → Debug together, explain as you go

## 🛠️ Debugging Tools

### For TAs to use during help sessions:

```bash
# Check environment
python -c "import os; print('Gemini:', bool(os.getenv('GEMINI_API_KEY'))); print('Pinecone:', bool(os.getenv('PINECONE_API_KEY')))"

# Test individual components
python -c "from backend.services.gemini_service import gemini_service; print(len(gemini_service.generate_embedding('test')))"

# Check Pinecone connection
python -c "from backend.services.pinecone_service import pinecone_service; print('Connected' if pinecone_service else 'Failed')"
```

## 💡 Teaching Moments

### Key Concepts to Emphasize
1. **RAG solves hallucination** - AI responses grounded in real documents
2. **Vector similarity** - How embeddings enable semantic search
3. **Pipeline thinking** - Each step enables the next
4. **Production considerations** - Error handling, scalability, costs

### Conceptual Questions to Ask
- "Why do we chunk documents instead of using the whole text?"
- "What's the difference between document and query embeddings?"
- "How does semantic search differ from keyword search?"
- "Why is retrieved context better than just general AI knowledge?"

## 📞 Escalation Guidelines

**Escalate to instructor if:**
- API services are down (affects multiple students)
- Fundamental homework design issues
- Student needs concept review beyond TA scope
- Suspected academic integrity issues

**Handle yourself:**
- Individual API key issues
- Code debugging and implementation help
- Environment setup problems
- Conceptual clarification within RAG scope

---

**Remember:** This homework is designed to be challenging but achievable. Most students should be able to complete it with guidance. Focus on helping them understand the concepts, not just getting the tests to pass!