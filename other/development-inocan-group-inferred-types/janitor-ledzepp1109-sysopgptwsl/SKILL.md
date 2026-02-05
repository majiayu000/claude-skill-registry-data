---
name: janitor
description: >-
  Safe cleanup + de-bloat operator for SYSopGPTWSL. Inventories candidates,
  proposes an action plan, and only deletes after explicit user confirmation.
  Defaults to repo-scoped, reversible moves into `sysop/out/janitor_trash/`.
  Use when the user says “clean up”, “cleanup”, “delete”, “remove duplicates”,
  “free disk space”, “declutter”, or “bloat”.
short-description: Safe cleanup (list → approve → act)
triggers:
  - janitor
  - clean up
  - cleanup
  - declutter
  - de-bloat
  - bloat
  - free disk space
  - remove duplicates
  - delete duplicates
  - delete files
  - remove files
  - purge
  - prune
version: 1.0.0
codex-version: ">=0.76.0"
metadata:
  short-description: Janitor protocol for safe cleanup
---

# Janitor Skill (SYSopGPTWSL)

## Contract

- **Never delete by surprise.** Always: **inventory → present → wait for approval → act → verify**.
- **Repo-scope first.** Do not modify/delete outside this repo unless the user explicitly asks *and* you generate manual scripts under `sysop/out/fixes/` (no auto host changes).
- **Prefer reversible actions.** Default action is to **move** candidates into `sysop/out/janitor_trash/<timestamp>/` and print a rollback command.
- **Evidence discipline.** Back non-obvious claims with command output.
- **No destructive ops**: never run `rm -rf`, `git reset --hard`, `git clean -fdx`.

## Do Now (flow)

### 0) Confirm scope + goal

Ask 1–3 short questions only if needed:
- Target roots (default: repo only)
- What “bloat” means (examples: build artifacts, backups, duplicates, logs)
- Safety mode: **report-only** vs **stage-to-trash** vs **delete**

### 1) Inventory (report-only first)

Produce a table with:
- full path
- bytes (or human size)
- last modified
- why it’s a candidate

Repo-first inventory hints:
- Large artifacts under `sysop/out/` (regeneratable reports)
- Old `*.bak-*` backups inside repo
- Duplicate seed rebuild artifacts like `sysop/out/fixes/**/objects.bak-*` (keep unless user wants to purge)
- Untracked large dirs causing snapshot warnings

### 2) Propose an action plan (no changes yet)

Group candidates into:
- **Safe to stage** (move to `sysop/out/janitor_trash/…`)
- **Requires review** (ambiguous value)
- **Never touch** (source code, canonical docs, anything the user flags)

### 3) Get explicit approval (required)

Ask the user to reply with one of:
- `STAGE <id list>` (preferred)
- `DELETE <id list>` (only if staging is rejected)
- `SKIP`

### 4) Execute (only after approval)

Default execution method:
- Create a timestamped trash folder: `sysop/out/janitor_trash/YYYYMMDD-HHMMSS/`
- Move candidates there (preserve paths by recreating dirs)
- Print rollback command that moves everything back

If user explicitly chooses delete:
- Delete only the approved items, using the least-destructive command possible (no `rm -rf`).

### 5) Verify + report

Show:
- what moved/deleted
- reclaimed space estimate
- rollback instructions (even if delete was chosen, note it’s irreversible)

## If user wants cleanup outside the repo

- Do **not** perform the cleanup directly from this repo run.
- Generate a reviewed script/instructions under `sysop/out/fixes/` (PowerShell or bash), including:
  - backups (`*.bak-YYYYMMDD-HHMMSS`) where relevant
  - rollback commands
  - a “dry run” mode if possible
