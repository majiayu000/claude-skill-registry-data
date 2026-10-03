---
name: component-bge-reranker
description: Rerank candidate documents by cross-encoder relevance score with a local BGE reranker model (BAAI/bge-reranker-large). Use after first-stage retrieval when semantic precision matters more than latency.
---

# BGE Reranker Component

Provide the `reranker` capability for an Agentic RAG slot.

## Interface

Input `RerankRequest`:

- `query`: original retrieval query
- `documents`: JSON-compatible documents containing `id` and `text`
- `top_k`: maximum returned documents
- optional `model`, `batch_size`, `max_length`, `device`

Output `RerankResult`:

- `documents`: documents re-ranked by normalized cross-encoder `score`

## Execution

Run `scripts/component.py:run(inputs, context)`. The Component lazily loads the local BGE cross-encoder and scores `(query, passage)` pairs with a Sigmoid-normalized relevance score. It performs reranking only; do not use it for first-stage retrieval or generation.
