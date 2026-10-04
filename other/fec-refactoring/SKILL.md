---
name: fec-refactoring
description: Use when restructuring existing frontend code while preserving observable behavior, including responsibility extraction, module movement, conditional simplification, API cleanup, or data organization. Do not use for new feature behavior, behavior-changing bug fixes, dependency or framework migrations, or proven dead-code cleanup.
---

# Skill: Behavior-Preserving Refactoring

## Purpose

Restructure live frontend code in small, evidence-backed steps while preserving the behavior users, callers, tests, routes, and integrations can observe.

## Core Contract

Every execution follows these rules:

1. **Behavior Preservation** — pure refactoring intentionally changes structure, not observable behavior.
2. **Green Baseline First** — record available verification before editing.
3. **One Refactoring at a Time** — one primary structural intent per step.
4. **Verify Every Step** — run the narrowest meaningful check immediately after each step.
5. **Revert Before Repairing** — if a new regression appears, revert that step before widening the edit.
6. **Separate Refactoring from Feature Work** — behavior changes belong in a different workflow.
7. **Smallest Safe Refactoring First** — prefer the narrowest transformation that fits the evidence.
8. **Stay Within the Diff Budget** — stop when actual scope materially exceeds the planned scope.

Pure refactoring uses **GREEN → REFACTOR → GREEN**. Do not manufacture a failing behavioral test merely to make a structural change look like feature TDD.

## Procedure

1. **Classify the request.** Confirm that the intended result is structural and behavior-preserving.
2. **Discover context.** Read project configuration, affected modules, public exports, routes, state boundaries, tests, and current diff.
3. **Record observable contracts.** Capture inputs, outputs, errors, side effects, UI states, events, network calls, state transitions, routes, and public APIs that matter.
4. **Establish the baseline.** Run existing narrow checks first; record pre-existing failures rather than attributing them to later edits.
5. **Diagnose structural evidence.** Identify the concrete smell or responsibility problem and check likely false positives.
6. **Build the safety net.** Reuse relevant tests; add characterization coverage only when needed to preserve existing behavior.
7. **Plan ordered micro-refactorings.** For each step record technique, rationale, prerequisites, risk, Diff Budget, verification, and rollback boundary.
8. **Apply exactly one primary transformation.** Avoid opportunistic cleanup, formatting churn, or unrelated redesign.
9. **Verify immediately.** Compare actual scope with the Diff Budget and run targeted checks.
10. **Handle regression.** Revert the current step, confirm the prior baseline, shrink or reorder the transformation, then retry only with evidence.
11. **Run broad final validation.** Escalate from targeted checks to typecheck, tests, build, E2E, accessibility, or specialty checks when relevant.
12. **Report proof strength.** Use PASS, PARTIAL, or NOT PROVEN and state remaining risk.

## Risk Classification

| Risk | Typical scope | Default action |
| --- | --- | --- |
| `SAFE` | Local/private code, stable contracts, easy rollback | Execute with step-level verification |
| `CAUTION` | Cross-module movement, shared state, imports, hooks/composables, lifecycle | Execute only with adequate safety evidence |
| `DANGER` | Public API, routes, persistence, network contracts, auth, SSR/hydration, broad state or inheritance redesign | Plan and stop for explicit approval unless already authorized |

Risk is contextual. A technique name alone never proves that a change is safe.

## Diff Budget

Before each executable step record:

```text
Expected files: N
Expected functions/components: N
Expected public API changes: 0
Expected behavior changes: 0
```

If the actual diff materially exceeds that budget, stop and reassess instead of silently expanding into redesign.

## References

- Load [principles.md](references/principles.md) for the safety rules, evidence model, and risk language.
- Load [workflow.md](references/workflow.md) for the state machine, baseline handling, rollback, and reporting contract.
- Load [when-to-refactor.md](references/when-to-refactor.md) when deciding whether restructuring is timely or should be deferred.
- Load [refactoring-vs-feature-change.md](references/refactoring-vs-feature-change.md) when ownership overlaps feature work, debugging, cleanup, migration, or review.

## Constraints

- Do not alter tests merely to accept behavior changed by the refactoring.
- Do not label auth, permission, routing, persistence, protocol, or public package changes `SAFE` without specific evidence.
- Do not stack additional structural edits after a newly introduced failure.
- Do not install a new test framework automatically when the project has none.
- Do not treat line count, complexity metrics, comments, a switch, or chaining as sufficient proof of a code smell.
- Do not perform remote Git writes by default.

## Expected Output

A small-step refactoring plan or implementation with explicit evidence, risk, Diff Budget, per-step verification, rollback history when applicable, and a final PASS/PARTIAL/NOT PROVEN behavior-preservation verdict.
