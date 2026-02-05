---
name: patch-agents-md-option-b
description: Update repository AGENTS.md for Option B (Tauri v2 + React/TypeScript desktop local-first) with executable commands, guardrails, and security/permission rules; creates backups and can add nested AGENTS.md.
---

## What this skill does

When invoked, this skill patches the repository instruction files that Codex and other coding agents read:

- Writes/updates **`AGENTS.md`** in the repo root for the Option B desktop architecture (Tauri v2 + React/TS + Rust orchestrator + Python sidecar).
- Optionally writes nested instruction files if the target directories exist:
  - `src-tauri/AGENTS.md` (Rust / Tauri backend)
  - `src/AGENTS.md` (React frontend)
- Creates timestamped backups under `.codex/backups/<timestamp>/...` before overwriting.

## When to use

Use this skill when the team has committed to **Option B** and you want AI coding agents to:

- run the correct dev/test commands,
- respect Desktop-local-first constraints (Workspace + Runs),
- treat Tauri capabilities / plugin scopes / sidecar execution as security-sensitive.

## How to run

From the repository root:

```bash
python .codex/skills/patch-agents-md-option-b/scripts/apply.py --dry-run
python .codex/skills/patch-agents-md-option-b/scripts/apply.py
```

### Options

- Root file only (skip nested files):

```bash
python .codex/skills/patch-agents-md-option-b/scripts/apply.py --no-nested
```

- Force overwrite (still makes backups):

```bash
python .codex/skills/patch-agents-md-option-b/scripts/apply.py --force
```
