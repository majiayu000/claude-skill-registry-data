---
name: processor
description: Process documents into RAG database. Use when user wants to chunk, embed, or index files into a vector database for semantic search.
---

# Document Processing

This skill helps you process documents, codebases, and papers into a searchable RAG (Retrieval-Augmented Generation) database using LanceDB.

## Quick Start

```bash
# 1. Check that services are running
uv run processor check

# 2. Process files into database
uv run processor process ./input -o ./lancedb

# 3. Verify results
uv run processor stats ./lancedb
```

## Common Use Cases

### Process a codebase
```bash
uv run processor process ./my-project -o ./code_db --content-type code
```

### Process papers/documents
```bash
uv run processor process ./papers -o ./papers_db
```

### Incremental updates (skip unchanged files)
```bash
uv run processor process ./input -o ./lancedb --incremental
```

### High-quality embeddings (slower, better retrieval)
```bash
uv run processor process ./input -o ./lancedb --text-profile high --code-profile high
```

## Embedding Profiles

| Type | Profile | Model | Dimensions | Use Case |
|------|---------|-------|------------|----------|
| text | low | Qwen3-Embedding-0.6B | 1024 | Fast, good quality |
| text | medium | Qwen3-Embedding-4B | 2560 | Balanced |
| text | high | Qwen3-Embedding-8B | 4096 | Maximum quality |
| code | low | jina-code-0.5b | 896 | Fast code search |
| code | high | jina-code-1.5b | 1536 | Best code search |

## Key Options

| Option | Values | Description |
|--------|--------|-------------|
| `--embedder` | ollama, transformers | Embedding backend |
| `--text-profile` | low, medium, high | Text embedding quality |
| `--code-profile` | low, high | Code embedding quality |
| `--table-mode` | separate, unified, both | Table organization |
| `--incremental/--full` | - | Skip unchanged files |
| `--content-type` | auto, code, paper, markdown | Force content detection |

## MCP Server

Start the processor MCP server for programmatic access:

```bash
uv run processor-mcp
```

Configure in Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "processor": {
      "command": "uv",
      "args": ["run", "processor-mcp"],
      "cwd": "/path/to/processor"
    }
  }
}
```

### Available MCP Tools

- `process_documents` - Process files into LanceDB
- `check_services` - Check backend availability
- `setup_models` - Download embedding models
- `get_db_stats` - Database statistics
- `export_db` - Export database

## Troubleshooting

### "Model not found" error
```bash
uv run processor setup  # Download required models
```

### Ollama not running
```bash
ollama serve  # Start Ollama server
```

### Check available models
```bash
uv run processor check
```
