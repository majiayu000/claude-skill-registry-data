---
name: implementing-document-indexing
description: Implements document indexing with heading-boundary chunking, embedding, FAISS vector store, and PageIndex-style hybrid retrieval. Use when building RAG pipelines, document search, or memory layers.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: [module-or-feature]
  stability: development
  last-verified-cc-version: 1.0.34
---

# Document Indexing Implementation

**Target**: $ARGUMENTS

Implements a **document indexing and hybrid retrieval** pipeline: parse documents,
build a heading-based tree index, chunk by heading boundaries, embed with
sentence-transformers, store in FAISS, and retrieve via hybrid search.

## Architecture Overview

```text
Document --> Parser --> Pages --> TreeIndex (PageIndex)
                                     |
                                     v
                              Chunker (heading-boundary + max-token)
                                     |
                                     v
                              Embedder (sentence-transformers)
                                     |
                                     v
                              VectorStore (FAISS IndexFlatIP)
                                     |
                                     v
                         HybridRetrieval (vector search -> full page -> tree filter)
```

## Chunking Strategy

See `references/chunking-strategies.md` for full reference.

**Heading-boundary chunking** (primary):

1. Split document by heading boundaries (H1-H6)
2. Each section becomes a chunk with heading hierarchy as metadata
3. If a section exceeds max tokens, split at sentence boundaries
4. Preserve heading path (e.g., `H1 > H2 > H3`) as chunk metadata

**Max-token splits** (fallback):

- Default max: 512 tokens
- Overlap: 64 tokens between splits
- Never split mid-sentence

## Retrieval Pipeline

See `references/retrieval-patterns.md` for full reference.

**Hybrid retrieval** (vector search + tree filter):

1. **Embed query** with same model used for indexing
2. **Vector search** top-k chunks from FAISS (cosine similarity via IndexFlatIP)
3. **Full page fetch** -- retrieve complete pages containing matched chunks
4. **Tree filter** -- use PageIndex tree to filter to relevant sections only
5. **Return** filtered sections with source citations (page, heading path)

## Data Models

```python
@dataclass
class Document:
    pages: list[Page]
    metadata: dict[str, str]

@dataclass
class Page:
    number: int
    content: str
    headings: list[str]

@dataclass
class TreeNode:
    heading: str
    level: int
    content: str
    children: list[TreeNode]

    def filter(self, predicate: Callable) -> TreeNode | None: ...
```

## Dependencies

```toml
[project]
dependencies = [
    "sentence-transformers>=3.0",
    "faiss-cpu>=1.9",
]
```

## Workflow

1. **Define data models** -- Document, Page, TreeNode dataclasses
2. **Implement parser** -- extract pages with headings from source documents
3. **Build tree index** -- construct PageIndex tree from heading hierarchy
4. **Implement chunker** -- heading-boundary splits with max-token fallback
5. **Implement embedder** -- sentence-transformers wrapper (encode, batch)
6. **Implement vector store** -- FAISS IndexFlatIP with add/search/save/load
7. **Implement hybrid retrieval** -- full pipeline: embed, search, fetch, filter
8. **Wire CLI** -- ingest and search commands

## Quality Checks

```bash
make validate
```

All type checks, linting, and tests must pass.
