---
name: core/testing
description: >-
  Use when testing Themis sagas or reducers with Vitest, typed-redux-saga
  mocks, expectSaga, or testSaga, including no-op reference equality and
  state/owner integrity.
type: sub-skill
library: themis
requires:
  - core
  - core/sagas
  - core/state-integrity
sources:
  - "@themislib/themis/docs/TESTING.md"
  - ../SKILL.md
triggers:
  - vi mock typed-redux-saga
  - expectSaga integration
  - testSaga stepwise
  - saga test plan
---
# Testing — reducer, selector, and saga checks

> Operational testing checklist. Human-facing examples: `@themislib/themis/docs/TESTING.md`. Saga effect details: `../sagas/SKILL.md`. Canonical checklist: [Layer rules](#layer-rules) and [Saga test setup cues](#saga-test-setup-cues).

## Use when

- Adding or updating tests for reducers, selectors, collections, async actions, or sagas.
- Reviewing state-integrity evidence for changed state/actions/selectors/sagas.
- Debugging redux-saga-test-plan matcher failures.

## Layer rules

| Layer | Test style | Required cues |
| --- | --- | --- |
| Reducers | Direct function calls | Initial state, each handled action, unknown/no-op same reference, serializable state when shape changes. |
| Collections | Reducer/selector tests | Assert via `getItem`, `getItems`, or selector helpers; include no-op reference checks. |
| Selectors | Pure `.select(mockState, ...)` calls | Use this path for pure output tests. Test adapter subscriptions/lifecycle separately with their Store context and scheduler. |
| Sagas | `runSaga`, manual stepping, or optional `expectSaga` / `testSaga` | Keep real typed effects; assert raw descriptors or provide controlled call results. |

## Saga test setup cues

- Prefer no effect-module mock: real typed effects delegate to raw descriptors, so `yield*` works with manual stepping, `runSaga`, and test-plan.
- If mocking is necessary, each typed effect must remain a generator wrapper, not a raw descriptor-returning function. Preserve context-method tuples in the `call` mock, including the `Array.isArray(fnOrDescriptor)` guard.
- In assertions and matchers, use `redux-saga/effects` descriptors or `redux-saga-test-plan` APIs, not descriptors imported from `typed-redux-saga`.
- If installed by the consumer, use `expectSaga` for behavior/integration and `testSaga` for order-sensitive generator steps such as root saga fork order. Do not assume optional test-plan is available or install it silently.

## State-integrity evidence

- Reducer tests assert canonical fields only; derived values are tested through selectors.
- Selector tests cover derived outputs instead of stored `filtered*`, `*Count`, `has*`, or selected entity copies.
- Handoff names the canonical owner for each new action, selector, or saga, or states that none was added.
- Search evidence lists terms/paths used to rule out duplicate action types, selectors, saga watchers, and registrations.

## Don't

- Do not call `selector(mockState)` in pure selector tests; use `.select(state)`. Adapter/lifecycle tests intentionally exercise the readable/signal/observable API with its required setup and cleanup.
- Do not replace a typed effect with a raw effect function: `yield*` requires an iterator. Do not pass `.effect()`'s generator object as a static provider key.
- Do not use real long timers in saga tests; prefer `.silentRun(0)` or a short bounded duration.
- Do not approve tests that assert reducer-maintained derived fields when selectors should own that value.
- Do not omit no-op reference checks for reducers or collection updates that should preserve identity.
- Do not leave one-line re-export/proxy wrapper files after refactors unless an adjacent compatibility comment documents the consumer, release window, and removal condition.

## Examples

### 1. Mock `typed-redux-saga` with a tuple-aware `call` guard

Usually omit this mock entirely. When isolation requires it, `vi.doMock` below is deliberately **not hoisted**: register it before dynamically importing the saga under test (and do not statically import that saga first). The async factory imports its own dependencies. Each wrapper returns the effect's resolved value to `yield*`.

```ts
import { vi } from "vitest";

vi.doMock("typed-redux-saga", async () => {
  const effects = await import("redux-saga/effects");
  return {
    call: function* (fnOrDescriptor: any, ...args: any[]): Generator<any, any, any> {
      return yield (Array.isArray(fnOrDescriptor)
        ? effects.call(fnOrDescriptor as [any, any], ...args)
        : effects.call(fnOrDescriptor, ...args));
    },
    put: function* (...args: Parameters<typeof effects.put>): Generator<any, any, any> { return yield effects.put(...args); },
    select: function* (...args: Parameters<typeof effects.select>): Generator<any, any, any> { return yield effects.select(...args); },
    takeLatest: function* (...args: Parameters<typeof effects.takeLatest>): Generator<any, any, any> { return yield effects.takeLatest(...args); },
  };
});
// Next: const { loadTodosWorker } = await import("./todos-saga");
// Restore with vi.doUnmock("typed-redux-saga") after the isolated test.
```

### 2. Test reducer branches and no-op identity

```ts
import { describe, expect, it } from "vitest";
import { createAction, createAsyncAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type TodosState = { items: string[]; filter: "all" | "open"; loading: boolean; error: string };
const setFilter = createAction<[filter: TodosState["filter"]]>("todos/setFilter");
const loadTodos = createAsyncAction<[query: string], { query: string }, string[]>("todos/loadAsync", "todos/load", (query) => ({ query }));
const initialState: TodosState = { items: [], filter: "all", loading: false, error: "" };
const todosReducer = createReducer(initialState)
  .with(setFilter, (state, { payload: [filter] }) => (state.filter === filter ? state : { ...state, filter }))
  .with(loadTodos, (state) => ({ ...state, loading: true, error: "" }))
  .with(loadTodos.failure, (state, { payload }) => ({ ...state, loading: false, error: payload.error.message }));

describe("todosReducer", () => {
  it("keeps no-op identity and covers async failure", () => {
    const current: TodosState = { ...initialState, filter: "open" };
    expect(todosReducer(current, setFilter("open"))).toBe(current);
    expect(todosReducer({ ...current, loading: true }, loadTodos.failure(new Error("Network"))).error).toBe("Network");
  });
});
```

### 3. Test selector output through `.select(state)`

```ts
import { describe, expect, it } from "vitest";
import { selectTodoCount, selectVisibleTodos } from "./todos-selectors";

const state = {
  todos: {
    items: [{ id: "a", title: "Write tests", completed: false }, { id: "b", title: "Review", completed: true }],
    filter: "open",
  },
};

describe("todo selectors", () => {
  it("derives visible todos from canonical reducer state", () => {
    expect(selectVisibleTodos.select(state).map((todo) => todo.id)).toEqual(["a"]);
    expect(selectTodoCount.select(state)).toBe(2);
  });
});
```

### 4. Use `expectSaga` with provided selector effects

```ts
import { describe, expect, it } from "vitest";
import { expectSaga } from "redux-saga-test-plan";
import * as matchers from "redux-saga-test-plan/matchers";
import { select } from "redux-saga/effects";
import { fetchTodos } from "./todos-api";
import { loadTodos } from "./todos-slice";
import { loadTodosWorker } from "./todos-saga";
import { selectCurrentUserId } from "./todos-selectors";

describe("loadTodosWorker", () => {
  it("loads todos for the selected user", async () => {
    const todos = [{ id: "t1", title: "Ship examples", completed: false }];
    const request = loadTodos("open");
    await expectSaga(loadTodosWorker, request)
      .provide([[select(selectCurrentUserId.select), "u1"], [matchers.call.fn(fetchTodos), todos]])
      .put({ type: loadTodos.success.type, payload: { request: request.payload, response: todos, seq: request.seq } })
      .silentRun();
    await expect(request.promise).resolves.toEqual(todos);
  });
});
```

The provider matches the raw SELECT yielded by `.effect()`: `.select` is the same underlying selector function. Include the same selector args in `select(selectFoo.select, ...args)` when applicable. This worker must `yield* put(action.success(todos))` to settle its **instance** request. Construct the expected action as data: calling `request.success(todos)` in test setup would settle the promise before exercising the worker and could hide a bug.

### 5. Use `testSaga` for root watcher order

```ts
import { describe, it } from "vitest";
import { testSaga } from "redux-saga-test-plan";
import { loadTodos, loadTodosWorker, todosRootSaga } from "./todos-saga";

describe("todosRootSaga", () => {
  it("registers the canonical latest-only watcher", () => {
    testSaga(todosRootSaga)
      .next()
      .takeLatest(loadTodos, loadTodosWorker)
      .next()
      .isDone();
  });
});
```

## Verification cues

- Run the smallest relevant test scope first, then broader validation if needed.
- Run architecture validation for state/actions/selectors/sagas changes when in scope: `npm run validate:architecture` in this repository, or run ESLint with the app's composed domain root config imported from `@themislib/themis/eslint-plugins` in a consuming app.
- Review docs/skills examples after changing them and run the smallest relevant test scope first.
- Manual review should confirm detailed background stays in `@themislib/themis/docs/TESTING.md` while this skill keeps only concise, gate-focused examples.

## See also

- `@themislib/themis/docs/TESTING.md` — human reference with reducer, selector, saga, and integration examples.
- `core/reducers/SKILL.md` — reducer purity and reference equality.
- Selected Store family selector skill — `.select(state)` selector testing.
- `core/sagas/SKILL.md` — saga effect and watcher conventions.
- `core/state-integrity/SKILL.md` — canonical ownership evidence.