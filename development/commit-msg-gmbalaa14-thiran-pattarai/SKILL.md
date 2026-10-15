---
name: commit-msg
description: Generate conventional commit messages and pull request documentation from git staged changes. Use this when you need to create commit messages following the Conventional Commits spec (feat, fix, docs, etc.), craft PR titles and descriptions that summarize multiple commits, or automatically infer related issues and breaking changes from your code changes. Invoke this whenever you're about to commit code and want a well-structured, standards-compliant message, or when preparing a pull request that needs a professional title and detailed context.
compatibility: Requires git repository with staged changes
disable-model-invocation: false
license: "MIT"
metadata:
  author: "Balagurunathan Marimuthu"
  version: "1.0.0"
---

# Commit Message Generator

Generate professional commit messages and PR documentation automatically from your git staged changes, following the Conventional Commits specification.

## What This Skill Does

This skill analyzes your staged git changes and generates:
- **Commit messages** with conventional format: `type(scope): subject. Details.`
- **PR titles** (max 100 chars) that capture the most important change
- **PR descriptions** with context in bullet points (max 100 chars each) and related issue references

## Usage

### For Commit Messages

**Within Claude Code:**
```
/commit-msg
Analyze my staged changes and suggest a commit message
```

Or describe what you're committing:
```
/commit-msg
I've added JWT authentication to the login endpoint and updated the auth middleware to validate tokens. Also fixed a bug where expired tokens weren't being refreshed properly.
```

**What you'll get:**
- Suggested type (feat, fix, docs, refactor, etc.) based on the changes
- Scope (derived from affected files/modules)
- Imperative subject line with ending period
- Detection of breaking changes (marked with `!` in the message)
- Body text explaining the "why" and impact

### For Pull Requests

When you have multiple commits ready for a PR:
```
/commit-msg
Generate a pull request message for my staged commits
```

**What you'll get:**
- **PR Title**: The most important commit's subject, max 100 chars
- **PR Description**: 
  - Broader context of all changes in bullet points (max 100 chars each)
  - Related issues (Fixes #123, Closes #456)
  - Any breaking changes highlighted
  - Code blocks with backticks for examples or important context

## How It Works

1. **Analyzes staged git changes** — reads the diff to understand what's being modified
2. **Determines commit type** — feat (new feature), fix (bug fix), docs, style, refactor, perf, test, chore, ci, or revert
3. **Infers scope** — based on changed files and modules
4. **Detects breaking changes** — looks for API changes, removed functionality, or significant modifications
5. **Generates message** — follows conventional commits format with imperative mood and proper structure
6. **For PRs** — synthesizes multiple commits into a coherent PR title and description

## Conventional Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring without feature changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Build, dependencies, tooling updates
- **ci**: CI/CD configuration changes
- **revert**: Reverting a previous commit

## Breaking Changes

The skill automatically detects breaking changes and marks them with `!`:
```
feat(auth)!: Remove support for legacy tokens.
```

This indicates downstream consumers need to update their code.

## Examples

**Commit message for a feature:**
```
feat(auth): Add JWT token refresh mechanism.

Implements automatic token refresh when tokens are near expiration. This improves user experience by preventing unexpected logouts during active sessions.

Breaking change: Legacy session tokens are no longer supported.
```

**PR description from multiple commits:**
```
Title: Add JWT authentication to login flow (98 chars)

## Overview
- Implemented JWT-based authentication system with automatic token refresh
- Updated middleware to validate all protected endpoints
- Fixed token expiration handling and added proper error responses
- Added comprehensive test coverage for auth flows

Fixes #234, #238
```

## Instructions for Generating Messages

When the user asks for a commit message or PR documentation, follow these steps:

### For Commit Messages

1. **Analyze the changes** — Look at the code changes described or staged in git
2. **Determine the type** — Choose from: feat, fix, docs, style, refactor, perf, test, chore, ci, revert
3. **Find the scope** — Extract from affected modules/files (e.g., "auth", "api", "utils")
4. **Detect breaking changes** — Look for: removed APIs, changed function signatures, database migrations, configuration changes. If found, mark with `!` after type: `feat(auth)!:`
5. **Write the subject** — Use imperative mood, start with lowercase, end with a period. Max ~50 chars.
6. **Add the body** — Explain the "why" and impact (2-3 sentences). Max ~100 chars per line.
7. **Humanize the message** — Apply the `/humanizer` skill to remove AI-like patterns and make it sound naturally written.

**Format:**
```
type(scope): subject.

Body explaining the change and why it matters. Include any migration
notes or breaking change explanations here.

Breaking change: if applicable, describe what changed and how to migrate.
```

### For Pull Requests

1. **Identify all commits** — List the commits in the PR
2. **Find the most important** — Usually the first feature commit or the one with the most impact
3. **Create PR title** — Use that commit's subject line, max 100 chars. Capitalize first letter.
4. **Write PR description** — Include:
   - Broader context of all changes (what was accomplished collectively)
   - Bullet points (max 100 chars each) describing:
     - Main features/fixes added
     - Bugs fixed
     - Tests added
     - Breaking changes (if any)
   - Related issues: `Fixes #123, Closes #456`
     - Any code examples in backticks
5. **Humanize the description** — Apply the `/humanizer` skill to remove AI-generated patterns and make it sound naturally written.

**Format:**
```markdown
## Summary
- Main achievement of this PR (max 100 chars).
- Secondary change or improvement (max 100 chars).
- Anything else notable (max 100 chars).

## Details
`code example or important change`

Fixes #234, #238
```

## Tips

- Stage your changes before invoking this skill — it reads from `git diff --cached`
- For better results, stage related changes together
- For PRs, commit your changes first, then ask for PR documentation
- The skill infers scopes intelligently based on file paths, but you can suggest a scope if needed
