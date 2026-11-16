---
name: jamwithai--production-agentic-rag
description: "Production-grade RAG system patterns — keyword search foundations + vector hybrid retrieval, FastAPI, OpenSearch, Airflow pipelines. Dùng khi build RAG cho production."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Production RAG system architecture từ "The Mother of AI Project" course.

## Core principle

> Build RAG the professional way: solid keyword search foundations first, then enhance with vectors — not AI-first approaches that skip search fundamentals.

## Stack

```
FastAPI          — API layer
PostgreSQL       — metadata store
OpenSearch       — BM25 keyword + vector hybrid search
Airflow          — data pipeline orchestration
Docker Compose   — full local stack
```

## Architecture phases

1. **Infrastructure** — Docker, FastAPI, PostgreSQL, OpenSearch, Airflow
2. **Data pipeline** — automated fetch + parse (arXiv papers or any domain)
3. **BM25 keyword search** — production search with filtering + relevance scoring
4. **Vector search** — semantic embeddings layer on top of keyword
5. **Hybrid retrieval** — combine BM25 + vector for best results
6. **Agentic RAG** — agent loop with tool use on top of retrieval

## Key patterns

```python
# Hybrid search: keyword + semantic
results = hybrid_search(
    query=user_query,
    bm25_weight=0.4,
    vector_weight=0.6,
    top_k=10
)
```

## Source

https://github.com/jamwithai/production-agentic-rag-course
