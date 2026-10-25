---
name: codex-sessions-manager
description: Use this skill when the user wants to inspect, search, export, verify,
  clean up, delete, restore, or purge local Codex sessions stored under ~/.codex.
metadata:
  source: https://github.com/1939869736luosi/codex-sessions-manager
---

# Codex Sessions Manager

## Overview

CLI-first local Codex history audit and recovery tool. Use official Codex for normal task management and permanent deletion. Use this tool to verify what remains under `~/.codex`, inspect legacy or damaged state, and perform previewable recoverable cleanup for confirmed residual IDs.

This is not a UI product, TUI, detail page, incremental scanner, or automatic cleanup service.

## Setup

```bash
npm install -g codex-sessions-manager
codex-sessions --version
```

The default Codex root is `~/.codex`. Use `--root <path>` for a different root.

For official Codex Skill discovery, place this Skill directory at either:

- project scope: `.agents/skills/codex-sessions-manager`
- user scope: `$HOME/.agents/skills/codex-sessions-manager`

The distributed Skill includes `agents/openai.yaml` inside the Skill directory.

## When To Use

- List/filter/search sessions (by project, time, status, source)
- Show session detail or timeline
- Inspect session family (parent/child/subagent/side/fork)
- Audit and verify what remains locally after official deletion
- Scan root for likely residue candidates
- Preview batch delete scope without executing
- Build explicit-ID delete plans
- Export session backup
- Delete sessions (permanent or recoverable trash)
- Restore or purge trash entries
- Verify post-delete cleanliness
- Clean stale JSONL indexes

## CLI Quick Reference

```bash
codex-sessions doctor [--json] [--details]
codex-sessions list [--limit N] [--project TEXT] [--status S] [--source-kind K]
codex-sessions sources [--json]
codex-sessions projects
codex-sessions show <id> [--json]
codex-sessions events <exact-id> [--output FILE]
codex-sessions family <id> [--children|--parents|--subagents|--impact|--full]
codex-sessions audit <id> [--json]
codex-sessions audit-root [--limit 50] [--status S...] [--source S...]
codex-sessions preview-root [--limit 50] [--status S...] [--source S...]
codex-sessions monthly-review [--limit 50] [--status S...] [--source S...] [--details]
codex-sessions export <id> [--output ./backup.json]
codex-sessions plan-delete <id...> [--include-children] [--include-family] [--json]
codex-sessions plan-delete --source-kind K --limit N [--json]
codex-sessions preview-plan <file> [--json]
codex-sessions delete <full-uuid...> [--trash] [--yes] [--allow-active]
codex-sessions trash-list
codex-sessions restore <exact-trash-id> --yes
codex-sessions purge <exact-trash-id> --yes
codex-sessions cleanup-index <full-uuid...> [--yes] [--allow-active]
codex-sessions cleanup-stale [--yes]
codex-sessions verify <id...>
codex-sessions recovery-status [--json]
codex-sessions recover <exact-operation-id> --yes
```

## Safety Rules

- All destructive commands require `--yes` (CLI) or `confirm=true` (MCP); without it you get preview only.
- Always run a separate preview before any destructive action, then require explicit user confirmation.
- `preview`, `plan-delete`, `family`, `impact`, `audit-root`, `preview-root`, `monthly-review` are read-only. They are never deletion authorization.
- Permanent delete removes only exact thread-linked logs. Trash retains them; restore leaves them unchanged; final purge removes them unless that ID is live again. Memory is always retained.
- Delete never recursively adds parent, child, or family sessions. List every intended ID explicitly.
- Allowlisted exact-key global-state refs are removable only through explicit-ID confirmed delete.
- Unknown global-state refs are warnings only; do not delete them automatically.
- Confirmed session mutations require full canonical UUIDs. Active-session deletion also requires `--allow-active` / `allowActive=true`.
- An interrupted write keeps an exclusive lock and durable recovery record. Inspect it before running the exact confirmed recovery operation.
- A committed operation with partial or failed verification remains committed and must be reported that way.

## MCP (Optional, Advanced)

```bash
codex-sessions-mcp                       # default: read-only profile (16 bounded tools)
codex-sessions-mcp --profile admin       # all 22 tools including destructive ops
```

Invalid `--profile` values exit with code 1. Default is read-only for safety.

`get_session` defaults to `detail=compact` (20 items / 64 KiB / 1 MiB source read). `detail=full` is still bounded (200 items / 256 KiB / 8 MiB source read). Session metadata is bounded too. Both return explicit completeness metadata; `sourceCompleteness` preserves parse/unsupported status when the MCP envelope is also `truncated_limit`, and `itemsKnown=null` means the reader stopped before EOF. `list_sessions` defaults to 50 concise records, accepts at most 200, and caps the response at 256 KiB. Use CLI JSON for complete local result sets and `export` for a JSON recovery bundle whose embedded text or base64 data can reconstruct source-file bytes.

All other MCP structured responses also have a final 256 KiB / 200-items-per-collection cap. Explicit session operations accept at most 50 IDs; `list_trash` defaults to 50 entries. Limit hits return `responseCompleteness` and `responseOmittedReason`. Exact backup export is CLI-only.

## Detailed References

For full CLI/MCP parameter reference, safety model, and advanced rules:

- [Detailed tool reference](docs/SKILL_DETAIL.md)
- [Safety guide](docs/SAFETY.md)
