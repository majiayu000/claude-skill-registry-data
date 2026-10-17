---
name: interpret-test-failure
description: Read a Vitest error, query test_history for prior occurrences, extract assertion shape, and compute a failure signature. Use when a test fails and you need to decide whether it's a new failure, a recurring known one, or flaky.
---

# Interpret a test failure

When a test fails, do the following:

1. **Read the assertion message and stack trace.** The MCP `test_errors` tool returns these. Identify:
   - The assertion matcher (`toBe`, `toEqual`, `toThrow`, etc.)
   - The expected vs actual values (or value shapes)
   - The top non-framework stack frame (skip `node:internal`, `node_modules/vitest/`)
2. **Query history.** Call `test_history({ project: ..., subProject: ... })` to see if this test has failed before. Look for the test's `fullName` in the records.
3. **Get the failure signature.** Call `failure_signature_get({ hash })` if the error has a recorded signature. Recurring signatures collapse to one row; the `occurrence_count` tells you how often this failure has been seen.
4. **Classify.** Combine the history and signature data:
   - `new-failure` — first time seeing this test fail
   - `persistent` — failed in two or more consecutive runs
   - `flaky` — mixed pass/fail across recent runs
   - `recovered` — was failing, now passing
   - `stable` — consistently passing

Use the classification to decide your next action. New failures need a hypothesis. Persistent failures may indicate a real bug or a structural test issue. Flaky tests should not be silenced — investigate the source of nondeterminism.

## Reusable outside TDD

This skill is not TDD-specific. The fix-failing-test and flaky-triage workflows both use it.
