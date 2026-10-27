---
name: cocoindex-code
description: >
  Semantic vector search over the codebase — find code by meaning, not exact names.
  Use when you need to locate implementations without knowing exact function/class names.
  Triggers on: "find code", "search codebase", "locate implementation", "what does X do"
allowed-tools: []
effort: low
---

# cocoindex-code — Semantic Search

Finds code by meaning using local vector embeddings (no API key, works offline).
Complement to codebase-memory-mcp (structural) — use both for complete discovery.

## When to Use This vs Other Tools

| Use cocoindex-code | Use codebase-memory-mcp instead |
|--------------------|---------------------------------|
| "find code that handles rate limiting" | "who calls `rateLimit()`?" |
| "locate authentication middleware" | "what does `AuthService` import?" |
| "find all error handling patterns" | "trace path from HTTP handler to DB" |
| Exploring unfamiliar codebase | Tracing known functions |
| Fuzzy conceptual search | Exact structural traversal |

## The One Tool: `search`

```json
{
  "query": "string — natural language or code snippet",
  "limit": 5,
  "offset": 0,
  "refresh_index": true,
  "languages": ["python", "typescript"],
  "paths": ["src/auth/*"]
}
```

**Result:** Array of `{file_path, language, content, start_line, end_line, score}`.

**After getting results:** Use the `Read` tool on `file_path` at `start_line`–`end_line` for full context.

## Performance Tips

- Set `refresh_index: false` for consecutive searches in the same session (no code changes)
- Use `languages` filter to scope search (faster for single-language queries)
- Use `paths` filter to limit to a directory (triggers full scan — slower than language filter)
- Default limit is 5. Increase to 10–20 for broad exploration.

## Lifecycle Management

**Index not built yet:** `ccc index` — or handled automatically on first MCP search.

**After major changes:** Index auto-refreshes on each MCP search call (`refresh_index=True` default).

**Check status:** `ccc status` shows chunks and file counts.

**Switch embedding model:** Edit `~/.cocoindex_code/global_settings.yml`, then `ccc reset && ccc index`.
Warning: model switch requires full re-index — different vector dimensions are incompatible.

## Supported Languages (29)

Python, JavaScript, TypeScript/TSX/JSX, Rust, Go, Java, C, C++, C#, SQL,
Shell/Bash, Markdown, PHP, Lua, Ruby, Swift, Kotlin, Scala, R, HTML, CSS/SCSS,
JSON, YAML/TOML, XML, Solidity, Pascal, Fortran, plain text.
