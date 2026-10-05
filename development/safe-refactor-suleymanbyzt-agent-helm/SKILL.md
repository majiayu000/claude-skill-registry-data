---
name: safe-refactor
description: Use when restructuring, cleaning up, or reorganizing existing code without changing its behavior. Enforces a test safety net before touching anything and proof that behavior was preserved.
---

# Safe Refactor

Goal: change the structure, prove the behavior did not change.

A refactor that changes behavior is not a refactor — it is an unreviewed
functional change. Refactoring is at least L2: send the Plan message and wait
for approval before starting.

## Steps

1. **Understand the current behavior.**
   Read the code, its callers, and its edge cases. List the invariants —
   the things that must still be true afterwards (outputs, side effects,
   error behavior, performance characteristics that matter).

2. **Build the safety net BEFORE changing code.**
   - Find the existing tests that cover this code. Run them; confirm green.
   - Where behavior is untested, add characterization tests: tests that pin
     down what the code does **today** — including odd behavior. You are
     documenting reality, not fixing it.
   - No safety net, no refactor.

3. **Plan small steps.**
   Break the refactor into steps that each keep the tests green. Prefer many
   small mechanical moves over one big rewrite.

4. **Refactor.**
   After every step: run the tests. If a test goes red, the last step broke
   behavior — fix the step, do not "adjust" the test.
   If you discover an actual bug mid-refactor, stop, report it, and handle
   it as a separate `bug-fix` task. Do not silently fix it inside the
   refactor.

5. **Verify preservation.**
   Full test suite green. Diff reviewed: only structural changes, no logic
   drift, no accidental behavior change. Run the `verify-work` skill.

6. **Record.**
   Journal entry: `docs/agent-journal/YYYY-MM-DD-refactor-<slug>.md`
   (format: Why / Safety net / Steps taken / Proof behavior preserved).

## Do not

- Do not mix refactoring with feature work or bug fixes in one change.
- Do not delete "weird" code you don't understand — it is load-bearing until
  proven otherwise. Investigate first.
- Do not widen the scope mid-refactor. New scope = new proposal.
