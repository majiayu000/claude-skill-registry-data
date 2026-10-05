---
name: angular
description: Use when building Angular applications. Covers standalone components, signals, RxJS discipline, change detection, dependency injection, and the patterns that keep large Angular codebases fast.
metadata:
  category: frontend
  version: 1.0.0
  tags: [angular, signals, rxjs, change-detection, typescript]
---

# Angular

## Purpose

Build modern Angular — standalone components, signals for state, RxJS only where streams genuinely help — and keep change detection from becoming the bottleneck it becomes by default.

## When to Use

- Building or reviewing an Angular 17+ application.
- Migrating from NgModules to standalone components, or from RxJS state to signals.
- Diagnosing performance problems caused by change detection.
- Preventing subscription leaks.

## Capabilities

- Standalone components, directives, and functional route guards.
- Signals: `signal`, `computed`, `effect`, and `toSignal` interop with RxJS.
- Change detection: `OnPush`, zoneless, and what triggers a check.
- RxJS operators for the cases where a stream is the right model.
- Dependency injection with `inject()` and provider scoping.

## Inputs

- The component or feature, and its data sources.
- Angular version, and whether zone.js is still in use.
- The performance symptom, if any.

## Outputs

- Standalone components with `OnPush` change detection.
- State in signals; asynchronous events in observables, converted at the boundary.
- No manual subscriptions without a matching teardown.

## Workflow

1. **Go standalone** — NgModules are legacy. Standalone components with explicit `imports` make the dependency graph readable.
2. **Use signals for state** — Synchronous, glitch-free, and integrated with change detection. Reserve RxJS for genuine streams: HTTP, WebSockets, user-input debouncing.
3. **Set `OnPush` everywhere** — Default change detection re-checks the entire component tree on every event. `OnPush` limits it to inputs that actually changed.
4. **Convert at the boundary** — `toSignal(this.http.get(...))` brings an observable into the signal world. Do not maintain state in a `BehaviorSubject` and mirror it into a signal.
5. **Never subscribe manually without teardown** — `takeUntilDestroyed()` or the `async` pipe. A subscription without an unsubscribe is a leak with a component attached.

## Best Practices

- Do not call methods from the template (`{{ getTotal() }}`). They run on every change-detection cycle. Use a `computed` signal.
- `subscribe()` inside `subscribe()` is a nested-subscription bug. Flatten with `switchMap`, `mergeMap`, or `concatMap` — chosen for the cancellation semantics you actually want.
- `switchMap` cancels the previous request, which is correct for typeahead and wrong for saving a form. Pick deliberately.
- Provide services at the component level when the state is component-scoped; `providedIn: 'root'` makes it a singleton shared by every consumer.
- `effect()` is for side effects only. Writing to a signal inside an effect creates a loop that Angular will warn about, and it usually means you wanted `computed`.
- Zoneless change detection (Angular 18+) removes zone.js entirely and requires signals throughout. It is worth targeting for new applications.

## Examples

**Signal state with an RxJS boundary:**

```typescript
@Component({
  selector: "app-order-list",
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [OrderCardComponent],
  template: `
    @if (orders.isLoading()) {
      <app-skeleton />
    } @else {
      @for (order of visibleOrders(); track order.id) {
        <app-order-card [order]="order" />
      } @empty {
        <p>No orders match this filter.</p>
      }
    }
  `,
})
export class OrderListComponent {
  private readonly api = inject(OrderApi);

  readonly status = signal<OrderStatus>("open");
  readonly orders = rxResource({
    request: () => ({ status: this.status() }),
    loader: ({ request }) => this.api.list(request.status),
  });

  // Derived state, recomputed only when its dependencies change.
  readonly visibleOrders = computed(() =>
    (this.orders.value() ?? []).filter((o) => !o.archived),
  );
}
```

**Subscription teardown without ceremony:**

```typescript
export class SearchComponent {
  private readonly destroyRef = inject(DestroyRef);

  constructor() {
    this.searchControl.valueChanges
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
        switchMap((q) => this.api.search(q)),   // cancels the in-flight request
        takeUntilDestroyed(this.destroyRef),    // unsubscribes on destroy
      )
      .subscribe((results) => this.results.set(results));
  }
}
```

## Notes

- The new control-flow syntax (`@if`, `@for`, `@switch`) is not sugar — it compiles to more efficient code than `*ngIf` and `*ngFor`, and `track` is mandatory in `@for`, which eliminates a whole class of list-diffing bugs.
- `OnPush` with mutable objects will not update: it compares references. Either treat inputs as immutable or use signals, which notify explicitly.
- A `computed` signal that reads another `computed` is fine and does not recompute unnecessarily — the graph is lazy and memoized.
