---
id: angular.performance.rxjs-performance
name: Angular RxJS Performance
description: >
  Reviews Angular RxJS usage for leaks, duplicated requests, nested subscriptions, unnecessary streams, and operator choices that affect performance.
stack:
  - Angular
  - TypeScript
  - RxJS
category: performance
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - RxJS performance
  - duplicated HTTP requests
  - nested subscriptions
  - takeUntilDestroyed
  - shareReplay
  - debounceTime
compatibility:
  angular:
    min: "2"
    rxjsInteropFrom: "16"
    takeUntilDestroyedStableFrom: "19"
---

# Angular RxJS Performance

## Purpose

Use this skill to optimize Angular RxJS flows by removing nested subscriptions, preventing leaks, avoiding duplicated work, and selecting operators based on cancellation, ordering, and concurrency semantics.

## Compatibility

Use the compatible variant:

- Angular 2-15: use `async`, `takeUntil`, `Subject`, and `ngOnDestroy` where manual subscriptions are necessary.
- Angular 16-18: use `takeUntilDestroyed` only when project dependencies support it.
- Angular 19+: prefer `takeUntilDestroyed` for lifecycle-bound manual subscriptions.
- All versions: prefer `async` when the observable value is used only in the template.

When duplicated HTTP requests or cacheable API reads are the main issue, keep the fix localized:

- deduplicate with shared streams only when multiple subscribers truly need the same in-flight value.
- use `shareReplay` only with explicit lifecycle semantics and bounded cache rules.
- avoid caching sensitive or fast-changing data unless invalidation is clear.
- prefer a facade or service boundary for controlled caching instead of scattering `subscribe` calls across components.

## When to Use

Use this skill when:

- `subscribe` appears inside another `subscribe`.
- HTTP calls repeat unexpectedly.
- Input changes trigger too many requests.
- Streams are duplicated across template and component code.
- Manual subscriptions have unclear cleanup.
- A form search, dashboard stream, or route-driven request feels slow or unstable.

## Do

Use `switchMap` for cancellable dependent requests:

```ts
readonly orders$ = this.userService.getUser().pipe(
  switchMap((user) => this.orderService.getOrders(user.id)),
);
```

Use throttling or debouncing for high-frequency inputs:

```ts
readonly results$ = this.searchControl.valueChanges.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  switchMap((query) => this.searchService.search(query)),
);
```

Define when a search becomes obsolete before choosing the operator order. Here, `switchMap` sees only debounced, distinct terms: the old request remains active during the 300 ms wait. If new input must invalidate it immediately, move the cancellation boundary to the raw-input stream and delay the new request inside that boundary. Define whether clearing input also clears results immediately; do not change that behavior as an incidental optimization.

Keep recoverable request errors inside the inner request when later searches must continue. Test the fallback and a later success on the same subscription. Verify the 299/300 ms boundary, a second input resetting the wait, normalized arguments, duplicate suppression, stale response rejection, and request teardown. A call-count assertion alone does not prove a race is fixed.

Use lifecycle-safe cleanup for imperative subscriptions:

```ts
this.form.valueChanges
  .pipe(takeUntilDestroyed(this.destroyRef))
  .subscribe((value) => this.formValue.set(value));
```

Use `shareReplay` only when sharing a source is intentional and lifecycle semantics are understood.
Prefer `shareReplay({ bufferSize: 1, refCount: true })` or an equivalent project-safe variant when sharing a cold stream across subscribers.
Do not use `shareReplay` as an accidental permanent cache.

## Do Not

Avoid nested subscriptions:

```ts
this.userService.getUser().subscribe((user) => {
  this.orderService.getOrders(user.id).subscribe((orders) => {
    this.orders = orders;
  });
});
```

Avoid unbounded manual subscriptions:

```ts
this.form.valueChanges.subscribe((value) => {
  this.search(value);
});
```

Avoid using `Subject` as an improvised global state layer when a simpler observable, signal, or scoped state service would be clearer.

## Review Checklist

- [ ] Nested subscriptions are removed.
- [ ] Manual subscriptions are justified.
- [ ] Template-only values use `async` where practical.
- [ ] High-frequency streams use `debounceTime`, `throttleTime`, or `distinctUntilChanged` when appropriate.
- [ ] `switchMap`, `concatMap`, `mergeMap`, and `exhaustMap` are selected by semantics.
- [ ] HTTP duplication is checked before adding `shareReplay`.
- [ ] Cache invalidation is defined when data is reused.
- [ ] Sensitive or rapidly changing data is not cached by default.
- [ ] Subscription cleanup matches the Angular version.
- [ ] Error, loading, and empty states remain explicit.
- [ ] Cancellation timing and empty-input behavior match the intended contract.
- [ ] Tests distinguish the intended concurrency strategy and verify recovery after an error.

## Expected Output

1. Identify stream-level performance and lifecycle risks.
2. Choose operators based on cancellation, ordering, and concurrency.
3. Replace nested subscriptions with composed streams.
4. Apply lifecycle cleanup compatible with the Angular version.
5. Explain request duplication, caching, and error-handling risks.
