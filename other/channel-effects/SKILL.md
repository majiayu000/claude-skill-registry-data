---
name: core/channel-effects
description: >-
  Use for consuming app-provided EventChannels in sagas, including websocket,
  DOM, IPC, and cleanup. For selector-derived channels, use
  core/selector-channels.
type: sub-skill
requires:
  - core
  - core/sagas
triggers:
  - take every channel
  - take latest channel
  - EventChannel consumer
  - channel cleanup
---
# Channel Effects — generic EventChannel consumers

> Use native redux-saga `takeEvery(channel, worker)` for every-event `EventChannel<T>` consumption and `takeLatest(channel, worker)` when each new event should cancel the previous worker.

Source: redux-saga channel watcher effects, [Native channel watchers](#native-channel-watchers).

## Imports

```typescript
import type { EventChannel } from "redux-saga";
import { call, join, take, takeEvery, takeLatest } from "typed-redux-saga";
```

## Native channel watchers

```typescript
const watcher = yield* takeEvery(channel, worker); // or takeLatest
yield* join(watcher); // keep the resource owner's try block alive
```

Use typed effects with `yield*`; raw `redux-saga/effects` descriptors are not iterable. `takeEvery` and `takeLatest` fork an attached watcher and return its Task immediately. They do not own app-created channels. Keep the owner's `try` block alive with `join(watcher)` and close the channel in `finally`; otherwise it closes at startup, before later events arrive. Parent cancellation cancels attached workers and enters the owner's cleanup. Channel END finishes the watcher after attached workers finish.

## Core Patterns

### 1. Fork a new worker for every event

```typescript
// createAppEventChannel is app-provided and returns EventChannel<MyEvent>
const channel = createAppEventChannel<MyEvent>("my:event");
try {
  const watcher = yield* takeEvery(channel, function* (data) {
    yield* call(handleEvent, data);
  });
  yield* join(watcher);
} finally {
  channel.close();
}
```

Every delivered event spawns a new worker concurrently — use when events are independent. Keep ownership of app-created channels explicit and close them in `finally`.

### 2. Cancel the previous worker for each new event

```typescript
// createAppEventChannel is app-provided and returns EventChannel<MyEvent>
const channel = createAppEventChannel<MyEvent>("my:event");
try {
  const watcher = yield* takeLatest(channel, function* (data) {
    yield* call(expensiveOperation, data);
  });
  yield* join(watcher);
} finally {
  channel.close();
}
```

Use native redux-saga `takeLatest(channel, worker)` when only the **latest** event matters (e.g., streaming progress, latest search). Keep ownership of app-created channels explicit and close them in `finally`.

### 3. Keep a serial `while (true) + take(channel)` loop when ordering matters

```typescript
// Valid serial alternative: finish one operation before taking another event.
const channel = createAppEventChannel<MyEvent>("my:event");
try {
  while (true) {
    const data = yield* take(channel);
    yield* call(handleEvent, data);
  }
} finally {
  channel.close();
}

```

This loop is not equivalent to `takeEvery`: it is serial rather than concurrent. Choose deliberately. An unbuffered `eventChannel` drops events while no taker is waiting (including while a serial worker runs). Configure the app's channel factory with an explicit buffer/overflow policy if those events must be retained; a bounded buffer also needs a deliberate overflow policy. Closing a channel unsubscribes; it does not by itself cancel already-forked workers.

## Common Mistakes

### ❌ Omitting cleanup or closing immediately after forking a watcher

**Mechanism:** A loop without `finally` leaks its subscription on cancellation. A watcher fork without a blocking owner enters `finally` too early. Use the serial loop above or keep the forked watcher joined; the loop itself is not a mistake.

```typescript
// WRONG
const ch = createAppEventChannel<Evt>("e");
while (true) {
  const data = yield* take(ch);
  yield* call(worker, data);
}
```

```typescript
// CORRECT
const ch = createAppEventChannel<Evt>("e");
try {
  const watcher = yield* takeEvery(ch, worker);
  yield* join(watcher);
} finally {
  ch.close();
}
```

Source: redux-saga channel watcher effects. Priority: **HIGH**.

### ❌ Using channel-effects where selector-channels fit

**Mechanism:** For selector-derived changes, `takeEveryFromSelector` / `takeLatestFromSelector` handle subscription and args-tuple keying automatically; wrapping a selector in a generic EventChannel throws those guarantees away.

```typescript
// WRONG
const ch = yield* createChannelFromSelector(selectItem, id);
yield* takeLatest(ch, worker);
```

```typescript
// CORRECT
yield* takeLatestFromSelector(selectItem, [id], worker);
```

Source context: package-internal store-utility saga implementation. Public selector-channel helpers are available from `@themislib/themis/saga`. Priority: **MEDIUM**.

## See also

- `core/selector-channels` — for selector-derived channels (the right tool for state changes).
- `core/sagas` — core saga patterns, `takeEvery` / `takeLatest` for actions.

