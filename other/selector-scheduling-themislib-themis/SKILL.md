---
name: svelte/selector-scheduling
description: >-
  Use for Svelte Store selector emission coalescing, rAF scheduling, or FPS
  tuning. Keep scheduling owned by Store; do not wrap selectors or import
  scheduler internals. Authoring/cache and call modes have separate owners.
type: sub-skill
requires:
  - svelte
  - svelte/selectors
triggers:
  - throttled readable
  - rAF coalescing
  - selector scheduler
---
# Selector emission scheduling — internal only

> Selector scheduler helpers are implementation details. Do not import them from package subpaths or teach consumers to wrap selector readables manually.

Public facade: `@themislib/themis/svelte-store` (`store.createSelector` and `Store` selector options). Selector implementation and scheduler internals are package-private; see `@themislib/themis/docs/SELECTORS.md` for behavior.

## Scheduling options

- Tune Svelte-readable selector coalescing only through the final constructor options argument: `new Store(reducers, middleware, { throttledSelectorFrequency })`.
- Treat this as Svelte Store family scheduling. Use the Store-owned scheduler
  rather than adding a second scheduling layer.
- Omit `throttledSelectorFrequency` for the default `64` FPS; explicit values must be finite numbers in the inclusive `1..256` range. Fractional values are supported.
- Selector trace output is disabled by default; pass `{ traceSelectors: true }` in the final Store options object only for temporary diagnostics.

Scheduling does not change which call mode is valid. Use
`../selector-lifecycle/SKILL.md` → **Call-mode map** for components, handlers,
services, tests, saga reads, and explicit binding; its **Bind explicitly with .withStore when no Svelte context is available**
section covers initialization and subscription cleanup. Authoring and cache reuse
live in `../selectors/SKILL.md` → **Choose the factory** and **Selector caching**.

## Do not

- Do not import selector scheduler internals from app code.
- Do not wrap Store-created selectors, selector callbacks, selector calls, or selector readables in extra `memoize`, `cache`, debounce/throttle, timer, `requestAnimationFrame`, scheduler, or writable-proxy layers just to reduce recomputes or UI updates.
- Do not rely on selector readables as audit/event streams; they represent the latest derived state and may coalesce intermediate writes.
- Respect `../selector-lifecycle/SKILL.md` → **Don't** even when a readable is cached or scheduled.

## Examples

### Configure coalescing on the Store

```ts
import { Store } from "@themislib/themis/svelte-store";
import { pointerReducer } from "./pointer-slice";

export const store = new Store({ pointer: pointerReducer }, [], {
  throttledSelectorFrequency: 30,
});
```

Define and compose selectors with `../selectors/SKILL.md` → **Examples**;
consume them using `../selector-lifecycle/SKILL.md` → **Examples**. The same
Store-owned scheduling applies without a custom wrapper or copied call-mode recipe.

### 6. ❌ Bad: wrapping selector readables in another cache or timer layer

```ts
// BAD: this compiles but adds stale updates on top of Store-owned caching/scheduling.
import { writable, type Readable } from "svelte/store";
import { selectPointer } from "./pointer-selectors";

type Pointer = { x: number; y: number };

export function createManuallyDebouncedPointer(): Readable<Pointer> {
  const output = writable<Pointer>({ x: 0, y: 0 });
  selectPointer().subscribe((value) => setTimeout(() => output.set(value), 100));
  return output;
}
```

### 7. ❌ Bad: treating selector readables as event logs

```ts
// BAD: selector readables represent latest state and may coalesce intermediate writes.
import { selectPointer } from "./pointer-selectors";

type Pointer = { x: number; y: number };

export function recordEveryPointerMove(audit: Pointer[]) {
  const unsubscribe = selectPointer().subscribe((pointer) => audit.push(pointer));
  return unsubscribe;
}
```

### 8. Prefer action or saga evidence when every event matters

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

- FPS values satisfy **Scheduling options**; default behavior needs no extra scheduler.
- Consumers needing every event use action/saga evidence, not coalesced state readables.
- Validate call sites against `../selector-lifecycle/SKILL.md` → **Verification cues**.

## See also

- `../selectors/SKILL.md` — building Store-bound selectors and cache contracts.
- `../selector-lifecycle/SKILL.md` — selector call-site modes and cleanup.
- `@themislib/themis/docs/SELECTORS.md` — selector memoization and lifecycle rules.