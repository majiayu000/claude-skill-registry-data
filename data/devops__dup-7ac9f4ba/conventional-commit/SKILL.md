---
name: conventional-commit
description: Generates commit messages following Conventional Commits 1.0.0 specification. Use when committing changes, staging files, creating commits, or when user says "commit", "git commit", or asks for a commit message.
---

# Conventional Commit Generator

Generate commit messages following [Conventional Commits 1.0.0](https://www.conventionalcommits.org/).

## Workflow

1. Run `git status` and `git diff HEAD` to analyze changes
2. Stage files: user-specified only, or `git add -A` for all
3. Determine type and scope from changes
4. Generate commit message incorporating user hints
5. Commit: `git commit -m "subject" -m "body" -m "footer"`
6. Output: `<hash> <subject>`

## Scope Boundaries

**DO:** Analyze git changes, generate messages, stage files, commit

**DO NOT:** Modify code, push (unless asked), create branches, amend without request

## Commit Format

```
<type>(<scope>)<!>: <description>

<body>

<footer>
```

## Type Selection

| Change | Type |
|--------|------|
| Bug fix | `fix` |
| New/changed feature | `feat` |
| Performance | `perf` |
| Restructuring | `refactor` |
| Formatting | `style` |
| Tests | `test` |
| Documentation | `docs` |
| Build/deps | `build` |
| CI/CD | `ci` |
| DevOps | `ops` |
| Other | `chore` |

## Subject Line (max 72 chars)

- Format: `type(scope): description` or `type: description`
- Imperative mood: "add" not "added"
- Lowercase first letter, no trailing period

## Breaking Changes

Add `!` before colon: `feat(api)!: remove endpoint`

Footer: `BREAKING CHANGE: description`

## Examples

```
feat: add email notifications on new messages
```

```
fix(cart): prevent ordering empty shopping cart
```

```
feat(api)!: remove status endpoint

BREAKING CHANGE: /api/status removed, use /api/health instead.
Refs: JIRA-1337
```

## Anti-patterns

Avoid: "update", "fix bug", "changes", "WIP", capitalized first letter, trailing period, past tense
