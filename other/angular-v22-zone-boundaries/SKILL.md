---
id: angular.zone.angular-v22-zone-boundaries
name: Angular v22 Zone Boundaries
description: >
  Use this skill when an Angular 22 app still depends on Zone.js behavior or needs to make change-detection boundaries explicit.
stack:
  - Angular
  - TypeScript
category: zone
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Zone.js
  - change detection
  - Eager
  - OnPush
  - zone boundaries
compatibility:
  angular:
    min: "22"
---

# Angular v22 Zone Boundaries

## Purpose

Use this skill when an Angular 22 app still depends on Zone.js behavior or needs to make change-detection boundaries explicit.

## When to Use

Use this skill when:

- The project still has significant Zone.js assumptions.
- You need to preserve or replace the previous default change-detection behavior.
- A third-party library still depends on zone-driven updates.

## When Not to Use

Do not use this skill when:

- The project is already in zoneless mode.
- The issue is only a template compile problem.
- No zone-related behavior is involved.

## Required Inputs

- zone-heavy code
- event handling
- component changeDetection settings
- third-party dependencies

## Procedure

1. Find the code that still depends on implicit zone updates.
2. Make the change-detection intent explicit where v22 changed defaults.
3. Check whether the third-party library needs a compatibility wrapper.
4. Validate that UI updates still happen when expected.

## Do

- Keep change-detection intent explicit.
- Document any reliance on Zone.js.
- Validate the interaction path, not just compilation.

## Do Not

- Do not assume implicit zone updates are still the right default.
- Do not remove zone support without checking dependencies.
- Do not blur zone behavior with pure performance tuning.

## Review Checklist

- [ ] The zone dependency is understood.
- [ ] Change detection is explicit.
- [ ] The interactive behavior was validated.

## Expected Output

1. A zone-boundary summary.
2. The explicit change-detection choice.
3. Any remaining third-party risk.
