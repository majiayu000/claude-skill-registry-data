---
name: svelte
description: >-
  Route Themis Store wiring, readable selector lifecycle, and migration
  guidance only for frontend paths with concrete Svelte/SvelteKit evidence.
  Use Core for shared Redux/saga concepts.
triggers:
  - Svelte
  - SvelteKit
  - .svelte component
  - +layout.svelte
  - +page.svelte
  - svelte-store
  - Svelte readable
  - Svelte selector readable
  - Store component wiring
  - Svelte selector lifecycle
  - Svelte store migration
  - Svelte component integration
---

# Svelte-readable routing index

Use this skill only after the repository root router has classified the target
code path as frontend-facing with concrete Svelte or SvelteKit evidence. Use the
leaf skills below for implementation details; do not copy large API examples into
this Svelte index.

Core Redux and redux-saga guidance lives under `../core/`. Svelte-readable
Store selector/component guidance lives under `./`.

## Svelte Store family rule

- A frontend Svelte/SvelteKit app using this skill has chosen the concrete
  Svelte Store family: `Store`, Svelte readables, component-init
  selector calls, and Svelte lifecycle/setup patterns.
- Keep selector creation, readable observation, component setup, and teardown
  within the Svelte Store APIs documented by this subtree.

Do not route generic web, Node, server, CLI, worker, test-harness, or no-Svelte
paths here merely because the repository contains a Svelte dependency. In mixed
repositories, route by the files and behavior being changed.

> This package uses a CUSTOM Redux setup — not Redux Toolkit (RTK). Do not use
> `createSlice`, `configureStore`, `createAsyncThunk`, or any RTK API.

## Docs vs skills ownership

- Treat `docs/` as the human-facing source of truth for concepts, API behavior,
  tradeoffs, and longer examples.
- Treat skill files as concise agent-facing execution guidance: routing,
  must-follow rules, pitfalls, verification cues, and citations to docs/source.
- Do not duplicate long explanatory doc sections in skills. Link to the relevant
  doc/source, then state only the operational rule an agent must follow.
- If docs and skills conflict, stop and report instruction drift instead of
  choosing silently.

Detailed docs to consult when a task needs conceptual background:
`@themislib/themis/docs/ARCHITECTURE.md`, `@themislib/themis/docs/SELECTORS.md`, `@themislib/themis/docs/SAGAS.md`,
`@themislib/themis/docs/WAITFOR.md`, `@themislib/themis/docs/REDUCERS.md`, `@themislib/themis/docs/COLLECTIONS.md`,
`@themislib/themis/docs/TESTING.md`, and `@themislib/themis/docs/INSTALLATION.md`.

## Agent Preflight Compliance Contract

Before editing code or docs under this skill:

- **MUST** read this skill plus every linked skill/doc that applies to the touched files.
- **MUST** confirm and record concrete Svelte/SvelteKit evidence for the target
  app/package/code path before using this route.
- **MUST** cite the applicable skills and docs in the implementation plan or completion handoff, including the rules used.
- **MUST** include verifier-ready evidence: searches, tests, or diff checks proving the cited rules were followed.
- **SHOULD** stop and ask when rules conflict or scope is unclear.
- **NEVER** claim completion when a required skill/doc was skipped or the handoff lacks compliance evidence.
- **NEVER** use this Svelte route without concrete Svelte or SvelteKit evidence.

## Always-on policy

- Redux owns shared/domain state; shared Svelte stores (`*.store.svelte.ts`) are deprecated. Ephemeral instance-local UI state remains local per `../core/core-policy/SKILL.md` → **Setup — core rules**.
- A Svelte app uses `Store` and Svelte-readable selectors for its Store-backed
  component reads.
- Redux state is canonical only: no derived fields, duplicated entity copies,
  parallel arrays/maps for the same records, or reducer-maintained selector outputs.
- Components render and dispatch; reducers update state; sagas own domain side effects. DOM-local focus, scroll, measurements, and widget lifecycle stay in components per `../core/core-policy/SKILL.md` → **Setup — core rules**.
- State must stay serializable; normalized object collections use `Collection<T, K>`.
- Actions, selectors, and sagas each have one canonical owner/implementation; run
  the state/action/selector/saga preflight searches before adding another.
- Run architecture validation before handoff whenever Redux state, actions,
  selectors, sagas, or their governance docs change. Inside this repository use
  `npm run validate:architecture`; in a consuming app run ESLint with the
  `svelte` domain root config imported from `@themislib/themis/eslint-plugins`.
  Include the exit code/output and canonical-owner evidence in the handoff.
- The architecture gate also checks RTK/shared Svelte-store boundaries,
  collection state shape/internal mutations, runtime state serialization,
  reducer purity, conservative component lifecycle/store access, and
  pass-through wrapper cleanup; Wave 3 adds selector call modes, typed saga
  `yield*` style, channel lifecycle cleanup, file-structure naming, and
  high-signal test-pattern hygiene. Report any rule-specific ignore reasons.
- Keep semantic or noisy adequacy questions verifier-guided; do not add or claim
  new CI gates beyond the documented modular gate set without explicit approval.
- Types belong in dedicated `{slice-name}-types.ts` modules.
- Before adding helpers or wrappers, search existing utilities and document reuse.
- For final review of recurring failures, route to `../core/verifier/SKILL.md`.

## Routing workflow

1. Start with `../core/core-policy/SKILL.md` for any shared-state task.
2. Add `../core/state-integrity/SKILL.md` before adding or changing Redux
   state, actions, selectors, or sagas.
3. Add the domain leaf or leaves that match the files and behavior being changed.
4. Add `../core/testing/SKILL.md` for tests or saga/reducer verification.
5. Add `../core/debugging/SKILL.md` for runtime inspection or reducer reference-equality issues.
6. Use `../core/verifier/SKILL.md` before handoff when reviewing reliability risks.

## Examples

### Route shared state changes to policy plus primitives

For editable todos shared across routes, load Core policy, state integrity,
actions, reducers, and Svelte selectors from the table below. Show canonical-owner
searches, reducer no-op tests, and selector `.select(state)` tests.

### Route side effects to sagas or persistence leaves

For startup preference persistence, load Core policy, sagas, local storage, and
testing. Reducers receive serializable facts only; sagas perform storage I/O.

### Route component wiring to lifecycle-aware skills

For rendering a selected todo and dispatching rename, load Svelte component
integration, selector lifecycle, and Core import boundaries. Create selector
readables during component initialization; dispatch through the configured Store.

### Route Store-first dispatch and state reads

Use `./store/SKILL.md` → **Correct import and class choice**, **Lifecycle rules**,
and **App saga lifetime** for construction, initialization, and cleanup. Use
`./selector-lifecycle/SKILL.md` → **Call-mode map** for direct state reads and
`./component-integration/SKILL.md` → **Template and handler wiring** for dispatch
through the configured Store. This index routes those procedures instead of
maintaining a second lifecycle implementation.

### Verification handoff evidence payload

Record skills/docs read, owner-search terms and paths, canonical owner files,
and verification commands with exit codes/key output, including architecture
validation and `git diff --check` when applicable.

### ❌ Bad: root request bypasses shared-state routing

Do not put shared route data in `writable(...)` and load only component integration:
that skips canonical ownership, reducer, selector, and saga review. Use the shared
state route above; a Svelte API does not make shared/domain state component-local.

## Core leaf routes

| Path | Use when |
| --- | --- |
| `../core/core-policy/SKILL.md` | Ownership, serializability, saga-only effects, shared-store deprecation, utility reuse. |
| `../core/state-integrity/SKILL.md` | Canonical state and action/selector/saga owners; no derived/duplicated data. |
| `../core/import-boundaries/SKILL.md` | Component/saga imports and Store-first public subpackages/entry points. |
| `../core/file-structure/SKILL.md` | Creating/moving slices, types, selectors, sagas, or Store registration. |
| `../core/state-serialization/SKILL.md` | Serializable, structured-clone-safe state. |
| `../core/actions/SKILL.md` | Custom `createAction` / `createAsyncAction`. |
| `../core/reducers/SKILL.md` | Immutable chained reducers and no-op reference equality. |
| `./selectors/SKILL.md` | Store-bound selector authoring/composition, collection reads, cache contracts, stable arguments. |
| `./selector-lifecycle/SKILL.md` | Component-init, handler, and saga call modes; Store-first dispatch. |
| `../core/selector-channels/SKILL.md` | Selector-triggered saga work and selector-backed channels. |
| `./selector-scheduling/SKILL.md` | FPS/coalescing; avoid extra schedulers and event-log assumptions. |
| `../core/wait-for/SKILL.md` | Suspend sagas until selector predicates pass or time out. |
| `../core/sagas/SKILL.md` | Typed saga flows/watchers, batching, debounce, retry/timeout, async-generator streams, orchestration. |
| `../core/saga-manager/SKILL.md` | Package crash tracking, serialized crash storage, cleanup, Store `runSaga` start/stop/restart, backoff. |
| `../core/local-storage/SKILL.md` | Saga storage reads/writes/removal, prefix listing, initialization, persistence. |
| `../core/channel-effects/SKILL.md` | Generic EventChannels: IPC, websocket, DOM events. |
| `../core/collections/SKILL.md` | Normalized `Collection<T, K>` entity state. |
| `../core/domain-scoped-state/SKILL.md` | State keyed by workspace, project, tenant, or other domain id. |
| `../core/boolean-preference/SKILL.md` | Set/toggle preference helpers and reducer registration. |
| `./store/SKILL.md` | Store choice/import, init/dispose, `useInitStore`/`useRunSaga`, shared runtime behavior. |
| `./component-integration/SKILL.md` | Root layout, template, and handler lifecycle wiring. |
| `../core/testing/SKILL.md` | Reducer/selector/saga tests, typed saga mocks, reference equality. |
| `../core/debugging/SKILL.md` | `window.svelteRedux` inspection and reducer reference-equality diagnosis. |
| `../core/verifier/SKILL.md` | Review-only instruction, cleanup, reuse, state/owner, automated, and semantic gates. |

## Related lifecycle routes

- First-time app setup: `../setup/SKILL.md`.
- Migration playbook: `./migration/SKILL.md`.
- Install/uninstall side effects and maintainer validation: `@themislib/themis/docs/INSTALLATION.md`.
- Generic plain redux-saga API reference, outside this package's typed-redux-saga conventions: `../core/redux-saga/SKILL.md`.
