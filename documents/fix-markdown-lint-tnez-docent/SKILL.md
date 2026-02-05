---
name: fix-markdown-lint
description: Fix markdown linting errors in documentation files
group: docent
keywords: [markdown, linting, quality, documentation]
version: 1.0.0
author: "@tnez"
---

# Runbook: Fix Markdown Linting

**Purpose:** Fix markdown linting errors in documentation files
**Owner:** Development Team
**Last Updated:** 2025-10-17
**Frequency:** Before releases, when CI lint workflow fails

## Overview

This runbook provides procedures for fixing markdown linting errors using `markdownlint-cli2`. Our CI/CD runs markdown linting on all `*.md` files, and errors will block merges to main.

**Script Reference:** `../../scripts/lint-markdown.sh`

**Expected duration:** 5-10 minutes for most fixes (auto-fix handles ~95% of errors)

## Prerequisites

### Required Tools

- `npm` - Node.js package manager
- Project dependencies installed (`npm install`)

### Required Access

- Write access to fix files locally

### Pre-Flight Checklist

Before starting, ensure:

- [ ] You have npm installed: `npm --version`
- [ ] Project dependencies installed: `ls node_modules/markdownlint-cli2`
- [ ] You are in the project directory

## Procedure

### Step 1: Check Current Lint Status

**Purpose:** Understand what errors exist

**Commands:**

```bash
# Run markdown linter (shows all errors)
npm run lint:md
# Or use the script directly:
scripts/lint-markdown.sh

# Count total errors
npm run lint:md 2>&1 | grep -c "MD0"

# See errors for specific file
scripts/lint-markdown.sh docs/guides/getting-started.md
```

**Validation:**

- Output shows list of files with errors
- Error codes displayed (MD032, MD031, MD029, etc.)
- Line numbers provided for each error

**If step fails:**

- If command not found: `npm install`
- If no errors: linting already passing!

---

### Step 2: Auto-Fix Errors

**Purpose:** Automatically fix ~95% of markdown linting errors

**Commands:**

```bash
# Auto-fix all fixable errors
npm run lint:md -- --fix
# Or use the script directly:
scripts/lint-markdown.sh --fix

# Check remaining errors
npm run lint:md
```

**Validation:**

- Most errors are automatically fixed
- Remaining errors are typically MD029 (ordered list numbering)
- Modified files appear in `git status`

**Common Auto-Fixed Errors:**

- **MD032**: Blank lines around lists (adds blank lines)
- **MD031**: Blank lines around code fences (adds blank lines)
- **MD009**: Trailing spaces (removes them)
- **MD010**: Hard tabs (converts to spaces)
- **MD047**: Files end with newline (adds newline)

**If step fails:**

- No failures expected - auto-fix is safe
- Review changes with `git diff` to understand what changed

---

### Step 3: Fix Remaining Errors Manually

**Purpose:** Handle errors that can't be auto-fixed

**Common Manual Fixes:**

#### MD029: Ordered List Numbering

**Error:**

```
file.md:193:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1]
```

**Cause:** Inconsistent ordered list numbering style

**Fix Options:**

**Option A:** Use sequential numbering (1, 2, 3)

```markdown
1. First item
2. Second item
3. Third item
```

**Option B:** Use all 1's (lazy numbering)

```markdown
1. First item
1. Second item
1. Third item
```

**Commands:**

```bash
# Find the problematic file and line
npm run lint:md 2>&1 | grep MD029

# Edit the file
$EDITOR docs/guides/getting-started.md

# Go to line number shown in error
# Fix numbering to be consistent
# Save and re-check
npm run lint:md
```

**Validation:**

- MD029 errors are gone
- List renders correctly in markdown preview

---

#### MD013: Line Too Long

**Error:**

```
file.md:45 MD013/line-length Line length [Expected: 80; Actual: 120]
```

**Cause:** Line exceeds 80 characters (or configured limit)

**Fix:**

```bash
# View the long line
sed -n '45p' docs/guides/getting-started.md

# Edit and break into multiple lines
$EDITOR docs/guides/getting-started.md

# For code blocks, this rule is often ignored - check if it should be
```

**Note:** Often better to configure `.markdownlintrc` to ignore line length in code blocks

---

#### MD040: Fenced Code Language

**Error:**

```
file.md:67 MD040/fenced-code-language Fenced code blocks should have a language specified
```

**Cause:** Code fence without language specifier

**Fix:**

```markdown
# Before (no language)
```

code here

```

# After (with language)
```bash
code here
```

```

**Common Languages:**

- `bash` - Shell commands
- `javascript` / `typescript` - JS/TS code
- `json` - JSON config
- `markdown` - Markdown examples
- `text` - Plain text output

---

### Step 4: Verify All Errors Fixed

**Purpose:** Confirm linting passes

**Commands:**

```bash
# Run linter
npm run lint:md

# Check exit code
echo $?
# Expected: 0 (success)

# Verify in CI (after commit)
gh run list --workflow=lint.yml --limit 3
```

**Validation:**

- `npm run lint:md` shows "0 error(s)"
- Exit code is 0
- `git status` shows modified files

**If step fails:**

- Review remaining errors
- Repeat Steps 2-3
- Check for typos in fixes

---

### Step 5: Review Changes

**Purpose:** Understand what changed before committing

**Commands:**

```bash
# See all changes
git diff

# Review specific file
git diff docs/guides/getting-started.md

# Check summary of changes
git diff --stat
```

**Validation:**

- Changes are only whitespace/formatting
- No content was accidentally modified
- Lists still make sense

**Common Changes to Expect:**

- Blank lines added before/after lists
- Blank lines added before/after code fences
- Trailing spaces removed
- List numbering made consistent

**If step fails:**

- If unwanted changes: `git checkout -- <file>`
- Re-run auto-fix and be more careful with manual edits

---

### Step 6: Commit Fixes

**Purpose:** Save linting fixes

**Commands:**

```bash
# Stage all markdown files
git add '*.md' 'docs/**/*.md'

# Or stage specific files
git add README.md docs/guides/getting-started.md

# Commit with clear message
git commit -m "chore: fix markdown linting errors

- Auto-fix whitespace and formatting issues
- Fix ordered list numbering consistency
- All lint checks now passing"

# Verify commit
git log -1 --stat
```

**Validation:**

- Commit contains only markdown files
- Commit message follows conventions
- Changes are reasonable in size

**If step fails:**

- Use `git commit --amend` to fix message
- Use `git reset HEAD~1` to undo and restart

---

## Validation

After completing all steps, verify:

1. **Local Lint Passes:**

   ```bash
   npm run lint:md
   # Expected: "Summary: 0 error(s)"
   ```

2. **Exit Code is 0:**

   ```bash
   npm run lint:md && echo "PASS" || echo "FAIL"
   # Expected: "PASS"
   ```

3. **Files Committed:**

   ```bash
   git log -1 --name-only
   # Expected: Shows markdown files changed
   ```

4. **CI Will Pass:**

   ```bash
   # After pushing
   gh run watch
   # Expected: Lint workflow succeeds
   ```

## Troubleshooting

### Common Issues

#### Issue 1: Too Many Errors (> 100)

**Symptoms:**

- Auto-fix leaves many errors
- Errors span many files

**Resolution:**

```bash
# Focus on one directory at a time
npx markdownlint-cli2 'docs/guides/**/*.md' --fix
npx markdownlint-cli2 'docs/rfcs/**/*.md' --fix

# Or one file at a time
npx markdownlint-cli2 docs/guides/getting-started.md --fix

# Check progress
npm run lint:md 2>&1 | grep -c "MD0"
```

---

#### Issue 2: Auto-Fix Breaks Formatting

**Symptoms:**

- Lists are malformed after auto-fix
- Code blocks have extra blank lines

**Resolution:**

```bash
# Revert changes
git checkout -- docs/guides/problematic-file.md

# Fix manually without auto-fix
$EDITOR docs/guides/problematic-file.md

# Check specific file
npx markdownlint-cli2 docs/guides/problematic-file.md
```

**Prevention:**

- Review `git diff` before committing
- Test one file first before bulk auto-fix

---

#### Issue 3: Error Code Not Clear

**Symptoms:**

- Don't understand what MD### means
- Not sure how to fix

**Resolution:**

```bash
# Get rule documentation URL
npm run lint:md 2>&1 | grep -A 1 "MD032"
# Shows link to: https://github.com/DavidAnson/markdownlint/blob/v0.34.0/doc/md032.md

# Or search for rule:
# https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md
```

**Common Rules:**

- MD009: No trailing spaces
- MD010: No hard tabs
- MD013: Line length
- MD029: Ordered list prefixes
- MD031: Fenced code blocks blank lines
- MD032: Lists blank lines
- MD040: Fenced code language
- MD047: Files end with newline

---

#### Issue 4: Linting Passes Locally, Fails in CI

**Symptoms:**

- `npm run lint:md` passes locally
- CI lint workflow fails

**Resolution:**

```bash
# Ensure you're linting the same files as CI
npm run lint:md

# Check if .gitignore is excluding files CI sees
git ls-files '*.md' | wc -l

# Verify no unstaged changes
git status

# Try exact CI command
npx markdownlint-cli2 '**/*.md' '!node_modules' '!lib'
```

**Common Causes:**

- Unstaged markdown files
- `.gitignore` differences
- Different markdownlint-cli2 versions

---

### When to Escalate

Escalate if:

- Auto-fix produces invalid markdown
- Linting rules conflict with project style
- CI failing but local passing consistently
- Need to change linting configuration

**Escalation Contact:**

- Repository maintainer
- DevOps team (for CI issues)

## Post-Procedure

After completion:

- [ ] All markdown files pass linting
- [ ] Changes committed and pushed
- [ ] CI lint workflow passes
- [ ] No documentation rendering issues

## Quick Reference

### Essential Commands

```bash
# Check errors
npm run lint:md

# Auto-fix everything
npm run lint:md -- --fix

# Fix specific directory
npx markdownlint-cli2 'docs/guides/**/*.md' --fix

# Fix specific file
npx markdownlint-cli2 docs/guides/file.md --fix

# Count remaining errors
npm run lint:md 2>&1 | grep -c "MD0"

# Commit fixes
git add '*.md' 'docs/**/*.md'
git commit -m "chore: fix markdown linting errors"
```

### Configuration

Linting configuration in `package.json` scripts:

```json
{
  "scripts": {
    "lint:md": "markdownlint-cli2 '**/*.md' '!node_modules' '!lib'"
  }
}
```

This project uses the default markdownlint rules. If you need to customize rules, you can create a `.markdownlintrc` or `.markdownlint.json` file in the project root.

## Notes

**Important Notes:**

- Auto-fix is safe - it won't change content, only formatting
- Always review `git diff` before committing
- Journal files in `docs/.journal/` are gitignored - lint errors OK
- Some errors can't be auto-fixed (MD029 ordered lists)

**Gotchas:**

- MD029 (ordered list) requires manual fix - choose consistent style
- Auto-fix adds a LOT of blank lines - this is correct!
- Markdown rendering may differ from linting rules - trust the linter
- CI runs on ALL markdown including those you didn't change

**Related Procedures:**

- [CI/CD Health Check](./ci-cd-health-check.md) - for checking lint workflow status
- [Prepare Release](./prepare-release.md) - linting is part of release preparation

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-10-17 | @tnez | Initial creation |
