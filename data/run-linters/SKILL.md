---
name: run-linters
description: Run linters after code changes to verify code quality. Use this skill after completing code modifications to catch and fix any linting issues.
allowed-tools: Bash(linters:*), Read, Edit
---

# Run Linters

Execute linters after code changes are complete to ensure code quality and consistency.

## When to Use

- After completing a set of code changes (not after each small edit)
- Before creating a commit or PR
- When asked to verify code quality

## Step 1: Run Linters

Execute the `linters` command which auto-detects active linters in the current repository and runs them with proper configurations:

```bash
linters
```

## Step 2: Analyze Results

- If no issues: Report success and proceed
- If issues found: Continue to Step 3

## Step 3: Fix Issues

For each issue reported:

1. Read the affected file
2. Understand the linting error
3. Fix the issue **in the source code** using Edit tool
4. Re-run `linters` to verify the fix

Repeat until all issues are resolved.

## Important Rules

- Do NOT run after every small change - wait until a logical set of changes is complete
- Fix all issues before reporting completion
- **NEVER modify linter configuration files** to suppress or ignore issues
- **NEVER add inline disable comments** (e.g., `// eslint-disable`, `# noqa`, `// nolint`) to bypass issues
- Always fix the actual code, not the linter rules
- If an issue seems impossible to fix properly, ask the user for guidance

## Forbidden Files - NEVER Modify

The following configuration files must NEVER be edited to work around linting issues:

**JavaScript/TypeScript:**

- `.eslintrc`, `.eslintrc.js`, `.eslintrc.json`, `.eslintrc.yml`
- `.prettierrc`, `.prettierrc.js`, `.prettierrc.json`
- `eslint.config.js`, `eslint.config.mjs`
- `tsconfig.json` (for strict mode or type checking options)

**Python:**

- `.flake8`, `setup.cfg` (flake8 section)
- `pyproject.toml` (tool.flake8, tool.pylint, tool.ruff sections)
- `.pylintrc`, `pylintrc`
- `ruff.toml`, `.ruff.toml`
- `mypy.ini`, `.mypy.ini`

**Ruby:**

- `.rubocop.yml`, `.rubocop_todo.yml`

**Go:**

- `.golangci.yml`, `.golangci.yaml`

**Rust:**

- `clippy.toml`, `.clippy.toml`
- `rustfmt.toml`, `.rustfmt.toml`

**Markdown:**

- `.markdownlint.json`, `.markdownlint.yaml`, `.markdownlint.yml`
- `.markdownlintrc`

**General:**

- `.editorconfig`
- Any file that defines linting rules or ignores

## Forbidden Patterns - NEVER Use

Do NOT add these patterns to bypass linting:

```text
# JavaScript/TypeScript
/* eslint-disable */
// eslint-disable-line
// eslint-disable-next-line
/* prettier-ignore */
// @ts-ignore
// @ts-nocheck

# Python
# noqa
# type: ignore
# pylint: disable
# ruff: noqa

# Go
//nolint
//nolint:all

# Ruby
# rubocop:disable

# Rust
#[allow(...)]
#![allow(...)]
```

If you encounter an issue that seems unfixable, explain the problem to the user and ask how they want to proceed.
