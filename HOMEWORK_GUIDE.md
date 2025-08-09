# StudyBuddy AI - RAG System Homework Guide

## 📚 Learning Objectives

By completing this homework, you will:
- Understand the complete RAG (Retrieval-Augmented Generation) pipeline
- Learn how to process and chunk documents for AI systems
- Master vector embeddings and semantic search
- Build a production-ready AI chat system grounded in real documents
- Gain hands-on experience with modern AI APIs (Gemini, Pinecone)

## 🎯 Overview

You will implement the 5 core steps of a RAG system:

1. **Load & Split**: Extract text from documents and chunk it intelligently
2. **Embed**: Convert text chunks into vector embeddings
3. **Store**: Save vectors in a searchable database
4. **Retrieve**: Find relevant chunks using semantic search
5. **Generate**: Create AI responses using retrieved context

## ⏰ Time Estimate: 2-4 hours

## 🧪 Testing Your Solutions

Before starting, verify your environment is set up correctly:

```bash
# Test that all imports work
python tests/test_imports.py
```

For each task, you can test your implementation:

```bash
# Test individual tasks
python tests/test_task1_document_processing.py
python tests/test_task2_embeddings.py
python tests/test_task3_vector_storage.py
python tests/test_task4_retrieval.py
python tests/test_task5_rag_generation.py

# Test everything at once
python tests/run_all_tests.py
```

**Important:** Run tests from the project root directory (where this README is located).

## 📋 Task Checklist

### ✅ Task 1: Document Loading & Text Extraction (30-45 minutes)
**File:** `backend/services/processor.py`

**Specific functions to implement:**
- [ ] **`_extract_text()` method** - Add file type dispatch logic (lines 104-106)
- [ ] **Text chunking in `process_document()`** - Uncomment chunking line (line 67)

**What you'll implement:**
- [ ] Text extraction dispatch for PDF, DOCX, and TXT files in `_extract_text()`
- [ ] Intelligent text chunking by uncommenting `self.text_splitter.split_text(text)`
- [ ] Error handling for different file formats

**Implementation details:**
- **Function:** `_extract_text(file_content, filename)` 
- **Location:** Around line 76 in processor.py
- **Task:** Replace `return "TODO: Implement text extraction logic"` with proper file type handling
- **Also:** In `process_document()`, replace `chunks = ["TODO: Implement chunking logic"]` with actual chunking

**Key learning:** How to prepare documents for AI processing

**Test your work:** 
```bash
# First verify imports work
python tests/test_imports.py

# Then test Task 1
python tests/test_task1_document_processing.py
```

---

### ✅ Task 2: Embedding Generation (20-30 minutes)  
**File:** `backend/services/gemini_service.py`

**Specific functions to implement:**
- [ ] **`generate_embedding()` method** - Replace placeholder return (line 60)
- [ ] **`generate_query_embedding()` method** - Replace placeholder return (line 98)

**What you'll implement:**
- [ ] Document embedding generation using `genai.embed_content()` API
- [ ] Query embedding generation with different task_type
- [ ] API error handling and validation

**Implementation details:**
- **Function:** `generate_embedding(text)` 
- **Location:** Around line 26 in gemini_service.py
- **Task:** Replace `return [0.0] * 768` with real `genai.embed_content()` call
- **Also:** `generate_query_embedding(query)` around line 74
- **Key difference:** Use `task_type="retrieval_document"` vs `task_type="retrieval_query"`

**Key learning:** How text becomes numerical vectors for AI

**Test your work:** `python tests/test_task2_embeddings.py`

---

### ✅ Task 3: Vector Storage (30-45 minutes)
**File:** `backend/services/pinecone_service.py`

**Specific functions to implement:**
- [ ] **`upsert_document_chunks()` method** - Replace `return False` (line 80)

**What you'll implement:**
- [ ] Vector preparation with unique IDs and metadata
- [ ] Pinecone upsert operation with project namespaces
- [ ] Metadata storage for document information

**Implementation details:**
- **Function:** `upsert_document_chunks(project_id, document_id, filename, chunks, embeddings)` 
- **Location:** Around line 32 in pinecone_service.py
- **Task:** Replace `return False` placeholder with actual vector storage logic
- **Key steps:** Create vector tuples → Set namespace → Call `self.index.upsert()`
- **Vector format:** `(vector_id, embedding, metadata)` tuples

**Key learning:** How vector databases enable fast semantic search

**Test your work:** `python tests/test_task3_vector_storage.py`

---

### ✅ Task 4: Similarity Retrieval (20-30 minutes)
**File:** `backend/services/pinecone_service.py`

**Specific functions to implement:**
- [ ] **`search_similar_chunks()` method** - Replace `return []` (line 146)

**What you'll implement:**
- [ ] Pinecone similarity search using `index.query()`
- [ ] Project-specific and global search with namespaces
- [ ] Result formatting with metadata extraction

**Implementation details:**
- **Function:** `search_similar_chunks(query_embedding, project_id, top_k)` 
- **Location:** Around line 105 in pinecone_service.py
- **Task:** Replace `return []` placeholder with actual similarity search
- **Key steps:** Set namespace → Call `self.index.query()` → Format results
- **Query parameters:** `vector`, `top_k`, `include_metadata=True`, `namespace`

**Key learning:** How AI finds relevant context for questions

**Test your work:** `python tests/test_task4_retrieval.py`

---

### ✅ Task 5: Context-Aware Generation (30-45 minutes)
**File:** `backend/routers/chat.py`

**Specific functions to implement:**
- [ ] **`chat_with_project()` function** - Replace RAG pipeline section (lines 45-47)

**What you'll implement:**
- [ ] Query embedding generation for user questions
- [ ] Vector search to find relevant document chunks
- [ ] Context extraction and response generation with retrieved information

**Implementation details:**
- **Function:** `chat_with_project(project_id, message)` 
- **Location:** Around line 11 in chat.py
- **Task:** Replace placeholder variables with complete RAG pipeline
- **Key steps:** Generate query embedding → Search vectors → Extract context → Generate response
- **Replace these lines:**
  - `query_embedding = None` → Real embedding generation
  - `relevant_chunks = []` → Real context retrieval  
  - `response = "TODO: ..."` → Real LLM generation with context

**Key learning:** How retrieval improves AI accuracy and reduces hallucination

**Test your work:** `python tests/test_task5_rag_generation.py`

## 🚀 Getting Started

### 1. Environment Setup

Ensure you have completed the installation steps from the README:

```bash
# Activate your environment
conda activate studybuddy

# Verify API keys are set
echo $GEMINI_API_KEY
echo $PINECONE_API_KEY
```

### 2. Find the TODO Comments

Each task has clear `TODO` comments in the code. Look for:
```python
# TODO: TASK X - [Description]
# Students need to implement...
```

### 3. Follow the Template

Each TODO section includes:
- Detailed implementation instructions
- Expected input/output behavior
- Code templates to uncomment and complete
- Validation assertions to guide you

### 4. Test Frequently

Run tests after implementing each task:
```bash
# Individual task tests
python tests/test_task1_document_processing.py
python tests/test_task2_embeddings.py
python tests/test_task3_vector_storage.py
python tests/test_task4_retrieval.py
python tests/test_task5_rag_generation.py

# All tests at once
python tests/run_all_tests.py
```

## 📝 Implementation Tips

### Task 1: Document Processing
**Look for:** `return "TODO: Implement text extraction logic"` in `_extract_text()` method
- The helper methods (`_extract_pdf_text`, etc.) are already implemented
- You just need to call them correctly in `_extract_text`
- **Replace the TODO return** with if/elif/else logic for file extensions
- **For chunking:** Replace `chunks = ["TODO: Implement chunking logic"]` with `chunks = self.text_splitter.split_text(text)`
- Pay attention to error handling for different file types

### Task 2: Embedding Generation
**Look for:** `return [0.0] * 768` placeholders in both embedding methods
- **Replace placeholder returns** with actual `genai.embed_content()` calls
- Use `task_type="retrieval_document"` for document embedding
- Use `task_type="retrieval_query"` for query embedding  
- Handle API errors gracefully (network issues, rate limits)
- Validate input text is not empty

### Task 3: Vector Storage
**Look for:** `return False` placeholder in `upsert_document_chunks()` method
- **Replace `return False`** with complete vector storage implementation
- Create unique IDs for each chunk: `f"{document_id}_{chunk_index}"`
- Store both preview text and full text in metadata
- Use project namespaces: `f"project_{project_id}"`
- The Pinecone `upsert` method takes a list of tuples: `(id, vector, metadata)`

### Task 4: Similarity Retrieval
**Look for:** `return []` placeholder in `search_similar_chunks()` method
- **Replace `return []`** with actual similarity search implementation
- Use `self.index.query()` for similarity search
- Set `include_metadata=True` to get document information
- Handle both project-specific and global search with namespaces
- Format results consistently with id, score, metadata, and text

### Task 5: RAG Generation
**Look for:** Three placeholder variables in `chat_with_project()` function
- **Replace `query_embedding = None`** with real embedding generation
- **Replace `relevant_chunks = []`** with actual search and context extraction  
- **Replace `response = "TODO: ..."`** with real LLM generation using context
- Follow the 5-step pipeline: embed query → search → extract text → generate response
- Extract text from search results: `[result["text"] for result in search_results]`

## 🐛 Common Issues & Solutions

### "Module not found" errors
```bash
# Make sure you're in the project root directory
cd /path/to/study-buddy-ai

# Run tests from project root
python tests/test_task1_document_processing.py
```

### API key errors
```bash
# Check your .env file
cat .env

# Ensure no extra quotes or spaces around keys
GEMINI_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
```

### Pinecone connection issues
- Verify your Pinecone account is active
- Check that your API key has proper permissions
- Ensure you have sufficient quota

### Embedding dimension mismatches
- Gemini text-embedding-004 produces 768-dimensional vectors
- Make sure your Pinecone index is configured for 768 dimensions

## ✅ Success Criteria

Your implementation is complete when:

1. **All tests pass**: `python tests/run_all_tests.py` shows all green checkmarks
2. **End-to-end functionality**: You can upload documents and chat with them
3. **Error handling**: System gracefully handles edge cases
4. **Code quality**: Following the provided templates and best practices

## 🎉 What's Next?

After completing all tasks:

1. **Test with real documents**: Upload PDFs, DOCX files, and try asking questions
2. **Experiment with parameters**: Try different chunk sizes, embedding models
3. **Add features**: Implement conversation memory, document summarization
4. **Deploy your system**: Use the deployment guide to make it publicly accessible

## 🆘 Getting Help

**Stuck on a task?**
1. Check the test output - it provides specific error messages
2. Review the TODO comments - they contain detailed instructions
3. Ask your TA during office hours
4. Use the debugging tips in each test file

**Common questions:**
- "My embeddings are all zeros" → Check API key and network connection
- "Search returns no results" → Make sure Task 3 (storage) is working first
- "Tests fail with assertions" → You haven't uncommented the template code yet

**Remember:** Each task builds on the previous one. Make sure earlier tasks are working before moving to later ones!

---

**Good luck! You're about to build a real AI system that powers document understanding! 🚀**