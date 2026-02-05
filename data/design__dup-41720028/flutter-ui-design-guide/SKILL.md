---
name: flutter-ui-design-guide
description: Apply Flutter design principles with Material Design and Cupertino (iOS-style) support when building cross-platform UI. Only execute this when the current project is a Flutter project and involves UI-related work. Use this skill for Flutter widgets, Dart layouts, or cross-platform app development. Ensures Material Design compliance (Android) and Cupertino guidelines (iOS), 8dp grid spacing, Material TextTheme, Theme-based colors with dark mode, and adaptive widgets. Prevents common anti-patterns like hardcoded colors, fixed text sizes, and excessive widget nesting.
---

# Flutter UI Design Guide

## Overview

Build cross-platform Flutter apps with Material Design (Android) and Cupertino (iOS) support. This skill provides guidelines for adaptive widgets, theming, spacing, typography, and component patterns optimized for both platforms.

## When to Use This Skill

Activate this skill when:
- Building Flutter UI with Material or Cupertino widgets
- Creating cross-platform app screens or layouts
- Working with Flutter development (Dart, Flutter SDK)
- Receiving requests like:
  - "Create a login screen in Flutter"
  - "Design a Flutter card layout"
  - "Build adaptive navigation in Flutter"
  - "Make this Flutter UI follow Material Design"
  - "Style this Flutter widget with Cupertino"

**Do NOT activate** for:
- Native iOS (SwiftUI/UIKit) only
- Native Android (Compose/XML) only
- Web development
- Backend/server code

## Core Design Philosophy

### Cross-Platform Principles

1. **Consistency** - Single codebase, pixel-perfect UI across platforms
2. **Adaptive** - Material (Android) and Cupertino (iOS) styles
3. **Widget Composition** - Reusable, composable widgets

### Flexible Extensions

4. **Simplicity** - Clear widget tree, minimal nesting
5. **Accessibility** - Semantics, 48dp touch targets

## Framework Approach

- **Material Default**: Material Design 3 widgets (Android style)
- **Cupertino Option**: iOS-style widgets when needed
- **Adaptive Widgets**: Platform auto-detection

## How to Use This Skill

### Step 1: Load Relevant Reference

```
Read references/design-principles.md - Cross-platform + adaptive design
Read references/color-system.md - Theme-based colors, dark mode
Read references/spacing-system.md - 8dp grid, EdgeInsets
Read references/typography.md - Material TextTheme, Cupertino text
Read references/component-patterns.md - Material + Cupertino widgets
Read references/anti-patterns.md - Common Flutter mistakes
```

### Step 2: Apply Component-Specific Patterns

- **Button**: Material (ElevatedButton) vs Cupertino (CupertinoButton)
- **Card**: Material Card widget
- **List**: ListView.builder for performance
- **TextField**: Material TextField vs Cupertino CupertinoTextField
- **Navigation**: AppBar, BottomNavigationBar, CupertinoNavigationBar
- **Dialog**: AlertDialog vs CupertinoAlertDialog

### Step 3: Validate Against Anti-Patterns

- ❌ Hardcoded colors (`Colors.black`, `Colors.white`)
- ❌ Fixed text sizes (no TextTheme)
- ❌ Excessive widget nesting
- ❌ setState overuse
- ❌ Column for long lists (use ListView)

### Step 4: Ensure System Consistency

**8dp grid**:
- Use: 4.0, 8.0, 16.0, 24.0, 32.0, 48.0
- `EdgeInsets.all(16.0)`, `SizedBox(height: 16.0)`

**Theme colors** (auto dark mode):
- `Theme.of(context).colorScheme.primary`
- `Theme.of(context).colorScheme.onSurface`
- `CupertinoTheme.of(context).primaryColor`

**TextTheme** (REQUIRED):
- `Theme.of(context).textTheme.headlineMedium`
- `Theme.of(context).textTheme.bodyMedium`

## Resources

### references/

- **design-principles.md** - Cross-platform, Material + Cupertino, widget composition
- **color-system.md** - ColorScheme, Theme, dark mode
- **spacing-system.md** - 8dp grid, EdgeInsets, SizedBox
- **typography.md** - Material TextTheme, Cupertino text styles
- **component-patterns.md** - Material + Cupertino widgets
- **anti-patterns.md** - Common mistakes: hardcoded colors, nesting, performance

## Quick Decision Tree

```
Flutter UI Component Request
│
├─ Material or Cupertino? → Material default, Cupertino for iOS feel
│
├─ What spacing? → 8dp grid (spacing-system.md)
│
├─ What colors? → Theme.of(context).colorScheme (color-system.md)
│
├─ What typography? → TextTheme (typography.md)
│
└─ Validation → Check anti-patterns.md
```

## Examples

**Good Request Flow**:
```
User: "Create a login form in Flutter"
→ Read references/component-patterns.md (TextField section)
→ Apply: TextField, Theme colors, TextTheme, 8dp spacing
→ Validate: No hardcoded colors, proper widget tree
→ Implement with Column { TextField, ElevatedButton }
```

**Implementation Checklist**:
- ✅ Spacing uses 8dp multiples
- ✅ TextTheme used (headlineMedium, bodyMedium)
- ✅ Theme colors (auto dark mode)
- ✅ Touch targets 48x48dp minimum
- ✅ Material or Cupertino widgets
- ✅ Minimal widget nesting
- ✅ ListView for long lists

## Flutter Code Examples

### ✅ Good: Theme-Based Colors

```dart
Text(
  '제목',
  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
    color: Theme.of(context).colorScheme.onSurface,
  ),
)
```

### ✅ Good: Material Button

```dart
ElevatedButton(
  onPressed: () {},
  child: Text('확인'),
)
```

### ❌ Bad: Hardcoded, No Theme

```dart
Text(
  '제목',
  style: TextStyle(fontSize: 24.0, color: Colors.black),  // ❌
)
```

## Platform-Specific Considerations

### Adaptive Widgets

```dart
Widget build(BuildContext context) {
  if (Theme.of(context).platform == TargetPlatform.iOS) {
    return CupertinoButton(child: Text('확인'), onPressed: () {});
  }
  return ElevatedButton(child: Text('확인'), onPressed: () {});
}
```

### Dark Mode

```dart
MaterialApp(
  theme: lightTheme,
  darkTheme: darkTheme,
  themeMode: ThemeMode.system,  // Auto dark mode
)
```

## Reference Documentation

- [Flutter Design](https://docs.flutter.dev/design)
- [Material Components](https://docs.flutter.dev/ui/widgets/material)
- [Cupertino Widgets](https://docs.flutter.dev/ui/widgets/cupertino)
