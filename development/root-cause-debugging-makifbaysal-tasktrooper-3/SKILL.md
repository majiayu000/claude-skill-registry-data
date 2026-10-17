---
name: root-cause-debugging
category: quality
description: Root-cause debugging discipline. Use when a test, build or pipeline fails, behaviour does not match expectations, a bug task arrives, or a task comes back in need_revision — before proposing any fix.
source: obra/superpowers (MIT), adapted
---
# Root-Cause Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find the root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Use this for ANY technical issue: a task returned to need_revision, a failing test, a red pipeline, unexpected behavior. Use it ESPECIALLY under time pressure — systematic is faster than guess-and-check thrashing.

## The Four Phases

Complete each phase before the next.

### Phase 1 — Build a feedback loop, then investigate

This is the skill: before anything else, name ONE command you have already run that goes red on THIS symptom — a failing test, a `curl` against the running service, a `browser_read_dom` that doesn't find what it should, a replayed payload. No loop, no hypothesis. If none exists, write the smallest one that reproduces it (a test is the default; a `curl`/DOM read is the fallback when the bug is only visible live) before reading another line of code.

1. **Read the feedback completely**: the reviewer/QA/pipeline comment on the task, the full error output, stack traces, exact files/lines/messages. They often contain the exact answer.
2. **Reproduce consistently** in the task workspace with the loop from above: does it happen every time? Not reproducible → gather more data, don't guess.
3. **Check recent changes**: git diff, recent commits on the task branch, config changes.
4. **Stage/prod symptom** (a runtime error, not a local failure): before reading code, `get_environment` for the environment, `list_runtime_errors` with `new: true` to see whether the group started with the latest deploy, then `query_runtime_logs` with `text:` set to the error message. You hold these tools; use them before guessing from the code alone.
5. **Multi-component systems** (API → service → database): add diagnostic logging at each component boundary — what enters, what exits — run once, and locate WHICH layer breaks before touching anything. Tag every line you add with a unique marker, e.g. `[DEBUG-a4f2]`, so cleanup is one `grep_code` for the tag before you finish — an untagged debug log left behind is a review finding.
6. **Trace the bad value backward** from where the error appears to where it originates. Fix at the source, not at the symptom.

### Phase 2 — Pattern analysis
- Find working examples of the same pattern in the codebase (codebase_search, grep_code).
- Read the reference implementation completely — don't skim.
- List every difference between working and broken; don't assume "that can't matter".

### Phase 3 — Hypothesis and testing
- List 3–5 hypotheses, ranked by likelihood. Each must be falsifiable: "If X is the cause, then changing Y will make the symptom disappear."
- Test the top one with the SMALLEST possible change. One variable at a time.
- Didn't work? Move to the next ranked hypothesis. Do NOT stack more fixes on top.

### Phase 4 — Implementation
1. Write a failing test that reproduces the issue (see tdd-workflow).
2. Implement the single fix that addresses the root cause. No bundled refactoring.
3. Verify: the test passes, no other test breaks, the original symptom is gone.
4. Address EVERY point from the revision comment explicitly — partial fixes come straight back.

## Was the test red before you started?

Before fixing a test you didn't write that's failing on your branch, check whether it failed on the base commit too: `git stash -u && <focused test command>; git stash pop`. If it was already red there, it's pre-existing, not something your change broke.
- **Small and adjacent to your change** → fix it in its own commit, separate from your feature commit.
- **Otherwise** → one comment naming the test, the failure, and the base commit SHA: that's a blocker a person must see, not something to silently carry or silently fix.

A regression that appeared somewhere in recent history (not clearly your change): `git bisect run <focused test>` to find the exact commit before theorizing about the cause.

## Test-failure triage

A test fails on code you touched: decide, don't assume. Did your change touch what this test covers?
- **Yes, and the test's expectation is still correct** → your code has a bug. Fix the code.
- **Yes, and the behavior genuinely changed on purpose** → the test is outdated. Update it to match, and say so in your closing message — never weaken or delete it to make it pass without that explicit call.

## When you don't know

If after Phase 1–3 you genuinely cannot identify the mechanism, say so plainly — "I don't understand why X happens" — rather than proposing a fix you don't believe in. Before declaring "no root cause": 95% of "no root cause" conclusions are incomplete investigation, so document exactly what you checked and where it dead-ended, add defensive handling/logging at the boundary you suspect, and say in your closing message what the next investigator should try first.

## The 3-Fix Rule

If 3 fixes have failed, STOP. Each fix revealing a new problem elsewhere means the architecture or approach is wrong, not the code. Question the pattern — add a task comment describing the architectural concern instead of attempting fix #4.

## Close

The root cause — not just "fixed it" — goes in your closing message: what broke, why, and the guard test that proves it. That message becomes the commit body the next debugger reads when this breaks again.

## Red Flags — STOP and return to Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "It's probably X, let me fix that"
- Proposing solutions before tracing data flow
- Multiple changes at once
- "One more fix attempt" after 2+ failures
- A debug log left in the diff without its `[DEBUG-xxxx]` tag removed

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, no need for process" | Simple issues have root causes too; the process is fast for them. |
| "Emergency, no time" | Systematic debugging is faster than thrashing. |
| "I see the problem, let me fix it" | Seeing symptoms is not understanding root cause. |
| "Multiple fixes at once saves time" | You can't isolate what worked, and you create new bugs. |
| "I'll write the test after the fix works" | Untested fixes don't stick. Test first proves it. |
