---
name: context7-tools
type: complex
depth: base
user-invocable: false
description: >-
  Queries Context7 library documentation via Python CLI. Use when resolving
  library IDs, fetching API references, code examples, or conceptual guides.
---

# [H1][CONTEXT7-TOOLS]
>**Dictum:** *Three commands mirror MCP capabilities plus unified convenience.*

<br>

Query Context7 library documentation. Matches MCP tool structure.

---
## [1][COMMANDS]

| [CMD]    | [ARGS]                   | [RETURNS]                              |
| -------- | ------------------------ | -------------------------------------- |
| resolve  | `<library> [query]`      | Top 5 matching IDs with scores         |
| docs     | `<library-id> <query>`   | Documentation filtered by query        |
| lookup   | `<library> <query>`      | Resolve + docs in one call             |

---
## [2][USAGE]

```bash
# Resolve library → see options
uv run .claude/skills/context7-tools/scripts/context7.py resolve effect

# Fetch docs for specific ID
uv run .claude/skills/context7-tools/scripts/context7.py docs /effect-ts/effect "Services"

# Unified: resolve + docs
uv run .claude/skills/context7-tools/scripts/context7.py lookup react "hooks"
```

Slash command: `/lib-docs react "hooks and state"`

---
## [3][SELECTION_LOGIC]

`lookup` auto-selects library by: VIP status → highest benchmark score.

Use `resolve` first when disambiguation needed.

