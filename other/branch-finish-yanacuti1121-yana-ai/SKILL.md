---
name: branch-finish
description: "Use when a development task is complete and ready to merge or close — before running git merge, git push, or closing a branch. Triggers on: 'I'm done', 'ready to merge', 'merge this', 'finish the branch', 'close the task'."
---

# Branch Finish Checklist Skill

Before merging or closing a branch, verify the work is actually done and the branch
is clean. This prevents partial merges and repo pollution.

## When to use this skill

- About to run `git merge`, `git push`, or close a worktree
- User says "merge this", "I'm done", "wrap it up"
- Task is marked complete in TODO.md

## The Checklist

Run each step and show output. Do not skip.

### 1 — Tests pass

```bash
bash core/tests/hooks/run-hook-tests.sh 2>&1 | tail -5
```

Required: `0 failed`. If tests fail → stop. Do not merge.

### 2 — No rogue files

```bash
git status --short
```

Check for:
- Untracked files that should not exist (`.env*`, `*.log`, `node_modules/`)
- Modified files outside the task scope

If anything unexpected appears → investigate before merging.

### 3 — Diff is clean

```bash
git diff main...HEAD --stat
```

Show the list of changed files. Confirm with user: "These N files will be merged. Correct?"

### 4 — No debug artifacts

```bash
git diff main...HEAD | grep -n "console\.log\|debugger\|TODO REMOVE\|HACK\|XXX" || echo "none found"
```

If anything found: list it. User decides whether to clean up.

### 5 — Commit messages are conventional

```bash
git log main..HEAD --oneline
```

Each commit message should follow `type: subject` (feat, fix, chore, docs, refactor).
If not: warn but do not block.

### 6 — Present options

After checklist passes:

```
Branch finish checklist: PASS

What next?
1. Merge locally (git merge into main)
2. Push and open PR
3. Keep branch open (not done yet)
4. Discard branch (confirm required)

Choose 1-4:
```

Wait for user choice before doing anything.

### Option 1: Merge locally
```bash
git checkout main
git merge <branch-name>
git branch -d <branch-name>
```

### Option 2: Push + PR
```bash
git push -u origin <branch-name>
# Then create PR via gh or GitLab CLI if available
```

### Option 3: Keep open
Report: "Branch kept open. Resume with /resume when ready."

### Option 4: Discard
Require typed "discard" confirmation before running:
```bash
git checkout main
git branch -D <branch-name>
```

## Constraints

- Never merge with failing tests.
- Never force-push without explicit user request.
- Always show the file list before merging — no silent merges.
- For Option 4, require typed confirmation. No "yes/y" shortcuts.
