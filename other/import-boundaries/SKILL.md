---
name: core/import-boundaries
description: >-
  Use when checking which store modules components, services, and sagas may
  import, including dispatch access and forbidden saga/reducer internals.
type: sub-skill
requires:
  - core
  - core/core-policy
triggers:
  - import boundaries
  - saga import rule
  - dispatch subpath
  - forbidden imports
---
# Import Boundaries

> Source: [Setup — the package export surface](#setup--the-package-export-surface); `package.json` exports map; public `@themislib/themis/svelte-store`; hidden root-entry implementation context; `@themislib/themis/docs/ARCHITECTURE.md` maintainer validation.

## Setup — the package export surface

The documented public surface is the approved subpackage interface plus explicit utility leaf subpaths. Do not teach consumers to import from the package root, from removed broad utility barrels, or from source-shaped deep paths.

The utility exports are explicit leaf entries, not wildcard domains. The package still does not export the root `themis`, `@themislib/themis/utils`, `@themislib/themis/utils/runtime/*`, selector implementation internals (`utils/svelte-selectors/*`, `utils/streaming-selectors/*`, or `utils/selector-core/*`), old `themis/components/*` paths, `themis/src/*`, or directory `index` barrels.

The public subpackages relevant to Store-family import boundaries include:

- `@themislib/themis/svelte-store` — canonical Svelte-readable `Store` class. Per-store operations go through the configured Store instance (`store.init`, `store.dispatch`, `store.state`, `store.createSelector`, `store.runSaga`, `store.dispose`). Utility helpers are not exported here; use the explicit utility leaf subpaths below.
- `@themislib/themis/streaming-store` — direct `StreamingStore` leaf for Kefir/observable selectors. Do not import streaming selector internals directly.
- `@themislib/themis/saga` — saga authoring helpers: `waitFor`, selector-channel helpers, and debounce/retry/streaming helpers.
- `@themislib/themis/types` — public TypeScript-only types such as `StoreState`, `PreloadedStoreState`, action, middleware, selector, reducer, and saga map types.
- `@themislib/themis/components-svelte/use-init-store`, `/use-run-saga` — optional Svelte lifecycle helper leaves. Do not import from old `components/*` paths or from a `components-svelte` directory barrel.
- `@themislib/themis/utils/collections/collection-utils` — approved direct collection utility leaf.
- `@themislib/themis/utils/store/create-action`, `/create-reducer`, `/boolean-preference`, `/domain-scoped` — the only package-level store utility leaf imports.
- `@themislib/themis/utils/sagas/debounce-saga`, `/retry-with-timeout`, `/wrap-async-generator`, `/selector-channel-effects` — approved direct saga utility leaves. Safe localStorage helpers are example/app-local utilities, not package exports.

Migration note: replace flat package-root examples, removed utilities-subpackage imports, and source-shaped deep imports with one of the public subpackages or approved utility leaf subpaths above.

## Core Patterns

### Components and component-level modules — allowed

- ✅ Actions from `*-slice.ts`
- ✅ Selectors from `*-selectors.ts`
- ✅ Types from `*-types.ts`
- ✅ The app's existing initialized `Store` instance for dispatch and one-time reads in event handlers (`store.dispatch`, `store.state`)

### Components — forbidden

- ❌ Saga files (`sagas/*.ts`) in ordinary components/handlers — dispatch the owning action instead. Only the explicit [bootstrap/lifetime owner](#bootstrap-and-lifetime-owner-exception) may import the saga it starts and stops.
- ❌ Operation/utility modules that dispatch internally
- ❌ Reducer internals or store init/setup modules
- ❌ Collection utils directly (access collections through selectors)
- ❌ `typed-redux-saga` or `redux-saga` — saga effect libraries have no meaning in a component; importing them at minimum bloats the bundle and often drags the saga middleware into client code

### Services and non-component TS

Services may import actions, selectors, and the app's existing initialized `Store` instance captured outside callbacks. Ordinary service operations may **not** import or call sagas directly — call `store.dispatch(triggeringAction())` instead. A service that is the explicit lifetime owner has only the startup exception below.

### Bootstrap and lifetime-owner exception

The designated bootstrap, layout/component, or service lifetime owner may import the configured Store and the saga function it passes to `store.runSaga(saga)`. Initialize the Store before starting the saga, retain the matching stop handle, and stop it at that same boundary. This is lifecycle wiring, not permission to invoke/step the generator, use saga effects in components, or move business logic into handlers. Do not add a second hidden owner for an already-owned saga.

For an owner that also owns Store initialization/disposal (adapt the boundary to the selected family):

```ts
import { store } from "$lib/store";
import { jobsSaga } from "$lib/store/slices/jobs/sagas/jobs-saga";

export function startJobsOwner() {
  const disposeStore = store.init();
  const stopJobs = store.runSaga(jobsSaga);
  return () => {
    stopJobs();
    disposeStore();
  };
}
```

If a longer-lived parent already owns the initialized Store, retain/call only the saga stop handle; do not initialize or dispose the parent's Store. Ordinary UI events still import actions and use `store.dispatch(action())`. Follow the chosen family's lifecycle leaf and [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle).

### Sagas

Sagas may import anything within the store directory (actions, selectors, other sagas, reducer internals, collection utils, app-local safe localStorage helpers, `typed-redux-saga` effects). This is the only layer where `yield*` of `typed-redux-saga` effects is allowed.

## Examples

### 1. Public package subpaths and utility leaf imports

Use the export list above, not a package-root or implementation import:
`createAction` comes from `@themislib/themis/utils/store/create-action`,
`retryWithTimeout` from `@themislib/themis/saga`, and `StoreState` from
`@themislib/themis/types` via `import type`. Import the concrete Store class
from the selected family's public subpackage.

### 2. Component imports actions, selectors, types, and the initialized Store instance

```ts
import { store } from "$lib/store";
import { selectItems, selectIsLoading } from "./slices/items/items-selectors";
import { removeItem } from "./slices/items/items-slice";
import type { Item } from "./slices/items/items-types";

export const items = selectItems();
export const loading = selectIsLoading();

export function handleDelete(item: Item) {
  const currentItems = selectItems.select(store.state);
  if (currentItems.length > 1) store.dispatch(removeItem(item.id));
}
```

### 3. Service/non-component TS uses one-shot reads and dispatch, not saga source

```ts
import { store } from "$lib/store";
import { selectQueuedJob } from "$lib/store/slices/jobs/jobs-selectors";
import { startJob } from "$lib/store/slices/jobs/jobs-slice";

export function startQueuedJob(jobId: string) {
  const queuedJob = selectQueuedJob.select(store.state, jobId);
  if (queuedJob) store.dispatch(startJob(jobId));
}
```

### 4. Saga layer may import saga effects, selectors, actions, and saga utilities

```ts
import { call, delay, put, takeLatest } from "typed-redux-saga";
import { loadJobs, refreshJobs } from "../jobs-slice";
import { selectQueuedJob } from "../jobs-selectors";

declare const api: { runJob(id: string): Promise<void>; refreshJobs(): Promise<void> };

export function* jobsSaga() {
  yield* takeLatest(loadJobs, function* loadQueuedJob(action: { payload: [string] }) {
    const job = yield* selectQueuedJob.effect(action.payload[0]);
    if (job) yield* call(api.runJob, job.id);
    yield* put(refreshJobs());
  });
  yield* takeLatest(refreshJobs, function* refreshJobsAfterIdle() {
    yield* delay(250);
    yield* call(api.refreshJobs);
  });
}
```

## Common Mistakes

### ❌ Importing saga files from components

Outside the explicit bootstrap/lifetime-owner exception, importing saga source
crosses the component boundary; invoking or stepping its generator bypasses
`Store.runSaga` lifecycle. Import the triggering action from its owning slice and
call `store.dispatch(fetchItems())` instead. The startup exception does not permit
business-saga calls or effect imports in event handlers.

Source: [Components — forbidden](#components--forbidden) · **Priority: HIGH**

### ❌ Hiding dispatch inside service helpers

Components and services should dispatch through the configured app `Store` instance or receive a dispatch function explicitly. A helper that captures a hidden module-level dispatch creates an unreviewable second boundary even when all imports type-check.

Keep the Store or dispatch parameter explicit at the call site rather than hiding
ownership in an operation helper. This does not permit business timers or other
domain effects outside sagas; `core/core-policy/SKILL.md` owns that rule.

Source: [Components and component-level modules — allowed](#components-and-component-level-modules--allowed), [Services and non-component TS](#services-and-non-component-ts) · **Priority: MEDIUM**

### ❌ Importing from `typed-redux-saga` in a component file

Effects (`call`, `put`, `select`, `takeEvery`, ...) only run inside saga generators.
Calling `put(triggerEffect())` in a handler just creates an unexecuted descriptor;
call `store.dispatch(triggerEffect())` instead. Effect imports also bloat the
client bundle and drag saga mocks (`core/testing`) into non-saga tests.

Source: [Components — forbidden](#components--forbidden) (No saga effects in components; saga-function imports only at the explicit lifetime owner) · **Priority: HIGH**

## See also

- `core/core-policy/SKILL.md` — the policy these boundaries enforce
- Selected Store family skill — Store dispatch + selector usage inside components

