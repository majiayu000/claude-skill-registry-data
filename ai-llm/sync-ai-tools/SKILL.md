---
name: sync-ai-tools
description: Sync Claude Code AI tooling (skills, MCP servers, rules) across Warp, Cursor, and VSCode. Idempotent — safe to re-run. Use when onboarding a new editor, after adding MCP servers, or when standards files change.
---

# Sync AI Tools

Keeps Claude Code as the source of truth and mirrors the relevant parts to Warp, Cursor, and VSCode so the same skills, MCP servers, and standards apply everywhere.

## What it syncs

| Asset | Source | Targets |
|---|---|---|
| Skills | `~/.claude/skills/` | `~/.agents/skills/` (Cursor reads via `~/.cursor/skills` symlink) |
| MCP servers | `~/.cursor/mcp.json` | `~/Library/Application Support/Code/User/mcp.json`, `~/.claude.json` (Warp File-based MCP reads this) |
| Standards | `~/.claude/standards/*.md` | `~/.cursor/rules/lucas-*.mdc` (agnostic subset only) |

## Run

```bash
bash ~/.claude/skills/sync-ai-tools/sync.sh
```

Prints a diff-style report of what changed.

## Prereqs

- Claude Code installed with skills in `~/.claude/skills/`
- Cursor installed (for `~/.cursor/`)
- VSCode installed (for `~/Library/Application Support/Code/User/`)
- Warp: enable **Settings → AI → MCP Servers → File-based MCP Servers** (one-time UI toggle — see `warp-ai-setup` skill)

## What it does NOT sync

- Claude-mechanism-specific standards (`rtk.md`, `session-budget.md`, hooks) — those rely on Claude Code internals that don't exist in Cursor/VSCode
- Claude hooks (settings.json PreToolUse/PostToolUse) — editor-specific, no 1:1 mapping
- Warp Workflows — managed separately in `~/.warp/workflows/`

## Re-running

Safe. Uses `rsync --delete-after` for skills and overwrites MCP configs. Prompts before deleting files in targets.
