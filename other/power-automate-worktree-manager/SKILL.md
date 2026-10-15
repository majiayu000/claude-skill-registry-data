---
name: power-automate-worktree-manager
description: "Manage git worktrees for parallel Power Automate flow development with Claude Code: create isolated worktrees, coordinate merges, clean up. Use when building several flows in parallel, running parallel Claude Code sessions, or merging completed flows."
---

# Power Automate Worktree Manager

Orchestrate parallel Power Automate flow development using git worktrees and multiple Claude Code instances.

## When to use

- Building several Power Automate flows at once (3+), or flows for different companies/clients in parallel.
- Testing different approaches to the same flow.
- Coordinating the merge of completed flows to the main branch and the cleanup afterwards.

## Quick start

### 1. Create the worktrees

```bash
python scripts/create_worktrees.py <flow-name-1> <flow-name-2> ... [options]
```

Options: `--base <branch>` (default: current branch), `--prefix <prefix>` (default `flow`), `--no-env` (skip copying env files), `--no-todo` (skip `.llm/todo.md`).

It creates one isolated worktree directory and one feature branch per flow (for example `flow/sharepoint-approval`), copies `.env` files, writes `.llm/todo.md` for Claude Code context and prints the paths. Create worktrees from the same, freshly pulled base branch.

### 2. Start Claude Code in each worktree

One terminal per worktree (`cd ../my-repo-<flow> && claude`). In each session use the custom slash commands (`/build-flow`, `/validate-flow`), work independently, commit regularly to the feature branch.

### 3. Merge completed work

```bash
bash scripts/manage_worktrees.sh                                  # interactive (recommended)
bash scripts/manage_worktrees.sh merge flow/sharepoint-approval main
```

Interactive menu: 1 list worktrees, 2 status (uncommitted changes), 3 merge one, 4 remove one, 5 clean up all.

Pre-merge checklist:
1. `bash scripts/manage_worktrees.sh status`, working directory clean, everything committed.
2. Update the base branch (`git checkout main && git pull`).
3. Run validation in the worktree (`/validate-flow`, build, tests).

Merge order: infrastructure changes (connections, environment variables), then independent flows (any order), then dependent flows (dependency order). After each merge: export the solution, import to a test environment, validate, fix before the next merge.

Conflicts: review markers, understand both changes, resolve (connections: merge both sets; `solution.xml`: keep the newer version and merge component lists; flow definitions rarely conflict), test, then `git commit`.

### 4. Clean up

After a successful merge remove worktrees and delete branches:

```bash
bash scripts/manage_worktrees.sh remove ../my-repo-sharepoint-approval flow/sharepoint-approval
```

Or the interactive menu, option 4 or 5. Stale references: `git worktree prune`. Force removal (`git worktree remove <path> --force`) loses uncommitted changes: commit or stash first.

## Scripts

- `scripts/create_worktrees.py [flows...] [options]`: creates worktrees, branches, env copies and task files.
- `scripts/manage_worktrees.sh [list|status|merge|remove|cleanup]`: list, status, interactive merge, remove worktrees and delete branches, bulk cleanup.

## References

- `references/workflow-patterns.md`: independent, dependent and experimental flow patterns, full merge strategy, best practices, custom prefixes, multi-company workflows, shell helper, troubleshooting ("Branch already exists", "Directory already exists", "Uncommitted changes", merge conflicts), end-to-end 9-flow example.
- `references/worktree-guide.md`: git worktree command reference, Power Automate patterns, naming conventions, conflict strategies, performance, Claude Code integration.
