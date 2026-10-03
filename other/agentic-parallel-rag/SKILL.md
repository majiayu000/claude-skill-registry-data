---
name: agentic-parallel-rag
description: Arrange parallel RAG with optional LLM query rewriting, two to four parallel retrieval branches, optional per-branch reranking, reciprocal rank fusion, and grounded generation. Use when complementary retrieval routes or multiple query views should be combined.
---

# Parallel RAG Workflow

Use this Skill only after the Manage stage selects it. Keep retrieval, reranking,
rewriting, and generation implementations outside the workflow script.

## Component selection

1. Optionally select one `rewriter` Component when rewriting or decomposing the
   query improves recall. When no `rewriter` is bound, every branch starts from
   the original query.
2. Select two to four distinct `retriever` Components. Prefer diversity, such as
   BM25 plus Vector Retrieval.
3. Optionally select one `reranker` Component; it is applied independently to
   each retrieval branch before fusion.
4. Select exactly one `generator` Component.
5. Load only the selected Component Skill bodies and implementations.

## Rewriter interface

A `rewriter` Component must provide the `rewriter` capability:

- Input `RewriteRequest`: `query`, optional `temperature`, optional `max_tokens`
- Output `RewriteResult`: either a single `rewritten_query` string (HyDE-style)
  or `queries`, a non-empty list of retrieval query strings

Each query becomes a fan-out point for all retrieval branches. The rewriter may
reformulate, decompose, or expand the query through the Executor Model; it must
not retrieve documents or generate a final answer. When the HyDE Rewriter is
selected, bind at least one Vector Retrieval branch and never add the
hypothetical document to the retrieved evidence.

## Workflow

Execute `scripts/workflow.py:run` after binding every required slot:

```text
RAGRequest
  -> optional rewriter (one or more query views)
  -> retrievers in parallel per query view
  -> optional per-branch reranker
  -> reciprocal rank fusion
  -> generator
  -> RAGResult
```

The workflow owns branch fan-out, reranking order, and fusion. Each retriever
owns only its concrete retrieval algorithm.
