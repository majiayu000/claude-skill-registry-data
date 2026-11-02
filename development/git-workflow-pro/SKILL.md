---
name: git-workflow-pro
description: Advanced Git operations, conventional commits, interactive rebase, bisect, worktrees, and release branch management. Use when restructuring messy commit history, performing interactive rebases, resolving complex merge conflicts, finding regressions with git bisect, or managing worktrees.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0
category: git-version-control
---

# Git Workflow Pro

> **Advanced History Hygiene, Interactive Rebasing, Git Bisect & Worktree Mastery**

---

## 🏗️ Core Principles

| Principle | Rule |
|-----------|------|
| **Atomic Commits** | Every commit represents ONE logical change. A commit must build and pass tests in isolation. |
| **Conventional Commits** | Format: `<type>(<scope>): <subject>`. Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `chore`, `revert`. Breaking: `feat!: ...` |
| **Clean Rebase > Messy Merges** | Rebase feature branches against `main` before submitting PRs. Keep linear git history free of duplicate merge bubbles. |
| **Bisect for Heisenbugs** | Use binary search (`git bisect`) with automated test scripts to locate regression commits instantly. |
| **Never Force Push to Shared Branches** | Use `--force-with-lease` on private feature branches only. Never overwrite `main` or release branches. |

---

## 📋 Advanced Git Commands Quick Reference

### 1. Interactive Rebase (`git rebase -i HEAD~N`)
```text
pick e4a123f feat(auth): add jwt token generator
squash 8b3c456 fix typo in jwt payload
reword 9d1f789 refactor: extract signing key to env
drop a1b2c3d remove debug console.log
```

### 2. Finding Regressions with `git bisect`
```bash
git bisect start
git bisect bad                 # Current commit is broken
git bisect good v2.1.0         # v2.1.0 was known good
git bisect run npm test        # Git automatically tests every commit and finds culprit
git bisect reset               # Return to HEAD after culprit found
```

### 3. Isolated Parallel Work with Git Worktrees
```bash
# Work on critical hotfix without stashing or switching current branch
git worktree add ../hotfix-branch -b hotfix/payment-crash
cd ../hotfix-branch
# Fix and commit
cd ../main-repo
git worktree remove ../hotfix-branch
```

---

## ❌ Anti-Patterns

- ❌ Commits with messages like `wip`, `fixed stuff`, `changes`, or `update`.
- ❌ Committing unrelated formatting fixes mixed with business logic changes.
- ❌ Blindly running `git add .` without reviewing unstaged changes with `git diff`.
