---
name: flutter-architecture
description: >-
  Provides Flutter app architecture patterns with feature-first structure, clean architecture,
  and state management (Bloc, Riverpod, Provider). Use when user asks about Flutter project
  structure, state management selection, dependency injection, or designing Flutter app architecture.
version: 1.0.0
---

# Flutter Architecture Patterns

Apply these patterns when designing or implementing Flutter applications.

## Feature-First Project Structure

Organize Flutter projects by feature, not by layer:

```
lib/
├── core/                          # Shared infrastructure
│   ├── constants/                 # App-wide constants
│   ├── errors/                    # Error classes and handling
│   ├── extensions/                # Dart extensions
│   ├── network/                   # HTTP client, interceptors
│   ├── theme/                     # App theme, colors, typography
│   └── utils/                     # Utility functions
├── features/                      # Feature modules
│   ├── auth/
│   │   ├── data/                  # Data layer
│   │   │   ├── datasources/       # Remote and local data sources
│   │   │   ├── models/            # Data models (JSON serializable)
│   │   │   └── repositories/      # Repository implementations
│   │   ├── domain/                # Domain layer
│   │   │   ├── entities/          # Business entities
│   │   │   ├── repositories/      # Repository interfaces
│   │   │   └── usecases/          # Business logic
│   │   └── presentation/          # UI layer
│   │       ├── bloc/              # State management
│   │       ├── pages/             # Screen widgets
│   │       └── widgets/           # Feature-specific widgets
│   └── [other_features]/
├── shared/                        # Shared UI components
│   ├── widgets/                   # Reusable widgets
│   └── services/                  # Shared services
└── main.dart
```

## Clean Architecture Layers

### Dependency Rule
- Presentation → Domain ← Data
- Domain has NO external dependencies
- Data implements Domain interfaces

### Layer Responsibilities

**Presentation**: UI components, state management, user interaction handling
**Domain**: Business entities, use cases, repository contracts
**Data**: API calls, local storage, data transformation

## State Management Selection

### Use Bloc When:
- Building enterprise applications
- Need explicit state transitions
- Complex business logic with multiple states
- Team prefers reactive programming patterns

### Use Riverpod When:
- Want compile-time safety for providers
- Need flexible dependency injection
- Building modern, testable applications
- Auto-dispose of resources is important

### Use Provider When:
- Building simpler applications
- Team is new to Flutter
- Don't need complex state management
- Rapid prototyping

## Key Dependencies

```yaml
dependencies:
  # State Management (choose one)
  flutter_bloc: ^8.1.0      # Bloc
  flutter_riverpod: ^2.4.0  # Riverpod
  provider: ^6.1.0          # Provider

  # Dependency Injection
  get_it: ^7.6.0
  injectable: ^2.3.0

  # Navigation
  go_router: ^13.0.0

  # Networking
  dio: ^5.4.0

  # Code Generation
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

dev_dependencies:
  build_runner: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  injectable_generator: ^2.4.0

  # Testing
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
```

## Quick Reference

| Aspect | Recommendation |
|--------|----------------|
| Structure | Feature-first |
| State | Bloc (enterprise), Riverpod (modern), Provider (simple) |
| DI | get_it + injectable |
| Navigation | go_router |
| HTTP | Dio |
| Immutability | Freezed |
| Testing | mocktail + bloc_test |

For detailed implementation examples, consult the flutter-architect agent.
