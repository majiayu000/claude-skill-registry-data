---
id: angular.signals.signals-rxjs-interop
name: Angular Signals RxJS Interop
description: >
  Reviews the boundary between Angular Signals and RxJS, focusing on toSignal, toObservable, cancellation, async orchestration, and version-safe interop patterns.
stack:
  - Angular
  - TypeScript
  - RxJS
category: signals
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - signals rxjs interop
  - toSignal
  - toObservable
  - interop boundary
  - angular signals rxjs
  - observable to signal
  - signal to observable
  - reactive boundary
compatibility:
  angular:
    min: "16"
    signalsFrom: "16"
    recommendedModern: "17+"
---

# Angular Signals RxJS Interop

## Purpose

Use this skill to define the boundary between Angular Signals and RxJS.

Interop should be deliberate. RxJS remains the right tool for async orchestration, cancellation, and stream composition, while Signals are best for synchronous local state and derived UI values.

The core rule is simple:

```txt
Convert at the boundary, not everywhere.
```

## When to Use

Use this skill when:

- an Observable needs to feed a signal-driven component
- a signal must be exposed to Observable consumers
- HTTP or router streams meet local UI state
- async orchestration and local derivation need a clean boundary

## Do

Convert streams at clear boundaries:

```ts
readonly user = toSignal(this.user$, { initialValue: null });
readonly filter$ = toObservable(this.filter);
```

Keep async work in RxJS:

```ts
readonly results$ = this.search$.pipe(
  debounceTime(300),
  switchMap((query) => this.api.search(query)),
);
```

Use Signals for local consumption after the conversion boundary.

## Do Not

Avoid converting every Observable into a Signal.

Avoid using Signals to replace cancellation-heavy async flows.

Avoid creating interop loops without a clear ownership model.

Avoid using experimental APIs as a default unless the project has explicitly accepted them.

## Review Checklist

- [ ] The interop boundary is explicit.
- [ ] RxJS still owns async orchestration.
- [ ] Signals still own local derived state.
- [ ] Conversion is not overused.
- [ ] The Angular version supports the APIs being used.

## Expected Output

1. Identify where interop is actually needed.
2. Define the conversion boundary.
3. Preserve RxJS for async workflows.
4. Preserve Signals for local synchronous state.
5. Explain why the conversion belongs where it does.
