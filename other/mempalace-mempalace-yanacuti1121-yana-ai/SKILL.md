---
name: mempalace--mempalace
description: "Local-first AI memory system — 96.6% R@5 trên LongMemEval, verbatim storage (không lossy summary), MCP server 29 tools, ChromaDB/Qdrant/pgvector backends. Zero API calls."
allowed-tools: Bash, Read, Write
user-invocable: true
---

MemPalace: hệ thống bộ nhớ AI local-first, benchmark cao nhất open-source — lưu verbatim (không tóm tắt), retrieval theo không gian (wing/room/drawer).

## Install

```bash
uv tool install mempalace
# hoặc
pipx install mempalace
```

## Cách dùng

```bash
# Index project hoặc Claude Code conversation archives
mempalace mine ./project/

# Semantic search
mempalace search "database migration strategy"

# Load context cho session mới
mempalace wake-up
```

## Architecture

```
Palace structure:
  Wing  — người, project (top-level namespace)
  Room  — topic trong wing
  Drawer — content gốc verbatim

Backends:
  ChromaDB  (default, local)
  SQLite    (exact match, correctness verification)
  Qdrant    (REST external)
  pgvector  (PostgreSQL)
```

## MCP Server

```json
{
  "mcpServers": {
    "mempalace": {
      "command": "mempalace",
      "args": ["mcp"]
    }
  }
}
```

29 tools: palace operations, cross-wing navigation, agent diaries, search.

## Performance

```
96.6% R@5 on LongMemEval  — zero API calls (embedding only)
98.4% R@5                 — hybrid pipeline (keyword + temporal boost)
>99%                      — với LLM reranking (Claude/Ollama compatible)
```

## Tính năng nổi bật

- **Verbatim storage** — không lossy extraction, không paraphrase
- **Knowledge graph** — temporal entity-relationship với validity windows
- **Auto-save hooks** — periodic save + pre-compression backup cho Claude Code
- **Agent diaries** — per-agent wings riêng, runtime discovery
- **Privacy** — không có gì rời máy trừ khi opt-in

## So với Memory OS

| | MemPalace | Memory OS |
|--|---------|-----------|
| Storage | Verbatim | Summarized |
| Benchmark | 96.6% LongMemEval | N/A |
| Backends | 4 pluggable | Qdrant only |
| MCP tools | 29 | 16 |
| Layers | 1 (palace metaphor) | 7 |

## Source

https://github.com/MemPalace/mempalace · MIT · +446⭐ today
