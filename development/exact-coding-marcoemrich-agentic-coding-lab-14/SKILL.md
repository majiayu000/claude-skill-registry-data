---
name: exact-coding
description: Predictive Test-Driven Development with a complete up-front test list, falsifiable predictions before deterministic checks, one-test Red-Green-Refactor cycles, and configurable human checkpoints. Invoke when the user explicitly asks for TDD or Predictive TDD. Do NOT invoke for ordinary coding tasks where TDD was not requested.
---

# EXACT Coding — SOL / Predictive TDD

This is the consumer form of the SOL-originated EXACT Coding line. It runs in
one shared context: Test List once, then one-test Red-Green-Refactor cycles.
Refactoring uses the Four Rules of Simple Design inline; this line deliberately
has no APP calculation, metric-driven end pass, or refactor subagent.

## Preparation

1. Read `.pi/skills/test-list/SKILL.md`.
2. Read `.pi/skills/predictive-tdd/SKILL.md`.
3. Determine the project's language and test framework. Read the matching file
   under `.pi/skills/predictive-tdd/stacks/` before changing code.
4. Read the complete specification and establish the applicable baseline gates.

Do not assume TypeScript or Vitest from this orchestration file. Concrete
inactive-test syntax, examples, paths, commands, compiler behavior, and quality
tools belong only to the selected stack profile.

## Sequence

1. Create the complete ordered test list with every future behavior inactive.
2. Apply the Test-List checkpoint from `.pi/skills/exact-coding/human-in-the-loop.md`.
3. For exactly one behavior at a time, follow the Predictive TDD skill:
   - activate one behavior and reach behavioral Red,
   - state falsifiable predictions before deterministic checks and compare them
     explicitly with reality,
   - apply the Red checkpoint,
   - reach Green with the smallest production change,
   - review and, where useful, refactor inline under the Four Rules,
   - apply the Refactor checkpoint.
4. Continue until every listed behavior is executable and all applicable gates
   from the active stack profile pass.

A test already satisfied by an earlier generalization is legitimate evidence.
Confirm it and do not manufacture a failure or production change.

## Human-in-the-loop

`.pi/skills/exact-coding/human-in-the-loop.md` is the single source of truth for checkpoints. Its default
`full-hitl` level stops after Test List, Red, and Refactor, and whenever a
prediction is wrong. Green has no default stop.

## Provenance

Exported from the promoted `exact-sol-v1.3-stack-profile-pi` workflow. The methodology was validated
on GPT-5.6 SOL with pi. Other harness trees are
mechanical ports of the same files, not claims of cross-harness validation.
