---
name: qdrant-vectordb
description: Use when working with Qdrant vector database for semantic search and RAG. Covers collection setup, embedding generation, vector upsert/search, HNSW indexing, filtering, and integration with OpenAI embeddings for textbook content retrieval.
---

# Qdrant Vector Database Skill

## Quick Start Workflow

When working with Qdrant:

1. **Check if Qdrant is configured**
   - Look for `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
   - For local: `http://localhost:6333`
   - For cloud: `https://xxx.qdrant.io`

2. **For collection creation**
   - Define vector size (1536 for OpenAI ada-002)
   - Choose distance metric (Cosine for semantic similarity)
   - Set up HNSW parameters for performance

3. **For content ingestion**
   - Chunk text into 800-character segments with 200-char overlap
   - Generate embeddings with OpenAI `text-embedding-ada-002`
   - Upsert vectors with metadata (chapter, section, file path)

4. **For semantic search**
   - Convert user query to embedding
   - Search with score threshold (>= 0.7 for relevance)
   - Return top 5 results with metadata

### Standard Patterns

#### Client Setup
```typescript
import { QdrantClient } from '@qdrant/js-client';

export const qdrant = new QdrantClient({
  url: process.env.QDRANT_URL,
  apiKey: process.env.QDRANT_API_KEY,
});
```

#### Collection Configuration
```typescript
await qdrant.createCollection('textbook_chunks', {
  vectors: {
    size: 1536, // OpenAI ada-002
    distance: 'Cosine',
  },
  hnsw_config: {
    m: 16,
    ef_construct: 100,
  },
});
```

### Best Practices

For Physical AI textbook RAG:
- **Collection name**: `textbook_chunks`
- **Vector size**: 1536 (OpenAI ada-002 embeddings)
- **Chunk size**: 800 characters with 200 overlap
- **Score threshold**: 0.7 minimum for relevance
- **Batch size**: 100 vectors per upsert operation
- **Metadata**: Always include chapter, section, file path

## Knowledge Base

For detailed information, see:
- **Docker Setup** → `references/docker-setup.md`
- **Collection Management** → `references/collections.md`
- **Embedding Generation** → `references/embeddings.md`
- **Search Patterns** → `references/search-patterns.md`
- **Performance Tuning** → `references/performance.md`
