---
name: streaming/selectors
description: >-
  Author StreamingStore selectors returning Kefir Observable values, with
  observable arguments, Store binding, pure .select composition/tests, and saga
  .effect calls. Keep streaming selector internals private.
type: sub-skill
requires:
  - streaming
  - core/state-integrity
sources:
  - "@themislib/themis/streaming-store"
  - package-internal streaming selector implementation
  - "@themislib/themis/docs/SELECTORS.md"
triggers:
  - streaming selector
  - Kefir selector
  - observable selector
  - selector stream args
  - StoreStreamingSelector
---
# Streaming selectors — Kefir/observable call model

Use this skill when `store.createSelector(...)` belongs to a `StreamingStore` and
direct selector calls should produce Kefir `Observable<R, any>` results.

This Streaming selector model is exclusive to the StreamingStore family for the
same app/package/code path. Do not apply alternate Store capture, template, or
lifecycle/setup guidance here.

## Authoring rules

- Create selectors through the configured `StreamingStore` instance.
- Keep this app on the Streaming Store family and keep alternate frontend patterns
  isolated to separate app/code paths.
- For pure derived callbacks and canonical state ownership, follow
  `../../core/state-integrity/SKILL.md` — **MUST / NEVER rules**.
- Compose selectors with `.select(state, ...args)` inside another selector.
- Keep generic selector helper modules Store-parameterized: accept a configured
  store and call `store.createSelector(...)` at the integration boundary.
- Trust Store-owned selector-result and observable-output caching; do not add extra memoize/cache/debounce/throttle wrappers solely for performance.
- Prefer primitive scalar selector arguments over freshly constructed object,
  array, or function arguments; object/function args are valid only when their
  identity is stable and intentional.
- Do not import from any `themis` streaming-selector internal deep path; those are
  implementation internals, not package API.

```ts
import { StreamingStore } from "@themislib/themis/streaming-store";

export const streamStore = new StreamingStore({ todos: todosReducer });
export const selectTodoCount = streamStore.createSelector((state) => {
  return state.todos.collection.ids.length;
});
```

This module defines selectors without reading stream state. Before invoking
them, follow `../selector-lifecycle/SKILL.md` — **Lifecycle map**; for observation
and cleanup examples use **Consumer subscription ownership** in that same skill.

## Call forms

| Context | Use | Result |
| --- | --- | --- |
| Streaming consumer | `selectFoo(...argsOrArgStreams)` | Kefir `Observable<R, any>` |
| Explicit StreamingStore binding | `selectFoo.withStore(streamStore)(...args)` | Kefir `Observable<R, any>` |
| Tests/handlers/composition | `selectFoo.select(state, ...args)` | Plain value `R` |
| Sagas | `yield* selectFoo.effect(...args)` | typed-redux-saga select effect |

Selector arguments may be plain values or Kefir observables. Plain values are
lifted to constant streams before combining with the Store state stream.
The owning Store's `throttledSelectorFrequency` option (default `64` FPS)
cadences Store-state changes, not the combined selector output. Plain-argument
selectors have a prompt initial value; an observable argument must first emit
before the selector can emit. Later rapid Store writes coalesce to the latest
state at a scheduled tick. Observable-argument changes can recompute and emit
changed results immediately using the latest emitted Store state, even within
that interval. The option is not an overall output-rate cap. There is no separate
public fast-selector API; `.select(store.state, ...plainArgs)` and saga `.effect`
are uncadenced one-shot reads. For opt-in diagnostics and constructor
options, read `../../core/selector-tracing/SKILL.md` — **Scope and safety rules**
and **Configure the Store** rather than adding a Streaming-specific trace policy.

Selector-channel helpers use the shared selector read shape, not direct Kefir
outputs. Their saga-context subscription behavior and plain stable argument
tuples are owned by `../../core/selector-channels/SKILL.md` — **Do** and
**Implementation cues**; one-shot waits belong to `../../core/wait-for/SKILL.md`
— **Do**. Saga read conventions belong to `../../core/sagas/SKILL.md` — **Do**.

## Selector caching

- Store-created selectors have internal selector-result caching/memoization.
- Direct Kefir `Observable` outputs are cached per StreamingStore instance + selector + arguments. Never-observed outputs and concurrent live consumers reuse the same observable. Removing one of several consumers retains it; removing the final observer evicts that output even if JavaScript references remain. The next identical call creates a new observable. Store disposal evicts all its outputs; cache counts are not active-observer counts.
- `.withStore(streamStore)` accepts an initialized StreamingStore object, not its raw Kefir stream. That Store is the cache source key and supplies state for computation. Two Store objects have separate cache entries even if they expose the same internal state stream.
- Do not wrap selector callbacks or selector calls in extra `memoize`, `cache`, manual cache maps, debounce, or throttle layers solely for performance.
- Prefer the same Store-bound selector + same arguments over props drilling/manual stream passing when the receiving consumer can reasonably call the selector in valid streaming setup; otherwise use `.select`, `.effect`, or `.withStore` as the context requires.

## Stable selector arguments

- Prefer primitive scalar selector arguments: ids, booleans, enum strings,
  numbers, `null`, or `undefined`.
- Do not pass freshly constructed object, array, or function arguments to direct
  `selectFoo(...)`, `.select(state, ...)`, `.effect(...)`, `.withStore(store)(...)`,
  selector-channel args tuples, or `waitFor` args tuples.
- Object/function args are valid only when the identity is stable and intentional,
  such as a module constant, memoized config, existing source object, or Kefir
  observable. Observable arguments are valid direct-call inputs when the stream is
  owned elsewhere; do not recreate a stream solely for a selector call.
- Prefer selector definitions like `(state, id, status)` over `(state, { id,
  status })`; destructure an object arg only when callers pass a documented stable
  reference.

## Collection reads

Use public collection utilities in selector callbacks when a package-level helper
is needed, and compose through `.select(state)` when another selector owns the
collection read.

```ts
import { getItem } from "@themislib/themis/utils/collections/collection-utils";

export const selectTodo = streamStore.createSelector((state, id: string) => {
  return getItem(state.todos.collection, id);
});
```

## Don't

- Do not teach alternate Store syntax or lifecycle setup for `StreamingStore`
  selectors.
- Do not call another selector's direct streaming form inside a selector callback;
  use `.select(state)` to keep composition pure and synchronous.
- Do not props-drill derived values solely to avoid selector calls when the consumer can call the same Store-bound selector with the same args in a valid streaming context.
- Do not add manual memoization/cache/debounce/throttle wrappers inside selector callbacks or around observable selector calls just to improve selector performance.
- Do not use standalone streaming selector utilities as public package imports.
- Do not construct `{ ... }`, `[ ... ]`, `() => ...`, or new argument streams inline
  just to call a selector; pass scalar args or stable intentional references.

## Verification cues

- Streaming selector examples return/observe Kefir observables only after the
  `StreamingStore` has been initialized.
- Unit tests for pure selector logic use `.select(mockState, ...args)`.
- Static scans show no public imports from `utils/streaming-selectors`.

## See also

- `../store/SKILL.md` — **Correct import and class choice**.
- `../selector-lifecycle/SKILL.md` — **Lifecycle map** for invocation and teardown timing.
- `../../core/state-integrity/SKILL.md` — **MUST / NEVER rules** for derived-value ownership.
