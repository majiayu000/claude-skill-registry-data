---
name: core/sagas
description: >-
  Use when writing typed-redux-saga watchers/workers, assigning ownership and
  app startup placement, debouncing, retrying with retryWithTimeout, or using
  wrapStreamingGenerator. Route lifecycle/crash/restart mechanics to core/saga-manager.
type: sub-skill
requires:
  - core
  - core/actions
  - core/state-integrity
triggers:
  - takeEvery saga
  - application saga startup
  - debounce saga
  - retryWithTimeout
  - wrapStreamingGenerator
  - typed redux saga
  - typed-redux-saga
---
# Sagas — agent implementation rules

Use this skill when editing saga code or writing instructions for saga changes. Keep this file short and operational; `@themislib/themis/docs/SAGAS.md` is the canonical human-facing guide for concepts, API shape, tradeoffs, and examples.

## Canonical references

- Human guide: `@themislib/themis/docs/SAGAS.md`
- Public API: `@themislib/themis/saga`; utility leaf exports include `@themislib/themis/utils/sagas/debounce-saga`, `@themislib/themis/utils/sagas/retry-with-timeout`, and `@themislib/themis/utils/sagas/wrap-async-generator`. Store-utility saga internals are implementation context only.
- Related skills: `core/actions`, `core/state-integrity`, `core/saga-manager`, `core/selector-channels`, `core/wait-for`, `core/testing`

## When to use sagas

- Use sagas for side effects, orchestration, persistence, timers, event listeners, and async workflows.
- Use selector-channel helpers when the trigger is a selector value change, not an action.
- Use `waitFor` for one-shot suspension until state reaches a predicate; do not use it for continuous monitoring.

## Do

- Use `typed-redux-saga` effects with `yield*` for every effect.
- Pass action creators directly to `take`, `takeEvery`, `takeLatest`, and `takeLeading`; do not pass `.type`.
- Read state through named selectors with `.effect(...)` inside sagas.
- Import the named selectors from the owning slice's `[slice]-selectors.ts` file; saga modules must not declare local `select*` functions/factories, even when they are not exported.
- Subscribe with concrete action creators, action-creator arrays, or selector-channel helpers; never use `take('*')` or other wildcard takes.
- Search before adding watchers: trigger action, worker name, registration name, and operation terms must have one canonical owner unless fan-out is intentional and documented.
- Choose an explicit owner for app saga startup; follow [Application saga startup](#application-saga-startup) and the linked lifecycle contract.
- Close manually-created channels in `finally`.
- Handle async action failures with `.failure(error)` and normalize non-`Error` throws.
- Settle promise-bearing requests through their instance callbacks on success, failure, and cancellation; see the explicit rejection policy in `core/actions`.
- Keep retried work idempotent when using `retryWithTimeout`.
- Keep stream handlers passed to `wrapStreamingGenerator` package-generic; do not add app-specific logging/reporting dependencies to the utility.
- Configure optional saga monitoring through the third Store/ReactStore/StreamingStore constructor options object as `{ sagaMonitor: true }`; omitted or `false` monitors stay disabled.

## Don't

- Do not put side effects in reducers or selector predicates.
- Do not call `selector.select(store.state, ...)` from saga-reachable code; convert the helper path to generators or pass values in.
- Do not declare or factory-construct `select*` selectors inside saga modules, even as module-private locals; move them to the owning `[slice]-selectors.ts` and import them.
- Do not subscribe to every action with `take('*')`, `takeEvery('*', ...)`, or other wildcard patterns; it wakes the saga on every dispatch and is especially harmful during streaming flows where chunk actions fire continuously.
- Do not add a parallel watcher for an action already owned by another saga.
- Do not treat initialization or manager internals as app saga registration; follow [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle) for startup and the public/internal boundary.
- Do not leave channels, retries, or long-running loops without cancellation/error paths.
- Do not assume `wrapStreamingGenerator` aborts/finalizes its source, or that `iterator.return()` interrupts a pending `next()`.
- Do not introduce detached `spawn`; use attached `fork` so child work is cancelled when the parent fails or is cancelled.
- Do not monkey-patch redux-saga globally or replace Store-owned saga middleware to observe effects; pass `{ sagaMonitor: true }` in Store options instead.

## Implementation cues

- Default user-triggered fetch/search flows to `takeLatest`; use `takeEvery` when every action must be processed and `takeLeading` when in-flight work should ignore newer triggers. For promise-bearing requests, cancelled workers need a `finally` settlement policy. Ignored `takeLeading` requests never enter a worker: use non-promise `createAction` triggers or an explicit admission/rejection owner instead.
- Compose root sagas from focused watcher/worker functions rather than mixing unrelated concerns in one worker.
- For debounce, watch the real action with `takeLatest` and call `delay(ms)` inside the worker before the effect; use `takeLeading` plus trailing `delay(ms)` only for leading/windowed behavior.
- Do not add new wrapper-action debounce flows or recommend `debounceSaga`/`debounceWithKeySaga` for new work; those exports remain for compatibility only.
- For transient failures, use `retryWithTimeout` and branch on all outcomes: `success`, `retries-exhausted`, and `timeout`.
- For async generators, use `wrapStreamingGenerator` from saga code and handle stream errors locally at the call site if app reporting is needed.
- For saga lifetime placement in components, services, or tests, follow [Application saga startup](#application-saga-startup); per-owner cancellation and whole-Store teardown belong to [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle).
- For saga monitoring, keep the normal constructor shape and pass `new Store(reducers, middleware, { throttledSelectorFrequency, sagaMonitor: true })` or the equivalent `ReactStore`/`StreamingStore` options object.
- For saga manager crash records and cleanup, read [Core Patterns](../saga-manager/SKILL.md#core-patterns); for auto-restart and backoff, read [Start, stop, restart, and backoff mechanics](../saga-manager/SKILL.md#start-stop-restart-and-backoff-mechanics).

## Application saga startup

Choose the lifetime owner before wiring app sagas: app-wide work belongs to the
application root or service lifetime; component/layout work belongs to that
component/layout lifetime; tests own their setup and cleanup explicitly. Use the
selected Store family's lifecycle skill for its framework hook or runtime boundary,
not a hook prescribed by core.

Place explicit app saga startup beside that owner's initialization/cleanup wiring.
Follow [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle) for
initialization order, `store.runSaga(sagaFn)`, matching cancel functions, and the
whole-Store disposal boundary. For slice modules and registration placement, use
[Register a normal slice](../file-structure/SKILL.md#register-a-normal-slice).

The [bootstrap/lifetime-owner exception](../import-boundaries/SKILL.md#bootstrap-and-lifetime-owner-exception) permits only startup/cleanup imports; ordinary component/service handlers still dispatch actions rather than import or call business sagas.

## Examples

### 1. Register one canonical action watcher and read state through selector effects

```ts
import { call, put, takeLatest } from "typed-redux-saga";

function* watchLoadTodos() {
  yield* takeLatest(loadTodos, loadTodosWorker);
}

function* loadTodosWorker() {
  const userId = yield* selectCurrentUserId.effect();
  const todos = yield* call(api.fetchTodos, userId);
  yield* put(loadTodosSuccess(todos));
}
```

### 2. Debounce trailing user input with takeLatest + delay

```ts
import { call, delay, put, takeLatest } from "typed-redux-saga";

function* watchSearchInput() {
  yield* takeLatest(searchInputChanged, function* searchAfterSettled(action) {
    yield* delay(300);
    const results = yield* call(api.search, action.payload[0]);
    yield* put(searchResultsLoaded(results));
  });
}
```

### 3. Debounce leading/windowed behavior with takeLeading + delay

Here `refreshRequested` is an ordinary `createAction` event, not a promise-bearing `createAsyncAction`: ignored triggers have no result to await.

```ts
import { call, delay, takeLeading } from "typed-redux-saga";

function* watchRefreshRequests() {
  yield* takeLeading(refreshRequested, function* refreshOncePerWindow(action) {
    try {
      yield* call(api.refresh, action.payload[0]);
    } finally {
      yield* delay(250);
    }
  });
}
```

### 4. Branch on every retryWithTimeout outcome

```ts
import { call, put } from "typed-redux-saga";
import { retryWithTimeout } from "@themislib/themis/saga";

function* syncRemoteState() {
  const outcome = yield* retryWithTimeout(
    function* () { yield* call(api.syncRemoteState); },
    { maxRetries: 2, timeoutMs: 30_000, getDelayMs: (attempt) => 500 * (attempt + 1) }
  );

  if (outcome === "retries-exhausted") yield* put(syncFailed("retry-limit"));
  if (outcome === "timeout") yield* put(syncFailed("timeout"));
}
```

### 5. Consume an async generator through wrapStreamingGenerator

```ts
import { call, put } from "typed-redux-saga";
import { wrapStreamingGenerator } from "@themislib/themis/saga";

function* streamMessages(
  openStream: (signal: AbortSignal) => AsyncGenerator<MessageChunk, MessageChunk | null | undefined, unknown>
) {
  const controller = new AbortController();
  const stream = openStream(controller.signal);
  try {
    yield* wrapStreamingGenerator(
      stream,
      function* (chunk) { yield* put(messageChunkReceived(chunk)); },
      { timeoutMs: 30_000, onError: (error) => reportStreamError(error) }
    );
  } finally {
    controller.abort(); // source must use this to unblock any pending next()
    try {
      yield* call([stream, stream.return], undefined);
    } catch (error) {
      reportStreamError(error); // cleanup failure must not replace the original error
    }
  }
}
```

`openStream` is app-provided and must honor abort, settle outstanding reads promptly, and release its resource in its own `finally`; `reportStreamError` must be non-throwing. The helper itself neither aborts nor calls `return()` on timeout/cancellation. Abort first: an async generator queues `return()` behind a pending `next()`, so `return()` alone cannot unblock I/O. Without a source abort/cancel contract this example cannot guarantee prompt cleanup. Cancellation is non-blocking; if another owner must wait for finalization, expose and await a separate source-completion signal rather than treating `task.cancel()`/`toPromise()` as a cleanup barrier.

## Verification cues

- Add or update saga tests with the package testing patterns; see `core/testing`.
- Check for duplicate watchers/registrations with targeted searches before and after edits.
- Verify `.effect(...)` selector reads are mockable with `expectSaga.provide()` when tests cover saga state reads.
- Run the smallest relevant test target when documentation examples changed.

## See also

- `@themislib/themis/docs/SAGAS.md` — full saga concepts, APIs, and examples.
- [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle) and [Core Patterns](../saga-manager/SKILL.md#core-patterns) — canonical lifecycle, crash storage/cleanup, restart, and backoff mechanics.
- `core/selector-channels` — selector change watchers and selector-backed channels.
- `core/wait-for` — one-shot selector predicate waits.
- `core/channel-effects` — generic `EventChannel` consumers.
- `core/local-storage` — persistence saga helpers.
- `core/testing` — saga test setup and mocks.
