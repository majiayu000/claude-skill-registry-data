---
name: mcp-graveyard
description: Audit which MCP server tools your Claude Code sessions actually invoke. Use when the user wants to find dead MCP servers (configured but never called), hallucinated MCP tool calls, or per-project MCP usage. Triggers on "which MCP servers don't I use?", "clean up MCP config", "remove unused MCP servers", "audit MCP tools". Runs locally; reads ~/.claude session JSONL logs and ~/.claude.json. No network calls.
license: MIT
metadata:
  author: sfrangulov
  version: "1.0.0"
---

# mcp-graveyard

CLI that audits MCP server tool usage. Server-first table grouped into ACTIVE / DEAD / HALLUCINATED / MISSING buckets.

## How to invoke

Run via `npx mcp-graveyard@latest <subcommand> [flags]` — no install needed.

## Subcommands

- `audit` (default) — classify every server. Flags: `--days N`, `--only <bucket>`, `--tools <server>` (drill-in), `--json`, `--claude-dir <path>`.
- `prune` — print removal plan. `--apply` to execute (with auto-backup of removed config to a timestamped file).
- `suggest` — actionable triage for unused/hallucinated.
- `projects` — per-project breakdown.

## Decision flow

- "which MCP servers do I not use?" → `npx mcp-graveyard@latest`
- "clean up MCP config" → `prune`, then `--apply`
- "MCP tool didn't work" → `suggest`
- per-project breakdown → `projects`

After running, print output verbatim. Do not summarize unless the user asks.
