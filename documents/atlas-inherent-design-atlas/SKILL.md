---
name: atlas
description: Ingest project documentation and code into persistent semantic memory (Qdrant + Voyage embeddings). Use when user wants to remember context across sessions, ingest docs, or search previous work. Requires Qdrant running locally and VOYAGE_API_KEY set.
allowed-tools: Bash(bun:*)
---

# Atlas - Persistent Semantic Memory

Atlas provides automatic context ingestion and retrieval using Voyage embeddings + Qdrant vector database. Solves the context overflow problem by storing knowledge persistently across sessions.

## Quick Start

### Prerequisites

1. **Qdrant running locally**:

```bash
docker run -d -p 6333:6333 qdrant/qdrant
```

2. **VOYAGE_API_KEY set** (get from https://voyageai.com):

```bash
export VOYAGE_API_KEY="your-key-here"
```

3. **Verify setup**:

```bash
curl http://localhost:6333/health
```

## Ingesting Context

Store files in Atlas memory for persistent retrieval:

### Ingest Single File

```bash
cd ~/production/atlas
bun run --filter @inherent.design/atlas atlas ingest /path/to/file.md
```

### Ingest Directory (Recursive)

```bash
cd ~/production/atlas
bun run --filter @inherent.design/atlas atlas ingest /path/to/docs/ --recursive
```

### Ingest Multiple Paths

```bash
cd ~/production/atlas
bun run --filter @inherent.design/atlas atlas ingest README.md src/index.ts docs/ -r
```

**What gets ingested**:

- Supported: `.md`, `.ts`, `.tsx`, `.js`, `.jsx`, `.json`, `.yaml`, `.qntm`, `.rs`, `.go`, `.py`, `.sh`, `.css`, `.html`
- Ignored: `node_modules`, `.git`, `dist`, `build`, `coverage`, `.atlas`

**Processing**:

- Chunks text (768 tokens, 13% overlap) for semantic coherence
- Embeds with Voyage-3-large (1024-dim)
- Stores in Qdrant with dual-indexing (semantic QNTM keys + temporal timestamps)
- Preserves original text for future consolidation

## Searching Context

Retrieve relevant context semantically:

### Basic Search

```bash
cd ~/production/atlas
bun run --filter @inherent.design/atlas atlas search "typescript patterns"
```

### Limited Results

```bash
cd ~/production/atlas
bun run --filter @inherent.design/atlas atlas search "memory consolidation" --limit 10
```

### Temporal Filtering (Since Date)

```bash
cd ~/production/atlas
bun run --filter @inherent.design/atlas atlas search "sleep patterns" --since "2025-12-25"
```

### Chronological Timeline

```bash
cd ~/production/atlas
bun run --filter @inherent.design/atlas atlas timeline --since "2025-12-01"
```

## When to Use This Skill

**Use Atlas when**:

- User asks to "remember this across sessions"
- Project context is too large for single session
- User wants to search previous work/decisions
- Documentation needs to be queryable
- Building on previous research or code

**Examples**:

- "Remember the API architecture we discussed"
- "What did we decide about the database schema?"
- "Find all mentions of authentication patterns"
- "Ingest all the .atlas research files"

## Architecture

Built on .atlas research (Steps 1-4 + Sleep Patterns):

**Stack**:

- Voyage-3-large embeddings (1024-dim, 9.74% better than OpenAI)
- Qdrant HNSW index (M=16, int8 quantization, 4x compression)
- RecursiveCharacterTextSplitter (semantic boundaries)
- Dual-indexing (QNTM semantic keys + RFC 3339 timestamps)

**Production Config** (from Step 3 research):

- Recall@10: >0.98
- Latency: 10-50ms (p95)
- Memory: 1.4GB RAM + 5GB disk per 1M vectors

## Technical Details

For implementation details, see:

- [docs/architecture.md](../docs/architecture.md) - Complete technical architecture

Packages:

- `@inherent.design/atlas-core` - Core library (embeddings, storage, search)
- `@inherent.design/atlas` - Command-line interface
- `@inherent.design/atlas-mcp` - MCP server for Claude Code integration
