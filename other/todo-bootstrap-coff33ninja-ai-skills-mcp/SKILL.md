---
name: todo-bootstrap
description: Create or refresh a project TODO checklist using Markdown checkboxes and keep it current as work progresses. Use when a repo has no TODO tracker, when the user asks for a backlog, roadmap, status checklist, or progress board, or when docs exist but do not yet include a canonical checkbox-based task list.
agent:
  display_name: "Todo Bootstrap"
  short_description: "Create and maintain project TODO lists"
  default_prompt: "Use todo-bootstrap to add or refresh a checkbox-based project TODO list and keep it current."
---

# Todo Bootstrap

## Overview

Establish a lightweight project tracker that lives in the repo and stays aligned with the actual codebase. Prefer Markdown checkboxes with `[ ]` for incomplete work and `[x]` for complete work.

## Workflow

## 1. Inspect Existing Tracking

Check whether the repo already has a canonical tracker before creating a new one.

Look for likely files first:

- `docs/TODO.md`
- `TODO.md`
- `docs/ROADMAP.md`
- `README.md` task sections
- existing issue/backlog docs the user clearly treats as the source of truth

If a clear TODO already exists, update it instead of creating a parallel tracker.

## 2. Choose the Canonical File

Prefer these locations:

- Use `docs/TODO.md` when the repo already has a `docs/` folder.
- Use `TODO.md` at repo root when there is no docs area.
- Add a short link from `docs/INDEX.md`, `docs/README.md`, or the main `README.md` when a docs index already exists.

## 3. Use the Checkbox Format

Use Markdown checkboxes only:

- `[ ]` incomplete
- `[x]` complete

Mark items complete only when the repo actually supports them or you verified them during the task. Do not mark aspirational work as complete.

Keep items concrete and scannable. Prefer outcome-focused wording such as:

- `[x] Render uploaded VRM models in Three.js`
- `[ ] Persist chat history across reloads`
- `[ ] Add backend proxy for model requests`

## 4. Structure the File

Prefer a small structure like:

- brief convention note
- `## Completed`
- `## Incomplete`
- optional `## Next` or `## Working Agreement`

Do not create a giant speculative roadmap unless the user asks for one.

## 5. Build the Initial List from Evidence

Ground the checklist in the codebase, docs, and commands you ran.

Use:

- source files for implemented features
- package scripts and successful command results
- docs that describe intended scope
- review findings for missing pieces

If you are unsure whether something is complete, leave it unchecked and phrase it narrowly.

## 6. Keep It Current

When the user asks for changes, reviews, fixes, or next steps, update the TODO if it is the repo's chosen tracker. Add new checked items for work completed in the current task and unchecked items for newly discovered gaps that materially matter.

Avoid rewriting the whole list every turn. Prefer small, surgical updates.

## 7. Automated TODO script

A bundled script at `scripts/todo.ps1` (PowerShell) manages TODO files:

```powershell
.\scripts\todo.ps1 -Path ".\" -Action create   # create a TODO.md
.\scripts\todo.ps1 -Path ".\" -Action check    # count completed/pending
```

To use as a project-local tool:

```powershell
cp <skill-path>/todo-bootstrap/scripts/todo.ps1 .ai_scripts/
.ai_scripts\todo.ps1 -Path "." -Action check
```

## Cross-references

- **anti-premature-termination** — TODO checklists serve as completion criteria.

- **project-backup-status** — TODO checklists help track backup and restoration steps.

- **audit-project** — Audit findings should be tracked in TODO items.
- **release-changelog** — Use a checklist for multi-step releases: bump version, write changelog, run quality gates, commit, verify CI. Track each step.
- **skill-loader** — Apply the capped selection policy when deciding which tracking and validation guardrails should also be active.
