---
name: git-use
description: Git operations with conventional commits.
TRIGGER: git commit, git push, git status, commit changes
---

# Git Operations

Handle git operations using
[Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

| Type       | Description                | SemVer |
| ---------- | -------------------------- | ------ |
| `feat`     | New feature                | MINOR  |
| `fix`      | Bug fix                    | PATCH  |
| `docs`     | Documentation only         | -      |
| `style`    | Formatting, no code change | -      |
| `refactor` | Neither fix nor feature    | -      |
| `perf`     | Performance improvement    | PATCH  |
| `test`     | Adding/correcting tests    | -      |
| `build`    | Build system, dependencies | -      |
| `ci`       | CI configuration           | -      |
| `chore`    | Other non-src/test changes | -      |
| `revert`   | Reverts a previous commit  | -      |

### Rules

1. Description: imperative mood, lowercase, no period, ≤50 chars (72 for body)
2. Scope: noun in parentheses describing affected area, e.g., `feat(api):`, `fix(parser):`, `docs(readme):`
3. Body: explain _what_ and _why_, not _how_ (blank line after description)
4. Footer: use for breaking changes, issue refs, co-authors
5. Breaking changes: append exclamation mark after type/scope OR add `BREAKING CHANGE:` footer (triggers MAJOR)
   - Example: `feat!:` or `refactor(api)!:`
   - Use double quotes in shell commands, not single quotes

### Examples

```
feat: add user authentication

fix: resolve memory leak in data processor

docs: correct spelling of CHANGELOG

feat(lang): add Polish language

fix: prevent racing of requests

Introduce a request id and a reference to latest request.
Dismiss incoming responses other than from latest request.

Refs: #123

feat!: drop support for Node 14

BREAKING CHANGE: Node 14 has reached end-of-life. Minimum required version is now Node 18.

refactor(api)!: rename endpoints for consistency

/users → /api/users
/posts → /api/posts

BREAKING CHANGE: All REST endpoints now prefixed with /api

revert: revert "feat: add experimental caching layer"

This reverts commit 676104e.
The caching implementation caused data inconsistencies in production.

Refs: #456
```

## Commit Workflow

1. `git status` — review all changes
2. `git diff [--staged]` — understand what changed
3. **Analyze grouping** — split if changes are logically independent:
   - Different types (`feat` + `fix` → 2 commits)
   - Unrelated areas (frontend + backend for different features → 2 commits)
   - Keep related changes together (one feature across multiple files → 1
     commit)
4. **For each logical group:**
   - Stage specific files: `git add <files>` (never blind `git add .`)
   - Commit:
     - Simple: `git commit -m "type(scope): description"`
     - With body: `git commit -m "type: description" -m "Body paragraph"`
     - With editor: `git commit` (for complex messages with body/footer)
5. `git status` — verify completion

## Rules

### Pre-commit Checks

Before committing, verify:

- **Secrets**: Exclude `.env`, `credentials.json`, API keys, tokens
- **Tests**: Run `npm test`, `pytest`, `cargo test`, or project-specific commands
- **Linting**: Run linters/formatters (`eslint`, `prettier`, `ruff`, etc.)
- **Hooks**: Check if pre-commit hooks exist (`.git/hooks/pre-commit`)
- **Unintended files**: Review `git status` output carefully

### Amending

```
git commit --amend           # edit message and content
git commit --amend --no-edit # keep message, add staged changes
```

⚠️ Warn user if commit was already pushed (requires `--force`).

### Push

```
git push                        # existing upstream
git push -u origin <branch>     # new branch
```
