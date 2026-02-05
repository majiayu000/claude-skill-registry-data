---
name: rag-pipeline-builder
description: Complete RAG (Retrieval-Augmented Generation) pipeline implementation with document ingestion, vector storage, semantic search, and response generation. Supports FastAPI backends with OpenAI and Qdrant. LangChain-free architecture.
category: backend
version: 2.0.0
---

# RAG Pipeline Builder Skill

## Purpose

Quickly scaffold and implement production-ready RAG systems with a **pure, lightweight stack** (No LangChain):
- Intelligent document chunking (Recursive + Markdown aware)
- Vector embeddings generation (OpenAI SDK)
- Vector storage and retrieval (Qdrant Client)
- Context-aware response generation
- Streaming API endpoints (FastAPI)

## When to Use This Skill

Use this skill when:
- Building high-performance RAG systems without framework overhead.
- Needing full control over the ingestion and retrieval logic.
- Implementing semantic search for technical documentation.

## Core Capabilities

### 1. Lightweight Document Chunking

Uses a custom `RecursiveTextSplitter` implementation that mimics LangChain's logic but without the dependency bloat.

**Strategy:**
1.  **Protect Code Blocks:** Regex replacement ensures code blocks aren't split in the middle.
2.  **Recursive Splitting:** Splits by paragraphs (`\n\n`), then lines (`\n`), then sentences (`. `) to respect document structure.
3.  **Token Counting:** Uses `tiktoken` for accurate sizing compatible with OpenAI models.

**Implementation Template:**
```python
# See scripts/chunking_example.py for complete implementation

class IntelligentChunker:
    """
    Markdown-aware chunking that preserves structure (LangChain-free)
    """
    def __init__(self, chunk_size=1000, overlap=200):
        # ... (uses standalone RecursiveTextSplitter)
```

### 2. Embedding Generation (OpenAI SDK)

Direct usage of `AsyncOpenAI` client for maximum control and performance.

```python
from openai import AsyncOpenAI

class EmbeddingGenerator:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        # Direct API call with batching logic
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=batch,
        )
        return [item.embedding for item in response.data]
```

### 3. Qdrant Integration (Native Client)

Direct integration with `qdrant-client` for vector operations.

```python
from qdrant_client import QdrantClient

class QdrantManager:
    def upsert_documents(self, documents: list[dict]):
        # Batch upsert logic
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )
```

### 4. FastAPI Streaming Endpoints

Native FastAPI streaming response handling.

```python
from fastapi.responses import StreamingResponse

@app.post("/api/v1/chat")
async def chat_endpoint(request: ChatRequest):
    # ... retrieval logic ...
    
    return StreamingResponse(generate(), media_type="text/plain")
```

## Usage Instructions

### 1. Install Lightweight Dependencies

```bash
pip install -r templates/requirements.txt
```

*(Note: `langchain` is NOT required)*

### 2. Ingest Documents

```bash
# Ingest markdown files using the pure-python ingestor
python scripts/ingest_documents.py docs/ --openai-key $OPENAI_API_KEY
```

### 3. Start API Server

```bash
uvicorn templates.fastapi-endpoint-template:app --reload
```

## Performance Benefits

Removing LangChain provides:
- **Faster Startup:** Reduced import overhead.
- **Smaller Docker Image:** Significantly fewer dependencies.
- **Easier Debugging:** No complex abstraction layers or "Chains" to trace through.
- **Stable API:** You own the logic, immune to framework breaking changes.

## Output Format

When this skill is invoked, provide:
1.  **Complete Pipeline Code** (LangChain-free)
2.  **Configuration File** (.env.example)
3.  **Ingestion Script** (scripts/ingest_documents.py)
4.  **FastAPI Endpoints** (api/routes/chat.py)
5.  **Testing Script** (scripts/test_rag.py)

## Time Savings

**With this skill:** ~45 minutes to generate a highly optimized, custom RAG pipeline without framework lock-in.