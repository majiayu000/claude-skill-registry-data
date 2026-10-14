---
name: characterization-test-scoping
description: "Trigger: characterization tests, seams, high-risk refactor planning, test safety planning. Scope high-risk refactor work around tests, seams, containment, and rollback."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "2.2.1"
  status: testing
---

## Activation Contract
Load this skill when a refactor plan runs at high/critical risk or when scoping work around characterization coverage, seams, and the test safety net.

## Hard Rules

- Prefer characterization coverage before structural change.
- Prioritize seam creation only when it reduces containment or rollback risk.
- Keep executable work behavior-preserving; move redesigns and behavior changes to follow-up.
- Require rollback-friendly increments and explicit containment rationale.
- Tests must precede structural refactoring.
- Keep characterization tests in a dedicated test class/file per unit (per `code-conventions`); they are a permanent regression net and never mix with intent-revealing unit tests.

## Decision Gates

| Signal | Action |
|---|---|
| No tests or unclear behavior | Put characterization coverage first |
| Hard-to-isolate dependency or long procedure | Recommend seams that improve testability or rollback safety |
| Proposed work changes behavior or public API | Move it to follow-up |

## Execution Steps

1. Identify current behavior that must be locked down first.
2. List the smallest characterization slices that reduce regression risk fastest.
3. Highlight seam opportunities that enable isolation, fakes, or safer rollback.
4. Prefer backlog items that can be validated incrementally.
5. Keep speculative cleanup and redesign out of executable refactor-plan backlog.

## Effect Reasoning

Choose what to characterize by tracing effects forward from each change point until they become observable, along the three propagation paths: return values, mutation of reachable state, and statics/globals or external writes. The methods where those effects surface are the test points; code the change cannot affect needs no characterization. Characterize only the zone the plan will touch (targeted characterization), never the whole unit by default.

## Pinch Points

When a change spans a cluster of coupled classes, find the narrowest downstream point where their effects converge and anchor a temporary integration-level characterization test there ("test one level back"). Pinch-point tests are scaffolding: they trade defect localization and speed for coverage, so the plan must schedule their removal or demotion once unit-level tests exist at the new seams.

## Test Priority

Boundary conditions and the happy path rank highest; expected error paths rank medium; code that rarely changes ranks lowest. A few tests that would catch a real regression beat many trivial ones. When a bug is in scope, the first test is one that reproduces it.

## Test Types

- Characterization tests for current behavior.
- Unit tests around isolated rules after seams exist.
- Integration tests for persistence/external boundaries.
- Contract tests for public APIs/events.
- Approval/snapshot tests for broad legacy outputs when appropriate; prefer whole-object asserts (recursive comparison, approval, snapshot) over field-by-field cascades for complex outputs.
- Mutation testing for critical rules using the concrete tool named by the tooling audit and compatibility matrix.
- Property-based tests for invariants and input spaces when useful; name the concrete library when present, otherwise reference the install task.

## Tooling-Aware Planning

When mutation, property, coverage, or assertion tooling is absent, do not silently skip that safety layer. Reference the `tooling_audit.install_tasks` item and explain which test step depends on it. If the matrix has a concrete tool for the detected stack, name that tool; if compatibility is uncertain, mark it as `hypothesis` and require verification before install.

## Output Contract

Return guidance that sharpens characterization coverage, seam selection, containment, rollback, and the test safety net.

## References

- the deep-planner protected-planning flow
- the tooling-audit skill
- the tooling-compatibility-matrix skill
