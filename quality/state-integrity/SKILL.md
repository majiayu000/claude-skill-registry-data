---
name: core/state-integrity
description: >-
  Use when modeling or reviewing canonical Redux state and
  action/selector/saga ownership, including derived data, duplicated entities,
  and duplicate implementations.
type: sub-skill
requires:
  - core
triggers:
  - canonical state
  - derived state
  - duplicate state
  - duplicate actions
  - duplicate selectors
  - duplicate sagas
  - state integrity
---
# State Integrity & Deduplication

> This is a hard gate for every Redux slice. Pair this guidance with architecture
> validation so enforcement does not rely on ad hoc review: use
> `npm run validate:architecture` in this repository, or run ESLint with the
> app's composed domain root config imported from
> `@themislib/themis/eslint-plugins` in a consuming app.

## MUST / NEVER rules

- **MUST** store each domain fact in exactly one canonical place.
- **MUST** use `Collection<T, K>` for entities with ids and primitive id arrays
  only for ordering, selection, or membership.
- **MUST** store ids/references, not duplicate entity objects, when one slice
  points at records owned by another slice.
- **MUST** derive counts, filters, sorted lists, booleans, display labels, joined
  views, and selected entity objects in selectors.
- **MUST** keep one canonical owner for each action type, selector, saga watcher,
  and saga registration name.
- **NEVER** add `filteredItems`, `visibleItems`, `activeCount`, `hasUnread`,
  `selectedItem`, or similar reducer-maintained fields when a selector can
  compute them from canonical state.
- **NEVER** keep both `Item[]` and `itemsById`, both `ids` and a parallel entity
  array, or two maps/collections for the same records.
- **NEVER** define the same action type string, selector implementation, saga
  watcher, or saga registration in multiple files.

## Wrong / correct state shapes

```typescript
// ❌ WRONG — duplicates records and stores selector outputs
type TodosState = {
  todos: Todo[];
  todosById: Record<string, Todo>;
  completedTodos: Todo[];
  completedCount: number;
  selectedTodo: Todo | null;
};
```

```typescript
// ✅ CORRECT — canonical records plus ids; selectors derive the rest
import { store } from "$lib/store/store";

type TodosState = {
  todos: Collection<Todo, "id">;
  selectedTodoId: string | null;
};

export const selectCompletedTodos = store.createSelector((state) =>
  getItems(state.todos.todos).filter((todo) => todo.completed),
);
export const selectSelectedTodo = store.createSelector((state) =>
  state.todos.selectedTodoId
    ? state.todos.todos.map[state.todos.selectedTodoId]
    : null,
);
```

```typescript
// ❌ WRONG — slice B stores a copied User object owned by users slice
type CommentsState = { comments: Collection<Comment, "id">; author: User };

// ✅ CORRECT — slice B stores the relationship; users slice owns User records
type CommentsState = { comments: Collection<Comment, "id">; authorId: string };
```

## Wrong / correct canonical owners

```typescript
// ❌ WRONG — same action type has two owners
export const loadTodos = createAction("todos/load");      // todos-slice.ts
export const refreshTodos = createAction("todos/load");   // dashboard-slice.ts

// ✅ CORRECT — one owner exports the action; other files import it
export const loadTodos = createAction("todos/load");      // todos-slice.ts
```

```typescript
import { store } from "$lib/store/store";

// ❌ WRONG — duplicated selector body in another slice/file
export const selectOpenTodos = store.createSelector((state) =>
  getItems(state.todos.todos).filter((todo) => !todo.completed),
);

// ✅ CORRECT — import or compose the canonical selector
export const selectOpenTodoCount = store.createSelector(
  (state) => selectOpenTodos.select(state).length,
);
```

```typescript
// ❌ WRONG — two watchers own the same trigger and can race
yield* takeLatest(loadTodos, loadTodosWorker);
yield* takeLatest(loadTodos, refreshTodosWorker);

// ✅ CORRECT — one watcher owns the trigger and delegates internally
yield* takeLatest(loadTodos, loadTodosWorker);
```

## Preflight search protocol

Before adding state, actions, selectors, or sagas:

1. Name the entity, operation, and slice that should own it.
2. Search state/type ownership for existing canonical data:
   `grep -RInE "TodosState|Collection<|createCollection|selectedTodoId|todosById|todoIds" src docs skills`.
3. Search action ownership before creating an action:
   `grep -RInE "createAction|createAsyncAction|todos/load|loadTodos" src docs skills`.
4. Search selector ownership before creating or copying a selector:
   `grep -RInE "store\.createSelector|selectOpenTodos" src docs skills`.
5. Search saga ownership before adding watchers or registrations:
   `grep -RInE "takeEvery|takeLatest|takeLeading|new Store|store\.runSaga|loadTodos" src docs skills`.
6. If an owner exists, import/extend/compose it instead of creating a parallel
   implementation. If no owner exists, create one in the owning slice and record
   why that slice is canonical.
7. Include the searched paths/terms and ownership decision in the handoff.

Use `rg` instead of `grep -RInE` when available; the required outcome is the
same: prove you looked for existing canonical state and owners before adding new
ones.

## Automated architecture gate workflow

Run architecture validation before handoff when a change touches Redux state,
action creators, selectors, saga watchers/registrations, or this package's
state/action/selector/saga guidance docs. Use `npm run validate:architecture`
inside this repository; in a consuming app, run ESLint with the app's composed
domain root config imported from `@themislib/themis/eslint-plugins`.
Inside this repository, passing means the command exits 0 and prints
`[architecture-validation] no architecture gate violations found` plus the number
of scanned source files. `npm run validate:release` also runs this gate first in
the maintainer workflow.

Include this evidence in the handoff:

1. Exact architecture-validation command and result.
2. Search terms/paths used for state, action, selector, and saga ownership.
3. The canonical state owner and why no stored field is selector-derivable or a
   duplicate entity representation.
4. The canonical owner for each new action type, selector, saga watcher, or saga
   registration, or a statement that no new owner was added.

Violations must be fixed before handoff unless they are reviewed false positives
or intentional temporary exceptions. Use only the gate's documented ignore
comments and include a reason:

- `// eslint-disable-next-line architecture/duplicate-action-type -- compatibility alias until migration ends`
- `/* eslint-disable architecture/suspicious-state-field -- persisted API snapshot, not local derivation */`

Prefer rule-specific ignores. Verifiers should reject broad ignores, missing
reasons, or exceptions that hide derived/duplicated Redux state or duplicate
actions/selectors/sagas without a migration, compatibility, or external-data
constraint.

## Verifier handoff expectations

Implementation handoffs must include:

1. The canonical state shape and why no stored field is selector-derivable.
2. Any new action, selector, or saga owner, or a statement that no new owner was
   added.
3. Search commands/terms used for state, actions, selectors, and sagas.
4. Tests or selector/reducer assertions covering derived values and no-op
   reference equality where state changed.
5. Architecture gate output for all Redux state/action/selector/saga changes, or
   an explicit statement that the task was unrelated to those surfaces.

## See also

- `core/core-policy` — always-on Redux ownership rules.
- `core/collections` — canonical entity storage.
- Selected Store family selector skill — where derived values belong.
- `core/verifier` — review gates for these rules.