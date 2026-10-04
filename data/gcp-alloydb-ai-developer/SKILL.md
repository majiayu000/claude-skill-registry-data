---
name: gcp-alloydb-ai-developer
description: "Design and build AI-powered applications on AlloyDB for PostgreSQL using AlloyDB AI — covering vector search, hybrid search (vector + full-text), AI SQL functions (ai_generate, ai_classify, ai_score, ai_embed), model endpoint management, and the AlloyDB Omni edge runtime. Prefer gcp-alloydb-cloudsql-dba for cluster operations, backup, HA, and DBA tasks; use this skill when the request is primarily about AlloyDB AI search, SQL AI functions, or embedding pipelines."
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-09"
  category: data
---

# GCP AlloyDB AI Developer

## Overview

AlloyDB AI is a collection of features built into AlloyDB for PostgreSQL that enables AI-powered search and SQL-native inference — including pgvector integration for vector similarity search, hybrid search combining vector + full-text BM25 scoring, AI SQL functions that invoke hosted models directly from SQL queries, and model endpoint management for custom or Vertex AI models.

## Core AlloyDB AI Capabilities

1. **Vector search with pgvector** — store and query embeddings using `<=>`, `<->`, `<#>` operators; HNSW and IVFFlat index types
2. **Hybrid search** — combine pgvector cosine similarity with full-text search (tsvector/tsquery) for more relevant retrieval
3. **AI SQL functions** — `google_ml.predict_row`, `google_ml.embedding`, `ai.generate_text`, `ai.classify`, `ai.score` — invoke AI models from SQL without leaving the database
4. **Model endpoint management** — register Vertex AI model endpoints or Gemini models as AlloyDB model resources; control access via IAM
5. **AlloyDB Omni** — run AlloyDB (including AlloyDB AI) on-premises or at the edge in a container

## Quick Start (pgvector + hybrid search)

```sql
-- Enable extensions
CREATE EXTENSION vector;
CREATE EXTENSION google_ml_integration;

-- Create table with embedding column
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  content TEXT,
  embedding vector(768)
);

-- Generate embeddings using AlloyDB AI function
UPDATE documents
SET embedding = google_ml.embedding('text-embedding-004', content);

-- Vector similarity search
SELECT id, content, embedding <=> $1 AS distance
FROM documents
ORDER BY distance LIMIT 10;

-- Hybrid search (vector + BM25 full-text)
SELECT id, content,
  (1 - (embedding <=> $1)) * 0.7 + ts_rank(to_tsvector(content), query) * 0.3 AS score
FROM documents, to_tsquery($2) query
WHERE to_tsvector(content) @@ query
ORDER BY score DESC LIMIT 10;
```

## Reference Directory

Load only when needed:

| Scenario | Trigger Keywords | Reference |
|---|---|---|
| Vector search setup | pgvector, embedding, similarity, HNSW, IVFFlat | references/vector-search.md |
| AI SQL functions | ai_generate, ai_classify, google_ml, predict_row | references/ai-functions.md |
| Hybrid search | hybrid, BM25, full-text, combined search | references/hybrid-search.md |
| Model endpoints | Vertex AI model, custom model, endpoint, model registry | references/model-endpoints.md |
| AlloyDB Omni | on-premises, edge, container, Omni | references/alloydb-omni.md |
| IAM & security | auth, service account, IAM, private IP, PSC | references/iam-security.md |

## Key Rules

- Always use pgvector's HNSW index for production vector search — IVFFlat requires manual reindexing as data grows
- The `google_ml_integration` extension must be enabled and the AlloyDB service account granted `roles/aiplatform.user` to call Vertex AI models from SQL
- Hybrid search weight tuning (e.g., 0.7 vector + 0.3 BM25) should be validated against your retrieval quality metrics — defaults are starting points
- AlloyDB AI functions execute synchronously within SQL transactions — avoid calling slow models in high-frequency OLTP paths
- AlloyDB Omni supports AlloyDB AI locally without Google Cloud connectivity — ideal for edge inference with pre-loaded models
- Separate the embedding pipeline (batch UPDATE) from the query path — do not regenerate embeddings on every SELECT

## Official Docs

- https://cloud.google.com/alloydb/docs/ai/overview
- https://cloud.google.com/alloydb/docs/ai/vector-embeddings
- https://cloud.google.com/alloydb/docs/omni/overview

## Security Notes

Read-only planning and advisory. Do not modify production AlloyDB schemas, model endpoint registrations, or IAM bindings without explicit approval.
