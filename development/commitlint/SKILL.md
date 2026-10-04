---
name: commitlint
description: >
  Validate commit messages against the Conventional Commits specification.
  Auto-detects and installs commitlint CLI if missing. Checks project
  config or falls back to sensible defaults. Use when validating commit
  messages, preparing PRs, or enforcing commit conventions.
compatibility: >
  Requires Node.js (npx). Works with any git repository.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Commitlint

Validate commit messages follow the
[Conventional Commits](https://www.conventionalcommits.org/) specification.
Enables automatic changelog generation, semantic versioning, and clean git
history.

## What this skill does

1. Checks if `@commitlint/cli` and `@commitlint/config-conventional` are
   installed; installs them if missing.
2. Detects project-specific commitlint configuration or falls back to a
   sensible default config.
3. Validates commit messages for type, scope, subject, body, and footer
   format.
4. Reports errors with specific fixes and examples.

## Installation check

```bash
# Check if commitlint is available
npx commitlint --version 2>/dev/null
```

If not installed, install globally:

```bash
npm install -g @commitlint/cli @commitlint/config-conventional
```

If installation fails (permissions, no npm), stop validation and report
the issue with remediation steps:

- Use `sudo npm install -g ...` or fix npm permissions
- Use a Node version manager (nvm, volta, fnm)
- Install Node.js if not present

Do **not** silently skip validation.

## Config detection priority

1. `commitlint.config.js` in project root
2. `.commitlintrc.json` in project root
3. `.commitlintrc.yaml` in project root
4. `.commitlintrc` in project root
5. `commitlint` field in `package.json`
6. Default config (see `references/conventional-commits.md`)

If no project config exists, create a temporary `.commitlintrc.json` using
the default config from the reference document before running validation.

## Validation workflow

```text
1. Check commitlint installation
   ├─ Installed → continue
   └─ Missing → install, then continue (fail if install fails)

2. Detect project config
   ├─ Found → use it
   └─ Not found → use default config from references/

3. Run validation
   ├─ From a string:
   │    echo "<message>" | npx commitlint
   ├─ From a file:
   │    cat <file> | npx commitlint
   └─ From last git commit:
        git log -1 --format=%B | npx commitlint

4. Report results
   ├─ Valid → confirm and proceed
   └─ Invalid → show errors, suggest fixes, re-validate after correction
```

## Validation methods

### Validate a commit message string

```bash
echo "feat(api): add login endpoint" | npx commitlint
```

### Validate contents of a file

```bash
cat path/to/message-file.txt | npx commitlint
```

### Validate the most recent git commit

```bash
git log -1 --format=%B | npx commitlint
```

## Error handling

### Install failure

If commitlint cannot be installed, report the error and provide
remediation steps. Do not proceed with validation.

### Invalid message

When validation fails, report each error with:

- The rule that failed (e.g., `type-enum`, `header-max-length`)
- What was wrong (e.g., type `feature` is not allowed)
- A concrete fix (e.g., use `feat` instead)

Example:

```text
Validation failed:

1. type-enum: type 'feature' is not allowed
   Allowed: feat, fix, docs, style, refactor, perf, test, build, ci,
            chore, revert
   Fix: use 'feat' instead of 'feature'

2. header-max-length: header is 72 characters (max 50)
   Fix: shorten to 'feat: add user authentication with JWT'
```

After reporting errors, suggest a corrected message and re-validate.

## Format reference

See `references/conventional-commits.md` for the full Conventional Commits
format specification, type descriptions, rules, default config, and
examples.
