---
id: angular.rxjs.observable-contracts
name: Angular Observable Contracts
description: >
  Designs Angular reactive contracts that expose readonly Observables instead of mutable arrays, public Subjects, writable signals, or copied subscription state.
stack:
  - Angular
  - TypeScript
  - RxJS
category: rxjs
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Observable as contract
  - expose streams
  - public BehaviorSubject
  - readonly Observable
  - mutable state exposure
  - Angular state service
compatibility:
  angular:
    min: "2"
    signalsFrom: "16"
---

# Angular Observable Contracts

## Purpose

Use this skill to expose reactive state safely through readonly Observables. The goal is to prevent external mutation, reduce manual subscription state, and create stable contracts between services, facades, and components.

## When to Use

Use this skill when:

- A service exposes `Subject` or `BehaviorSubject` publicly.
- Components manually copy Observable emissions into arrays or booleans.
- A state service exposes mutable internals.
- A facade needs a stable public contract.
- Multiple consumers compose the same state.
- A shared library needs a version-compatible reactive API.

## Do

Expose readonly Observable contracts:

```ts
@Injectable()
export class UserStateService {
  private readonly usersSubject = new BehaviorSubject<readonly User[]>([]);

  readonly users$: Observable<readonly User[]> =
    this.usersSubject.asObservable();

  setUsers(users: readonly User[]): void {
    this.usersSubject.next(users);
  }
}
```

Expose loading and error state explicitly:

```ts
readonly loading$: Observable<boolean> = this.loadingSubject.asObservable();
readonly error$: Observable<unknown | null> = this.errorSubject.asObservable();
```

Use `async` in templates when the value is only rendered:

```html
<app-user-list [users]="users$ | async" />
```

For Angular 16+ local signal state, expose readonly signals:

```ts
private readonly usersSignal = signal<readonly User[]>([]);
readonly users = this.usersSignal.asReadonly();
```

Keep Observables for async flows that need cancellation, retries, composition, or multiple emissions over time.

Specify the temporal contract as well as the emitted type: when input takes effect, whether duplicate values trigger work, which overlapping response may survive, and whether an error completes the stream or allows another command. Keep empty, loading, and failure states distinguishable when consumers depend on that distinction.

## Do Not

Avoid exposing writable subjects:

```ts
usersSubject = new BehaviorSubject<User[]>([]);
```

Avoid public writable signals from state services:

```ts
readonly users = signal<User[]>([]);
```

Avoid copying stream values into mutable component fields unless imperative integration requires it:

```ts
this.userService.users$.subscribe((users) => {
  this.users = users;
});
```

Avoid exposing API DTO streams directly to reusable UI components when a view model contract would be safer.

## Review Checklist

- [ ] Subjects are private.
- [ ] Public streams are readonly Observables.
- [ ] Writable signals are not exposed from state services.
- [ ] Components use `async` for template-only Observable values when practical.
- [ ] Commands update state through explicit methods.
- [ ] Error and loading states are part of the contract when relevant.
- [ ] DTO, domain, and view model boundaries are clear.
- [ ] Shared contracts remain compatible with target Angular versions.
- [ ] Tests cover emission timing, obsolete work, and post-error behavior where the contract requires them.

## Expected Output

1. Find mutable public reactive state.
2. Replace public subjects with readonly Observable contracts.
3. Preserve update methods as the only mutation path.
4. Keep async flows as Observables unless a Signal is clearly appropriate.
5. Add tests that verify emissions and protect against external mutation.
