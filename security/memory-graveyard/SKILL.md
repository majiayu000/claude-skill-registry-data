---
name: memory-graveyard
description: Audit which entries in your project's MEMORY.md Claude actually reads. Use when the user wants to find dead memory entries, broken pointers in MEMORY.md, orphan memory files, or surface entries that fall below the system-prompt truncation cutoff. Triggers on "audit MEMORY.md", "dead memory entries", "broken memory pointers", "memory hygiene", "unused memory", "memory truncation". Runs locally; reads ~/.claude/projects session JSONL logs and memory directories. No network calls.
license: MIT
metadata:
  author: sfrangulov
  version: "1.0.0"
---

# memory-graveyard

CLI that audits per-project file-based memory (`MEMORY.md` index + `memory/*.md` entries). Bucketed audit (ACTIVE / DEAD / MISSING / HALLUCINATED) plus a static linter that flags broken pointers, orphan files, truncation-budget overflow, index size, and stale dated entries.

## How to invoke

Run via `npx memory-graveyard@latest <subcommand> [flags]` — no install needed.

## Subcommands

- `audit` (default) — 4-bucket per-project table. Flags: `--days N`, `--only <bucket>`, `--json`, `--project <path>`, `--claude-dir <path>`.
- `lint` — static checks on `MEMORY.md` and the memory dir. Flags: `--truncation-cutoff N` (default 200), `--stale-days N` (default 30), `--json`. Exit 1 on findings.
- `prune` — plan removal of dead entries and hallucinated pointers. `--apply` to execute (with snapshot backup in `.graveyard-backup/<timestamp>/`). `--include orphans|broken-pointers`, `--exclude <basename>`.
- `projects` — cross-project sweep, surfaces cold memory dirs. `--cold-days N` (default 90).

## Decision flow

- "what entries in my MEMORY.md are dead?" → `npx memory-graveyard@latest`
- "is anything in MEMORY.md broken?" → `npx memory-graveyard@latest lint`
- "clean up MEMORY.md" → `prune`, then `--apply`
- "which projects have stale memory dirs?" → `projects`

After running, print output verbatim. Do not summarize unless the user asks.
