---
name: svelte/migration/side-effects
description: >-
  Use when moving domain-owned Svelte subscriptions, $effect blocks, fetches,
  localStorage, timers, or IPC listeners into sagas. Keep DOM-local effects in
  components.
type: sub-skill
requires:
  - core/core-policy
  - core/sagas
  - svelte/migration
triggers:
  - migrate $effect
  - move side effect
  - timer to saga
  - fetch to saga
---
# Migration — `$effect` / `fetch` / Subscriptions → Saga

> Migrate domain/business effects to sagas after assessment. Reducers remain pure;
> DOM-local component effects retain their component lifetime.

## Effect ownership boundary

Use `../../../core/core-policy/SKILL.md` → **Setup — core rules** and
`../assessment/SKILL.md` → **Decision Framework** before applying a recipe.
Domain persistence, network/IPC flows, subscriptions, and business timers belong
in sagas. Focus, scroll, measurements, and third-party widget setup/cleanup tied
to rendered DOM remain component-owned. Do not globalize those effects merely
because they use `$effect`, `onMount`, listeners, or timers.

Choose startup/cancellation ownership explicitly using `../../store/SKILL.md` →
**App saga lifetime**. `store.init()` does not start app sagas; an `onMount`-started
saga cancels on unmount and starts again on remount.

## Examples

### User-triggered fetch becomes a `takeLatest` worker

```typescript
// src/lib/store/slices/users/sagas/users-saga.ts
import { call, put, takeLatest } from "typed-redux-saga";
import { createAction } from "@themislib/themis/utils/store/create-action";
import { setUsername } from "../users-slice";

export const loadUser = createAction<[userId: string]>("users/loadUser");

function* loadUserWorker(action: ReturnType<typeof loadUser>) {
  const response = yield* call(fetch, `/api/users/${action.payload[0]}`);
  const data = (yield* call([response, "json"])) as { name: string };
  yield* put(setUsername(data.name));
}

export function* usersSaga() {
  yield* takeLatest(loadUser, loadUserWorker);
}
```

### Timers/debounce migrate to saga cancellation semantics

```typescript
// src/lib/store/slices/search/sagas/search-saga.ts
import { call, delay, put, takeLatest } from "typed-redux-saga";
import { queryChanged, searchResultsLoaded } from "../search-slice";

declare const api: { search(query: string): Promise<SearchResult[]> };

export function* searchSaga() {
  yield* takeLatest(queryChanged, function* searchAfterSettled(action) {
    yield* delay(300);
    const results = yield* call(api.search, action.payload[0]);
    yield* put(searchResultsLoaded(results));
  });
}
```

### Store subscriptions migrate to selector-channel helpers

```typescript
// src/lib/store/slices/session/sagas/session-saga.ts
import { call } from "typed-redux-saga";
import { takeLatestFromSelector } from "@themislib/themis/saga";
import { selectSessionToken } from "../session-selectors";

declare function reconnectWithToken(token: string): Promise<void>;

export function* sessionSaga() {
  yield* takeLatestFromSelector(selectSessionToken, function* ({ payload, prevPayload }) {
    if (payload && payload !== prevPayload) {
      yield* call(reconnectWithToken, payload);
    }
  });
}
```

### Persistence uses safe saga helpers instead of direct browser calls

```typescript
// src/lib/store/slices/settings/sagas/settings-saga.ts
import { call, takeEvery } from "typed-redux-saga";
import { setLocalStorageJSON } from "$lib/store/utils/safe-local-storage-saga";
import { settingsSaved } from "../settings-slice";
import { selectSettings } from "../settings-selectors";

export function* settingsSaga() {
  yield* takeEvery(settingsSaved, function* () {
    const settings = yield* selectSettings.effect();
    yield* call(setLocalStorageJSON, "settings", settings);
  });
}
```

### Async action success/failure flow stays in the worker, not the component

```typescript
// src/lib/store/slices/profile/sagas/profile-saga.ts
import { call, put, takeEvery } from "typed-redux-saga";
import { createAsyncAction } from "@themislib/themis/utils/store/create-action";

type Profile = { id: string; name: string };
declare const api: { saveProfile(profile: Profile): Promise<Profile> };

export const saveProfile = createAsyncAction<[profile: Profile], Profile>(
  "profile/saveProfile",
  "profile/saveProfileStatus"
);

export function* profileSaga() {
  yield* takeEvery(saveProfile, function* (action) {
    try {
      const saved = yield* call(api.saveProfile, action.payload[0]);
      yield* put(action.success(saved));
    } catch (error) {
      yield* put(action.failure(error instanceof Error ? error : new Error(String(error))));
    }
  });
}
```

## Conversion Recipes

These recipes apply only to domain-owned work classified above.

| Source pattern | Saga equivalent |
| --- | --- |
| `$effect` persistence | Action watcher + app-local safe storage helper; see persistence example. |
| Store subscription reacting to state | Selector-channel helper with plain args and `payload` / `prevPayload`; see subscription example. |
| Fetch + state update | `call(fetch, ...)`, bound `call([response, "json"])`, then `put`; see fetch example. |
| Debounce / timeout | `takeLatest` + `delay` / one `yield* delay(ms)`. |
| Interval | Cancellation-owned loop: `while (true) { yield* delay(ms); ... }`. |
| DOM listener / IPC | `createChannelFrom...` + redux-saga `takeEvery(channel, worker)`; see core/channel-effects. |
| Domain startup formerly in onMount | Explicit mount-scoped `onMount(() => store.runSaga(sagaFn))`; see `../../store/SKILL.md` → **App saga lifetime** |

## Common Pitfalls

- Do not keep a component `$effect` and add a saga for the same trigger; that creates duplicate ownership and double writes.
- Use `takeLatest` for user-triggered fetch/search flows so stale responses are cancelled before they overwrite newer state.
- Close manually-created channels in `finally`; prefer selector-channel helpers when simple `takeEvery`/`takeLatest`/`takeLeading` semantics are enough.
- Keep reducers pure: no `fetch`, no direct `localStorage`, no clocks, no random IDs, and no logging side effects.

## Cross-References

- `../../../core/sagas/SKILL.md` — full saga surface (takeEvery / takeLatest / takeLeading, Store-first saga startup, debounce with delay)
- `../../../core/local-storage/SKILL.md` — safe localStorage helpers and persistence-saga pattern
- `../../../core/channel-effects/SKILL.md` — generic EventChannel consumers for DOM / IPC / websocket listeners
- `../../../core/selector-channels/SKILL.md` — reacting to selector value changes from sagas
- `../../store/SKILL.md` — explicit saga startup and cancellation lifetime
