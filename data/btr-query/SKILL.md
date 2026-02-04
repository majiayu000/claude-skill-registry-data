---
name: btr-query
description: Search LOCAL BTR context tree (NOT ByteRover/brv). Use when the user asks "how did we implement", "what's our pattern for", "find context about", "query BTR", "search BTR", "find in BTR", or needs project-specific knowledge.
allowed-tools: Read, Grep, Glob, Bash
---

# BTR Query

## ⚠️ CRITICAL: BTR ≠ ByteRover

**This skill uses `btr` (local context tree), NOT `brv` (ByteRover CLI).**

| Command | Tool | Syntax |
|---------|------|--------|
| ✓ CORRECT | `btr` | `btr query "search term"` / `btr list` / `btr stats` |
| ✗ WRONG | `brv` | Different tool, different syntax, requires auth |

**PREFER MCP tools when available:**
- `mcp__btr__query_context` - For searching
- `mcp__btr__list_contexts` - For browsing
- `mcp__btr__get_stats` - For statistics

Only use Bash `btr` commands if MCP tools are unavailable.

Find and retrieve relevant context using intelligent search.

## Quick Start

```bash
btr query "<natural language query>" [--domain <domain>] [--limit <n>]
```

## Instructions

1. Understand the user's information need
2. Formulate a natural language query
3. Optionally filter by domain for more focused results
4. Run the CLI command
5. Present results with relevance context
6. Offer to retrieve full content if summary shown

## Examples

### Find authentication patterns
```bash
btr query "how do we handle JWT authentication"
```

### Search within a specific domain
```bash
btr query "rate limiting implementation" --domain api
```

### Get more results
```bash
btr query "error handling" --limit 10
```

For advanced query patterns, see [advanced-queries.md](advanced-queries.md).
