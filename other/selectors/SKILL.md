---
name: react/selectors
description: >-
  Author pure ReactStore selectors with cached ReadonlySignal results and stable
  scalar/signal arguments. Route consumption and tracking to selector-lifecycle.
type: sub-skill
requires:
  - react
  - core/state-integrity
sources:
  - "@themislib/themis/react-store"
  - "@preact/signals-react"
  - "@preact/signals-react/runtime"
  - "@themislib/themis/docs/SELECTORS.md"
  - ../signals/SKILL.md
triggers:
  - React selector
  - direct selector signal
  - signal selector
  - ReadonlySignal selector
  - ReactStore selector
---
# React selectors — authoring and caching

Use this skill when `store.createSelector(...)` belongs to a `ReactStore` and
direct selector calls should produce Preact React `ReadonlySignal<R>` results.
This leaf owns selector definitions and caching, not consumer lifecycle. For
signal-first consumption and plain-value fallback boundaries, follow
[Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map) and
[React signal consumption guardrails](../selector-lifecycle/SKILL.md#react-signal-consumption-guardrails).

## Authoring rules

- Create selectors through the configured `ReactStore` instance.
- Keep selector callbacks pure and derived-only; reducers must not store selector
  outputs.
- Compose selectors with `.select(state, ...args)` inside another selector.
- Trust Store-owned selector-result caching and signal scheduling; do not wrap Store-created selectors in extra `memoize`, `cache`, debounce/throttle, manual cache maps, or scheduler helpers.
- Prefer primitive scalar selector arguments over freshly constructed object,
  array, or function arguments; object/function args are valid only when their
  identity is stable and intentional.
- Do not import from `themis` React selector internal deep paths.

```ts
import { reactStore } from "./react-store";

export const selectTodo = reactStore.createSelector((state, id: string) => {
  return state.todos.collection.map[id];
});
```

## Selector argument API

Choose the consumer entry point using
[Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map); the argument API
below describes how signal-aware entry points evaluate their inputs.

Selector arguments may be plain values or Preact React `ReadonlySignal` values
for direct calls, `.useValue(...args)`, and `.withStore(...)(...args)`. Signal
arguments are unwrapped through `.value` and their subscriptions feed the
selector's argument inputs, so the derived signal updates when Store state or
signal arguments change. `.select(state, ...args)` and `.effect(...args)` are plain synchronous or
saga paths; pass plain argument values there instead of signal wrappers.

Store-state changes reach active selector signals on the owning Store cadence;
signal-argument changes can recompute and emit changed results immediately,
downstream of that cadence. Initial snapshots are prompt. The frequency option
is not an overall output-rate cap. Configuration and temporary trace options
belong to [Store-first scheduling rule](../selector-scheduling/SKILL.md#store-first-scheduling-rule).
Saga and selector-channel reads do not subscribe to React signals; follow
[React signal consumption guardrails](../selector-lifecycle/SKILL.md#react-signal-consumption-guardrails)
for that boundary.

## Selector caching

- Store-created selectors have internal selector-result caching/memoization.
- Direct React `ReadonlySignal` outputs are cached per ReactStore instance + selector + arguments. Never-observed outputs and concurrent live consumers reuse the same signal. Removing one of several consumers retains it; removing the final observed consumer evicts that output even if JavaScript references remain. The next identical call creates a new signal. Store disposal evicts all its outputs; cache counts are not active-consumer counts.
- Do not wrap selector callbacks, direct signal calls, or `.useValue(...args)` calls in extra `memoize`, `cache`, manual cache maps, debounce, or throttle layers solely for performance.
- Prefer the same Store-bound selector + same arguments over props drilling when
  the receiving consumer can call it in a valid context; choose that context's
  entry point via [Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map).

## Stable selector arguments

- Prefer primitive scalar selector arguments: ids, booleans, enum strings,
  numbers, `null`, or `undefined`.
- Do not pass freshly constructed object, array, or function arguments to direct
  `selectFoo(...)`, `.useValue(...)`, `.select(state, ...)`, `.effect(...)`,
  `.withStore(store)(...)`, selector-channel args tuples, or `waitFor` args
  tuples.
- Object/function args are valid only when the identity is stable and intentional,
  such as a module constant, memoized config, existing source object, or Preact
  signal. Signal arguments are valid direct-call inputs because the selector
  tracks their `.value`; do not recreate the signal solely for a selector call.
- Prefer selector definitions like `(state, id, includeDone)` over
  `(state, { id, includeDone })`; destructure an object arg only when callers pass
  a documented stable reference.

## Authoring examples

Consumer examples for direct signals, hook fallbacks, handlers, explicit Store
bindings, and sagas live in [Examples](../selector-lifecycle/SKILL.md#examples).
These examples focus on argument tracking and pure selector definitions.

### Signal arguments update derived selectors

```tsx
import { useSignal } from "@preact/signals-react";
import { selectVisibleTodos } from "./todos-selectors";

export function FilteredTodos() {
  const filter = useSignal("open");
  const todos = selectVisibleTodos(filter);
  return <TodoList todos={todos} onFilterChange={(next) => filter.value = next} />;
}
```

The selector receives a signal argument and internally tracks `filter.value`.
Consumers still receive a `ReadonlySignal<R>` result.

### Pure composition and tests

```ts
export const selectOpenTodoTitles = reactStore.createSelector((state) => {
  return selectTodos.select(state)
    .filter((todo) => !todo.completed)
    .map((todo) => todo.title);
});

expect(selectOpenTodoTitles.select(mockState)).toEqual(["Write docs"]);
```

Keep composition synchronous against the supplied state snapshot. Consumer
wrong-shape and hook-boundary mistakes are covered in
[Pitfalls](../selector-lifecycle/SKILL.md#pitfalls).

## Don't

- Follow [React signal consumption guardrails](../selector-lifecycle/SKILL.md#react-signal-consumption-guardrails)
  for signal/plain-value and hook boundaries; this leaf does not redefine them.
- Do not add manual memoization or throttling wrappers around selector calls, direct signals, or `.useValue(...)`; configure selector coalescing through the owning `ReactStore` options instead.
- Do not props-drill derived values solely to avoid selector calls when the consumer can call the same Store-bound selector with the same args in a valid React/signal context.
- Do not use standalone React selector utilities as public package imports.
- Do not construct `{ ... }`, `[ ... ]`, or `() => ...` selector arguments inline
  during render or hook execution; use scalar args or a stable intentional
  reference.

## Verification cues

- Check consumer examples against [Verification cues](../selector-lifecycle/SKILL.md#verification-cues).
- Definitions are Store-bound, pure, and use stable arguments without extra caches.
- Unit tests for pure selector logic use `.select(mockState, ...args)`.

## See also

- `../store/SKILL.md` — Store class and import choice.
- `@themislib/themis/docs/SELECTORS.md` — human reference and examples for all call forms.
- `../../core/state-integrity/SKILL.md` — canonical derived-value ownership.