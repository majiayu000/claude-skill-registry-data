---
name: state-store
description: Redux store wiring for the chota-react-saga template — single createStore, combineReducers per domain, applyMiddleware(sagaMiddleware), composeWithDevTools, and a one-line `sagaMiddleware.run(rootSaga)` at boot. Use when scaffolding the root store or auditing how slices and middleware compose.
when_to_use: Authoring or reviewing `src/state/index.js` (the store), `src/state/rootReducer.js`, or wiring up new middleware; verifying that the saga middleware is created BEFORE `createStore` and `.run(rootSaga)` is called AFTER.
paths:
  - "**/state/index.{js,ts}"
  - "**/state/rootReducer.{js,ts}"
  - "**/state/store.{js,ts}"
---

# Store (Saga template)

## What is the Store?

The store is the single source of truth for application state. It holds the combined reducer, the middleware chain, and the dispatcher. In the saga template the store is also the seam where the saga middleware gets `.run(rootSaga)` so every slice's watcher starts listening at boot.

## Key Principles

1. **One store, period.** No nested stores, no per-feature stores. Every slice lives under `combineReducers({...})` and is reached through `useSelector((state) => state.<slice>.…)`.

2. **`createStore` from `redux` (not `configureStore`).** This template stays on plain redux + redux-saga + the devtools extension. RTK's `configureStore` would compose middleware differently and conflict with `composeWithDevTools(applyMiddleware(...))`.

3. **Saga middleware is created first, run last.** Order matters: `const sagaMiddleware = createSagaMiddleware()` → wrap with `applyMiddleware(sagaMiddleware)` → enhance with `composeWithDevTools(...enhancers)` → `createStore(reducer, composedEnhancers)` → finally `sagaMiddleware.run(rootSaga)`. Calling `.run()` before `createStore` is a runtime error.

4. **Store is provided once, at the App root.** `<Provider store={store}>` wraps the React tree in `App.jsx`. Containers reach state through `useSelector` and dispatch with `useDispatch`. Nothing else imports `store` directly.

5. **DevTools opt-in.** `composeWithDevTools` is a no-op when the extension isn't installed, so it's safe to ship in production builds without conditional code.

## Best Practices

✅ **DO**:
- Keep `rootReducer.js` to a single `combineReducers({ ... })` call. Add `/* istanbul ignore file */` so coverage doesn't penalise the wiring file.
- Keep `index.js` (the store) under ~25 lines. It does four things: import, create middleware, compose, run.
- Add slices to `combineReducers` in alphabetical order; add watchers to `rootSagas` `all([...])` in the same order. Easier diffing as the app grows.

❌ **DON'T**:
- Don't `applyMiddleware(thunk, sagaMiddleware)` — pick one async strategy. The saga template chose sagas.
- Don't lazy-load slices into the store. Reducer composition must be static at boot so the saga's `select(state => state.x)` is safe.
- Don't run sagas in tests by reaching into the production store. Use `runSaga` from `redux-saga` to drive workers in isolation.

## Code Patterns

### `src/state/index.js`

```javascript
import { composeWithDevTools } from '@redux-devtools/extension'
import { createStore, applyMiddleware } from 'redux'
import createSagaMiddleware from "redux-saga";

import reducer from "./rootReducer";
import sagas from "./rootSagas";

// 1. create the saga middleware
const sagaMiddleware = createSagaMiddleware();

// 2. mount it on the Store
const enhancer = applyMiddleware(sagaMiddleware)
const enhancers = [enhancer];
const composedEnhancers = composeWithDevTools(...enhancers)

const store = createStore(reducer, composedEnhancers);

// 3. then run the saga (after createStore!)
sagaMiddleware.run(sagas);

export default store;
```

### `src/state/rootReducer.js`

```javascript
/* istanbul ignore file */
import { combineReducers } from "redux";
import todo from "./todo/todo.reducer";
import filters from "./filters/filters.reducer";
import config from "./config/config.reducer";

export default combineReducers({
  todo,
  filters,
  config,
});
```

### Provider wiring at the app root (`src/App.jsx`)

```jsx
import { Provider } from "react-redux";
import store from "./state";
import HomePage from "./pages";

export default function App() {
  return (
    <Provider store={store}>
      <HomePage />
    </Provider>
  );
}
```

### Reading and dispatching from a container

```jsx
import { useSelector, useDispatch } from "react-redux";
import { readTodo } from "../state/todo/todo.actions";

const todos = useSelector((state) => state.todo.todoItems);
const dispatch = useDispatch();
dispatch(readTodo());   // saga middleware sees this, runs the worker
```

## Related Terminologies

- **Reducer** — slices are wired through `combineReducers` here.
- **Saga** — `rootSagas.js` is run by this file.
- **Middleware** — sagas ARE middleware; this file is where they get applied.
- **DevTools** — `composeWithDevTools` is the wiring point.

## Quality Gates

- [ ] `createStore` is called once; the result is the default export.
- [ ] `sagaMiddleware.run(sagas)` is called AFTER `createStore`.
- [ ] `combineReducers` is the only thing rootReducer.js does.
- [ ] No `configureStore`, no thunk middleware, no async logic in `index.js`.
- [ ] Provider wraps the whole tree; no nested `<Provider>`.

**Source**: `templates/chota-react-saga/src/state/index.js`, `rootReducer.js`
