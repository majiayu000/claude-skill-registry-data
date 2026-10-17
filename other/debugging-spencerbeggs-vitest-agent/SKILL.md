---
name: debugging
description: Use when tests are failing, when investigating flaky or persistent failures, or when a failure signature needs systematic diagnosis through vitest-agent's test_history, test_errors, and failure_signature_get surfaces.
---

# Debugging Test Failures

Systematic approach to diagnosing and fixing test failures using
MCP tools.

## Step 1: Classify the Failure

Use `test_history` to understand the failure pattern:

- **New failure:** First time this test failed. Likely caused by
  a recent change
- **Persistent failure:** Failed multiple runs in a row. Likely a
  real bug or environment issue
- **Flaky test:** Intermittent pass/fail. Could be timing,
  ordering, or shared state

## Step 2: Examine the Error

Use `test_errors` to search for the specific error:

- Search by error name to find similar failures across tests
- Check if the same error appears in other projects
- Look at the diff (expected vs received) for assertion failures

## Step 3: Find Related Tests

Use `test (action: for_file)` to find all tests that cover the file
containing the failure. This helps you:

- Understand the test surface for the affected code
- Find tests that might be affected by the same bug
- Identify missing test coverage

## Step 4: Check Coverage Context

Use `test_coverage` to see:

- Which lines in the failing file are uncovered
- Whether the failure is in a well-tested or poorly-tested area
- Coverage trends (is coverage improving or degrading?)

## Step 5: Document Findings

Use `note (action: create)` to record:

- Root cause analysis
- Steps to reproduce
- Fix strategy
- Any workarounds applied

Pin important notes with `note (action: update)` so they persist across
sessions.

## Step 6: Verify the Fix

1. Run the specific failing test:
   `run_tests({ files: ["path/to/failing.test.ts"] })`
2. Run the full suite to check for regressions: `run_tests({})`
3. Check `test_trends` to confirm coverage direction

Always use the `run_tests` MCP tool instead of running vitest via
Bash. It uses Vitest's programmatic API, so results persist to the
database and all query tools reflect the latest run immediately.
