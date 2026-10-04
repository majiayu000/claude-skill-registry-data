---
name: git-workflow
description: >-
  Git workflow and commit conventions. Branching strategy, Conventional
  Commits, PR workflow. Use when: Phase 3 finalization, commit, PR preparation.
  Not for: basic git commands.
---

# Git Workflow

## Overview

Standardized Git workflow for efficient collaboration.

## Branching Strategy

```
main ─────────────────────────────────────────►
        │                           │
develop ├───────────────────────────┼─────────►
        │           │               │
feature/x ──────────┘               │
                                    │
feature/y ──────────────────────────┘
```

### Branch Types

| Type | Convention | Base | Merge to |
|------|------------|------|----------|
| main | `main` | - | - |
| develop | `develop` | main | main |
| feature | `feature/short-name` | develop | develop |
| bugfix | `bugfix/short-name` | develop | develop |
| hotfix | `hotfix/short-name` | main | main + develop |
| release | `release/vX.Y.Z` | develop | main + develop |

### Branch Naming

```
feature/add-user-authentication
bugfix/fix-login-redirect
hotfix/security-patch-xss
release/v2.1.0
```

## Conventional Commits

### Format

```
<type>(<scope>): <description>

[body]

[footer]
```

### Types

| Type | Usage | Example |
|------|-------|---------|
| `feat` | New feature | `feat(auth): add JWT refresh` |
| `fix` | Bug fix | `fix(api): handle null response` |
| `docs` | Documentation | `docs(readme): add install guide` |
| `style` | Formatting (no code) | `style: fix indentation` |
| `refactor` | Refactoring | `refactor(user): extract validator` |
| `test` | Tests | `test(auth): add login tests` |
| `chore` | Maintenance | `chore(deps): update lodash` |
| `perf` | Performance | `perf(query): optimize user fetch` |
| `ci` | CI/CD | `ci: add github actions` |

### Rules

1. **Type required** — Always start with type
2. **Scope optional** — Context in parentheses
3. **Imperative description** — "add" not "added"
4. **Line < 72 chars** — For readability
5. **Body optional** — Details if needed
6. **Footer for refs** — `Closes #123`, `BREAKING CHANGE:`

### Examples

```
feat(auth): add JWT token refresh

- Implement token refresh endpoint
- Add refresh token to login response
- Update auth middleware

Closes #123
```

```
fix(api): handle null response from external service

The external API sometimes returns null instead of an empty
array. This caused a TypeError in the mapping function.

Fixes #456
```

```
feat(user)!: change email validation rules

BREAKING CHANGE: Email addresses must now include a TLD.
Previously accepted emails like "user@localhost" are no longer valid.
```

## PR Workflow

### Before Creating PR

- [ ] Rebase on recent develop
- [ ] All tests pass
- [ ] Lint clean (no errors)
- [ ] Commits squashed if needed
- [ ] Feature Document updated (STANDARD/LARGE)

### PR Template

```markdown
## Description
[Summary of changes in 2-3 sentences]

## Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Refactoring (no functional change)

## Tests
- [ ] Unit tests added/modified
- [ ] Integration tests added/modified
- [ ] Manual tests performed

## Checklist
- [ ] Code self-reviewed
- [ ] Documentation updated
- [ ] No console.log/var_dump
- [ ] Feature Document completed (if applicable)

## Screenshots (if UI)
[Before/After if applicable]

## Links
- Feature Document: docs/features/xxx.md
- Issue: #123
```

### Review Workflow

```
1. Create PR → Draft if WIP
2. Auto-assign reviewers
3. CI/CD checks pass
4. Peer review
5. Resolve comments
6. Approval (min 1)
7. Squash & Merge
```

## Useful Commands

### Daily Workflow

```bash
# New feature
git checkout develop
git pull
git checkout -b feature/my-feature

# Commit
git add .
git commit -m "feat(scope): description"

# Push and PR
git push -u origin feature/my-feature
```

### Maintenance

```bash
# Rebase on develop
git fetch origin
git rebase origin/develop

# Squash commits
git rebase -i HEAD~3

# Amend last commit
git commit --amend
```

## Recommended Git Hooks

| Hook | Action |
|------|--------|
| pre-commit | Lint, format |
| commit-msg | Validate Conventional Commit |
| pre-push | Unit tests |

## EPCI Phase 3 Checklist

- [ ] Commits follow Conventional Commits
- [ ] Branch named correctly
- [ ] Rebase on recent develop
- [ ] PR template completed
- [ ] Feature Document finalized
- [ ] CI/CD passes
