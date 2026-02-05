---
name: encyclopedia
description: Knowledge retrieval from multiple sources. Search docs, web, and code with intelligent routing.
license: MIT
metadata:
  version: 2.1.0
  dependencies: python>=3.10
---

# Encyclopedia: The World's Knowledge

> "A billion pages, a billion facts. The Encyclopedia knows all."

## Overview

**Encyclopedia** is the knowledge skill of the Cognitive Construct. It aggregates multiple information sources into a unified, reliable interface: library documentation via Context7, web search via Exa, Perplexity, and (optionally) Kagi, code analysis via repository inspection, and optional advanced sources like SearXNG and CodeGraphContext.

The skill automatically routes queries to the most appropriate source, merges results, deduplicates using semantic similarity, and ranks by relevance. All backend queries are executed via CLI tools, keeping the interface simple and composable.

## Commands

### `search "<query>"`
Perform a general knowledge search across all available sources. Include `repo:owner/name` anywhere in the query to automatically pull repository context from `mcp-git-ingest` (and CodeGraphContext when enabled).

```bash
python3 scripts/encyclopedia.py search "repo:anthropics/anthology describe auth middleware"
```

**Options:**
- `--sources <list>`: Comma-separated list of sources to query (context7, exa, perplexity, kagi, searxng, codegraph, mcp_git_ingest)
- `--limit <n>`: Maximum results to return (default: 5)

**Output:**
```json
{
  "status": "success",
  "results": [...],
  "sources_used": ["context7", "exa", "mcp_git_ingest"],
  "degraded": false,
  "degradation": {"missing": [], "errors": []}
}
```

### `lookup "<topic>"`
Look up documentation for a specific library, API, or topic.

```bash
python3 scripts/encyclopedia.py lookup "fastapi" --version latest
```

**Options:**
- `--version <ver>`: Specific version to look up (default: latest)

**Output:**
```json
{"status": "success", "topic": "fastapi", "version": "0.115.0", "content": "..."}
```

### `code "<repo_path>" "<query>"`
Analyze a code repository and answer questions about it.

```bash
python3 scripts/encyclopedia.py code "github.com/owner/repo" "how does authentication work"
```

**Options:**
- `--depth <shallow|deep>`: Analysis depth (default: shallow)

**Output:**
```json
{"status": "success", "repository": "owner/repo", "analysis": "..."}
```

## Configuration

### Required Environment Variables

Set in `.env.local`:

```bash
# Required (at least one)
EXA_API_KEY=...           # Exa web search
PERPLEXITY_API_KEY=...    # Perplexity AI search

# Optional (enhanced capabilities)
CONTEXT7_API_KEY=...      # Higher rate limits for library docs
KAGI_API_KEY=...          # Kagi search (closed beta)
SEARXNG_URL=...           # Self-hosted SearXNG instance
NEO4J_URI=...             # CodeGraphContext (requires Neo4j)
NEO4J_USERNAME=...
NEO4J_PASSWORD=...

# Feature flags (default state shown)
ENCYCLOPEDIA_ENABLE_CONTEXT7=true
ENCYCLOPEDIA_ENABLE_KAGI=false
ENCYCLOPEDIA_ENABLE_SEARXNG=false
ENCYCLOPEDIA_ENABLE_CODEGRAPH=false
```

### CLI Tool Paths

Encyclopedia invokes CLI tools for each backend. Override paths via environment:

```bash
CONTEXT7_CLI=context7         # context7 resolve/docs commands
EXA_CLI=exa-mcp-server        # preferred; avoids collision with system `exa` (the `ls` replacement)
KAGI_CLI=kagi                 # kagi search/summarize commands
PERPLEXITY_CLI=perplexity     # perplexity query command
SEARXNG_CLI=searxng           # searxng search command
GIT_INGEST_CLI=mcp-git-ingest # mcp-git-ingest tree/read commands
CGC_CLI=cgc                   # cgc find/analyze commands
```

Note: if `exa` on your machine is the `ls` replacement (often at `/usr/bin/exa`), install `exa-mcp-server` and/or set `EXA_CLI=exa-mcp-server`.

### Credential Validation

Encyclopedia validates credentials at startup and returns clear errors:
- Missing: `"EXA_API_KEY not found"`
- CLI not found: `"cli_not_found"`

## Source Routing

Encyclopedia classifies queries and routes to appropriate sources:

| Query Type | Primary Sources | Fallback Sources |
|------------|-----------------|------------------|
| `library_docs` | context7 | exa |
| `general_search` | exa, perplexity | kagi (flagged), searxng |
| `code_context` | mcp-git-ingest (requires `repo:` hint) | exa, CodeGraphContext (optional) |

**Classification Strategy:**
1. Explicit type hint: `"doc: React"` or `"code: auth.py"` override routing.
2. Repository hints: `repo:owner/name` automatically trigger `code_context`.
3. Pattern matching: URLs → general_search; `def/class/function` → code_context.
4. Keyword triggers: `"latest"`, `"current"`, `"2024"` → general_search.
5. Default: library_docs.

## Result Merging

When multiple sources return results:

1. **Parallel query** with 5-second timeout per source
2. **Semantic deduplication**: similarity > 0.85 → merge, keeping higher-priority source
3. **Ranking**: by relevance score, then recency
4. **Source priority**: context7 > exa > perplexity > kagi > searxng

### Graceful Degradation Metadata

When any required provider is disabled via feature flag, missing credentials, or returns an error, the CLI reports:

- `degraded (bool)`: `true` if the request fell back to a reduced capability.
- `degradation.missing`: structured entries `{source, reason, optional}` describing skipped providers.
- `degradation.errors`: runtime failures (timeouts, HTTP errors) with optionality indicators.

This metadata makes it clear when optional backends (Kagi, SearXNG, CodeGraphContext) were unavailable and why, without exposing raw stack traces.

## Backend CLI Tools

Encyclopedia invokes these CLI tools for backend queries:

| Backend | CLI Command | Example |
|---------|-------------|---------|
| **Context7** | `context7 resolve <query> --json` | `context7 resolve "react hooks" --json` |
| **Exa** | `exa search <query> --json` | `exa search "python async" --json -n 5` |
| **Perplexity** | `perplexity -p <query>` | `perplexity -p "explain kubernetes"` |
| **Kagi** | `kagi search <query> --json` | `kagi --json search "rust vs go"` |
| **SearXNG** | `searxng search <query> --json` | `searxng search "linux kernel" --json` |
| **mcp-git-ingest** | `mcp-git-ingest tree <repo>` | `mcp-git-ingest tree https://github.com/owner/repo` |
| **CodeGraphContext** | `cgc find <query> --json` | `cgc find "authenticate" --json` |

All tools should be installed and available in PATH. Install via:

```bash
# Python tools (via uv)
uv tool install context7
uv tool install exa-mcp-server
uv tool install kagi
uv tool install perplexity
uv tool install searxng
uv tool install mcp-git-ingest
uv tool install codegraphcontext

# Or via npm for TypeScript tools
npm install -g @upstash/context7-mcp
npm install -g exa-mcp-server
```

## Error Handling

Encyclopedia returns structured errors without exposing internal details:

```json
{"status": "error", "code": 2, "message": "No results found for query"}
```

Error codes:
- `1`: Configuration error (missing credentials, CLI not found)
- `2`: No results / resource not found
- `3`: Backend unavailable (will use fallback)
- `4`: Internal error

## Synergies

Encyclopedia optionally integrates with other Cognitive Construct skills:

- **→ Inland Empire**: Frequently accessed topics are cached as memories
- **← Rhetoric**: Deliberation can fetch relevant documentation context

Enable synergies via `--synergy` flag or `ENCYCLOPEDIA_SYNERGY=true` environment variable.

## Files

- `~/.encyclopedia/cache/`: Response cache (TTL: 1 hour)
- `~/.encyclopedia/sessions/`: Query session history
- `resources/source_config.json`: Source priority and routing rules
