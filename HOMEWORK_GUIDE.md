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

## 📋 Task Checklist

### ✅ Task 1: Document Loading & Text Extraction (30-45 minutes)
**File:** `backend/services/processor.py`

**What you'll implement:**
- [ ] Text extraction from PDF, DOCX, and TXT files
- [ ] Intelligent text chunking with overlap
- [ ] Error handling for different file formats

**Key learning:** How to prepare documents for AI processing

**Test your work:** `python tests/test_task1_document_processing.py`

---

### ✅ Task 2: Embedding Generation (20-30 minutes)  
**File:** `backend/services/gemini_service.py`

**What you'll implement:**
- [ ] Document embedding generation using Gemini API
- [ ] Query embedding generation for search
- [ ] API error handling and validation

**Key learning:** How text becomes numerical vectors for AI

**Test your work:** `python tests/test_task2_embeddings.py`

---

### ✅ Task 3: Vector Storage (30-45 minutes)
**File:** `backend/services/pinecone_service.py`

**What you'll implement:**
- [ ] Store embeddings in Pinecone vector database
- [ ] Project-based organization using namespaces
- [ ] Metadata storage for document information

**Key learning:** How vector databases enable fast semantic search

**Test your work:** `python tests/test_task3_vector_storage.py`

---

### ✅ Task 4: Similarity Retrieval (20-30 minutes)
**File:** `backend/services/pinecone_service.py`

**What you'll implement:**
- [ ] Semantic similarity search using cosine similarity
- [ ] Project-specific and global search capabilities
- [ ] Result ranking and formatting

**Key learning:** How AI finds relevant context for questions

**Test your work:** `python tests/test_task4_retrieval.py`

---

### ✅ Task 5: Context-Aware Generation (30-45 minutes)
**File:** `backend/routers/chat.py`

**What you'll implement:**
- [ ] Complete RAG pipeline integration
- [ ] Context injection into LLM prompts
- [ ] Response generation with document grounding

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
- The helper methods (`_extract_pdf_text`, etc.) are already implemented
- You just need to call them correctly in `_extract_text`
- For chunking, uncomment the line using `self.text_splitter.split_text(text)`
- Pay attention to error handling for different file types

### Task 2: Embedding Generation
- Use `genai.embed_content()` for both document and query embeddings
- Different `task_type` parameters optimize for different use cases
- Handle API errors gracefully (network issues, rate limits)
- Validate input text is not empty

### Task 3: Vector Storage
- Create unique IDs for each chunk: `f"{document_id}_{chunk_index}"`
- Store both preview text and full text in metadata
- Use project namespaces: `f"project_{project_id}"`
- The Pinecone `upsert` method takes a list of tuples: `(id, vector, metadata)`

### Task 4: Similarity Retrieval
- Use `self.index.query()` for similarity search
- Set `include_metadata=True` to get document information
- Handle both project-specific and global search
- Format results consistently with id, score, metadata, and text

### Task 5: RAG Generation
- Follow the 5-step pipeline: embed query → search → extract text → generate response
- Use `gemini_service.generate_query_embedding()` for queries
- Extract text from search results: `[result["text"] for result in search_results]`
- Pass context to `generate_response()` method

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