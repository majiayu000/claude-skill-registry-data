---
id: angular.performance.pipes-and-memoization
name: Angular Pipes and Memoization Optimization
description: >
  Optimizes Angular data transformations by choosing between pure pipes, computed signals, memoization, and precomputed view models.
stack:
  - Angular
  - TypeScript
category: performance
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - pure pipe
  - impure pipe
  - memoization
  - computed values
  - repeated transformation
  - view model mapping
compatibility:
  angular:
    min: "2"
    signalsFrom: "16"
---

# Angular Pipes and Memoization Optimization

## Purpose

Use this skill to reduce repeated data transformation cost by choosing the right tool: pure pipe, computed signal, memoized function, or precomputed view model.

## Compatibility

Use the compatible variant:

- Angular 2+: pure pipes and precomputed view models are available.
- Angular 16+: computed signals are available when the project uses signals.
- All versions: impure pipes require explicit justification because they can run frequently.

Do not assume a pipe is always faster. The decision depends on purity, input stability, calculation cost, reuse, and readability.

## When to Use

Use this skill when:

- A transformation repeats across templates.
- A component repeatedly filters, sorts, maps, formats, or aggregates data.
- A pipe is impure or suspected of running too often.
- A computed signal or memoized value could replace repeated calculation.
- The code needs a clear separation between raw DTOs and view models.

## Do

Use a pure pipe for deterministic reusable formatting:

```ts
@Pipe({
  name: "totalPrice",
  pure: true,
})
export class TotalPricePipe implements PipeTransform {
  transform(items: readonly Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

Use computed signals for local reactive derivation when supported:

```ts
readonly filteredItems = computed(() =>
  this.items().filter((item) => item.active),
);
```

Use a view model mapper for API data:

```ts
this.viewModel = response.items.map((item) => ({
  id: item.id,
  label: `${item.code} - ${item.name}`,
}));
```

## Do Not

Avoid impure pipes without strong reason:

```ts
@Pipe({
  name: "expensiveFilter",
  pure: false,
})
export class ExpensiveFilterPipe implements PipeTransform {}
```

Avoid HTTP calls, service mutations, or side effects in pipes.

Avoid memoization when the cache invalidation rules are unclear or memory growth is unbounded.

## Review Checklist

- [ ] The transformation is pure or side effects are removed.
- [ ] The transformation depends only on explicit inputs.
- [ ] The calculation cost is high enough to justify optimization.
- [ ] A pure pipe is used for reusable view formatting.
- [ ] A computed signal is used only when signals are supported and already fit the state model.
- [ ] A view model is used when mapping API data into UI shape.
- [ ] Impure pipes are avoided or strongly justified.
- [ ] Memoization has clear cache keys and bounded lifetime.

## Expected Output

1. Classify the transformation by purity, cost, and reuse.
2. Select pure pipe, computed, memoization, or view model mapping.
3. Avoid introducing side effects into rendering paths.
4. Keep the implementation compatible with the Angular version.
5. Add or update tests for transformation behavior when needed.
