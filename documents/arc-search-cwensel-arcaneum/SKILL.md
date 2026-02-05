---
name: arc-search
description: Semantic and full-text search across indexed collections. Use when user mentions searching a collection, semantic search, vector search, knowledge base, or finding content in indexed code, markdown, or PDFs.
allowed-tools: Bash(arc:*), Read
---

```bash
arc collection list                                          # list collections
arc search semantic "query" --collection NAME --limit 10     # conceptual queries
arc search text "query" --index NAME --limit 10              # exact terms
```

Options: `--json` for structured output, `--filter "key=value"` for metadata filtering.
