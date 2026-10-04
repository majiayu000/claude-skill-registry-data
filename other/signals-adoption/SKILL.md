---
id: angular.architecture.signals-adoption
name: Signals Adoption
description: >
  Adopt Angular signals in bounded post-upgrade modernization slices to replace or complement local component state, derived state, and reactive glue without mixing the change into an Angular version hop.
stack:
  - Angular
  - TypeScript
category: architecture
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - signals
  - signal state
  - reactive state modernization
  - computed effect adoption
compatibility:
  angular:
    min: "17"
---

# Signals Adoption

## Purpose

Adopt Angular signals in bounded modernization slices after the app is stable on a compatible Angular version.

## When to Use

- The app is already on a stable Angular version that supports signals.
- The team wants to modernize local component state incrementally.
- The change is architectural modernization, not a version upgrade.

## When Not to Use

- The app is still in the middle of a major Angular hop.
- The target slice is not well tested.
- The app is not on a version that supports signals.

## Required Inputs

- local component state
- derived state usage
- reactive glue code
- computed values and effects
- tests for the target slice

## Procedure

1. Select a bounded feature area.
2. Identify state that is local and stable.
3. Replace the smallest safe slice with signals.
4. Keep interop with existing observables explicit.
5. Validate rendering, effects, and tests.

## Do

- Prefer incremental conversion.
- Keep effects narrow and intentional.
- Validate change detection and UI updates.

## Do Not

- Do not convert the whole app in one pass.
- Do not mix signals adoption with upgrade hops.
- Do not replace service-level reactive architecture without a plan.

## Review Checklist

- [ ] Slice is bounded.
- [ ] State updates are correct.
- [ ] Tests pass.
- [ ] Remaining reactive debt is documented.

## Expected Output

1. Slice converted to signals.
2. Remaining observable/state debt.
3. Test result.
4. Follow-up list.

## Exit Criteria

- Adoption is incremental.
- The next slice is clear.
