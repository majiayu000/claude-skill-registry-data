---
name: mobile-pro-max
description: "Mobile development intelligence. 12 domains, 9 stacks, 250+ entries. Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check mobile code. Domains: pattern, package, error, perf, test, security, interface, arch, idiom, anti, tooling, dependency. Stacks: flutter, react-native, swiftui, jetpack-compose, kotlin-multiplatform, capacitor, expo, native-ios, native-android. Integrations: arch_system generator."
---

# Mobile Pro Max - App Generator

## When User Requests Mobile Work

Follow this workflow for every mobile-related task:

### 1. Analyze Requirements

Extract from the user's request:

- **Platform**: iOS, Android, cross-platform, web-to-mobile
- **Project type**: consumer app, enterprise app, e-commerce, social, fintech, health
- **Domain**: UI/UX, networking, storage, auth, payments, maps, camera, push notifications
- **Constraints**: specific framework? offline-first? real-time? performance-critical?
- **Scale**: MVP, production, enterprise

### Default Stack (always use unless user specifies otherwise)

| Component          | Default              | Package                         |
| ------------------ | -------------------- | ------------------------------- |
| **Framework**      | **Flutter 3.x**      | `flutter`                       |
| **Language**       | **Dart 3.x**         | Sound null safety               |
| **State Mgmt**     | Riverpod             | `flutter_riverpod`              |
| **Navigation**     | GoRouter             | `go_router`                     |
| **HTTP Client**    | Dio                  | `dio` + `retrofit`              |
| **DI**             | GetIt + Injectable   | `get_it` + `injectable`         |
| **Models**         | Freezed              | `freezed` + `json_serializable` |
| **Local DB**       | Drift                | `drift` (SQLite)                |
| **Secure Storage** | Flutter Secure       | `flutter_secure_storage`        |
| **Error Handling** | fpdart Either        | `fpdart`                        |
| **Testing**        | mocktail + bloc_test | `mocktail` + `bloc_test`        |
| **CI/CD**          | GitHub Actions       | + Fastlane for store deployment |

**Project structure**: Flutter Clean Architecture with feature-first:

```
lib/
  core/
    constants/         — app-wide constants
    theme/             — ThemeData, colors, typography
    utils/             — utility functions, extensions
    errors/            — Failure classes, error handling
    network/           — Dio client, interceptors
  features/
    auth/
      data/            — datasources, models, repository impl
      domain/          — entities, repository interface, use cases
      presentation/    — BLoC/providers, screens, widgets
    home/
      data/
      domain/
      presentation/
    products/
      data/
      domain/
      presentation/
  shared/
    widgets/           — reusable widgets (AppButton, AppCard, etc.)
    services/          — analytics, push notifications, etc.
  l10n/                — localization ARB files
  app.dart             — MaterialApp.router setup
  main.dart            — entry point, DI setup
test/
  unit/                — unit tests (use cases, repositories)
  widget/              — widget tests
  integration/         — integration tests
```

### 2. Generate Architecture System (REQUIRED for new projects)

```bash
python3 skills/mobile/scripts/search.py "<project description>" --arch-system -p "ProjectName"
```

This gives you: architecture, packages, error strategy, patterns, structure, testing approach, state management, CI/CD pipeline.

### 3. Supplement with Domain Searches

Based on the project needs, search relevant domains:

```bash
# Patterns for the task
python3 skills/mobile/scripts/search.py "mvvm bloc clean architecture" --domain pattern

# Error handling approach
python3 skills/mobile/scripts/search.py "either result type crash reporting" --domain error

# Security patterns
python3 skills/mobile/scripts/search.py "secure storage certificate pinning" --domain security

# Performance tips
python3 skills/mobile/scripts/search.py "widget rebuild list optimization" --domain perf

# Testing patterns
python3 skills/mobile/scripts/search.py "widget test bloc test mocking" --domain test

# UI/UX guidelines
python3 skills/mobile/scripts/search.py "responsive layout dark mode accessibility" --domain interface
```

### 4. Stack Guidelines

If using a specific framework/stack:

```bash
python3 skills/mobile/scripts/search.py "state management navigation" --stack flutter
python3 skills/mobile/scripts/search.py "hooks performance memoization" --stack react-native
python3 skills/mobile/scripts/search.py "observable state swiftdata" --stack swiftui
python3 skills/mobile/scripts/search.py "viewmodel stateflow hilt" --stack jetpack-compose
python3 skills/mobile/scripts/search.py "expect actual ktor" --stack kotlin-multiplatform
python3 skills/mobile/scripts/search.py "eas build expo router" --stack expo
```

### 5. Implement

Apply all recommendations from the search results:

- Use recommended architecture and project structure
- Apply patterns (MVVM, BLoC, Clean Architecture, Repository, etc.)
- Follow error handling strategy (Either types, typed failures)
- Implement security best practices (secure storage, certificate pinning)
- Add tests following testing strategy (unit > widget > integration)
- Build responsive layouts with design system

### 6. Always Generate Project Configuration

Every Flutter project MUST include:

**pubspec.yaml** (core dependencies):

```yaml
name: my_app
description: A Flutter application
version: 1.0.0+1

environment:
  sdk: ">=3.2.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.4.0
  go_router: ^13.0.0
  dio: ^5.4.0
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0
  get_it: ^7.6.0
  injectable: ^2.3.0
  fpdart: ^1.1.0
  flutter_secure_storage: ^9.0.0
  drift: ^2.14.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  injectable_generator: ^2.4.0
  drift_dev: ^2.14.0
  mocktail: ^1.0.0
  bloc_test: ^9.1.0
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
    - assets/icons/
```

**analysis_options.yaml**:

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_const_constructors: true
    prefer_const_declarations: true
    avoid_print: true
    require_trailing_commas: true
    prefer_single_quotes: true

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
```

**Makefile**:

```makefile
run:
	flutter run
test:
	flutter test
analyze:
	flutter analyze --fatal-warnings
format:
	dart format .
build-runner:
	dart run build_runner build --delete-conflicting-outputs
watch:
	dart run build_runner watch --delete-conflicting-outputs
build-apk:
	flutter build apk --release --obfuscate --split-debug-info=build/debug-info/
build-ios:
	flutter build ipa --release --obfuscate --split-debug-info=build/debug-info/
clean:
	flutter clean && flutter pub get
```

## Pre-Delivery Checklist

Before delivering mobile code, verify:

- [ ] `flutter analyze --fatal-warnings` passes
- [ ] `dart format .` passes (no formatting issues)
- [ ] `flutter test` passes with adequate coverage
- [ ] No hardcoded strings (use localization)
- [ ] All user input validated (client-side AND server-side)
- [ ] Sensitive data stored in flutter_secure_storage (not SharedPreferences)
- [ ] No hardcoded API keys or secrets (use --dart-define)
- [ ] Proper error handling (Either types, typed failures, no empty catch blocks)
- [ ] All StreamSubscriptions cancelled in dispose()
- [ ] All Controllers disposed in dispose()
- [ ] Const constructors used where possible
- [ ] BuildContext not used across async gaps (check mounted)
- [ ] Responsive layout tested on multiple screen sizes
- [ ] Dark mode supported and tested
- [ ] Accessibility labels on interactive elements
- [ ] Minimum tap target size 48x48
- [ ] Loading, error, and empty states handled for all async data
- [ ] Code obfuscation enabled for release builds

## Quick Domain Reference

| Domain       | When to Search                                                     |
| ------------ | ------------------------------------------------------------------ |
| `pattern`    | Need a design pattern (MVVM, BLoC, Repository, Clean Architecture) |
| `package`    | Choosing a pub.dev package for a use case                          |
| `error`      | Error handling strategy, either types, crash reporting             |
| `perf`       | Performance optimization, widget rebuilds, memory, lists           |
| `test`       | Testing approach, widget tests, BLoC tests, mocking, golden tests  |
| `security`   | Secure storage, certificate pinning, obfuscation, auth             |
| `interface`  | UI/UX design, responsive layout, accessibility, Material Design 3  |
| `arch`       | Project structure, architecture patterns, modular design           |
| `idiom`      | Dart conventions, null safety, extensions, pattern matching        |
| `anti`       | Avoiding common mistakes (massive widgets, setState abuse, leaks)  |
| `tooling`    | Flutter DevTools, Fastlane, FVM, Mason, CI/CD                      |
| `dependency` | pubspec.yaml, CocoaPods, Gradle, version management                |

## Resources

- **scripts/**: BM25 search engine, architecture system generator
- **data/**: 12 domains and 9 stacks with 250+ curated mobile entries
