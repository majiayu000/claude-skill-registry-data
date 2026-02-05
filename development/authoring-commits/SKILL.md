---
name: authoring-commits
description: Conventional Commits standards for git messages. Use when creating commits, writing commit messages, or reviewing commit history.
---

# Commit Authoring

Write commit messages following Conventional Commits v1.0.0.

## Message Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Rules

1. Prefix with type, optional scope in parentheses, optional `!` for breaking changes, colon, space
2. `feat` for new features (MINOR in SemVer)
3. `fix` for bug fixes (PATCH in SemVer)
4. Description immediately follows the colon and space
5. Body separated by one blank line, free-form
6. Footers one blank line after body, token-separator-value format
7. Footer tokens use `-` instead of spaces (except `BREAKING CHANGE`)
8. `!` before `:` indicates breaking change; `BREAKING CHANGE:` footer may be omitted if `!` is used
9. Breaking changes correlate with MAJOR in SemVer

## Types

| Type | Purpose | SemVer |
|------|---------|--------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `docs` | Documentation only | - |
| `style` | Formatting, whitespace | - |
| `refactor` | Neither fix nor feature | - |
| `perf` | Performance improvement | - |
| `test` | Adding or updating tests | - |
| `build` | Build system or dependencies | - |
| `ci` | CI configuration | - |
| `chore` | Maintenance tasks | - |

## Description

Use imperative mood: "add feature" not "added feature". Keep under 50 characters. No period. Lowercase after type prefix.

## Body

Wrap at 72 characters. Explain what and why, not how.

## Prohibited

Do not include "Generated with Claude Code", AI attribution, Co-authored-by lines for AI, emoji, time estimates, dates, or TODO items.

## Examples

Simple:
```
docs: correct spelling of CHANGELOG
```

With scope:
```
feat(lang): add Polish language
```

Breaking change:
```
feat!: send email to customer when product ships

BREAKING CHANGE: customers now receive emails by default.
```

With body:
```
fix: prevent duplicate form submissions

Disables submit button after first click and adds
debounce to the handler.
```

With footer:
```
fix: resolve race condition in auth flow

Refs: #123
Reviewed-by: Alice
```
