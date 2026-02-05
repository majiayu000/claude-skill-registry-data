---
name: helping-with-commits
description: Automates Git commit creation with Conventional Commits. Use when user wants to commit changes. (project)
allowed-tools: Read, Grep, Glob, Bash
---

# Commit Helper

Create commits following Conventional Commits specification and project conventions.

## Project-Specific Scopes

Use these scopes for leapmultix: `arcade`, `i18n`, `ui`, `a11y`, `perf`, `pwa`, `test`, `deps`

Omit scope if changes span multiple domains.

## Validation Before Commit

Always run before committing:

```bash
npm run format:check  # If fails → npm run format
npm run lint          # If fails → npm run lint:fix
npm test
npm run i18n:compare  # Only if i18n/* modified
```

## Project Examples

```
feat(arcade): add power-up system to Multimiam
fix(i18n): correct missing Spanish translation keys
refactor(ui): extract modal component logic
chore(deps): update jest to 29.7.0
```

## Rules

1. **Never commit without user approval** - Always show the commit message and wait for explicit validation
2. **Never mention AI** in commit messages (no "Generated with Claude", no "Co-Authored-By: Claude")
3. **Never commit** if tests fail (unless explicit WIP request)
4. **Never commit** secrets or API keys
5. **Multiple changes = multiple commits** if they have different types (feat + fix = 2 commits)
