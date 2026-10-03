---
name: agentic-conditional-rag
description: Route each RAG request at runtime to lexical, semantic, or hybrid retrieval, with an optional rewriter for semantic retrieval, optional reranking, and grounded generation. Use when the best retrieval strategy cannot be fixed before execution.
---

# Conditional RAG Agentic Skill

Route each request at runtime through exactly one of three retrieval strategies: `lexical`, `semantic`, or `hybrid`.

## Slot Binding

Bind the slots as follows:

- `classifier`: select `component-classifier`.
- `rewriter`: optionally select `component-hyde-rewriter`.
- `lexical_retriever`: select `component-bm25-retriever`.
- `semantic_retriever`: select `component-vector-retriever`.
- `reranker`: optionally select `component-bge-reranker`.
- `generator`: select `component-grounded-generator`.

Do not exchange the lexical and semantic Retriever bindings.

## Routing

Call `classifier` first with the original query and routing constraints.

- `lexical`: do not call the Rewriter. Send the original query only to `lexical_retriever`.
- `semantic`: if a Rewriter is bound, send its non-empty `rewritten_query` only to `semantic_retriever`; otherwise send the original query.
- `hybrid`: send the original query to `lexical_retriever`; send the optional rewritten query, or the original query when no Rewriter is bound, to `semantic_retriever`; fuse the two ranked lists with reciprocal rank fusion.

Reject any classifier route other than `lexical`, `semantic`, or `hybrid`.

## Evidence Safety

The Classifier result and Rewriter output control routing and retrieval only. They are never evidence documents.

Always use the original query for optional reranking and final generation. Pass only real documents returned by the Retriever slots to the Reranker and Generator.

## Execution

Run `scripts/workflow.py:run(request, components)` after every required slot is bound. Record classification, rewriting, retrieval, fusion, reranking, and generation decisions in the returned trace.