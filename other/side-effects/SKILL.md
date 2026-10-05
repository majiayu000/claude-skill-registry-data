---
name: react/migration/side-effects
description: >-
  Move shared React useEffect fetches, subscriptions, timers, and persistence to
  sagas; keep permitted DOM-local effects local.
type: sub-skill
requires:
  - core/sagas
  - core/core-policy
  - react/component-integration
  - react/migration
triggers:
  - migrate React useEffect
  - React timer to saga
  - React fetch to saga
---
# React side-effect migration

Classify existing React effects with
[When to use Redux vs component-local state](../../../core/core-policy/SKILL.md#when-to-use-redux-vs-component-local-state)
and [Setup — core rules](../../../core/core-policy/SKILL.md#setup--core-rules)
before migrating business work to sagas. Keep permitted DOM-local effects local.

React sources include `useEffect` fetches, subscriptions, timers, debounces,
storage sync, IPC/websocket listeners, and custom hooks that hide async work.

## Before: component-owned async effect

```tsx
import * as React from "react";
import { useUserContext } from "./UserProvider";

export function UserLoader({ userId }: { userId: string }) {
  const { setUsername } = useUserContext();
  React.useEffect(() => {
    let cancelled = false;
    fetch(`/api/users/${userId}`).then((res) => res.json()).then((data) => {
      if (!cancelled) setUsername(data.name);
    });
    return () => { cancelled = true; };
  }, [setUsername, userId]);
  return null;
}
```

## After: action-triggered saga

```ts
import { call, put, takeLatest } from "typed-redux-saga";
import { createAction } from "@themislib/themis/utils/store/create-action";
import { setUsername } from "../users-slice";

type UserResponse = { name: string };

export const loadUser = createAction<[userId: string]>("users/loadUser");

function fetchUser(userId: string) {
  return fetch(`/api/users/${userId}`).then((response) => response.json() as Promise<UserResponse>);
}

function* loadUserWorker(action: ReturnType<typeof loadUser>) {
  const user = yield* call(fetchUser, action.payload[0]);
  yield* put(setUsername(user.name));
}

export function* usersSaga() {
  yield* takeLatest(loadUser, loadUserWorker);
}
```

## Start the saga from ReactStore setup

Choose the lifetime before wiring a migrated saga; moving business logic to a
saga does not make it app-wide. Core
[Application saga startup](../../../core/sagas/SKILL.md#application-saga-startup)
supplies the framework-neutral contract:

- **App-wide work:** start from the existing React bootstrap/root or service
  owner after Store initialization. Retain the matching cancel function and call
  it when that owner ends, before whole-Store disposal. Follow
  [Start app sagas explicitly](../../component-integration/SKILL.md#start-app-sagas-explicitly)
  and [Dispose at the same owner boundary](../../component-integration/SKILL.md#dispose-at-the-same-owner-boundary).
- **Component/layout-scoped work:** start when that component/layout mounts and
  return the matching cancel function from its lifecycle effect. The parent app
  must already have initialized the shared Store; the scoped owner must not
  initialize or dispose the parent's Store. Unmount scoped owners before the app
  disposes it.

For example, if `usersSaga` should run only while one users layout is mounted,
mount this lifetime owner in that layout, not at the app root:

```tsx
import { useEffect } from "react";
import { reactStore } from "../react-store";
import { usersSaga } from "./sagas/users-saga";

export function UsersRuntime() {
  useEffect(() => reactStore.runSaga(usersSaga), []);
  return null;
}
```

This effect only wires startup and cleanup under the
[bootstrap/lifetime-owner exception](../../../core/import-boundaries/SKILL.md#bootstrap-and-lifetime-owner-exception);
fetching and other business work remain in the saga. Do not also start the same
saga at the root or in another concurrent owner. Ordinary component handlers
still dispatch actions instead of importing or invoking business sagas.

## Conversion recipes

| React source pattern | Saga target |
| --- | --- |
| useEffect(() => fetch(...), [id]) | Action + takeLatest(action, worker) + call + put |
| Component debounce with setTimeout | Action + takeLatest(action, worker) + delay |
| Reconnect on derived state change | Selector-channel helper from saga code |
| localStorage sync in component/hook | Saga persistence helper called from takeEvery |
| WebSocket/DOM/IPC subscription shared across app | Channel setup in saga with cleanup in finally |
| Async success/failure local state | createAsyncAction flow handled inside saga worker |

## Rules

- Keep reducers pure; never move React effects into reducers.
- Use `takeLatest` for stale-response-prone fetch/search flows.
- Use `takeEvery` when every action must be processed.
- Use selector `.effect(...args)` in sagas when the saga needs current derived state.
  Follow [Saga reads](../../selector-lifecycle/SKILL.md#saga-reads) for call-mode boundaries.
- Do not keep both a migrated `useEffect` and a saga for the same trigger.
- Do not use selector `.useValue(...args)` or direct React signals from saga code.

## Bad: duplicate ownership

```tsx
// BAD: this duplicates the saga that also persists settingsSaved.
React.useEffect(() => {
  localStorage.setItem("settings", JSON.stringify(settings));
}, [settings]);
```

## Cross-references

- `../../../core/sagas/SKILL.md` — framework-neutral saga patterns.
- `../../../core/selector-channels/SKILL.md` — reacting to selector value changes from sagas.
- `../../selector-lifecycle/SKILL.md` — saga selector reads without React hooks/signals.