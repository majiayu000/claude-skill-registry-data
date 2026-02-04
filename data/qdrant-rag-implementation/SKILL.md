---
name: qdrant-rag-implementation
description: This skill provides guidance for implementing robust Qdrant vector database integration with RAG (Retrieval Augmented Generation) systems, including proper async client handling, error management, and performance optimization.
---

# Qdrant RAG Implementation Skill

## Purpose

This skill provides comprehensive guidance for implementing robust Qdrant vector database integration with RAG (Retrieval Augmented Generation) systems, including proper async client handling, error management, and performance optimization.

## When to Use This Skill

This skill should be used when implementing or troubleshooting Qdrant vector database integrations in RAG systems, particularly when facing issues with:
- Async/sync OpenAI client compatibility
- Qdrant method parameter errors
- Connection and timeout issues
- Performance optimization for vector operations
- Embedding dimension validation
- Batch processing of documents

## How to Use This Skill

### Initialize Qdrant Client Properly

1. Configure timeout parameters at initialization:
```python
from qdrant_client import QdrantClient

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
    timeout=30,           # Global timeout in seconds
    grpc_port=6334,       # gRPC port for faster communication
    prefer_grpc=True      # Use gRPC for better performance
)
```

2. Use appropriate timeout parameters for specific methods:
```python
# These methods accept timeout parameter:
- create_collection(timeout=30)
- delete_collection(timeout=30) 
- query_points(timeout=30)
- info(timeout=30)

# These methods do NOT accept timeout parameter (use client's global timeout):
- get_collections()
- get_collection()
- upsert()
```

### Handle Async OpenAI Clients Correctly

When working with AsyncOpenAI clients (like Qwen):

1. Properly await API calls since the `create` method itself is async:
```python
# For AsyncOpenAI clients, the create method is inherently async
response = await self.client.chat.completions.create(
    model=self.model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=500,
    temperature=0.1
)
```

2. Do NOT use `acreate` method with AsyncOpenAI clients, as it doesn't exist.

### Qdrant Method Updates

Use current Qdrant client methods:

1. Replace deprecated `search` with `query_points`:
```python
# OLD (deprecated):
search_results = self.client.search(
    collection_name=self.collection_name,
    query_vector=query_embedding,
    limit=limit
)

# NEW (current):
search_results = self.client.query_points(
    collection_name=self.collection_name,
    query=query_embedding,  # parameter renamed from query_vector
    limit=limit,
    timeout=self.timeout
)
# Access results via search_results.points instead of search_results
```

2. Use `info()` for health checks instead of non-existent `health()`:
```python
# For health checks:
info = self.client.info()  # No timeout parameter
return {
    "status": "healthy",
    "version": getattr(info, 'version', 'unknown'),
    "commit": getattr(info, 'commit', 'unknown')
}
```

### Proper ID Handling for Qdrant

Qdrant requires integer IDs, not string UUIDs:

```python
# Convert string IDs to integer format
def get_point_id(chunk_id, content=""):
    try:
        # Try to convert to integer if possible
        return int(chunk_id) if chunk_id.isdigit() else hash(chunk_id) % (10**9)
    except (ValueError, AttributeError):
        # Fallback to hash of content
        import hashlib
        return int(hashlib.md5(content.encode()).hexdigest(), 16) % (10**9)

point_id = get_point_id(chunk.chunk_id, chunk.content)
```

### Embedding Dimension Validation

Verify embedding dimensions match collection configuration:

```python
def validate_embedding_dimensions(self, embedding: List[float], expected_size: int = 384):
    if len(embedding) != expected_size:
        raise ValueError(f"Embedding dimension mismatch: got {len(embedding)}, expected {expected_size}")
```

### Batch Processing for Performance

Process multiple documents in batches for better performance:

```python
def store_document_chunks(self, chunks: List[DocumentChunk]) -> bool:
    batch_size = 64  # Recommended batch size
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        # Convert and prepare points for this batch
        points = []
        for chunk in batch:
            points.append(models.PointStruct(
                id=get_point_id(chunk.chunk_id, chunk.content),
                vector=chunk.embedding,
                payload={
                    "content": chunk.content,
                    "doc_path": chunk.doc_path,
                    "metadata": chunk.metadata
                }
            ))
        
        # Upload batch to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
```

### Comprehensive Error Handling

Implement proper error handling throughout the system:

1. In VectorStore operations:
```python
def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
    try:
        # Validate embedding dimensions
        self.validate_embedding_dimensions(query_embedding)
        
        # Perform search with timeout
        search_results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
            timeout=self.timeout
        )

        # Format results
        results = []
        for result in search_results.points:
            results.append({
                "content": result.payload["content"],
                "doc_path": result.payload["doc_path"],
                "metadata": result.payload.get("metadata", {}),
                "score": result.score
            })
        
        return results
    except Exception as e:
        logging.error(f"Failed to search in vector store: {e}")
        return []
```

2. In RAGService with async handling:
```python
async def query(self, query_text: str, top_k: int = 5) -> QueryResponse:
    try:
        # Validate inputs
        if not query_text or not query_text.strip():
            return QueryResponse(answer="Please provide a query", sources=[], metadata={})
        
        # Generate embedding
        from data.embeddings import EmbeddingService
        embedding_service = EmbeddingService()
        query_embedding = embedding_service.embed_text(query_text)
        
        # Verify vector store connection
        if not self.vector_store.check_connection():
            return QueryResponse(answer="Service temporarily unavailable", sources=[], metadata={})
        
        retrieved_docs = self.vector_store.search(query_embedding, limit=top_k)
        
        if not retrieved_docs:
            return QueryResponse(answer="I don't know", sources=[], metadata={"retrieved_docs_count": 0})
        
        # Generate response with async API call
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant..."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        # Process and return response
        return QueryResponse(
            answer=response.choices[0].message.content.strip(),
            sources=list(set([doc["doc_path"] for doc in retrieved_docs])),
            metadata={
                "retrieved_docs_count": len(retrieved_docs),
                "sources_count": len(set([doc["doc_path"] for doc in retrieved_docs]))
            }
        )
    except Exception as e:
        logging.error(f"Error in query processing: {e}")
        return QueryResponse(
            answer="An error occurred while processing your query",
            sources=[],
            metadata={"error": str(e)}
        )
```

### Global Service Instance Pattern

For performance, use global service instances instead of creating on each request:

```python
# In main.py - create global instances once
vector_store = VectorStore(collection_name="Humanoids", timeout=30)
rag_service = RAGService(vector_store_collection="Humanoids", vector_store_timeout=30)
rag_service.set_vector_store(vector_store)

# In endpoints, use the global instances
@app.post("/api/query")
async def handle_query(req: QueryRequest):
    try:
        rag_result = await rag_service.query(req.query)
        # Process result...
    except Exception as e:
        logging.error(f"RAG query failed: {e}")
        # Handle gracefully...
```

### Collection Management

Properly manage Qdrant collections with verification:

```python
def _ensure_collection_exists(self):
    try:
        # Check if collection exists using global timeout
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        collection_exists = self.collection_name in collection_names
        
        if not collection_exists:
            # Create collection with proper configuration
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
                timeout=self.timeout
            )
        else:
            # Verify collection configuration matches expected settings
            collection_info = self.client.get_collection(collection_name=self.collection_name)
            # Add validation logic here...
    except Exception as e:
        logging.error(f"Failed to manage collection: {e}")
        raise
```