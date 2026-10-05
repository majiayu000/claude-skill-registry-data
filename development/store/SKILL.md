---
name: svelte/store
description: >-
  Use for Svelte-readable Store imports and runtime lifecycle, including
  initialization, disposal, state, dispatch, runSaga, useInitStore, and
  useRunSaga.
type: sub-skill
requires:
  - svelte
  - core/import-boundaries
sources:
  - "@themislib/themis/svelte-store"
  - "@themislib/themis/components-svelte/use-init-store"
  - "@themislib/themis/components-svelte/use-run-saga"
  - "@themislib/themis/docs/ARCHITECTURE.md"
  - "@themislib/themis/README.md"
triggers:
  - Svelte Store class
  - svelte-store import
  - Svelte Store state lifecycle
  - useInitStore
  - useRunSaga
  - Svelte readable Store
---
# Store import and lifecycle

Use this skill when a task needs the canonical Svelte-readable Store variant. For shared state policy, reducers, actions, sagas, and package import boundaries, also follow the matching `core/*` skills.

This is Svelte Store family guidance for Svelte component and application code.

## Correct import and class choice

- Use `Store` from `@themislib/themis/svelte-store`.
- Do not import `Store` from the package root, `src/*`, or selector internals such as `utils/svelte-selectors/*`.

```ts
import { Store } from "@themislib/themis/svelte-store";

export const store = new Store({ todos: todosReducer });
// Initialize this instance inside the owning Svelte component, not this module.
```

## Lifecycle rules

- Construct `Store` with app-owned reducers and optional middleware, then call `store.init(initialState?)` during the owning Svelte component's initialization, before invoking direct selector calls. The current Svelte adapter reads component context in `init()`; fresh standalone service/test initialization throws `lifecycle_outside_component` (wrapped with guidance). Use real component initialization for adapter tests, or `.select(mockState)` for pure selector tests.
- Infer state with `StoreState<typeof store>` from `@themislib/themis/types`; avoid an explicit `: Store` annotation that loses constructor reducer-map inference. `getReducers()` returns a copy of the composed reducer map, including package-owned `@internal_` keys; filter those keys when reporting app registrations. `addMiddleware(...)` adds middleware before initialization. Custom middleware is prepended before the base chain.
- Direct selector calls return Svelte `Readable` outputs backed by the Store-owned state stream after initialization and throw before `init()` or after `dispose()`.
- If a Store runtime or context already exists in the Svelte component tree, `init()` skips setup and returns a noop disposer. Do not try to add child-layout reducers, middleware, or sagas by repeating `init()`; configure the owning Store instead.
- `init()` creates Redux/readable state and starts the package-owned saga manager, but does **not** start app sagas. Start each app saga explicitly after initialization; see **App saga lifetime** below.
- Capture the disposer returned by `init()` and register `onDestroy(dispose)` in a component owner. It is equivalent to `store.dispose()`, which stops Store-owned tasks/subscriptions, removes devtools registration, and is safe before initialization. Tests and non-component owners must also dispose their Store.
- `initDevTool()` explicitly registers an initialized Store for inspection and returns its own cleanup function; it is not part of normal bootstrap. See `../../core/debugging/SKILL.md` for diagnostics.
- Use `store.dispatch(action)` and `store.state` on the initialized Store. For async dispatch completion use `../../core/actions/SKILL.md`; for app selector creation use `../selectors/SKILL.md` → **Choose the factory**.
- Do not manually register package-owned `@internal_` reducers or internal sagas.

## App saga lifetime

- `store.runSaga(sagaFn)` derives the managed name from the function, starts the saga, and returns a per-saga cancel function. It throws before `init()` or for a reserved internal name; never start `@internal_sagaManager` yourself.
- In a component, `onMount(() => store.runSaga(sagaFn))` starts on mount and returns cancellation to Svelte for unmount. Remounting starts it again; this is not a once-per-Store-creation initializer.
- A service or test that receives an already component-initialized Store may keep `const cancel = store.runSaga(sagaFn)` and call `cancel()` when that operation ends. This does not make fresh standalone Svelte `Store.init()` supported.
- Per-saga cancellation is distinct from whole-Store teardown. Use the cancel function for ordinary mount/operation cleanup and `store.dispose()` only when the owner ends the Store lifetime.
- Framework-neutral lifetime placement lives in `../../core/sagas/SKILL.md` → **Application saga startup**; managed startup/cancellation/disposal lives in `../../core/saga-manager/SKILL.md` → **Store saga lifecycle**. Root-layout wiring lives in `../component-integration/SKILL.md` → **Root layout wiring**.

```ts
// The component owner has already initialized this Store and owns its disposal.
const cancel = store.runSaga(editorSaga);
cancel(); // end this saga's operation
```

## Svelte component lifecycle helpers

- `useInitStore(store, initialState?)` from `@themislib/themis/components-svelte/use-init-store` calls `store.init(initialState)` and disposes via `onDestroy`. Call it at component init time. Neither it nor `store.init()` installs Svelte component context.
- `useRunSaga(saga)` from `@themislib/themis/components-svelte/use-run-saga` reads Svelte component context and silently returns when it is absent. Ordinary `init()`/`useInitStore()` setup therefore does not enable this helper. No public provider/setup recipe currently fills that gap; do not invent one or rely on this helper for normal startup.
- Use the supported explicit component-owner path: `const dispose = store.init(); onDestroy(dispose); onMount(() => store.runSaga(sagaFn));`. See `../component-integration/SKILL.md` → **Root layout wiring**. The mount callback returns cancellation; it does not run during SSR. The bootstrap/lifetime owner may import its saga; ordinary handlers still dispatch actions, not invoke business sagas.
- Import these helpers from their leaf subpaths only, not from old `components/*` paths or a `components-svelte` directory barrel.

## Svelte Store guarantees

- `Store` is the only Store class whose selector direct calls return Svelte readables for `$selector$` template reads.
- Keep selector direct calls, component initialization, and readable template
  bindings within the Svelte Store lifecycle described above.

## Verification cues

- Imports use `@themislib/themis/svelte-store` for `Store` and `@themislib/themis/components-svelte/*` leaf subpaths for lifecycle helpers.
- Svelte examples initialize the Store in a real component before readable selector reads; tests distinguish real SSR context from browser mount behavior and assert unsupported standalone init where relevant.
- The app path initializes the Store before direct readable selector calls.

## See also

- `../selectors/SKILL.md` — `store.createSelector`, composition, and cache contracts.
- `../selector-lifecycle/SKILL.md` — component-init, handler, and saga call modes.
- `../component-integration/SKILL.md` — root layout wiring and template reactivity.
- `../../core/import-boundaries/SKILL.md` — public package import surface.

