---
name: ak-graphify
description: "Build queryable knowledge graphs from code, docs, papers and images."
when_to_use: "Invoke when repeated relationship queries justify a reusable graph over native search."
category: engineering
keywords: [knowledge-graph, code-analysis, tree-sitter, codebase-understanding, ast]
argument-hint: "[path] [--mcp|--report|--watch]"
related: [ak-repomix, ak-scout, ak-gkg]
maturity: beta
metadata:
  version: "1.0.1"
  author: safishamsi
  attribution: "https://github.com/safishamsi/graphify"
---

# Graphify — Knowledge Graph Builder

Turn any folder of code, docs, papers, or images into a queryable knowledge graph. Uses tree-sitter AST for code (20 languages), Whisper for audio/video, and LLM subagents for documents.

## When to Use

- Repeated architecture or dependency questions that benefit from a reusable graph
- Discovering cross-file relationships and dependency chains
- Finding "god nodes" (most-connected concepts) in large projects
- Navigating by structure instead of grepping every file
- Preparing a reusable representation when build cost is justified by repeated queries

## Installation

**Note:** The PyPI package is `graphifyy` (double-y). Other `graphify*` packages on PyPI are unaffiliated.

AgentKit already bundles this skill in the installed plugin. Do not run
`graphify install` for AgentKit setup: upstream uses that command to install a
standalone Claude skill.

```bash
# Core install
pip install graphifyy

# With MCP server support
pip install 'graphifyy[mcp]'

# Full install (MCP + PDF + video + office + Leiden community detection)
pip install 'graphifyy[all]'
```

**Requirements:** Python 3.10+

## Choose the discovery cost

For one function or a small file lookup, use native search directly. Before graph construction, inspect existing graph/cache provenance and source revision; refresh only stale inputs and verify consequential inferred edges against source. Before LLM processing, review which documents/images leave the machine and confirm that this data transfer is within the user-authorized scope. Record build time/provider cost when observable, otherwise mark unknown.

## Quick Start

```bash
# Build knowledge graph from current directory
graphify .

# Build from specific path
graphify /path/to/project

# Watch mode (auto-rebuild on file changes)
graphify . --watch
```

## Output Artifacts

| File | Purpose |
|------|---------|
| `graphify-out/graph.html` | Interactive visualization with search + community filtering |
| `graphify-out/GRAPH_REPORT.md` | God nodes, surprising connections, suggested questions |
| `graphify-out/graph.json` | Persistent graph for queries across sessions |
| `graphify-out/cache/` | SHA256-based incremental updates (only reprocesses changed files) |

## MCP Server Mode

Expose the graph as an MCP server for Claude to query directly:

```bash
python -m graphify.serve graphify-out/graph.json
```

### MCP Tools Available

| Tool | Purpose |
|------|---------|
| `query_graph` | Search for concepts and relationships |
| `get_node` | Get details of a specific node |
| `get_neighbors` | Find related concepts |
| `shortest_path` | Find connection path between two concepts |

### Claude Code MCP Setup

Add to `.claude/.mcp.json`:
```json
{
  "mcpServers": {
    "graphify": {
      "command": "python",
      "args": ["-m", "graphify.serve", "graphify-out/graph.json"]
    }
  }
}
```

## Three-Pass Architecture

1. **AST extraction (local, no API)** — tree-sitter parses code in 20 languages deterministically
2. **Audio/video transcription (local)** — Whisper runs on-device for media files
3. **Semantic extraction (API)** — LLM subagents process docs, papers, images in parallel

### Supported Languages (tree-sitter)

Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia

## Confidence Tagging

Relationships in the graph are tagged by provenance:

| Tag | Meaning |
|-----|---------|
| `EXTRACTED` | Directly from AST (imports, function calls, class inheritance) |
| `INFERRED` | LLM-derived with confidence score |
| `AMBIGUOUS` | Uncertain — needs human verification |

## Workflow Integration

### Before Planning

```bash
# Only build when repeated relationship queries justify it; otherwise scout
graphify .
# Claude reads GRAPH_REPORT.md → understands architecture → better plans
```

### With Scout

```bash
# Reuse the graph for high-level structure; scout specific files
graphify .                        # build graph
/ak-scout "auth module"           # find specific files
```

### Incremental Updates

Graph rebuilds are incremental — only changed files get reprocessed. Cache at `graphify-out/cache/` tracks file hashes.

## Privacy

- **Code:** Processed locally via tree-sitter AST. No file contents leave your machine.
- **Audio/Video:** Transcribed locally via Whisper.
- **Docs/Images:** Sent to your configured model provider (Claude/OpenAI) for semantic extraction.

## Limitations

- First build on large codebases can be slow (AST parsing + LLM calls)
- Semantic extraction quality depends on the underlying model
- Neo4j integration requires separate setup (`pip install 'graphifyy[neo4j]'`)
- Leiden community detection requires `pip install 'graphifyy[leiden]'`

## Workflow Position

**Typically precedes:** `/ak-plan` (understand architecture before planning)
**Related:** `/ak-scout` (quick file search), `/ak-repomix` (full context dump), `/ak-gkg` (semantic symbol navigation)
