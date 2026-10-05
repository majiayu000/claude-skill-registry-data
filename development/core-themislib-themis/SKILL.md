---
name: core
description: >-
  Route shared Redux state, actions, reducers, collections, sagas, channels,
  logging, serialization, testing, debugging, review, and explicit store pruning.
  Pair Core with one Store family per app for framework-specific behavior.
type: core
triggers:
  - redux core
  - core redux
  - shared state
---
# Core Redux and saga routing

Use this skill for framework-independent Redux/redux-saga work in the
`themis` package. It routes to the core skills that are not owned
by Store-family-specific taxonomy waves.

## Routing ownership

This index owns core routing, not leaf operational contracts. Match specialized
requests to the relative `SKILL.md` paths in **Core leaf routes** below; each
leaf owns its implementation rules. Loading this index through a leaf's
`requires: core` provides preflight context, not a competing implementation owner.

> This package uses a CUSTOM Redux setup — not Redux Toolkit (RTK). Do not use
> `createSlice`, `configureStore`, `createAsyncThunk`, or any RTK API.

## Preflight

- Read this skill plus every linked core leaf that applies to touched files.
- Cite the applicable skills and docs in implementation plans and handoffs.
- Include verifier-ready evidence: owner searches, focused tests, validation
  scripts, or `git diff --check` depending on the change.
- Stop and ask if a request crosses into Store-family-specific selector,
  component, lifecycle, or observable behavior.
- Pair core with at most one concrete Store family for a given app/code path;
  core is shared Redux/redux-saga guidance and is not permission to integrate
  multiple concrete Store family patterns in one app.

## Core routing workflow

1. Start with `./core-policy/SKILL.md` for shared-state or architecture decisions.
2. Add `./state-integrity/SKILL.md` before adding/changing Redux state, actions,
   selectors, watchers, or saga registration.
3. If and only if the user explicitly asks to prune unused Redux store surface
   area, add `./store-pruning/SKILL.md` before deleting selectors, actions,
   reducers, sagas, exports, tests, or orphaned helpers.
4. Add domain leaves that match the behavior being changed.
5. Add `./testing/SKILL.md` for reducer, saga, or verification changes.
6. Add `./verifier/SKILL.md` before handoff for reliability-sensitive reviews.

## Core leaf routes

| Route | Use when |
| --- | --- |
| `./core-policy/SKILL.md` | Redux ownership, side-effect boundaries, serializability, and utility reuse rules. |
| `./state-integrity/SKILL.md` — **Preflight search protocol** | Preventing derived/duplicated Redux state and duplicate action/selector/saga ownership. |
| `./store-pruning/SKILL.md` — **Agent preflight** | Explicit-only pruning of unused Redux selectors, actions, handlers, sagas, and orphaned store logic when the user asks for pruning. |
| `./import-boundaries/SKILL.md` | Public package imports, saga import boundaries, and Store-first public subpackages. |
| `./file-structure/SKILL.md` | Slice file layout, type modules, sagas, and Store registration patterns. |
| `./state-serialization/SKILL.md` — **Do** and **Don't** | Structured-clone-safe Redux state values. |
| `./actions/SKILL.md` — **Do** and **Async action cues** | `createAction` and `createAsyncAction` action creators. |
| `./reducers/SKILL.md` — **Do** and **Implementation cues** | `createReducer`, immutable chained reducers, and no-op reference equality behavior. |
| `./sagas/SKILL.md` — **Do** and **Implementation cues** | typed-redux-saga flows, watchers, debounce, retry/timeout, and side-effect orchestration. |
| `./saga-manager/SKILL.md` — **Store saga lifecycle** and **Start, stop, restart, and backoff mechanics** | `store.runSaga`, per-owner cancellation, whole-Store disposal, and package-owned crash/restart behavior. |
| `./channel-effects/SKILL.md` | Generic EventChannel consumers for IPC, websocket, or DOM channels. |
| `./selector-channels/SKILL.md` | Saga reactions to selector value changes. |
| `./wait-for/SKILL.md` | One-shot saga waits for selector predicates. |
| `./local-storage/SKILL.md` | Safe app-local localStorage persistence from sagas. |
| `./redux-action-logging/SKILL.md` — **Store-owned logging streams** and **Logger factory lifecycle** | Construction-time `logReduxActions`, action/state diffs, and shared stream/logger ownership across Store families. |
| `./selector-tracing/SKILL.md` | Selector performance, tracing configuration, privacy-safe interval aggregates, and lifetime summaries. |
| `./collections/SKILL.md` | Normalized `Collection<T, K>` entity state. |
| `./domain-scoped-state/SKILL.md` | State keyed by workspace, project, tenant, or domain id. |
| `./boolean-preference/SKILL.md` | Boolean set/toggle preference helper registration. |
| `./testing/SKILL.md` — **Layer rules** and **Verification cues** | Reducer/saga testing, typed-redux-saga mocks, and reference equality assertions. |
| `./debugging/SKILL.md` | Runtime inspection and reducer reference-equality diagnostics. |
| `./verifier/SKILL.md` — **Required gate sequence** | Review quality gates for instruction drift, duplicate owners, and evidence. |
| `./redux-saga/SKILL.md` — **Package guidance takes precedence** | Generic upstream API details only; use `./sagas/SKILL.md` for Themis typed effect rules and `./saga-manager/SKILL.md` for Store-owned lifecycle. |

## Related non-core routes

- Store family selector, component, lifecycle, migration, and observable-output
  guidance is selected by the root router outside core.
- Concrete Store families are mutually exclusive per app. Mixed repositories may
  use different families in separate apps/packages/code paths, but one app must
  not combine multiple Store family patterns.
