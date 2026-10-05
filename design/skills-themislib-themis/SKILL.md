---
name: themis
description: >-
  Route first-time Themis setup and shared Redux/saga guidance. Choose Svelte
  or React only with concrete UI evidence; default to Streaming for Node/no-UI
  paths or absent UI evidence. Use one Store family per app; prune only on
  explicit request.
type: core
sources:
  - ./setup/SKILL.md
  - ./core/SKILL.md
  - ./svelte/SKILL.md
  - ./react/SKILL.md
  - ./streaming/SKILL.md
  - "@themislib/themis/README.md"
  - "@themislib/themis/docs/ARCHITECTURE.md"
triggers:
  - themis
  - skill router
  - root skill router
  - Store routing
  - greenfield setup
  - StreamingStore
  - ReactStore
  - Svelte + Redux
  - React signals
  - Redux saga
  - Redux store pruning
  - selector lifecycle
  - Store state lifecycle
  - selector before init
  - Node store
---
# themis skill router

Use this repository root skill first when choosing package guidance. Its job is routing only: load `./setup/SKILL.md` for first-time app setup, load the family that matches the environment and touched code path, then load the leaf skills named by that family. Do not treat this file as a replacement index for `./setup/`, `./core/`, `./svelte/`, `./react/`, or `./streaming/`.

For the package's custom Redux API and architecture constraints, read `./core/core-policy/SKILL.md` — **Setup — core rules**.

## App-level Store family rule

- **Svelte Store, React Store, and Streaming Store patterns are mutually exclusive for a single app.** One app must choose exactly one concrete Store family: `Store` plus Svelte readable/component lifecycle patterns, `ReactStore` plus Preact signal/React `.useValue(...)` patterns, or `StreamingStore` plus Kefir/observable selector patterns.
- Do not mix `./svelte/`, `./react/`, and `./streaming/` concrete Store guidance for the same app, package entry, runtime, or code path. `./core/` may be paired with the one selected concrete family because it is shared Redux/redux-saga guidance, not a second Store family.
- Mixed repositories must route per app/package/code path. Separate apps in the same repository may choose different families, but one app must not use patterns from multiple concrete Store families.

## Selector output cache routing

- After selecting the family, route Svelte readable cache guidance to `./svelte/selectors/SKILL.md` — **Selector caching** and `./svelte/selector-scheduling/SKILL.md`.
- Route React `ReadonlySignal` cache guidance to `./react/selectors/SKILL.md` — **Selector caching** and `./react/selector-scheduling/SKILL.md`; preferred consumer call modes belong to `./react/selector-lifecycle/SKILL.md` — **Call-mode map**.
- Route Streaming/Kefir `Observable` cache guidance to `./streaming/selectors/SKILL.md` — **Selector caching** and `./streaming/selector-lifecycle/SKILL.md` — **Lifecycle map**.

## Universal architecture routing

For every family, route Redux ownership and component-versus-saga side-effect decisions to `./core/core-policy/SKILL.md` — **Setup — core rules** and **When to use Redux vs component-local state**. That skill owns the policy, including the DOM-local exception; this router does not redefine it.

For existing effects, classify them with that policy before loading the selected family's migration leaf: `./react/migration/side-effects/SKILL.md` or `./svelte/migration/side-effects/SKILL.md`. Do not load both for the same app.

## Generic lifecycle routing

Unqualified requests such as `selector lifecycle`, `Store state lifecycle`, or `selector before init` enter here, not a concrete family leaf. First identify the target app/package/code path using **Routing decision order**. If the path itself is unknown, ask for it; once classified, absence of concrete UI evidence defaults to Streaming. Load only the selected family's Store and selector-lifecycle leaves through `./svelte/SKILL.md`, `./react/SKILL.md`, or `./streaming/SKILL.md`. A generic lifecycle phrase alone is not evidence for any UI family.

## Routing decision order

1. **Shared Redux or saga concept only.** → `./core/` Use core for action creators, reducers, state modeling, serializability, typed-redux-saga flows, saga manager behavior, selector channels, `waitFor`, explicit Redux store pruning, testing, debugging, and verifier handoff that apply across Store families.
2. **Frontend-facing plus Svelte/SvelteKit evidence.** → `./svelte/` Use Svelte only when the target app/code path is UI/frontend-facing and there is concrete Svelte or SvelteKit evidence: a Svelte dependency, `svelte.config.*`, `.svelte` component files, SvelteKit `+layout`/`+page` files, imports from `svelte`, `Store` from `@themislib/themis/svelte-store`, or Svelte readable/template integration. Generic browser or web work is not enough. Do not also apply ReactStore/signals or StreamingStore/Kefir selector, setup, or lifecycle guidance to that same app.
3. **Frontend-facing plus React evidence.** → `./react/` Use React when the target app/code path imports React, uses JSX/TSX React components/hooks, imports `ReactStore` from `@themislib/themis/react-store`, or expects Preact React signal selectors/`.useValue(...)` component reads. Do not also apply Svelte readable or StreamingStore/Kefir guidance to that same app.
4. **Node/server/no-UI path.** → `./streaming/` by default. Use Streaming for Node services, server routes, background workers, CLIs, scripts, test harnesses, Kefir/observable selectors, `StreamingStore`, or any app/code path where concrete Svelte or React UI evidence is absent. Absence of UI evidence defaults to Streaming. Do not also apply Store/readable/component/setup, React `.useValue(...)`, or signal-render guidance to that same app.
5. **Mixed repositories route by the task path.** A repository-level Svelte or React dependency does not make every change UI-specific. Classify the specific files and behavior being changed, then choose Core plus at most one concrete Store family for each app/package/code path.

## Route matrix

| Situation | Read these skills |
| --- | --- |
| First-time app setup or greenfield Store wiring | ./setup/SKILL.md plus exactly one matching family router and any needed core leaves |
| Redux ownership, actions, reducers, serializable state, typed-redux-saga, selector channels, or tests with no Store-variant behavior | ./core/SKILL.md plus matching core leaves |
| Explicit request to prune unused Redux store selectors, actions, handlers, sagas, or orphaned store logic | ./core/SKILL.md plus ./core/store-pruning/SKILL.md; do not apply pruning automatically to unrelated work |
| Svelte component setup, SvelteKit root layout wiring, Svelte readable selector calls, $selector template usage, or migration from Svelte stores/runes | ./svelte/SKILL.md plus matching Svelte leaves and any needed core leaves |
| React component setup, ReactStore imports, Preact React signal selectors, direct signal reads, selector .useValue(...args), React selector lifecycle/scheduling, or React migration/adoption work | ./react/SKILL.md plus matching React leaves (`react/store`, `react/selectors`, `react/component-integration`, `react/selector-lifecycle`, `react/selector-scheduling`, `react/migration/**`) and any needed core leaves |
| Node services, server modules, background jobs, package scripts, CLIs, tests, Kefir streams, observable selector arguments, or StreamingStore | ./streaming/SKILL.md plus matching Streaming leaves and any needed core leaves |
| A mixed task that touches reducer policy and Svelte component wiring | ./core/SKILL.md for shared policy and ./svelte/SKILL.md for component/readable behavior |
| A mixed task that touches reducer policy and Streaming selector behavior | ./core/SKILL.md for shared policy and ./streaming/SKILL.md for observable behavior |
| A mixed repository with a Svelte frontend and a separate Node worker app | Route the frontend app to ./svelte/ and the worker app to ./streaming/ separately; do not mix both concrete Store families inside either app |

## Consumer skill install routing

When a consuming app asks for packaged AI skills, use the same evidence as **Routing decision order** to select the smallest matching bundle:

- React evidence → React bundle.
- Svelte/SvelteKit evidence → Svelte bundle.
- Streaming/no-UI or observable evidence → Streaming bundle.
- Shared Redux/redux-saga guidance only → Core bundle.
- Choose all families only when every family is intentionally needed across separate apps or paths.

Continue at `./setup/SKILL.md` — **Installation workflow**. The sole operational owner is `@themislib/themis/docs/INSTALLATION.md` — **Consumer CLI and bundle selection** and **Verify, refresh, cleanup, and uninstall**; it specifies commands, bundle contents, destinations, compatibility links, collision/refresh behavior, and cleanup ordering.

## Evidence to record in handoff

- The code path classified as frontend/Svelte, frontend/React, Node/server/Streaming, or shared Core, with the concrete evidence used and the single concrete Store family chosen for that app.
- The exact skill family and leaf skills read.
- For mixed repositories, why repository-wide dependencies did or did not affect the specific path being changed.
- Confirmation that the same app/package/code path did not mix Svelte, React, and Streaming Store concrete patterns.
- Verification that no placeholder, shim-only, or barrel-only skill replaced the meaningful core, Svelte, React, or Streaming directory roots.