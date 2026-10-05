---
name: core/actions
description: >-
  Use when creating Themis actions with createAction or createAsyncAction,
  including tuple payloads, async request promises, and action ownership.
type: sub-skill
requires:
  - core
  - core/state-integrity
triggers:
  - create action
  - tuple payload
  - async action
  - action creator
---
# Actions — `createAction` / `createAsyncAction`

> Operational guidance for action creator work. API details and longer examples live in `@themislib/themis/docs/REDUCERS.md` → Actions and Async Actions. Public API: `@themislib/themis/utils/store/create-action`; related reducer guidance: [Do](../reducers/SKILL.md#do).

## Use when

- Adding or reusing slice action creators.
- Wiring async request/success/failure flows to reducers or sagas.
- Checking action type ownership during state-integrity work.

## Do

- Search first for the intended action type, creator names, and operation terms; one action type string has one canonical owner.
- Namespace action types as `sliceName/actionName`.
- Use tuple payload typing for positional args, e.g. `createAction<[id: string]>(...)`.
- Use a payload modifier only when callers should pass positional args but reducers/sagas need a shaped payload.
- Pass action creators directly to `takeEvery`/`takeLatest`; their `toString()` exposes the action type.

## Async action cues

- `createAsyncAction<[Args], Success>(asyncType, stagesType)` creates the request creator plus static `.success` and `.failure` creators.
- A dispatched request action carries `payload`, `promise`, and per-instance `success`/`failure` creators.
- Themis internally observes ignored async-action rejections, preventing unhandled-rejection events without changing the original promise; explicit awaiters still receive the original rejection.
- Prefer `try/catch` around `await store.dispatch(asyncAction(...))` when handling a result or failure; dispatch returns the request's original, typed promise.
- Reducers normally handle the request creator, `.success`, and `.failure` to update loading/data/error fields.
- Sagas watch the request creator unless they are intentionally reacting to success/failure events.
- Only the request instance's `action.success(result)` / `action.failure(error)` settles its promise; static stages merely create Redux actions. Dispatch the instance stage as well when reducers need the update.
- Settlement is an application policy, not automatic: `takeLatest` cancellation enters `finally`, not `catch`. Reject cancelled requests explicitly as below. With `takeLeading`, an ignored request never reaches a worker: use ordinary `createAction` triggers when no response is guaranteed, or an explicit admission owner that rejects ignored requests. Do not await a promise-bearing request when its watcher is absent/stopped.

## Examples

### No-payload action for explicit events

```ts
import { createAction, createAsyncAction } from "@themislib/themis/utils/store/create-action";

export const resetTodos = createAction("todos/reset");

const resetAction = resetTodos();
// Current runtime payload is [], although the no-argument overload says undefined.
// Handle the event by its type; do not branch on payload === undefined.
const refreshTodos = createAsyncAction<void>("todos/refreshAsync", "todos/refresh");
const refreshAction = refreshTodos(); // same [] runtime / undefined type discrepancy
const resetTuple = createAction<[]>("todos/resetTuple")(); // typed and runtime []
const resetUndefined = createAction("todos/resetUndefined", () => undefined)();
```

The async example explicitly selects the response-type overload (`<void>`), which declares `undefined` payload; with no type arguments the current overload order can instead infer `any[]`. Both produce runtime `[]` without a modifier. If shape matters, choose an explicit contract: `createAction<[]>("todos/reset")` gives a typed empty tuple; `createAction("todos/reset", () => undefined)` intentionally produces runtime `undefined`. These are existing API limitations, not a reason to change the public API during a guidance fix.

### Tuple payload action consumed by reducers

```ts
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

const renameTodo = createAction<[id: string, title: string]>("todos/rename");
const reducer = createReducer({ titles: {} as Record<string, string> }).with(
  renameTodo,
  (state, { payload: [id, title] }) => ({ ...state, titles: { ...state.titles, [id]: title } })
);
```

### Payload modifier when reducers need a named object

```ts
import { createAction } from "@themislib/themis/utils/store/create-action";

export const renameTodo = createAction(
  "todos/rename",
  (id: string, title: string, requestedAtMs: number) => ({ id, title, requestedAtMs })
);

const action = renameTodo("todo-1", "Ship docs", Date.now());
action.payload.id satisfies string;
```

### Async request/success/failure triplet

```ts
import { createAsyncAction } from "@themislib/themis/utils/store/create-action";

type Todo = { id: string; title: string };
export const loadTodo = createAsyncAction<[id: string], { id: string }, Todo>(
  "todos/loadAsync",
  "todos/load",
  (id) => ({ id })
);

const request = loadTodo("todo-1");
const success = request.success({ id: "todo-1", title: "Ship docs" });
success.payload.request.id satisfies string;
```

### Await dispatch when the caller needs the result

Using `loadTodo` above and an initialized Themis `store` whose saga settles the request:

```ts
try {
  const todo = await store.dispatch(loadTodo("todo-1"));
  todo satisfies Todo;
} catch (error) {
  console.error("Unable to load todo", error);
}
```

### Watch request creators directly in sagas

```ts
import { call, cancelled, put, takeLatest } from "typed-redux-saga";
import { createAsyncAction } from "@themislib/themis/utils/store/create-action";
import { fetchTodo } from "./todos-api";

type Todo = { id: string; title: string };
const loadTodo = createAsyncAction<[id: string], { id: string }, Todo>(
  "todos/loadAsync",
  "todos/load",
  (id) => ({ id })
);

function* watchTodos() {
  yield* takeLatest(loadTodo, function* loadTodoWorker(action) {
    try {
      const todo = yield* call(fetchTodo, action.payload.id);
      yield* put(action.success(todo));
    } catch (error) {
      yield* put(action.failure(error instanceof Error ? error : new Error(String(error))));
    } finally {
      if (yield* cancelled()) {
        yield* put(action.failure(new Error("Todo request cancelled")));
      }
    }
  });
}
```

Policy here: supersession and owner teardown reject the cancelled request and emit its failure stage. Keep reducer updates correlated with `payload.request` if older cancellation/failure actions could overwrite newer results. Saga cancellation does not abort an arbitrary Promise/API operation; supply a source-specific abort policy when needed.

### ❌ Bad: duplicate owner plus tuple/object payload drift

```ts
import { createAction } from "@themislib/themis/utils/store/create-action";

type RenameTodoPayload = { id: string; title: string };

// BAD: two modules now claim the same action type, and callers get a tuple-wrapped object.
export const renameTodoFromList = createAction<[payload: RenameTodoPayload]>("todos/rename");
export const renameTodoFromDetail = createAction<[payload: RenameTodoPayload]>("todos/rename");

const [{ id, title }] = renameTodoFromList({ id: "todo-1", title: "Ship docs" }).payload;
```

## Don't

- Do not create aliases with the same type string in another module.
- Do not pass `.type` to saga watchers; pass the creator.
- Do not assume cancellation, ignored requests, or static success/failure stages settle an instance promise.
- Do not use object payload types for one-argument actions unless an existing public contract already requires that shape.
- Do not place generated timestamps or IDs in reducers; generate them before dispatch.
- Do not attach `action.promise.catch(...)` to Themis async actions, including defensive `action.promise.catch(() => undefined)`: it is redundant and reported by `redundant-async-action-catch` when the promise is statically proven to come from a Themis async action. Use the dispatch-await pattern above for caller-owned error handling.

## Verification cues

- Reducer tests cover each action handler and no-op reference equality.
- Saga tests prove request watchers receive the request creator, not an accidental success/failure creator.
- State-integrity handoff names the canonical owner or states that no new action owner was added.

## See also

- `@themislib/themis/docs/REDUCERS.md` — human reference for action and async-action examples.
- `core/reducers/SKILL.md` — consuming actions in `.with()` handlers.
- `core/sagas/SKILL.md` — watcher patterns and typed-redux-saga usage.
- `core/state-integrity/SKILL.md` — duplicate-owner search protocol.
- `core/file-structure/SKILL.md` — where action creators belong.