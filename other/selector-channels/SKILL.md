---
name: core/selector-channels
description: >-
  Use takeLatestFromSelector, takeEveryFromSelector, or takeLeadingFromSelector
  for saga reactions to selector changes. Reserve createChannelFromSelector
  for custom race/condition/timeout flows; close raw channels in finally.
type: sub-skill
requires:
  - core
  - core/sagas
triggers:
  - take latest selector
  - take every selector
  - channel from selector
  - react to state
---
# Selector Channels — agent implementation rules

Use this skill when a saga should react to selector value changes instead of action dispatches. Keep detailed examples in `@themislib/themis/docs/SAGAS.md`; this skill is for quick implementation decisions and guardrails.

## Canonical references

- Human guide: `@themislib/themis/docs/SAGAS.md#selector-channel-effects`
- Public API: `@themislib/themis/utils/sagas/selector-channel-effects` or aggregate `@themislib/themis/saga`.
- Related skills: `core/sagas`, `core/wait-for`, `core/channel-effects`, plus the selected Store family selector lifecycle skill when direct selector call modes matter.

## Choose the helper

- `takeLatestFromSelector` — default for load/search/recompute-on-change; cancels previous worker.
- `takeEveryFromSelector` — every selector emission must be handled independently.
- `takeLeadingFromSelector` — ignore new emissions while current work runs.
- `createChannelFromSelector` — only for custom `race`, conditional loops, manual cancellation, or timeout flows.
- `waitFor` — one-shot wait before continuing, not a continuous watcher.

## Do

- Use named selectors created by the selected Store family utilities; selector-channel helpers require the shared `.select(state, ...args)` / `.effect(...args)` read shape.
- Import the selectors from the owning slice's `[slice]-selectors.ts` file; do not declare local `select*` functions/factories inside saga modules.
- Pass plain stable selector arguments as the args tuple in the second position, e.g. `[itemId]`, matching `.select(state, ...args)` / `.effect(...args)` rather than direct-call reactive argument wrappers.
- Prefer primitive scalar args in selector-channel tuples; pass object/function args only when their identity is stable and intentional.
- Expect worker payloads to include `{ payload, prevPayload }`.
- Prefer the `take*FromSelector` helpers because they create and clean up channels for you.
- Close raw channels in `finally` every time.
- Keep selector-channel workers focused and cancellation-safe.

## Don't

- Do not wrap selector channels in generic `channel-effects`; selector helpers already own the lifecycle.
- Do not use closures or inline selector lambdas to smuggle arguments.
- Do not declare module-local `select*` selectors inside the saga file to feed selector-channel helpers; move them to `[slice]-selectors.ts` and import them.
- Do not fall back to `take('*')` or other wildcard takes when a selector-channel helper or concrete action creator would model the intent.
- Do not choose a raw channel for simple load-on-change behavior.
- Do not leave manual channel loops without cancellation and cleanup.
- Do not confuse selector channels with action watchers; use core saga effects for actions.
- Do not pass or subscribe to direct reactive/observable selector outputs in selector-channel effects.
- Do not put fresh object, array, or function literals in selector-channel args
  tuples; split to scalar args or create a stable reference before the helper call.

## Implementation cues

- Selector-channel effects use the saga-context Redux store directly: read with `getState()` and subscribe with `subscribe()`. Do not introduce family-specific reactive wrappers for selector channels.
- For no-arg selectors, pass the worker directly to the helper.
- For selectors with args, pass the args tuple before the worker.
- The args tuple may be a fresh array wrapper, but the values inside it should be
  stable selector args; avoid `[ { id } ]`, `[ids.map(...)]`, or `[() => ...]`
  unless the inner value is an intentional stable reference.
- The first channel emission can have `prevPayload` as `null`/`undefined`; guard transition logic accordingly.
- If multiple dispatches produce intermediate values, model the final UI value with selectors or action design; there is no public lock/unlock action API.
- For generic IPC/websocket/DOM `EventChannel` consumers, route to `core/channel-effects` instead.

## Examples

### 1. Use takeLatestFromSelector for no-arg selector changes

```ts
import { put } from "typed-redux-saga";
import { takeLatestFromSelector } from "@themislib/themis/saga";

function* watchCurrentItem() {
  yield* takeLatestFromSelector(selectCurrentItemId, function* ({ payload: itemId }) {
    if (itemId) yield* put(loadItem(itemId));
  });
}
```

### 2. Pass selector arguments as an args tuple

```ts
import { call } from "typed-redux-saga";
import { takeEveryFromSelector } from "@themislib/themis/saga";

function* watchTodo(todoId: string) {
  yield* takeEveryFromSelector(selectTodoById, [todoId], function* ({ payload: todo }) {
    if (todo) yield* call(syncTodo, todo);
  });
}
```

Use scalar args like `todoId`. Do not pass freshly built selector option objects
such as `[{ id: todoId }]`; if a selector intentionally keys by object identity,
construct that object once and reuse the stable reference.

### 3. Use takeLeadingFromSelector when in-flight work should ignore new values

```ts
import { takeLeadingFromSelector } from "@themislib/themis/saga";

function* watchCheckoutReadiness() {
  yield* takeLeadingFromSelector(selectCheckoutReady, function* ({ payload: ready }) {
    if (ready) yield* submitCheckoutWorker();
  });
}
```

### 4. Read payload and prevPayload when transition semantics matter

```ts
import { put } from "typed-redux-saga";
import { takeEveryFromSelector } from "@themislib/themis/saga";

function* watchConnectionStatus() {
  yield* takeEveryFromSelector(selectConnectionStatus, function* ({ payload, prevPayload }) {
    if (prevPayload === "connecting" && payload === "connected") {
      yield* put(connectionEstablished());
    }
  });
}
```

### 5. Use createChannelFromSelector only for custom race/timeout flows

```ts
import { call, delay, race, take } from "typed-redux-saga";
import { createChannelFromSelector } from "@themislib/themis/saga";

function* waitForFirstReadyItem(itemId: string) {
  const channel = yield* createChannelFromSelector(selectTodoById, itemId);
  try {
    return yield* race({ item: take(channel), timeout: delay(5_000) });
  } finally {
    channel.close();
  }
}
```

### 6. ❌ Bad: wrapping auto-forking helpers or hiding args in closures

```ts
// BAD: the helper already forks and owns channel cleanup; closure args bypass the public args tuple.
function* watchTodoBad(todoId: string) {
  yield* fork(takeLatestFromSelector, () => selectTodoById.select(store.state, todoId), syncTodoWorker);
}

function* watchTodoGood(todoId: string) {
  yield* takeLatestFromSelector(selectTodoById, [todoId], syncTodoWorker);
}
```

## Verification cues

- Test that the selected helper matches desired cancellation behavior (`latest`, `every`, or `leading`).
- For raw channel use, test cancellation/timeout paths and assert cleanup where practical.
- Search for accidental duplicate selector watchers if adding a new watcher for existing state.
- Run the smallest relevant saga tests when docs/skills examples change.

## Common mistakes to prevent

- Hand-rolled channel loops where `takeLatestFromSelector` is enough.
- Missing `channel.close()` in `finally`.
- Passing selector args through closures instead of an args tuple.
- Passing freshly constructed object/array/function selector args in the tuple.
- Using generic `takeLatest(channel, worker)` on a channel created from a selector instead of `takeLatestFromSelector`.
- Declaring `select*` selectors locally in the saga module instead of importing them from `[slice]-selectors.ts`.
- Reaching for `take('*')` instead of a selector-channel helper or a concrete action creator.

## See also

- `@themislib/themis/docs/SAGAS.md` — full selector-channel examples and saga context.
- `core/wait-for` — one-shot selector waits.
- `core/channel-effects` — generic `EventChannel` consumers.
- Selected Store family selector lifecycle skill — selector initialization and call modes.