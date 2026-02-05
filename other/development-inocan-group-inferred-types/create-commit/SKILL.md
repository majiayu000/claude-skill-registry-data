---
name: create-commit
description: When asked to commit the codebase, follow these guidelines
---

## Process

- Look at the current staged and unstaged changes with `git status` and `git diff`
- Stage changes if needed using `git add .`
- Create focused, atomic commits with clear messages
- Refrain from adding one big commit, instead create multiple smaller atomic commits when it makes sense to do so

## Scope Guidelines

Prefer feature/change-focused scopes over package names:

- **First choice**: Feature or domain names that describe what's being changed
- **Fallback**: Package names if no clear feature scope exists
- **Always use**: `deps`/`deps-dev` for dependency updates
- **Infrastructure**: Generic scopes like `ci`, `docker`, `scripts` are fine

## Rules

- Use conventional commit format: `type(scope): description`
- Keep title under 100 characters
- Use `--no-verify` for .md files
- Never use heredoc or cat for commit messages
- Avoid ANSI codes in commit messages
- Never adjust code when running this, only create commits
