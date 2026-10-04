---
name: speckit-git-clean
description: Clean up the current feature worktree, branch, issue, and any uncommitted
  changes.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: git:commands/speckit.git.clean.md
---

# Clean Current Feature

Remove a feature worktree that is no longer needed. By default, the command resolves the feature from the current worktree's git branch, then discards uncommitted changes, removes the feature worktree, deletes the feature branch, and closes any linked GitHub issue.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Behavior

1. Parse arguments. Support `--force` / `-f`, `--worktree <path>`, `--spec <path>`, and `--issue <number>`. A single positional target is also allowed and may be a worktree path, a spec directory, or an issue number.
2. Resolve the cleanup target in this order:
   - an explicit `--worktree` path or worktree-like positional path
   - an explicit `--spec` path or `specs/<slug>` positional path
   - an explicit `--issue` number or `#<issue>` positional value
   - the current worktree (`git rev-parse --show-toplevel`)
3. Derive `feature_directory` and the feature branch from git in the target worktree, and read `source_issue` from its `.specify/feature.json` when present. The worktree path is never read from a file — doing so is how this command used to be pointed at the *previous* feature's worktree (issue #33).
4. If the target worktree has uncommitted changes:
   - abort with a file list unless `--force` was passed
   - when `--force` is passed, discard tracked and untracked changes before removal
5. Close the linked GitHub issue when `source_issue` is present and `gh` is available.
6. Remove the feature worktree with `git worktree remove` when the target is not the primary checkout.
7. Delete the feature branch with `git branch -D` after the worktree is removed.
8. Leave a short status summary describing what was cleaned and what was skipped.

## Execution

- **Bash**: `.specify/extensions/git/scripts/bash/clean.sh [--force|-f] [--worktree <path>] [--spec <path>] [--issue <number>] [target]`

## Graceful Degradation

- If Git is not available or the current directory is not a repository: warn and exit.
- If no `specs/<branch>` directory exists for the current branch and no explicit target is provided: refuse and explain how to point the command at a worktree, spec, or issue.
- If `gh` is missing or the issue cannot be resolved: the cleanup still proceeds and prints a notice.
- If the target is the primary checkout, the script will not remove that checkout in place; it will only clean the working tree and report the branch/worktree details so the user can rerun from a different checkout if needed.