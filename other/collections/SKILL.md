---
name: core/collections
description: >-
  Use for normalized entity storage with Themis Collection helpers, including
  immutable CRUD, lookups, filtering, and reference counting.
type: sub-skill
library: themis
requires:
  - core
  - core/reducers
sources:
  - "@themislib/themis/docs/COLLECTIONS.md"
  - "@themislib/themis/utils/collections/collection-utils"
triggers:
  - create collection
  - addItem collection
  - upsert item
  - reference counting
---
# Collections — `Collection<T, K>`

> Operational guidance for normalized entity state. Full API reference and examples: `@themislib/themis/docs/COLLECTIONS.md`. Public API: `@themislib/themis/utils/collections/collection-utils`.

## Use when

- State contains entities with a unique string id and needs O(1) lookup plus stable ordering.
- Reducers need immutable add/update/remove/upsert operations.
- Multiple features reference shared entities and need reference-count cleanup.

## Shape and imports

- A collection is `{ idField, ids, map, refsCount }`; `ids` preserves order and `map` stores id → item.
- Import helpers from `@themislib/themis/utils/collections/collection-utils`.
- Use selectors, not components, to read collection contents.

## Do

- Initialize with `createCollection<T, K>(idField, items?)`.
- Use helpers (`addItem`, `addItems`, `upsertItem`, `updateItem`, `replaceItem`, `removeItem`, `filterCollection`) instead of mutating `.ids`, `.map`, or `.refsCount`.
- Preserve parent reducer reference equality when a helper returns the same collection reference.
- Use `getItem` for O(1) reads and `getItems` for ordered materialization.
- Use `store.createSelector(...)` plus `getItem`/`getItems` for selector-facing reads.

## Reference counting cues

- Use `addItemAndCountRef` / `upsertItemAndCountRef` when adding shared entities and incrementing ownership together.
- Use `increaseRefsCount` and `decreaseRefsCount` for manual ownership changes.
- `decreaseRefsCount` removes the item from `ids`, `map`, and `refsCount` when the count reaches `<= 0`.
- `getRefsCount` returns `1` for an existing item with no explicit count and `0` for a missing item.

## Don't

- Do not store entities as `Item[]` when id lookup is needed.
- Do not store `Map`/`Set` in Redux state; use collections or plain records.
- Do not add derived flags to item records when a separate relationship map or selector can represent the view.
- Do not call `getItems(collection).find(...)` for id lookup; use `getItem(collection, id)`.
- Do not import collection utilities directly into components; expose app reads through selectors.

## Examples

### Serializable initial collection state

```ts
import { type Collection, createCollection } from "@themislib/themis/utils/collections/collection-utils";

type Todo = { id: string; title: string; completed: boolean };
type TodosState = { todos: Collection<Todo, "id"> };

export const initialState: TodosState = {
  todos: createCollection<Todo, "id">("id"),
};
```

### Add, update, upsert, and remove in reducers

```ts
import { addItem, createCollection, removeItem, updateItem, upsertItem } from "@themislib/themis/utils/collections/collection-utils";

type Todo = { id: string; title: string; completed: boolean };
const state = { todos: createCollection<Todo, "id">("id") };

const todos = addItem(state.todos, { id: "todo-1", title: "Draft", completed: false });
const renamed = updateItem(todos, { id: "todo-1", title: "Ship docs" });
const synced = upsertItem(renamed, { id: "todo-2", title: "Review", completed: false });
const withoutDraft = removeItem(synced, "todo-1");

const nextState = withoutDraft === state.todos ? state : { ...state, todos: withoutDraft };
```

### Reference-count shared entities

```ts
import { addItemAndCountRef, createCollection, decreaseRefsCount, getRefsCount } from "@themislib/themis/utils/collections/collection-utils";

type Todo = { id: string; title: string; completed: boolean };
const state = { todos: createCollection<Todo, "id">("id") };

const withOwner = addItemAndCountRef(state.todos, { id: "todo-1", title: "Draft", completed: false });
const ownerCount = getRefsCount(withOwner, "todo-1");
const afterRelease = decreaseRefsCount(withOwner, "todo-1");

ownerCount satisfies number;
afterRelease.ids satisfies string[];
```

### Collection selectors expose item and ordered-list reads

```ts
import { Store } from "<selected Store family package>";
import { type Collection, createCollection, getItem, getItems } from "@themislib/themis/utils/collections/collection-utils";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type Todo = { id: string; title: string; completed: boolean };
type TodosState = { todos: Collection<Todo, "id"> };
const initialState: TodosState = { todos: createCollection<Todo, "id">("id") };
const todosReducer = createReducer(initialState);
const store = new Store({ todos: todosReducer });

export const selectTodo = store.createSelector((state, id: string) => getItem(state.todos.todos, id));
export const selectTodos = store.createSelector((state) => getItems(state.todos.todos));
```

### Plain arrays are fine for tiny ordered facts without id lookup

```ts
type BreadcrumbState = {
  labels: string[];
};

const breadcrumbs: BreadcrumbState = {
  labels: ["Projects", "Settings"],
};
```

### ❌ Bad: mutating internals corrupts normalized identity

```ts
import { type Collection, createCollection } from "@themislib/themis/utils/collections/collection-utils";
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type Todo = { id: string; title: string; completed: boolean };
type TodosState = { todos: Collection<Todo, "id"> };
const initialState: TodosState = { todos: createCollection<Todo, "id">("id") };
const renameTodo = createAction("todos/rename", (id: string, title: string) => ({ id, title }));

// BAD: direct ids/map writes can create duplicates or dangling ids and bypass helper no-op behavior.
export const todosReducer = createReducer(initialState).with(renameTodo, (state, { payload }) => {
  state.todos.map[payload.id] = { ...state.todos.map[payload.id], title: payload.title };
  state.todos.ids.push(payload.id);
  return state;
});
```

## Verification cues

- Reducer tests cover add/update/remove/upsert branches and no-op same-reference behavior.
- Selector tests cover item lookup and list materialization using `.select(mockState, ...)`.
- Manual review checks that detailed helper examples remain in `@themislib/themis/docs/COLLECTIONS.md`; this skill keeps only implementation cues.

## See also

- `@themislib/themis/docs/COLLECTIONS.md` — human reference for helper signatures and examples.
- `core/reducers/SKILL.md` — pure immutable reducer updates.
- Selected Store family selector skill — collection selector helpers.
- `core/state-serialization/SKILL.md` — collections as serializable alternatives to `Map`/`Set`.