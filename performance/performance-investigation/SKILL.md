---
name: performance-investigation
description: Use when investigating slowness, high resource usage, timeouts, or any optimization request. Enforces measure-first performance work — profile, prove the bottleneck, fix, measure again. No optimization based on guesses.
---

# Performance Investigation

Goal: every performance claim comes with two numbers — before and after.

"It's probably the N+1 query" is a hypothesis, not a diagnosis. Optimizing
unmeasured code is guessing with extra steps.

## Steps

1. **Define the symptom as a number.**
   What is slow, how slow, under what conditions, and what would "fixed" mean?
   ("List endpoint takes 4.2s at 10k rows; target under 500ms.") If the user
   can't give a target, propose one.

2. **Measure before touching anything.**
   Profile, add timings, check query plans, reproduce under realistic data —
   whatever fits the stack. The goal is a **proven bottleneck**: evidence
   showing where the time/memory actually goes. If the measurement contradicts
   your intuition, the measurement wins.

3. **Propose with numbers.**
   Send the Problem / Plan / Risk / Question message. The Problem line carries
   the measurement, the Plan targets the proven bottleneck only. Performance
   fixes that touch queries, caching, or concurrency are L2 — wait for
   approval.

4. **Fix one thing.**
   The smallest change that addresses the proven bottleneck. Never bundle
   several optimizations in one step — you won't know which one worked, or
   which one broke something.

5. **Measure again, same conditions.**
   Same data, same scenario, same tool. Report both numbers. If the fix
   didn't move the number, say so and revert it — an ineffective optimization
   is pure complexity cost.

6. **Guard the win where practical.**
   A benchmark test, a query-count assertion, or at minimum the measurement
   commands recorded in the journal so the numbers can be reproduced.

7. **Record.**
   Journal entry: `docs/agent-journal/YYYY-MM-DD-perf-<slug>.md` with the
   before/after numbers and how they were measured.

## Do not

- Do not optimize code you haven't measured — no matter how obvious it looks.
- Do not trade readability for micro-gains that no measurement demanded.
- Do not accept "feels faster". Numbers or it didn't happen.
