---
name: rag-pipeline
description: Use when building Retrieval-Augmented Generation systems. Covers document chunking, embedding generation, vector indexing, semantic search, context building, and integration of retrieval with LLM completion for accurate Q&A on Physical AI textbook content.
---

# RAG Pipeline Skill

## Quick Start Workflow

When building or maintaining the RAG pipeline:

1. **Content Ingestion (One-time setup)**
   - Read all Docusaurus markdown files from `/docs`
   - Chunk text (800 chars, 200 overlap)
   - Generate embeddings with OpenAI ada-002
   - Upsert to Qdrant with metadata

2. **Query Flow (Runtime)**
   - Receive user question
   - Generate query embedding
   - Search Qdrant (top 5 results, score >= 0.7)
   - Build context from relevant chunks
   - Pass to OpenAI GPT-4 with context
   - Return answer + sources

3. **Continuous Improvement**
   - Monitor search quality (are results relevant?)
   - Adjust chunk size if needed
   - Update score thresholds
   - Add filters for specific chapters

### Standard Architecture

```
User Question
    ↓
[Generate Embedding]
    ↓ 
[Search Qdrant]
    ↓
[Extract Top 5 Chunks]
    ↓
[Build Context String]
    ↓
[GPT-4 with Context]
    ↓
AI Answer + Sources
```

### Key Parameters

- **Chunk size**: 800 characters
- **Overlap**: 200 characters
- **Embedding model**: `text-embedding-ada-002`
- **LLM model**: `gpt-4` or `gpt-3.5-turbo`
- **Search limit**: 5 chunks
- **Score threshold**: 0.7
- **Context window**: ~3000 tokens max

### Best Practices

For Physical AI textbook RAG:
- **Preserve code blocks** when chunking
- **Include chapter/section** in metadata
- **Cite sources** in responses
- **Cache embeddings** for popular queries
- **Log all queries** for analytics
- **Handle "no results"** gracefully

## Knowledge Base

Detailed guides available:
- **Chunking Strategies** → `references/chunking.md`
- **Ingestion Script** → `references/ingestion-script.md`
- **Query Pipeline** → `references/query-pipeline.md`
- **Context Building** → `references/context-building.md`
- **Error Handling** → `references/error-handling.md`
