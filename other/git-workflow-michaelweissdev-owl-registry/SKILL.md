---
name: git-workflow
description: >
  Inspect repository status, inspect diffs, stage focused changes, create
  well-scoped commits, and coordinate with remotes safely. Use when preparing
  code changes for commit, reviewing unstaged modifications, managing Git staging,
  resolving repository dirty state, or synchronizing with remote branches.
compatibility: >
  Agent Skills-compatible coding agents with access to a Git repository
  in the local workspace.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "git, version-control, diff, staging, commits"
  topics: "version-control, devtools"
---

# Git Workflow

A disciplined, non-destructive Git workflow ensures atomic changes, readable history, and safe collaboration. AI agents must operate predictably by prioritizing read-only inspection, respecting user work-in-progress, and never running destructive commands without authorization.

## Core Rules

1. **Inspect before acting**: Always check `git status --short` and `git diff` before modifying the staging area or index.
2. **Never blindly stage all files**: Never execute `git add .` or `git add -A` unless every changed file has been verified as belonging to the task.
3. **Keep commits atomic**: One commit should represent one logical change with its accompanying tests and documentation.
4. **Distinguish read from write**: Commands like `git status`, `git diff`, and `git log` are read-only and safe. Commands like `git commit`, `git checkout`, `git reset`, and `git push` modify state and require intent.
5. **Never discard work without authorization**: Commands that delete uncommitted code (`git checkout -- .`, `git restore .`, `git reset --hard`, `git clean -fd`) can permanently destroy work. Never run them without explicit confirmation.
6. **Treat remotes with care**: Never force push (`--force` or `-f`) to shared branches. Never push without user direction.

---

## 1. Inspection and Diagnosis (Read-Only)

Before any file modifications or staging operations, determine current working tree state:

```bash
# High-level overview: branch, tracking status, staged and unstaged files
git status --short --branch

# Inspect unstaged modifications
git diff --stat
git diff

# Inspect staged modifications
git diff --cached --stat
git diff --cached

# Check recent commit history to match repository style
git log -5 --oneline --decorate
```

Interpret short status flags:
- ` M` (space, M): Unstaged modification in tracked file.
- `M ` (M, space): Staged modification ready for commit.
- `MM`: File has both staged changes and subsequent unstaged changes.
- `??`: Untracked file (check whether it belongs in `.gitignore`).
- `UU`: Unresolved merge conflict.

---

## 2. Staging Boundaries and Hygiene

Staging prepares the exact snapshot that will become the next commit.

### Focused Staging
Stage only files that belong to the current logical change:

```bash
# Stage specific files
git add src/core/parser.py tests/test_parser.py

# Verify staged snapshot against unstaged working tree
git status --short
git diff --cached --stat
```

### Partial Staging (Hunks)
When a file contains unrelated changes (e.g., experimental debug logging alongside a bug fix), use hunk staging:

```bash
# Interactively review and stage individual diff hunks
git add -p src/core/parser.py
```

### Unstaging Without Data Loss
If a file was staged by mistake, unstage it without altering file contents:

```bash
# Unstage a file (preserves working tree changes)
git restore --staged <path>
# Or in older Git:
git reset HEAD <path>
```

---

## 3. Creating Commits

1. Confirm the staged diff matches the intended change:
   ```bash
   git diff --cached
   ```
2. Check that no stray secrets, temporary files, or unrelated formatting changes are staged.
3. Commit with a clear, standard-compliant message (following Conventional Commits):
   ```bash
   git commit -m "fix(parser): handle empty input stream without throwing EOFError"
   ```
4. Verify the new commit on top of HEAD:
   ```bash
   git log -1 --stat
   ```

---

## 4. Remote Synchronization

### Fetching and Checking Divergence
Always fetch to update remote-tracking branches before pulling or pushing:

```bash
git fetch origin

# Check how many commits HEAD is ahead or behind origin/main
git rev-list --left-right --count HEAD...origin/main
```
Output `2  0` means local is 2 commits ahead (ready to push).
Output `0  3` means local is 3 commits behind (needs fast-forward or rebase).
Output `2  3` means branches have diverged.

### Pulling Safely
Avoid unintended merge commits during regular feature development:

```bash
# Rebase local commits onto updated upstream branch
git pull --rebase origin <branch-name>

# Fast-forward only (fails if branches have diverged)
git pull --ff-only origin <branch-name>
```

### Pushing
Only push to feature branches when instructed:

```bash
git push -u origin feature/my-feature
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `git add .` | Stages temporary files, `.env` secrets, or unrelated edits | Explicitly stage targeted files: `git add <files>` |
| `git checkout -- <file>` | Permanently deletes uncommitted work | Review file diff first; ask confirmation before discard |
| `git commit -am "fix"` | Combines staging and committing, bypassing diff review | Separate `git add <file>`, verify `git diff --cached`, then commit |
| `git push --force` | Overwrites team members' work on remote branch | Use `--force-with-lease` only on private feature branches if required |
| Committing `.env` / credentials | Security breach | Verify `.gitignore` before staging untracked configuration files |

---

## 6. Real-World Scenarios

### Scenario A: Committing a Targeted Bugfix Amongst Unrelated Work
You edited `src/auth.py` (bug fix), `src/ui.py` (incomplete UI experimentation), and created `debug.log`.

```bash
# 1. Inspect status
git status --short
# Output:
#  M src/auth.py
#  M src/ui.py
# ?? debug.log

# 2. Add debug.log to .gitignore if applicable, or remove it
echo "debug.log" >> .gitignore

# 3. Stage only the bug fix and tests
git add src/auth.py tests/test_auth.py

# 4. Verify only auth changes are staged
git diff --cached --stat

# 5. Commit with precise message
git commit -m "fix(auth): prevent session timeout during active token refresh"

# 6. Verify result
git status --short
# src/ui.py remains safely in working tree as unstaged work
```

### Scenario B: Synchronizing Local Feature Branch with Updated Main

```bash
# 1. Ensure working tree is clean or stashed
git status --short

# 2. Fetch latest changes from remote
git fetch origin

# 3. Rebase feature branch on top of updated upstream main
git rebase origin/main

# 4. If clean: verify log
git log -3 --oneline

# 5. Run tests to confirm integration
pytest
```

---

## 7. Validation Checklist

- [ ] `git status --short` shows only intended changes are staged.
- [ ] `git diff --cached` contains no unintended changes, keys, or debug statements.
- [ ] `git log -1` verifies the commit author, message, and committed files.
- [ ] Working tree status is clean or matches expected remaining tasks.
