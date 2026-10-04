---
name: state-reducer
description: Pure switch/case reducers for the chota-react-saga template — initial-state file, three-phase async cases per CRUD verb, optimistic mutations with `previousState<Items>` rollback, fall-through SUCCESS/ERROR for toggle and delete.
when_to_use: Authoring or reviewing `<slice>.initial.js` and `<slice>.reducer.js`; verifying every action type from `state-actions` has a matching case (or falls through `default`); ensuring optimistic ops capture rollback state on the REQUEST.
paths:
  - "**/state/**/*.initial.{js,ts}"
  - "**/state/**/*.reducer.{js,ts}"
---

# Reducer (Saga template)

## What is a Reducer?

A reducer is a pure function `(state, action) → next state`. It's the only piece of code in the app allowed to *describe* state changes; everything else (UI, sagas, selectors) only reads. In the saga template each domain slice has its own reducer; `combineReducers` glues them into the root reducer.

## Key Principles

1. **Initial state lives in its own file.** `<slice>.initial.js` exports `intial<Slice>State` (note the legacy spelling without the 'i' — preserved for the chota-react-saga template's import surface). Reducer tests import it directly.

2. **Three cases per async op, one per sync op.** Every async CRUD verb owns a triple of `case <OP>_<ENTITY>`, `case <OP>_<ENTITY>_SUCCESS`, `case <OP>_<ENTITY>_ERROR`. Sync ops collapse to one case.

3. **`isLoading`, `isContentLoading`, `isActionLoading`.** Three independent flags. `isContentLoading` is set during READ (full reload). `isActionLoading` is set during CREATE/UPDATE. The wider `isLoading` flag covers both. The UI picks which one to render against.

4. **Optimistic on the REQUEST, rollback on the ERROR.** For toggle/delete, the REQUEST case mutates the items list AND captures `previousState<Items>: [...state.<items>]` so the saga can read it on failure. The fall-through `case TOGGLE_X_SUCCESS: case DELETE_X_SUCCESS:` clears `previousState<Items>` to `undefined`.

5. **Spread for immutability.** Never mutate `state`; always `{ ...state, … }`. Same for nested objects. The reducer is the source of truth for that invariant.

6. **Default branch returns current state.** No `throw`, no `console.warn`. Unknown actions are an expected condition (other slices' actions reach this reducer too).

## Best Practices

✅ **DO**:
- Import `<slice>.initial.js` as `intial<Slice>State` — the legacy spelling matches what other files export.
- Import the helper transforms (e.g. `toggleCheckedState`) from `<slice>.helper.js`; the helper is shared with the saga.
- Keep `let <items> = []` declared at the top of the function when the reducer rebuilds the list (update/toggle/delete) to avoid `const` rebinding noise.
- Group cases in the order **READ, CREATE, EDIT, UPDATE, TOGGLE, DELETE**; group SUCCESS/ERROR right after their REQUEST.

❌ **DON'T**:
- Don't dispatch from a reducer (mutating `dispatch` from inside violates purity).
- Don't read `Date.now()`, `Math.random()`, or `window.*` from a reducer. Side effects belong to the saga.
- Don't keep entity ids in `currentTodoItem` after a successful UPDATE — clear it back to `intial<Slice>State.currentTodoItem` so the form resets.

## Code Patterns

### Initial state (`<slice>.initial.js`)

```javascript
const intialTodoState = {
  isLoading: false,
  isActionLoading: false,
  isContentLoading: false,
  error: '',
  todoItems: [],
  currentTodoItem: { text: '', id: '' }
};

export default intialTodoState;
```

### Reducer (`<slice>.reducer.js`)

```javascript
import { toggleCheckedState } from "./todo.helper";
import intialTodoState from "./todo.initial";
import {
  CREATE_TODO, CREATE_TODO_SUCCESS, CREATE_TODO_ERROR,
  READ_TODO,   READ_TODO_SUCCESS,   READ_TODO_ERROR,
  EDIT_TODO,
  UPDATE_TODO, UPDATE_TODO_SUCCESS, UPDATE_TODO_ERROR,
  TOGGLE_TODO, TOGGLE_TODO_SUCCESS, TOGGLE_TODO_ERROR,
  DELETE_TODO, DELETE_TODO_SUCCESS, DELETE_TODO_ERROR,
} from "./todo.type";

const todo = (state = intialTodoState, action) => {
  let todoItems = [];

  switch (action.type) {

    // ── Standard Content Loading ────────────────────────────────────────
    case READ_TODO:
      return { ...state, isLoading: true, isContentLoading: true };

    case READ_TODO_SUCCESS:
      return { ...state, isLoading: false, isContentLoading: false, todoItems: action.payload };

    case READ_TODO_ERROR:
      return { ...state, isLoading: false, isContentLoading: false, error: action.error };

    // ── Standard Action Modification ────────────────────────────────────
    case CREATE_TODO:
      return { ...state, isLoading: true, isActionLoading: true, currentTodoItem: action.payload };

    case CREATE_TODO_SUCCESS:
      return {
        ...state,
        isLoading: false, isActionLoading: false,
        todoItems: [...state.todoItems, {
          id: action.payload.id,
          text: action.payload.text,
          completed: false,
        }],
        currentTodoItem: intialTodoState.currentTodoItem,
      };

    case CREATE_TODO_ERROR:
      return {
        ...state,
        isLoading: false, isActionLoading: false,
        error: action.error,
        currentTodoItem: intialTodoState.currentTodoItem,
      };

    // ── Selected Entity (sync stage step) ───────────────────────────────
    case EDIT_TODO:
      return { ...state, currentTodoItem: action.payload };

    // ── Partial Action Modification ─────────────────────────────────────
    case UPDATE_TODO:
      todoItems = state.todoItems.map((todo) =>
        todo.id === action.payload.id
          ? { ...todo, text: action.payload.text }
          : todo
      );
      return { ...state, isActionLoading: true, todoItems, currentTodoItem: action.payload };

    case UPDATE_TODO_SUCCESS:
      return { ...state, isActionLoading: false, currentTodoItem: intialTodoState.currentTodoItem };

    case UPDATE_TODO_ERROR:
      return { ...state, error: action.error, isActionLoading: false, currentTodoItem: intialTodoState.currentTodoItem };

    // ── Parallel Action Modification (optimistic) ───────────────────────
    case TOGGLE_TODO:
      todoItems = state.todoItems.map((todo) =>
        todo.id === action.payload.id ? toggleCheckedState(todo) : todo
      );
      return { ...state, previousStateTodoItems: [...state.todoItems], todoItems };

    case DELETE_TODO:
      todoItems = state.todoItems.filter((todo) => todo.id !== action.payload.id);
      return {
        ...state,
        previousStateTodoItems: [...state.todoItems],
        todoItems,
        currentTodoItem: intialTodoState.currentTodoItem,
      };

    // toggle and delete share fall-through SUCCESS/ERROR cases:
    case TOGGLE_TODO_SUCCESS:
    case DELETE_TODO_SUCCESS:
      return { ...state, previousStateTodoItems: undefined, isLoading: false };

    case TOGGLE_TODO_ERROR:
    case DELETE_TODO_ERROR:
      return {
        ...state,
        previousStateTodoItems: undefined,
        isLoading: false,
        error: action.error,
        todoItems: action.payload,   // saga sends the rollback list as payload
      };

    default:
      return state;
  }
};

export default todo;
```

## Related Terminologies

- **Actions** — every type matched in `switch` is exported from `<slice>.type.js`.
- **Saga** — emits SUCCESS/ERROR actions that this reducer responds to.
- **Helper** — `<slice>.helper.js` provides `toggleCheckedState` (shared with the saga).
- **Selectors** — derive view-data from this state shape; they're the only consumers downstream.

## Quality Gates

- [ ] Every type imported is matched in a `case`; nothing `default`-only.
- [ ] Optimistic ops set `previousState<Items>` on REQUEST.
- [ ] SUCCESS clears `currentTodoItem` and `previousState<Items>`.
- [ ] No `await`, no `dispatch`, no `Math.random()`, no `Date`.
- [ ] `default` returns `state` untouched.

**Source**: `templates/chota-react-saga/src/state/todo/todo.reducer.js`, `todo.initial.js`
