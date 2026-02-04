---
name: commit-formatter
description: Use this skill when the user needs help formatting git commit messages according to Conventional Commits specification. Provides guidance on commit types, scope, and message structure.
---

# Commit Formatter Skill

## When to Use

This skill MUST be used when:
- User asks to create a git commit message
- User requests help with commit message format
- User mentions "conventional commits" or commit standards
- User asks how to format commits for their repository

## What This Skill Does

Guides users in creating well-formatted git commit messages following the Conventional Commits specification (https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, whitespace)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvements
- **test**: Adding or correcting tests
- **chore**: Changes to build process or auxiliary tools
- **ci**: CI configuration changes
- **build**: Changes to build system or dependencies

## Instructions

When helping users format commits:

1. **Analyze the changes**: Ask about or review what was changed
2. **Determine the type**: Select the most appropriate commit type
3. **Identify scope** (optional): If changes are isolated to a component/module
4. **Write description**: Short (max 50 chars), imperative mood ("add" not "added")
5. **Add body** (if needed): Explain what and why, not how (wrap at 72 chars)
6. **Add footers** (if needed): Breaking changes, issue references

## Examples

### Simple Feature
```
feat: add user authentication to API
```

### Feature with Scope
```
feat(auth): implement JWT token refresh mechanism
```

### Bug Fix with Body
```
fix: prevent race condition in user signup

The signup process was not properly locking user records,
causing duplicate accounts when multiple requests arrived
simultaneously. Added transaction locking to prevent this.
```

### Breaking Change
```
feat!: change API response format to match REST standards

BREAKING CHANGE: API responses now return data in 'data' field
instead of root level. Update all API clients accordingly.
```

### With Issue Reference
```
fix: correct validation error in email field

Fixes #123
```

## Best Practices

- Keep the first line under 50 characters
- Separate subject from body with blank line
- Use imperative mood ("change" not "changed" or "changes")
- Explain what and why in the body, not how
- Reference issues and PRs in footer
- Use `!` or `BREAKING CHANGE:` for breaking changes
- One logical change per commit

## Platform Compatibility

This skill works on:
- Claude Code (recommended - can analyze git diff)
- Claude.ai (provide change description)
- Claude API (integrate in your git workflow)
