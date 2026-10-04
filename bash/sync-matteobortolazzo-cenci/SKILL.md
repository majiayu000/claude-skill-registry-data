---
name: sync
description: "Sync main, rebase active worktrees, and clean up merged branches safely."
compatibility: Requires Claude Code skill arguments and model-selection extensions.
argument-hint: [additional context]
user-invocable: true
disable-model-invocation: true
model: haiku
allowed-tools: Read, AskUserQuestion, Bash(git status:*), Bash(git stash:*), Bash(git add:*), Bash(git commit:*), Bash(git fetch:*), Bash(git checkout:*), Bash(git pull --ff-only:*), Bash(git branch -v:*), Bash(git branch -D:*), Bash(git worktree list:*), Bash(git worktree prune:*), Bash(git worktree remove:*), Bash(git -C:*)
---

> **Client dispatch**: In Codex, read `codex-runtime` and `sync/codex.md`, execute that native procedure, and do not continue into the Claude procedure below.

> **Interaction rule**: Every question, confirmation, or approval directed at the user — anywhere in this skill, including error recovery — MUST be asked with the `AskUserQuestion` tool. Never ask in plain text. If an instruction says "ask the user" or "confirm", that means `AskUserQuestion`.

## Task

Sync the local repository: pull latest main, rebase active worktrees onto updated main, prune stale remote references, and clean up local branches and worktrees left over from merged PRs.

### Parse `$ARGUMENTS`

All of `$ARGUMENTS` is optional **user context** (additional instructions or focus areas).
If empty, proceed normally with full sync.

## Process

If user context was provided, use it to steer the sync (e.g., skip certain steps, focus on specific cleanup).

### Step 1: Check for uncommitted work

```bash
git status --short
```

If the current branch has uncommitted changes, use `AskUserQuestion` to ask how to proceed, with options:
- **Stash** — `git stash -u` the changes, then continue
- **Commit** — commit the changes on the current branch, then continue
- **Abort** — stop the sync entirely, leaving the changes untouched

### Step 2: Update main

Fetch all remotes and prune deleted remote branches, as its own Bash call:
```bash
git fetch --all --prune
```

Switch to `main` as its own standalone call:
```bash
git checkout main
```
If that call fails (no `main` branch in this repo), switch to `master` instead, as a
second standalone call — never compound the two with `||` (shell-rules: every segment
of a compound is evaluated independently by the approval system):
```bash
git checkout master
```

Fast-forward to latest, as its own Bash call:
```bash
git pull --ff-only
```

If `pull --ff-only` fails (local main has diverged), **stop and warn the user** — do not force-reset.

### Step 3: Rebase active worktrees

For each non-main worktree (skip any marked `[gone]` in `git branch -v`):

1. **Check for detached HEAD** — skip if detached:
   ```bash
   git -C <worktree-path> symbolic-ref --short HEAD
   ```
   If this fails, the worktree is in detached HEAD state — skip it.

2. **Check for uncommitted changes** — skip if dirty:
   ```bash
   git -C <worktree-path> status --porcelain
   ```
   If output is non-empty, skip this worktree (uncommitted changes would conflict with rebase).

3. **Rebase onto main**:
   ```bash
   git -C <worktree-path> rebase main
   ```

4. **If rebase fails** (conflicts): abort and note the failure, then continue to the next worktree:
   ```bash
   git -C <worktree-path> rebase --abort
   ```

Track results for the report: which worktrees were rebased, skipped (dirty/detached), or had conflicts.

### Step 4: Prune stale worktrees

```bash
git worktree prune
```

This removes worktree entries whose directories no longer exist on disk.

### Step 5: Clean up gone branches

List branches whose remote tracking branch has been deleted (marked `[gone]`):

```bash
git branch -v
```

Run `git worktree list` once as its own Bash call and keep its output in context:

```bash
git worktree list
```

For each branch marked `[gone]`:
1. Match the branch name against that captured output in reasoning (no further shell
   call needed — this is a text comparison over output already in context, not a new
   command).
2. If a worktree exists and is **not** the main worktree, remove it:
   ```bash
   git worktree remove <worktree-path>
   ```
3. Delete the local branch:
   ```bash
   git branch -D "$branch"
   ```

### Step 6: Report

Summarize what was done:
- Current main commit (short hash + subject)
- Rebase results: which worktrees were rebased successfully, which were skipped (dirty/detached), which had conflicts
- Number of branches cleaned up (list them)
- Number of worktrees removed (list paths)
- Any remaining worktrees (`git worktree list`)

If nothing needed cleaning or rebasing, say so.
