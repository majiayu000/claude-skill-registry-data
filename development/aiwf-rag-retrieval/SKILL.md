---
name: aiwf-rag-retrieval
description: Use for retrieval-augmented generation, embeddings, chunking, document ingestion, semantic or hybrid search, reranking, citations, context packs, retrieval evaluation, embedding-model migration, and debugging missing, stale, duplicated, or poorly grounded results.
---

# AIWF RAG Retrieval

## Core Rule

Treat retrieval as a reproducible data contract. Record corpus version, source identity, parser, chunking policy, embedding model and revision, vector dimension, normalization, distance metric, index settings, filters, reranker, and prompt context format before tuning results.

## Workflow

1. Inspect source manifests, ingestion code, stable document and chunk IDs, embedding configuration, vector backend, query path, filters, reranker, context builder, citations, and existing eval queries.
2. Reproduce one failing or representative query. Capture retrieved IDs, scores, metadata, order, and final context before changing the pipeline.
3. Separate failure classes: source missing, parse failure, bad chunk boundary, stale index, embedding mismatch, filter bug, approximate-index recall, reranker issue, or generation-grounding failure.
4. Change one retrieval variable at a time and compare against a fixed query set.
5. Rebuild or migrate indexes deliberately when embedding identity, vector dimension, distance metric, chunking, or canonical IDs change.

## Guardrails

- Never mix vectors from different embedding models or revisions without separate named spaces and explicit routing.
- Store embedding identity and chunking version with the index. A collection name alone is not provenance.
- Keep raw source, parsed document, chunk, embedding, and generated answer identifiers traceable.
- Do not claim better retrieval from a few appealing answers. Measure retrieval quality before answer style.
- Preserve access-control and tenant filters before semantic ranking.
- Keep source citations bound to retrieved source IDs; do not let the model invent URLs or document names.
- Add `aiwf-data-storage` for schema, migration, transaction, backup, or vector-backend changes and `aiwf-ai-evals` for promotion gates.

## Validation

Use a small frozen query set with relevant document IDs. Report retrieval metrics such as recall at k, precision at k, reciprocal rank, latency, duplicate rate, and no-result behavior when they fit the project. For answer evaluation, also check citation correctness and whether each material claim is supported by retrieved context.

## Primary Sources

- Chroma embedding functions: https://docs.trychroma.com/docs/embeddings/embedding-functions
- Chroma collection configuration: https://docs.trychroma.com/docs/collections/configure
- Qdrant collections and vector contracts: https://qdrant.tech/documentation/manage-data/collections/
- pgvector: https://github.com/pgvector/pgvector
