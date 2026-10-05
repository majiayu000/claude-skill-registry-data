---
name: react/component-integration
description: >-
  Wire ReactStore at the React app root: init/dispose ownership, runSaga startup,
  and Store-first dispatch. Route selector consumption to selector-lifecycle.
type: sub-skill
requires:
  - react
  - react/store
  - react/selector-lifecycle
  - core/core-policy
sources:
  - "@themislib/themis/react-store"
  - ../signals/SKILL.md
  - ../selector-lifecycle/SKILL.md
  - ../store/SKILL.md
triggers:
  - React component integration
  - ReactStore component wiring
  - bootstrap ReactStore
  - React reducer registry
  - TSX Store dispatch
  - React signal component
  - selector .useValue component
---
# React component integration — ReactStore app wiring

Use this skill when a React/TSX app has chosen the `ReactStore` family. Create
one configured `ReactStore`, initialize it before React renders selector-using
components, start app sagas after initialization, and dispatch through that same
configured store instance from components and handlers.

This is React Store family guidance for JSX/TSX components, custom hooks, and
the app bootstrap boundary. First-time installation and family selection start
at `../../setup/SKILL.md`; migration sequencing starts at
[Adoption checkpoint](../migration/setup/SKILL.md#adoption-checkpoint).

## Create and configure ReactStore

Create the store in an app-owned module, not inside a component render or custom
hook. Pass app-owned reducers in the constructor map, optional middleware as the
second argument, and options such as `throttledSelectorFrequency` as the third
argument when needed.

```ts
// src/store/react-store.ts
import { ReactStore } from "@themislib/themis/react-store";
import type { StoreState } from "@themislib/themis/types";
import { todosReducer } from "./todos/todos-slice";

export const reactStore = new ReactStore({ todos: todosReducer });
export type AppState = StoreState<typeof reactStore>;
```

Key rules:

- Use `ReactStore` only from `@themislib/themis/react-store` for this React app
  path.
- Use `reactStore.createSelector(...)` for app-local selectors so state inference follows the configured store.
- Do not add package-owned `@internal_` reducers or internal sagas.
- Do not create a new `ReactStore` per component, route, hook call, or render.

## Initialize before React renders selector users

Call `reactStore.init(initialState?)` once at the app bootstrap/root ownership
boundary before rendering components that call direct signal selectors or
`.useValue(...args)` fallbacks. The returned disposer is equivalent to
`reactStore.dispose()`.

Pass preloaded state to `reactStore.init(preloadedState)` when the app needs
hydration. Initialize before selector reads because direct selector calls need the
active Store-owned state stream and throw before `init()` and after `dispose()`.

## Dispose at the same owner boundary

The owner that calls `reactStore.init()` owns teardown: usually the browser
bootstrap or test harness, or an embedded/micro-frontend mount adapter.

```tsx
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { reactStore } from "./store/react-store";
import { todosSaga } from "./store/todos/sagas/todos-saga";

export function mountReactApp(container: HTMLElement) {
  const root = createRoot(container);
  const disposeStore = reactStore.init();
  const cancelTodosSaga = reactStore.runSaga(todosSaga);

  root.render(<App />);

  return () => {
    root.unmount();
    cancelTodosSaga();
    disposeStore();
  };
}
```

The browser bootstrap can call this adapter and register its returned cleanup
with `import.meta.hot.dispose(...)` for HMR. Unmount React and cancel the app saga
before disposing the store.

Do not hide `init()` in a child component `useEffect` if descendants render
selectors immediately; effects run after render, too late for direct signal
selectors or `.useValue(...args)` fallbacks that need the initialized store.

## Start app sagas explicitly

`reactStore.init()` starts package-owned runtime work but does not auto-start app
sagas. The `mountReactApp` example above starts its app-wide saga inside the
owner function, immediately after `init()`, and retains its cancel function in
the same cleanup closure. Importing the module does not start the runtime or
the saga. Do not move `runSaga` to module scope when initialization happens only
at mount time.

Choose the saga's lifetime using core
[Application saga startup](../../core/sagas/SKILL.md#application-saga-startup).
App-wide sagas use the root owner above; component/layout-scoped sagas use that
component/layout's lifecycle and matching cancellation, as shown in
[React side-effect migration](../migration/side-effects/SKILL.md#start-the-saga-from-reactstore-setup).

`reactStore.runSaga(sagaFn)` throws if `init()` has not been called or the saga name is reserved for package internals. Do not start `@internal_sagaManager` directly.

## Component reads and dispatch

Once the app runtime is initialized, prefer signal-aware component reads and
dispatch through the same configured store. Choose the read API using
[Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map) and apply
[React signal consumption guardrails](../selector-lifecycle/SKILL.md#react-signal-consumption-guardrails).
The `.value` reads below require the tracking described in that owner.

```tsx
import { reactStore } from "../store/react-store";
import { selectTodoById } from "../store/todos/todos-selectors";
import { toggleTodo } from "../store/todos/todos-slice";

export function TodoRow({ id }: { id: string }) {
  const todo = selectTodoById(id);

  if (!todo.value) return null;

  return (
    <button onClick={() => reactStore.dispatch(toggleTodo(id))}>
      {todo.value.completed ? "✓" : "○"} {todo.value.title}
    </button>
  );
}
```

Import or receive the configured `ReactStore` instance; event handlers dispatch
with `reactStore.dispatch(action)`. When a handler also needs a snapshot, follow
[Handler and test one-shot reads](../selector-lifecycle/SKILL.md#handler-and-test-one-shot-reads)
rather than creating a render subscription.

For React business effects versus DOM-local hooks, apply
[Setup — core rules](../../core/core-policy/SKILL.md#setup--core-rules).
Use [React side-effect migration](../migration/side-effects/SKILL.md) when moving
an existing effect; saga startup and cancellation stay at its selected lifetime
owner, while Store initialization/disposal stay at the app owner described above.

## Common mistakes

### Initializing in an effect after children render

`useEffect(() => reactStore.init(), [])` is too late if children read selectors
during render. Initialize at bootstrap, or withhold selector-using children
until explicit initialization completes.

### Creating stores in components or hooks

`new ReactStore(...)` in a component/hook can create a runtime every render or
mount. Create/configure it once in an app module or explicit mount adapter.

### Treating direct selector signals as plain values

Wiring the runtime does not turn selector signals into plain values. Apply
[Pitfalls](../selector-lifecycle/SKILL.md#pitfalls) for wrong-shape reads,
tracking requirements, and necessary plain-value fallback boundaries.

## See also

- `../store/SKILL.md` — `ReactStore` import, lifecycle, and Store runtime behavior.
- `../signals/SKILL.md` — Preact Signals `.value`, tracking, direct JSX signal
  rendering, and component-local signal hooks.
- `../selector-lifecycle/SKILL.md` — selector call modes across components, handlers, tests, composition, explicit binding, and sagas.
- `../selectors/SKILL.md` — selector authoring for Preact React signals.
- `../../setup/SKILL.md` — first-time Store-family selection and setup.