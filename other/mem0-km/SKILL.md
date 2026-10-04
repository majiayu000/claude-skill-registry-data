---
name: mem0_KM
description: Shared long-term memory system — search, store, and recall facts across all agents and machines via self-hosted mem0 REST API
globs:
  - "**/*"
alwaysAllow: []
---
# Mem0 — Shared Long-Term Memory

Self-hosted mem0 (v1.2.0) on Mac Studio provides persistent, semantic memory shared across all AI agents and machines.

## Quick Reference

| Operation | Method | Endpoint | Body |
|-----------|--------|----------|------|
| **Search** | POST | `/search` | `{"query": "...", "user_id": "kosta", "limit": 10}` |
| **Add** | POST | `/memories` | `{"messages": [{"role": "user", "content": "..."}], "user_id": "kosta", "metadata": {...}}` |
| **List** | GET | `/memories?user_id=kosta` | — |
| **Delete** | DELETE | `/memories/{id}` | — |
| **Update metadata** | PATCH | `/memories/{id}/metadata` | `{"metadata": {...}}` |

**Base URL**: `http://100.69.228.58:8888` (Tailscale, no auth required)

## Access Methods

### MCP Tools (Claude Code, Craft Agent, Codex)
If mem0 MCP is configured, use tools directly:
- `search_memories` — semantic search
- `add_memory` — store a new memory
- `get_memories` — list all memories
- `delete_memory` — delete by ID

### REST API (curl, any agent)
```bash
# Search
curl -s -X POST http://100.69.228.58:8888/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "coding preferences", "user_id": "kosta", "limit": 5}'

# Add
curl -s -X POST http://100.69.228.58:8888/memories \
  -H 'Content-Type: application/json' \
  -d '{"messages": [{"role": "user", "content": "Kosta uses bun as default package manager"}], "user_id": "kosta", "metadata": {"category": "preferences", "source": "my-agent"}}'

# List all
curl -s "http://100.69.228.58:8888/memories?user_id=kosta"
```

## Metadata Schema (5 fields)

Every memory should include metadata. Set at write time or patch later.

| Field | Required | Type | Values |
|-------|----------|------|--------|
| `category` | **Yes** | string | `coding` · `environment` · `preferences` · `personal` · `workflow` |
| `source` | **Yes** | string | Agent identifier: `craft-agent`, `claude-code`, `hermes`, `codex`, `droid`, etc. |
| `machine` | Only if host-specific | string | `macbook`, `studio`, `mini` |
| `expires_at` | If temporal | string | ISO 8601 datetime |
| `sensitive` | If private | boolean | `true` / `false` |

### Category Guide
- **coding** — languages, frameworks, patterns, project structure, tooling
- **environment** — machine setup, paths, installed software, configs
- **preferences** — user preferences, workflow habits, communication style
- **personal** — bio, contacts, schedule, non-technical facts
- **workflow** — processes, conventions, team agreements, active projects

## Usage Protocol

1. **Search before work** — at the start of every substantive task, search mem0 for relevant context
2. **Store after learning** — when you learn a stable fact, preference, or decision, store it
3. **Always tag** — set `category` and `source` in metadata on every write
4. **Dedup** — search before writing to avoid storing duplicate facts
5. **Don't store** — secrets, tokens, credentials, ephemeral session data, or transient state
6. **Don't set `machine`** — unless the fact is specific to one machine (e.g., a path that only exists on Studio)

## Pitfalls

- **`add_memory` is slow** (10-30s) — mem0 uses an LLM to extract facts from your content. This is normal.
- **Content is auto-decomposed** — mem0 breaks your input into atomic facts. Write naturally, don't over-structure.
- **Search is semantic** — use natural language queries, not keywords. "What package manager does Kosta prefer?" works better than "bun npm".
- **`user_id` defaults to `kosta`** — no need to specify unless working with a different user.
- **Graph relations** — Neo4j stores entity relationships automatically. Search results may include a `relations` array.
