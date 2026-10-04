---
name: state-saga
description: Redux-Saga (generator-based) middleware for async side effects — yields declarative effects (call/put/select/takeLatest/delay) instead of imperative async code, watcher-per-slice composition, optimistic updates with rollback. Use when authoring per-slice operations.js, the rootSagas composer, or reviewing saga workers.
when_to_use: Authoring or reviewing per-slice operations.js (saga workers + watcher), rootSagas composer, helper.js (optimistic-update transforms used by both reducer and saga), or asserting that REQUEST actions get caught by takeLatest and SUCCESS/ERROR get put as plain objects.
paths:
  - "**/state/**/*.operations.{js,ts}"
  - "**/state/**/*.helper.{js,ts}"
  - "**/state/rootSagas.{js,ts}"
  - "**/sagas/**/*.{js,ts}"
---

# State Saga

## What is a Saga?

A saga is a generator function that observes dispatched actions and orchestrates async side effects (HTTP requests, optimistic UI, retries, debounced flows) by yielding **declarative effects** to the saga middleware. The middleware runs the effects; the saga itself stays pure and synchronous-looking, which makes it trivial to read, test, and step through.

In the elegant universal-architecture, every async slice owns one `*.operations.js` file: an API caller per CRUD verb, a worker generator per verb, and a single `watch<Entity>s()` watcher generator that `takeLatest`s the REQUEST type to its worker. The watchers fan in to a single `rootSagas.js` composer that the store runs once at boot.

## Key Principles

1. **Declarative effects over imperative code.** A saga `yield put(action)` instead of `dispatch(action)`; `yield call(fn, args)` instead of `await fn(args)`. The middleware runs them, so the saga itself is pure data.

2. **Watcher per slice, worker per op.** Each slice exports exactly one `watch<Entity>s()` generator. The watcher does nothing but `takeLatest(<REQUEST_TYPE>, <worker>)` for each async op. Workers are the named functions that actually call the API and `put` SUCCESS/ERROR.

3. **REQUEST is a plain action, not a function.** Containers `dispatch(read<Entity>())`. The saga middleware lets the action pass through to the reducer (which sets `isContentLoading: true`) AND fires the worker. No thunks, no `createAsyncThunk`.

4. **Errors are actions.** A worker's `try/catch` always ends in `yield put(<op><Entity>Error(...))`; never throws past the middleware. The reducer responds to ERROR like any other action.

5. **Optimistic mutations roll back from `previousState<Items>`.** For toggle/delete the reducer stores the pre-mutation list under `previousState<Items>` on the REQUEST. The worker's `catch` reads it via `yield select(...)` and dispatches ERROR with that list as payload, so the reducer can restore.

6. **`call` returns a Promise; `yield <promise>` resolves it.** The classic two-line pattern: `const res = yield call(api); const json = yield res.json();` — no `await` required.

## Best Practices

✅ **DO**:
- Wire one `watch<Entity>s()` per slice; let the watcher own all `takeLatest` for that slice's REQUEST types.
- Put helper transforms (`mapTodoData`, `toggleCheckedState`) in `<slice>.helper.js` so both the saga AND the reducer can import them.
- For optimistic ops (toggle/delete), `yield delay(500)` before reading `previousState<Items>` to surface the failed-out animation.
- Let the worker dispatch SUCCESS/ERROR; the reducer is the only place state shape changes.

❌ **DON'T**:
- Don't `dispatch` directly from a worker — `yield put` instead, so the middleware can intercept (for logs, devtools, tests).
- Don't fetch inside reducers, components, or selectors. The saga is the seam.
- Don't `takeEvery` for user-driven CRUD — `takeLatest` cancels in-flight workers, which is what users expect (rapid clicks).
- Don't put RTK's `createAsyncThunk` next to sagas; pick one async strategy per app.

## Code Patterns

### Per-slice operations.js

```javascript
import { put, takeLatest, call, select, delay } from "redux-saga/effects";
import { CREATE_TODO, READ_TODO, UPDATE_TODO, TOGGLE_TODO, DELETE_TODO } from "./todo.type";
import {
  createTodoSuccess, createTodoError,
  readTodoSuccess, readTodoError,
  updateTodoSuccess, updateTodoError,
  toggleTodoSuccess, toggleTodoError,
  deleteTodoSuccess, deleteTodoError,
} from "./todo.actions";
import { mapTodoData, toggleCheckedState } from "./todo.helper";
import fetchApi from "../../utils/api";

// API callers — one per CRUD verb. Toggle reuses update's PUT.
export function getTodoApi()             { return fetchApi('/todos'); }
export function addTodoApi(payload)      { return fetchApi('/todos', { method: 'POST',   body: payload }); }
export function updateTodoApi(payload)   { return fetchApi('/todos', { method: 'PUT',    body: payload }); }
export function deleteTodoApi(payload)   { return fetchApi('/todos', { method: 'DELETE', body: payload }); }

// READ worker — straight call → success/error.
export function* getTodos() {
  try {
    const res = yield call(getTodoApi);
    const data = yield res.json();
    yield put(readTodoSuccess(mapTodoData(data)));
  } catch (error) {
    yield put(readTodoError(error.toString()));
  }
}

// CREATE worker — server assigns id (or window.crypto in the demo wrapper).
export function* addTodos(action) {
  try {
    const payload = { ...action.payload, id: window.crypto.randomUUID() };
    yield call(addTodoApi, payload);
    yield put(createTodoSuccess(payload));
  } catch (error) {
    yield put(createTodoError(error.toString()));
  }
}

// TOGGLE worker — optimistic; rollback from previousStateTodoItems on error.
export function* updateToggleTodos(action) {
  try {
    yield call(updateTodoApi, toggleCheckedState(action.payload));
    yield put(toggleTodoSuccess());
  } catch (error) {
    yield delay(500);
    const prev = yield select((state) => state.todo.previousStateTodoItems);
    yield put(toggleTodoError(prev, error.toString()));
  }
}

// Watcher: ONE per slice; takeLatest each REQUEST → its worker.
export function* watchTodos() {
  yield takeLatest(CREATE_TODO, addTodos);
  yield takeLatest(READ_TODO,   getTodos);
  yield takeLatest(UPDATE_TODO, updateTodos);
  yield takeLatest(TOGGLE_TODO, updateToggleTodos);
  yield takeLatest(DELETE_TODO, deleteTodos);
}
```

### rootSagas.js — fan-in composer

```javascript
import { all } from "redux-saga/effects";
import { watchTodos } from "./todo/todo.operations";

export default function* rootSaga() {
  yield all([
    watchTodos(),
    // watchOtherSlice(),  // add per slice as the app grows
  ]);
}
```

### helper.js — pure transforms shared by reducer and saga

```javascript
// Maps API response → reducer-shape. Trivial here; non-trivial in real APIs.
export const mapTodoData = (todoData) => todoData;

// Used by BOTH the reducer (for the optimistic flip) and the saga
// (when the API call succeeds, the saga doesn't need this — but
// passes the toggled item to the API so the server flips too).
export const toggleCheckedState = (payload) => ({
  ...payload,
  completed: !payload.completed,
});
```

### Wiring at the store

```javascript
import createSagaMiddleware from "redux-saga";
import rootSaga from "./rootSagas";
const sagaMiddleware = createSagaMiddleware();
const store = createStore(reducer, applyMiddleware(sagaMiddleware));
sagaMiddleware.run(rootSaga);   // ← run once at boot
```

## Related Terminologies

- **Actions** — defines the REQUEST/SUCCESS/ERROR types the saga listens for and dispatches.
- **Reducer** — switches on REQUEST/SUCCESS/ERROR; reads `previousState<Items>` on rollback.
- **Middleware** — sagas ARE middleware (composed via `createSagaMiddleware()` + `applyMiddleware`).
- **API** — the saga's `call()` target; lives in `src/utils/api.js`.

## Quality Gates

- [ ] One `watch<Entity>s()` watcher per slice; everything else is private.
- [ ] Workers always `yield put(<op>Success/<op>Error)`; nothing escapes the try/catch.
- [ ] Optimistic ops read `previousState<Items>` via `yield select(...)` on error.
- [ ] No `await`, no `dispatch` inside generators — only `yield call/put/select/delay/takeLatest`.
- [ ] No thunks coexist; this app uses sagas exclusively for async.

**Source**: `templates/chota-react-saga/src/state/todo/todo.operations.js`, `rootSagas.js`
