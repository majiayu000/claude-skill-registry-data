---
name: git-workflow-conventional-commits
description: Enforces standardized git workflow — conventional commits, atomic commits (one concern per), branch naming, PR standards, and commit message formatting. Prevents inconsistent history and unreadable git log.
---

# Git Workflow & Conventional Commits

## Problem it solves

Without a standardized git workflow, commits are inconsistent and history is unreadable:
- Vague commit messages ("fix stuff", "changes", "updated")
- Commits mixing multiple unrelated changes
- No correlation between commits and issues/PRs
- Branch names that don't describe the work
- Hard to generate changelogs or release notes
- Difficult to find which change introduced a bug

## Protocol

### 1. Conventional commit format

Every commit message must follow:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types** (pick one):
- `feat` — A new feature
- `fix` — A bug fix
- `refactor` — Code change that neither fixes nor adds
- `docs` — Documentation only
- `test` — Adding or fixing tests
- `chore` — Build, deps, tooling, CI
- `perf` — Performance improvement
- `style` — Formatting, whitespace (no code change)
- `ci` — CI pipeline changes

**Scope**: Optional, but use it for the module/area (e.g., `feat(auth):`, `fix(api):`)

**Description**: Imperative present tense, lowercase, no period at end. Max 72 chars.

```
feat(auth): add OAuth2 login flow
fix(api): handle empty response from upstream service
refactor: extract validation logic into shared module
```

### 2. Atomic commits

One concern per commit:
- A commit should contain exactly one logical change
- If a change touches two concerns (e.g., refactor + feature), split into two commits
- If you're describing the commit with "and" or "also", split it

Examples:
- ❌ `feat: add user profile and fix login bug` — split into two
- ✅ `feat: add user profile` + `fix: correct login redirect`

### 3. Branch naming

Use descriptive branch names with a consistent format:

```
<type>/<description>
```

Examples:
- `feat/oauth2-login`
- `fix/empty-response-handling`
- `refactor/extract-validation`

Separate words with hyphens. Keep names under 50 chars.

### 4. Pull request standards

When creating a PR:
- Title follows conventional commit format
- Description includes: what, why, how to test, related issues
- Link to any relevant spec or design doc
- Mark breaking changes clearly with `BREAKING CHANGE:` footer

### 5. Before committing

Review the diff — is this a single atomic change?
Write the commit message first (it forces you to think about intent)

## Detection triggers

Activate when:
- About to run `git add` or `git commit`
- Creating a branch
- Opening a PR
- Writing a commit message
- User says "commit this", "push", "create PR"

## When NOT to use

- WIP/save-point commits in a private branch
- Squash-and-merge where only the PR title matters
- User explicitly says "just commit, no convention needed"

## Cross-references

- **yeet** — Use yeet for fast push/PR creation; this skill ensures the commits yeet pushes follow quality conventions.

- **release-changelog** — Conventional commits feed directly into changelog generation. Consistent types make release notes automatic.

- **code-review** — Review should verify commit messages follow conventions and commits are atomic.

- **spec-driven-development** — The spec scope determines what goes into each atomic commit.

- **test-driven-development** — Each commit should include tests for its change.

- **anti-premature-termination** — Do not declare a merge done until commits are squashed/conventional and PR standards are met.
- **incremental-implementation** — Use incremental slices to produce atomic commits. Each slice maps to one or more conventional commits.
