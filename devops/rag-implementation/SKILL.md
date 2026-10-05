---
name: rag-implementation
description: Design, implement, and evaluate retrieval-augmented generation with traceable ingestion, privacy-aware indexing, hybrid retrieval, grounded answers, and.
license: MIT
---

# Retrieval-Augmented Generation

## Contract and corpus

Define users/questions, answer/citation requirements, freshness, latency/cost, permissions, deletion, languages, and failure policy. Inventory source ownership, formats, versioning, sensitive data, access controls, and update cadence. Do not index content the application is not authorized to reveal.

## Pipeline

1. Parse deterministically and preserve source ID, version/hash, page/section/line, title, ACL, and timestamps.
2. Chunk on semantic/structural boundaries with limited overlap; keep tables/code and parent context intentionally.
3. Build a lexical baseline. Add embeddings only when evaluation shows benefit; keep backend/model configurable and record exact versions.
4. Filter by authorization before retrieval and again before answer assembly.
5. Retrieve bounded candidates, combine lexical/semantic ranks when useful, rerank a small set, diversify duplicates, and pass only relevant evidence.
6. Instruct the answer layer to use provided evidence, cite source IDs/ranges, distinguish inference, and abstain when support is insufficient.
7. Incrementally update by content hash and remove stale/deleted chunks and caches.

External embedding/vector/reranking services require authorization and a privacy/retention review. Do not install infrastructure or send private corpora outside the approved boundary automatically.

## Evaluation

Create labeled queries with relevant sources and expected abstentions. Measure retrieval recall@k/MRR or nDCG, citation correctness, answer support, unsupported-claim rate, ACL leakage, freshness, latency, cost, and failure recovery. Compare no-retrieval, lexical, semantic, and hybrid baselines. Test injection inside documents, conflicting sources, stale updates, deleted documents, and permission changes.

## Completion report

Document corpus/provenance, parser/chunker, index and versioning, ACL/deletion, retrieval/reranking, prompt/output contract, evaluation results, observability, deployment/rollback, and unresolved coverage.
