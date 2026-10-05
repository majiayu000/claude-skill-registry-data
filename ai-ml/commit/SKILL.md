---
description: Format, test, then commit with a conventional commit message
argument-hint: "[optional commit message]"
disable-model-invocation: true
allowed-tools: "Read, Edit, Bash(composer *), Bash(./vendor/bin/phel *), Bash(vendor/bin/phel *), Bash(git *)"
---

# /commit

## Context

!`git diff --stat`
!`git diff --cached --stat`
!`git status --short`

## Instructions

1. **Format** - auto-format staged `.phel` files (no-op on non-Phel changes):
   ```bash
   git diff --cached --name-only --diff-filter=ACMR | grep '\.phel$' | xargs -r vendor/bin/phel format
   ```
   Note: a PostToolUse hook already runs `vendor/bin/phel format` on every Edit/Write - this step covers files staged from other tools.

2. **Test**:
   ```bash
   composer test
   ```
   Fix failures before continuing.

3. **Stage** specific files by name (never `git add -A`).

4. **Draft commit message**:
   - Use `$ARGUMENTS` if given, else generate from the diff.
   - Conventional commit prefixes: `feat:`, `fix:`, `ref:`, `chore:`, `docs:`, `test:`, `ci:`.
   - Scope only when clearly scoped (`feat(statement)`, `fix(connection)`).
   - Never mention AI tooling.

5. **Commit**: `git commit -m "<message>"`.

6. **Changelog check** - if `feat:` / `fix:`, warn when `## [Unreleased]` in `CHANGELOG.md` wasn't updated.

7. Report hash + files.
