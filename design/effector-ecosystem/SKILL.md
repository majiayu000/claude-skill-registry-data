---
name: effector-ecosystem
description: "Use when designing, reviewing, generating, or refactoring React applications built with Effector, effector-react, Farfetched, Atomic Router, @effector/next, patronum, effector-storage, forms, i18n, testing, and related Effector ecosystem tooling. For Feature-Sliced Design project structure and placement decisions, use the separate effector-fsd skill."
license: MIT
---

# Effector Ecosystem Skill

## Purpose

Use this skill for frontend applications that use or plan to use:

- React or React-compatible UI
- Effector for business logic and state
- `effector-react` for binding units to components
- Farfetched for remote operations
- `@withease/contracts` or compatible contracts for runtime validation
- Supporting packages from the Effector ecosystem: `patronum`, `atomic-router`, `effector-storage`, `effector-action`, `effector-forms`, `@withease/factories`, `@withease/i18next`, `@withease/web-api`, `@effector/next`, `@effector/reflect`, `@withease/redux`, `eslint-plugin-effector`, Effector Babel/SWC plugins

This skill is **project-structure agnostic**. It may use paths like `entities/user` or `shared/api` in examples, but it must not decide Feature-Sliced Design placement rules. When the question is mainly about layers, slices, public APIs, import boundaries, file placement, or project structure in an Effector project, use `effector-fsd`.

The target architecture:

> UI is dumb. Business logic is declarative. Remote data is validated. Startup is explicit and scoped. Remote-operation semantics are modeled, not hidden in React components.

## Activation triggers

Use this skill when the user asks about:

- Effector model design
- `sample`, `combine`, `attach`, effects, stores, events, factories, Scope, SSR, `scopeBind`
- React binding with `useUnit`
- Farfetched query/mutation/barrier/cache/concurrency/contracts
- Atomic Router route models and route loaders
- `@effector/next`, App Router, Pages Router, SSR, hydration, Scope serialization
- Persistence, forms, i18n, browser APIs, testing, and ecosystem package choice
- Reviewing code for Effector/Farfetched/Scope/React anti-patterns
- Creating templates for models, queries, mutations, forms, routing, persistence, or tests

Do **not** use this skill as the primary source for FSD structure. Use `effector-fsd` for placement and import-boundary decisions.

## First response behavior

When answering, first identify the goal:

1. Designing a model or flow
2. Refactoring an existing model/component/API operation
3. Reviewing a code fragment
4. Choosing ecosystem packages
5. Creating a query, mutation, route, form, persistence adapter, or test
6. Integrating with SSR/Next.js/Scope

If the user gives code, review it against this skill and return:

- What is good
- What is wrong
- Why it is wrong
- A minimal corrected version
- Any placement note only as an example, unless `effector-fsd` is also in scope


## Full audit mode

When the user asks for a full audit, deep review, architecture audit, or “is everything best practice?”, do not stop at local anti-patterns. Perform a cross-cutting static data-flow audit. Build and inspect these graphs before writing the final answer:

1. **Startup graph:** `main`/entrypoint → `fork`/`Provider` → `appStarted` → storage/session restore → router/history installation → initial route open. Flag router/history startup that can open protected routes before auth state is known.
2. **Auth lifecycle graph:** login success, session restore success/failure, logout/session clear, token refresh, `401/403` API failures, route redirects, protected-route rejection. Flag any `sessionCleared`/logout/unauthorized path that does not update route state.
3. **Remote-operation graph:** every Farfetched query/mutation, its starters, refresh/invalidation sources, `concurrency`, `abortAll`, cache/update policy, and `$pending` gates. Flag duplicated starts, unintentional `TAKE_EVERY`, stale-result races, and page models that refetch while their route is closed.
4. **Scope and external callbacks graph:** timers, history listeners, DOM/browser listeners, SDK callbacks, WebSockets, storage pickup, HMR/unmount cleanup. Flag module-level mutable handles such as `let intervalId`, missing `scopeBind`, and declared `appDestroyed`/stop events that are never called.
5. **Reactive purity graph:** all `sample.fn`, `combine`, store `.map`, reducers, and contracts. Flag transformations that can throw (`new Date(...).toISOString()`, `JSON.parse`, unsafe property access), long inline algorithms, and success handlers that read operation `$data` instead of the `clock` payload.
6. **React async boundary graph:** components that pass Effector events to callback props expecting `Promise`, local pending state around Effector events, direct route/API calls, or business branching in JSX.

For each finding, include file/path evidence, severity, why it matters, a minimal fix, and an acceptance criterion. If a problem is not directly visible but follows from Effector static graph semantics, explicitly say it is an inferred risk and show the chain of units that creates it.

## Non-negotiable principles

### 1. UI must stay dumb

React components must:

- render data
- call events, effects, query/mutation starters, or route actions already prepared in models
- pass props to dumb components
- bind Effector units through `useUnit`

React components must not:

- contain business decisions
- call API directly
- branch over domain workflow rules
- call `sample`, `createEvent`, `createStore`, `createEffect`, or factories during render
- read stores through `$store.getState()`
- use `watch` for application behavior
- pass raw events/effects to DOM handlers or ordinary callback props when Scope/SSR may be used

### 2. Prefer one `useUnit` shape per connected component

For every component that reads/calls several Effector units from the same model, prefer a single `useUnit` call with an object or array shape:

```tsx
const { value, submitDisabled, onValueChange, onSubmit } = useUnit($$form);
```

or:

```tsx
const [value, submitDisabled, onValueChange, onSubmit] = useUnit([
  $value,
  $submitDisabled,
  valueChanged,
  submitted,
]);
```

Then destructure every returned value and pass the bound callbacks to JSX. Name handler-like values returned from `useUnit` with React-style `on*` aliases: expose `onSubmit: submitted`, `onValueChange: valueChanged`, `onRetryClick: retryClicked`. Keep Effector events named as facts in models; alias them only for React binding.

Avoid repeated bindings in the same component:

```tsx
// bad by default: noisy and easier to desync during refactoring
const value = useUnit($value);
const submitDisabled = useUnit($submitDisabled);
const onValueChange = useUnit(valueChangedEvent);
```

Split the component when subscription granularity matters instead of scattering many `useUnit` calls in one component.

### 3. Effector models must be static and declarative

Create units at module level only.

Use:

- `createEvent` for facts that happened
- `createStore` for state
- `createEffect` only for side effects not already handled by Farfetched
- `attach` to inject stores/params into an effect declaratively
- `sample` as the main connection operator
- `combine` for view models
- `split` or `effector-action` for complex branching when it improves readability
- named pure functions for non-trivial data transformation used by `combine`, `sample.fn`, or store `.map`
- `patronum` for common operators like debounce, throttle, reset, status, pending helpers
- factories for repeated same-shaped model logic that needs independent instances
- `scopeBind` for callbacks that leave Effector's call stack and must still work inside a Scope

Avoid:

- imperative chains inside effects
- nested event calls inside effects
- `watch` for logic
- `$store.getState()` for production logic
- creating models from React components
- using derived stores as mutation targets
- long inline mapping, sorting, grouping, normalization, or formatting inside `combine`, `sample.fn`, or store `.map`
- returning `undefined` from store reducers unless `skipVoid: false` is intentional
- oversized models that own several unrelated workflows at once
- huge object stores when several atomic stores are clearer

Prefer concern-based submodels over large all-in-one models. When a model grows into several workflows, split it into submodels such as `$$form`, `$$filters`, `$$list`, `$$selection`, or `$$dialog`; keep each submodel responsible for its own state and local rules. The top-level model should stay thin and orchestrate interactions between submodels with `sample` and other declarative connections.

Keep Effector models declarative by extracting non-trivial data transformation to named pure functions. Small boolean checks or simple field joins can stay inline; complex mapping, sorting, grouping, DTO normalization, permission-derived view models, or formatting should live near the owning model/API/domain helper. The model should connect stores/events and call these functions, not hide algorithms inside reactive operators.

Prefer factories over copy-pasted Effector model code for repeated forms, filters, widgets, or other independent instances with the same behavior. In SSR/Scope/SID-sensitive apps, use `@withease/factories` and configure the Effector Babel/SWC plugin `factories` field; invoke factories at module top level, never during render.

### 4. Farfetched owns remote operations

Use Farfetched for backend communication:

- `createJsonQuery` for data reads
- `createJsonMutation` for data writes
- `declareParams<T>()` for typed params
- `response.contract` for runtime validation
- `mapData` to map DTOs after validation
- `mapError: ({ error }) => ...` to normalize transport/validation/domain errors with the current Farfetched object-argument shape
- `concurrency` operator for route/search/filter cancellation; for submit de-duplication prefer an explicit Effector `$pending` gate and choose Farfetched concurrency cautiously
- `createBarrier` + `applyBarrier` for auth refresh or unavailable-resource flows
- `keepFresh`, `cache`, `.refresh`, and `update` for refresh/cache semantics when appropriate
- `request.fetch.credentials` for cookie/session APIs in current Farfetched code
- `@farfetched/atomic-router` for query-driven route loading when Atomic Router is used

Never trust backend data without a runtime contract.

### 5. Application startup must be explicit and scoped

Prefer one application event such as `appStarted` and one page/route event such as `pageStarted` over several free-floating startup functions.

Default pattern:

```ts
const scope = fork();
await allSettled(appStarted, { scope, params: startParams });
```

Connect storage pickup, i18n, router start, initial queries, and browser integrations from that event with `sample` or effects. Avoid sequences like this by default:

```ts
await startAppClock(scope);
await allSettled(appStarted, { scope });
await startRouter(scope);
```

Treat that sequence as wrong by default. Prefer modeling adapter installation as effects started from `appStarted` (`sample({ clock: appStarted, target: routerStartedFx })`). Keep free-floating `startAppClock(scope)` / `startRouter(scope)` only as a documented last-resort host wiring boundary that cannot be expressed as a scoped effect before the first callback fires. Business decisions must still be triggered from `appStarted`, route events, or scope-bound callbacks.

Use `allSettled(scope)` only when you intentionally need to wait for already-started async work that was triggered outside the direct `allSettled(event, { scope })` call, for example by a `scopeBind` callback from a timer, SDK, history listener, or WebSocket.

### 6. Packages are chosen by purpose

Do not add packages because they are popular. Choose them when they solve a specific architectural problem.

Use the package map in `references/01-package-map.md` and the detailed notes in `references/10-ecosystem-library-notes.md`.

## Path examples

Code examples may use path aliases such as:

```txt
@/shared/api/base-url
@/entities/session
@/features/profile-update
@/pages/user/model/page.model
```

These are illustrative. Do not infer full project-structure rules from this skill. For placement and boundary decisions, use `effector-fsd`.

## Naming rules

Stores:

```ts
export const $user = createStore<User | null>(null);
export const $isAuthorized = createStore(false);
```

Events:

```ts
export const formSubmitted = createEvent<FormValues>();
export const searchChanged = createEvent<string>();
export const pageOpened = createEvent();
```

`useUnit` UI binding shapes should expose these events as handler aliases:

```ts
export const $$form = {
  value: $value,
  onValueChange: valueChanged,
  onSubmit: formSubmitted,
};
```

Effects:

```ts
export const analyticsTrackedFx = createEffect<AnalyticsPayload, void>();
```

Queries/mutations:

```ts
export const userQuery = createJsonQuery(...);
export const updateProfileMutation = createJsonMutation(...);
```

Avoid vague names:

```ts
// bad
export const setData = createEvent<any>();
export const update = createEvent();
export const fx = createEffect();
```

## Required references

Before giving a detailed answer, consult the relevant files:

- `references/00-source-policy.md`
- `references/01-package-map.md`
- `references/03-effector-modeling.md`
- `references/04-farfetched-contracts.md`
- `references/05-react-ui-binding.md`
- `references/06-routing-forms-persistence-i18n.md`
- `references/07-testing-tooling.md`
- `references/08-anti-patterns.md`
- `references/09-review-checklist.md`
- `references/10-ecosystem-library-notes.md`
- `references/11-nextjs.md`
- `references/12-production-audit-playbook.md`

## Default answer style

Be specific. Prefer concrete code examples.

When correcting code, show the minimal correct version first, then explain.

When placement is the central question, switch to or ask to apply `effector-fsd`.

When a choice is trade-off based, say what the default should be and when to deviate.
