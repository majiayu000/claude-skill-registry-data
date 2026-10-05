---
name: debugging-patterns
description: "Isolate root causes through structured evidence gathering, pattern analysis, hypothesis testing (max 3 at a time, highest confidence first), and fix validation with a reproducing test before implementation. Use when any verification step fails, tests break, or debugging a reported bug. This skill MUST be consulted because symptom-fixing creates new bugs, and unbounded hypothesis testing causes tunnel vision; root cause must be proven before any fix attempt."
allowed-tools: Bash, Read, Grep, Glob, TaskCreate, TaskList, TaskUpdate
context: fork
agent: general-purpose
---

# Debugging Patterns

## Contract

Iron law: **find and prove the root cause before attempting any fix; a symptom fix is a failure.** Invoked by `/flow:debug` Phases 1–3 (evidence → hypotheses → fix), by `/flow:start` and `/flow:resolve` on demand whenever a build, test, server-start, smoke, E2E, or visual step fails (no `bug` label required), and by the `error-handler-inspector` agent. Returns the confirmed root cause with evidence, the hypothesis table with each result, a reproducing test that failed before the fix and passes after, and a full-suite run with no regressions. Permitted skips: none — a clear error message shortens the investigation (one or two hypotheses) but never removes the reproducing test.

## Evidence Before Theory

Read the full error message and stack trace first — never skim, never start with "let me understand the code." Then `git log --oneline -10` and `git diff HEAD~3..HEAD --stat` for recent changes. Reproduce the failure; if you cannot reproduce it you cannot verify a fix. Trace backward from the error, checking inputs, API responses, and config values at each boundary, and only then read code.

## Hypothesis Discipline

Form at most `debugging.maxHypotheses` (default 3) hypotheses at a time. More means insufficient evidence — return to evidence gathering. Create one task per hypothesis:

```
TaskCreate("Hypothesis 1: {theory}", "Confidence: High\nTest: {specific test}\nEvidence: {what points here}")
```

Rules:
- Test highest confidence first, ONE at a time — never change two things simultaneously.
- `TaskUpdate(status: "in_progress")` before testing; `TaskUpdate(status: "completed")` after, recording confirmed or disproven. A disproven hypothesis is progress.
- Write all hypotheses down before testing any, and actively seek disconfirming evidence for the leading one.
- Before blaming the last change, check whether the bug predates it (`git stash && test`). Check simple causes (typo, wrong variable, off-by-one) before elaborate ones.

Display the table:

| # | Hypothesis | Confidence | Test | Result |
|---|-----------|------------|------|--------|

## Fix Validation

Write a test that reproduces the bug BEFORE fixing. If it does not fail, you have not found the bug.

1. Write the failing test; confirm it fails for the right reason.
2. Implement the minimal fix.
3. Confirm the test passes.
4. Run the full suite — no regressions.

Track as `TaskCreate("Fix validation", ...)`; `TaskList` must show every hypothesis and the fix task completed before returning.

## Verification Failure Mode

When invoked because a verification step failed (build, test, server start, smoke, E2E, visual): read the output fully, form one or two hypotheses, fix, re-verify. Iteration ceilings belong to the caller (`closedLoop.maxBuildIterations`, `closedLoop.maxServerRetries`, `closedLoop.maxDebugIterations`). The user never has to supply logs or say what went wrong — you have the same output.

## Stop Conditions

| Trigger | Action |
|---------|--------|
| 3+ failed fix attempts | Stop fixing forward; the problem is architectural. Return to EXPLORE. |
| Cannot explain current behavior | Do not guess. Add logging and assertions; investigate more. |
| Tunnel vision (three tests of one theory with no new evidence) | Step back; list what you KNOW vs what you ASSUME. |
| Fix works but you cannot explain why | Revert. An unexplained fix is a time bomb. |

## Not Fixes

A try-catch that hides the error, "quick fix now, proper fix later", or "probably a race condition" without timing evidence are symptom fixes. "I know what's wrong" still requires proof — if you are right it takes thirty seconds. "It works on my machine" means the bug is in the environment difference; investigate that.
