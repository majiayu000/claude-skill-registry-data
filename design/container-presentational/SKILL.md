---
id: angular.components.container-presentational
name: Angular Container Presentational Components
description: >
  Splits Angular components into container and presentational responsibilities when it improves data flow, reuse, testability, and UI boundaries.
stack:
  - Angular
  - TypeScript
category: components
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - container presentational
  - smart dumb components
  - split Angular component
  - presentational component fetching data
  - component too large
  - reusable Angular component
compatibility:
  angular:
    min: "2"
    signalInputsFrom: "17"
    recommendedModern: "17+"
---

# Angular Container Presentational Components

## Purpose

Use this skill to separate Angular feature orchestration from reusable UI rendering. The goal is to make components easier to test, reuse, and reason about without splitting simple components unnecessarily.

## When to Use

Use this skill when:

- A component fetches data and renders detailed UI at the same time.
- A table, form, card list, dialog, or widget should be reusable.
- A component injects several services only to pass data into the template.
- A presentational-looking component calls HTTP, global state, navigation, or permissions services.
- Unit tests require many unrelated mocks.
- The same visual component is needed in multiple features.

## Do

Use a container for orchestration:

```txt
users-page.component
  - injects facade or data services
  - loads data
  - handles navigation
  - transforms data for the view
  - passes inputs to UI components
  - handles output events
```

Use a presentational component for rendering:

```txt
user-list.component
  - receives data through inputs
  - emits user actions through outputs
  - renders UI
  - has minimal formatting logic
  - does not know API or global state details
```

For Angular 2+ compatible code:

```ts
@Input() users: readonly UserViewModel[] = [];
@Output() selected = new EventEmitter<UserViewModel>();
```

For modern Angular, use signal inputs only when the project supports them:

```ts
readonly users = input.required<readonly UserViewModel[]>();
readonly selected = output<UserViewModel>();
```

Name outputs as business events:

```ts
@Output() userSelected = new EventEmitter<UserViewModel>();
```

## Do Not

Avoid presentational components that fetch data:

```ts
export class UserListComponent {
  private readonly userApi = inject(UserApiService);
}
```

Avoid splitting components when the split adds ceremony without reuse, testability, or clarity.

Avoid outputs named after implementation details:

```ts
@Output() clicked = new EventEmitter<string>();
```

Avoid putting large business orchestration into a container template.

## Review Checklist

- [ ] The split solves a real complexity, reuse, or testing problem.
- [ ] The container owns data loading, orchestration, and side effects.
- [ ] The presentational component receives data and emits events only.
- [ ] The presentational component does not inject feature API, router, or global state services.
- [ ] Inputs are typed with view models instead of raw API DTOs when appropriate.
- [ ] Outputs describe business intent.
- [ ] Angular version supports any modern APIs used in the proposal.
- [ ] Tests can mock the presentational component or facade simply.

## Expected Output

1. Identify current component responsibilities.
2. Decide whether a split is justified.
3. Propose container and presentational boundaries.
4. Provide compatible input/output examples.
5. Add or recommend tests for event emission and container orchestration.
