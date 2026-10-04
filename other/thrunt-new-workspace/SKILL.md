---
name: thrunt-new-workspace
description: Create an isolated workspace with repo copies and independent .planning/
argument-hint: "--name <name> [--repos repo1,repo2] [--path /target] [--strategy worktree|clone] [--branch name] [--auto]"
allowed-tools: Read, Bash, Write, AskUserQuestion
---

<context>
**Flags:**
- `--name` (required) — Workspace name
- `--repos` — Comma-separated repo paths or names. If omitted, interactive selection from child git repos in cwd
- `--path` — Target directory. Defaults to `~/thrunt-workspaces/<name>`
- `--strategy` — `worktree` (default, lightweight) or `clone` (fully independent)
- `--branch` — Branch to checkout. Defaults to `workspace/<name>`
- `--auto` — Skip interactive questions, use defaults
</context>

<objective>
Create a physical workspace directory containing copies of specified git repos (as worktrees or clones) with an independent `.planning/` directory for isolated THRUNT sessions.

**Use cases:**
- Multi-repo orchestration: work on a subset of repos in parallel with isolated THRUNT state
- Feature branch isolation: create a worktree of the current repo with its own `.planning/`

**Creates:**
- `<path>/WORKSPACE.md` — workspace manifest
- `<path>/.planning/` — independent planning directory
- `<path>/<repo>/` — git worktree or clone for each specified repo

**After this command:** `cd` into the workspace and run `/hunt-new-program` to initialize THRUNT.
</objective>

<execution_context>
@.github/thrunt-god/workflows/new-workspace.md
@.github/thrunt-god/references/ui-brand.md
</execution_context>

<process>
Execute the new-workspace workflow from @.github/thrunt-god/workflows/new-workspace.md end-to-end.
Preserve all workflow gates (validation, approvals, commits, routing).
</process>
