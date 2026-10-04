---
id: angular.state.signals-vs-rxjs
name: Angular Signals vs RxJS State Decision
description: >
  Chooses between Angular Signals and RxJS based on Angular version, state lifetime, synchronicity, cancellation needs, and feature boundaries.
stack:
  - Angular
  - TypeScript
  - RxJS
category: state
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Signals vs RxJS
  - should this use signals
  - should this use observables
  - Angular state decision
  - toSignal
  - toObservable
compatibility:
  angular:
    min: "2"
    signalsFrom: "16"
    recommendedSignals: "17+"
    currentSafe: "19+"
---

# Angular Signals vs RxJS State Decision

## Purpose

Use this skill to choose the right reactive primitive for Angular state. The goal is to avoid forcing Signals into asynchronous workflows or keeping RxJS boilerplate where simple local synchronous state is enough.

## When to Use

Use this skill when:

- The user asks whether a feature should use Signals, RxJS, both, or neither.
- Local UI state is stored in a global store.
- A component uses RxJS for simple synchronous toggles, selected tabs, or derived flags.
- Signals are proposed for HTTP, router streams, WebSockets, debounced search, or cancellation-heavy flows.
- A feature mixes Signals and Observables without a clear boundary.
- Angular version compatibility is unknown.

## Do

Use this decision policy:

```txt
local synchronous UI state -> Signals when Angular supports them, otherwise component property or BehaviorSubject
derived synchronous state -> computed when Angular supports it, otherwise getter, memoized value, or RxJS map
HTTP and async orchestration -> RxJS Observable
router params and form valueChanges -> RxJS Observable, optionally converted at the boundary
WebSockets and event streams -> RxJS Observable
shared feature API -> facade contract using Observables or read-only Signals by version and project style
global app state -> store, facade, or explicit state service
```

For Angular 2-15, do not use Signals:

```ts
readonly selectedTab$ = new BehaviorSubject<'active' | 'inactive'>('active');
```

For Angular 16+ where the project accepts Signals:

```ts
readonly selectedTab = signal<'active' | 'inactive'>('active');
readonly hasSelection = computed(() => this.selectedTab() === 'active');
```

Use RxJS for cancellable async flows:

```ts
readonly results$ = this.searchControl.valueChanges.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  switchMap((query) => this.userApi.searchUsers(query)),
);
```

Use interop at clear boundaries, not everywhere:

```ts
readonly user = toSignal(this.user$, { initialValue: null });
```

## Do Not

Avoid global state for trivial local UI state:

```ts
this.store.dispatch(openDropdown());
```

Avoid replacing async RxJS flows with signal effects by default:

```ts
effect(() => {
  this.http.get(`/api/users/${this.userId()}`).subscribe();
});
```

Avoid recommending `resource` or `httpResource` as a stable baseline when the project has not explicitly accepted experimental APIs.

Avoid mixing Signals and Observables in the same feature without explaining ownership and conversion boundaries.

## Review Checklist

- [ ] Angular version supports any Signal API being recommended.
- [ ] State lifetime is classified as local, feature, shared, or global.
- [ ] State synchronicity is classified as synchronous value or asynchronous flow.
- [ ] RxJS is preserved for cancellation, retries, debouncing, streams, and HTTP orchestration.
- [ ] Signals are limited to local synchronous state or readable derived state where appropriate.
- [ ] Interop usage has a clear boundary.
- [ ] Experimental APIs are avoided unless explicitly requested.
- [ ] The feature does not use multiple state models without a policy.

## Expected Output

1. Detect Angular version and existing state style.
2. Classify the state problem by lifetime and synchronicity.
3. Choose Signals, RxJS, a facade, or a store based on the decision policy.
4. Provide compatible code for the detected version.
5. Explain why alternatives were rejected.
