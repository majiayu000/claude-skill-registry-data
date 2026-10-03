---
name: agentic-sequential-skill
description: Arrange a sequential RAG workflow with one optional query rewriter, one required retriever, one optional reranker, and one required grounded generator. Use after Manage selects a simple one-route retrieval and generation process.
---

# Sequential RAG Skill

Use this Skill only after the Manage stage selects it. This Skill defines process order and Component selection guidance; it does not implement rewriting, retrieval, reranking, or generation.

## Component selection

1. Optionally select one `rewriter` Component when query-document wording mismatch is likely.
2. Select exactly one `retriever` Component.
3. When selecting the HyDE Rewriter, select a semantic Vector Retriever and do not use the hypothetical document as a BM25-only query.
4. Optionally select one `reranker` Component when first-stage ranking is noisy.
5. Select exactly one `generator` Component.
6. Load only the selected Component Skill bodies and implementations.

Prefer BM25 without a Rewriter for exact names, identifiers, and strong lexical anchors.

Prefer Vector Retrieval without a Rewriter for ordinary paraphrases and semantic matching.

Prefer the single-sample HyDE Rewriter (`N=1`) followed by Vector Retrieval when the original query is short, abstract, or phrased differently from relevant corpus documents.

## Query handling

- Send the original query to the optional Rewriter.
- Send the single `rewritten_query` to the Retriever when the HyDE Rewriter is selected.
- Send the original query to the Reranker and Generator.
- Never add a hypothetical HyDE document to the retrieved evidence.

## Workflow

Execute `scripts/workflow.py:run` after every required slot is bound:

```text
RAGRequest
  -> optional rewriter
  -> retriever
  -> optional reranker
  -> generator
  -> RAGResult
```

The workflow script may call slots through `components`, but it must never import a concrete Component implementation.
