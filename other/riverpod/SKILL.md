---
name: flutter-riverpod-pattern
description: Implements state management in Flutter applications using Riverpod 3.x and Code Generation.
tags: [flutter, riverpod, state-management, providers]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Riverpod Pattern (3.x)

## Context

Apply when creating or modifying state management using Riverpod in Flutter projects. We use **Riverpod 3.x** with code generation (`riverpod_annotation`).

> **3.0 Migration**: `AutoDisposeNotifier`, `FamilyNotifier`, and per-provider `Ref` subclasses (`ExampleRef`, `FutureProviderRef`) are removed — use `Notifier` and `Ref` everywhere. `StateProvider`/`StateNotifierProvider`/`ChangeNotifierProvider` moved to `package:riverpod/legacy.dart`.

## Instructions

1. **Code Generation**: Always use `@riverpod` and `riverpod_annotation`. Never manually write `Provider`, `FutureProvider`, etc.
2. **State classes**: Use `freezed` for complex states, or `AsyncValue` for async operations.
3. **Naming**: Class `FeatureName` extending `_$FeatureName`, file `feature_name_provider.dart`.
4. **File structure**:
   ```text
   feature_name/
   ├── providers/
   │   └── feature_name_provider.dart
   ├── pages/
   │   └── feature_name_page.dart
   └── widgets/
       └── ...
   ```
5. **Never** put business logic in widgets — delegate to Notifiers.
6. **Use** `ConsumerWidget` or `ConsumerStatefulWidget`.
7. **Error handling**: Use `AsyncValue.guard()` for async error handling.
8. **Unified Ref**: Always use `Ref` in code-gen — not `ExampleRef` or typed variants.
   ```dart
   @riverpod
   Example example(Ref ref) => Example(); // ✅ 3.x
   // Example example(ExampleRef ref) => Example(); // ❌ 2.x removed
   ```

## Provider Lifecycle

### Global Singleton (`keepAlive: true`)
```dart
@Riverpod(keepAlive: true)
class UserRepository extends _$UserRepository {
  @override
  FutureOr<void> build() { /* init */ }
}
```

### autoDispose (Default)
```dart
@riverpod
class TaskList extends _$TaskList {
  @override
  FutureOr<List<Task>> build() async {
    return ref.watch(userRepositoryProvider.notifier).fetchTasks();
  }
}
```

### `Ref.mounted` — Safety after async gaps
Riverpod 3.0 throws if you interact with a disposed Ref/Notifier. Always check after async:
```dart
Future<void> addTodo(String title) async {
  final newTodo = await api.addTodo(title);
  if (!ref.mounted) return; // Must check after await
  state = [...state, newTodo];
}
```

## Automatic Retry

Providers auto-retry on failure (200ms exponential backoff up to 6.4s). Configure globally or per-provider:

```dart
// Global
ProviderScope(
  retry: (retryCount, error) {
    if (error is ProviderException) return null;
    if (retryCount > 5) return null;
    return Duration(seconds: retryCount * 2);
  },
  child: MyApp(),
);

// Per-provider
Duration? myRetry(int retryCount, Object error) => retryCount > 3 ? null : Duration(seconds: retryCount * 2);

@Riverpod(retry: myRetry)
class TodoList extends _$TodoList {
  @override
  List<Todo> build() => [];
}
```

## Mutations (Experimental)

React to side-effects with loading/success/error states. Prevents disposal during in-flight operations:

```dart
final addTodoMutation = Mutation<void>();

class AddTodoButton extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final addTodo = ref.watch(addTodoMutation);
    return switch (addTodo) {
      MutationIdle() => ElevatedButton(
          onPressed: () => addTodoMutation.run(ref, (tsx) async {
            await tsx.get(todoListProvider.notifier).addTodo('New Todo');
          }),
          child: const Text('Submit'),
        ),
      MutationPending() => const CircularProgressIndicator(),
      MutationError() => const Text('Failed'),
      MutationSuccess() => const Text('Done!'),
    };
  }
}
```

> Use `tsx.get()` instead of `ref.read()` — keeps provider alive until mutation completes.

## Offline Persistence (Experimental)

```dart
@riverpod
@JsonPersist()
class TodosNotifier extends _$TodosNotifier {
  @override
  FutureOr<List<Todo>> build() async {
    persist(ref.watch(storageProvider.future));
    return await fetchTodos();
  }
}
```

## AsyncValue (Sealed in 3.0)

Exhaustive pattern matching, renamed `valueOrNull` → `value`, progress support:

```dart
return switch (ref.watch(myProvider)) {
  AsyncData(:final value) => Text('$value'),
  AsyncError(:final error) => Text('Error: $error'),
  AsyncLoading(:final progress) => LinearProgressIndicator(value: progress),
};
```

- `AsyncValue.isFromCache` — true when from offline persistence
- `AsyncLoading(progress: 0.5)` — optional progress reporting

## Form Management (Reactive Forms)

When handling forms, encapsulate the `FormGroup` within the `Action Notifier`. This keeps validation logic out of the UI and ensures the form state is disposed of correctly.

### Implementation Pattern
1. **Initialize**: Create the `FormGroup` in the `build()` method.
2. **Dispose**: Register `form.dispose` in `ref.onDispose`.
3. **Validate**: Perform validation before executing side effects.
4. **Access**: Retrieve values directly from the form controls.

```dart
@riverpod
class LoginNotifier extends _$LoginNotifier {
  late final FormGroup form;

  @override
  FutureOr<void> build() {
    form = fb.group({
      'email': ['', Validators.required, Validators.email],
      'password': ['', Validators.required],
    });

    // Ensure form is disposed when provider is disposed
    ref.onDispose(form.dispose);
  }

  Future<void> login() async {
    if (form.invalid) {
      form.markAllAsTouched();
      return;
    }

    state = const AsyncValue.loading();
    // Use form.control('name').value to get data
    final result = await ref.read(authRepositoryProvider).login(
      email: form.control('email').value,
      password: form.control('password').value,
    );
    
    // ... handle result
  }
}
```

## UI Performance & Optimization

### 1. Selective Rebuilds (`ref.select`)
```dart
final name = ref.watch(userProvider.select((u) => u.name)); // Only rebuilds on name change
```

### 2. Granular Rebuilds (`Consumer`)
```dart
Consumer(
  builder: (context, ref, child) {
    final themeMode = ref.watch(settingsProvider.select((s) => s.themeMode));
    return Text('Current mode: $themeMode');
  },
)
```

### 3. Side Effects (`ref.listen`)
```dart
ref.listen(authProvider, (previous, next) {
  if (next is AsyncError) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$next')));
  }
});
```

### 4. Pause/Resume & Weak Listeners
Invisible widget listeners are auto-paused via `TickerMode`. Manual control:
```dart
final sub = ref.listen(provider, (prev, next) {});
sub.pause();
sub.resume();

// Weak: listen without preventing auto-dispose
ref.listen(provider, weak: true, (prev, next) {});
```

### 5. List Optimization (Family)
```dart
@riverpod
Task individualTask(Ref ref, String taskId) {
  return ref.watch(taskListProvider).value!.firstWhere((t) => t.id == taskId);
}
// Widget: ref.watch(individualTaskProvider(id))
```

## Testing

```dart
// Auto-disposing container
final container = ProviderContainer.test();

// Mock only build method
myProvider.overrideWithBuild((ref) => 42);

// Override with value
myFutureProvider.overrideWithValue(AsyncValue.data(42));

// Widget test container access
ProviderContainer container = tester.container();
```

## Anti-patterns

- ❌ Watching global state without `.select`
- ❌ Business logic in `build()` — use computed providers
- ❌ Missing `const` constructors for static widgets
- ❌ Passing `WidgetRef` to child widgets — use `Consumer`
- ❌ Using `setState` for provider-managed data
- ❌ Using legacy providers (`StateProvider`, etc.) in new code
- ❌ Using typed Ref (`ExampleRef`) — use `Ref`
- ❌ Ignoring `ref.mounted` after async gaps

## Resources

- https://riverpod.dev/docs/whats_new
- https://riverpod.dev/docs/3.0_migration
- https://riverpod.dev/docs/concepts2/providers
- https://riverpod.dev/docs/concepts2/mutations
- https://riverpod.dev/docs/concepts2/offline
- https://riverpod.dev/docs/concepts2/retry
- https://pub.dev/packages/riverpod_annotation
