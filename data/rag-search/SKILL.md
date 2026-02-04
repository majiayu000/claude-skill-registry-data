---
name: rag-search
description: Search RAG database for relevant content. Use for semantic queries over processed documents, code, or papers.
---

# RAG Search

This skill helps you search processed document databases using semantic similarity and retrieval-time optimizations.

## Quick Search

```bash
# Basic vector search
uv run processor search ./lancedb "how does the caching work"

# Hybrid search (vector + keyword)
uv run processor search ./lancedb "ConfigParser yaml loading" --hybrid

# Search code
uv run processor search ./lancedb "authentication middleware" --table code_chunks
```

## Available Tables

| Table | Content |
|-------|---------|
| `text_chunks` | Documents, papers, markdown (default) |
| `code_chunks` | Source code |
| `image_chunks` | Figures from papers |
| `chunks` | Unified table (if created with --table-mode unified) |

## MCP Server

Start the RAG MCP server for programmatic access:

```bash
uv run rag-mcp
```

Generate a config template:
```bash
uv run rag-mcp --config_generate
```

Configure in Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "rag": {
      "command": "uv",
      "args": ["run", "rag-mcp"],
      "cwd": "/path/to/processor"
    }
  }
}
```

### Available MCP Tools

- `search` - Vector/hybrid search with optimizations
- `search_images` - Search image chunks
- `list_tables` - List available tables
- `generate_config` - Create config template

## Retrieval Optimizations

Enable these for better results at the cost of latency:

| Optimization | Flag | Latency | Best For |
|--------------|------|---------|----------|
| Hybrid Search | `hybrid=True` | +10-30ms | Keyword-heavy queries |
| HyDE | `use_hyde=True` | +200-500ms | Knowledge questions |
| Reranking | `rerank=True` | +50-200ms | High precision needs |
| Parent Expansion | `expand_parents=True` | +5-20ms | Broader context |

### Recommended Combinations

**Fast search (default):**
No optimizations - pure vector similarity

**Better recall:**
```python
search(query="...", hybrid=True)
```

**Knowledge questions:**
```python
search(query="what is...", use_hyde=True, rerank=True)
```

**Code search:**
```python
search(query="...", table="code_chunks", hybrid=True)
```

**Maximum precision:**
```python
search(query="...", hybrid=True, use_hyde=True, rerank=True)
```

## Configuration

Edit `rag_config.yaml` to set defaults:

```yaml
# Embedding profiles (must match processor config)
text_profile: "low"
code_profile: "low"
ollama_host: "http://localhost:11434"

# Default search behavior
default_limit: 5
default_hybrid: false

# HyDE settings (uses Claude SDK by default, falls back to Ollama)
hyde:
  enabled: false
  backend: "claude_sdk"  # claude_sdk (default) or ollama
  claude_model: "haiku"  # haiku, sonnet, opus
  ollama_model: "llama3.2:latest"  # fallback

# Reranking settings
reranker:
  enabled: false
  model: "BAAI/bge-reranker-v2-m3"
  top_k: 20
  top_n: 5
```

## Understanding Results

Results include:
- `content`: Matched chunk text
- `source_file`: Original file path
- `score`: Similarity (0-1, higher is better)
- `metadata`: Additional fields (section, language, etc.)

## Troubleshooting

### No results found
1. Check database exists: `uv run processor stats ./lancedb`
2. Verify table has data: `--table text_chunks`
3. Try broader query terms

### Poor quality results
1. Enable hybrid search: `--hybrid`
2. Check embedding profiles match processor config
3. Consider reranking: `rerank=True`

### Slow searches
1. Disable HyDE if not needed
2. Reduce rerank_top_k
3. Check Ollama server performance
