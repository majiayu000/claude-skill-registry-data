---
allowed-tools: Bash, Read, Grep
description: 'Create well-structured git commits following conventional commit format.

  Use when committing changes, preparing commits, or reviewing staged changes.'
name: commit
---

# Commit Workflow

Create well-structured git commits following conventional commit format.

## Process

1. **Review changes**: Examine staged and unstaged modifications
2. **Analyze scope**: Determine what areas of the codebase are affected
3. **Select type**: Choose the appropriate commit type
4. **Write message**: Craft a clear, descriptive commit message
5. **Execute commit**: Perform the commit with the message

## Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation changes only |
| `style` | Formatting, whitespace, no code change |
| `refactor` | Code restructuring without behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or dependencies |
| `ci` | CI/CD configuration |
| `chore` | Maintenance, tooling, other |

## Message Format

```
type(scope): subject

[optional body]

[optional footer]
```

### Rules

- **Subject**: Imperative mood, no period, max 50 chars
- **Scope**: Optional, identifies the module/area affected
- **Body**: Explain what and why (not how), wrap at 72 chars
- **Footer**: Reference issues, breaking changes

## Examples

### Feature Addition
```
feat(auth): add OAuth2 login with Google provider

Implement Google OAuth authentication flow:
- Add OAuth client configuration
- Create callback handler
- Store tokens securely in session

Closes #123
```

### Bug Fix
```
fix(api): handle null response from external service

The payment gateway occasionally returns null for
declined transactions. Add null check and return
appropriate error message.

Fixes #456
```

### Documentation
```
docs(readme): update installation instructions

Add prerequisites section and troubleshooting guide.
```

### Refactoring
```
refactor(utils): extract date formatting to shared module

Move duplicated date formatting logic from three
components into a shared utility function.
```

## Anti-Patterns to Avoid

- `updated stuff` - Too vague
- `fix bug` - Which bug? Where?
- `WIP` - Don't commit work-in-progress
- `asdf` or `temp` - Meaningless
- Giant commits touching unrelated files

## Pre-Commit Checklist

Before committing, verify:

- [ ] Changes are staged (`git status`)
- [ ] No unintended files included
- [ ] Tests pass (if applicable)
- [ ] Linting passes (if applicable)
- [ ] Commit message follows format
- [ ] Scope accurately reflects changes
