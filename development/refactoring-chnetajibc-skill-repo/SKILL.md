---
name: refactoring
description: "Refactor preserving behavior: reduce complexity, honor Chestertons Fence. Verify with tests; no unrelated scope."
---

# refactoring

Same behavior, simpler code — proven by tests, scoped to the task.
## Inspection

Map callers, tests, and behavior contracts of the target; check git history for why it looks this way (Chesterton's Fence).

## Decision rules

Refactor only with covering tests; smallest behavior-preserving steps; delete dead code outright; never mix refactor with feature changes in one diff.


## Activate when

- Complexity, duplication, or decay blocks change; opportunistic cleanup inside a touched area.

## Do NOT activate for

- Rewrites or architecture changes (plan those); formatting-only passes (see tooling/formatting).

## Procedure

1. Cover with tests first (characterization tests for legacy); understand why the code is shaped this way (Chesterton's Fence) before removing anything.
2. Small steps: extract, rename, deduplicate — running tests after each; one behavior-preserving move at a time.
3. Delete dead code outright (no "maybe later" branches); keep the diff scoped to the task.
4. Verify: full suite green, no behavior change (diff reviewed for semantic shifts), complexity reduced measurably.

## Failure modes

Refactor+feature in one diff; removing code nobody proved dead; 'cleanup' that changes semantics; no test run between steps.

## Escalation

Architecture-scale moves → architecture/modularity; legacy without tests → characterization tests first (core/testing).
