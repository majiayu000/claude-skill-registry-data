---
name: "version-control"
description: 'Apply effective Git workflows including commit conventions, branching strategies, and pull request best practices. Use when writing commit messages, choosing branching strategies, configuring git hooks, resolving merge conflicts, or implementing semantic versioning.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Version Control

> **Purpose**: Effective use of Git for collaboration and code management.

---

## When to Use This Skill

- Writing Git commit messages following conventions
- Choosing a branching strategy
- Configuring Git hooks for quality gates
- Resolving merge conflicts
- Implementing semantic versioning with Git tags

## Prerequisites

- Git 2.30+ installed
- Text editor configured for Git

## Decision Tree

```
Git operation?
+- Starting new work?
| +- Feature -> branch from main: feature/issue-123-description
| +- Bug fix -> branch from main: fix/issue-456-description
| - Hotfix -> branch from release: hotfix/critical-issue
+- Committing?
| +- Small, atomic changes (one logical change per commit)
| - Format: type(scope): description (#issue)
+- Merging?
| +- Feature branch -> squash merge to main
| +- Release branch -> merge commit (preserve history)
| - Conflict? -> Rebase feature on main, resolve, re-push
- Undoing?
 +- Uncommitted changes? -> git stash or git checkout
 +- Last commit (not pushed)? -> git reset --soft HEAD~1
 - Pushed commit? -> git revert (never force-push shared branches)
```

## Commit Messages

```bash
# Format
type(scope): Brief description (50 chars max)

Detailed explanation (wrap at 72 characters)

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance
- perf: Performance improvement
- ci: CI/CD changes
- build: Build system changes

# Examples
feat(auth): Add password reset functionality

Implements password reset via email with time-limited tokens.
Tokens expire after 1 hour.

Fixes #234

---

fix(api): Correct null reference in UserService

Added null check before accessing user properties in
GetUserProfileAsync method.

Resolves #456
```

---

## Git Workflow

```bash
# Feature branch
git checkout main
git pull origin main
git checkout -b feature/user-auth

# Make changes
git add .
git commit -m "feat(auth): Add login endpoint"

# Push and create PR
git push origin feature/user-auth

# After PR review, rebase if needed
git fetch origin
git rebase origin/main

# Squash commits before merging (optional)
git rebase -i HEAD~3

# Force push after rebase
git push origin feature/user-auth --force-with-lease
```

---

## Branching Strategy

### GitFlow

```bash
# Main branches
- main/master: Production-ready code
- develop: Integration branch

# Supporting branches
- feature/*: New features
- bugfix/*: Bug fixes
- hotfix/*: Emergency production fixes
- release/*: Release preparation

# Example workflow
git checkout develop
git pull origin develop
git checkout -b feature/add-payment

# ... make changes ...
git push origin feature/add-payment
# Create PR to develop

# Release
git checkout -b release/v1.2.0 develop
# ... version bump, final testing ...
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags
```

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`setup-hooks.ps1`](scripts/setup-hooks.ps1) | Install Git hooks (pre-commit, commit-msg) for quality enforcement | `./scripts/setup-hooks.ps1 [-Mode native]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Merge conflict in binary files | Use Git LFS for binaries, prefer text-based formats where possible |
| Git hook not running | Check executable permissions (chmod +x), verify .git/hooks/ path |
| Detached HEAD state | Create a branch from current state: git checkout -b recovery-branch |

## References

- [Git Config Hooks Versioning](references/git-config-hooks-versioning.md)