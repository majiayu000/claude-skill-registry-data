---
name: lint
description: Run the linter and formatter check. Use before opening a PR to ensure code style compliance. Reads lint command from claude/build.md.
---

# Lint Skill

Run linter and formatter, fix auto-fixable issues.

## Protocol

### 1. Read lint command
Read `claude/build.md` for the lint and format commands.

### 2. Run formatter check (non-destructive)
```bash
# Example: npx biome check . 2>&1 | tail -30
# Example: black --check . 2>&1 | tail -20
```

### 3. Run linter
```bash
# Example: npx eslint . --max-warnings 0 2>&1 | tail -40
# Example: ruff check . 2>&1 | tail -30
```

### 4. Auto-fix safe issues
```bash
# Example: npx biome check --write . 2>&1 | tail -20
# Example: black . && ruff check --fix . 2>&1 | tail -20
```

### 5. Review remaining issues
For issues that can't be auto-fixed:
- Understand the rule being violated
- Fix the root cause (not by disabling the rule)
- Only disable a rule if you understand exactly why it's a false positive

### 6. Re-run to confirm clean
```bash
# Run the same check commands again — must exit 0
```

### 7. Report
```
Lint: PASS — 0 errors, 0 warnings
Format: PASS
```
or
```
Lint: FAIL — 3 errors, 5 warnings
  - error: ... (fixed)
  - warning: ... (fixed)
  Remaining: 0 (all resolved)
```

## Rules
- NEVER suppress a lint rule without a written justification in a comment
- NEVER "fix" lint by converting errors to warnings
- Pre-existing lint issues: document them, do NOT fix unrelated issues
- Only fix lint issues introduced by the current change (unless asked to do a lint pass)
