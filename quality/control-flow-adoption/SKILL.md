---
id: angular.architecture.control-flow-adoption
name: Control Flow Adoption
description: >
  Adopt Angular control flow syntax in bounded post-upgrade modernization slices to replace structural directive boilerplate with `@if`, `@for`, and `@switch` without mixing the change into an Angular version hop.
stack:
  - Angular
  - TypeScript
category: architecture
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - control flow
  - "@if"
  - "@for"
  - "@switch"
  - structural directives modernization
compatibility:
  angular:
    min: "17"
---

# Control Flow Adoption

## Purpose

Adopt Angular control flow syntax in bounded modernization slices after the app is stable on a compatible Angular version.

## When to Use

- The app is already on a stable Angular version that supports control flow.
- The team wants to replace structural directive boilerplate incrementally.
- The change is architectural modernization, not a version upgrade.

## When Not to Use

- The app is still in the middle of a major Angular hop.
- The target slice is not well tested.
- The app is not on a version that supports the new syntax.

## Required Inputs

- templates using `*ngIf`
- templates using `*ngFor`
- templates using `*ngSwitch`
- shared UI fragments
- test coverage for the target slice

## Procedure

1. Select a bounded feature area.
2. Replace one structural directive family at a time.
3. Keep expressions and tracking logic explicit.
4. Validate templates, accessibility, and tests.
5. Stop after the slice is stable.

## Do

- Prefer incremental conversion.
- Keep `track` expressions deliberate.
- Validate empty-state and fallback rendering.

## Do Not

- Do not convert the whole app in one pass.
- Do not mix control flow adoption with upgrade hops.
- Do not change business logic while changing template syntax.

## Review Checklist

- [ ] Slice is bounded.
- [ ] Rendering is equivalent or intentionally changed.
- [ ] Tests pass.
- [ ] Remaining template debt is documented.

## Expected Output

1. Slice converted to control flow.
2. Remaining structural directives.
3. Test result.
4. Follow-up list.

## Exit Criteria

- Adoption is incremental.
- The next slice is clear.
