---
name: core/wait-for
description: >-
  Use waitFor when a saga must pause until a named selector matches a
  predicate, optionally with a timeout.
type: sub-skill
requires:
  - core
  - core/sagas
triggers:
  - waitFor selector
  - suspend saga
  - wait predicate
  - timeout wait
---
# waitFor — agent implementation rules

Use this skill for one-shot saga waits on selector state. Keep conceptual/API prose and examples in `@themislib/themis/docs/WAITFOR.md`; this skill should stay concise and operational.

## Canonical references

- Human guide: `@themislib/themis/docs/WAITFOR.md`
- Public API: `waitFor` from `@themislib/themis/saga`.
- Channel helpers: `@themislib/themis/utils/sagas/selector-channel-effects` or aggregate `@themislib/themis/saga`.
- Related skills: `core/sagas`, `core/selector-channels`, `core/testing`, plus the selected Store family selector skill for family-specific selector authoring.

## Use when

- A saga must wait for a selector value before continuing.
- The condition is one-shot: proceed after the predicate matches or timeout handling runs.
- The selector already exists as a named selector, authored with `store.createSelector(...)` for app-local selectors when a configured Store exists.

## Do

- Call as `waitFor(selector, argsTuple, predicate, timeoutMs?)`.
- Pass `[]` for no-arg selectors and `[arg1, arg2]` for stable selector arguments.
- Prefer primitive scalar args in the tuple; pass object/function args only when
  their identity is stable and intentional.
- Keep the predicate pure: no dispatches, API calls, mutations, timers, or state reads.
- Add a timeout for production waits unless an indefinite wait is explicitly safe.
- Check the boolean return when a timeout is supplied.
- Guard previous-value comparisons because the immediate check passes `undefined` as `prevVal`, and the first selector-channel emission can pass `null`.

## Don't

- Do not pass inline selectors or closures; create/reuse a named selector.
- Do not swap the args tuple and predicate.
- Do not ignore `false` from timed waits.
- Do not use `waitFor` for polling or continuous reactions; use `takeLatestFromSelector`, `takeEveryFromSelector`, or a selector channel instead.
- Do not duplicate the implementation's channel/race logic in app code.
- Do not put fresh object, array, or function literals in the args tuple; split to
  scalar args or pass a stable intentional reference.

## Implementation cues

- Import from `@themislib/themis/saga` unless an existing app-local barrel already re-exports it.
- For boolean readiness, predicate on the desired final value rather than assuming truthiness.
- For status transitions, include the terminal states in the predicate and branch after `waitFor` if different terminal outcomes matter.
- For timeout paths, dispatch or return an explicit timeout outcome before continuing with state-dependent work.
- If a saga needs every future selector change, route to `core/selector-channels` instead.

## Examples

### 1. Wait for a no-arg boolean selector and handle timeout

```ts
import { put } from "typed-redux-saga";
import { waitFor } from "@themislib/themis/saga";

function* loadWhenReady() {
  const ready = yield* waitFor(selectIsReady, [], (value) => value === true, 5_000);
  if (!ready) {
    yield* put(loadTimedOut());
    return;
  }
  yield* put(loadData());
}
```

### 2. Pass selector arguments as the required args tuple

```ts
import { waitFor } from "@themislib/themis/saga";

function* processItem(itemId: string) {
  const ready = yield* waitFor(selectItemStatus, [itemId], (status) => status === "ready", 10_000);
  if (ready) yield* startItemProcessing(itemId);
}
```

Use scalar args like `itemId`. Avoid args tuples such as `[{ id: itemId }]`
unless that object is a stable, intentional selector key reused across calls.

### 3. Guard previous-value comparisons on the immediate check

```ts
import { waitFor } from "@themislib/themis/saga";

function* waitForReconnect() {
  const reconnected = yield* waitFor(
    selectConnectionStatus,
    [],
    (value, prevVal) => prevVal === "connecting" && value === "connected",
    15_000
  );
  return reconnected;
}
```

### 4. Branch after terminal-state waits

```ts
import { put } from "typed-redux-saga";
import { waitFor } from "@themislib/themis/saga";

function* waitForUpload(uploadId: string) {
  const finished = yield* waitFor(selectUploadPhase, [uploadId], (phase) => phase === "done" || phase === "failed", 60_000);
  if (!finished) return yield* put(uploadTimedOut(uploadId));
  const phase = yield* selectUploadPhase.effect(uploadId);
  if (phase === "failed") yield* put(uploadFailed(uploadId));
}
```

### 5. Use waitFor inside an action worker before state-dependent work

```ts
import { call, put } from "typed-redux-saga";
import { waitFor } from "@themislib/themis/saga";

function* publishAfterAuthWorker(action: ReturnType<typeof publishDocument>) {
  const authenticated = yield* waitFor(selectAuthReady, [], Boolean, 5_000);
  if (!authenticated) return yield* put(publishRejected(action.payload[0], "auth-timeout"));
  yield* call(api.publishDocument, action.payload[0]);
}
```

### 6. ❌ Bad: ignoring false and treating prevVal as present on the first check

```ts
// BAD: timeout false is ignored, and prevVal can be undefined or null before a real transition.
function* publishAfterAnyStatusChange(documentId: string) {
  yield* waitFor(selectDocumentStatus, [documentId], (value, prevVal) => value !== prevVal, 5_000);
  yield* call(api.publishDocument, documentId);
}

function* publishAfterRealStatusChange(documentId: string) {
  const changed = yield* waitFor(
    selectDocumentStatus,
    [documentId],
    (value, prevVal) => prevVal !== undefined && prevVal !== null && value !== prevVal,
    5_000
  );
  if (changed) yield* call(api.publishDocument, documentId);
}
```

## Verification cues

- Test immediate-match, later-match, and timeout paths when changing `waitFor` usage.
- In saga tests, provide selector `.effect(...)` values and channel/timer effects through existing test helpers.
- Run the smallest relevant saga tests when docs/skills examples change.

## Common mistakes to prevent

- `waitFor(selectReady, predicate)` — missing `[]` args tuple.
- `waitFor(selectItem, [{ id }], predicate)` — fresh object selector arg.
- Acting after a timed wait without checking the returned boolean.
- Predicate change detection that treats initial `prevVal === undefined` or first-emission `prevVal === null` as a real transition.
- Replacing one-shot waits with hand-rolled selector channels.

## See also

- `@themislib/themis/docs/WAITFOR.md` — full signature, behavior walkthrough, and examples.
- `@themislib/themis/docs/SAGAS.md` — selector-channel and saga orchestration context.
- `core/selector-channels` — continuous selector watchers.
- Selected Store family selector lifecycle skill — selector call modes.