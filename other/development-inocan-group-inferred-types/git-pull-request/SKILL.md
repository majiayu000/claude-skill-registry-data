---
name: git-pull-request
description: Use when creating pull requests. Covers PR structure, GitHub CLI usage, branch workflow, and pre-PR validation. Triggers on PR creation, branch merging, or when preparing changes for review.
---

# Git Pull Request

Create structured, reviewable pull requests. Use GitHub CLI for remote operations.

## Principles

**Pull Requests**
- **Complete before creating** - All tests pass, linting clean, code works as intended
- **Tell the story** - Why → What → How, in that order
- **Link to code** - Use GitHub permalinks to reference specific implementations
- **One concern per PR** - Avoid mixing unrelated changes; split if needed

**Workflow**
- **Check for related issues** - Link PRs to issues they address
- **Review your own diff first** - Read through changes before requesting review
- **Keep PRs reviewable** - Aim for <400 lines changed; split larger work

## Pull Request Format

### Title

Format: `[Scope] Short summary`

- **Scope**: Module, component, or area of the codebase (e.g., API, Auth, Database, UI, Docs)
- **Summary**: What changed, in imperative mood

Examples:
- `[API] Add v2 users endpoint`
- `[Auth] Fix nil pointer on login`
- `[Docs] Add setup instructions to README`
- `[Rate Limiting] Implement token bucket algorithm`
- `[Database] Add index for user email lookups`

### Body Template

```markdown
## What are you trying to accomplish?

Brief description of what changed and why, focusing on user or system impact.

Closes #123
Relates-to #456

## What approach did you use?

### [Category/Area 1]
- Summary of change ([`path/to/file.py#L10-L25`](permalink))
- Another change ([`path/to/other.py#L5`](permalink))

### [Category/Area 2]
- Summary of change ([`path/to/file.py#L50`](permalink))

## How did you validate the changes?

- [ ] Unit tests pass (`uv run pytest`)
- [ ] Linting passes (`uv run ruff check .`)
- [ ] Manual testing: [describe steps and results]
- [ ] Tested edge cases: [list any edge cases verified]
```

### PR Example

```markdown
## What are you trying to accomplish?

Add rate limiting to prevent API abuse. Users were able to make unlimited
requests, causing performance degradation during peak hours.

Closes #891

## What approach did you use?

### Rate Limiting Implementation
- Added token bucket rate limiter ([`app/middleware/rate_limit.py#L15-L45`](link))
- Configured per-endpoint limits ([`app/config.py#L23-L30`](link))

### API Changes
- Added `X-RateLimit-*` response headers ([`app/middleware/rate_limit.py#L50-L60`](link))
- Return 429 with retry-after on limit exceeded ([`app/middleware/rate_limit.py#L65`](link))

### Tests
- Unit tests for token bucket algorithm ([`tests/test_rate_limit.py`](link))
- Integration tests for endpoint limits ([`tests/integration/test_api_limits.py`](link))

## How did you validate the changes?

- [x] Unit tests pass (added 12 new tests)
- [x] Load tested with 1000 req/s, limits enforced correctly
- [x] Verified headers appear in responses
- [x] Confirmed 429 response includes valid Retry-After
```

Title for this PR: `[Rate Limiting] Add token bucket rate limiter to API`

## GitHub CLI Commands

### Pull Requests

```bash
# Create PR (opens editor for body)
gh pr create --title "[API] Add rate limiting"

# Create PR with body
gh pr create --title "[Auth] Fix session timeout" --body "Closes #234"

# Create draft PR
gh pr create --draft --title "[WIP] New feature"

# Push and create PR in one step
git push -u origin feature-branch && gh pr create

# View PR status
gh pr status

# View specific PR
gh pr view 456

# Check PR checks/CI status
gh pr checks
```

### Branch Operations

```bash
# Create branch linked to issue
gh issue develop 123 --name "fix-login-bug"

# Check out PR locally
gh pr checkout 456

# Merge PR
gh pr merge 456 --squash --delete-branch
```

## Pre-PR Checklist

Before creating a pull request:

```bash
# 1. Ensure all changes committed
git status

# 2. Pull latest from base branch
git fetch origin main
git rebase origin/main  # or merge

# 3. Run tests
uv run pytest

# 4. Run linting
uv run ruff check .
uv run ruff format --check .

# 5. Review your own changes
git diff origin/main...HEAD

# 6. Check for related issues
gh issue list --search "relevant keywords"

# 7. Push and create PR
git push -u origin HEAD
gh pr create
```
