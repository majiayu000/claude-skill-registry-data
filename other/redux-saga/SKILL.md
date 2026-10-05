---
name: core/redux-saga
description: >-
  Use for upstream redux-saga API semantics: middleware, runSaga, effects,
  watchers, channels, buffers, tasks, cancellation, context, and testing helpers.
  Themis saga rules take precedence.
type: sub-skill
requires:
  - core
  - core/sagas
sources:
  - https://redux-saga.js.org/docs/api
triggers:
  - redux-saga
  - redux saga API
  - createSagaMiddleware
  - saga effects
  - saga channels
  - runSaga
  - saga cancellation
  - saga testing
---
# redux-saga — API reference skill

> Source: official redux-saga API Reference, https://redux-saga.js.org/docs/api, retrieved 2026-05-15.

## Package guidance takes precedence

Use this leaf only for generic upstream redux-saga API behavior; it is not a
second core router. Read [Preflight](../SKILL.md#preflight), then follow
[Do](../sagas/SKILL.md#do) and [Implementation cues](../sagas/SKILL.md#implementation-cues)
for Themis `typed-redux-saga` / `yield*`, watcher ownership, and effect choices.
For the configured Store's `store.runSaga` API rather than upstream `runSaga`,
follow [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle).
Upstream examples below do not authorize replacing Store-owned middleware or
overriding those package-specific rules.

## Agent Preflight Compliance Contract

Before editing code or docs that use this skill:

- **MUST** identify whether the target code uses plain `redux-saga` or this repo's `typed-redux-saga` conventions; adapt examples accordingly.
- **MUST** cite this skill and any package-specific saga skill used in the handoff.
- **MUST** verify watcher ownership before adding `takeEvery`, `takeLatest`, `takeLeading`, `throttle`, or `debounce` for an existing trigger.
- **SHOULD** prefer native redux-saga channel-aware effects before adding wrapper utilities.
- **MUST NOT** introduce detached `spawn` in this repository; use attached `fork` so parent failure/cancellation also reaches children.
- **MUST** implement repository debounce with `takeLatest` or `takeLeading` plus `delay`, not action-wrapper debounce utilities.
- **NEVER** introduce runtime source, dependency, or artifact routing changes when only API guidance is requested.

## Setup — middleware and root saga startup

`createSagaMiddleware(options)` creates Redux middleware. Supported options include initial `context`, `sagaMonitor`, `onError`, `effectMiddlewares`, and a custom `channel` used by `take` and `put` effects.

In themis app setup, the concrete Store owns saga middleware creation. Use this low-level API reference to understand redux-saga behavior, but configure Store-owned monitoring by passing `{ sagaMonitor: true }` in the third `Store`/`ReactStore`/`StreamingStore` constructor options argument instead of replacing the middleware. Omitted or `false` saga monitoring remains disabled.

`middleware.run(saga, ...args)` returns a `Task` descriptor and drives yielded
plain Effect objects until the generator returns, throws, or is cancelled.
See [Common mistakes](#common-mistakes) for startup and cleanup requirements.

## Core patterns

### 1. Waiting and watcher helpers

Use `take(pattern)` for one action, `takeMaybe(pattern)` when the saga must receive the `END` sentinel instead of auto-terminating, and watcher helpers for common loops. Patterns can be `"*"`, strings, arrays, predicates, or action creators whose `toString()` returns an action type.

`takeEvery` runs concurrent workers, `takeLatest` cancels stale workers, and
`takeLeading` ignores new triggers while a worker runs. Generic patterns include
wildcards; Themis code must instead use concrete action creators/arrays or
selector channels as required by [Do](../sagas/SKILL.md#do).

`takeEvery`, `takeLatest`, `takeLeading`, `throttle`, and `debounce` also accept a
`Channel` in place of a pattern; see [Common mistakes](#common-mistakes) before adding wrappers.

### 2. Blocking and non-blocking effects

`call`, `apply`, and `cps` are blocking; `fork` and `spawn` start work without blocking the parent. `fork` is attached to the parent: parent completion waits for children, child errors bubble upward, and cancellation propagates downward. `spawn` is detached and does not share parent completion, error, or cancellation flow.

```typescript
import { call, cancel, cancelled, fork, join } from "redux-saga/effects";

function* worker() {
  try {
    yield call(api.sync);
  } finally {
    if (yield cancelled()) yield call(api.abortSync);
  }
}

function* supervisor() {
  const attachedTask: Task = yield fork(worker);
  const metricsTask: Task = yield fork(backgroundMetrics);
  yield cancel(metricsTask);  // non-blocking cancellation request
  yield join(attachedTask);   // blocking wait for attachedTask outcome
}
```

Use `cancel(task)`, `cancel([...tasks])`, or `cancel()` for self-cancellation. Cancellation calls the generator's `return()`, jumps to `finally`, and cancels the currently blocked effect plus attached child tasks.

### 3. Store I/O, state reads, context, and timing

Use `put(action)` for scheduled dispatch, `putResolve(action)` when dispatch returns a Promise and the saga must wait, `put(channel, message)` for channel output, and `select(selector, ...args)` for state reads. `setContext(props)` merges saga context; `getContext(prop)` reads one context value. `delay(ms, value)` blocks for time.

`retry(maxTries, delayMs, fn, ...args)` is a blocking helper built from `call` and `delay`: it retries failures until success or attempts are exhausted, then rethrows the last error.

### 4. Channels, buffers, and cleanup

Use `actionChannel(pattern, buffer?)` to queue matching store actions while a
worker is blocked, `channel(buffer?)` for task-to-task messages, and `eventChannel`
to bridge external sources. Use `flush(channel)` to recover buffered messages;
follow [Common mistakes](#common-mistakes) for unsubscribe/close ownership.

Buffer choices: `buffers.none()`, `fixed(limit)`, `expanding(initialSize)`, `dropping(limit)`, and `sliding(limit)`. The default `channel()` uses an expanding FIFO buffer: ten is its initial capacity, not a maximum. Choose an explicit bounded buffer when backlog memory must be limited; that choice also determines overflow behavior.

```typescript
import { buffers, channel } from "redux-saga";

const defaultQueue = channel<number>(); // expands: retains all 25 queued messages
const recentQueue = channel<number>(buffers.sliding(10)); // keeps the latest ten
const firstQueue = channel<number>(buffers.dropping(10)); // drops new arrivals when full
const strictQueue = channel<number>(buffers.fixed(10)); // throws on the eleventh put
```

These examples assume no pending taker. `eventChannel` is different: it defaults to no buffer, so pass one explicitly if events must wait for a consumer. Close owned queues when their lifetime ends.

### 5. Concurrency combinators and helpers

Use `race` when the first completion wins; losing effects are automatically cancelled. Use `all` to run effects in parallel and wait for all successes, or throw when any effect rejects.

`throttle(ms, patternOrChannel, saga, ...args)` suppresses new starts during the window.
Its pattern overload creates an action channel with `buffers.sliding(1)`;
a supplied channel retains its caller-chosen buffering/overflow policy.
For latest-pending external messages, explicitly use `buffers.sliding(1)` when
creating the supplied `channel` or `eventChannel`, rather than assuming throttle adds it.

Here a producer puts progress messages into `latestMessages`; the owner joins its
attached watcher and closes its channel. `handleMessage` is the app's worker.

```typescript
import { buffers, channel } from "redux-saga";
import { join, throttle } from "redux-saga/effects";

const latestMessages = channel<{ value: number }>(buffers.sliding(1));
function* watchLatestMessages() {
  try {
    yield join(yield throttle(100, latestMessages, handleMessage));
  } finally {
    latestMessages.close();
  }
}
```

Upstream's native
`debounce(ms, patternOrChannel, saga, ...args)` waits until messages settle before
forking the worker; Themis restrictions are in [Common mistakes](#common-mistakes).

## Interface quick reference

| Interface | What agents need to know |
| --- | --- |
| Task | Returned by fork, spawn, middleware.run, and runSaga; supports isRunning(), isCancelled(), result(), error(), toPromise(), and cancel(). |
| Channel | Message queue with take(callback), put(message), flush(callback), and close(); closed empty channels deliver END. |
| Buffer | Strategy behind a channel; implements isEmpty(), put(message), and take(). |
| SagaMonitor | Receives rootSagaStarted, effectTriggered, effectResolved, effectRejected, effectCancelled, and actionDispatched events for instrumentation. |

## Blocking / non-blocking cheat sheet

| Effect | Blocking? | Notes |
| --- | --- | --- |
| take, takeMaybe, call, apply, cps, join, putResolve, cancelled, delay, retry, race | Yes | race blocks until one branch wins, then cancels losers. |
| put, fork, spawn, cancel, actionChannel, flush, select, setContext, getContext | No | select resolves immediately against current state. |
| put(channel, message) | Depends | It can block when an unbuffered put is consumed immediately by a taker. |
| all([...]) / all({ ... }) | Mixed | Blocks until all child effects complete; child effect types determine actual waits. |
| takeEvery, takeLatest, takeLeading, throttle, debounce | No | Helpers fork watcher tasks; their internals may use blocking effects. |

## External execution with `runSaga`

`runSaga(options, saga, ...args)` starts a saga without Redux middleware. Provide a `channel` for `take`, a `dispatch(output)` function for `put`, and `getState()` for `select`. It returns the same `Task` interface as `middleware.run`.

```typescript
import { runSaga, stdChannel } from "redux-saga";
import { put, take } from "redux-saga/effects";

function* auditSaga() {
  const action: { type: string } = yield take("AUDIT");
  yield put({ type: "AUDITED", action });
}

const dispatched: Array<{ type: string; action?: { type: string } }> = [];
const input = stdChannel();
const task = runSaga(
  { channel: input, dispatch: (output) => dispatched.push(output), getState: () => ({}) },
  auditSaga,
);

input.put({ type: "AUDIT" });
await task.toPromise();
```

## Testing helpers

- `cloneableGenerator(generatorFunc)` from `@redux-saga/testing-utils` creates cloneable generator instances for branch testing without replaying setup yields.
- `createMockTask()` from `@redux-saga/testing-utils` returns a mock `Task` for testing `fork`, `join`, and `cancel` flows.
- Prefer effect-level assertions for small generators and integration-style saga tests for cancellation, channel cleanup, and watcher concurrency.

## Common mistakes

- Do not call `middleware.run` before mounting saga middleware on the Redux store;
  mount first, then start the root saga.
- Do not treat `take` and `takeMaybe` as equivalent on `END`: `take` auto-terminates;
  use `takeMaybe` when the saga must handle the closed-input sentinel itself.
- Do not introduce detached `spawn` in this repository; use attached `fork` so
  parent cancellation reaches children and child failures remain visible.
- Do not leave external subscriptions or owned channels open: `eventChannel`
  subscribe functions must return unsubscribe callbacks; close owned channels in `finally`.
- Do not rely on `channel()` to bound a backlog; its default buffer expands. Choose and test an explicit overflow policy.
- Do not wrap native channel-aware watchers without added value; use their channel
  overloads unless a wrapper provides documented cleanup, typing, or domain behavior.
- Do not use native `debounce` in Themis examples or add wrapper-action debounce
  utilities; watch the real action with `takeLatest`/`takeLeading` and `delay` in the worker.

## See also

- `../sagas/SKILL.md` — repository-specific typed-redux-saga conventions.
- `../channel-effects/SKILL.md` — package-provided channel consumer wrappers and when they add cleanup value.
- `../testing/SKILL.md` — repository-specific saga test patterns and mocks.