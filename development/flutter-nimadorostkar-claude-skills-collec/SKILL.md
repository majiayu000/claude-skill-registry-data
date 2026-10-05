---
name: flutter
description: Use when building Flutter applications. Covers widget composition, state management, build-method performance, platform channels, and the rendering behavior behind most Flutter jank.
metadata:
  category: mobile
  version: 1.0.0
  tags: [flutter, dart, widgets, state-management, performance]
---

# Flutter

## Purpose

Build Flutter applications whose widget tree rebuilds only where it must. Flutter's performance model is simple and unforgiving: a `setState` at the top of the tree rebuilds everything below it.

## When to Use

- Building or reviewing a Flutter application.
- Choosing and applying a state-management approach.
- Diagnosing jank or excessive rebuilds.
- Integrating with platform-native code.

## Capabilities

- Widget composition and the `StatelessWidget`/`StatefulWidget` boundary.
- State management with Riverpod, Bloc, or Provider — and when plain state suffices.
- Build-method optimization: `const` constructors, selective rebuilds, keys.
- Async: `Future`, `Stream`, `FutureBuilder`, and their failure states.
- Platform channels for native functionality.

## Inputs

- The feature set and target platforms.
- The current state-management approach, if any.
- The jank or rebuild symptom, if debugging.

## Outputs

- A widget tree where rebuilds are scoped to what changed.
- State that is testable without a widget tree.
- Async UI that handles loading, error, and empty explicitly.

## Workflow

1. **Compose small widgets** — A 300-line `build` method rebuilds as one unit. Extracting subtrees into widgets is the primary performance tool in Flutter, not a style preference.
2. **Mark everything possible `const`** — A `const` widget is never rebuilt. This is the cheapest optimization available and most codebases leave it on the table.
3. **Scope the rebuild** — `Consumer`, `Selector`, or a Riverpod provider that watches one field. `setState` in a parent rebuilds every child that is not `const`.
4. **Handle all three async states** — Loading, error, and data. `FutureBuilder` without an error branch shows a spinner forever when the request fails.
5. **Profile in profile mode** — Debug mode is meaningfully slower and will mislead you in both directions. Use the DevTools timeline on a real device.

## Best Practices

- `const` constructors are the highest-leverage change in most Flutter codebases. Enable `prefer_const_constructors` in the linter and fix every warning.
- Never build a widget inside a `build` method as a function call (`Widget _buildHeader()`). It defeats the element-tree diffing entirely. Extract a real widget class.
- Keys matter when reordering or removing items from a list of stateful widgets. Without them, state attaches to the wrong item.
- Business logic does not belong in a widget. If it cannot be tested without pumping a widget tree, it is in the wrong place.
- `ListView.builder`, not `ListView(children: [...])`, for anything that could be long. The latter builds every child immediately.
- An `AnimationController` without a `dispose` is a leak that ticks forever.

## Examples

**Scoped rebuild versus a rebuild of everything:**

```dart
// Costly: setState here rebuilds the whole screen, including the static header
// and the entire list, on every counter tick.
class _DashboardState extends State<Dashboard> {
  int _count = 0;

  @override
  Widget build(BuildContext context) => Column(
    children: [
      const DashboardHeader(),         // const: spared, correctly
      OrderList(orders: widget.orders), // not const: rebuilt every tick
      Text('$_count'),
      ElevatedButton(onPressed: () => setState(() => _count++), child: const Text('+')),
    ],
  );
}

// Better: only the Text listening to the counter rebuilds.
class Dashboard extends ConsumerWidget {
  const Dashboard({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) => Column(
    children: [
      const DashboardHeader(),
      const OrderList(),
      Consumer(builder: (_, ref, __) => Text('${ref.watch(counterProvider)}')),
      ElevatedButton(
        onPressed: () => ref.read(counterProvider.notifier).increment(),
        child: const Text('+'),
      ),
    ],
  );
}
```

**Async with every state handled:**

```dart
switch (ref.watch(ordersProvider)) {
  AsyncData(:final value) when value.isEmpty => const EmptyState(),
  AsyncData(:final value) => OrderList(orders: value),
  AsyncError(:final error) => ErrorState(error: error, onRetry: _retry),
  _ => const LoadingSkeleton(),
}
```

## Notes

- Extracting a subtree into a `const` widget removes it from the rebuild path entirely — the framework short-circuits on identity. This is why "just extract widgets" is genuine performance advice in Flutter and not merely tidiness.
- `RepaintBoundary` isolates a subtree's painting. It helps when a small animated element sits inside an expensive static one, and hurts if applied indiscriminately.
- Impeller replaced Skia as the default renderer on iOS (and now Android), which eliminates the shader-compilation jank that used to affect first-run animations.
