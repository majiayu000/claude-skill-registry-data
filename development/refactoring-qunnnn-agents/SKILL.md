---
name: flutter-refactor
description: Guidelines for refactoring Flutter widgets and logic to improve maintainability and readability.
tags: [flutter, refactor, clean-code, widgets, architecture]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Refactoring Skill

## Context

Use this skill when refactoring existing Flutter code or when building new features to ensure high code quality. The focus is on keeping widgets small and decomposing complex logic.

## Core Principles

### 1. Widget Size Limit (~80 Lines)
- **Limit**: Aim for a maximum of **80 lines** per widget class (including its `build` method).
- **Rationale**: Smaller widgets are easier to test, debug, and reuse.
- **Action**: If a widget exceeds this limit, identify logical UI blocks and extract them into separate widgets.

### 2. Atomic Widget Extraction (Files)
- **Separate Files**: Do not keep multiple widget classes in the same file if they are complex.
- **Organization**:
    - Extract sub-widgets into a `widgets/` directory relative to the page/feature.
    - Use descriptive names (e.g., `AppointmentCard`, `MedicineListTile`).
    - Use barrel files (`index.dart`) to export widgets for cleaner imports.
- **Private Widgets**: Only keep `_PrivateWidget` in the same file if it is extremely simple (< 20 lines) and highly specific to the parent. Otherwise, extract it.

### 3. Logic Decomposition Pattern
Move logic out of the `build` method and the widget class itself as much as possible.

#### A. State Management (Cubits/Blocs/Providers)
- **Delegate**: All business logic, API calls, and complex state transitions must be handled by a state manager (e.g., Cubit, Bloc, or Notifier).
- **Clean build()**: The `build` method should be a pure mapping of state to UI.

#### B. UI Helper Methods vs. Widgets
- **Avoid Helper Methods**: Avoid `Widget _buildHeader() { ... }` methods within the state class. They don't benefit from Flutter's build optimizations.
- **Prefer Widgets**: Extract them into `StatelessWidget` classes.

#### C. Logic Mixins & Extensions
- **Mixins**: Use mixins for shared UI logic (e.g., form validation, scroll handling).
- **Extensions**: Use extensions for data formatting (e.g., `DateTimeX.toHumanReadable()`).

#### D. Controller Pattern
- For complex UI interactions (like custom animations or sophisticated forms), use a dedicated `Controller` class to encapsulate the imperative logic.

## Examples

### Before Refactor (Monolithic)
```dart
// 200+ lines in one file
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Complex Header (50 lines)
          Container(...), 
          // Complex List (100 lines)
          ListView.builder(...),
          // Complex Footer (50 lines)
          ElevatedButton(...),
        ],
      ),
    );
  }
}
```

### After Refactor (Decomposed)
```text
lib/feature/
├── pages/
│   └── my_page.dart (Scaffold + layout only)
└── widgets/
    ├── my_header.dart
    ├── my_list.dart
    └── my_footer.dart
```

```dart
// my_page.dart (Clean and readable)
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Column(
        children: [
          MyHeader(),
          Expanded(child: MyList()),
          MyFooter(),
        ],
      ),
    );
  }
}
```

## Checklist
- [ ] Is the widget class under 80 lines?
- [ ] Are complex UI components extracted into their own files?
- [ ] Is business logic separated from UI code?
- [ ] Are we using `const` constructors where possible?
- [ ] Does each file have a single responsibility?
