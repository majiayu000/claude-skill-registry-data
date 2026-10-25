---
name: markdownlint-validator
description: Guide for identifying and fixing markdownlint violations in Markdown files. Use this skill whenever asked to fix markdown linting errors, validate markdown files, resolve markdownlint violations, clean up markdown formatting issues, enforce markdown style rules, or correct any MD### rule failures. Always load this skill when working with .markdownlint config files or markdownlint-cli output.
---

# Markdownlint Validator

This skill covers identifying, fixing, and preventing markdownlint rule violations across Markdown files. It targets the [DavidAnson/markdownlint](https://github.com/DavidAnson/markdownlint) rule set (v0.x), used by VS Code, markdownlint-cli, and markdownlint-cli2.

## Quick Decision Guide

| Task | Load |
|---|---|
| Look up a specific rule (MD###), its parameters, or edge cases | `references/rules.md` |
| Configure `.markdownlint.json`, disable rules, inline suppression | `references/config.md` |
| Run linting against files in bulk | `scripts/validate.sh` |

Always read the relevant reference file before fixing non-trivial violations.

## Core Workflow

### 1. Get the violations

```bash
# Install markdownlint-cli if not present
npm install -g markdownlint-cli

# Lint files (outputs rule ID, file, line, description)
markdownlint "docs/**/*.md"

# Or use the validate script
bash scripts/validate.sh docs/
```

### 2. Triage

- Group violations by rule ID (e.g., all MD022 together).
- Check if the rule is **auto-fixable** (marked ✓ in `references/rules.md`) — fix those first with `markdownlint --fix`.
- Fix non-auto-fixable violations manually, one rule at a time.

### 3. Auto-fix what you can

```bash
markdownlint --fix "docs/**/*.md"
```

Auto-fixable rules include: MD004, MD005, MD007, MD009, MD010, MD011, MD012, MD014, MD018–MD021, MD023, MD026, MD029, MD030, MD031, MD032, MD034, MD037–MD039, MD044, MD047, MD053, MD054, MD058.

### 4. Fix remaining violations manually

Read `references/rules.md` for the relevant rule's description and fix pattern. The most common manual fixes are listed below.

### 5. Re-validate

```bash
markdownlint "docs/**/*.md"
```

Zero output = clean.

---

## Common Violations — Quick Fix

| Rule | Violation | Fix |
|---|---|---|
| MD009 | Trailing spaces | Remove trailing whitespace from each line |
| MD010 | Hard tabs | Replace `\t` with spaces (usually 2 or 4) |
| MD012 | Multiple consecutive blank lines | Collapse to one blank line |
| MD013 | Line too long (>80 chars) | Wrap text; or disable/configure the rule for long URLs |
| MD022 | Heading not surrounded by blank lines | Add blank line before and after every heading |
| MD031 | Fenced code block not surrounded by blank lines | Add blank line before ` ``` ` and after ` ``` ` |
| MD032 | List not surrounded by blank lines | Add blank line before and after every list block |
| MD040 | Fenced code block missing language | Add language tag: ` ```bash `, ` ```python `, ` ```text ` |
| MD041 | First line is not an H1 | Add `# Title` as first line, or disable if file is a fragment |
| MD047 | File does not end with newline | Add a trailing newline at end of file |
| MD051 | Broken link fragment (`#anchor`) | Match fragment exactly to heading text (lowercase, hyphens) |
| MD058 | Table not surrounded by blank lines | Add blank line before and after every table |

### Heading fragment format (MD051)

GitHub heading algorithm: lowercase, remove punctuation, spaces → hyphens, append `-N` if duplicate.

```markdown
## My Heading (2026)    →  #my-heading-2026
## API Reference        →  #api-reference
## API Reference        →  #api-reference-1  (duplicate)
```

---

## Inline Suppression

When a violation is intentional and cannot be restructured:

```markdown
<!-- markdownlint-disable MD013 -->
This line is intentionally very long because it contains a URL that cannot be split.
<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable-next-line MD033 -->
<details><summary>Click to expand</summary>
```

For file-wide suppression, use front matter or `.markdownlint.json`. See `references/config.md`.

---

## Debugging Checklist

| Symptom | Check |
|---|---|
| Violations persist after `--fix` | Rule is not auto-fixable; fix manually |
| MD013 fires on URLs | Set `"line-length": { "line_length": 120 }` or use `strict: false` |
| MD041 fires on partial/fragment files | Disable: `"first-line-heading": false` in config |
| MD033 fires on intentional HTML | Add to `allowed_elements` in config |
| Violations only in certain directories | Use `.markdownlint.json` in that subdirectory |
| Rule not in this skill's tables | Check `references/rules.md` for full rule list |
