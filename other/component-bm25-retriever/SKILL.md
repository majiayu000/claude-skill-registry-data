---
name: component-bm25-retriever
description: Retrieve and rank title-and-text documents with a field-aware BM25F implementation. Use for exact names, identifiers, quotations, rare terms, and queries with reliable lexical overlap.
---

# BM25F Retriever Component

Provide the `retriever` capability for an Agentic RAG slot.

## Interface

Input `RetrievalRequest`:

- `query`: retrieval query
- `documents`: JSON-compatible documents containing `id` and `text`
- `top_k`: maximum returned documents
- optional `k1` and `b` for saturation and body-length normalization
- optional `title_boost` and `title_b` for title weighting and normalization

Defaults are `top_k=10`, `k1=1.2`, `b=0.5`, `title_b=0.75`, and
`title_boost=3.0`. These are the B3 parameters selected by the frozen retrieval
benchmark; callers may override every value.

Output `RetrievalResult`:

- `documents`: ranked document dictionaries with BM25F `score`

## Execution

Run `scripts/component.py:run(inputs, context)`. Title and text term frequencies are
normalized against their own field lengths before being combined. This Component
performs retrieval only. Do not choose other Skills or generate an answer.
