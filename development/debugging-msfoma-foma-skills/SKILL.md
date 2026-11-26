---
name: debugging
description: >-
  Finds the root cause of a bug before fixing it. Use when something behaves unexpectedly, throws, fails a test, runs slow, or the user says "find out why". Not for a precisely diagnosed fix, test runs, reviews or tests-first work.
license: Apache-2.0
metadata:
  level: "method"
  uses: "tdd"
  agents: "explorer"
  tokens: "635"
---

Reproduce the bug with a fast check, find the root cause by testing one hypothesis at a time, then fix it and lock it with a test.

Uses: foma-skills:tdd (regression test), agent `explorer` (wide code search, model haiku; self-contained brief, answer ≤10 lines).

Path: a clear error with one suspect place → a one-command repro, fix, regression test, suite (skip shrinking and the hypothesis log); unclear, flaky, cross-module or after a failed fix → all steps. Say which path in one line.

## Steps
1. Read the full error and stack trace, then recent changes (`git log`, `git diff`). A search across many files (who calls X, where Y is set): delegate it to the explorer agent.
2. Build a fast loop that shows the bug: a failing test, script, curl or CLI run asserting the user's exact symptom. Run it and show it fail. No loop possible: list what you tried and ask the user for access, a captured artifact or permission to add instrumentation.
3. Reproduce and shrink: cut inputs, config and steps one at a time until every remaining part is needed. Confirm it is the user's bug, not a nearby one. Flaky: raise the failure rate (loop it, add load, pin time and seeds) before going on.
4. Hypothesise: state "If X is the cause, then changing Y will remove the bug / Z will worsen it". Test one at a time with the smallest probe: debugger or a targeted log tagged `[DEBUG-xxxx]`. Performance bug: measure a baseline first, then bisect.
5. Fix the root cause, one change. Write the regression test through foma-skills:tdd and see it fail before the fix and pass after. No honest seam for the test: say so in the report.
6. Re-run the loop from step 2, then the suite. Remove every `[DEBUG-` line (grep) and throwaway files.

## Rules
- No fix before a reproduction and a stated root-cause hypothesis; seeing the symptom is not knowing the cause.
- One change per attempt; a failed attempt is reverted, never built on.
- After 3 failed fixes stop, question the approach (shared state, coupling) and ask the user before attempt 4.
- Never "log everything and grep"; every probe tests a named prediction.
- Redact secrets from shown commands, logs and artifacts as `<REDACTED>`.

If the error surfaces deep in a call chain or you need to find which test pollutes state, read `references/tracing.md`.
If the bug is flaky, timing-dependent or a test sleeps for a fixed delay, read `references/flaky-timing.md`.

## Report
- Root cause (`file:line`) and the fix.
- Evidence: loop before and after, regression test, suite result.
- Not checked: <…>
