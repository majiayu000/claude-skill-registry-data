---
name: svelte/migration/derived-stores
description: >-
  Use when converting shared Svelte derived() stores, $derived runes, or
  getters into selectors composed through a configured Themis Store.
type: sub-skill
requires:
  - svelte/selectors
  - svelte/migration
  - core/collections
triggers:
  - migrate derived
  - migrate $derived
  - derived to selector
  - convert derivation
---
# Migration — `derived` / `$derived` → `store.createSelector`

> App-level `derived()` stores and shared `$derived` values become named
> selectors created from the configured app `Store`. Compose selectors with
> `.select(state)` inside selector bodies. Consumer call modes are owned by
> `../../selector-lifecycle/SKILL.md` → **Call-mode map**.

## Examples

### 1. Before: shared `derived()` store slated for migration

```typescript
// migration/counter-derived-before.ts
import { derived, writable } from "svelte/store";

export const count = writable(0);
export const username = writable("Ada");
export const doubled = derived(count, ($count) => $count * 2);
export const greeting = derived(username, ($name) => `Hello, ${$name}!`);
```

### 2. After: no-argument selectors with `.select(state)` composition

```typescript
// src/lib/store/slices/counter/counter-selectors.ts
import { store } from "$lib/store/store";

export const selectCount = store.createSelector((state) => state.counter.count);
export const selectUsername = store.createSelector((state) => state.counter.username);
export const selectDoubled = store.createSelector((state) => selectCount.select(state) * 2);
export const selectGreeting = store.createSelector((state) => {
  return `Hello, ${selectUsername.select(state)}!`;
});
```

### 3. Parameterized selectors replace functions that returned `derived()` stores

```typescript
// src/lib/store/slices/todos/todos-selectors.ts
import { store } from "$lib/store/store";
import { getItems } from "@themislib/themis/utils/collections/collection-utils";

// state.todos.items is Collection<Todo, "id">; the array is derived output only.
export const selectTodos = store.createSelector((state) => getItems(state.todos.items));
export const selectTodosForProject = store.createSelector((state, projectId: string) => {
  return selectTodos.select(state).filter((todo) => todo.projectId === projectId);
});
```

### 4. Svelte 5 `$derived`/getter source becomes serializable state plus selectors

```typescript
// migration/profile-runes-before.svelte.ts
declare function $state<T>(value: T): T;
declare function $derived<T>(value: T): T;

export const profile = $state({ firstName: "Ada", lastName: "Lovelace" });
export const displayName = $derived(`${profile.firstName} ${profile.lastName}`);
```

```typescript
// src/lib/store/slices/profile/profile-selectors.ts
import { store } from "$lib/store/store";

export const selectProfile = store.createSelector((state) => state.profile);
export const selectDisplayName = store.createSelector((state) => {
  const profile = selectProfile.select(state);
  return `${profile.firstName} ${profile.lastName}`;
});
```

### 5. Components consume migrated selectors as readables at initialization

```typescript
// Inside the <script> of src/lib/components/ProfileSummary.svelte
import { selectDisplayName, selectProfile } from "$lib/store/slices/profile/profile-selectors";

const profile$ = selectProfile();
const displayName$ = selectDisplayName();
```

### 6. Sagas read migrated derived values with `.effect(...)`

```typescript
// src/lib/store/slices/profile/sagas/profile-saga.ts
import { call, takeLatest } from "typed-redux-saga";
import { profileSaved } from "../profile-slice";
import { selectDisplayName } from "../profile-selectors";

function* announceProfileSaved() {
  const displayName = yield* selectDisplayName.effect();
  yield* call(console.info, `Saved ${displayName}`);
}

export function* profileSaga() {
  yield* takeLatest(profileSaved, announceProfileSaved);
}
```

### 7. ❌ Bad: inline derivation duplicates ownership

```typescript
// ❌ BAD: recomputes a migrated derived value in a handler instead of using the selector owner.
import { getItems, type Collection } from "@themislib/themis/utils/collections/collection-utils";

type Todo = { id: string; completed: boolean };
type AppState = { todos: { items: Collection<Todo, "id"> } };
type AppStore = { state: AppState; dispatch(action: { type: string; payload?: unknown }): void };

declare const store: AppStore;
declare const selectCompletedCount: { select(state: AppState): number };
declare function saveCompletedCount(count: number): { type: string; payload: [number] };

export function badSaveCompletedCount() {
  const completed = getItems(store.state.todos.items).filter((todo) => todo.completed).length;
  store.dispatch(saveCompletedCount(completed));
}

export function goodSaveCompletedCount() {
  const completed = selectCompletedCount.select(store.state);
  store.dispatch(saveCompletedCount(completed));
}
```

## Rules

- One selector per derived expression — keep selectors narrow so proxy-tracking
  memoization can short-circuit re-computation.
- Compose upstream selectors with `upstream.select(state)` inside the body;
  never call `upstream()` there because that is the component-init readable mode.
- For selectors parameterized by an id or key, put the arguments on
  `store.createSelector((state, arg) => ...)` instead of creating a new selector
  per call site.
- Derived arrays are valid selector outputs, not entity-array storage. Normalize
  the slice using `../../../core/collections/SKILL.md` → **Shape and imports**.
- When wiring migrated consumers, apply `../../selector-lifecycle/SKILL.md` →
  **Call-mode map** for saga, handler, test, and component reads.

## Cross-References

- `../../selectors/SKILL.md` — selector authoring, composition, and cache contracts
- `../../selector-lifecycle/SKILL.md` — readable / direct / saga usage
- `../component-migration/SKILL.md` — component consumption after selector migration

