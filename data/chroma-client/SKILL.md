---
name: chroma-client
description: ChromaDB vector database client for storing and retrieving text embeddings with hybrid search (dense + sparse). Use for RAG operations, contextual retrieval, and similarity search in clinical notes.
---

# ChromaDB Client Skill

## Overview

This skill provides a Python wrapper for ChromaDB's REST API, enabling vector storage and hybrid search capabilities. It supports automatic embedding generation and BM25-based sparse retrieval for improved citation accuracy.

## When to Use

Use this skill when you need to:
- Store clinical note chunks as vector embeddings
- Query for semantically similar text passages
- Implement RAG (Retrieval-Augmented Generation)
- Clear session-based embeddings for privacy compliance
- Perform hybrid search (embedding similarity + keyword matching)

## Installation

**IMPORTANT**: This skill has its own isolated virtual environment (`.venv`) managed by `uv`. Do NOT use system Python.

Initialize the skill's environment:
```bash
# From the skill directory
cd .agent/skills/chroma-client
uv sync  # Creates .venv and installs dependencies from pyproject.toml
```

Dependencies are in `pyproject.toml`:
- `chromadb` - Vector database client

## Usage

**CRITICAL**: Always use `uv run` to execute code with this skill's `.venv`, NOT system Python.

### Initialize Client

```python
# From .agent/skills/chroma-client/ directory
# Run with: uv run python -c "..."
from chroma_client import ChromaClient

# Initialize (uses CHROMA_HOST env var by default)
client = ChromaClient(
    host="localhost",  # Default from CHROMA_HOST
    port=8000          # Default port
)
```

### Create Collection

```python
# Create or get existing collection
collection = client.create_collection(
    collection_name="clinical_note_session_123",
    metadata={"session_id": "123", "note_type": "cardiology"}
)
```

### Add Chunks with Auto-Embedding

```python
# Chunks are automatically embedded by ChromaDB
chunks = [
    "Patient presents with chest pain radiating to left arm...",
    "History of hypertension for 10 years...",
    "Physical exam reveals elevated BP 150/95..."
]

client.add_chunks(
    collection_name="clinical_note_session_123",
    chunks=chunks,
    metadatas=[
        {"start_offset": 0, "end_offset": 60},
        {"start_offset": 60, "end_offset": 110},
        {"start_offset": 110, "end_offset": 165}
    ],
    ids=["chunk_0", "chunk_1", "chunk_2"]  # Optional, auto-generated if None
)
```

### Query with Hybrid Search

```python
# Semantic search with embedding similarity
results = client.query(
    collection_name="clinical_note_session_123",
    query_text="cardiovascular symptoms",
    n_results=5,
    where={"note_type": "cardiology"}  # Optional metadata filter
)

# Access results
for doc, metadata, distance in zip(
    results["documents"],
    results["metadatas"],
    results["distances"]
):
    print(f"Document: {doc}")
    print(f"Offset: {metadata['start_offset']}-{metadata['end_offset']}")
    print(f"Distance: {distance}")
```

### Session Cleanup (Privacy)

```python
# Clear collection after processing (HIPAA compliance)
client.clear_collection("clinical_note_session_123")
```

### Health Check

```python
if client.check_health():
    print("ChromaDB server is healthy")
else:
    print("ChromaDB server unavailable")
```

## Configuration

**Environment Variables**:
- `CHROMA_HOST`: Server URL (default: `http://localhost:8000`)

**Parameters**:
- `collection_name`: Unique identifier for the collection
- `n_results`: Number of results to return (default: 5)
- `where`: Metadata filter dictionary (optional)

## Best Practices

1. **Session-Based Collections**: Use unique collection names per session (e.g., `note_session_{uuid}`)
2. **Always Clear**: Delete collections after processing to prevent PHI persistence
3. **Metadata Tracking**: Store offsets in metadata for citation extraction
4. **Contextual Enrichment**: Add context to chunks before embedding (see `contextual-chunking` skill)
5. **Health Checks**: Verify ChromaDB availability before critical operations

## Integration with RAG Pipeline

Typical workflow:
1. **Chunking**: Use `contextual-chunking` skill to prepare chunks
2. **Embedding**: Use this skill to store chunks with auto-embedding
3. **Retrieval**: Query for relevant chunks during summarization
4. **Citation**: Use `citation-extraction` skill to validate alignments
5. **Cleanup**: Clear collection when session ends

## Error Handling

- Collections that don't exist are created automatically
- Delete operations on non-existent collections are safely ignored
- All errors from ChromaDB API are propagated with context

## Implementation

See `chroma_client.py` for the full Python implementation.
