---
license: MIT
name: qmd
description: Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.
---

# qmd - Quick Markdown Search

Local search engine for Markdown notes, docs, and knowledge bases. Index once, search fast.

## When to use (trigger phrases)

- "search my notes / docs / knowledge base"
- "find related notes"
- "retrieve a markdown document from my collection"
- "search local markdown files"

## Default behavior (important)

- Prefer `qmd search` (BM25). It's typically instant and should be the default.
- Use `qmd vsearch` only when keyword search fails and you need semantic similarity (can be very slow on a cold start).
- Avoid `qmd query` unless the user explicitly wants the highest quality hybrid results and can tolerate long runtimes/timeouts.

## Search modes

| Mode | Command | Speed | Use case |
|------|---------|-------|----------|
| BM25 (default) | `qmd search` | Instant | Keyword matching |
| Vector | `qmd vsearch` | ~1 min cold | Semantic similarity |
| Hybrid | `qmd query` | Slowest | LLM reranking (skip unless requested) |

## Common commands

```bash
qmd search "query"              # default - fast keyword search
qmd search "query" -c notes     # search specific collection
qmd search "query" -n 10        # more results
qmd search "query" --json       # JSON output
qmd search "query" --all --files --min-score 0.3
```

## Useful options

- `-n <num>`: number of results
- `-c, --collection <name>`: restrict to a collection
- `--all --min-score <num>`: return all matches above a threshold
- `--json` / `--files`: agent-friendly output formats
- `--full`: return full document content

## Retrieve documents

```bash
qmd get "path/to/file.md"       # Full document
qmd get "#docid"                # By ID from search results
qmd multi-get "journals/2025-05*.md"
qmd multi-get "doc1.md, doc2.md, #abc123" --json
```

## Maintenance

```bash
qmd status                      # Index health
qmd update                      # Re-index changed files
qmd embed                       # Update embeddings
```

## Setup (if not installed)

```bash
# Install
bun install -g https://github.com/tobi/qmd

# Create collection
qmd collection add /path/to/notes --name notes --mask "**/*.md"
qmd context add qmd://notes "Description of this collection"  # optional
qmd embed  # one-time to enable vector + hybrid search
```

## Performance notes

- `qmd search` is typically instant
- `qmd vsearch` can be ~1 minute on cold start (loads local LLM for query expansion)
- `qmd query` adds LLM reranking on top of `vsearch`, even slower

## Common Pitfalls

### Search query too vague (irrelevant results)
**Problem:** Broad queries like "notes" or "project" return hundreds of low-relevance matches.

**Solution:**
- Use specific keywords: `qmd search "Python async context managers"` not `qmd search "Python"`
- Combine keywords: `qmd search "deadline March quarterly review"`
- Use quotes for exact phrases: `qmd search "exact phrase match"`
- Check result scores: `qmd search "query" --all --min-score 0.5` to filter low-confidence matches

### Index not updated (missing recent files)
**Problem:** Newly created or recently modified files don't appear in search results.

**Solution:**
```bash
# Check index status
qmd status

# Re-index all changed files
qmd update

# Full re-index if update doesn't help
qmd collection remove <name>
qmd collection add /path/to/notes --name <name> --mask "**/*.md"
qmd embed  # if vector search enabled
```

### Path filters wrong (excluding relevant directories)
**Problem:** Search doesn't find files because the collection mask is too narrow or collection path is wrong.

**Solution:**
```bash
# List current collections
qmd status

# Verify collection path matches your notes location
# If path changed, re-add collection:
qmd collection remove <old-name>
qmd collection add /path/to/notes --name <name> --mask "**/*.md"

# Common issue: subdirectories excluded by mask
# If notes are in journals/2025/*, use: --mask "**/*.md"
# Not: --mask "*.md" (which only matches top level)
```

### Search timeout on large vaults (performance issues)
**Problem:** `qmd query` or `qmd vsearch` hangs or times out on large knowledge bases (1000+ files).

**Solution:**
- Avoid `qmd query` on large vaults (LLM reranking is too slow)
- Use `qmd search` instead (BM25 is fast even on huge collections)
- If semantic search needed, use `qmd vsearch` with `-n 5` to limit results
- Restrict search scope with `-c <collection>` to search one collection instead of all:
  ```bash
  qmd search "query" -c notes -n 5  # faster than searching all collections
  ```
- If vault exceeds 5000 files, consider splitting into multiple collections

### Missing configuration (qmd not initialized)
**Problem:** `qmd status` shows "No collections" or `qmd search` returns no results.

**Solution:**
```bash
# Install qmd if missing
bun install -g https://github.com/tobi/qmd

# Set up a collection
qmd collection add /path/to/notes --name notes --mask "**/*.md"

# Enable vector search (optional but recommended)
qmd embed

# Verify setup
qmd status  # Should show your collection with file count
```

### Semantic search returns irrelevant results (vsearch/query)
**Problem:** Vector search matches by topic but misses what you actually wanted.

**Solution:**
- Fall back to `qmd search` (BM25 keyword matching is more precise for specific terms)
- Rephrase query to include actual keywords: not "What are my goals?" but "goals quarterly review objectives"
- Use `qmd query` if available (adds LLM reranking), but only if you can tolerate slow runtime
- Use `-n 3` to get fewer, higher-confidence matches from vector search
