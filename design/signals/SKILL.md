---
name: react/signals
description: >-
  Use Preact signals in ReactStore components/custom hooks: ReadonlySignal,
  .value, computed, JSX rendering, Babel/useSignals tracking, and component-local
  signals. Selector call modes belong to selector-lifecycle.
type: sub-skill
requires:
  - react
sources:
  - "@preact/signals-react"
  - "@preact/signals-react/runtime"
  - "https://preactjs.com/guide/v10/signals/"
  - "https://github.com/preactjs/signals/blob/main/packages/react/README.md"
  - "https://github.com/preactjs/signals/blob/main/packages/core/README.md"
  - ../selectors/SKILL.md
triggers:
  - Preact signal
  - React signal
  - ReadonlySignal
  - signal .value
  - useSignals
  - useSignal
  - useComputed
  - useSignalEffect
  - computed signal
  - JSX signal rendering
---
# React/Preact signals — tracking and consumption

Use this skill for React apps that chose `ReactStore` and Preact Signals. It
owns general signal tracking and component-local signals;
[Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map) owns ReactStore
selector consumption choices, while `../selectors/SKILL.md` owns authoring.

This skill covers React signal consumption only. Keep selector outputs and
component-local signals within the React tracking mechanisms described below.

## Signal model

- A signal is an object whose current value is read through `.value`.
- `ReadonlySignal<T>` is the correct type for ReactStore selector outputs and
  computed outputs. Treat it as read-only: read `.value`, do not assign it.
- Mutable `Signal<T>` values may assign `.value`, but app/domain shared state
  should live in reducers and ReactStore selectors instead of module-level
  shared signals.
- `computed(fn)` returns a read-only computed signal. Dependencies are tracked
  from signal `.value` reads inside `fn`.
- ReactStore direct selector calls already return scheduled `ReadonlySignal<R>`
  values; do not wrap them in extra `computed`, debounce, cache, or subscription
  layers just to make them reactive.

## React tracking requirement

React components that read `signal.value` must be rendered under one of the
official React tracking mechanisms:

1. Prefer the `@preact/signals-react` Babel transform for automatic component
   reactivity when the component statically reads `.value`.
2. If the transform is unavailable for the file, call `useSignals()` from
   `@preact/signals-react/runtime` in the component/custom hook before reading
   direct signal values. `selector.useValue(...args)` already uses this runtime
   path internally and is only a plain-value fallback boundary.
3. When a component can avoid reading `.value`, passing or rendering the signal
   intentionally is valid. The React adapter supports direct signal rendering in
   JSX text; for React 18 typing, wrap text signal output in a Fragment when
   needed.

Static transform limits matter. Signals read in render props, callback bodies,
object getters/setters, or other code the transform cannot see may not be
tracked. Move the read into a small component that statically accesses
`.value`, pass the `ReadonlySignal<T>` through, or use the explicit
`useSignals()` fallback in that component.

## Component-local signals

Use component-local signal hooks when the state is genuinely local UI state:

```tsx
import { useComputed, useSignal, useSignalEffect } from "@preact/signals-react";

export function DraftTitle() {
  const draft = useSignal("");
  const remaining = useComputed(() => 80 - draft.value.length);
  useSignalEffect(() => {
    document.title = `${remaining.value} left`;
  });
  return <input value={draft.value} onInput={(event) => draft.value = event.currentTarget.value} />;
}
```

Rules:

- Use `useSignal`, `useComputed`, and `useSignalEffect` inside React components
  or custom hooks for component-local signal state/effects.
- Do not call `signal()` in a component render to create a new signal each
  render.
- Do not move app shared/domain state into module-level `signal(...)` just to
  avoid reducers, selectors, or actions.
- Keep business side effects in sagas; reserve `useSignalEffect` for UI-local
  integration like focus, measurement, document title, or imperative widgets.

## ReactStore selector signal consumption

ReactStore selectors produce read-only signals that use the tracking mechanisms
above. For component/prop examples and necessary plain-value fallbacks, follow
[React signal consumption guardrails](../selector-lifecycle/SKILL.md#react-signal-consumption-guardrails)
and [Examples](../selector-lifecycle/SKILL.md#examples); this skill does not
define a second selector call-mode policy.

## Direct JSX signal rendering

```tsx
import { useComputed, useSignal } from "@preact/signals-react";

export function DraftLength() {
  const draft = useSignal("");
  const label = useComputed(() => `${draft.value.length} characters`);
  return <><input onChange={(event) => draft.value = event.currentTarget.value} />{label}</>;
}
```

Use direct JSX signal rendering only when the JSX position intentionally accepts
a signal as text. For props, conditions, array/object operations, or values sent
to non-signal-aware APIs, read `.value` in a tracked component or use a
documented plain-value fallback.

Selector-specific fallback choices are in
[Fallback hook/plain-value read](../selector-lifecycle/SKILL.md#fallback-hookplain-value-read).

## Do / don't

Do:

- Type selector results and props as `ReadonlySignal<T>` when consumers can be
  signal-aware.
- Read `.value` where a plain value is needed and make sure the read is tracked.
- Pass `ReadonlySignal<T>` through props to small presentational components that
  read it statically.
- Use `computed()` for local derived signals, not for duplicating Store selector
  memoization.

Don't:

- For selector results, apply the signal/plain-value boundaries in
  [Pitfalls](../selector-lifecycle/SKILL.md#pitfalls).
- Do not destructure, map, compare, or serialize a signal object as if it were
  the selected value.
- Do not replace ReactStore selectors with module-level shared signals for app
  domain data.

## Verification cues

- Component examples that read `.value` mention Babel transform or explicit
  `useSignals()` tracking.
- Selector-specific examples follow
  [Verification cues](../selector-lifecycle/SKILL.md#verification-cues).
- React signal guidance remains scoped to ReactStore selector outputs and
  component-local signal state.
