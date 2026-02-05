---
name: atomic-commits
description: Creates semantic atomic commits using Conventional Commits. Use always when committing changes, staging files, or when asked to commit code. Analyzes diffs, suggests scope, and can split changes into granular commits.
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

# Atomic Commits

Creates well-structured, semantic commits following [Conventional Commits](https://www.conventionalcommits.org/) specification. Automatically analyzes changes and creates atomic, focused commits.

## Core Principles

1. **Atomic**: Each commit represents ONE logical change
2. **Semantic**: Type prefix describes the nature of the change
3. **Scoped**: Optional scope indicates the affected module/component
4. **Descriptive**: Message explains WHAT and WHY, not HOW

## Workflow

### Step 1: Analyze Changes

Run these commands to understand the current state:

```bash
git status
git diff --staged
git diff
```

### Step 2: Identify Commit Types

For each logical change, determine the appropriate type:

| Type       | When to Use                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | New feature for the user                                |
| `fix`      | Bug fix for the user                                    |
| `docs`     | Documentation only changes                              |
| `style`    | Formatting, missing semicolons (no code change)         |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf`     | Performance improvement                                 |
| `test`     | Adding or fixing tests                                  |
| `build`    | Build system or external dependencies                   |
| `ci`       | CI configuration files and scripts                      |
| `chore`    | Other changes that don't modify src or test files       |
| `revert`   | Reverts a previous commit                               |

### Step 3: Determine Scope

Analyze changed files to suggest scope:

- `api/` → scope: `api`
- `core/database.py` → scope: `db`
- `agents/faq_agent/` → scope: `faq-agent`
- `tests/` → scope: `tests`
- Multiple areas → consider splitting into multiple commits

### Step 4: Create Atomic Commits

If changes span multiple concerns, split them:

```bash
git add -p  # Stage hunks interactively (but explain to user)
```

Or stage specific files:

```bash
git add <specific-files>
git commit -m "<type>(<scope>): <description>"
```

### Step 5: Validate Message Format

Before committing, validate the message follows the pattern:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Rules:

- Type is required and lowercase
- Scope is optional, lowercase, in parentheses
- Description starts lowercase, no period at end
- Max 72 characters for first line
- Body wrapped at 72 characters
- Breaking changes: add "!" after type/scope or "BREAKING CHANGE:" in footer
- **NEVER add auto-generated labels** like "Generated with Claude Code", "Co-Authored-By", or any AI attribution
- Commit messages must be clean and professional, as if written by the developer

## Commit Message Template

```
<type>(<scope>): <short description>

<body - explain WHAT and WHY>

<footer>
```

## Breaking Changes

For breaking changes, use one of:

```bash
feat(api)!: change authentication method

feat(api): change authentication method

BREAKING CHANGE: API now requires Bearer token instead of API key
```

## Multi-Commit Strategy

When changes are complex, create separate commits for:

1. **Preparation**: Refactoring needed before the feature
2. **Core**: The main feature/fix implementation
3. **Tests**: New or updated tests
4. **Docs**: Documentation updates

Example sequence:

```
refactor(auth): extract token validation to separate function
feat(auth): add OAuth2 support
test(auth): add OAuth2 integration tests
docs(auth): update authentication guide
```

## Interactive Mode

When asked to commit, always:

1. Show the user what will be committed (files and diff summary)
2. Suggest the commit type and scope
3. Propose a commit message
4. Ask for confirmation before executing

## References

See [CONVENTIONS.md](CONVENTIONS.md) for detailed type definitions.
See [EXAMPLES.md](EXAMPLES.md) for real-world examples.
