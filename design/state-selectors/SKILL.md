---
name: state-selectors
description: Selector functions for the chota-react-saga template — colocated with each slice, return derived view-data from the saga state shape (isLoading/isContentLoading/isActionLoading/error/<items>/<current>), filter/sort projections that combine slices (e.g. visibleTodos × selectedFilter).
when_to_use: Writing `selectXxx`/`getVisibleXxx` helpers colocated with a slice; deriving filtered or aggregated lists from `<items>` and the filter slice; replacing raw `state.x.y` access in containers.
paths:
  - "**/state/**/*.selectors.{js,ts}"
---

# Selectors (Saga template)

## What is a Selector?

A selector is a pure function `(state) => derivedValue` that hides the state shape from consumers. Containers call selectors with `useSelector(selector)`; components only see the projected view-data, never the slice's internal flags or normalisation tricks.

## Key Principles

1. **Colocate selectors with their slice.** `<slice>.selectors.js` lives next to `<slice>.reducer.js`. Cross-slice selectors live where the *primary* slice lives (e.g. `getVisibleTodos` lives in `todo.selectors.js` because that's where the items list lives, even though it also reads `filters`).

2. **One selector per derived shape.** A selector returns either a primitive (`isLoading`), a slice ref (`state.todo`), a list (`state.todo.todoItems`), or a derived projection (`getVisibleTodos`). Don't fuse unrelated derivations into one selector.

3. **Pass-through selectors are not boilerplate, they're API.** `getTodoItems = (state) => state.todo.todoItems` looks redundant but it's the contract: tomorrow you can normalise the slice or rename the field, and only this file changes.

4. **Cross-slice selectors take both slices as args.** The `getVisibleTodos(todoSlice, filterId)` pattern keeps the selector pure and easily testable; the container picks the slices via `useSelector` and passes them in.

5. **Memoise only when measured.** Plain selectors are cheap. Reach for `createSelector` (reselect) when a selector returns a NEW array/object on every call AND that result is consumed by a memoised component — otherwise you'll see needless re-renders.

## Best Practices

✅ **DO**:
- Name boolean flag selectors `is…` (`isLoading`, `isContentLoading`).
- Name list selectors `get<Plural>` and projections `get<Verb><Plural>` (e.g. `getVisibleTodos`).
- Keep selectors stateless: no module-level caches; if you need memoisation, use reselect.

❌ **DON'T**:
- Don't fetch inside selectors. Sagas do that.
- Don't read `localStorage` or `Date.now()` from a selector. Tests will fail nondeterministically.
- Don't return `state` itself — projects always start one level in (`state.todo`).

## Code Patterns

### Slice selectors (`todo.selectors.js`)

```javascript
// Saga state shape:
//   { isLoading, isActionLoading, isContentLoading, error,
//     todoItems[], currentTodoItem, previousStateTodoItems? }

// Pass-through projections — the API for downstream consumers.
export const getTodo = (state) => state.todo;
export const getTodoItems = (state) => state.todo.todoItems;
export const getCurrentTodoItem = (state) => state.todo.currentTodoItem;

// Lifecycle flags (the UI picks one to render against).
export const isContentLoading = (state) => state.todo.isContentLoading;
export const isActionLoading  = (state) => state.todo.isActionLoading;
export const getError         = (state) => state.todo.error;

// Cross-slice: takes the slice + the filter id, returns the view list.
// (the container picks both via useSelector and calls this in render).
export const getVisibleTodos = (todoSlice, filterId) => {
  const items = todoSlice.todoItems;
  switch (filterId) {
    case "SHOW_COMPLETED": return items.filter((t) => t.completed);
    case "SHOW_ACTIVE":    return items.filter((t) => !t.completed);
    case "SHOW_ALL":
    default:               return items;
  }
};
```

### Filter slice selectors (`filters.selectors.js`)

```javascript
// The filter slice is an array of { id, label, selected }.
export const getSelectedFilter = (state) =>
  state.filters.find((f) => f.selected) || state.filters[0];

export const getFilters = (state) => state.filters;
```

### Calling from a container

```jsx
import { useSelector } from "react-redux";
import { getSelectedFilter } from "../state/filters/filters.selectors";
import { getVisibleTodos } from "../state/todo/todo.selectors";

const selectedFilter = useSelector(getSelectedFilter);
const todoData = useSelector((state) =>
  getVisibleTodos(state.todo, selectedFilter.id)
);
```

### When to add `createSelector`

```javascript
// Reach for reselect when a derived projection is hot AND consumed by
// a memoised component. Most slices don't need this.
import { createSelector } from "reselect";

const selectTodo = (state) => state.todo;
const selectFilter = (state, filterId) => filterId;

export const makeGetVisibleTodos = createSelector(
  [selectTodo, selectFilter],
  (todoSlice, filterId) => /* …same logic as above… */
);
```

## Related Terminologies

- **Reducer** — owns the state shape selectors project from.
- **Container** — the only call-site of `useSelector(selector)`.
- **Filters** — the cross-slice friend of `getVisibleTodos`.

## Quality Gates

- [ ] One selectors file per slice; no mixing.
- [ ] Pass-through selectors exist for every consumed field.
- [ ] No side effects (no fetch, no `Math.random`, no `Date.now`).
- [ ] Cross-slice selectors take slice args, not `state`.
- [ ] `createSelector` only used where memoisation is measurably needed.

**Source**: `templates/chota-react-saga/src/state/todo/todo.selectors.js`, `filters.selectors.js`
