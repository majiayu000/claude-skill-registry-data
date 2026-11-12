---
name: git-workflow
description: "Git 워크플로우 — 브랜치 네이밍, 커밋 가이드라인, PR 템플릿(Summary·Test Plan), 유용한 git 명령, 안티패턴. Use when 브랜치 전략을 정하거나 PR을 작성하고 git 협업 규칙을 정리할 때."
---

# Git Workflow Patterns

Git 워크플로우 패턴 및 best practices.

## Quick Reference

```
Git 워크플로우
    │
    ├─ 커밋 ─────────> <type>(<scope>): <subject>
    │
    ├─ 브랜치 ───────> feature/#123-description
    │
    ├─ PR 크기 ──────> 최대 400줄 (테스트 제외)
    │
    └─ 머지 방식 ────> Squash and Merge
```

---

## Commit Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| refactor | Code refactoring |
| test | Add/modify tests |
| docs | Documentation |
| chore | Build, config changes |
| style | Code style (formatting) |
| perf | Performance improvement |

### Examples

```bash
# Feature
feat(auth): add JWT token refresh

# Bug fix
fix(api): resolve null pointer in user handler

# Refactoring
refactor(service): extract validation logic

# Tests
test(user): add table-driven tests for GetByID
```

## Branch Naming

```
<type>/<issue-number>-<description>

# Examples
feature/#123-user-authentication
fix/#456-login-redirect
refactor/#789-api-handlers
docs/#101-api-documentation
```

## Commit Guidelines

### Single Logical Change

```bash
# Good - one logical change
git add internal/handler/user.go internal/service/user.go internal/handler/user_test.go
git commit -m "feat(user): add user creation endpoint"

# Bad - multiple unrelated changes
git add .
git commit -m "add user feature and fix login bug and update readme"
```

### Atomic Commits

```bash
# Feature implementation as single commit
# handler + service + repository + test = one commit

git add internal/handler/user.go
git add internal/service/user.go
git add internal/repository/user.go
git add internal/handler/user_test.go
git commit -m "feat(user): implement user CRUD operations"
```

## Pull Request

### Size Limit

- **Max 400 lines changed** (excluding tests)
- Large features: split into multiple PRs
- Each PR: one logical change

### PR Template

```markdown
## Summary
Brief description of changes (1-3 sentences)

## Changes
- Change 1
- Change 2
- Change 3

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues
Closes #123
```

### Issue Linking

```bash
# In commit message
feat(auth): add login endpoint (#123)

# In PR body
Closes #123
Fixes #456
Related to #789
```

## Workflow Steps

1. Create issue (if not exists)
2. Create branch from main: `feature/#123-description`
3. Make small, atomic commits
4. Push branch
5. Create PR with template
6. Request review
7. Address feedback
8. Squash and merge
9. Delete branch
10. Issue auto-closes

## Useful Commands

```bash
# Commit with conventional format
git commit -m "feat(scope): description"

# Amend last commit (unpushed only)
git commit --amend

# Interactive rebase (clean up commits)
git rebase -i HEAD~3

# Cherry-pick specific commit
git cherry-pick <commit-hash>

# Stash changes
git stash
git stash pop
```

## Anti-patterns

| Mistake | Correct | Why |
|---------|---------|-----|
| `git add .` blindly | Review changes first | Avoid unwanted files |
| Large PRs (1000+ lines) | Split into smaller PRs | Review quality |
| Vague commit messages | Descriptive messages | History clarity |
| Force push to shared branch | Only force push to own branch | Team coordination |
| No issue reference | Link to issue | Traceability |
| Merge commits | Squash or rebase | Clean history |
