---
name: vector-db-ops
description: Use when vector database operations — Pinecone, Weaviate, Qdrant, ChromaDB.
  Indexing, querying, filtering, and managing vector embeddings for RAG and similarity
  search. Use when working with vector db ops.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- infrastructure
- memory
- ops
- self-improvement
- vector
version: 1.0.0
category: core
---


## Overview

Vector database operations for AI applications. Covers embedding generation, index creation, metadata filtering, hybrid search, and production deployment across Pinecone, Weaviate, Qdrant, and ChromaDB.

## Capabilities

- Generate and store vector embeddings from text, images, and code
- Create and manage collections with metadata schemas
- Perform semantic similarity search with filters
- Implement hybrid search (dense + sparse vectors)
- Optimize index parameters for speed and recall
- Manage vector database lifecycle (backup, scaling, monitoring)

## When to Use
**Trigger phrases:**
- "vector db ops"
- "Vector database operations — Pinecone, Weaviate, Qdrant, ChromaDB"


- Building RAG (Retrieval-Augmented Generation) systems
- Implementing semantic search for documents or products
- Creating recommendation engines based on similarity
- Building memory systems for AI agents
- Implementing image/code similarity search

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Pinecone
```python
import pinecone
from openai import OpenAI

# Initialize
pc = pinecone.Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("my-index")

# Upsert vectors
openai = OpenAI()
response = openai.embeddings.create(input=["text"], model="text-embedding-3-small")
embeddings = response.data[0].embedding

index.upsert(vectors=[{
    "id": "doc-1",
    "values": embeddings,
    "metadata": {"source": "pdf", "page": 42}
}])

# Query
results = index.query(vector=query_embedding, top_k=10, include_metadata=True,
                       filter={"source": {"$eq": "pdf"}})
```

### Qdrant
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

client = QdrantClient(":memory:")  # or url="http://localhost:6333"

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Insert
client.upsert(collection_name="documents", points=[
    PointStruct(id=1, vector=embedding, payload={"text": "hello", "category": "greeting"})
])

# Search with filter
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(must=[FieldCondition(key="category", match=MatchValue(value="greeting"))]),
    limit=5,
)
```

### ChromaDB (Local)
```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docs")

# Add documents
collection.add(
    documents=["Document text here"],
    metadatas=[{"source": "web"}],
    ids=["doc-1"],
)

# Query
results = collection.query(query_texts=["search query"], n_results=5)
```

### Hybrid Search (Pinecone)
```python
from pinecone import SparseVector

# Dense + sparse hybrid
results = index.query(
    vector=dense_embedding,
    sparse_vector=SparseVector(indices=[1, 5, 10], values=[0.1, 0.3, 0.2]),
    top_k=10,
    alpha=0.7,  # 0=sparse only, 1=dense only
)
```

### Chunking Strategy
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_text(document)
```

## Common Patterns
- Use structured input/output schemas for reliable automation
- Add retry logic with exponential backoff for external calls
- Validate inputs before processing to fail fast
- Log execution steps for debugging and auditing


### Embedding Models
- OpenAI `text-embedding-3-small` (1536 dim) — good balance
- OpenAI `text-embedding-3-large` (3072 dim) — highest quality
- Cohere `embed-v3` (1024 dim) — multilingual
- Local: `sentence-transformers/all-MiniLM-L6-v2` (384 dim)

### Index Tuning
- HNSW: fast approximate search, good for most use cases
- IVF: better for very large datasets
- PQ (Product Quantization): memory-efficient for billions of vectors

### Production Considerations
- Batch upserts (100-1000 vectors per call)
- Metadata filtering before vector search for efficiency
- Monitor recall@k metrics
- Implement re-ranking for precision

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |