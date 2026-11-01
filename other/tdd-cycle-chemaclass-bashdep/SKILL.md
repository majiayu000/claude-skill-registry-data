---
name: tdd-cycle
description: Run a complete RED -> GREEN -> REFACTOR cycle for a single test
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# TDD Cycle

Execute a complete RED -> GREEN -> REFACTOR cycle for one test.

## Workflow

### 1. Verify Task File

Check for `.tasks/YYYY-MM-DD-*.md`. If missing for a non-trivial change,
create one before proceeding.

### 2. RED - Write Failing Test

1. Show the test inventory from the task file; ask which test to implement
2. Read the surrounding tests in `tests/unit/bashdep_test.sh` to match style:
    - Pure-logic test (no filesystem) → add near the top
    - Filesystem test → add near the bottom; use `$TEST_DIR` and the
      `_seed_lock` / `_seed_installed` helpers
3. Reset `BASHDEP_*` globals in the test body if it depends on a mode flag
4. Run: `lib/bashunit tests --filter <test_name>` - **must fail**
5. Verify the failure is for the RIGHT reason (assertion mismatch, not
    syntax error or missing function)
6. Update the task file: current red bar + logbook entry

### 3. GREEN - Make It Pass

1. Write **minimal** code in `bashdep` - only enough to satisfy THIS test
2. Run: `lib/bashunit tests --filter <test_name>` - **must pass**
3. Run the full suite: `make test` - nothing else regressed
4. Update the task file: tick the test + logbook entry

### 4. REFACTOR - Improve Code

1. Improve readability, naming, extract duplication - no behavior changes
2. Run `make test` after each change
3. Quality checks: `make sa && make lint`
4. Update the task file with refactoring notes

### 5. Next Test

Show the updated test inventory. Ask whether to continue or stop.

## Critical Rules

- **Never skip RED** - always verify the test fails first
- **Minimal code in GREEN** - resist scope creep
- **All tests green during REFACTOR** - revert immediately if broken
- **Bash 3.2+** - see `.claude/rules/bash-style.md`
- **Honor modes** - any new mutating code must respect
  `BASHDEP_DRY_RUN`, `BASHDEP_SILENT`, `BASHDEP_VERBOSE`, `BASHDEP_FORCE`
