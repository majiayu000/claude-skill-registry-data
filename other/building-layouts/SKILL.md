---
name: flutter-building-layouts
description: Builds Flutter layouts using the constraint system and layout widgets. Use when creating or refining the UI structure of a Flutter application.
tags: [flutter, layout, constraints, responsive, adaptive, row, column, stack]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Layouts

## Contents
- [Core Layout Principles](#core-layout-principles)
- [Structural Widgets](#structural-widgets)
- [Adaptive and Responsive Design](#adaptive-and-responsive-design)
- [Workflow: Implementing a Complex Layout](#workflow-implementing-a-complex-layout)
- [Examples](#examples)

## Core Layout Principles

Master the fundamental Flutter layout rule: **Constraints go down. Sizes go up. Parent sets position.**

- **Pass Constraints Down:** Parent Widget passes constraints (min/max width and height) to children. A Widget cannot choose its own size independently of its parent's constraints.
- **Pass Sizes Up:** Child Widget calculates its desired size within the given constraints and passes it back up to the parent.
- **Set Position via Parent:** The parent Widget defines x/y coordinates of children. Children do not know their own position on screen.
- **Avoid Unbounded Constraints:** Never pass unbounded constraints (`double.infinity`) in the cross-axis of a flex box (`Row`/`Column`) or within scrollable regions (`ListView`). This causes render exceptions.

## Structural Widgets

Select the appropriate structural Widget based on the required arrangement:

| Widget | Use When |
|---|---|
| `Row` | Horizontal linear layout |
| `Column` | Vertical linear layout |
| `Expanded` | Force fill available space in `Row`/`Column` |
| `Flexible` | Allow sizing up to available space |
| `Stack` | Widgets must overlap on Z-axis |
| `Positioned` | Anchor children to specific edges of `Stack` |
| `SizedBox` | Enforce strict width/height constraints |
| `Container` | Apply padding, margins, borders, background |
| `Wrap` | Overflow items to the next line automatically |
| `LayoutBuilder` | Build conditionally based on parent constraints |

## Adaptive and Responsive Design

- **Responsive (fitting UI into available space):** Use `LayoutBuilder`, `Expanded`, and `Flexible` to dynamically adjust size and placement based on parent constraints.
- **Adaptive (adjusting UI usability per form factor):** Use conditional rendering to swap entire layout structures. E.g., bottom navigation on mobile, side navigation rail on tablets/desktop.

### Breakpoint Strategy

```dart
// Standard breakpoints
static const double compact = 600;   // Phone
static const double medium = 840;    // Tablet
static const double expanded = 1200; // Desktop
```

## Workflow: Implementing a Complex Layout

- [ ] **Phase 1: Visual Deconstruction**
  - [ ] Break down the target UI into a hierarchy of rows, columns, and grids.
  - [ ] Identify overlapping elements (requiring `Stack`).
  - [ ] Identify scrolling regions (requiring `ListView` or `SingleChildScrollView`).
- [ ] **Phase 2: Constraint Planning**
  - [ ] Determine which Widgets need tight constraints (fixed size) vs. loose constraints (flexible).
  - [ ] Identify unbounded constraint risks (e.g., a `ListView` inside a `Column`).
- [ ] **Phase 3: Implementation**
  - [ ] Build from the outside in, starting with `Scaffold` and primary structural Widgets.
  - [ ] Extract deeply nested layout sections into separate widgets for readability.
- [ ] **Phase 4: Validation**
  - [ ] Run on target devices/simulators.
  - [ ] Enable "Debug Paint" in Flutter Inspector to visualize render boxes.
  - [ ] Check for yellow/black striped overflow warnings.
  - [ ] If overflow occurs: wrap in `Expanded` (inside flex box) or wrap parent in scrollable Widget.

## Examples

### Resolving Unbounded Constraints

```dart
// ❌ BAD: Throws unbounded height exception
Column(
  children: [
    Text('Header'),
    ListView(
      children: [/* items */],
    ),
  ],
)

// ✅ GOOD: ListView is constrained to remaining space
Column(
  children: [
    Text('Header'),
    Expanded(
      child: ListView(
        children: [/* items */],
      ),
    ),
  ],
)
```

### Responsive Layout with LayoutBuilder

```dart
Widget buildAdaptiveLayout(BuildContext context) {
  return LayoutBuilder(
    builder: (context, constraints) {
      if (constraints.maxWidth > 600) {
        // Tablet/Desktop: Side-by-side layout
        return Row(
          children: [
            SizedBox(width: 250, child: SidebarWidget()),
            Expanded(child: MainContentWidget()),
          ],
        );
      } else {
        // Mobile: Stacked layout with navigation
        return Column(
          children: [
            Expanded(child: MainContentWidget()),
            BottomNavigationBarWidget(),
          ],
        );
      }
    },
  );
}
```

### Scrollable Form Layout

```dart
// Common pattern for forms that may exceed screen height
Scaffold(
  body: SafeArea(
    child: SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Form fields
          const SizedBox(height: 16),
          // More fields...
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: _submit,
            child: const Text('Submit'),
          ),
        ],
      ),
    ),
  ),
)
```

### Stack with Positioned Children

```dart
Stack(
  children: [
    // Background image
    Positioned.fill(
      child: Image.asset('assets/bg.png', fit: BoxFit.cover),
    ),
    // Overlay content
    Positioned(
      bottom: 16,
      left: 16,
      right: 16,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Text('Overlay Content'),
        ),
      ),
    ),
  ],
)
```

## Anti-patterns

- ❌ Placing `ListView` directly inside `Column` without `Expanded` (unbounded height)
- ❌ Nesting `Row` inside `Row` without `Expanded`/`Flexible` (unbounded width)
- ❌ Using `Container` when `SizedBox`, `Padding`, or `DecoratedBox` would suffice
- ❌ Hardcoding pixel sizes instead of using responsive constraints
- ❌ Using `MediaQuery.of(context).size` when `LayoutBuilder` is more appropriate

## Resources

- https://docs.flutter.dev/ui/layout
- https://docs.flutter.dev/ui/layout/constraints
- https://docs.flutter.dev/ui/adaptive-responsive
- https://docs.flutter.dev/ui/layout/building-adaptive-apps
- https://docs.flutter.dev/cookbook/design/responsive
- https://api.flutter.dev/flutter/widgets/LayoutBuilder-class.html
