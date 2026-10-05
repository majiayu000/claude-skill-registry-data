---
name: react
description: >-
  Route React UI work to ReactStore and Preact signals: signal-first reads,
  necessary .useValue fallbacks, tracking, lifecycle, scheduling, and migration.
  Use core for shared Redux/saga work.
type: core
requires:
  - core
sources:
  - ./signals/SKILL.md
  - ./selectors/SKILL.md
  - ./store/SKILL.md
  - ./component-integration/SKILL.md
  - ./selector-lifecycle/SKILL.md
  - ./selector-scheduling/SKILL.md
  - ./migration/SKILL.md
  - "@themislib/themis/README.md"
  - "@themislib/themis/docs/SELECTORS.md"
  - "@themislib/themis/react-store"
triggers:
  - ReactStore
  - react-store import
  - React selector
  - Preact signal
  - React signal
  - signal .value
  - useSignals
  - selector .useValue
  - Preact signal selector
  - ReadonlySignal selector
  - React component integration
  - React selector lifecycle
  - React selector scheduling
  - React migration
---
# ReactStore and signal selector routing

Use this root for React-specific `themis` work when the touched app or
code path has React evidence: React components/hooks, JSX/TSX UI, imports from
`react`, `ReactStore` from `@themislib/themis/react-store`, or Preact React signal
selector consumption. Generic Redux/redux-saga guidance remains in `../core/`.

## React Store family rule

- A React app using this skill has chosen `ReactStore` and Preact React signal
  direct selector calls as the preferred component/custom-hook integration path.
  `.useValue(...args)` remains available only for necessary hook/plain-value fallbacks.
- Keep this app path on `ReactStore` and Preact React signal integration.

## React leaf routes

| Route | Use when |
| --- | --- |
| `./signals/SKILL.md` | General Preact Signals guidance for ReactStore apps: `ReadonlySignal<T>`, `.value`, `computed`, Babel transform/`useSignals()` tracking, direct JSX signal rendering, component-local signal hooks, and avoiding module-level shared signal state. |
| `./store/SKILL.md` | Public `ReactStore` import and runtime API summary; app bootstrap mechanics live in component-integration. |
| `./selectors/SKILL.md` | Authoring Store-bound selectors, pure composition, argument tracking/stability, and cached `ReadonlySignal<R>` outputs; consumer call modes live in selector-lifecycle. |
| `./component-integration/SKILL.md` | Wiring `ReactStore` into JSX/TSX React apps, bootstrap/root init and disposal ownership, app saga startup through `reactStore.runSaga(sagaFn)`, React component reads through direct signals first, and Store-first dispatch. |
| `./selector-lifecycle/SKILL.md` | Choosing React selector call modes across component render/custom hooks, direct signal-aware code, handlers/callbacks/tests, sagas, selector composition, and explicit `.withStore(...)` binding. |
| `./selector-scheduling/SKILL.md` | React `ReadonlySignal`/`.useValue(...args)` scheduling guidance: same source + selector + args output reuse, Store-owned selector coalescing, `throttledSelectorFrequency`, package-private scheduler boundaries, and no manual debounce/audit-log misuse. |
| `./migration/SKILL.md` | React migration/adoption work from local React state/context/hooks/effects/external stores to `ReactStore`, selectors, actions, reducers, sagas, signal-first component consumption, and cleanup. |

First-time installation and family choice start at
[Store-family decision gate](../setup/SKILL.md#store-family-decision-gate).
Once React is selected, [Create and configure ReactStore](./component-integration/SKILL.md#create-and-configure-reactstore)
owns runtime bootstrap. Adoption of existing state uses the migration
[Adoption checkpoint](./migration/setup/SKILL.md#adoption-checkpoint), not another bootstrap procedure.

## Routing rules

- Use `ReactStore` only from `@themislib/themis/react-store`.
- Create production app-local React selectors through the configured
  `ReactStore` instance: `reactStore.createSelector(...)`.
- Signal-first consumers and necessary plain-value fallbacks follow
  [Call-mode map](./selector-lifecycle/SKILL.md#call-mode-map); tracking and
  wrong-shape boundaries follow [React signal consumption guardrails](./selector-lifecycle/SKILL.md#react-signal-consumption-guardrails).
- Output reuse and avoiding extra memoization follow
  [Selector caching](./selectors/SKILL.md#selector-caching).
- Store-owned cadence and temporary trace options follow
  [Store-first scheduling rule](./selector-scheduling/SKILL.md#store-first-scheduling-rule).
- React component, selector lifecycle, selector scheduling, and migration work must
  route to the React leaves above as operational guidance for this app.

Use the React leaves above for operational guidance. They cover component wiring,
selector call modes and scheduling, Store lifecycle, and migration in full.

## Verification cues

- Examples import package APIs only from public subpaths such as
  `@themislib/themis/react-store`, `@themislib/themis/saga`, and
  `@themislib/themis/types`.
- React guidance states that direct selector calls returning signals are preferred
  for React consumers, while `.useValue(...args)` returns plain `R` only as a necessary
  hook/plain-value fallback.
- Signal examples mention `.value` tracking through the Babel transform or
  explicit `useSignals()` and do not introduce module-level shared signal state.
- The app path uses `ReactStore` and Preact React signals consistently.