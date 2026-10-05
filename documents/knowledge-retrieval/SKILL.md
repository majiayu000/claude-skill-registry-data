---
name: knowledge-retrieval
description: Semantic search over ingested documents using RAG (LlamaIndex/ChromaDB or Foundational RAG)
allowed-tools: knowledge-retrieval
---

# Knowledge Retrieval

Perform semantic search over a pre-ingested document collection using Retrieval-Augmented Generation (RAG). Backed by LlamaIndex with ChromaDB or NVIDIA Foundational RAG.

## When to Use

- Searching internal or pre-ingested documents and reports
- Finding information in PDFs, whitepapers, or technical documentation
- Retrieving domain-specific knowledge not available on the open web
- This is the **highest priority** source — check the knowledge base first before web or paper searches

## How to Use

1. Formulate a semantic search query describing the information needed
2. Call `knowledge_retrieval` with the query
3. Review returned chunks for relevance
4. Note the citation metadata (filename, page number) for sourcing

## Result Format

Results are returned as text chunks with citation metadata:

```
Relevant text passage from the ingested document...

Citation: filename.pdf, p.12
```

## Constraints

- Searches only over documents that have been ingested into the knowledge index
- Returns ranked chunks based on semantic similarity
- Citation format: `Citation: filename.ext, p.X`
- Each call counts toward the researcher's 8-call limit per task

## Backend Options

- **LlamaIndex + ChromaDB** — Local vector store with LlamaIndex orchestration
- **NVIDIA Foundational RAG** — NVIDIA-hosted RAG service with NeMo Retriever
