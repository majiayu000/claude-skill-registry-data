---
id: angular.rxjs.avoid-nested-subscriptions
name: Avoid Nested Subscriptions
description: >
  Replaces nested RxJS subscriptions with composable operators and lifecycle-safe subscription handling in Angular code.
stack:
  - Angular
  - TypeScript
  - RxJS
category: rxjs
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - nested subscribe
  - subscription inside subscription
  - switchMap
  - combineLatest
  - takeUntilDestroyed
  - RxJS lifecycle
---

# Avoid Nested Subscriptions

## Purpose

Use this skill to replace subscription pyramids with clear RxJS composition. The goal is to prevent leaks, race conditions, duplicated requests, hidden ordering bugs, and hard-to-test asynchronous flows.

## When to Use

Use this skill when:

- A `subscribe` call appears inside another `subscribe`.
- A request depends on the result of a previous observable.
- Multiple observable values must be combined before updating state.
- The code manually stores many subscriptions.
- Component lifecycle cleanup is missing or unclear.
- The task mentions RxJS leaks, duplicated API calls, or async race conditions.

## Do

Use `switchMap` when a new source value should cancel the previous inner operation:

```ts
readonly userDetails$ = this.route.paramMap.pipe(
  map((params) => params.get('id')),
  filter((id): id is string => id !== null),
  switchMap((id) => this.usersService.getUserDetails(id)),
);
```

Use `combineLatest` when multiple ongoing sources define the current view state:

```ts
readonly viewModel$ = combineLatest([
  this.user$,
  this.permissions$,
]).pipe(
  map(([user, permissions]) => ({ user, permissions })),
);
```

Use `forkJoin` when independent one-time operations must complete together:

```ts
forkJoin({
  profile: this.usersService.getProfile(userId),
  settings: this.settingsService.getSettings(userId),
}).subscribe(({ profile, settings }) => {
  this.profile.set(profile);
  this.settings.set(settings);
});
```

Use `concatMap` when operations must run sequentially and order matters:

```ts
saveClicks
  .pipe(concatMap((payload) => this.ordersService.save(payload)))
  .subscribe();
```

For search or route changes, verify which source emission reaches `switchMap`. An upstream debounce or filter can delay or prevent cancellation. In a search test, emit an old response after the replacement request starts and assert that it is ignored; also assert teardown when cancellation itself is required. For write operations, do not choose `switchMap` merely to remove nesting if cancellation would lose intended work.

If a failed inner request should not stop future input, handle its error inside the flattening operator. Test a failure followed by success through the same subscription, rather than recreating the stream after the error.

In Angular components, prefer `async` in templates or use `takeUntilDestroyed` for imperative subscriptions:

```ts
this.form.valueChanges
  .pipe(takeUntilDestroyed(this.destroyRef))
  .subscribe((value) => this.formValue.set(value));
```

## Do Not

Avoid nested subscriptions:

```ts
this.route.paramMap.subscribe((params) => {
  const id = params.get("id");

  this.usersService.getUserDetails(id).subscribe((user) => {
    this.permissionsService
      .getPermissions(user.role)
      .subscribe((permissions) => {
        this.viewModel = { user, permissions };
      });
  });
});
```

Avoid ignoring lifecycle cleanup for long-lived streams:

```ts
this.form.valueChanges.subscribe((value) => {
  this.formValue = value;
});
```

## Review Checklist

- [ ] No `subscribe` call is nested inside another `subscribe`.
- [ ] `switchMap` is used for cancelable dependent work.
- [ ] `concatMap` is used for ordered sequential work.
- [ ] `mergeMap` is used only when concurrent inner work is intended.
- [ ] `combineLatest` is used for ongoing combined state.
- [ ] `forkJoin` is used for one-time parallel completion.
- [ ] Component subscriptions use `async` or `takeUntilDestroyed`.
- [ ] Error handling remains explicit after the refactor.
- [ ] Cancellation, ordering, and continued operation after errors are tested at the public boundary.

## Expected Output

1. Identify nested subscriptions and lifecycle risks.
2. Determine the correct RxJS operator based on cancellation, ordering, and combination semantics.
3. Refactor the observable chain without changing behavior.
4. Preserve explicit error and loading handling.
5. Add or update tests when async behavior changes.
