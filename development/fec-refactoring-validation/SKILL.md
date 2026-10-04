---
name: fec-refactoring-validation
description: Use when proving that a frontend refactoring preserved existing behavior, selecting an appropriate safety net, validating each structural step, or assigning a PASS, PARTIAL, or NOT PROVEN preservation verdict.
---

# Skill: Refactoring Validation

## Purpose

Define the observable contract and the smallest credible evidence needed to prove that structural edits preserved existing frontend behavior.

## Procedure

1. Record the relevant behavior contract before substantial edits.
2. Classify safety-net coverage as A, B, or C.
3. Run and record the pre-change baseline.
4. Match verification to the current refactoring risk and affected boundary.
5. After every structural step, run the narrowest sufficient check immediately.
6. If a newly introduced failure appears, revert that step before broader repair.
7. At the end, run the broad gates justified by the affected surface.
8. Assign PASS, PARTIAL, or NOT PROVEN from evidence, not optimism.

Pure structural work uses **GREEN → REFACTOR → GREEN**.

## Safety-Net Levels

| Level | Evidence | Execution guidance |
| --- | --- | --- |
| A — Strong | Existing tests cover relevant behavior | Use tests as the primary safety net |
| B — Partial | Important behavior is only partly covered | Add focused characterization of current behavior before risky steps |
| C — None | No useful automated behavior coverage | Do not auto-install a framework; keep CAUTION/DANGER plan-only unless a minimal safety net is authorized |

## Frontend Contract Checklist

Check relevant items, not every item mechanically:

- function inputs, outputs, exceptions, and error mapping;
- DOM structure that consumers depend on, visible states, focus, keyboard flow, and accessibility semantics;
- props, emits, slots, hook/composable return values, and event ordering;
- requests, payloads, cancellation, retries, cache keys, and loading/error transitions;
- store state, persistence, object identity, memoization, refs/reactivity, and lifecycle timing;
- routes, URLs, guards, package exports, serialized fields, and backend-facing DTOs.

## References

- Load [behavior-preservation.md](references/behavior-preservation.md) for contract construction and proof levels.
- Load [refactoring-test-checklist.md](references/refactoring-test-checklist.md) for targeted verification by frontend risk.

## Constraints

- Passing unrelated tests does not prove preservation.
- A green test written only after the change is weaker evidence than a pre-change baseline or characterization test.
- Do not rewrite expected values simply because the refactor changed behavior.
- Do not hide missing proof behind a PASS label.
- Do not install a new test framework without explicit authorization.

## Expected Output

A behavior-preservation record containing baseline status, safety-net level, per-step checks, final validation, unresolved coverage gaps, and a PASS/PARTIAL/NOT PROVEN verdict.
