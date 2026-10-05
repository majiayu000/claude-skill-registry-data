---
name: reviewing-plans
description: Use when reviewing an AI-generated implementation plan before execution, when handed a plan to approve, or when checking if a plan is ready to act on
---

# Reviewing Plans

**Core mindset:** You're not checking whether the plan sounds smart. You're checking whether a diligent but literal executor can follow it step by step and arrive at exactly what you wanted — nothing more, nothing less.

**Announce at start:** "I'm using the reviewing-plans skill to review this plan."

---

## 1. Problem & Scope

- Does it restate and solve the *actual* problem, not a nearby easier one?
- Is this the simplest approach that solves it, or is there an obvious simpler alternative?
- No extra features or refactors you didn't ask for. No vague hand-waving ("handle edge cases") on the hard parts.
- If you can't tie a step to your original request in one sentence, cut it.

## 2. Step Quality

Each step must be **specific** (exact files/functions), **atomic** (one thing), **ordered** (no forward dependencies), and **verifiable** (clear "done" condition).

Red flags: vague steps ("clean up the code"), bundled mega-steps, assumed knowledge not in the plan.

## 3. Dependencies & Risk

- Steps in the right order? Hidden dependencies called out?
- What's the blast radius? Destructive actions (deletions, migrations) isolated and done last?
- If step N fails, are steps 1–(N-1) still usable?

## 4. Verification

- Does it start from a known state and end with a verified one?
- Every meaningful step has a *concrete* check ("run suite X, expect green" not just "run tests").
- Final end-to-end verification exists, not just step-by-step.
- Existing behavior is confirmed preserved.

## 5. What's Missing

- Failure handling (network errors, invalid input, partial state)
- Existing tests — will they still pass?
- Boundaries (empty states, first run, large datasets)
- Cleanup (dead code, imports, deprecations)

## 6. Exit Criteria

"Done" is clearly defined, independently verifiable, and ends with a concrete deliverable — not "continue improving."

## 7. Red Flags Cheat Sheet

| You see | It means |
|-|-|
| "Refactor/update as needed" | No plan, will improvise |
| "For completeness" / "While we're here" | Scope creep |
| Steps with no verification | Will claim success unchecked |
| New abstractions for one use case | Over-engineering |
| Touching unrelated files | Scope creep or misunderstanding |
| "Should be straightforward" | Hasn't thought it through |
| No mention of existing tests | Will break things silently |
| "We'll handle that later" | Deferring the hard part |
| "Similar to how we did X" | Assuming without verifying |
| Plan starts with code changes, not verification | Guessing, not diagnosing |
