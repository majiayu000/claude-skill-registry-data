---
name: svelte/migration/writable-stores
description: >-
  Use when converting shared Svelte writable() stores or $state runes,
  including set/update calls, into Themis Redux actions and reducers.
type: sub-skill
requires:
  - core/actions
  - core/reducers
  - core/collections
  - core/state-serialization
  - svelte/migration
triggers:
  - migrate writable
  - migrate $state
  - writable to slice
  - convert setter
---
# Migration — `writable` / `$state` → Slice + Actions + Reducer

> Converts the mutable state primitives (Svelte 4 `writable` / `readable` and
> Svelte 5 `$state`) into an `initialState` + `createAction` + `createReducer`
> trio. For selector conversion see
> `../derived-stores/SKILL.md`.

## State: `writable` / `$state` → Initial State

Apply this only to fields classified as shared/domain state by
`../assessment/SKILL.md` → **Decision Framework**. The examples abbreviate types;
put application slice types in dedicated type modules per
`../../../core/core-policy/SKILL.md` → **Setup — core rules**.

```typescript
// BEFORE: Svelte store
import { writable } from "svelte/store";
export const count = writable(0);
export const username = writable("");

// ─── OR with Svelte 5 runes ───
declare function $state<T>(value: T): T;
let runeCount = $state(0);
let runeUsername = $state("");

// AFTER: Redux slice
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type CounterState = {
  count: number;
  username: string;
};

const initialState: CounterState = {
  count: 0,
  username: "",
};

export const setCount = createAction<[value: number]>("counter/setCount");
export const setUsername = createAction<[value: string]>("counter/setUsername");

export const counterReducer = createReducer<CounterState>(initialState)
  .with(setCount, (state, { payload: [value] }) => state.count === value ? state : { ...state, count: value })
  .with(setUsername, (state, { payload: [value] }) => state.username === value ? state : { ...state, username: value });
```

## State Updates: `store.set` / `store.update` → `dispatch(action())`

```typescript
// BEFORE: Svelte store
declare const count: { set(value: number): void; update(fn: (value: number) => number): void };
count.set(42);
count.update((n) => n + 1);

// ─── OR with Svelte 5 runes ───
let runeCount = 0;
runeCount = 42;
runeCount += 1;

// AFTER: Redux
// In the slice, define the actions:
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type CounterState = { count: number };
const initialState: CounterState = { count: 0 };

export const setCount = createAction<[value: number]>("counter/setCount");
export const increment = createAction("counter/increment");

export const counterReducer = createReducer<CounterState>(initialState)
  .with(setCount, (state, { payload: [value] }) => state.count === value ? state : { ...state, count: value })
  .with(increment, (state) => ({ ...state, count: state.count + 1 }));

// In the component, through the configured Store:
import { store } from "$lib/store/store";
store.dispatch(setCount(42));
store.dispatch(increment());
```

## Additional Migration Examples

### `$state` object → serializable slice state

```typescript
// migration/preferences-state.before.svelte.ts
declare function $state<T>(value: T): T;

export const preferences = $state({
  theme: "dark" as "light" | "dark",
  sidebarOpen: true,
});
```

```typescript
// src/lib/store/slices/preferences/preferences-slice.ts
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type PreferencesState = { theme: "light" | "dark"; sidebarOpen: boolean };
const initialState: PreferencesState = { theme: "dark", sidebarOpen: true };

export const setTheme = createAction<[theme: PreferencesState["theme"]]>("preferences/setTheme");
export const setSidebarOpen = createAction<[open: boolean]>("preferences/setSidebarOpen");

export const preferencesReducer = createReducer<PreferencesState>(initialState)
  .with(setTheme, (state, { payload: [theme] }) => state.theme === theme ? state : { ...state, theme })
  .with(setSidebarOpen, (state, { payload: [sidebarOpen] }) => state.sidebarOpen === sidebarOpen ? state : { ...state, sidebarOpen });
```

### Entity-array writable → `Collection`

Identified object entities use `Collection<T, K>` regardless of collection size
or lookup frequency. Arrays in Redux state hold primitive facts/ids only; see
`../../../core/collections/SKILL.md` → **Shape and imports** and **Do**.

```typescript
// src/lib/store/slices/todos/todos-slice.ts
import { createCollection, upsertItem, type Collection } from "@themislib/themis/utils/collections/collection-utils";
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type Todo = { id: string; title: string; completed: boolean };
type TodosState = { items: Collection<Todo, "id"> };

const initialState: TodosState = { items: createCollection<Todo, "id">("id") };
export const todoReceived = createAction<[todo: Todo]>("todos/todoReceived");

export const todosReducer = createReducer<TodosState>(initialState).with(
  todoReceived,
  (state, { payload: [todo] }) => {
    const items = upsertItem(state.items, todo);
    return items === state.items ? state : { ...state, items };
  }
);
```

## Common Pitfalls

- Do not copy non-serializable legacy values into the new slice. Use
  `../../../core/state-serialization/SKILL.md` → **Do**, **Don't**, and **Examples**
  for timestamps, records/collections, patterns, plain objects, functions, and promises.
- Preserve no-op identity and return new state only for actual changes. Follow
  `../../../core/reducers/SKILL.md` → **Do** and **Immutable collection update with parent no-op guard**.
- An immutable spread does not make an entity array valid Redux state. Use
  `../../../core/collections/SKILL.md` → **Add, update, upsert, and remove in reducers**;
  keep the normalized owner required by `../../../core/state-integrity/SKILL.md` → **MUST / NEVER rules**.
- Do not move persistence, fetches, logging, or clock reads into reducers.
  `../../../core/reducers/SKILL.md` → **Don't** owns purity; migrate domain effects
  using `../side-effects/SKILL.md` → **Effect ownership boundary** and **Examples**.

## Cross-References

- `../../../core/actions/SKILL.md` — full `createAction` surface
- `../../../core/reducers/SKILL.md` — full `createReducer` surface (no-op reference-equality)
- `../../../core/state-serialization/SKILL.md` — serializable state rules

