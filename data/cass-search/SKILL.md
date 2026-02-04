---
name: cass-search
description: Search past AI sessions with CASS. Use when looking for past solutions, searching session history, finding how something was done before, or when the user mentions "cass", "history", or "past sessions".
---

# CASS (Cross-Agent Session Search)

Search and retrieve content from past AI coding sessions.

## When This Applies

| Signal | Action |
|--------|--------|
| "How did we do this before?" | `cass search` |
| "Find past solutions" | `cass search` |
| Looking for patterns | `cass search` |
| View specific session | `cass view` |
| Today's activity | `cass timeline` |

---

## CRITICAL RULE

**Always use `--robot` or `--json`. Never run bare `cass`.**

Bare `cass` launches a TUI that will hang AI agents.

---

## Search

```bash
# Basic search
cass search "query" --robot --limit 5

# Lean output (path, line, agent)
cass search "query" --robot --fields minimal

# With summary (title, score)
cass search "query" --robot --fields summary

# Token budget
cass search "query" --robot --max-tokens 2000

# Wildcard prefix
cass search "auth*" --robot

# Workspace-specific
cass search "query" --workspace "/path/to/project" --robot
```

---

## View & Expand

```bash
# View full session
cass view /path/to/session.jsonl --json

# Expand specific line with context
cass expand /path -n 42 -C 3 --json
```

---

## Timeline

```bash
# Today's sessions
cass timeline --today --json

# Last week
cass timeline --since 7d --json

# Recent activity
cass timeline --days 7 --json --limit 10
```

---

## Export

```bash
cass export /path/session.jsonl --format markdown
cass export /path/session.jsonl --format json
```

---

## Indexing

```bash
# If search returns nothing
cass index --full

# Health check
cass health
```

---

## Output Formats

```bash
--robot-format jsonl     # Streaming line-delimited JSON
--robot-format compact   # Minimal output
```

---

## Query Tips

| Query Type | Example |
|------------|---------|
| Exact phrase | `"error handling"` |
| Wildcard | `auth*` |
| Multiple terms | `database migration` |
| Recent | Add `--since 7d` |

---

## Quick Reference

```bash
cass search "query" --robot --limit 5      # Basic search
cass search "query" --robot --fields minimal   # Lean output
cass view /path.jsonl --json               # View session
cass expand /path -n 42 -C 3 --json        # Expand with context
cass timeline --today --json               # Today's activity
cass index --full                          # Rebuild index
```

---

## When to Use CASS vs Other Tools

| Need | Use |
|------|-----|
| Past session content | CASS |
| Learned patterns/rules | cass-memory (`cm`) |
| Current codebase | Warp-Grep or Grep |
| Web documentation | Exa |
| Task graph | bv |

---

## See Also

- `cass-memory/` — Cross-agent learning with `cm`
- `project-memory/` — Session context retrieval
