---
name: core/saga-manager
description: >-
  Use for Store saga init/run/cancel/dispose and restart behavior, crash reports,
  and retry backoff. Saga-manager internals, including addCrash/clearCrashes,
  are not app imports.
type: sub-skill
library: themis
requires:
  - core
  - core/import-boundaries
  - core/state-serialization
sources:
  - "@themislib/themis/docs/SAGAS.md#saga-manager"
  - public configured Store instance API
  - package-internal saga manager implementation
triggers:
  - saga manager
  - saga crash
  - store.runSaga
  - Store.dispose
  - addCrash
  - clearCrashes
  - saga restart
  - getBackOffDelay
---

# Saga Manager — crash and restart guidance

Use this skill when an agent must explain, verify, or minimally adjust saga manager guidance. Keep `@themislib/themis/docs/SAGAS.md#saga-manager` as the human-facing source for long-form behavior; this file is the concise operational checklist.

## Agent preflight compliance contract

- **MUST** read `@themislib/themis/docs/SAGAS.md#saga-manager`, this skill, and any touched source before editing saga-manager guidance.
- **MUST** cite whether the task concerns public Store lifecycle behavior or package-owned internals.
- **MUST** preserve import boundaries: app code uses public `Store` APIs and saga functions, not package-internal saga-manager modules.
- **SHOULD** run targeted saga-manager tests when behavior claims change.
- **NEVER** document `addCrash`, `clearCrashes`, reducer state paths, or `@internal_sagaManager` as public app APIs unless a separate public export task approves it.

## Store saga lifecycle

This section owns the shared Store saga lifecycle contract. For where app startup
belongs, follow [Application saga startup](../sagas/SKILL.md#application-saga-startup);
the selected Store family supplies framework-specific wiring.

- Initialize the Store before starting app sagas. `Store.init()` wires the Redux store and middleware, creates the selected Store variant's selector resources, and starts the package-owned saga manager internally; it does not auto-start app sagas.
- App sagas are started explicitly with `store.runSaga(sagaFn)` after initialization; Store derives a manager name from the saga function.
- `store.runSaga(sagaFn)` dispatches `startSaga(name, sagaFn)` and returns a cancel function that dispatches `stopSaga(name)`; the manager listens for those lifecycle actions.
- Retain each returned cancel function and invoke it when that lifetime owner ends. Shared-task reference counting is defined in [Start, stop, restart, and backoff mechanics](#start-stop-restart-and-backoff-mechanics).
- `Store.dispose()` and the disposer returned by `Store.init()` tear down the initialized Store runtime and stop Store-owned saga tasks, including running app sagas forked by the manager.
- Whole-Store teardown belongs only to the owner ending the entire Store context; it is not a substitute for an individual saga owner's cancel function.
- The reserved manager name is `@internal_sagaManager`; do not register, run, or expose it as an app saga. App code must not import package-internal actions such as `addCrash` or `clearCrashes`.

## Core Patterns

### 1. Crash tracking has two package-owned surfaces

- In-memory manager status tracks `isRunning`, `launchedAtTs`, and raw crash records (`Date` + `Error`) for monitoring/restart logic.
- On every unhandled saga error, the manager also dispatches `addCrash(sagaName, report)` with a serialized report: `crashedAtTs` plus plain `{ name, message, stack? }` error data.
- The serialized path keeps Redux state serializable; the raw status record types remain implementation details.

### 2. Crash report storage and retention

- The internal saga-manager reducer state is package-owned and keyed by saga name.
- Each entry is `{ reports, omittedCount }`; `reports` contains serialized crash reports for that saga only.
- The reducer keeps the newest `MAX_SAGA_CRASH_REPORTS` reports. When older reports are trimmed, `omittedCount` increases by the number trimmed.

### 3. Cleaning crash records is per saga name

- `clearCrashes(sagaName)` deletes only that saga name's crash entry.
- Clearing one saga does not clear reports for other saga names.
- Treat `clearCrashes` as package-internal until a public export/API is intentionally added.

### Start, stop, restart, and backoff mechanics

- Multiple overlapping `store.runSaga(sagaFn)` calls for the same derived saga name and function share one running task and increment a reference counter.
- The saga stops only after every returned cancel function has been invoked.
- Full Store disposal is a separate lifecycle boundary: follow [Store saga lifecycle](#store-saga-lifecycle), not disposal as a replacement for per-owner cancels.
- If the managed saga throws an unhandled error, `autoRestart` records the crash, logs it, waits, and restarts the saga automatically.
- `getBackOffDelay(restarts)` is `min(1000 * 2^restarts, 10 minutes)`: first restart waits 1s, then 2s, 4s, and so on up to the cap.
- Restart pressure decays after stable runtime: before incrementing, the manager subtracts one restart count per full minute since the last start, bounded at zero.

## Examples

### 1. Start app sagas explicitly by function

```ts
export const store = new Store({ todos: todosReducer });
store.init();

const cancelSyncTodos = store.runSaga(syncTodosSaga);
// Register cancelSyncTodos with the selected Store family root cleanup.
```

### 2. Pair every runSaga owner with its own cancel function

```ts
const cancelListPage = store.runSaga(syncTodosSaga);
const cancelDetailsPanel = store.runSaga(syncTodosSaga);

cancelListPage();
// syncTodos stays running for the details panel owner.
cancelDetailsPanel();
// syncTodos can stop after the final owner cancels.
```

### 3. Use Store disposal only for whole-store teardown

```ts
const disposeStore = store.init({ todos: preloadedTodosState });
const cancelSync = store.runSaga(syncTodosSaga);

cancelSync();
disposeStore();
```

### 4. Describe persisted crash reports as serialized package-owned state

```ts
type PersistedSagaCrashReport = {
  crashedAtTs: number;
  error: { name: string; message: string; stack?: string };
};

const syncTodosCrash: PersistedSagaCrashReport = {
  crashedAtTs: Date.now(),
  error: { name: "Error", message: "network failed" },
};
```

### 5. Model per-saga cleanup without implying global crash deletion

```ts
type CrashState = Record<string, { reports: unknown[]; omittedCount: number }>;

const afterClearingSyncTodos: CrashState = {
  syncUsers: { reports: [{ crashedAtTs: 1 }], omittedCount: 0 },
};
```

### 6. ❌ Bad: using Store.dispose as routine per-saga cleanup

```ts
// BAD: this tears down the whole initialized Store context for all owners.
function closeDetailsPanel() {
  store.dispose();
}

function closeDetailsPanelSafely(cancelSyncTodos: () => void) {
  cancelSyncTodos();
}
```

## Common mistakes to prevent

- **Promoting internals as app APIs** — `addCrash`, `clearCrashes`, raw manager status records, reducer state keys, and `@internal_sagaManager` are package-owned. Public facade: the configured Store instance (`store.runSaga`); source context: `@themislib/themis/docs/SAGAS.md#saga-manager` and package-internal saga manager implementation.
- **Saying cleanup is global** — `clearCrashes(sagaName)` removes only one saga entry. This is package-internal behavior, not a public app API.
- **Forgetting reference counting** — duplicate `store.runSaga(sagaFn)` calls for the same function share the saga and require matching cancels before the task stops. Public facade: the configured Store instance; source context: package-internal saga manager implementation.
- **Using Store disposal as per-saga cleanup** — `store.dispose()` stops tasks owned by the initialized Store context as part of whole-store teardown; use `store.runSaga(sagaFn)` cancel functions for normal saga lifetimes. Public API: configured Store instance lifecycle methods.
- **Flattening backoff behavior** — backoff starts at 1s, doubles to a 10-minute cap, and restart pressure decays after stable runtime. Source context: package-internal saga manager implementation.

## Verification cues

- Skill/doc-only edits with examples: review the rendered examples and run `git diff --check`.
- Metadata or architecture-governed examples changed: run `npm run validate:architecture`.
- Behavior-sensitive claims changed or questioned: run `npx --no-install vitest run src/slices/saga-manager/sagas/manager.test.ts`.

## See also

- `@themislib/themis/docs/SAGAS.md#saga-manager` — canonical human-facing explanation.
- [Do](../sagas/SKILL.md#do) and [Application saga startup](../sagas/SKILL.md#application-saga-startup) — typed-redux-saga implementation rules and framework-neutral startup ownership.
- `core/import-boundaries` — public package exports and forbidden deep imports.
- `core/testing` — saga/reducer verification patterns.