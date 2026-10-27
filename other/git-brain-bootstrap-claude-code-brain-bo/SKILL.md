---
name: git
description: Git workflow helpers — status, rebase, commit, amend, log, stash, branch management. Includes pre-push checklist. NEVER git push autonomously.
---

# Git Skill

Git workflow helpers for everyday operations.

## Usage

```
/git status          # Current branch + dirty files + recent commits
/git branch          # List branches
/git rebase main     # Rebase onto main
/git commit <msg>    # Stage all + commit
/git amend           # Stage all + amend last commit
/git log             # Last 20 commits
/git stash           # Stash changes
/git stash pop       # Pop stash
/git conflicts       # Find conflict markers
```

## ⚠️ NEVER `git push` Autonomously

Always present the proposed command and wait for user confirmation:
```
Proposed: git push origin feature/my-branch
⏳ Waiting for your confirmation before pushing...
```

## Instructions

### Determine action from $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `status` | `git status --short` + `git --no-pager log --oneline -5` |
| `branch` | `git branch --show-current` |
| `branches` | `git --no-pager branch -a \| head -30` |
| `stash` | `git stash` |
| `stash pop` | `git stash pop` |
| `rebase main` | `git fetch origin main && git rebase origin/main` |
| `commit <message>` | `git add -A && git commit -m "<message>"` |
| `amend` | `git add -A && git commit --amend --no-edit` |
| `log` | `git --no-pager log --oneline -20` |
| `conflicts` | `grep -rn '^<<<<<<<\|^=======\|^>>>>>>>' . 2>/dev/null \| head -20` |

### Branch Naming Convention:
- Feature: `feat/<ticket-id>-<short-description>`
- Fix: `fix/<ticket-id>-<short-description>`
- Chore: `chore/<description>`

### Pre-Push Checklist (present to user before any push):
1. ✅ Build passes
2. ✅ Tests pass
3. ✅ Lint clean on changed files
4. ✅ No conflict markers in repo
5. ✅ Diff review complete (merge-base aware)
6. 📋 Proposed: `git push origin <branch>`
7. ⏳ Waiting for user confirmation...
