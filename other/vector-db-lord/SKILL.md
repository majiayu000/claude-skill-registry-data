---
name: vector-db-lord
description: Lord skill for vector databases and RAG — DB selection, hybrid search, quantization, reranking, knowledge graphs for agentic RAG, index selection, and evaluation metrics.
triggers:
  - vector db lord
  - vector database
  - vector db
  - pinecone
  - weaviate
  - qdrant
  - milvus
  - pgvector
  - chroma
  - hybrid search
  - قاعدة بيانات متجهية
  - بحث متجهي
personas:
  - ML
  - DATA
  - ARCH
  - DEV
  - MLOPS
tech_stack: []
lord: true

---

# Vector DB Lord

[OBJ] Design and optimize vector search and RAG systems — from DB selection and hybrid search to quantization, reranking, and evaluation — for production-grade retrieval at scale.

## Problem

Vector search looks simple in a tutorial: embed, store, query. In production it breaks: pure dense search misses keyword matches, recall drops at scale, costs explode with billions of vectors, and stale embeddings return irrelevant results. RAG without hybrid search, reranking, and evaluation is a demo, not a system.

## Rules

1. [REQ] **Vector DB selection.** Pinecone serverless (managed, auto-scaling, good for start-ups), Weaviate 1.39 (hybrid built-in, modules for embeddings), Qdrant 1.13+ (Rust, fast filtering, self-hostable), Milvus (scale, billions of vectors, distributed), pgvector 0.8.2 (Postgres extension, good if already on PG), Chroma (embedded, prototyping), turbopuffer (serverless, S3-backed, cheap). Match DB to scale, hosting, and team expertise.
2. [REQ] **Hybrid search.** Combine BM25 (keyword/lexical) + dense (semantic) + sparse (learned sparse like SPLADE). Weighted fusion or reciprocal rank fusion (RRF). Pure dense misses exact keyword matches; pure BM25 misses semantic similarity. Hybrid is the default for production RAG.
3. [REQ] **Query-time rescoring.** Retrieve top-K (oversample, e.g., K=100) with fast approximate search, then rescore top-N (e.g., N=20) with a cross-encoder or ColBERT-style late interaction. Rescoring improves precision without full reranking cost.
4. [REQ] **MMR for diversity.** Use Maximal Marginal Relevance (MMR) when result diversity matters (exploratory search, recommendation). MMR balances relevance and novelty — prevents top-K from being near-duplicates. Tunable λ: 1.0 = pure relevance, 0.0 = pure diversity.
5. [REQ] **Multi-vector / ColBERT late interaction.** For high-precision retrieval, use ColBERT or multi-vector representations. Store token-level embeddings; late interaction scoring at query time. Higher storage cost but significantly better recall than single-vector.
6. [REQ] **Quantization.** Use quantization to reduce memory and speed up search: 8-bit scalar (simple, 4× memory reduction, minimal recall loss), 4-bit (more aggressive, test recall), product quantization (PQ, good for billions), binary quantization (extreme compression, use for first-stage retrieval + rescore with full vectors).
7. [REQ] **Reranking.** Always rerank top candidates with a cross-encoder model (Cohere Rerank, bge-reranker, Jina Reranker). Cross-encoders see query + document jointly, unlike bi-encoders. Reranking is the single highest-ROI step in RAG pipelines.
8. [REQ] **Knowledge graphs for agentic RAG.** For agentic RAG, combine vector search with a knowledge graph (entity-relationship). The agent retrieves entities, traverses relationships, and synthesizes. GraphRAG (Microsoft) or Neo4j + vector hybrid. Pure vector RAG misses multi-hop reasoning.
9. [REQ] **Index selection.** HNSW (default — fast query, high memory, good recall), IVF (good for billion-scale, lower recall, tunable nprobe), DiskANN (disk-based, good for large datasets that don't fit in RAM). Choose based on dataset size, latency target, and memory budget.
10. [REQ] **Filtering strategies.** Pre-filtering (filter before vector search — accurate but slow if filter is selective), post-filtering (filter after — fast but may return too few results), in-filter (filter during search — Qdrant/Weaviate support this). Use in-filtering when available; it balances speed and accuracy.
11. [REQ] **Metadata management.** Store metadata alongside vectors (source, date, tags, permissions). Filter on metadata at query time. Keep metadata schema consistent — schema drift breaks filters. Version metadata schema like any other schema.
12. [REQ] **Embedding model selection.** Match embedding model to task: general (text-embedding-3-large, bge-m3), multilingual (multilingual-e5), domain-specific (BioBERT for medical, CodeBERT for code). Benchmark on YOUR data — don't trust the model's published benchmarks.
13. [REQ] **Chunking strategies.** Chunk by semantic boundaries (paragraphs, sections) not fixed token count. Overlap chunks by 10-20% to preserve context. For code, chunk by function/class. For markdown, chunk by headers. Document the chunking strategy — it affects recall as much as the embedding model.
14. [REQ] **Evaluation metrics.** Measure: recall@k (did the relevant doc appear in top-k?), nDCG (graded relevance, position-weighted), MRR (mean reciprocal rank, for single-relevant-answer queries). Evaluate on a held-out test set with human-labeled relevance. No RAG system ships without retrieval evaluation.
15. [REQ] **Cost optimization.** Quantize vectors (8-bit or PQ), use serverless where possible (Pinecone serverless, turbopuffer), cache frequent queries, batch embedding API calls, use smaller embedding models for first-stage retrieval + larger for reranking. Monitor cost per 1K queries.
16. [REQ] **Scaling strategies.** Vertical (bigger machine — HNSW in RAM) up to ~10M vectors. Horizontal sharding (partition by metadata or hash) for >10M. Disk-based (DiskANN) for datasets >RAM. Hybrid: hot data in RAM (HNSW), cold data on disk (DiskANN). Plan scaling before you need it.
17. [REQ] **Incremental updates.** Support incremental insert/update/delete without rebuilding the index. HNSW supports this natively. For IVF, periodic rebuild needed. Document the update strategy — stale vectors return stale results.
18. [PROHIBIT] Deploying a RAG system without hybrid search, reranking, and a retrieval evaluation test set — pure dense search without evaluation is a prototype, not production.

## References

- Pinecone: https://pinecone.io
- Weaviate: https://weaviate.io
- Qdrant: https://qdrant.tech
- Milvus: https://milvus.io
- pgvector: https://github.com/pgvector/pgvector
- Chroma: https://trychroma.com
- turbopuffer: https://turbopuffer.com
- GraphRAG: https://github.com/microsoft/graphrag
- ColBERT: https://github.com/stanford-futuredata/ColBERT
