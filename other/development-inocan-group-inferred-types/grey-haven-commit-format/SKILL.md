---
name: grey-haven-commit-format
description: Format commit messages according to Grey Haven Studio's actual commitlint configuration (100 char header, lowercase subject, conventional commits). Use when creating git commits or reviewing commit messages.
# v2.0.43: Skills to auto-load for commit work
skills:
  - grey-haven-code-style
# v2.0.74: Tools for commit formatting
allowed-tools:
  - Read
  - Bash
  - Grep
  - TodoWrite
---

# Grey Haven Commit Message Format

Follow Grey Haven Studio's **actual** commit message standards, enforced by commitlint configuration from production templates.

## Format Structure

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## CRITICAL Rules (Commitlint Enforced)

**These rules are automatically enforced by commitlint:**

1. **Header max length: 100 characters** (NOT 72 or 50!)
2. **Type: REQUIRED** and must be lowercase
3. **Subject: REQUIRED** and lowercase (NO sentence-case, start-case, pascal-case, or upper-case)
4. **Body: blank line before** (if included)
5. **Footer: blank line before** (if included)

## Commit Types

Use **exactly** these types from Grey Haven's commitlint configuration:

| Type | Use Case | Example |
|------|----------|---------|
| **feat** | New feature for the user | `feat(auth): add magic link authentication` |
| **fix** | Bug fix for the user | `fix(api): resolve race condition in order processing` |
| **docs** | Documentation changes only | `docs(readme): update TanStack Start setup guide` |
| **style** | Code style changes (formatting) - no logic changes | `style: apply Prettier to all TypeScript files` |
| **refactor** | Code refactoring - neither fixes a bug nor adds a feature | `refactor(repositories): simplify user query logic` |
| **test** | Adding or updating tests | `test(auth): add integration tests for OAuth flow` |
| **chore** | Maintenance tasks, dependency updates | `chore(deps): upgrade React to v19.1.0` |
| **perf** | Performance improvements | `perf(db): add composite index on user_id and created_at` |
| **ci** | CI/CD configuration changes | `ci: add Vitest coverage threshold check` |
| **build** | Build system or dependency changes | `build: configure bun for monorepo` |
| **revert** | Revert a previous commit | `revert: feat(auth): add OAuth authentication` |

**Any other type will be REJECTED by commitlint.**

## Subject Line Rules

### Requirements
- **Max length: 100 characters** (header includes type + scope + subject)
- **Case: lowercase ONLY** - NO capitals anywhere
- **Format: imperative mood** - "add" not "added" or "adds"
- **No period** at the end
- **Be specific** about what changed

### Calculating Header Length
```
feat(auth): add OAuth provider for Google authentication
^---------^ = 9 chars (type + scope)
            ^----------------------------------------^ = 45 chars (subject)
Total: 54 characters (within 100 limit ✅)
```

### Good Examples
```
feat(auth): add password reset with email verification
fix(api): prevent duplicate user email registrations
docs: update API authentication guide with examples
refactor(utils): simplify date formatting helper functions
perf(db): add composite index on user_id and created_at
```

### Bad Examples (Fail Commitlint)
```
❌ feat(auth): Add OAuth provider     # Uppercase 'A' (violates subject-case)
❌ Fix bug in API                      # Uppercase 'F' (violates subject-case)
❌ feat: add new feature.              # Period at end
❌ WIP                                 # Not a valid type
❌ added new endpoint                  # Missing type
❌ feat(api): Added endpoint and updated schema and added validation and wrote tests and updated docs
   # Exceeds 100 characters
```

## Scope Guidelines

The scope should indicate which part of the codebase is affected:

### Frontend Scopes (TanStack Start/React)
- `auth`, `ui`, `forms`, `layout`, `routes`, `queries`, `db`, `server`

### Backend Scopes (FastAPI/Python)
- `api`, `models`, `repositories`, `services`, `schemas`, `db`, `utils`, `config`

### Infrastructure Scopes
- `deps`, `docker`, `deploy`, `scripts`, `ci`, `hooks`

**Scope is optional** - omit if change affects multiple areas or is global.

## Body (Optional)

Use the body to provide additional context when needed.

### When to Include a Body
- Explaining **why** the change was made (motivation)
- Describing **implementation approach** that isn't obvious
- Noting **breaking changes** or important considerations
- Referencing **related Linear issues** or GitHub issues
- Listing **multiple changes** in a larger commit

### Body Format
- **Blank line REQUIRED** between subject and body
- Wrap at **90 characters per line**
- Use **bullet points** for lists (markdown format)
- Write in **present tense**, imperative mood

## Footer (Optional)

### Breaking Changes (CRITICAL)
Start with `BREAKING CHANGE:` followed by description:

```
feat(api): migrate user IDs to UUID format

Change user ID format from sequential integers to UUIDs for better
scalability and security in multi-tenant architecture.

BREAKING CHANGE: User IDs are now UUIDs instead of sequential integers.
All API clients must update to handle UUID format. Database migration
required before deploying this change.
```

### Linear Issue References
```
Fixes GREY-456
Related to GREY-123
```

### GitHub Issue References
```
Fixes #234
Closes #456
Related to #789
```

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete commit message examples
  - [frontend-examples.md](examples/frontend-examples.md) - TypeScript/TanStack examples
  - [backend-examples.md](examples/backend-examples.md) - Python/FastAPI examples
  - [multi-tenant-examples.md](examples/multi-tenant-examples.md) - Multi-tenant patterns
  - [breaking-change-examples.md](examples/breaking-change-examples.md) - Breaking changes
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Configuration and rules
  - [commitlint-config.md](reference/commitlint-config.md) - Commitlint configuration
  - [scope-reference.md](reference/scope-reference.md) - Detailed scope guidelines
  - [validation.md](reference/validation.md) - Pre-commit validation
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [simple-commit.txt](templates/simple-commit.txt) - Simple commit template
  - [with-body.txt](templates/with-body.txt) - Commit with body template
  - [breaking-change.txt](templates/breaking-change.txt) - Breaking change template

- **[checklists/](checklists/)** - Pre-commit validation
  - [commit-checklist.md](checklists/commit-checklist.md) - Pre-commit checklist

## Quick Checklist

Before committing, verify:

- [ ] Type is one of: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
- [ ] Type is lowercase
- [ ] Subject is lowercase (NO capitals anywhere)
- [ ] Subject uses imperative mood ("add" not "added")
- [ ] Full header is under 100 characters
- [ ] Subject doesn't end with a period
- [ ] Body has blank line after subject (if included)
- [ ] Breaking changes start with "BREAKING CHANGE:"

## When to Apply This Skill

Use this skill when:
- Creating git commits in Grey Haven projects
- Reviewing pull requests and commit messages
- Setting up commit message templates
- Configuring commitlint for new projects
- Writing release notes from commit history
- Squashing commits before merging

## Template Reference

These standards come from Grey Haven's actual templates:
- **cvi-template**: TanStack Start + React 19 (commitlint.config.cjs)
- **cvi-backend-template**: FastAPI + SQLModel (same commitlint config)

## Critical Reminders

1. **Header max: 100 characters** (NOT 72 or 50!)
2. **Subject: lowercase ONLY** (NO capitals anywhere)
3. **Types: exact match required** (feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert)
4. **Body/footer: blank line before** (enforced by commitlint)
5. **Breaking changes: use BREAKING CHANGE:** prefix
6. **Linear issues: reference as GREY-123**
7. **Multi-tenant: mention tenant_id when relevant**
8. **Python projects: activate .venv before committing**
9. **Pre-commit hooks: will validate format automatically**
10. **Squash merges: preferred for main branch**
