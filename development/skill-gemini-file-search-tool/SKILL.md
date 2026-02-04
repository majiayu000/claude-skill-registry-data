---
name: skill-gemini-file-search-tool
description: Manage Gemini RAG stores with Code-RAG support
---

# When to use
- Managing Gemini File Search stores and documents
- Uploading documents for RAG queries (including codebases)
- Querying stores with natural language
- Building Code-RAG systems for semantic code search

# Gemini File Search Tool Skill

## Purpose

Comprehensive guide for managing Google's fully managed RAG (Retrieval-Augmented Generation) system using the `gemini-file-search-tool` CLI. This tool eliminates the complexity of vector databases, embeddings, and retrieval infrastructure by providing a production-ready interface to Gemini File Search.

## When to Use This Skill

**Use this skill when:**
- Creating and managing Gemini File Search stores
- Uploading documents for semantic search and RAG queries
- Building Code-RAG systems (semantic code search with natural language)
- Querying document stores with natural language
- Managing upload caches and operation status
- Implementing document search in AI applications

**Do NOT use this skill for:**
- General document processing (use document-skills instead)
- File system operations (use Read/Write tools)
- Cloud infrastructure management (use AWS/GCP CLIs)

## CLI Tool: gemini-file-search-tool

Production-ready CLI and Python library for Google's Gemini File Search API, a fully managed RAG system that automatically handles document ingestion, chunking, embedding generation, and semantic retrieval with zero infrastructure overhead.

### Installation

```bash
# Clone repository
git clone https://github.com/dnvriend/gemini-file-search-tool.git
cd gemini-file-search-tool

# Install globally with uv
uv tool install .

# Verify installation
gemini-file-search-tool --help
```

### Prerequisites

**Authentication (Choose one):**

**Option 1: Gemini Developer API (Recommended for development)**
```bash
export GEMINI_API_KEY="your-api-key-here"
# Or
export GOOGLE_API_KEY="your-api-key-here"
```
Get API key from: https://aistudio.google.com/apikey

**Option 2: Vertex AI (For production)**
```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

### Quick Start

```bash
# Create a store
gemini-file-search-tool create-store "my-docs"

# Upload documents
gemini-file-search-tool upload "*.pdf" --store "my-docs" -v

# Query with natural language
gemini-file-search-tool query "What is the main topic?" --store "my-docs" --show-cost
```

## Progressive Disclosure

<details>
<summary><strong>📖 Store Management Commands (Click to expand)</strong></summary>

### create-store - Create New Store

Create a new Gemini File Search store for document storage and RAG queries.

**Usage:**
```bash
gemini-file-search-tool create-store "STORE_NAME" [--display-name NAME] [-v]
```

**Arguments:**
- `STORE_NAME`: Store identifier (required, positional)
- `--display-name NAME`: Human-readable display name (optional)
- `-v`: Verbose logging

**Examples:**
```bash
# Create store with auto-generated display name
gemini-file-search-tool create-store "research-papers"

# Create store with custom display name
gemini-file-search-tool create-store "docs" --display-name "Project Documentation"

# Capture output for processing
gemini-file-search-tool create-store "code" | jq '.name'
```

**Output:**
```json
{
  "name": "fileSearchStores/abc123",
  "display_name": "research-papers",
  "create_time": "2025-11-20T10:30:00Z",
  "update_time": "2025-11-20T10:30:00Z"
}
```

---

### list-stores - List All Stores

List all available Gemini File Search stores with their metadata.

**Usage:**
```bash
gemini-file-search-tool list-stores [-v]
```

**Arguments:**
- `-v`: Verbose logging

**Examples:**
```bash
# List all stores
gemini-file-search-tool list-stores

# List with verbose logging
gemini-file-search-tool list-stores -v

# Filter stores with jq
gemini-file-search-tool list-stores | jq '.[] | select(.display_name | contains("docs"))'

# Count stores
gemini-file-search-tool list-stores | jq 'length'
```

**Output:**
```json
[
  {
    "name": "fileSearchStores/abc123",
    "display_name": "research-papers",
    "create_time": "2025-11-20T10:30:00Z",
    "update_time": "2025-11-20T10:30:00Z"
  }
]
```

---

### get-store - Get Store Details

Get detailed information about a specific store.

**Usage:**
```bash
gemini-file-search-tool get-store "STORE_NAME" [-v]
```

**Arguments:**
- `STORE_NAME`: Store name/ID (accepts display names, IDs, or full resource names)
- `-v`: Verbose logging

**Examples:**
```bash
# Get by display name
gemini-file-search-tool get-store "research-papers"

# Get by ID
gemini-file-search-tool get-store "abc123"

# Extract specific field
gemini-file-search-tool get-store "docs" | jq '.create_time'
```

---

### update-store - Update Store

Update a store's display name or metadata.

**Usage:**
```bash
gemini-file-search-tool update-store "STORE_NAME" --display-name "NEW_NAME" [-v]
```

**Examples:**
```bash
# Rename store
gemini-file-search-tool update-store "docs" --display-name "Production Documentation"
```

---

### delete-store - Delete Store

Delete a Gemini File Search store and all its documents.

**Usage:**
```bash
gemini-file-search-tool delete-store "STORE_NAME" [--force] [-v]
```

**Arguments:**
- `STORE_NAME`: Store to delete (required)
- `--force`: Skip confirmation prompt
- `-v`: Verbose logging

**Examples:**
```bash
# Delete with confirmation
gemini-file-search-tool delete-store "old-docs"

# Delete without confirmation
gemini-file-search-tool delete-store "temp-store" --force
```

**Note:** Shows cache statistics before deletion and automatically removes cache file after successful deletion.

</details>

<details>
<summary><strong>📁 Document Management Commands (Click to expand)</strong></summary>

### upload - Upload Documents

Upload files to a Gemini File Search store with intelligent caching, glob support, and parallel processing.

**Usage:**
```bash
gemini-file-search-tool upload FILES... --store "STORE_NAME" [OPTIONS]
```

**Arguments:**
- `FILES`: File paths or glob patterns (required, positional)
- `--store NAME`: Target store name (required)
- `--title TEXT`: Custom metadata title (optional)
- `--url URL`: Custom metadata URL (optional)
- `--max-tokens N`: Max tokens per chunk (default: 200)
- `--max-overlap N`: Max overlap tokens (default: 20)
- `--num-workers N`: Concurrent workers (default: CPU cores)
- `--skip-validation`: Skip file validation checks
- `--ignore-gitignore`: Ignore .gitignore patterns
- `--dry-run`: Preview files without uploading
- `--rebuild-cache`: Force re-upload all files
- `--no-wait`: Async upload without polling
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Key Features:**
- **Intelligent Caching**: Automatically skips unchanged files using mtime-based optimization (O(1) check)
- **Glob Patterns**: Supports `*.pdf`, `docs/**/*.md`, `src/**/*.py`
- **Gitignore Support**: Respects `.gitignore` patterns by default
- **Parallel Processing**: Concurrent uploads with configurable workers
- **System File Filtering**: Auto-skips `__pycache__`, `.pyc`, `.DS_Store`
- **Async Mode**: Fire-and-forget uploads with `--no-wait`

**Examples:**
```bash
# Upload single file
gemini-file-search-tool upload document.pdf --store "papers"

# Upload multiple files
gemini-file-search-tool upload doc1.pdf doc2.pdf --store "papers"

# Upload with glob pattern
gemini-file-search-tool upload "*.pdf" --store "papers" -v

# Upload recursive with markdown files
gemini-file-search-tool upload "docs/**/*.md" --store "documentation" -v

# Upload codebase for Code-RAG
gemini-file-search-tool upload "src/**/*.py" --store "my-codebase" -v

# Async upload with 8 workers
gemini-file-search-tool upload "*.pdf" --store "papers" --no-wait --num-workers 8

# Dry-run to preview files
gemini-file-search-tool upload "**/*.py" --store "code" --dry-run -v

# Rebuild cache (force re-upload)
gemini-file-search-tool upload "**/*.py" --store "code" --rebuild-cache
```

**Output:**
```json
[
  {"file": "doc1.pdf", "status": "completed", "document": {"name": "documents/123"}},
  {"file": "doc2.pdf", "status": "skipped", "reason": "Already exists"},
  {"file": "doc3.pdf", "status": "pending", "operation": "operations/456"}
]
```

---

### list-documents - List Documents in Store

List all documents in a Gemini File Search store.

**Usage:**
```bash
gemini-file-search-tool list-documents --store "STORE_NAME" [-v/-vv/-vvv]
```

**Arguments:**
- `--store NAME`: Store name (required)
- `-v/-vv/-vvv`: Verbosity levels

**Examples:**
```bash
# List all documents
gemini-file-search-tool list-documents --store "papers"

# With verbose logging
gemini-file-search-tool list-documents --store "papers" -vv

# Count documents
gemini-file-search-tool list-documents --store "papers" | jq 'length'
```

**Note:** Uses REST API workaround due to SDK bug #1661. Only works with Developer API (not Vertex AI).

</details>

<details>
<summary><strong>🔍 Query Commands (Click to expand)</strong></summary>

### query - Natural Language RAG Queries

Query a Gemini File Search store with natural language using Retrieval-Augmented Generation.

**Usage:**
```bash
gemini-file-search-tool query "PROMPT" --store "STORE_NAME" [OPTIONS]
```

**Arguments:**
- `PROMPT`: Natural language query (required, positional)
- `--store NAME`: Store to query (required)
- `--query-model {flash|pro}`: Model for RAG query (default: flash)
- `--query-grounding-metadata`: Include source citations in response
- `--metadata-filter "key=value"`: Filter documents by metadata
- `--show-cost`: Include token usage and cost estimation
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Enhancement Options (Use Sparingly):**
- `--enhance-mode {generic|code-rag|obsidian}`: Query optimization mode (disabled by default)
- `--enhancement-model {flash|pro}`: Model for enhancement (default: flash)
- `--show-enhancement`: Display enhanced query
- `--dry-run-enhancement`: Preview enhancement without executing query

**Examples:**
```bash
# Basic query
gemini-file-search-tool query "What is DORA?" --store "papers"

# Query with citations and cost tracking
gemini-file-search-tool query "How does authentication work?" \
  --store "codebase" --query-grounding-metadata --show-cost -v

# Query with Pro model
gemini-file-search-tool query "Explain the architecture" \
  --store "docs" --query-model pro

# Code-RAG query (semantic code search)
gemini-file-search-tool query "Where is error handling implemented?" \
  --store "my-codebase" --query-grounding-metadata

# With metadata filtering
gemini-file-search-tool query "Python best practices" \
  --store "docs" --metadata-filter "language=python"
```

**Output:**
```json
{
  "response_text": "DORA stands for DevOps Research and Assessment...",
  "usage_metadata": {
    "prompt_token_count": 150,
    "candidates_token_count": 320,
    "total_token_count": 470
  },
  "grounding_metadata": {
    "grounding_chunks": [
      {
        "retrieved_context": {
          "title": "/path/to/doc.pdf",
          "text": "Relevant excerpt..."
        }
      }
    ]
  },
  "estimated_cost": {
    "total_cost_usd": 0.00010725,
    "model": "gemini-2.5-flash"
  }
}
```

**Important Notes:**
- **Enhancement is disabled by default**: Benchmarks show simple queries work best for RAG
- **Flash model recommended**: 12x more cost-efficient than Pro, adequate for RAG
- Only use `--enhance-mode` for vague or poorly worded queries

</details>

<details>
<summary><strong>💾 Cache Management Commands (Click to expand)</strong></summary>

### sync-cache - Sync Pending Operations

Synchronize pending upload operations and update cache with final status.

**Usage:**
```bash
gemini-file-search-tool sync-cache --store "STORE_NAME" [OPTIONS]
```

**Arguments:**
- `--store NAME`: Store name (required)
- `--num-workers N`: Parallel workers (default: 4)
- `--text`: Human-readable output (default: JSON)
- `-v`: Verbose logging

**Examples:**
```bash
# Sync with default workers
gemini-file-search-tool sync-cache --store "papers"

# Sync with 8 parallel workers
gemini-file-search-tool sync-cache --store "codebase" --num-workers 8 -v

# Human-readable output
gemini-file-search-tool sync-cache --store "docs" --text
```

**When to Use:**
- After `upload --no-wait` operations
- To check status of pending uploads
- To update cache with final document IDs

---

### flush-cache - Clear Cache File

Delete the cache file for a specific store to start fresh.

**Usage:**
```bash
gemini-file-search-tool flush-cache --store "STORE_NAME" [--force] [-v]
```

**Arguments:**
- `--store NAME`: Store name (required)
- `--force`: Skip confirmation prompt
- `-v`: Verbose logging

**Examples:**
```bash
# Flush with confirmation
gemini-file-search-tool flush-cache --store "old-docs"

# Flush without confirmation
gemini-file-search-tool flush-cache --store "temp" --force
```

**When to Use:**
- Before rebuilding cache
- When cache is corrupted
- For clean slate troubleshooting

---

### cache-report - Generate Cache Status Report

Show cache statistics and operation status.

**Usage:**
```bash
gemini-file-search-tool cache-report --store "STORE_NAME" [FILTERS] [OPTIONS]
```

**Arguments:**
- `--store NAME`: Store name (required)
- `--pending-only`: Show only pending operations
- `--errors-only`: Show only failed operations
- `--completed-only`: Show only completed operations
- `--all`: Show all cached files
- `--text`: Human-readable output (default: JSON)
- `-v`: Verbose logging

**Examples:**
```bash
# Show summary + pending operations
gemini-file-search-tool cache-report --store "papers"

# Show only failed operations
gemini-file-search-tool cache-report --store "docs" --errors-only

# Show all cached files
gemini-file-search-tool cache-report --store "code" --all --text
```

</details>

<details>
<summary><strong>💻 Code-RAG: Semantic Code Search (Click to expand)</strong></summary>

### What is Code-RAG?

Code-RAG (Retrieval-Augmented Generation for Code) enables uploading entire codebases and querying them with natural language. This is powerful for:

- **Codebase Onboarding**: New developers ask questions about architecture
- **Code Discovery**: Find implementations without grepping
- **Architecture Analysis**: Understand design patterns and structure
- **Documentation Generation**: Generate contextual docs from code
- **AI Coding Assistants**: Build agents that answer codebase questions

### Code-RAG Workflow

**Step 1: Upload Codebase**
```bash
# Upload all Python files
gemini-file-search-tool upload "src/**/*.py" --store "my-project" -v

# Upload multiple languages
gemini-file-search-tool upload "src/**/*.{py,js,go}" --store "polyglot-project" -v

# Upload with custom chunking
gemini-file-search-tool upload "**/*.py" --store "large-project" \
  --max-tokens 500 --max-overlap 50 --num-workers 8
```

**Step 2: Query with Natural Language**
```bash
# Architectural questions
gemini-file-search-tool query "How does the authentication system work?" \
  --store "my-project" --query-grounding-metadata -v

# Implementation discovery
gemini-file-search-tool query "Where is error handling for API calls implemented?" \
  --store "my-project" --show-cost

# Design pattern analysis
gemini-file-search-tool query "What design patterns are used in this codebase?" \
  --store "my-project" --query-model pro
```

**Step 3: Get Source References**
```bash
# Query with full citations
gemini-file-search-tool query "Explain the database layer" \
  --store "my-project" --query-grounding-metadata | \
  jq '.grounding_metadata.grounding_chunks[].retrieved_context.title'
```

### Code-RAG Best Practices

1. **Comprehensive Docstrings**: Well-documented code provides better semantic search results
2. **Modular Structure**: Clear file/function organization improves retrieval accuracy
3. **Use Flash Model**: Cost-effective and sufficient for code search
4. **Enable Grounding**: Always use `--query-grounding-metadata` to verify sources
5. **Gitignore Support**: Automatically skips `__pycache__`, build artifacts, etc.

### Meta Note

This tool itself was built using Code-RAG! During development, we uploaded the codebase to a Gemini File Search store and queried it to understand implementation details, find bugs, and plan features. The tool enables the very functionality it provides.

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

### Intelligent Caching System

**Location:** `~/.config/gemini-file-search-tool/stores/`

**How it Works:**
- Tracks uploaded files per store in JSON cache files
- Uses mtime-based optimization (O(1) check before O(n) hash)
- For 1000 unchanged files: ~0.1s (mtime) vs ~5-10s (full hash)
- Automatically skips unchanged files on re-upload
- Per-store isolation prevents cache conflicts

**Cache Structure:**
```json
{
  "/absolute/path/to/file.py": {
    "hash": "sha256-hash",
    "mtime": 1731969000.0,
    "remote_id": "documents/123",
    "last_uploaded": "2025-11-18T22:30:00Z"
  }
}
```

**Cache States:**
- **Completed**: Has `remote_id`, file successfully uploaded
- **Pending**: Has `operation`, async upload in progress
- **Missing**: Not in cache, needs upload

---

### Parallel Processing

**Upload Concurrency:**
```bash
# Default: Uses CPU core count
gemini-file-search-tool upload "*.pdf" --store "papers"

# Custom workers
gemini-file-search-tool upload "*.pdf" --store "papers" --num-workers 8
```

**Sync Concurrency:**
```bash
# Parallel operation status checking
gemini-file-search-tool sync-cache --store "papers" --num-workers 8
```

---

### Cost Tracking

**Query Cost Estimation:**
```bash
gemini-file-search-tool query "What is this?" --store "docs" --show-cost
```

**Output:**
```json
{
  "estimated_cost": {
    "input_cost_usd": 0.00001125,
    "output_cost_usd": 0.000096,
    "total_cost_usd": 0.00010725,
    "model": "gemini-2.5-flash"
  }
}
```

**Current Pricing (2025-01):**
- **Flash**: $0.075 input / $0.30 output per 1M tokens
- **Pro**: $1.25 input / $5.00 output per 1M tokens

---

### Authentication Methods

**Developer API (Recommended for Development):**
```bash
export GEMINI_API_KEY="AIza..."
gemini-file-search-tool list-stores
```

**Vertex AI (Recommended for Production):**
```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="my-project"
export GOOGLE_CLOUD_LOCATION="us-central1"
gemini-file-search-tool list-stores
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Authentication error - missing API key**
```bash
Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is required
```

**Solution:**
1. Get API key from https://aistudio.google.com/apikey
2. Set environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

---

**Issue: File not uploading**

**Solution:**
1. Check if file is in cache and unchanged:
   ```bash
   gemini-file-search-tool cache-report --store "your-store" | grep "your-file"
   ```
2. Force re-upload with `--rebuild-cache`:
   ```bash
   gemini-file-search-tool upload "file.pdf" --store "your-store" --rebuild-cache
   ```

---

**Issue: Pending operations not completing**

**Solution:**
Run sync-cache to check operation status:
```bash
gemini-file-search-tool sync-cache --store "your-store" -v
```

---

**Issue: Store not found**

**Solution:**
1. List all stores:
   ```bash
   gemini-file-search-tool list-stores
   ```
2. Use exact display name or ID from list output

---

**Issue: Query returning no results**

**Solution:**
1. Verify documents were uploaded successfully:
   ```bash
   gemini-file-search-tool list-documents --store "your-store"
   ```
2. Check if uploads are pending:
   ```bash
   gemini-file-search-tool cache-report --store "your-store" --pending-only
   ```
3. Try simpler query (avoid over-specification)

---

### Getting Help

```bash
# General help
gemini-file-search-tool --help

# Command-specific help
gemini-file-search-tool upload --help
gemini-file-search-tool query --help

# Verbose logging for debugging
gemini-file-search-tool upload "file.pdf" --store "test" -vvv
```

---

### Known Issues

**SDK Bug #1661 - Document Listing**
- `list-documents` uses REST API workaround
- Only works with Developer API (not Vertex AI)
- GitHub: https://github.com/googleapis/python-genai/issues/1661

</details>

## Exit Codes

- `0`: Success
- `1`: Error (authentication, validation, API error)

## Output Formats

**JSON (Default):**
All commands output JSON to stdout, logs to stderr for easy piping:
```bash
gemini-file-search-tool list-stores | jq '.[] | .display_name'
```

**Text (Select Commands):**
Some commands support `--text` flag for human-readable output:
```bash
gemini-file-search-tool cache-report --store "docs" --text
```

## Best Practices

1. **Use Caching**: Let the tool manage duplicates automatically, don't manually track uploads
2. **Flash Model for RAG**: 12x more cost-efficient than Pro, perfectly adequate for semantic search
3. **Enable Grounding**: Always use `--query-grounding-metadata` to verify sources and validate answers
4. **Simple Queries**: Keep queries simple and direct, avoid over-specification (RAG relies on semantic similarity)
5. **Code-RAG Documentation**: Comprehensive docstrings maximize retrieval quality for code search
6. **Parallel Processing**: Use `--num-workers` to speed up large uploads
7. **Async + Sync**: Use `--no-wait` for bulk uploads, then `sync-cache` to check final status

## Resources

- **GitHub**: https://github.com/dnvriend/gemini-file-search-tool
- **Gemini File Search API**: https://ai.google.dev/gemini-api/docs/file-search
- **Google AI Studio**: https://aistudio.google.com/
- **API Keys**: https://aistudio.google.com/apikey
- **Pricing**: https://ai.google.dev/pricing
