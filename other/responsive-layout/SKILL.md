---
name: responsive-layout
description: Builds responsive and adaptive Flutter user interfaces across mobile, tablet, desktop, and web form factors using LayoutBuilder, MediaQuery, and adaptive breakpoints.
version: 1.0.0
---

# Responsive Layout in Flutter

Techniques for building cross-platform Flutter layouts that adapt to phones, tablets, foldables, and desktops.

## Breakpoint System

```dart
class ResponsiveBreakpoints {
  static const double mobile = 600;
  static const double tablet = 900;
  static const double desktop = 1200;

  static bool isMobile(BuildContext context) =>
      MediaQuery.sizeOf(context).width < mobile;

  static bool isTablet(BuildContext context) =>
      MediaQuery.sizeOf(context).width >= mobile &&
      MediaQuery.sizeOf(context).width < desktop;

  static bool isDesktop(BuildContext context) =>
      MediaQuery.sizeOf(context).width >= desktop;
}
```

## Pattern 1: `LayoutBuilder` for Component Adaptability

Use `LayoutBuilder` when a component should adapt based on its parent container's width, rather than the entire screen:

```dart
class AdaptiveCardList extends StatelessWidget {
  const AdaptiveCardList({super.key});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth > 800) {
          // Grid layout on wide containers
          return GridView.builder(
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 3,
              childAspectRatio: 1.5,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
            ),
            itemCount: 9,
            itemBuilder: (context, index) => CardTile(index),
          );
        } else {
          // Vertical list on narrow containers
          return ListView.builder(
            itemCount: 9,
            itemBuilder: (context, index) => CardTile(index),
          );
        }
      },
    );
  }
}
```

## Pattern 2: Master-Detail Layout for Tablets/Desktop

```dart
Widget build(BuildContext context) {
  final isWide = ResponsiveBreakpoints.isTablet(context) || ResponsiveBreakpoints.isDesktop(context);

  if (isWide) {
    return Row(
      children: [
        const SizedBox(width: 320, child: ItemsListPane()),
        const VerticalDivider(width: 1),
        const Expanded(child: ItemDetailPane()),
      ],
    );
  }

  return const ItemsListPane(); // Mobile pushes to detail route
}
```

## Performance Note: `MediaQuery.sizeOf(context)`
In Flutter 3.10+, use `MediaQuery.sizeOf(context)` instead of `MediaQuery.of(context).size`. `sizeOf` only triggers re-renders when the size changes, preventing rebuilds on orientation/insets changes.
