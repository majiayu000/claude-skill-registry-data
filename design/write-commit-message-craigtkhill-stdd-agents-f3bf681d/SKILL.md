---
name: write-commit-message
description: Use when creating git commits. Defines conventional commit format and message structure guidelines.
---

# Commit Message Guidelines

Guidelines for writing clear, consistent git commit messages.

## Conventional Commits Format

Use the conventional commits style:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Full Format with All Options

```
<type>[optional scope]!: <description>

[optional body]

[optional footer: value]
[optional footer: value]
```

### Commit Types

- **feat:** New feature
- **fix:** Bug fix
- **test:** Adding or updating tests
- **docs:** Documentation changes
- **refactor:** Code refactoring (no functional changes)
- **style:** Code style changes (formatting, whitespace)
- **chore:** Maintenance tasks, dependencies
- **perf:** Performance improvements
- **ci:** CI/CD configuration changes
- **build:** Build system changes

### Scope (Optional)

Add scope in parentheses to provide additional context:

### Breaking Changes

Indicate breaking changes with `!` after type/scope:

### Description Guidelines

- Use imperative mood ("add feature" not "added feature")
- Start with lowercase
- No period at the end
- Keep under 72 characters
- Be specific and descriptive

## Multi-line Commits

For complex changes, use a body to provide context:

## Footers

Footers provide metadata about the commit.

### Breaking Changes

Document breaking changes in footer:

## Commit Message Customization

**IMPORTANT**: Do NOT include AI attribution footers like:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

Keep commit messages clean and focused on the changes themselves.

## Before Committing

1. Check for remote updates: `git fetch`
2. Review your changes: `git status` and `git diff`
3. Stage relevant files: `git add <files>`
4. Write clear commit message

## Commit Frequency

- Commit logical units of work
- Don't commit half-finished features
- Ensure tests pass before committing
- One commit per requirement or bug fix (when practical)

## Integration with STDD Workflow

When following the spec-test-driven development workflow:

1. After completing a requirement (spec + test + implementation)
2. Ensure all tests pass
3. Run any precommit hooks
3. Commit with descriptive message
4. Reference requirement ID in commit body if helpful
