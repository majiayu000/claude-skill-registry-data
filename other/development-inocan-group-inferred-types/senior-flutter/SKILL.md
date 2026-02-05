---

# === CORE IDENTITY ===
name: senior-flutter
title: Senior Flutter Skill Package
description: Flutter and Dart development expertise for building beautiful, performant cross-platform applications. Covers widget architecture, state management (Riverpod, Bloc, Provider), platform channels, and production deployment. Use when building Flutter apps, implementing complex UIs, optimizing performance, or integrating native code.
domain: engineering
subdomain: flutter-development

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "55% faster UI development, 40% reduced platform-specific code"
frequency: "Daily for Flutter development teams"
use-cases:
  - Building cross-platform apps with Flutter
  - Implementing complex widget architectures
  - Managing state with Riverpod, Bloc, or Provider
  - Integrating native iOS/Android code via platform channels
  - Optimizing Flutter app performance

# === RELATIONSHIPS ===
related-agents:
  - cs-flutter-engineer
  - cs-mobile-engineer
related-skills:
  - senior-mobile
  - senior-ios
related-commands: []
orchestrated-by:
  - cs-flutter-engineer

# === TECHNICAL ===
dependencies:
  scripts: []
  references:
    - dart-patterns.md
    - widget-architecture.md
    - state-management.md
  assets: []
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack:
  - Flutter 3.x
  - Dart 3.x
  - Riverpod
  - Bloc
  - Provider
  - GoRouter
  - Freezed
  - Dio
  - Firebase
  - Platform Channels

# === EXAMPLES ===
examples:
  -
    title: Riverpod State Management
    input: "Implement async data fetching with Riverpod"
    output: "AsyncNotifierProvider with loading, error, and data states"
  -
    title: Platform Channel Integration
    input: "Call native iOS/Android code from Flutter"
    output: "MethodChannel implementation with proper error handling"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-12-13
updated: 2025-12-13
license: MIT

# === DISCOVERABILITY ===
tags:
  - flutter
  - dart
  - mobile
  - cross-platform
  - riverpod
  - bloc
  - provider
  - widgets
  - engineering
featured: true
verified: true
---

# Senior Flutter

Flutter and Dart expertise for building production-grade cross-platform applications. This skill covers widget architecture, state management patterns, native integration, and performance optimization.

## Overview

This skill provides comprehensive Flutter and Dart development expertise for building beautiful, performant cross-platform applications. It covers widget architecture, state management (Riverpod, Bloc, Provider), platform channels for native integration, and performance optimization techniques. Uses Python tools from the senior-mobile skill for scaffolding and validation.

## Quick Start

```bash
# Generate a new Flutter project
python3 ../../senior-mobile/scripts/mobile_scaffolder.py --framework flutter --state riverpod --output ./my-app

# Analyze project configuration
python3 ../../senior-mobile/scripts/platform_detector.py --check all

# Validate for Play Store submission
python3 ../../senior-mobile/scripts/app_store_validator.py --store google --strict
```

## Python Tools

This skill uses Python tools from the `senior-mobile` skill:

- **mobile_scaffolder.py** - Generate Flutter project with clean architecture
- **platform_detector.py** - Analyze project configuration for iOS/Android
- **app_store_validator.py** - Validate against App Store/Play Store requirements

```bash
# Generate Flutter project with Riverpod and GoRouter
python3 ../../senior-mobile/scripts/mobile_scaffolder.py \
  --framework flutter \
  --navigation go-router \
  --state riverpod \
  --ci github-actions

# Full project analysis
python3 ../../senior-mobile/scripts/platform_detector.py --check all --depth full
```

## Core Capabilities

- **Widget Architecture** - Build complex, reusable widget trees with proper lifecycle management
- **State Management** - Implement Riverpod, Bloc, or Provider patterns effectively
- **Platform Channels** - Integrate native iOS/Android code seamlessly
- **Performance Optimization** - Profile and optimize rendering, reduce jank
- **Clean Architecture** - Structure large Flutter applications for maintainability

## Key Workflows

### Workflow 1: Flutter Clean Architecture Setup

**Time:** 2-4 hours for initial structure

**Steps:**
1. Create Flutter project with proper configuration
2. Set up folder structure following clean architecture
3. Configure dependency injection
4. Implement core abstractions (Result, Either, UseCase)
5. Set up routing with GoRouter
6. Configure state management (Riverpod recommended)
7. Add code generation (Freezed, json_serializable)
8. Create base widgets and themes

**Reference:** `references/widget-architecture.md`

**Project Structure:**
```
lib/
├── core/
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/
│   │   ├── api_client.dart
│   │   └── network_info.dart
│   ├── router/
│   │   └── app_router.dart
│   └── theme/
│       └── app_theme.dart
├── features/
│   └── auth/
│       ├── data/
│       │   ├── datasources/
│       │   ├── models/
│       │   └── repositories/
│       ├── domain/
│       │   ├── entities/
│       │   ├── repositories/
│       │   └── usecases/
│       └── presentation/
│           ├── providers/
│           ├── screens/
│           └── widgets/
├── shared/
│   ├── widgets/
│   └── extensions/
└── main.dart
```

**Core Setup:**
```dart
// lib/core/router/app_router.dart
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'app_router.g.dart';

@riverpod
GoRouter appRouter(AppRouterRef ref) {
  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomeScreen(),
        routes: [
          GoRoute(
            path: 'profile/:id',
            builder: (context, state) => ProfileScreen(
              userId: state.pathParameters['id']!,
            ),
          ),
        ],
      ),
    ],
    errorBuilder: (context, state) => ErrorScreen(error: state.error),
  );
}

// lib/main.dart
void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(
    ProviderScope(
      child: const MyApp(),
    ),
  );
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);

    return MaterialApp.router(
      routerConfig: router,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
    );
  }
}
```

### Workflow 2: State Management Implementation

**Time:** 1-2 hours per feature

**Steps:**
1. Define feature state model with Freezed
2. Create repository interface and implementation
3. Implement provider/notifier for state management
4. Build UI that reacts to state changes
5. Handle loading, error, and success states
6. Add unit tests for business logic

**Reference:** `references/state-management.md`

**Riverpod Pattern (Recommended):**
```dart
// Domain entity with Freezed
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    String? avatarUrl,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Repository interface
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<List<User>> getUsers();
  Future<void> updateUser(User user);
}

// Riverpod provider with AsyncNotifier
@riverpod
class UsersNotifier extends _$UsersNotifier {
  @override
  Future<List<User>> build() async {
    return ref.read(userRepositoryProvider).getUsers();
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() =>
      ref.read(userRepositoryProvider).getUsers()
    );
  }

  Future<void> updateUser(User user) async {
    await ref.read(userRepositoryProvider).updateUser(user);
    await refresh();
  }
}

// UI consumption
class UsersScreen extends ConsumerWidget {
  const UsersScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersNotifierProvider);

    return usersAsync.when(
      data: (users) => ListView.builder(
        itemCount: users.length,
        itemBuilder: (context, index) => UserTile(user: users[index]),
      ),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => ErrorWidget(
        error: error,
        onRetry: () => ref.read(usersNotifierProvider.notifier).refresh(),
      ),
    );
  }
}
```

**Bloc Pattern (Alternative):**
```dart
// Events
@freezed
class UserEvent with _$UserEvent {
  const factory UserEvent.loadUsers() = LoadUsers;
  const factory UserEvent.refreshUsers() = RefreshUsers;
  const factory UserEvent.updateUser(User user) = UpdateUser;
}

// State
@freezed
class UserState with _$UserState {
  const factory UserState.initial() = _Initial;
  const factory UserState.loading() = _Loading;
  const factory UserState.loaded(List<User> users) = _Loaded;
  const factory UserState.error(String message) = _Error;
}

// Bloc
class UserBloc extends Bloc<UserEvent, UserState> {
  final UserRepository _repository;

  UserBloc(this._repository) : super(const UserState.initial()) {
    on<LoadUsers>(_onLoadUsers);
    on<RefreshUsers>(_onRefreshUsers);
    on<UpdateUser>(_onUpdateUser);
  }

  Future<void> _onLoadUsers(LoadUsers event, Emitter<UserState> emit) async {
    emit(const UserState.loading());
    try {
      final users = await _repository.getUsers();
      emit(UserState.loaded(users));
    } catch (e) {
      emit(UserState.error(e.toString()));
    }
  }
}
```

### Workflow 3: Platform Channel Integration

**Time:** 2-4 hours per integration

**Steps:**
1. Define method channel contract
2. Implement Dart side with proper error handling
3. Implement iOS side (Swift)
4. Implement Android side (Kotlin)
5. Add platform availability checks
6. Test on both platforms
7. Document API for team

**Reference:** `references/dart-patterns.md`

**Dart Implementation:**
```dart
class NativeBattery {
  static const _channel = MethodChannel('com.example.app/battery');

  static Future<int> getBatteryLevel() async {
    try {
      final level = await _channel.invokeMethod<int>('getBatteryLevel');
      return level ?? -1;
    } on PlatformException catch (e) {
      throw BatteryException('Failed to get battery level: ${e.message}');
    }
  }

  static Stream<int> batteryLevelStream() {
    const eventChannel = EventChannel('com.example.app/battery_stream');
    return eventChannel
        .receiveBroadcastStream()
        .map((event) => event as int);
  }
}

// iOS Swift Implementation (ios/Runner/AppDelegate.swift)
/*
import Flutter
import UIKit

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    let controller = window?.rootViewController as! FlutterViewController
    let batteryChannel = FlutterMethodChannel(
      name: "com.example.app/battery",
      binaryMessenger: controller.binaryMessenger
    )

    batteryChannel.setMethodCallHandler { [weak self] call, result in
      if call.method == "getBatteryLevel" {
        self?.receiveBatteryLevel(result: result)
      } else {
        result(FlutterMethodNotImplemented)
      }
    }

    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }

  private func receiveBatteryLevel(result: FlutterResult) {
    let device = UIDevice.current
    device.isBatteryMonitoringEnabled = true
    let batteryLevel = Int(device.batteryLevel * 100)
    result(batteryLevel)
  }
}
*/

// Android Kotlin Implementation (android/app/src/main/kotlin/.../MainActivity.kt)
/*
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity: FlutterActivity() {
    private val CHANNEL = "com.example.app/battery"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler { call, result ->
                if (call.method == "getBatteryLevel") {
                    val batteryLevel = getBatteryLevel()
                    result.success(batteryLevel)
                } else {
                    result.notImplemented()
                }
            }
    }

    private fun getBatteryLevel(): Int {
        val batteryManager = getSystemService(BATTERY_SERVICE) as BatteryManager
        return batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
    }
}
*/
```

### Workflow 4: Widget Performance Optimization

**Time:** 2-4 hours per optimization session

**Steps:**
1. Profile with Flutter DevTools
2. Identify unnecessary rebuilds
3. Implement const constructors where possible
4. Use RepaintBoundary for complex widgets
5. Optimize list rendering with proper keys
6. Implement pagination for large datasets
7. Re-profile to verify improvements

**Reference:** `references/widget-architecture.md`

**Performance Patterns:**
```dart
// AVOID: Widget rebuilds entire subtree
class BadExample extends StatelessWidget {
  final List<Item> items;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // This header rebuilds when items change
        const Header(),
        ListView.builder(
          itemCount: items.length,
          itemBuilder: (context, index) => ItemTile(item: items[index]),
        ),
      ],
    );
  }
}

// BETTER: Isolate rebuilds with proper structure
class GoodExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Header never rebuilds
        const Header(),
        // Only list area rebuilds
        Expanded(
          child: Consumer<ItemsProvider>(
            builder: (context, provider, _) => ListView.builder(
              itemCount: provider.items.length,
              itemBuilder: (context, index) => ItemTile(
                key: ValueKey(provider.items[index].id),
                item: provider.items[index],
              ),
            ),
          ),
        ),
      ],
    );
  }
}

// Use RepaintBoundary for expensive widgets
class ExpensiveAnimation extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      child: CustomPaint(
        painter: ComplexAnimationPainter(),
        size: const Size(200, 200),
      ),
    );
  }
}

// Optimize images
class OptimizedImage extends StatelessWidget {
  final String url;

  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: url,
      // Resize to actual display size
      memCacheWidth: 200,
      memCacheHeight: 200,
      placeholder: (context, url) => const ShimmerPlaceholder(),
      errorWidget: (context, url, error) => const Icon(Icons.error),
    );
  }
}
```

## Dart Patterns

### Null Safety and Pattern Matching

```dart
// Pattern matching with Dart 3
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  final T data;
  const Success(this.data);
}

class Failure<T> extends Result<T> {
  final Exception error;
  const Failure(this.error);
}

// Using pattern matching
void handleResult(Result<User> result) {
  switch (result) {
    case Success(data: final user):
      print('User: ${user.name}');
    case Failure(error: final e):
      print('Error: $e');
  }
}

// Records for multiple return values
(String, int) getUserInfo() {
  return ('John', 30);
}

void main() {
  final (name, age) = getUserInfo();
  print('$name is $age years old');
}
```

### Extension Methods

```dart
extension StringExtensions on String {
  String get capitalize =>
    isEmpty ? this : '${this[0].toUpperCase()}${substring(1)}';

  bool get isValidEmail =>
    RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);
}

extension ContextExtensions on BuildContext {
  ThemeData get theme => Theme.of(this);
  TextTheme get textTheme => theme.textTheme;
  ColorScheme get colorScheme => theme.colorScheme;

  void showSnackBar(String message) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }
}

// Usage
final email = 'test@example.com';
if (email.isValidEmail) {
  context.showSnackBar('Valid email!');
}
```

### Async Patterns

```dart
// Proper async error handling
Future<Result<User>> fetchUser(String id) async {
  try {
    final response = await dio.get('/users/$id');
    return Success(User.fromJson(response.data));
  } on DioException catch (e) {
    return Failure(NetworkException(e.message ?? 'Network error'));
  } catch (e) {
    return Failure(UnknownException(e.toString()));
  }
}

// Stream transformations
Stream<List<Message>> watchMessages(String chatId) {
  return firestore
      .collection('chats')
      .doc(chatId)
      .collection('messages')
      .orderBy('timestamp', descending: true)
      .limit(50)
      .snapshots()
      .map((snapshot) => snapshot.docs
          .map((doc) => Message.fromFirestore(doc))
          .toList());
}
```

## References

- **[dart-patterns.md](references/dart-patterns.md)** - Dart 3.x patterns, null safety, async
- **[widget-architecture.md](references/widget-architecture.md)** - Widget lifecycle, keys, render objects
- **[state-management.md](references/state-management.md)** - Provider, Riverpod, Bloc comparison

## Tools Integration

This skill uses Python tools from the `senior-mobile` skill:

```bash
# Generate Flutter project structure
python3 ../../senior-mobile/scripts/mobile_scaffolder.py \
  --framework flutter \
  --navigation go-router \
  --state riverpod

# Detect Flutter project configuration
python3 ../../senior-mobile/scripts/platform_detector.py --check all

# Validate for Play Store
python3 ../../senior-mobile/scripts/app_store_validator.py --store google
```

## Best Practices

### Widget Design
- Keep widgets small and focused (single responsibility)
- Use composition over inheritance
- Implement const constructors
- Separate logic from UI
- Use proper keys for dynamic lists

### State Management
- Choose one pattern and use consistently
- Keep state as local as possible
- Avoid global state when possible
- Test business logic independently

### Performance
- Profile before optimizing
- Use lazy loading for large lists
- Implement image caching
- Minimize widget rebuilds
- Use isolates for heavy computation

### Testing
- Unit test business logic
- Widget test UI components
- Integration test critical flows
- Use golden tests for visual regression

## Success Metrics

- **UI Development Speed:** 55% faster with hot reload
- **Code Sharing:** 90%+ across platforms
- **App Performance:** 60 FPS on mid-range devices
- **Test Coverage:** 80%+ for business logic
