---
name: pull-request-conventions
description: Use when creating or merging pull requests - provides branch naming, PR title format, and description requirements for consistent PR workflows
---

# Pull Request Conventions

## Branch Naming Convention

**Format:** `<type>/<issue-number>-<description>` or `<type>/<description>`

**Types** (must match conventional commit types):

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `chore` - Maintenance tasks
- `refactor` - Code restructuring
- `test` - Adding or updating tests
- `build` - Build system changes
- `ci` - CI configuration
- `perf` - Performance improvements
- `style` - Code style changes (formatting, etc.)

**Examples:**

- `feat/123-user-auth`
- `fix/login-error`
- `docs/api-guide`
- `refactor/simplify-validation`

## PR Title Convention

PR titles must follow Conventional Commits format.

**Format:** `<type>[optional scope]: <description>`

**Why:** PR title becomes the squash merge commit message on main.

**Examples:**

- `feat(auth): add JWT validation`
- `fix: resolve login error`
- `docs(api): update endpoint documentation`

## Deriving PR Title

**Primary source: commits.**
The PR title should reflect what the changes actually accomplish, not just the branch name.

**Process:**

1. Review commit history to understand the changes
2. Identify the primary type (`feat`, `fix`, `refactor`, etc.)
3. Summarize the changes concisely
4. Add scope if clearly scoped to a specific area

**Branch name as fallback:**
If starting from branch name (e.g., when branch already exists), use it as a hint:

1. Extract type from prefix: `feat/...` → `feat`
2. Remove issue number if present: `feat/123-user-auth` → `user auth`
3. Convert hyphens to spaces

**Scope is optional** - add when the change is clearly scoped to a specific area:

- `feat/auth-jwt-validation` → `feat(auth): jwt validation`
- `fix/login-error` → `fix: login error` (no obvious scope)

**Important:** The branch name may diverge from actual changes during development.
Always verify the title accurately reflects what the PR contains.

## PR Description Requirements

**Foundational principle: Description must be 100% accurate.**

### Required Sections

```markdown
## Summary

<1-3 bullet points describing what changed and why>

## Test plan

<How to verify the changes work>
```

### Accuracy Rules

The description must reflect the **final state** of changes, not the journey:

- If code was added then removed: don't mention it
- If approach changed mid-development: describe final approach only
- If features were split to other PRs: don't reference them

### Common Red Flags

When reviewing PR descriptions, watch for:

- Mentions features that were removed
- Describes approach that was changed
- References safeguards that were removed
- Contains code examples that don't match final implementation
