---
id: angular.architecture.facade-pattern
name: Angular Facade Pattern
description: >
  Introduces or reviews Angular facades that provide a focused feature API over data access, state, permissions, navigation, and orchestration.
stack:
  - Angular
  - TypeScript
  - RxJS
category: architecture
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - facade pattern
  - Angular facade
  - feature facade
  - component injects many services
  - simplify Angular tests
  - feature API
compatibility:
  angular:
    min: "2"
    signalsFrom: "16"
    recommendedModern: "17+"
---

# Angular Facade Pattern

## Purpose

Use this skill to introduce a focused feature API between components and lower-level services. The goal is to reduce coupling, simplify tests, and keep orchestration out of UI components.

## When to Use

Use this skill when:

- A component injects many services from different concerns.
- Components duplicate loading, error, permission, and mapping logic.
- Tests require excessive mocks for one feature component.
- Several components need the same feature-level operations.
- Feature state and API calls need a stable public contract.
- A module, route, or microfrontend boundary needs an explicit interface.

## Do

Expose a narrow feature contract:

```ts
@Injectable()
export class UserFacade {
  readonly users$ = this.userState.users$;
  readonly loading$ = this.userState.loading$;
  readonly error$ = this.userState.error$;

  constructor(
    private readonly userApi: UserApiService,
    private readonly userState: UserStateService,
  ) {}

  loadUsers(): void {
    this.userState.setLoading(true);

    this.userApi
      .getUsers()
      .pipe(finalize(() => this.userState.setLoading(false)))
      .subscribe({
        next: (users) => this.userState.setUsers(users),
        error: (error) => this.userState.setError(error),
      });
  }
}
```

Keep the component simple:

```ts
readonly users$ = this.userFacade.users$;
readonly loading$ = this.userFacade.loading$;

ngOnInit(): void {
  this.userFacade.loadUsers();
}
```

Use a structure that reveals boundaries:

```txt
users/
  data-access/
    user-api.service.ts
    user-state.service.ts
  facade/
    user.facade.ts
  feature/
    users-page.component.ts
  ui/
    user-list.component.ts
  models/
    user.model.ts
```

## Do Not

Avoid a facade that becomes a god service:

```txt
UserFacade
  - users
  - auth
  - payments
  - notifications
  - export
  - analytics
```

Avoid adding a facade for a trivial component if it only forwards one method and adds no stable boundary.

Avoid hiding bad domain boundaries behind a nicer class name.

Avoid mixing UI formatting, API calls, permissions, and unrelated business domains in the same facade.

## Review Checklist

- [ ] The facade owns one feature or bounded context.
- [ ] Components depend on the facade instead of many low-level services.
- [ ] Public facade properties are readonly.
- [ ] Commands are named by user or feature intent.
- [ ] Data access and state services remain separate when complexity justifies it.
- [ ] The facade simplifies tests with fewer mocks.
- [ ] The facade does not become a dumping ground.
- [ ] Signals are only exposed when the Angular version and project style support them.

## Expected Output

1. Identify coupling between components and low-level services.
2. Decide whether a facade creates real value.
3. Propose a bounded facade API.
4. Move orchestration behind the facade incrementally.
5. Provide testing guidance using facade mocks.
