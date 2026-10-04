---
name: markdownlint
description: >
  Validate markdown files against formatting standards. Auto-detects and
  installs markdownlint-cli if missing. Checks project config or falls
  back to sensible defaults. Supports auto-fix mode. Use when creating
  or modifying markdown files, validating documentation, or enforcing
  markdown conventions.
compatibility: >
  Requires Node.js (npx). Works with any project containing markdown
  files.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Markdownlint

Validate markdown files follow formatting standards. Enables consistent
documentation, readable diffs, and POSIX compliance.

## What this skill does

1. Checks if `markdownlint-cli` is installed; installs if missing.
2. Detects project-specific markdownlint configuration or falls back to a
   minimal default config.
3. Validates markdown files for formatting, structure, and style.
4. Optionally auto-fixes common issues with `--fix` flag; reports errors
   with specific rules and fixes.

## Installation check

```bash
# Check if markdownlint is available
markdownlint --version 2>/dev/null
```

If not installed, install globally:

```bash
npm install -g markdownlint-cli
```

If installation fails (permissions, no npm), stop validation and report
the issue with remediation steps:

- Use `sudo npm install -g ...` or fix npm permissions
- Use a Node version manager (nvm, volta, fnm)
- Install Node.js if not present

Do **not** silently skip validation.

## Config detection priority

1. `.markdownlint.json` in project root
2. `.markdownlint.yaml` in project root
3. `.markdownlintrc` in project root
4. `markdownlint` field in `package.json`
5. Default config (see `references/markdownlint-config.json`)

If no project config exists, create a temporary `.markdownlint.json` using
the default config from the reference file before running validation.

## Validation workflow

```text
1. Check markdownlint installation
   ├─ Installed → continue
   └─ Missing → install, then continue (fail if install fails)

2. Detect project config
   ├─ Found → use it
   └─ Not found → use default config from references/

3. Run validation
   ├─ Check only:
   │    markdownlint <files-or-directories>
   └─ Auto-fix:
        markdownlint --fix <files-or-directories>

4. Report results
   ├─ Valid → confirm and proceed
   └─ Invalid → show errors, suggest fixes, re-validate after correction
```

## Validation methods

### Check files (default)

```bash
markdownlint README.md CHANGELOG.md docs/
```

### Auto-fix common issues

```bash
markdownlint --fix README.md CHANGELOG.md docs/
```

Note: some issues (like MD001 heading-increment) cannot be auto-fixed and
require manual correction. Re-run without `--fix` after fixing to confirm
all issues resolved.

## Error handling

### Install failure

If markdownlint cannot be installed, report the error and provide
remediation steps. Do not proceed with validation.

### Validation failure

When validation fails, report each error with:

- The rule that failed (e.g., `MD022/blanks-around-headings`)
- What was wrong (e.g., heading not surrounded by blank lines)
- A concrete fix

Example:

```text
Validation failed:

1. MD022/blanks-around-headings: heading not surrounded by blank lines
   File: README.md:15
   Fix: add blank lines before and after the heading

2. MD047/single-trailing-newline: file does not end with newline
   File: CHANGELOG.md:89
   Fix: add a single newline at end of file
```

After reporting errors, suggest running `markdownlint --fix` for
auto-fixable issues and provide manual fixes for the rest. Re-validate
after corrections.

## Format reference

See `references/markdownlint-rules.md` for the full rule reference, common
fixes, and auto-fixable rules.
