---
name: skill-vector-rag-tool
description: Local RAG with Ollama and FAISS
---

# When to use

- Index codebases or documents for semantic search
- Query vector stores for relevant code/document chunks
- Manage vector stores (create, delete, list)
- Set up local RAG with Ollama embeddings

# vector-rag-tool Skill

## Purpose

CLI for local RAG (Retrieval-Augmented Generation) with Ollama embeddings and FAISS vector search. Index codebases and documents into vector stores for semantic search.

## When to Use

Use this skill when:

- Indexing source code or documentation for semantic search
- Querying indexed content by meaning (not just keywords)
- Managing vector stores (create, list, delete, info)
- Configuring S3 Vectors backend for cloud storage

Do NOT use for:

- Simple text search (use grep instead)
- Tasks unrelated to vector search or RAG

## Prerequisites

```bash
# Ollama with embedding model
brew install ollama
ollama pull embeddinggemma
```

## Quick Start

```bash
# Index Python files
vector-rag-tool index "**/*.py" --store my-project --no-dry-run

# Query for relevant code
vector-rag-tool query "how does authentication work" --store my-project

# List stores
vector-rag-tool store list
```

## Commands

### index - Index files into vector store

```bash
# Preview (dry-run default)
vector-rag-tool index "*.py" --store my-store

# Actually index files
vector-rag-tool index "*.md" "*.py" --store my-store --no-dry-run

# Index to S3 Vectors
vector-rag-tool index "src/**/*.py" --store my-store \
    --bucket my-vectors-bucket --profile dev --no-dry-run

# Force reindex all
vector-rag-tool index "docs/**/*.md" --store my-store --force --no-dry-run

# Custom chunk size
vector-rag-tool index "**/*.py" --store my-store --chunk-size 500 --no-dry-run
```

Options:

| Option | Description |
|--------|-------------|
| `--store/-s` | Store name (required) |
| `--bucket/-b` | S3 bucket for remote storage |
| `--region/-r` | AWS region (default: eu-central-1) |
| `--profile/-p` | AWS profile name |
| `--dry-run/-n` | Preview mode (default: enabled) |
| `--no-dry-run` | Actually perform indexing |
| `--force/-f` | Force reindexing all files |
| `--chunk-size/-c` | Target chunk size (default: 1500) |
| `--chunk-overlap/-o` | Overlap between chunks (default: 200) |
| `-v/-vv/-vvv` | Verbosity (INFO/DEBUG/TRACE) |

### query - Query vector store

```bash
# Basic query
vector-rag-tool query "machine learning" --store my-store

# More results
vector-rag-tool query "deep learning" --store my-store --top-k 10

# Query S3 backend
vector-rag-tool query "neural networks" --store my-store \
    --bucket my-vector-store --profile dev

# JSON output
vector-rag-tool query "attention mechanism" --store my-store --json

# From stdin
echo "query text" | vector-rag-tool query --store my-store --stdin

# Full chunks for RAG grounding
vector-rag-tool query "authentication" --store my-store --full --json
```

Options:

| Option | Description |
|--------|-------------|
| `--store/-s` | Store name (required) |
| `--top-k/-k` | Number of results (default: 5) |
| `--json` | JSON output |
| `--stdin` | Read query from stdin |
| `--snippet-length/-l` | Max snippet length (default: 300) |
| `--full/-F` | Return full chunk content |

Output format:

```json
{
  "query": "authentication",
  "store": "my-store",
  "total_results": 5,
  "results": [
    {
      "score": 0.85,
      "file_path": "src/auth.py",
      "line_start": 42,
      "line_end": 78,
      "content": "..."
    }
  ]
}
```

### store - Manage vector stores

```bash
# List stores
vector-rag-tool store list
vector-rag-tool store list --format json

# Create store
vector-rag-tool store create my-store
vector-rag-tool store create my-store --dimension 1536

# Store info
vector-rag-tool store info my-store
vector-rag-tool store info my-store --format json

# Delete store
vector-rag-tool store delete my-store
vector-rag-tool store delete my-store --force
```

### completion - Shell completion

```bash
# Bash
eval "$(vector-rag-tool completion bash)"

# Zsh
eval "$(vector-rag-tool completion zsh)"

# Fish
vector-rag-tool completion fish > ~/.config/fish/completions/vector-rag-tool.fish
```

## Chunking Guidelines

| Use Case | Chunk Size | Rationale |
|----------|------------|-----------|
| Code search | 1000-1500 | Full functions/classes |
| Documentation | 500-1000 | Paragraphs and sections |
| Fine-grained | 300-500 | More specific matches |

## Verbosity Levels

| Flag | Level | Output |
|------|-------|--------|
| (none) | WARNING | Errors and warnings only |
| `-v` | INFO | High-level operations |
| `-vv` | DEBUG | Detailed info |
| `-vvv` | TRACE | Library internals |

## Troubleshooting

```bash
# Verify installation
vector-rag-tool --version

# Verify Ollama
ollama list  # Should show embeddinggemma

# List stores
vector-rag-tool store list

# Check store info
vector-rag-tool store info my-store

# Debug mode
vector-rag-tool query "test" --store my-store -vv
```

## Exit Codes

- `0`: Success
- `1`: Client error (invalid arguments)
- `2`: Server error (backend error)
