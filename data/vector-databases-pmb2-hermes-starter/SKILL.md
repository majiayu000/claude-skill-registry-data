---
name: vector-databases
description: "Use when working with vector databases (ChromaDB, Qdrant, Weaviate, Pinecone) for RAG, semantic search, and AI application backends. Covers setup, ingestion, querying, and optimization."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vector-databases, RAG, semantic-search, embeddings, chromadb, qdrant, weaviate, pinecone]
    triggers: [vector-database, RAG, semantic-search, embeddings, chromadb, qdrant, weaviate, pinecone, similarity-search]
    related_skills: [llama-cpp, dspy, huggingface-hub, obsidian, hermes-agent]
platforms: [linux, macos, windows]
---

# Vector Databases for AI Applications

## Overview

Vector databases store and retrieve high-dimensional embeddings — numerical representations of text, images, or audio. They power **Retrieval-Augmented Generation (RAG)**, semantic search, recommendation systems, and memory for AI agents. This skill covers the most common open-source vector databases and how to use them from the Hermes agent environment.

## When to Use

- Adding semantic search or RAG to an AI application
- Building agent memory that retrieves by similarity, not keyword
- Setting up embedding pipelines for document ingestion
- Choosing between ChromaDB (simple, embedded), Qdrant (self-hosted), Weaviate (graph + vector), or Pinecone (managed)
- Debugging retrieval quality — wrong results, missing chunks, slow queries

**Don't use for:** Keyword/full-text search (Postgres FTS5 or Elasticsearch is better). Exact-match lookups (use a regular database index). Very small datasets (<100 items, where brute-force cosine similarity in numpy is sufficient).

## Quick Comparison

| Database | Type | Hosting | Python Client | Best For |
|---|---|---|---|---|
| **ChromaDB** | Embedded / Client-server | Local or cloud | `chromadb` | Quick prototyping, single-user, small-medium datasets |
| **Qdrant** | Vector engine | Self-hosted or cloud | `qdrant-client` | Production, filtering + hybrid search, performance |
| **Weaviate** | Vector + graph | Self-hosted or cloud | `weaviate-client` | Multi-modal data, needs metadata graph traversal |
| **Pinecone** | Managed vector DB | Cloud-only | `pinecone` | Zero-ops, high-scale, enterprise |
| **PGVector** | Postgres extension | Any Postgres | `pgvector` | Already-using-Postgres, simple setup |

## Quick Start — ChromaDB (Simplest On-Ramp)

```python
import chromadb

# In-memory (ephemeral)
client = chromadb.Client()
collection = client.create_collection("my_docs")

# Add documents with auto-generated IDs
collection.add(
    documents=["This is a document about cats", "This is about dogs"],
    metadatas=[{"source": "wiki"}, {"source": "wiki"}],
    ids=["doc1", "doc2"]
)

# Query
results = collection.query(query_texts=["feline animals"], n_results=2)
print(results["documents"][0])  # → ["This is a document about cats", ...]
```

### Persistent ChromaDB (Survives Restarts)

```python
client = chromadb.PersistentClient(path="./chroma_data")
```

## Quick Start — Qdrant (Self-Hosted)

```bash
# Start with Docker
docker run -p 6333:6333 qdrant/qdrant
```

```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

client = QdrantClient("localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# Insert with pre-computed embeddings
client.upsert(
    collection_name="my_collection",
    points=[
        PointStruct(id=1, vector=[0.1] * 384, payload={"text": "hello world"}),
    ],
)

# Search
results = client.search(
    collection_name="my_collection",
    query_vector=[0.1] * 384,
    limit=5,
)
```

## Embedding Models Compatible with Hermes

| Model | Dimensions | Provider | Use Case |
|---|---|---|---|
| `all-MiniLM-L6-v2` | 384 | Sentence-Transformers | General purpose, fast |
| `text-embedding-ada-002` | 1536 | OpenAI API | Cloud, high quality |
| `BAAI/bge-small-en-v1.5` | 384 | Sentence-Transformers | BGE family, retrieval |
| `intfloat/e5-mistral-7b-instruct` | 4096 | Sentence-Transformers | Highest quality (slow) |
| LLM embedding passthrough | varies | llama.cpp | Local only, no extra model |

**Tip:** Match dimensions to your vector DB config. ChromaDB auto-detects from the first insert; Qdrant/Pinecone require explicit `vector_size` on collection creation.

## RAG Pipeline Template

```python
# 1. Load documents
documents = [
    {"text": "...", "metadata": {"source": "file1.md"}},
    # ...
]

# 2. Chunk into segments
chunks = []
for doc in documents:
    for i in range(0, len(doc["text"]), 500):  # 500-char chunks
        chunk = doc["text"][i:i+500]
        chunks.append({"text": chunk, **doc["metadata"]})

# 3. Embed and store (using ChromaDB)
import chromadb
client = chromadb.Client()
collection = client.create_collection("rag_kb")
collection.add(
    documents=[c["text"] for c in chunks],
    metadatas=[{"source": c["source"]} for c in chunks],
    ids=[f"chunk_{i}" for i in range(len(chunks))],
)

# 4. Query at runtime
def retrieve(query: str, k: int = 5):
    results = collection.query(query_texts=[query], n_results=k)
    return results["documents"][0]

# 5. (Optional) Pass retrieved context to LLM
context = retrieve("user's question")
prompt = f"Context: {context}\n\nQuestion: ...\nAnswer:"
```

## Common Pitfalls

1. **Embedding dimension mismatch.** ChromaDB auto-derives dimensions from the first insert, but Qdrant/Weaviate/Pinecone require explicit declaration. If you change embedding models later, you must create a new collection with the new dimension.

2. **Chunk size affects retrieval quality.** Too small (< 100 chars) → context is fragmented. Too large (> 2000 chars) → noise drowns the signal. 500-1000 chars is a good starting point. Overlap chunks by 10-20% to avoid cutting sentences in half.

3. **No re-ranking.** Raw vector similarity returns results based on embedding proximity, which may not match actual relevance. For production RAG, add a cross-encoder re-ranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) after the initial vector search.

4. **Forgetting to install the client.** Each vector DB requires its own Python package. `pip install chromadb` / `qdrant-client` / `weaviate-client` / `pinecone` / `pgvector`.

5. **Pinecone free tier limits.** The Pinecone free tier (Starter) has a max of 1 pod index with limited storage. For non-production, ChromaDB or local Qdrant is more flexible.

6. **Hybrid search requires careful tuning.** Qdrant and Weaviate support keyword + vector hybrid search, but the weighting (`alpha` parameter) needs tuning per dataset. Start with `alpha=0.75` (75% vector, 25% keyword) and adjust based on recall evaluations.

## Verification Checklist

- [ ] Client connects without error (`client.get_collections()` or `.get_collection_info()`)
- [ ] Documents insert and return a valid ID/UUID
- [ ] Query with a semantically related text returns expected results at position 0-1
- [ ] Correct embedding model dimensions match the vector DB config
- [ ] RAG pipeline returns context relevant to the user's question
- [ ] Empty/edge-case queries return gracefully (e.g., no docs → empty list, not a crash)

## Related Skills

- `llama-cpp` — Local inference for embedding generation and LLM RAG
- `dspy` — Declarative LM programs that can use vector retrieval as a module
- `huggingface-hub` — Download embedding models from HuggingFace
- `obsidian` — Knowledge base built from local notes (vectorize with this skill)
- `hermes-agent` — Configure Hermes agent with memory/retrieval backends
