---
name: svelte/selectors
description: >-
  Use when authoring or composing Svelte Store-bound selectors with
  store.createSelector, including collection lookups, cache behavior, and
  stable arguments. Call modes belong to svelte/selector-lifecycle.
type: sub-skill
requires:
  - svelte
  - core/state-integrity
triggers:
  - create selector
  - cached selector
  - collection selector
  - proxy memoization
---
# Selectors — `store.createSelector` / collection utility reads

> Operational guidance for selector authoring. Full API reference and examples: `@themislib/themis/docs/SELECTORS.md`. Public facade: `store.createSelector(...)` from `@themislib/themis/svelte-store`; selector/cache internals are package-private implementation context.

## Use when

- Adding derived values, filtered/sorted views, counts, display labels, `has*` booleans, or entity lookups.
- Replacing duplicated reducer state with computed state.
- Defining selector composition, cache contracts, and stable arguments.

## Choose the factory

- `store.createSelector(...)` for app-local selectors next to a configured Svelte
  Store; it preserves `StoreState<typeof store>` inference after reducer
  registration and returns Svelte readables from direct calls.
- Generic/shared selector helpers should accept a configured Store and create selectors through `store.createSelector(...)`; do not import standalone selector creation utilities from the package.
- Use public collection utilities such as `getItem(collection, id)` and `getItems(collection)` inside `store.createSelector(...)` callbacks for O(1) item lookup and ordered materialization.
- Do not import standalone selector creation utilities from package subpaths or inject selector behavior through Store constructors; selector creation is Store-bound public API.

## Call-site handoff

After defining a selector, choose how to consume it using
`../selector-lifecycle/SKILL.md` → **Call-mode map**, **Do**, and **Don't**.
That owner covers component-init reads, handlers/async/tests, saga effects,
composition call modes, explicit `.withStore` binding, and selector-channel
compatibility. Channel helper choice and args tuples live in
`../../core/selector-channels/SKILL.md` → **Choose the helper** and **Do**.

## Selector caching

- Store-created selectors have internal selector-result caching/memoization.
- Direct readable outputs are cached per Store instance + selector + arguments. Never-subscribed outputs and concurrent live consumers reuse the same Svelte readable. Removing one of several consumers retains it; removing the final subscriber evicts that output even if JavaScript references remain. The next identical call creates a new readable. Store disposal evicts all its outputs; cache counts are not active-subscriber counts.
- Do not wrap selector callbacks or selector calls in extra `memoize`, `cache`, manual cache maps, debounce, or throttle layers solely for performance.
- Prefer the same Store-bound selector + same arguments over props drilling when the consumer can use it directly; choose its call mode through `../selector-lifecycle/SKILL.md` → **Call-mode map**.

## Stable selector arguments

- Prefer primitive scalar selector arguments: ids, booleans, enum strings,
  numbers, `null`, or `undefined`.
- Do not pass freshly constructed object, array, or function arguments to
  `selectFoo(...)`, `.select(state, ...)`, `.effect(...)`, `.withStore(store)(...)`,
  selector-channel args tuples, or `waitFor` args tuples.
- Object/function args are valid only when the identity is stable and intentional,
  such as a module constant, memoized config, existing source object, or other
  stable reference supported by the selected Store family.
- Prefer selector definitions like `(state, id, includeArchived)` over
  `(state, { id, includeArchived })`; destructure an object arg only when the
  selector contract documents that callers pass a stable object identity.

## Do

- Search for an existing selector owner by name, entity, operation, and output shape before adding one.
- Keep derived data out of reducer state and expose it through selectors.
- Compose selectors with `.select(state)` so there is one canonical implementation.
- Back entity lookup selectors with `Collection<T, K>` rather than repeated array scans.
- Treat `@internal_` state domains as implementation details even when memoization behavior references them.
- Prefer direct Store-bound selector reuse over drilling derived props when the consumer is in valid readable context and can call the same selector with the same args.
- Split selector options objects into scalar selector parameters when possible so
  repeated calls share stable cache keys.

## Don't

- Do not call the readable form inside another selector; compose with `.select(state)` and follow `../selector-lifecycle/SKILL.md` → **Don't** for other call sites.
- Do not duplicate selector bodies in multiple files.
- Do not store selector outputs in reducer state.
- Expose named selectors for saga consumers; saga call-site rules live in `../selector-lifecycle/SKILL.md` → **Do**.
- Do not add manual memoization/cache/debounce/throttle wrappers inside selector callbacks or around selector calls just to improve selector performance.
- Do not hide fresh selector object/array/function args behind helper functions;
  pass stable scalar args or a stable intentional reference instead.

## Examples

### 1. Create app-local selectors from the configured Store

```ts
import { store } from "$lib/store";

export const selectTodoCount = store.createSelector((state) => {
  return state.todos.collection.ids.length;
});
```

### 2. Use parameterized selectors for entity lookup

```ts
export const selectTodoById = store.createSelector((state, todoId: string) => {
  return state.todos.collection.map[todoId];
});

const selectedTodo = selectTodoById.select(store.state, activeTodoId);
```

Prefer scalar parameters like `activeTodoId`. Avoid inline object arguments such
as `{ id: activeTodoId }` unless that object reference is stable and
intentionally part of the selector contract.

### Compose selectors with .select(state), not readable calls

```ts
export const selectVisibleTodos = store.createSelector((state) => {
  const todos = selectAllTodos.select(state);
  const filter = selectTodoFilter.select(state);
  return todos.filter((todo) => filter.showCompleted || !todo.completed);
});
```

### 4. Back collection reads with public collection utilities

```ts
import { getItem, getItems, type Collection } from "@themislib/themis/utils/collections/collection-utils";

export const selectTodosCollection = store.createSelector(
  (state): Collection<Todo, "id"> => state.todos.collection
);
export const selectTodo = store.createSelector((state, id: string) => getItem(selectTodosCollection.select(state), id));
export const selectTodos = store.createSelector((state) => getItems(selectTodosCollection.select(state)));
```

### 5. Pass a configured Store into shared selector helpers

```ts
import type { store as appStore } from "$lib/store";

export function createProjectSelectors(store: typeof appStore) {
  const selectProjects = store.createSelector((state) => state.projects.items);
  const selectProject = store.createSelector((state, id: string) => selectProjects.select(state)[id]);
  return { selectProjects, selectProject };
}
```

The configured app Store has a `projects` reducer whose `items` is a record
keyed by project id. Its concrete type preserves that state shape; a bare
`Store` defaults to an empty app state map and cannot type this helper.

### Explicit readable binding

For SSR/services that already own an initialized Store, follow
`../selector-lifecycle/SKILL.md` → **Bind explicitly with .withStore when no Svelte context is available**.
This is a consumption choice, not a second selector factory or cache.

### 7. ❌ Bad: creating selectors in lifecycle code and storing derived state

```ts
// BAD: every call creates a selector owner and duplicates derived state ownership.
function createVisibleTodoReadable(showCompleted: boolean) {
  const selectVisibleTodos = store.createSelector((state) =>
    selectTodos.select(state).filter((todo) => showCompleted || !todo.completed)
  );
  return selectVisibleTodos();
}

export const selectVisibleTodosOnce = store.createSelector((state) => {
  const filter = selectTodoFilter.select(state);
  return selectTodos.select(state).filter((todo) => filter.showCompleted || !todo.completed);
});
```

## Verification cues

- Selector tests use `.select(mockState, ...)` and cover composition if one selector depends on another.
- Reducer tests do not assert stored derived fields for values that belong in selectors.
- Manual overlap check confirms call-mode procedures are owned by `../selector-lifecycle/SKILL.md` → **Call-mode map**; this skill retains authoring/composition/cache examples.

## See also

- `@themislib/themis/docs/SELECTORS.md` — human reference and examples for all call forms.
- `../selector-lifecycle/SKILL.md` — lifecycle crash prevention.
- `../../core/selector-channels/SKILL.md` — reacting to selector changes from sagas.
- `../../core/collections/SKILL.md` — normalized state shape and collection utilities used by selectors.
- `../../core/state-integrity/SKILL.md` — canonical derived-value ownership.
- `../../core/testing/SKILL.md` — `.select(state)` testing rule.
