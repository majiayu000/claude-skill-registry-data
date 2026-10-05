---
name: react/selector-lifecycle
description: >-
  Choose ReactStore selector call modes: preferred signals, necessary .useValue
  fallbacks, Babel/useSignals tracking, .select for handlers/tests/composition,
  .effect for sagas, and .withStore binding.
type: sub-skill
requires:
  - react
  - react/selectors
sources:
  - "@themislib/themis/react-store"
  - ../signals/SKILL.md
  - ../selectors/SKILL.md
triggers:
  - React selector lifecycle
  - selector .useValue
  - selector .withStore
  - selector .select
  - selector .effect
  - selector .useValue lifecycle
  - direct signal read
  - useSignals selector
  - select in React handler
---
# React selector lifecycle — call-mode guardrails

Use this skill when choosing how a `ReactStore` selector should be called from
React components, custom hooks, event handlers, tests, sagas, or other selectors.
The direct call form returns a Preact React signal and is the preferred React
consumer integration path when callers can pass, read, or render signals. Use
`.useValue(...args)` only when a hook/plain value is necessary and adapting the
consumer to accept signals is impractical.

Use this lifecycle for apps that chose the React Store family. This is the
canonical owner of the React selector call-mode matrix and consumer boundaries;
selector definitions and argument evaluation belong to
[Selector argument API](../selectors/SKILL.md#selector-argument-api).

## Call-mode map

| Context | Correct React call | Result | Why |
| --- | --- | --- | --- |
| Preferred React/signal-aware consumer | const valueSignal = selectFoo(...argsOrSignals) | Preact React ReadonlySignal<R> | Creates a signal-backed selector result for components, helpers, or hooks that can accept/read signals. |
| Hook/plain-value fallback | const value = selectFoo.useValue(...argsOrSignals) | Plain value R | Use only for third-party APIs, legacy component boundaries, or custom-hook contracts that require plain values. |
| Event handler/callback/test | selectFoo.select(state, ...args) | Plain value R | Performs a synchronous one-shot read without React hook/runtime requirements. |
| Selector composition | otherSelector.select(state, ...args) | Plain value R | Keeps selector callbacks pure and synchronous with state already in scope. |
| Saga | yield* selectFoo.effect(...args) | typed-redux-saga select effect | Reads via redux-saga state selection, not React signals or hooks. |
| Explicit binding | selectFoo.withStore(reactStore)(...args) | Preact React ReadonlySignal<R> | Binds to an explicit ReactStore instead of the selector's original store. |

## Do

- Prefer direct selector calls for `ReadonlySignal<R>` values in signal-aware
  components, hooks, and helpers; pass signals or read `.value` in tracked components.
- Track component `.value` reads with the Preact Signals Babel transform or an
  explicit `useSignals()` fallback in the reading component. Configuration and
  transform limitations belong to
  [React tracking requirement](../signals/SKILL.md#react-tracking-requirement).
- Use `.useValue(...args)` only when a component/custom-hook contract needs a plain
  value and adapting the consumer to signals is impractical.
- Use `.select(reactStore.state, ...args)` for handler/test snapshots and
  `.select(state, ...args)` for pure selector composition.
- Use `.effect(...args)` in sagas; use selector-channel helpers for reactive saga work.
- Bind with `.withStore(...)` only when an explicit alternate `ReactStore` is intended.

## React signal consumption guardrails

Apply the [Do](#do) / [Don't](#dont) call-mode rules alongside these signal details.

- Direct JSX signal rendering is valid when the JSX text position intentionally
  accepts a signal. For props, conditions, arrays, and objects, read `.value` or
  use a plain-value fallback boundary.
- `.select(state, ...args)` and `.effect(...args)` take plain selector arguments,
  not signal wrappers.
- Selector-channel helpers use the Redux store's `getState()` / `subscribe()`
  from saga context with plain stable argument tuples; they do not subscribe to
  direct `ReadonlySignal` selector outputs.

## Don't

- Do not call `.useValue(...args)` outside React components/custom hooks: handlers,
  sagas, tests, module initialization, and ordinary utilities cannot call these hooks.
- Do not call the direct signal form inside pure selector composition; use
  `.select(state, ...args)` instead.
- Do not pass signal results into pure reducers/selectors or compare them as plain
  values; read `.value` at tracked consumer boundaries.
- Do not create direct signals for one-shot handler/test reads; use `.select`.
- Do not pass the selector object itself to saga `select`; use `.effect(...args)`
  or `.select(state, ...args)` intentionally.
- Do not apply non-React selector lifecycle rules to a React app.

## Examples

### React component read with direct signals

```tsx
import { selectTodoById } from "../store/todos/todos-selectors";
import type { ReadonlySignal } from "@preact/signals-react";

type Todo = { title: string } | undefined;

function TodoTitleView({ todo }: { todo: ReadonlySignal<Todo> }) {
  return <span>{todo.value?.title ?? "Untitled"}</span>;
}

export function TodoTitle({ id }: { id: string }) {
  const todo = selectTodoById(id);
  return <TodoTitleView todo={todo} />;
}
```

### Fallback hook/plain-value read

```tsx
export function useCanEditTodo(id: string) {
  const todo = selectTodoById.useValue(id);
  const currentUser = selectCurrentUser.useValue();
  return Boolean(todo && currentUser && todo.ownerId === currentUser.id);
}
```

Use this fallback only when the hook contract must return a plain boolean and
rewriting callers to accept the underlying signals would be too invasive.

### Handler and test one-shot reads

```tsx
import { reactStore } from "../store/react-store";
import { deleteTodo } from "../store/todos/todos-slice";

function onDelete(id: string) {
  const todo = selectTodoById.select(reactStore.state, id);
  if (todo && !todo.completed) reactStore.dispatch(deleteTodo(id));
}
```

### Compose selectors

```ts
export const selectVisibleTodos = reactStore.createSelector((state) => {
  const todos = selectTodos.select(state);
  const filter = selectTodoFilter.select(state);
  return todos.filter((todo) => todo.status === filter.status);
});
```

### Saga reads

```ts
import { put } from "typed-redux-saga";

export function* saveCurrentTodoWorker() {
  const todoId = yield* selectCurrentTodoId.effect();
  if (todoId) yield* put(saveTodo(todoId));
}
```

### Explicit Store binding

```ts
const selectTodoFromPreviewStore = selectTodoById.withStore(previewStore);
const previewTodoSignal = selectTodoFromPreviewStore("todo-1");
```

`.withStore(...)` returns the direct-call family result for the explicit binding;
for `ReactStore`, that result is a Preact React `ReadonlySignal<R>`.

## Pitfalls

- React components that read `signal.value` without the Babel transform or an
  explicit `useSignals()` fallback may fail to re-render when the signal changes.
- `.select(state, ...args)` is pure and synchronous but not reactive. Components
  that need updates should prefer direct selector signals, falling back to
  `.useValue(...args)` only for necessary plain-value boundaries.

## Verification cues

- Component/custom-hook examples prefer direct selector signals and only use
  `.useValue(...args)` for documented plain-value fallbacks.
- Handler, callback, test, and selector-composition code uses
  `.select(state, ...args)` rather than `.useValue(...args)` or direct signals.
- Saga code uses `.effect(...args)`.
- Explicit alternate-store examples use `.withStore(...)` and treat the result as a
  signal-producing binding.
- Direct `.value` reads mention React signal tracking, and direct JSX signal
  rendering is limited to intentional signal-aware JSX positions.

## See also

- `../component-integration/SKILL.md` — app bootstrap, Store lifecycle, saga
  startup, component dispatch, and handler examples.
- `../selectors/SKILL.md` — authoring ReactStore selectors.
- `../store/SKILL.md` — `ReactStore` import and initialization rules.
- `@themislib/themis/docs/SELECTORS.md` — human reference for selector call forms.