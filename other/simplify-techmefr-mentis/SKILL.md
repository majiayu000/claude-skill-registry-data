---
name: simplify
description: Use when the review is done and before SHIP, quality pass on the changed code (reuse, simplification, efficiency), no bug hunting.
---

# simplify

Step 9 of the pipeline (`WORKFLOW.md`). Clean up what was built, once it's correct.

## When
After `review` (`reviewed`), before `ship`.

## Steps
1. Re-read the diff: missed reuse, duplicated code, pointless indirection, over-abstraction.
2. Simplify at identical behaviour (the GATE tests stay green).
3. Check consistency with what `archi` (3) wrote down, and mark as built what is now built — so the
   architecture record stops describing a plan and starts describing the code.

4. Prove the behaviour held: run the same proof you ran at the gate, on the simplified code, and read the result
   (`skills/gate` §8). A simplification you did not re-verify is a change you did not review.
5. A simplification that moves responsibility between files or layers is a structural change: follow
   `skills/safe-refactor` for it (proof first, one boundary per step) rather than folding it into this pass.
6. Remove only what the change itself made redundant; leave neighbouring code and report it instead
   (`skills/code-baseline` §0).

## Output / checkpoint
`simplified`.

## Guardrails
Quality only: **no** bug hunting here (that was `review`/`gate`). Don't change behaviour; if a
simplification breaks a test, it's a real change → back to `code`. Never edit a test to make a simplification
pass: that is the behaviour change, hidden (`skills/tdd`).

## Origin
Native Claude Code (`simplify` skill) + internal, rewritten.
