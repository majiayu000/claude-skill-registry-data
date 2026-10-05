---
name: core/file-structure
description: >-
  Use when organizing Themis slices, types, selectors, sagas, and tests,
  including naming, reducer registration, and app saga startup placement.
  Store lifecycle mechanics belong to core/saga-manager.
type: sub-skill
requires:
  - core
triggers:
  - slice layout
  - slice directory
  - saga-only slice
  - scaffold slice
---
# File Structure & Registration

> Source: @themislib/themis/docs/ARCHITECTURE.md → Slice File Structure + Store Initialization; see [Core leaf routes](../SKILL.md#core-leaf-routes) for related owners.

## Setup — slice directory layout

```
src/slices/{slice-name}/
  {slice-name}-types.ts          # Types, interfaces, enums (safe to import from any process)
  {slice-name}-slice.ts          # The only action/reducer owner module for this slice
  {slice-name}-selectors.ts      # The only selector owner module for this slice
  {slice-name}-slice.test.ts     # Reducer tests
  sagas/
    {slice-name}-saga.ts         # Saga logic
    {slice-name}-saga.test.ts    # Saga tests
```

Each slice directory owns exactly one `*-slice.ts` module and exactly one `*-selectors.ts` module. If a feature needs multiple logical slices, split them into sibling directories named after the slice owners instead of adding multiple slice or selectors files to one directory. Physical paths stay kebab-case, while the logical slice identity used in reducer-map keys and action namespaces is always camelCase (for example `src/slices/user-preferences/user-preferences-slice.ts` registers as `userPreferences` and emits `"userPreferences/updateTheme"`).

The top-level store lives at `src/store.ts` (or wherever you export your `Store` instance) and registers all slices. `@themislib/themis/docs/ARCHITECTURE.md` shows the short form: `src/slices/<domain>/` with the same filenames.

## Core Patterns

### Register a normal slice

```typescript
// src/store.ts
import { Store } from '<selected Store family package>';
import type { StoreState } from '@themislib/themis/types';
import { mySliceReducer } from './slices/my-slice/my-slice-slice';
import { mySliceSaga } from './slices/my-slice/sagas/my-slice-saga';

export const store = new Store({ mySlice: mySliceReducer });
export type AppState = StoreState<typeof store>;
```

Use `StoreState<typeof store>` for app state typing after constructing the store with app reducer maps. Constructor reducer maps preserve reducer-state inference without an explicit `: Store` annotation. Register only app-owned reducers. `Store` manages internal reducers such as `@internal_storeUtility` automatically under reserved `@internal_` names; do not use that prefix for app-owned registrations or couple selectors/tests to the internal state shape. For the package-owned saga manager boundary, follow [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle).

Then in the application's selected Store family root lifecycle, initialize the store and start each app saga explicitly by function. Use the selected Store family skill for component/runtime lifecycle details; core owns the file layout, saga registration, and reducer ownership rules.

For initialization order, `store.runSaga(sagaFn)`, manager naming, matching cancels,
and Store-wide teardown, follow [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle).
When deciding between root, component/layout, service, or test ownership, follow
[Application saga startup](../sagas/SKILL.md#application-saga-startup); keep the
explicit startup calls next to that owner's lifecycle wiring, not in a constructor saga map.

### Saga-only slice (no state, no reducer)

Some slices exist only to define saga trigger actions with no meaningful state. Keep the action creators and saga but **do not register a reducer**.

```typescript
// src/slices/triggers/triggers-slice.ts
import { createAction } from '@themislib/themis/utils/store/create-action';

export const rescanWorkspace = createAction('triggers/rescanWorkspace');
```

```typescript
// src/slices/triggers/sagas/triggers-saga.ts
import { takeEvery, call } from 'typed-redux-saga';
import { rescanWorkspace } from '../triggers-slice';

export function* triggersSaga() {
  yield* takeEvery(rescanWorkspace, function* () {
    yield* call(rescan);
  });
}
```

```typescript
// src/store.ts
export const store = new Store({}); // no reducer map entry; start with store.runSaga(triggersSaga)
```

### Naming conventions

- **Type definitions:** `{slice-name}-types.ts` — all types, interfaces, enums
- **State type:** `{Feature}State` (e.g., `NotificationsState`) — defined in `-types.ts`
- **Reducer:** `{feature}Reducer` (e.g., `notificationsReducer`)
- **Actions:** verb phrases (e.g., `addNotification`, `fetchItems`)
- **Selectors:** `select` prefix (e.g., `selectNotifications`, `selectIsLoading`)
- **Logical slice identity:** camelCase reducer-map keys and action namespaces (e.g., `userPreferences`)
- **Action types:** `"sliceName/actionName"` with camelCase `sliceName` (e.g., `"userPreferences/updateTheme"`)

## Common Mistakes

### ❌ Registering a reducer for a saga-only slice

Empty reducers add state-tree noise and run on every action; saga-only slices define trigger actions without state.

```typescript
// WRONG
export const noopReducer = createReducer({});
export const store = new Store({ triggers: noopReducer });
```

```typescript
// CORRECT — no reducer map entry; start the saga with store.runSaga(triggersSaga)
export const store = new Store({});
```

Source: [Saga-only slice (no state, no reducer)](#saga-only-slice-no-state-no-reducer) · **Priority: MEDIUM**

### ❌ Adding multiple slice or selectors owner files to one directory

One directory means one logical slice owner. Multiple owners make reducer keys, action namespaces, and selector ownership ambiguous.

```text
// WRONG — two logical slices in one directory
src/slices/settings/profile-slice.ts
src/slices/settings/profile-selectors.ts
src/slices/settings/theme-slice.ts
src/slices/settings/theme-selectors.ts
```

```text
// CORRECT — split by slice owner
src/slices/profile/profile-slice.ts
src/slices/profile/profile-selectors.ts
src/slices/theme/theme-slice.ts
src/slices/theme/theme-selectors.ts
```

Source: `./SKILL.md` — **Setup — slice directory layout** · **Priority: HIGH**

### ❌ Using kebab-case or snake_case as the logical slice identity

File and directory names may be kebab-case, but reducer-map keys and action namespaces must be camelCase.

```typescript
// WRONG
export const updateTheme = createAction("user-preferences/updateTheme");
export const store = new Store({ "user-preferences": userPreferencesReducer });
```

```typescript
// CORRECT
export const updateTheme = createAction("userPreferences/updateTheme");
export const store = new Store({ userPreferences: userPreferencesReducer });
```

Source: [Naming conventions](#naming-conventions) · **Priority: HIGH**

### ❌ Naming selectors without the `select` prefix

Breaks the `.select` / `.effect` lookup convention used across the codebase and tests; reviewers cannot tell a selector from a plain function.

```typescript
// WRONG
export const isLoading = store.createSelector(...);
```

```typescript
// CORRECT
export const selectIsLoading = store.createSelector(...);
```

Source: [Naming conventions](#naming-conventions) · **Priority: MEDIUM**

### ❌ Defining state types inline in `{slice-name}-slice.ts`

Cross-process imports (e.g. Electron preload) pull in the reducer and action-creator factories just to get types; always put types in `{slice-name}-types.ts`.

```typescript
// WRONG — feature-slice.ts
export type FeatureState = { items: Collection<Item, 'id'> };
export const featureReducer = createReducer<FeatureState>(...);
```

```typescript
// CORRECT — feature-types.ts
export type FeatureState = { items: Collection<Item, 'id'> };

// feature-slice.ts
import type { FeatureState } from './feature-types';
```

Source: `../core-policy/SKILL.md` — **Types live in `{slice-name}-types.ts`**; `./SKILL.md` — **Setup — slice directory layout** · **Priority: MEDIUM**

## See also

- `../core-policy/SKILL.md` — **Types live in `{slice-name}-types.ts`**
- `../actions/SKILL.md` — action naming and namespacing
- [Store saga lifecycle](../saga-manager/SKILL.md#store-saga-lifecycle) — init/run/cancel/dispose mechanics
- Selected Store family skill — Store initialization wiring