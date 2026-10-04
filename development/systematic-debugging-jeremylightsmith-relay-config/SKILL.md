---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask the real issue.

**Core principle:** ALWAYS find the root cause before attempting a fix. Symptom fixes are failure.

## The Iron Law

    NO FIX WITHOUT ROOT-CAUSE INVESTIGATION FIRST

If you haven't completed Phase 1, you cannot propose a fix.

## When to Use

Any technical issue: test failures, production bugs, unexpected behavior, performance
problems, compile/build failures, integration issues. **Especially** under time pressure,
when "one quick fix" seems obvious, or after a previous fix didn't work. Don't skip because
the issue "seems simple" — simple bugs have root causes too, and systematic is *faster* than
guess-and-check thrashing.

## The Four Phases

Complete each phase before the next.

### Phase 1 — Root-cause investigation (before ANY fix)
1. **Read the error carefully.** ExUnit assertion diffs, stack traces, `** (Module)` errors,
   line/file refs — they often contain the exact answer. Don't skim past warnings.
2. **Reproduce consistently.** Can you trigger it reliably? `mix test path/to_test.exs:LINE`.
   Not reproducible → gather more data, don't guess.
3. **Check recent changes.** `git diff`, recent commits, new deps, config/env differences.
4. **Gather evidence across boundaries** in multi-component flows (LiveView → context →
   Ecto → DB; or a GenServer/PubSub pipeline). Add temporary `IO.inspect(label: ...)` or
   `dbg()` at each boundary, run once, and see WHERE the data first goes wrong — then
   investigate that component, not the symptom site.
5. **Trace the bad value backward.** Where does it originate? What passed it in? Keep tracing
   up to the source. Fix at the source, not where it surfaced.

### Phase 2 — Pattern analysis
- Find similar **working** code in this codebase. What works that's like the broken thing?
- If following a pattern/reference, read it COMPLETELY — don't skim.
- List every difference between working and broken, however small ("that can't matter" is
  where the bug hides). Note the config/env/assumptions each relies on.

### Phase 3 — Hypothesis and testing
- State ONE hypothesis explicitly: "I think X is the root cause because Y."
- Test it with the SMALLEST possible change — one variable at a time.
- Worked? → Phase 4. Didn't? → form a NEW hypothesis; don't stack fixes on top.
- Don't understand something? Say so and investigate — don't pretend.

### Phase 4 — Implementation
1. **Write a failing test first** that reproduces the bug (use the `test-driven-development`
   skill). You must have it before fixing — it proves the fix and prevents regression.
2. **One fix, addressing the root cause.** No "while I'm here" improvements, no bundled
   refactoring.
3. **Verify** (use `verification-before-completion`): the new test passes, nothing else
   broke, `mix precommit` is green.
4. **If the fix doesn't work:** STOP. Count your attempts. < 3 → return to Phase 1 with the
   new information. **≥ 3 failed fixes → stop guessing and question the architecture** (next).

### When 3+ fixes fail — question the architecture
If each fix reveals new coupling/shared state elsewhere, or every fix needs "massive
refactoring," or each fix spawns new symptoms — that's not a failed hypothesis, it's the
wrong design. Stop and discuss with the user whether the pattern itself is sound before
attempting fix #4.

## Red Flags — STOP and return to Phase 1

"Quick fix now, investigate later" · "just try changing X and see" · "add several changes,
run tests" · "it's probably X, let me fix that" · "I don't fully get it but this might work"
· proposing fixes before tracing data flow · "one more fix attempt" after 2+ failures · each
fix uncovering a new problem in a different place.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Issue is simple, skip the process" | Simple bugs have root causes too; the process is fast for them. |
| "Emergency, no time" | Systematic is faster than guess-and-check thrashing. |
| "Try this first, investigate later" | The first fix sets the pattern. Do it right from the start. |
| "I'll test after confirming the fix" | Untested fixes don't stick. Test-first proves it. |
| "Multiple fixes at once saves time" | You can't isolate what worked; it causes new bugs. |
| "I see the problem, let me fix it" | Seeing the symptom ≠ understanding the root cause. |

## Related skills
- `test-driven-development` — for the Phase 4 failing test.
- `verification-before-completion` — to confirm the fix before claiming success.
