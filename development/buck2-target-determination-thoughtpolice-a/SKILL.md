---
name: buck2-target-determination
description: This skill should be used when determining which Buck2 targets are affected by code changes for incremental builds and tests. Use this when users ask to test/build changed code, find affected targets, or run incremental workflows with jj revisions.
---

# Buck2 Target Determination

## Overview

Target determination identifies which Buck2 targets are affected by code changes between two jj revisions. This enables incremental workflows that only build/test what changed, dramatically reducing build times (often 10-100x faster than full builds).

## When to Use This Skill

Use this skill when:
- User wants to "test what changed" or "test my changes"
- User asks to "build only affected targets"
- User requests "incremental build/test"
- Setting up CI/CD workflows that should only test affected code
- Analyzing impact of changes before committing
- User mentions `quicktd` or target determination

## How Target Determination Works

The `quicktd` tool:
1. Accepts two jj revsets (e.g., `'@-'` and `'@'`)
2. Computes file changes between those revisions
3. Builds Buck2 target graphs at both revisions
4. Identifies targets whose BUILD files or sources changed
5. Outputs affected targets to a file path

**Critical**: Always use the `root//` cell prefix with quicktd to avoid ambiguous cell references.

## Basic Usage Pattern

```bash
# Find targets affected between parent (@-) and current (@)
TARGETS=$(buck2 run root//buck/tools/quicktd -- '@-' '@' depot//src/...)

# Build affected targets
buck2 build @$TARGETS

# Test affected targets
buck2 test @$TARGETS
```

**Why at-file syntax (`@$TARGETS`)?** Target lists can be extremely large (thousands of targets), exceeding command-line length limits. At-file syntax loads targets from a file.

## Common Revset Patterns

### Development Workflows

```bash
# Changes in current commit (most common)
buck2 run root//buck/tools/quicktd -- '@-' '@' depot//src/...

# Changes since trunk
buck2 run root//buck/tools/quicktd -- 'trunk()' '@' depot//src/...

# Last 3 commits
buck2 run root//buck/tools/quicktd -- '@---' '@' depot//src/...

# Specific commit range
buck2 run root//buck/tools/quicktd -- 'abc123' 'def456' depot//src/...
```

### CI/CD Workflows

```bash
# Changes in pull request (compared to main)
buck2 run root//buck/tools/quicktd -- 'trunk()' '@' depot//...

# Full repository scan
buck2 run root//buck/tools/quicktd -- 'root()' '@' depot//...
```

### Scope Limiting

```bash
# Only specific directory
buck2 run root//buck/tools/quicktd -- '@-' '@' depot//src/myproject/...

# Multiple directories
buck2 run root//buck/tools/quicktd -- '@-' '@' depot//src/... depot//tools/...
```

## Complete Workflow Examples

### Pre-Commit Testing

```bash
# 1. Make changes
jj new -m "feat: implement feature"
# ... edit files ...

# 2. Find affected targets
TARGETS=$(buck2 run root//buck/tools/quicktd -- '@-' '@' depot//src/...)

# 3. Build affected targets
buck2 build @$TARGETS

# 4. Test affected targets
buck2 test @$TARGETS

# 5. If passing, commit
jj commit -m "feat: implement feature"
```

### Impact Analysis

```bash
# See what targets are affected
TARGETS=$(buck2 run root//buck/tools/quicktd -- '@-' '@' depot//src/...)

# Count affected targets
wc -l $TARGETS

# Show affected targets
cat $TARGETS

# Find which are tests
buck2 query "kind('.*_test', set(@$TARGETS))"

# Find which are binaries
buck2 query "kind('.*_binary', set(@$TARGETS))"
```

## Helper Script Usage

Use `scripts/quicktd_helper.py` for simplified invocations:

```bash
# Interactive mode - prompts for revsets
python3 scripts/quicktd_helper.py

# Quick patterns
python3 scripts/quicktd_helper.py --pattern current    # '@-' to '@'
python3 scripts/quicktd_helper.py --pattern trunk      # 'trunk()' to '@'
python3 scripts/quicktd_helper.py --pattern full       # 'root()' to '@'

# Custom revsets
python3 scripts/quicktd_helper.py --from '@---' --to '@' --scope depot//src/myproject/...

# Auto-build affected targets
python3 scripts/quicktd_helper.py --pattern current --build

# Auto-test affected targets
python3 scripts/quicktd_helper.py --pattern current --test

# Both build and test
python3 scripts/quicktd_helper.py --pattern trunk --build --test
```

The helper provides:
- Better error messages
- Target count and preview
- Optional auto-build/test
- Common pattern shortcuts

## Troubleshooting

### "No targets affected"

Possible causes:
- No files changed (check `jj diff`)
- Changes only to files not in any BUILD target
- Scope too narrow (expand from `depot//src/myproject/...` to `depot//src/...`)
- Files not committed to jj (Buck2 only sees committed files)

Solution:
```bash
# Check what changed
jj diff

# Verify files are committed
jj status

# Expand scope
buck2 run root//buck/tools/quicktd -- '@-' '@' depot//...
```

### "Could not find cell" error

The `root//` prefix is missing. Always use:

```bash
# ✓ Correct
buck2 run root//buck/tools/quicktd -- ...

# ✗ Wrong
buck2 run //buck/tools/quicktd -- ...
```

### Large target lists cause failures

Use at-file syntax (`@filename`) instead of passing targets directly:

```bash
# ✓ Correct
TARGETS=$(buck2 run root//buck/tools/quicktd -- '@-' '@' depot//src/...)
buck2 test @$TARGETS

# ✗ Wrong (may exceed command-line limits)
buck2 test $(cat $TARGETS)
```

## Performance Benefits

Real-world example:
```bash
# Without target determination (builds everything)
time buck2 test depot//src/...
# → 1847 actions, 15m 23s

# With target determination (1 file changed)
TARGETS=$(buck2 run root//buck/tools/quicktd -- '@-' '@' depot//src/...)
time buck2 test @$TARGETS
# → 12 actions, 8.3s
# → 111x faster!
```

## Best Practices

1. **Always use `root//` prefix** - Prevents cell reference errors
2. **Use at-file syntax** - Required for large target lists
3. **Scope appropriately** - Balance coverage vs speed
4. **Commit before testing** - Buck2 only sees committed files
5. **Cache the output** - Store `$TARGETS` for multiple commands
6. **Check target count** - `wc -l $TARGETS` to verify results
7. **Run quality tests separately** - `depot//buck/tests/...` aren't in quicktd scope

## Resources

### scripts/quicktd_helper.py
Python helper script that wraps quicktd with common patterns and better output formatting.

### references/revset_patterns.md
Comprehensive guide to jj revset patterns for use with quicktd.
