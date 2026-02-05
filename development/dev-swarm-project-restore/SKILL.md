---
name: dev-swarm-project-restore
description: Restore a project from 99-archive, a remote git repo, or a local codebase back to the workspace root, including reconstructing missing docs, stages, and sprints. Use when the user asks to resume work on an existing project.
---

# AI Builder - Project Restore

This skill restores an existing project to the workspace root from an archive, remote git repo, or local codebase, including re-adding `src` and reconstructing missing docs when needed.

## When to Use This Skill

- User asks to restore a project from `99-archive/`
- User wants to restore a project from a remote git repository or a non-archived local codebase
- User needs `ideas.md`, stage folders, or sprints reconstructed to resume work

## Your Roles in This Skill

See `dev-swarm/docs/general-dev-stage-rule.md` for role selection guidance.

## Role Communication

See `dev-swarm/docs/general-dev-stage-rule.md` for the required role announcement format.

## Instructions

Follow these steps in order:

### Step 1: Archive the Current Project

Archive the current project using agent skill `dev-swarm-project-archive`.

### Step 2: Identify the Restore Source

Confirm whether the source is:
- `99-archive/{archive-folder}`
- Remote git repository URL
- Local codebase path (not created by archive; with or without git history)

Record the source in your notes before proceeding.

### Step 3: Restore the Project

- If restoring from `99-archive/`, follow `references/restore-procedure.md`.
- If restoring from a remote git repo or local codebase, follow `references/external-restore.md`.

### Step 4: Reverse-Engineer Missing Docs (If Needed)

If the codebase has little or no documentation, follow `references/reverse-engineering.md` to reconstruct:
- `ideas.md`
- stage folders `00-*` through `10-*`
- sprints and backlogs in `09-sprints/`
- feature specs under `features/`

## Expected Output

- Archived project content restored to workspace root
- `ideas.md` present at the root
- `src/` re-added as a submodule at the correct commit
- `99-archive/` retains the archived snapshot
- Reconstructed stages, sprints, and features when docs were missing

## Key Principles

- Keep the restore process reversible and traceable in git history
- Prefer existing git history to restore the `src` submodule state
- Ask for user approval before destructive or irreversible operations
