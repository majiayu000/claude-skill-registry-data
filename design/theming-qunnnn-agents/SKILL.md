---
name: flutter-theming-apps
description: Customizes the visual appearance of a Flutter app using the theming system. Use when defining global styles, colors, or typography.
tags: [flutter, theming, material3, design-system, styling]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Theming (Material 3)

## Contents
- [Core Theming Concepts](#core-theming-concepts)
- [Material 3 Guidelines](#material-3-guidelines)
- [Component Theme Normalization](#component-theme-normalization)
- [Button Styling](#button-styling)
- [Platform Idioms & Adaptive Design](#platform-idioms--adaptive-design)
- [Workflows](#workflows)
- [Examples](#examples)

## Core Theming Concepts
Flutter applies styling in a strict hierarchy: styles applied to the specific widget → themes that override the immediate parent theme → the main app theme.

- Define app-wide themes using the `theme` property of `MaterialApp` with a `ThemeData` instance.
- Override themes for specific widget subtrees by wrapping them in a `Theme` widget and using `Theme.of(context).copyWith(...)`.
- **Do not** use deprecated `ThemeData` properties:
  - Replace `accentColor` with `colorScheme.secondary`.
  - Replace `accentTextTheme` with `textTheme` (using `colorScheme.onSecondary` for contrast).
  - Replace `AppBarTheme.color` with `AppBarTheme.backgroundColor`.

## Material 3 Guidelines
Material 3 is the default theme as of Flutter 3.16.

- **Colors:** Generate color schemes using `ColorScheme.fromSeed(seedColor: Colors.blue)`. This ensures accessible contrast ratios.
- **Elevation:** Material 3 uses `ColorScheme.surfaceTint` to indicate elevation instead of just drop shadows. To revert to M2 shadow behavior, set `surfaceTint: Colors.transparent` and define a `shadowColor`.
- **Typography:** Material 3 updates font sizes, weights, and line heights. If text wrapping breaks legacy layouts, adjust `letterSpacing` on the specific `TextStyle`.
- **Modern Components:**
  - Replace `BottomNavigationBar` with `NavigationBar`.
  - Replace `Drawer` with `NavigationDrawer`.
  - Replace `ToggleButtons` with `SegmentedButton`.
  - Use `FilledButton` for a high-emphasis button without the elevation of `ElevatedButton`.

## Component Theme Normalization
When defining `ThemeData`, strictly use the `*ThemeData` suffix:
- `cardTheme`: Use `CardThemeData` (Not `CardTheme`)
- `dialogTheme`: Use `DialogThemeData` (Not `DialogTheme`)
- `tabBarTheme`: Use `TabBarThemeData` (Not `TabBarTheme`)
- `appBarTheme`: Use `AppBarThemeData` (Not `AppBarTheme`)
- `bottomAppBarTheme`: Use `BottomAppBarThemeData` (Not `BottomAppBarTheme`)
- `inputDecorationTheme`: Use `InputDecorationThemeData` (Not `InputDecorationTheme`)

## Button Styling
Legacy button classes (`FlatButton`, `RaisedButton`, `OutlineButton`) are obsolete.

- Use `TextButton`, `ElevatedButton`, and `OutlinedButton`.
- Configure button appearance using a `ButtonStyle` object.
- For simple overrides, use `TextButton.styleFrom(foregroundColor: Colors.blue)`.
- For state-dependent styling (hovered, focused, pressed, disabled), use `MaterialStateProperty.resolveWith`.

## Platform Idioms & Adaptive Design
When building adaptive apps, respect platform-specific norms.

- **Scrollbars:** Desktop users expect omnipresent scrollbars; mobile users expect them only during scrolling.
- **Selectable Text:** Web and desktop users expect text to be selectable. Use `SelectableText`.
- **Horizontal Button Order:** Windows places confirmation buttons on the left; macOS/Linux place them on the right.
- **Context Menus & Tooltips:** Desktop users expect hover and right-click interactions.

## Workflows

### Migrating Legacy Themes to Material 3
- [ ] Remove `useMaterial3: false` from `ThemeData` (it is true by default).
- [ ] Replace manual `ColorScheme` definitions with `ColorScheme.fromSeed()`.
- [ ] Search for and replace deprecated `accentColor`, `accentColorBrightness`, `accentIconTheme`, and `accentTextTheme`.
- [ ] Search for `AppBarTheme(color: ...)` and replace with `backgroundColor`.
- [ ] Update `ThemeData` component properties to use `*ThemeData` classes.
- [ ] Replace legacy buttons (`FlatButton` → `TextButton`, `RaisedButton` → `ElevatedButton`, `OutlineButton` → `OutlinedButton`).
- [ ] Replace legacy navigation components (`BottomNavigationBar` → `NavigationBar`, `Drawer` → `NavigationDrawer`).

### Implementing Adaptive UI Components
- [ ] If displaying a list/grid, wrap it in a `Scrollbar` and set `thumbVisibility` based on platform.
- [ ] If displaying read-only data, use `SelectableText` instead of `Text`.
- [ ] If implementing a dialog with action buttons, check the platform for button order.
- [ ] If implementing interactive elements, wrap them in `Tooltip` widgets for mouse hover.

## Examples

### Modern Material 3 ThemeData Setup

```dart
MaterialApp(
  title: 'Adaptive App',
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.light,
    ),
    appBarTheme: const AppBarThemeData(
      backgroundColor: Colors.deepPurple,
      elevation: 0,
    ),
    cardTheme: const CardThemeData(
      elevation: 2,
    ),
    textTheme: const TextTheme(
      bodyMedium: TextStyle(letterSpacing: 0.2),
    ),
  ),
  home: const MyHomePage(),
);
```

### State-Dependent ButtonStyle

```dart
TextButton(
  style: ButtonStyle(
    foregroundColor: MaterialStateProperty.all<Color>(Colors.blue),
    overlayColor: MaterialStateProperty.resolveWith<Color?>(
      (Set<MaterialState> states) {
        if (states.contains(MaterialState.hovered)) {
          return Colors.blue.withOpacity(0.04);
        }
        if (states.contains(MaterialState.focused) || states.contains(MaterialState.pressed)) {
          return Colors.blue.withOpacity(0.12);
        }
        return null;
      },
    ),
  ),
  onPressed: () {},
  child: const Text('Adaptive Button'),
)
```

### Adaptive Dialog Button Order

```dart
Row(
  textDirection: Platform.isWindows ? TextDirection.rtl : TextDirection.ltr,
  mainAxisAlignment: MainAxisAlignment.end,
  children: [
    TextButton(
      onPressed: () => Navigator.pop(context, false),
      child: const Text('Cancel'),
    ),
    FilledButton(
      onPressed: () => Navigator.pop(context, true),
      child: const Text('Confirm'),
    ),
  ],
)
```

## Resources

- https://docs.flutter.dev/cookbook/design/themes
- https://docs.flutter.dev/ui/design
- https://docs.flutter.dev/ui/widgets/styling
- https://docs.flutter.dev/release/breaking-changes/material-3-migration
- https://docs.flutter.dev/release/breaking-changes/material-3-default
- https://docs.flutter.dev/release/breaking-changes/component-theme-normalization
- https://docs.flutter.dev/release/breaking-changes/component-theme-normalization-updates
- https://docs.flutter.dev/release/breaking-changes/buttons
- https://docs.flutter.dev/release/breaking-changes/theme-data-accent-properties
- https://docs.flutter.dev/release/breaking-changes/appbar-theme-color
- https://docs.flutter.dev/ui/adaptive-responsive/idioms
