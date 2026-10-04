---
id: angular.performance.onpush-change-detection
name: OnPush Change Detection
description: >
  Helps improve Angular rendering performance by applying ChangeDetectionStrategy.OnPush only when component data flow supports it.
stack:
  - Angular
  - TypeScript
category: performance
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - OnPush
  - ChangeDetectionStrategy
  - change detection
  - Angular performance
  - slow rendering
---

# OnPush Change Detection

## Purpose

Use this skill to improve Angular rendering performance by applying `ChangeDetectionStrategy.OnPush` safely and intentionally. The goal is to reduce unnecessary checks without hiding state mutation bugs or breaking view updates.
This skill is complementary to `change-detection-optimization`; keep it focused on explicit OnPush adoption and mutation safety.

## When to Use

Use this skill when:

- A component renders frequently without visible data changes.
- The component receives most data through inputs, observables, or signals.
- A performance task mentions change detection, slow rendering, or heavy templates.
- A component can be updated through immutable state changes.
- The current code already has tests or clear rendering behavior to verify.
- The project can prove the state flow before introducing OnPush.

## Do

Prefer `OnPush` when the component has explicit data flow and immutable updates:

```ts
@Component({
  selector: "app-user-card",
  templateUrl: "./user-card.component.html",
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserCardComponent {
  @Input({ required: true }) user!: UserViewModel;
}
```

Prefer replacing object mutation with new references:

```ts
this.user = {
  ...this.user,
  displayName: nextDisplayName,
};
```

For asynchronous data, prefer template subscriptions with `async` or state exposed through signals:

```html
<app-user-card [user]="user$ | async" />
```

```ts
readonly fullName = computed(() => {
  const user = this.user();
  return `${user.firstName} ${user.lastName}`;
});
```

Use `markForCheck` only when an external callback updates state outside Angular's normal path and the component still needs the view refreshed.

## Do Not

Avoid applying `OnPush` blindly:

```ts
@Component({
  selector: "app-user-editor",
  templateUrl: "./user-editor.component.html",
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserEditorComponent {
  @Input() user!: User;

  rename(value: string): void {
    this.user.name = value;
  }
}
```

Avoid using `OnPush` as a cosmetic change when the component relies on hidden side effects, mutable shared objects, or untracked state changes.

Avoid turning unrelated services, global stores, or routing state into an OnPush justification if the real issue is elsewhere.

## Review Checklist

- [ ] `OnPush` is applied only where the component data flow is explicit.
- [ ] Inputs are not mutated directly.
- [ ] Arrays and objects are replaced immutably when their visible state changes.
- [ ] Observables are consumed with `async`, signals, or explicit lifecycle-safe subscriptions.
- [ ] Signals use `set`, `update`, or computed values instead of hidden mutation.
- [ ] Forms, overlays, timers, and imperative callbacks still update the view correctly.
- [ ] Tests or manual verification cover the affected rendering path.

## Expected Output

1. Inspect the component data flow before adding `OnPush`.
2. Identify mutation or side-effect risks.
3. Apply the smallest safe change needed for rendering performance.
4. Preserve existing behavior and avoid broad architecture rewrites.
5. Add or update tests when rendering behavior changes.
