---
name: streaming/store
description: >-
  Use @themislib/themis/streaming-store for StreamingStore imports,
  init/dispose, process bootstrap, and whole-Store ownership. Route selector call
  validity and subscriptions to streaming/selector-lifecycle.
type: sub-skill
requires:
  - streaming
  - core/import-boundaries
sources:
  - "@themislib/themis/streaming-store"
  - "@themislib/themis/docs/ARCHITECTURE.md"
  - "@themislib/themis/README.md"
triggers:
  - StreamingStore
  - streaming-store import
  - Streaming Store state lifecycle
  - Kefir Store
  - observable Store
---
# StreamingStore import and lifecycle

Use this skill when a task needs the Kefir/observable Store variant. For shared state policy, reducers, actions, sagas, and package import boundaries, also follow the matching `core/*` skills.

This is Streaming Store family guidance. For the same app/package/code path, do not apply alternate Store-family or lifecycle patterns.

## Correct import and class choice

- Use `StreamingStore` from `@themislib/themis/streaming-store`.
- Do not import `StreamingStore` from the package root, `src/*`, or `utils/streaming-selectors/*`.

```ts
import { StreamingStore } from "@themislib/themis/streaming-store";
import type { StoreState } from "@themislib/themis/types";

export const streamStore = new StreamingStore({ todos: todosReducer });
export type AppState = StoreState<typeof streamStore>;
```

## Lifecycle rules

- The process/server/worker/test owner constructs the `StreamingStore` with app-owned reducers and optional middleware/options, calls `streamStore.init(initialState?)`, and retains the returned disposer for that owner's shutdown.
- Initialization creates the Redux runtime and its Store-owned Kefir state source. The returned disposer delegates to `streamStore.dispose()` for whole-Store teardown. Selector invocation errors and observation timing are owned by `../selector-lifecycle/SKILL.md` — **Lifecycle map** and **Operational guardrails**.
- Preserve constructor inference with `StoreState<typeof streamStore>` rather than widening the configured instance. For reducer registration, state shape, and reserved package-owned domains, read `../../core/file-structure/SKILL.md` — **Register a normal slice** and `../../core/saga-manager/SKILL.md` — **Store saga lifecycle**.
- Use the initialized instance for `streamStore.state` and `streamStore.dispatch`; action/async-dispatch semantics belong to `../../core/actions/SKILL.md` — **Await dispatch when the caller needs the result**. App-saga placement belongs to `../../core/sagas/SKILL.md` — **Application saga startup**; startup, cancellation, and internal-manager boundaries belong to `../../core/saga-manager/SKILL.md` — **Store saga lifecycle**.

## Process bootstrap

Keep initialization and shutdown at one non-UI owner boundary. Application-specific saga and observer logic stay in their own modules; this example assumes `todosSaga` and `startConsumers` are app-owned functions.

```ts
const dispose = streamStore.init();
const cancelTodosSaga = streamStore.runSaga(todosSaga);
const stopConsumers = startConsumers();
// When the process/test owner ends:
stopConsumers();
cancelTodosSaga();
dispose();
```

For the Kefir subscription implementation behind `startConsumers`, read `../selector-lifecycle/SKILL.md` — **Consumer subscription ownership**. Store initialization does not start app sagas; follow `../../core/saga-manager/SKILL.md` — **Store saga lifecycle** for their explicit registration.

## Logging and tracing streams

StreamingStore uses the cross-family diagnostics contract, not a separate Kefir
logging API. Read `../../core/selector-tracing/SKILL.md` — **Configure the Store**,
**Aggregate summaries**, and **Store-family symmetry and lifecycle** for tracing
options, summary allocation, and selector-resource cleanup.
Read `../../core/redux-action-logging/SKILL.md` — **Store-owned logging streams**,
**Logger factory lifecycle**, **Read one action's group**, and **Keep logging
opt-in and temporary** for the read-only stream inventory/types, logger
replacement/disposer and reinitialization, middleware events, and rendering. Direct Kefir consumers
follow `../selector-lifecycle/SKILL.md` — **Consumer subscription ownership**;
they do not take over Store-owned logger or timer cleanup.

## Streaming family boundary

- `StreamingStore` selector direct calls return Kefir observables.
- Keep one concrete Store selector and lifecycle pattern per app/code path.

## Verification cues

- Imports use `@themislib/themis/streaming-store` for `StreamingStore`.
- Examples and docs do not describe `Store` as a streaming API.
- Process/test shutdown invokes the Store disposer and the app-owned saga cancel functions.
- Selector usage follows `../selector-lifecycle/SKILL.md` — **Verification cues**, including error-path tests when applicable.

## See also

- `../selectors/SKILL.md` — **Call forms** for the Kefir selector return model.
- `../selector-lifecycle/SKILL.md` — **Lifecycle map** for invocation/teardown timing.
- `../../core/import-boundaries/SKILL.md` — **Setup — the package export surface**.