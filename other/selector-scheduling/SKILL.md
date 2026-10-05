---
name: react/selector-scheduling
description: >-
  Tune ReactStore signal/.useValue coalescing with throttledSelectorFrequency.
  Keep scheduling Store-owned: no private scheduler imports, debounce wrappers,
  or audit-log use.
type: sub-skill
requires:
  - react
  - react/selectors
sources:
  - "@themislib/themis/react-store"
  - ../selectors/SKILL.md
triggers:
  - React selector scheduling
  - signal selector scheduler
  - throttled React selector
  - throttledSelectorFrequency React
---
# React selector scheduling — internal only

> Selector scheduler helpers are package-private implementation details. React
> consumers must not import scheduler internals, wrap selector outputs in their
> own debounce layer, or treat selector emissions as event/audit logs.

Public facade: `@themislib/themis/react-store`. Create selectors through the
configured `ReactStore` instance and tune selector coalescing only through
`ReactStore` options such as `throttledSelectorFrequency`.

## Store-first scheduling rule

Scheduling applies to signal-backed render consumers. Choose the consumer API
using [Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map); this leaf
owns cadence, not component/hook/handler/saga boundary rules.

- Create production selectors with the configured `ReactStore` instance:
  `reactStore.createSelector(...)`.
- Direct `ReadonlySignal` outputs and `.useValue(...args)` use the owning
  `ReactStore`'s cadenced state stream. The state tick rate is capped by
  `throttledSelectorFrequency`; signal-argument changes can emit changed results
  immediately and are not capped by that option. The initial snapshot is prompt;
  later Store writes coalesce at the next scheduled tick.
- Same-Store/selector/args outputs share the retained cache entry, including
  never-observed outputs. Final-consumer cleanup evicts it; follow
  [Selector caching](../selectors/SKILL.md#selector-caching) for identity boundaries.
- Tune coalescing only with the final constructor options argument, for example
  `new ReactStore(reducers, middleware, { throttledSelectorFrequency })`.
- Omit `throttledSelectorFrequency` for the default `64` FPS. Explicit values
  must be finite numbers in the inclusive `1..256` range; fractional values are
  supported.
- Selector trace output is disabled by default; pass `{ traceSelectors: true }`
  in the same final options object only for temporary diagnostics.
- Snapshot and saga reads do not use React render scheduling; follow
  [React signal consumption guardrails](../selector-lifecycle/SKILL.md#react-signal-consumption-guardrails).
- There is no separately named public fast-selector API. `.select(store.state, ...plainArgs)`
  and saga `.effect(...plainArgs)` are one-shot uncadenced reads, not alternate
  render subscriptions; selector-channel sagas subscribe to Redux, not this cadence.

## Do not

- Do not import selector scheduler helpers from package internals or source-shaped
  paths.
- Do not wrap selector callbacks, selector signals, or `.useValue(...args)` results with ad hoc `memoize`, `cache`, debounce, `setTimeout`, `requestAnimationFrame`, streams, or proxy state just to reduce React renders.
- Do not manually subscribe to selector outputs from React components; use the
  consumer integration in [Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map).
- Do not rely on selector outputs as audit/event streams; they represent the
  latest derived state and may coalesce intermediate writes.
- Do not replace this React signal scheduling model with unrelated selector
  scheduling rules in the same React app path.

## Examples

### Configure coalescing at the ReactStore owner

```ts
import { ReactStore } from "@themislib/themis/react-store";
import { pointerReducer } from "./pointer-slice";

export const reactStore = new ReactStore(
  { pointer: pointerReducer },
  undefined,
  { throttledSelectorFrequency: 120, traceSelectors: true }
);
```

### Define selectors through the configured Store

```ts
import { reactStore } from "./react-store";

type Pointer = { x: number; y: number };

export const selectPointer = reactStore.createSelector((state): Pointer => {
  return state.pointer.current;
});

export const selectPointerLabel = reactStore.createSelector((state) => {
  const pointer = selectPointer.select(state);
  return `${pointer.x},${pointer.y}`;
});
```

### Consumer integration

Direct signal outputs already schedule Store-state changes, not argument changes. Component/hook, handler/test, and
saga examples belong to [Examples](../selector-lifecycle/SKILL.md#examples),
including the distinction between render subscriptions and one-shot reads.

### ❌ Bad: manual debounce wrapper around selector output

```tsx
// BAD: this adds stale local state on top of Store-owned selector coalescing.
import * as React from "react";
import { selectPointer } from "./pointer-selectors";

export function useManuallyDebouncedPointer() {
  const pointer = selectPointer();
  const [debounced, setDebounced] = React.useState(pointer.value);
  React.useEffect(() => {
    const id = window.setTimeout(() => setDebounced(pointer.value), 100);
    return () => window.clearTimeout(id);
  }, [pointer]);
  return debounced;
}
```

### ❌ Bad: treating selector outputs as event logs

```tsx
// BAD: selector values are latest-state projections and can coalesce writes.
import * as React from "react";
import { selectPointer } from "./pointer-selectors";

export function PointerAuditPanel({ audit }: { audit: Array<{ x: number; y: number }> }) {
  const pointer = selectPointer();
  React.useEffect(() => {
    audit.push(pointer.value);
  }, [audit, pointer]);
  return null;
}
```

### Prefer actions or sagas when every event matters

```ts
import { call, takeEvery } from "typed-redux-saga";
import { pointerMoved } from "./pointer-slice";

declare const auditLog: { write(event: string, payload: unknown): Promise<void> };

export function* pointerAuditSaga() {
  yield* takeEvery(pointerMoved, function* auditPointerMove(action) {
    yield* call(auditLog.write, "pointer-moved", action.payload[0]);
  });
}
```

## Verification cues

- Cadence is configured at the Store, not with consumer wrappers.
- Selector outputs are latest-state projections, not event logs.
- Consumer examples follow [Verification cues](../selector-lifecycle/SKILL.md#verification-cues).

## See also

- `../selectors/SKILL.md` — building `ReactStore` selectors.
- `../selector-lifecycle/SKILL.md` — choosing direct signal, `.useValue`, `.select`, `.effect`, and `.withStore` call modes.
- `@themislib/themis/docs/SELECTORS.md` — selector memoization and lifecycle rules.