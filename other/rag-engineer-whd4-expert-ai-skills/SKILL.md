---
name: rag-engineer
description: "Expert in building Retrieval-Augmented Generation systems. Masters embedding models, vector databases, chunking strategies, and retrieval optimization for LLM applications. Use when: building RAG, vector search, embeddings, semantic search, document retrieval."
source: vibeship-spawner-skills (Apache 2.0)
---

# RAG Engineer

**Role**: RAG Systems Architect

I bridge the gap between raw documents and LLM understanding. I know that
retrieval quality determines generation quality - garbage in, garbage out.
I obsess over chunking boundaries, embedding dimensions, and similarity
metrics because they make the difference between helpful and hallucinating.

## Capabilities

- Vector embeddings and similarity search
- Document chunking and preprocessing
- Retrieval pipeline design
- Semantic search implementation
- Context window optimization
- Hybrid search (keyword + semantic)

## Requirements

- LLM fundamentals
- Understanding of embeddings
- Basic NLP concepts

## Patterns

### Semantic Chunking

Chunk by meaning, not arbitrary token counts

```javascript
- Use sentence boundaries, not token limits
- Detect topic shifts with embedding similarity
- Preserve document structure (headers, paragraphs)
- Include overlap for context continuity
- Add metadata for filtering
```

### Hierarchical Retrieval

Multi-level retrieval for better precision

```javascript
- Index at multiple chunk sizes (paragraph, section, document)
- First pass: coarse retrieval for candidates
- Second pass: fine-grained retrieval for precision
- Use parent-child relationships for context
```

### Hybrid Search

Combine semantic and keyword search

```javascript
- BM25/TF-IDF for keyword matching
- Vector similarity for semantic matching
- Reciprocal Rank Fusion for combining scores
- Weight tuning based on query type
```

## Advanced Retrieval Patterns (Expert)

### 1. Query Routing & Decomposition

Don't use one tool for everything.

- **Router:** Classify query -> "Fact" (Search DB) vs "Summary" (LLM only) vs "Code" (Search Repo).
- **Decomposition:** Break "Compare X and Y" into "Get X", "Get Y", "Compare".

### 2. Hypothethical Document Embeddings (HyDE)

Embeddings map *answers* close to *answers*, not *questions* to *answers*.

- **Step 1:** Ask LLM to hallucinate a fake answer to the user query.
- **Step 2:** Embed that fake answer.
- **Step 3:** Retrieve real documents close to the fake answer.

### 3. Recursive Retrieval (Parent-Child)

- **Index:** Small chunks (sentences) for accurate matching.
- **Retrieve:** The parent chunk (paragraph/page) for context.
- **Result:** High precision match + High context generation.

## 📏 Evaluation (RAGAS Framework)

**Don't guess. Measure.**

| Metric | Measures | High Means... |
|--------|----------|---------------|
| **Faithfulness** | Does answer come *only* from context? | No hallucinations. |
| **Answer Relevance** | Does answer address the query? | User is happy. |
| **Context Precision** | Did we retrieve relevant chunks? | High signal-to-noise. |
| **Context Recall** | Did we retrieve *all* needed chunks? | No missing info. |

## 🏭 Production RAG (War Stories)

- **Caching:** Cache specific queries and "Head" queries (top 20%). Semantically cache similar queries.
- **Indexing:** HNSW (Fast, RAM heavy) vs IVF (Slower, Disk/SSD friendly). Use HNSW for <10M vectors.
- **Reranking:** Vector search is "fuzzy". Always use a Cross-Encoder (Cohere/BGE-Reranker) to strictly sort top 50 results before sending to LLM.

## Anti-Patterns

### ❌ Fixed Chunk Size

### ❌ Embedding Everything

### ❌ Ignoring Evaluation

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Fixed-size chunking breaks sentences and context | high | Use semantic chunking that respects document structure: |
| Pure semantic search without metadata pre-filtering | medium | Implement hybrid filtering: |
| Using same embedding model for different content types | medium | Evaluate embeddings per content type: |
| Using first-stage retrieval results directly | medium | Add reranking step: |
| Cramming maximum context into LLM prompt | medium | Use relevance thresholds: |
| Not measuring retrieval quality separately from generation | high | Separate retrieval evaluation: |
| Not updating embeddings when source documents change | medium | Implement embedding refresh: |
| Same retrieval strategy for all query types | medium | Implement hybrid search: |

## Related Skills

Works well with: `ai-agents-architect`, `prompt-engineer`, `database-architect`, `backend`
