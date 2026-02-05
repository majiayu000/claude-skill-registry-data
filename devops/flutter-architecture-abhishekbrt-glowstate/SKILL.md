---
name: flutter-architecture
description: Feature-first architecture patterns for scalable Flutter apps. Covers project structure, dependency injection with Riverpod, repository pattern, and clean architecture layers. Use when setting up new projects, creating features, or making structural decisions.
---

# Flutter Architecture

## Core Principle

**Feature-First, Layer-Second**: Group by feature (auth, home, profile), then by layer (data, domain, presentation) within each feature.

## When to Use What

| Decision | Guidance |
|----------|----------|
| New project | Start with `core/` + first feature folder |
| New feature | Create `features/{name}/` with data/domain/presentation |
| Shared widget | Only in `core/widgets/` if used by 3+ features |
| Shared logic | `core/` for network, error handling, providers |

## Detailed Guides

| Topic | Guide | Use When |
|-------|-------|----------|
| Project Structure | [feature-first-structure.md](references/feature-first-structure.md) | Setting up folders, creating features |
| Dependency Injection | [dependency-injection.md](references/dependency-injection.md) | Riverpod DI, provider dependencies, testing |
| Repository Pattern | [repository-pattern.md](references/repository-pattern.md) | Data layer, caching, error handling |

## Quick Reference

### Feature Module Template

```
features/auth/
├── data/
│   ├── datasources/
│   │   ├── auth_remote_source.dart
│   │   └── auth_local_source.dart
│   ├── models/
│   │   └── user_model.dart           # JSON serialization
│   ├── repositories/
│   │   └── auth_repository_impl.dart  # Implements interface
│   └── providers/
│       └── auth_repository_provider.dart  # Riverpod provider
├── domain/
│   ├── entities/
│   │   └── user.dart                  # Pure business object
│   └── repositories/
│       └── auth_repository.dart       # Interface (abstract class)
└── presentation/
    ├── providers/
    │   └── auth_provider.dart         # State management (Riverpod)
    ├── screens/
    │   └── login_screen.dart
    └── widgets/
        └── login_form.dart
```

### Interface-First Pattern (TDD)

```dart
// 1. Define interface in domain/repositories/
abstract class AuthRepository {
  Future<User> login(String email, String password);
  Future<void> logout();
  Future<User?> getCurrentUser();
}

// 2. Create implementation shell in data/repositories/
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteSource _remoteSource;
  final AuthLocalSource _localSource;

  AuthRepositoryImpl({
    required AuthRemoteSource remoteSource,
    required AuthLocalSource localSource,
  }) : _remoteSource = remoteSource,
       _localSource = localSource;

  @override
  Future<User> login(String email, String password) {
    throw UnimplementedError(); // RED phase
  }
  
  // ... other methods
}
```

### Provider Registration (Riverpod)

```dart
// features/auth/data/providers/auth_repository_provider.dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'auth_repository_provider.g.dart';

@riverpod
AuthRepository authRepository(Ref ref) {
  return AuthRepositoryImpl(
    remoteSource: ref.watch(authRemoteSourceProvider),
    localSource: ref.watch(authLocalSourceProvider),
  );
}

// features/auth/presentation/providers/auth_provider.dart
@riverpod
class Auth extends _$Auth {
  @override
  FutureOr<User?> build() async {
    final repo = ref.watch(authRepositoryProvider);
    return repo.getCurrentUser();
  }

  Future<void> login(String email, String password) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      return ref.read(authRepositoryProvider).login(email, password);
    });
  }

  Future<void> logout() async {
    await ref.read(authRepositoryProvider).logout();
    state = const AsyncData(null);
  }
}
```

### Alternative: BLoC with GetIt

For complex event-driven features, use BLoC pattern with GetIt:

```dart
// core/di/injection.dart (alternative approach)
import 'package:get_it/get_it.dart';

final sl = GetIt.instance;

void configureDependencies() {
  // Core
  sl.registerLazySingleton<ApiClient>(() => ApiClient());
  
  // Feature: Auth
  _initAuth();
}

void _initAuth() {
  sl.registerLazySingleton<AuthRemoteSource>(
    () => AuthRemoteSource(client: sl()),
  );
  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(remoteSource: sl(), localSource: sl()),
  );
  sl.registerFactory<AuthBloc>(
    () => AuthBloc(repository: sl()),
  );
}
```

## State Management Choice

| Scenario | Use |
|----------|-----|
| Most features | Riverpod `AsyncNotifierProvider` |
| Simple sync state | Riverpod `NotifierProvider` |
| Complex event flows | BLoC (with GetIt DI) |

See [state-management/SKILL.md](../state-management/SKILL.md) for detailed guidance.

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Widget directly calling API | Widget → Provider → Repository → DataSource |
| Business logic in widgets | Move to Notifier/BLoC |
| Concrete class dependencies | Depend on abstract interfaces |
| Circular feature dependencies | Extract shared code to `core/` |
| God objects (one class does everything) | Single responsibility per class |
| Passing `ref` to business classes | Inject dependencies directly |
