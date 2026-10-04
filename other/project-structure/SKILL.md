---
name: flutter-project-structure
description: Establishes a clean, modular architecture and project structure for Flutter applications.
tags: [flutter, architecture, clean-architecture, modular]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Project Structure

## Context

Apply when creating new features, modules, or navigating the codebase in a modular Flutter project.

## Instructions

1. **Feature-first organization**: Group by feature, not by type.
2. **Module structure**:
   ```text
   lib/
   ├── main.dart                    # Entry point
   ├── app.dart                     # MaterialApp / Router setup
   ├── core/                        # Shared utilities, constants, extensions
   │   ├── constants/
   │   ├── extensions/
   │   ├── theme/
   │   ├── utils/
   │   ├── widgets/                 # Shared/reusable widgets
   │   └── import/                  # Centralized imports (app_imports.dart)
   ├── features/                    # Feature-based modules
   │   ├── features.dart            # Global barrel exporting all features
   │   └── <feature_name>/
   │       ├── <feature_name>.dart  # Feature root barrel
   │       ├── data/
   │       │   ├── models/
   │       │   │   └── index.dart
   │       │   ├── datasources/
   │       │   │   └── index.dart
   │       │   └── repositories/
   │       │       └── index.dart
   │       ├── domain/
   │       │   ├── entities/
   │       │   │   └── index.dart
   │       │   ├── repositories/
   │       │   │   └── index.dart
   │       │   └── usecases/
   │       │       └── index.dart
   │       └── presentation/
   │           ├── providers/
   │           │   └── index.dart
   │           ├── pages/
   │           │   └── index.dart
   │           └── widgets/
   │               └── index.dart
   ├── l10n/                        # Localization
   └── injection/                   # Dependency injection setup
   ```
3. **Import rules**:
   - Features should NOT import from other features directly.
   - Use the `core/` layer for shared logic.
   - Data layer is accessed via repository interfaces in the domain layer.
4. **Widget decomposition**: If a widget exceeds ~150 lines, decompose into smaller widgets.
5. **Barrel files (The "Deep Barrel" Pattern)**: Use a hierarchical barrel system to consolidate imports.
   - **Layer Barrels (`index.dart`)**: Every leaf directory (entities, models, providers, etc.) MUST have an `index.dart` exporting its handwritten contents.
     - ⚠️ **Rule**: Never export generated files (`.g.dart`, `.freezed.dart`) in barrels.
   - **Feature Barrels (`<feature_name>.dart`)**: The feature root MUST have a barrel file named after the feature that exports all its layer-level `index.dart` files.
   - **Global Features Barrel (`features.dart`)**: The `lib/features/` root MUST have a `features.dart` file exporting all individual feature barrels.
   - This allows importing an entire feature via:
     `import 'package:<package_name>/features/<feature_name>/<feature_name>.dart';`
     Or multiple features via:
     `import 'package:<package_name>/features/features.dart';`
6. **Centralized Imports**: Use `lib/core/import/` to consolidate common dependencies.
   - `packages_imports.dart`: Exports all third-party packages (Flutter, Riverpod, etc.).
   - `app_imports.dart`: Exports `packages_imports.dart` + all `core` layers + all `features`.
   - ⚠️ **Important**: Add `// ignore_for_file: invalid_export_of_internal_element` at the top of these barrel files to allow exporting generator-internal members (like Riverpod's `$` types) without warnings.
   - This allows any file in the app to access most common logic with a single import:
     `import 'package:<package_name>/core/import/app_imports.dart';`
   - ⚠️ **Rule**: Always use `package:` imports instead of relative paths for these centralized barrels to ensure project-wide consistency.

## Anti-patterns

- ❌ Cross-feature imports (feature A importing from feature B directly)
- ❌ Business logic in widgets
- ❌ Monolithic files with `part` directives for non-generated code
- ❌ Deeply nested widget trees without extraction

## Resources

- https://docs.flutter.dev/app-architecture
- https://docs.flutter.dev/app-architecture/concepts
- https://docs.flutter.dev/app-architecture/guide
- https://docs.flutter.dev/app-architecture/recommendations
- https://docs.flutter.dev/resources/architectural-overview
