---
name: react/store
description: >-
  Use @themislib/themis/react-store for ReactStore imports, init/dispose, and
  runSaga/dispatch/state behavior. Defer app wiring and selector call modes to
  their React owners.
type: sub-skill
requires:
  - react
  - core/import-boundaries
sources:
  - "@themislib/themis/react-store"
  - "@themislib/themis/docs/ARCHITECTURE.md"
  - "@themislib/themis/README.md"
triggers:
  - ReactStore
  - react-store import
  - ReactStore state lifecycle
  - signal Store
---
# ReactStore import and lifecycle

Use this skill when a task needs the React signal Store variant. For shared state
policy, reducers, actions, sagas, and package import boundaries, also follow the
matching `core/*` skills.

## Correct import and class choice

- Use `ReactStore` from `@themislib/themis/react-store`.
- Do not import React selector internals from `src/*` or `utils/react-selectors/*`.

```ts
import { ReactStore } from "@themislib/themis/react-store";

export const reactStore = new ReactStore({ todos: todosReducer });
const dispose = reactStore.init();
```

## Lifecycle rules

This is a runtime API summary. Bootstrap, init/dispose ownership, and app saga
startup procedures belong to
[Create and configure ReactStore](../component-integration/SKILL.md#create-and-configure-reactstore)
and its lifecycle sections. Consumer call-mode decisions belong to
[Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map).

- Construct `ReactStore` with app-owned reducers and optional middleware, then
  call `reactStore.init(initialState?)` before invoking direct selector calls or
  `.useValue(...args)`.
- React selector calls return Preact React signal outputs backed by the Store-owned
  state stream after initialization and throw before `init()` or after `dispose()`.
- Keep app shared/domain state in reducers and ReactStore selectors rather than
  module-level shared Preact signals.
- `reactStore.dispatch`, `reactStore.state`, `reactStore.runSaga(sagaFn)`, and
  `reactStore.dispose()` follow the shared Store runtime behavior documented in
  `@themislib/themis/docs/ARCHITECTURE.md`; saga runtime mechanics are in
  [Store saga lifecycle](../../core/saga-manager/SKILL.md#store-saga-lifecycle).
- Do not manually register package-owned `@internal_` reducers or internal sagas.

## Verification cues

- Imports use `@themislib/themis/react-store` for `ReactStore`.
- React examples initialize the Store before signal selector reads.
- The app path uses only the public ReactStore runtime and React signal selectors.