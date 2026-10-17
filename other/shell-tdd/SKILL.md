---
name: shell-tdd
description: Shell-based TDD test harness patterns — pass/fail counters, common assertions,
  set -e gotchas, and exit code conventions for bash test scripts
type: reference
version: 1.0.0
category: development
capabilities:
- shell_test_harness
- bash_assertions
- tdd_shell_patterns
tools:
- Bash
- Read
- Edit
related_skills:
- tdd-obra
- gitignore-scaffold
- testing-tdd-london
requires: []
see_also: []
tags: []
---

# Shell TDD Test Harness

## Quick Start

Shell TDD scripts follow a simple pattern: counter functions, if-block assertions,
and `exit $FAIL` for CI integration. The critical rule is **never use `(( var++ ))`
with `set -e`** — use `var=$((var + 1))` instead.

## Template

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); echo "  PASS: $1"; }
fail() { FAIL=$((FAIL + 1)); echo "  FAIL: $1"; }

echo "=== Suite: <name> ==="

# --- AC1: <description> ---
echo ""
echo "--- AC1: <description> ---"

if <check>; then
    pass "<what passed>"
else
    fail "<what failed>"
fi

# --- Summary ---
echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
exit $FAIL
```

## Common Assertions

```bash
# File exists
if [ -f "$path" ]; then pass "file exists"; else fail "file missing"; fi

# Directory exists
if [ -d "$path" ]; then pass "dir exists"; else fail "dir missing"; fi

# File contains text
if grep -q "pattern" "$file"; then pass "pattern found"; else fail "pattern missing"; fi

# Git ignores file
if git check-ignore -q "$path"; then pass "ignored"; else fail "not ignored"; fi

# Command succeeds
if command_here; then pass "command ok"; else fail "command failed"; fi

# Command output matches expected value
if [ "$(command)" = "expected" ]; then pass "output matches"; else fail "output mismatch"; fi

# File is not empty
if [ -s "$path" ]; then pass "file has content"; else fail "file empty"; fi

# String variable is non-empty
if [ -n "$var" ]; then pass "var set"; else fail "var empty"; fi
```

## Gotchas

### 1. Counter increment with `set -e` (CRITICAL)

```bash
# BROKEN — exits script when PASS=0 because (( 0 )) returns exit code 1
(( PASS++ ))

# CORRECT — arithmetic substitution always succeeds
PASS=$((PASS + 1))
```

Why: `(( expr ))` returns exit code 1 when the expression evaluates to 0.
When `PASS=0`, `(( PASS++ ))` evaluates `0` (the pre-increment value), which is
falsy, so `set -e` kills the script on the very first pass.

### 2. `set -e` and conditionals

`set -e` does **not** exit when a failing command is inside an `if` condition,
`while` condition, or the left side of `&&`/`||`. Always wrap checks that might
fail in `if` blocks rather than running them bare.

```bash
# BROKEN — exits script if grep finds nothing
grep -q "pattern" "$file"

# CORRECT — if block suppresses set -e for the condition
if grep -q "pattern" "$file"; then pass "found"; else fail "missing"; fi
```

### 3. `set -u` and optional variables

Use `${var:-default}` for variables that may be unset. Bare `$var` with `set -u`
exits immediately if `var` is not defined.

### 4. `set -o pipefail` and pipes

The pipe exit code is the rightmost non-zero exit. A `grep | head` where grep
finds nothing will fail the whole pipe. Wrap in `if` when failure is expected.

## Exit Code Convention

`exit $FAIL` — zero means all tests passed, non-zero equals the failure count.
This integrates directly with CI: any non-zero exit fails the build.
