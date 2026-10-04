---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
---

# Systematic Debugging

## Overview

**Core principle:** find the root cause before attempting a fix. A fix that only addresses the symptom is a failure, even if the symptom goes away.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Use this for any technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures. Use it *especially* under time pressure, when a "quick fix" looks obvious, or after a previous fix didn't work — those are exactly the conditions where guessing feels fastest and costs the most.

## The Four Phases

Complete each phase before moving to the next.

### Phase 1: Root Cause Investigation

1. **Read the error completely.** Full stack trace, exact message, line numbers, error codes — don't skim past it.
2. **Reproduce it consistently.** Exact steps, does it happen every time? If it's not reproducible, gather more data before guessing.
3. **Check recent changes.** `git diff`, `git log`, recent dependency bumps, config or environment changes.
4. **In a multi-component flow (e.g. `client` → `agent` API → Postgres/Sequelize → Kafka → `consumer`), add diagnostic logging at each boundary** before proposing a fix: what enters this component, what leaves it, is config/env actually propagating. Run once to see *where* it breaks, then investigate that specific component — don't guess which layer is at fault.
5. **Trace data flow backward** when the error surfaces deep in a call stack: where did the bad value originate, what called this with that value, keep tracing until you reach the source. Fix at the source, not where the symptom happened to surface.

### Phase 2: Pattern Analysis

- Find a working example of similar code in the same codebase — what does it do differently?
- If following an existing pattern, read the reference implementation completely, not just the parts that look relevant.
- List every difference between the working and broken cases, however small it seems.
- Understand what the broken code depends on: config, environment, assumptions about call order.

### Phase 3: Hypothesis and Testing

- State a single hypothesis clearly: "I think X is the root cause because Y."
- Test it with the smallest possible change — one variable at a time.
- Confirmed? Move to Phase 4. Not confirmed? Form a new hypothesis — don't stack another fix on top of the failed one.
- If you genuinely don't understand something, say so rather than guessing forward.

### Phase 4: Implementation

1. **Write a failing test reproducing the bug first** — see the `test-driven-development` skill in `superpowers/` for the cycle. This is required before the fix, not optional.
2. **Implement one fix addressing the root cause.** No bundled refactoring, no "while I'm here" changes.
3. **Verify**: does the new test pass, do other tests still pass, is the original symptom actually gone? See `verification-before-completion` in `superpowers/` before claiming it's fixed.
4. **If the fix doesn't work:** stop. Count attempts. Fewer than 3 → return to Phase 1 with the new information. **3 or more failed fixes on the same issue means the architecture is the problem, not the fix** — stop attempting patches and raise the architectural question explicitly instead of trying a 4th fix.

## Red Flags — Stop and Return to Phase 1

- "Quick fix for now, investigate properly later"
- "Let me just try changing X and see"
- Proposing a fix before tracing where the bad value came from
- Changing several things at once and running the tests to see what sticks
- "One more fix attempt" after two have already failed
- Each attempted fix reveals a new problem somewhere else — that's an architecture signal, not a debugging signal

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Issue is simple, skip the process" | Simple bugs have root causes too; the process is fast when the bug really is simple |
| "Emergency, no time to investigate" | Guess-and-check thrashing is slower than one focused investigation pass |
| "I'll write the test after confirming the fix" | An untested "fix" is just a guess that happened to make the symptom disappear once |
| "Multiple fixes at once saves time" | You can't tell which one worked, and you may have introduced a new bug |

## Quick Reference

| Phase | Key activity | Exit condition |
|---|---|---|
| 1. Root Cause | Read errors, reproduce, check diffs, trace data flow | You understand *what* and *why* |
| 2. Pattern | Compare against a working example | Differences are identified |
| 3. Hypothesis | One theory, minimal test of it | Confirmed, or a new hypothesis |
| 4. Implementation | Failing test → fix → verify | Bug resolved, full suite green |

95% of "there's no root cause, it's just flaky/environmental" conclusions turn out to be an incomplete Phase 1. Before accepting that verdict, make sure the investigation was actually exhausted.
