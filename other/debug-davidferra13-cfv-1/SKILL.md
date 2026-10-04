---
name: debug
description: Systematic 4-phase debugging. NO fixes without root cause investigation first. Prevents thrashing and random guessing.
user-invocable: true
---

# Systematic Debugging

**Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Complete Phase 1 fully before proposing any solution.

## Phase 1: Root Cause Investigation

1. **Read the exact error.** Quote it verbatim. Do not paraphrase.
2. **Reproduce consistently.** Identify the exact steps that trigger it every time.
3. **Review recent changes.** `git log --oneline -10`. What changed in the last 10 commits near this area?
4. **Gather evidence across boundaries.** Check: server logs, browser console, DB query output, network tab. Pick up facts, not hunches.

Do NOT move to Phase 2 until you can state: "The error is X, it happens when Y, it started after Z."

## Phase 2: Pattern Analysis

1. Find a working example in the codebase that does the same thing (same pattern, same flow, same table).
2. Diff the working code against the broken code. List specific differences.
3. Identify which difference is the most likely cause.

## Phase 3: Hypothesis and Testing

1. State your hypothesis: "The bug is caused by [specific thing] because [evidence]."
2. Design a minimal test: one change, one verification.
3. Do NOT make multiple simultaneous changes. One at a time.

## Phase 4: Fix and Verify

1. Write a failing test first (if the bug is testable).
2. Apply the single targeted fix.
3. Verify: run the relevant test or Playwright flow. Read full output.
4. Confirm no regressions in adjacent code.

## Red Flags - Stop if You're Doing These

- Trying a fix before completing Phase 1
- Making multiple changes at once
- "Just trying" something without evidence
- Reverting and retrying the same approach (3-strike rule applies)

## Escalation

After 3 failed fix attempts: stop, commit partial progress, report to user. Do not continue thrashing. The architecture itself may be flawed - that requires a different kind of decision, not more debugging.

For hard architectural bugs: call `opus-advisor` with "Think deeply and use extended thinking."
