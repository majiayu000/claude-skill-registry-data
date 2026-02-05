---
name: auto-commit
description: Automatically commits changes using conventional commits format (feat:, fix:, docs:, chore:, refactor:, test:, style:). Use after completing bug fixes, feature implementations, or documentation updates. Triggered automatically via Stop hook.
---

# Auto-Commit with Conventional Commits

Automatically stage and commit changes using the conventional commits specification.

## Conventional Commits Format

```
<type>(<scope>): <description>

[optional body]
```

### Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `chore` | Maintenance (deps, configs, build) |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or modifying tests |
| `style` | Formatting, whitespace, linting |
| `perf` | Performance improvements |
| `ci` | CI/CD changes |

### Scope (Optional)

Add scope in parentheses for context:
- `feat(auth): add login endpoint`
- `fix(api): handle null response`
- `docs(readme): update install instructions`

## Commit Workflow

1. Check for changes: `git status`
2. If changes exist:
   - Stage all: `git add -A`
   - Review staged: `git diff --staged`
   - Determine type from changes
   - Write concise description (imperative mood)
   - Commit with proper format

## Message Guidelines

- Use imperative mood: "add feature" not "added feature"
- Keep first line under 72 characters
- Don't end with period
- Be specific but concise

### Good Examples

```
feat(api): add user authentication endpoint
fix: resolve null pointer in payment processing
docs: update API usage examples
chore: upgrade dependencies to latest versions
refactor(db): extract query builder to separate module
```

### Bad Examples

```
updated stuff          # Too vague
Fixed the bug.         # Don't end with period
Added new feature      # Wrong tense
```

## Important

- Only commit, do NOT push
- Always use conventional commits format
- Include scope when it adds clarity
