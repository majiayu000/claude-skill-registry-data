---
name: agentic-hybrid-rag
description: Classify each request as non-retrieval, single-step, or multi-step, then execute the smallest suitable grounded RAG workflow with optional rewriting, reranking, and critique.
---

# Hybrid Agentic RAG

Use the fixed classifier in `complexity` mode before execution.

## Slots

- `classifier`: select `component-classifier`.
- `retriever`: select one retriever.
- `rewriter`: optional retrieval-query rewriter.
- `reranker`: optional evidence reranker.
- `generator`: select grounded generator.
- `critic`: select answer critic for multi-step execution.

## Routes

- `non-retrieval`: call the Generator with the original query and no documents.
- `single-step`: optionally rewrite the query, retrieve once, optionally rerank, then generate.
- `multi-step`: repeatedly retrieve, accumulate new documents, optionally rerank, generate, and critique until approved, no new evidence, or `max_iterations` is reached.

Always use the original query for generation, reranking, and critique. Rewritten queries are retrieval aids only. Classifier output and generated rewrites are never evidence.

Run `scripts/workflow.py:run(request, components)` after all required slots are bound.
