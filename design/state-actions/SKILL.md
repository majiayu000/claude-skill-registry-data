---
name: state-actions
description: Plain-object Redux actions for the chota-react-saga template — three-phase async triples (REQUEST / SUCCESS / ERROR) per CRUD verb, single-phase actions for sync ops, UPPER_SNAKE type constants, and explicit hand-written action creators (no createAsyncThunk).
when_to_use: Authoring or reviewing `<slice>.type.js` constants and `<slice>.actions.js` creators; designing new entity operations; verifying the REQUEST/SUCCESS/ERROR triple matches the reducer's three-phase switch and the saga worker's `put(...)` calls.
paths:
  - "**/state/**/*.type.{js,ts}"
  - "**/state/**/*.actions.{js,ts}"
---

# Actions (Saga template)

## What are Actions?

Actions are plain JavaScript objects describing "what happened"—not how state should change, just that a user clicked submit or an API resolved. They are the only source of information for the store; in the saga template they are also the **only** way the UI talks to the saga middleware (no thunks, no async functions inside `dispatch`).

## Key Principles

1. **Three phases per async op.** Every async CRUD verb gets exactly three constants and three creators: `<OP>_<ENTITY>` (REQUEST), `<OP>_<ENTITY>_SUCCESS`, `<OP>_<ENTITY>_ERROR`. The container dispatches the bare REQUEST; the saga `put`s the SUCCESS or ERROR.

2. **One phase for sync ops.** Stage-style ops (e.g. `EDIT_TODO`, which only sets `currentTodoItem`) emit the bare REQUEST and nothing else. The reducer handles it directly.

3. **UPPER_SNAKE_CASE type constants.** Every type is declared once in `<slice>.type.js` and imported by both the action creator and the reducer. Prevents typo-driven silent bugs.

4. **Plain serializable objects.** Action payloads are POJOs only — no functions, Promises, classes, or Date instances. This is what makes redux-saga's effects testable: the saga compares dispatched actions by deep equality.

5. **Hand-written creators, not RTK.** This template intentionally does NOT use `createSlice` / `createAsyncThunk`. The saga middleware listens for the REQUEST type directly, so abstracting creator boilerplate would only obscure the action surface.

6. **Per-op signature.** `create<E>(text)` takes the new content and seeds `{text, completed:false, id:undefined}`. `delete<E>(id)` takes the id, packs `{id}`. `toggle<E>` and `update<E>` take the full payload. `read<E>()` takes nothing meaningful (often called from `useEffect` on mount). Success/error creators all take `payload` or `error`.

## Best Practices

✅ **DO**:
- Co-locate types and creators in the slice folder (`<slice>.type.js`, `<slice>.actions.js`).
- Group creators in CRUD-canonical order: `create → read → edit → update → toggle → delete`.
- Make `<op>Error(error)` accept any throwable; convert with `error.toString()` at the saga boundary.
- For optimistic ops (toggle/delete), have `<op>Error(payload, error)` carry the rollback list as `payload`.

❌ **DON'T**:
- Don't put `dispatch` calls inside action creators — creators return objects, full stop.
- Don't add async behaviour to creators (no thunks). The saga middleware is the only async seam.
- Don't reuse one action type for multiple ops (`UPDATE_TODO` should not also mean "create a new todo").

## Code Patterns

### Type constants (`<slice>.type.js`)

```javascript
// Three phases per async op…
export const CREATE_TODO         = "CREATE_TODO"
export const CREATE_TODO_SUCCESS = "CREATE_TODO_SUCCESS"
export const CREATE_TODO_ERROR   = "CREATE_TODO_ERROR"
export const READ_TODO           = "READ_TODO"
export const READ_TODO_SUCCESS   = "READ_TODO_SUCCESS"
export const READ_TODO_ERROR     = "READ_TODO_ERROR"
export const UPDATE_TODO         = "UPDATE_TODO"
export const UPDATE_TODO_SUCCESS = "UPDATE_TODO_SUCCESS"
export const UPDATE_TODO_ERROR   = "UPDATE_TODO_ERROR"
export const TOGGLE_TODO         = "TOGGLE_TODO"
export const TOGGLE_TODO_SUCCESS = "TOGGLE_TODO_SUCCESS"
export const TOGGLE_TODO_ERROR   = "TOGGLE_TODO_ERROR"
export const DELETE_TODO         = "DELETE_TODO"
export const DELETE_TODO_SUCCESS = "DELETE_TODO_SUCCESS"
export const DELETE_TODO_ERROR   = "DELETE_TODO_ERROR"
// …one phase per sync op.
export const EDIT_TODO           = "EDIT_TODO"
```

### Action creators (`<slice>.actions.js`)

```javascript
import {
  CREATE_TODO, CREATE_TODO_SUCCESS, CREATE_TODO_ERROR,
  READ_TODO,   READ_TODO_SUCCESS,   READ_TODO_ERROR,
  EDIT_TODO,
  UPDATE_TODO, UPDATE_TODO_SUCCESS, UPDATE_TODO_ERROR,
  TOGGLE_TODO, TOGGLE_TODO_SUCCESS, TOGGLE_TODO_ERROR,
  DELETE_TODO, DELETE_TODO_SUCCESS, DELETE_TODO_ERROR,
} from "./todo.type";

// CREATE: container passes text; saga assigns id; reducer appends on SUCCESS.
export const createTodo        = (text)    => ({ type: CREATE_TODO,         payload: { text, completed: false } });
export const createTodoSuccess = (payload) => ({ type: CREATE_TODO_SUCCESS, payload });
export const createTodoError   = (error)   => ({ type: CREATE_TODO_ERROR,   error });

// READ: container fires on mount; saga fetches; reducer hydrates on SUCCESS.
export const readTodo          = (payload) => ({ type: READ_TODO,           payload });
export const readTodoSuccess   = (payload) => ({ type: READ_TODO_SUCCESS,   payload });
export const readTodoError     = (error)   => ({ type: READ_TODO_ERROR,     error });

// EDIT: sync; reducer just sets currentTodoItem.
export const editTodo          = (payload) => ({ type: EDIT_TODO,           payload });

// UPDATE: optimistic write through; saga PUTs and SUCCESS clears currentTodoItem.
export const updateTodo        = (payload) => ({ type: UPDATE_TODO,         payload });
export const updateTodoSuccess = (payload) => ({ type: UPDATE_TODO_SUCCESS, payload });
export const updateTodoError   = (error)   => ({ type: UPDATE_TODO_ERROR,   error });

// TOGGLE: optimistic flip; ERROR carries the previous list for rollback.
export const toggleTodo        = (payload) => ({ type: TOGGLE_TODO,         payload });
export const toggleTodoSuccess = ()        => ({ type: TOGGLE_TODO_SUCCESS });
export const toggleTodoError   = (payload, error) => ({ type: TOGGLE_TODO_ERROR, payload, error });

// DELETE: optimistic remove; same rollback shape as toggle.
export const deleteTodo        = (id)      => ({ type: DELETE_TODO,         payload: { id } });
export const deleteTodoSuccess = ()        => ({ type: DELETE_TODO_SUCCESS });
export const deleteTodoError   = (payload, error) => ({ type: DELETE_TODO_ERROR, payload, error });
```

### Dispatching from a container

```jsx
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { readTodo, toggleTodo, editTodo, deleteTodo } from "../state/todo/todo.actions";

function TodoListContainer() {
  const dispatch = useDispatch();

  // READ on mount — saga middleware sees REQUEST, runs getTodos worker.
  useEffect(() => { dispatch(readTodo()); }, [dispatch]);

  return /* …pass dispatch handlers down to organism… */;
}
```

### Per-op signature cheatsheet

| Op       | Request creator                  | Success creator        | Error creator                    |
|----------|----------------------------------|------------------------|----------------------------------|
| `create` | `createTodo(text)`               | `createTodoSuccess(p)` | `createTodoError(error)`         |
| `read`   | `readTodo(payload?)`             | `readTodoSuccess(p)`   | `readTodoError(error)`           |
| `edit`   | `editTodo(payload)` *(sync)*     | —                      | —                                |
| `update` | `updateTodo(payload)`            | `updateTodoSuccess(p)` | `updateTodoError(error)`         |
| `toggle` | `toggleTodo(payload)`            | `toggleTodoSuccess()`  | `toggleTodoError(prevList, err)` |
| `delete` | `deleteTodo(id)`                 | `deleteTodoSuccess()`  | `deleteTodoError(prevList, err)` |

## FSA-ish — but only `type` is mandatory

The template doesn't enforce strict FSA; success/error variants either carry `payload` or carry `error` (a string), and `meta` is unused. The contract that matters:

```javascript
{ type: <STRING_CONST>, payload?: any, error?: string }
```

## Related Terminologies

- **Saga** — listens for REQUEST types, dispatches SUCCESS/ERROR.
- **Reducer** — switches on all three phases per op.
- **Store** — dispatches actions through the saga middleware first, then to reducers.

## Quality Gates

- [ ] Three constants per async op; one per sync op.
- [ ] Creators are pure POJO factories (no `dispatch`, no closures over state).
- [ ] Toggle/delete success creators take **no args**; error creators carry `(prevList, error)`.
- [ ] Test imports use the same name as the constants (no aliasing).
- [ ] No `createAsyncThunk` / `createSlice` (those belong to a different archetype).

**Source**: `templates/chota-react-saga/src/state/todo/todo.type.js`, `todo.actions.js`
