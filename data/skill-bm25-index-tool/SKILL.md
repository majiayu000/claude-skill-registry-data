---
name: skill-bm25-index-tool
description: Lightning-fast BM25 full-text search for files
---

# When to use

- Search large document collections (knowledge bases, notes, code)
- Index files with glob patterns for instant full-text search
- Query multiple indices simultaneously with merge strategies
- Find related documents using TF-IDF similarity
- Track search history and analyze query patterns
- Process batch queries efficiently with parallel execution

# bm25-index-tool Skill

## Purpose

This skill provides comprehensive access to `bm25-index-tool`, a production-ready CLI for lightning-fast full-text search using the BM25 ranking algorithm. Designed for AI agents and developers who need powerful search with minimal setup.

**Core Capabilities:**
- **Index Creation**: Index thousands of files in seconds with glob patterns
- **Search**: Query single or multiple indices with BM25 ranking
- **Path Filtering**: Scope searches to specific directories with glob patterns
- **Related Documents**: Find similar content using TF-IDF
- **Batch Processing**: Process multiple queries with parallel execution
- **Query History**: Track all searches in SQLite database
- **Statistics**: Analyze index health, vocabulary, term frequencies
- **Caching**: LRU cache for repeated queries
- **Merge Strategies**: Combine multi-index results (RRF, union, intersection, weighted)

## When to Use This Skill

**Use this skill when:**
- Searching knowledge bases, notes, documentation, or code
- Building search features in applications
- Analyzing document collections with BM25 ranking
- Finding related content based on similarity
- Processing batch queries for efficiency
- Working with Obsidian vaults, documentation sites, or code repositories
- Needing JSON output for downstream processing

**Do NOT use this skill for:**
- Tasks requiring real-time indexing (index rebuild required)
- Incremental updates (full re-index only)
- Fuzzy matching (BM25 is keyword-based)
- Vector search or semantic similarity (use embeddings instead)

## CLI Tool: bm25-index-tool

The `bm25-index-tool` provides lightning-fast BM25 search with advanced features like multi-index queries, path filtering, related documents, and comprehensive history tracking.

### Installation

```bash
# Clone and install
git clone https://github.com/dnvriend/bm25-index-tool.git
cd bm25-index-tool
uv tool install .
```

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Start

```bash
# Create an index from markdown files
bm25-index-tool create vault --pattern "~/vault/**/*.md"

# Search the index
bm25-index-tool query vault "kubernetes networking"

# Search with JSON output (AI agent friendly)
bm25-index-tool query vault "docker" --format json

# Get comprehensive help with examples
bm25-index-tool query --help  # Shows 20+ examples
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

<!-- TODO: Add detailed command documentation for each CLI command -->
<!-- Template for each command:

### command-name - Brief Description

Detailed explanation of what this command does.

**Usage:**
```bash
bm25-index-tool command-name ARGUMENT [OPTIONS]
```

**Arguments:**
- `ARGUMENT`: Description of argument
- `--option VALUE` / `-o VALUE`: Description of option
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Example 1: Basic usage
bm25-index-tool command-name "example"

# Example 2: With options
bm25-index-tool command-name "example" --option value

# Example 3: Pipeline usage
bm25-index-tool command-name "example" --json | jq '.'
```

**Output:**
Description of what this command returns.

---

Repeat for each command...
-->

### help - Show Help Information

Display help information for CLI commands.

**Usage:**
```bash
bm25-index-tool --help
bm25-index-tool COMMAND --help
```

**Examples:**
```bash
# General help
bm25-index-tool --help

# Command help
bm25-index-tool command --help

# Version info
bm25-index-tool --version
```

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

<!-- TODO: Add advanced features documentation -->

### Multi-Level Verbosity Logging

Control logging detail with progressive verbosity levels. All logs output to stderr.

**Logging Levels:**

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals | Deep debugging |

**Examples:**
```bash
# INFO level - see operations
bm25-index-tool command -v

# DEBUG level - see detailed info
bm25-index-tool command -vv

# TRACE level - see all internals
bm25-index-tool command -vvv
```

---

### Shell Completion

Native shell completion for bash, zsh, and fish.

**Installation:**
```bash
# Bash (add to ~/.bashrc)
eval "$(bm25-index-tool completion bash)"

# Zsh (add to ~/.zshrc)
eval "$(bm25-index-tool completion zsh)"

# Fish (save to completions)
bm25-index-tool completion fish > ~/.config/fish/completions/bm25-index-tool.fish
```

---

### Pipeline Composition

<!-- TODO: Add pipeline examples when commands support --json and --stdin -->
Compose commands with Unix pipes for powerful workflows.

**Examples:**
```bash
# Example pipeline workflows will be added when CLI commands are implemented
bm25-index-tool command --json | jq '.'
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Command not found**
```bash
# Verify installation
bm25-index-tool --version

# Reinstall if needed
cd bm25-index-tool
uv tool install . --reinstall
```

<!-- TODO: Add command-specific troubleshooting when functionality is known -->

**Issue: General errors**
- Try with verbose flag: `-vv` to see detailed error information
- Check that all prerequisites are installed
- Ensure you're using Python 3.14+

### Getting Help

```bash
# Show help
bm25-index-tool --help

# Command-specific help
bm25-index-tool COMMAND --help
```

</details>

## Exit Codes

- `0`: Success
- `1`: Client error (invalid arguments, validation failed)
- `2`: Server error (API error, network issue)
- `3`: Network error (connection failed, timeout)

## Output Formats

<!-- TODO: Update with actual output formats when commands are implemented -->

**Default Output:**
- Human-readable formatted output
- Varies by command

**JSON Output (`--json` flag):**
- Machine-readable structured data
- Perfect for pipelines and processing
- Available on commands that support structured output

## Best Practices

<!-- TODO: Add command-specific best practices -->
1. **Use verbosity progressively**: Start with `-v`, increase to `-vv`/`-vvv` only if needed
2. **Check help first**: Use `--help` to understand command options
3. **Leverage shell completion**: Install completion for better CLI experience

## Resources

- **GitHub**: https://github.com/dnvriend/bm25-index-tool
- **Python Package Index**: https://pypi.org/project/bm25-index-tool/
- **Documentation**: <!-- TODO: Add documentation URL if available -->
