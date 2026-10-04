---
id: angular.signals.signals-state-patterns-v16
name: Angular Signals State Patterns v16+
description: >
  Reviews Angular Signals state patterns for Angular 16+ projects, focusing on signal, computed, and effect usage, local state boundaries, and RxJS coexistence.
stack:
  - Angular
  - TypeScript
category: signals
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - signals v16
  - angular 16 signals
  - signals state patterns 16
  - local state signals
  - computed effect v16
compatibility:
  angular:
    min: "16"
    signalsFrom: "16"
---

# Angular Signals State Patterns v16+

## Purpose

Use this skill for Angular 16+ projects where Signals are available and local state needs a clear, version-aware pattern.

This variant anchors Signals at the point where Angular introduced them, so the guidance does not overreach into older baselines.

## When to Use

Use this skill when:

- the project is Angular 16 or newer
- Signals are part of the state strategy
- local derived state needs to be simplified
- the team wants version-accurate adoption guidance

## Do

Use `signal` and `computed` for local synchronous state.

Use `effect` only for controlled side effects.

Keep RxJS for async orchestration and cancellation.

## Do Not

Avoid recommending Signals for Angular 2-15 projects.

Avoid treating `effect` as a substitute for stream orchestration.

## Review Checklist

- [ ] Angular version is 16 or newer.
- [ ] Signals are used only where supported.
- [ ] Local state is the main use case.
- [ ] RxJS still handles async flows.

## Expected Output

1. Confirm Signals are version-appropriate.
2. Recommend local-state patterns.
3. Separate derivation from side effects.
4. Preserve RxJS for async work.
5. Produce 16+ guidance only.
