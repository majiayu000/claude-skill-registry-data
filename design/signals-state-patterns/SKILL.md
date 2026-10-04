---
id: angular.signals.signals-state-patterns
name: Angular Signals State Patterns
description: >
  Designs Angular local state patterns with Signals, focusing on signal, computed, effect usage, state boundaries, derived values, and when not to replace RxJS.
stack:
  - Angular
  - TypeScript
category: signals
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - signals state
  - signal patterns
  - computed effect
  - local reactive state
  - angular signals
  - signal store
  - derived state
  - signals architecture
compatibility:
  angular:
    min: "16"
    signalsFrom: "16"
    recommendedModern: "17+"
    currentSafe: "19+"
---

# Angular Signals State Patterns

## Purpose

Use this skill to design or review local state with Angular Signals.

Signals are best for synchronous, local, derived UI state. They simplify stateful components when the state boundary is clear and the problem does not require stream orchestration.

The core rule is simple:

```txt
Use Signals for local state and derivations, not for every async workflow.
```

## When to Use

Use this skill when:

- local component state is becoming noisy
- derived state should be explicit
- a feature wants signal-first local state
- `computed` values would reduce duplicate logic
- `effect` may be needed for a controlled side effect

## Do

Prefer a small local state model:

```ts
readonly count = signal(0);
readonly doubled = computed(() => this.count() * 2);

increment(): void {
  this.count.update((value) => value + 1);
}
```

Use `effect` for controlled side effects only:

```ts
effect(() => {
  console.log("count changed", this.count());
});
```

Keep Signals near the component or feature boundary unless you have a documented shared-state contract.

## Do Not

Avoid replacing HTTP orchestration or cancellation-heavy streams with `effect`.

Avoid global signal stores for trivial local state.

Avoid using Signals without a clear state ownership boundary.

Avoid mixing multiple state models without a reason.

## Review Checklist

- [ ] State is local and synchronous enough for Signals.
- [ ] Derived state is expressed with `computed`.
- [ ] `effect` is used only for intentional side effects.
- [ ] RxJS remains available for async orchestration.
- [ ] The state boundary is explicit.

## Expected Output

1. Classify the state lifetime and synchronicity.
2. Recommend signal-based local state where appropriate.
3. Separate derivation from mutation.
4. Flag misuse of `effect` for orchestration.
5. Explain when RxJS remains the better fit.
