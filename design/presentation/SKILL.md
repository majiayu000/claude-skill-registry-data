---
name: presentation
description: Generate presentation layer code (Freezed states, Riverpod notifiers, screens, widgets) from feature specifications. Creates the UI layer with proper state management. Use after /data to implement screens and state handling.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Presentation - Presentation Layer Generator

Generate presentation layer components that handle UI state and render screens using domain entities.

## Philosophy

The presentation layer is **domain-aware, data-blind**:
- Imports domain entities and repository interfaces
- Never imports data layer (models, repository implementations)
- Uses Freezed sealed states for exhaustive pattern matching
- Uses Riverpod AsyncNotifier with disposal safety

This keeps the UI decoupled from data sources and serialization details.

## When to Use This Skill

- After `/data` has implemented repositories
- When creating screens from spec requirements
- When adding new screens or actions to existing features
- User asks to "create screen", "implement UI", "add presentation layer"

## What This Skill Creates

```
lib/features/{feature}/presentation/
├── providers/
│   ├── {feature}_state.dart         # Freezed sealed state
│   └── {feature}_notifier.dart      # AsyncNotifier with safe state
├── screens/
│   └── {feature}_screen.dart        # ConsumerWidget with pattern matching
└── widgets/
    └── {feature}_item.dart          # Extracted reusable widgets
```

## Workflow

### Step 1: Locate Requirements

Check for:
```
lib/features/{feature}/.spec.md           # Feature specification
lib/features/{feature}/domain/            # Domain entities
lib/features/{feature}/data/              # Repository implementation
```

If domain/data layers don't exist, ask user to run `/domain` and `/data` first.

### Step 2: Analyze UI Requirements

From the spec, identify:
- **Screens** - Section 4.1 (list, detail, form, etc.)
- **State Fields** - What data each screen needs
- **Actions** - User interactions (refresh, create, delete, submit)
- **Navigation** - How screens connect

### Step 3: Generate Code

Use reference files in `reference/` directory as templates:

| Component | Reference File |
|-----------|----------------|
| List state | `reference/providers/list_state.dart` |
| Detail state | `reference/providers/detail_state.dart` |
| Form state | `reference/providers/form_state.dart` |
| Basic notifier | `reference/providers/basic_notifier.dart` |
| CRUD notifier | `reference/providers/crud_notifier.dart` |
| Form notifier | `reference/providers/form_notifier.dart` |
| List screen | `reference/screens/list_screen.dart` |
| Detail screen | `reference/screens/detail_screen.dart` |
| Form screen | `reference/screens/form_screen.dart` |
| List item widget | `reference/widgets/list_item.dart` |
| Form field widget | `reference/widgets/form_field.dart` |

### Step 4: Run Code Generation

```bash
dart run build_runner build --delete-conflicting-outputs
```

### Step 5: Verify

```bash
dart analyze lib/features/{feature}/presentation/
```

## Commands

| Command | Purpose |
|---------|---------|
| `/presentation {feature}` | Generate full presentation layer |
| `/presentation {feature} --only=providers` | Generate only state and notifier |
| `/presentation {feature} --only=screens` | Generate only screens |
| `/presentation {feature} --add-screen={Name}` | Add new screen to existing feature |

## Screen Types

| Type | Use When | State Complexity |
|------|----------|------------------|
| **List** | Displaying collection | `initial`, `loading`, `loaded(items)`, `error` |
| **Detail** | Single item view | `initial`, `loading`, `loaded(item)`, `error` |
| **Form** | Create/edit | Form fields + `isSubmitting`, validation |
| **Confirmation** | Destructive actions | Minimal, action-focused |

## State Design Principles

1. **Sealed unions** - Use Freezed `sealed class` for exhaustive matching
2. **Domain entities only** - Never put DTOs in state
3. **Derived state** - Compute `isEmpty`, `hasError` from base state
4. **Separate form state** - Forms use field-based state, not sealed unions

**Core pattern:** `sealed class` with `initial`, `loading`, `loaded(items)`, `error(message)`

## Notifier Design Principles

1. **Disposal safety** - Track `_disposed` flag, check after every await
2. **Repository injection** - Read repository from ref, never import data layer
3. **Error mapping** - Convert exceptions to user-friendly messages (via `/i18n`)
4. **Action methods** - One public method per user action

**Core pattern:**
```dart
bool _disposed = false;
void _safeSetState(State s) { if (!_disposed) state = s; }
// Check _disposed after EVERY await
```

## Screen Pattern

**Core pattern:**
```dart
switch (state) {
  StateInitial() || StateLoading() => CircularProgressIndicator(),
  StateLoaded(:final items) => ListView.builder(/*...*/),
  StateError(:final message) => Text(message),
}
```

## Checklist

Before finishing presentation layer:

- [ ] All screens from spec are created
- [ ] State uses domain entities only
- [ ] Notifier has `_disposed` flag and `_safeSetState`
- [ ] Screen uses `switch` pattern matching on state
- [ ] All user actions have corresponding notifier methods
- [ ] Loading states shown during async operations
- [ ] Error states display user-friendly messages (i18n keys)
- [ ] Empty states handled with helpful messages
- [ ] No data layer imports (no models, no repository implementations)
- [ ] Widgets extracted when screen exceeds 200 lines
- [ ] `build_runner` executed successfully

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| State class | `{Feature}State` | `BookmarksState` |
| State file | `{feature}_state.dart` | `bookmarks_state.dart` |
| Notifier class | `{Feature}Notifier` | `BookmarksNotifier` |
| Notifier file | `{feature}_notifier.dart` | `bookmarks_notifier.dart` |
| Screen class | `{Feature}Screen` | `BookmarksScreen` |
| Screen file | `{feature}_screen.dart` | `bookmarks_screen.dart` |
| Widget | `{Feature}{Component}` | `BookmarkListItem` |

## Presentation Layer Rules

1. **No data layer imports** - Only import from domain/
2. **Freezed for states** - Sealed unions for exhaustive matching
3. **Disposal safety** - Always check `_disposed` after await
4. **Pattern matching** - Use `switch` expression on sealed states
5. **Widgets for reuse** - Extract when >50 lines or used multiple times

## Guides

| Guide | Use For |
|-------|---------|
| [patterns-guide.md](patterns-guide.md) | State patterns, notifier patterns, screen structures |
| [examples.md](examples.md) | Complete before/after examples |
| [reference/](reference/) | Actual code templates |

## Related Skills

- `/data` - Run first to implement repository
- `/domain` - Creates entities used by presentation
- `/feature-init` - Initialize feature scaffold
- `/i18n` - Localize user-facing strings and error messages
- `/design` - Polish UI/UX patterns after basic implementation
- `/a11y` - Add accessibility support
- `/testing` - Create widget tests
