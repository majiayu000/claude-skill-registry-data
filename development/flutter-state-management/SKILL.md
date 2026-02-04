---
name: flutter-state-management
description: Master Flutter state management with BLoC, Riverpod, Provider, and GetX. Learn when to use each solution and implement scalable state patterns. Use for choosing and implementing state management in Flutter apps.
---

# Flutter State Management

Comprehensive guide to state management in Flutter, covering BLoC, Riverpod, Provider, GetX, and other modern patterns for building scalable Flutter applications.

## When to Use This Skill

- Choosing the right state management solution
- Implementing BLoC pattern with flutter_bloc
- Using Riverpod for dependency injection and state
- Migrating from one state management to another
- Scaling state management in large apps
- Testing state management logic
- Implementing reactive patterns
- Managing complex application state
- Handling asynchronous state updates
- Building offline-first applications

## Core Concepts

### 1. State Management Overview
- **Local state**: State needed by a single widget
- **App state**: State shared across widgets
- **Ephemeral state**: Temporary UI state
- **Application state**: Business logic and data
- **Persistent state**: Data that survives app restarts
- **Derived state**: Computed from other state

### 2. When to Use Each Solution
- **setState**: Simple local widget state
- **InheritedWidget/Provider**: Simple dependency injection
- **Riverpod**: Modern DI with compile-time safety
- **BLoC**: Complex business logic, testability
- **GetX**: Rapid development, minimal boilerplate
- **Redux**: Predictable state with time-travel debugging
- **MobX**: Reactive programming with observables

## BLoC Pattern (Business Logic Component)

### Pattern 1: Basic BLoC Implementation

```dart
// Event
abstract class CounterEvent {}

class IncrementCounter extends CounterEvent {}

class DecrementCounter extends CounterEvent {}

// State
class CounterState {
  final int count;

  const CounterState(this.count);
}

// BLoC
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(const CounterState(0)) {
    on<IncrementCounter>(_onIncrement);
    on<DecrementCounter>(_onDecrement);
  }

  void _onIncrement(IncrementCounter event, Emitter<CounterState> emit) {
    emit(CounterState(state.count + 1));
  }

  void _onDecrement(DecrementCounter event, Emitter<CounterState> emit) {
    emit(CounterState(state.count - 1));
  }
}

// UI
class CounterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => CounterBloc(),
      child: CounterView(),
    );
  }
}

class CounterView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(
        child: BlocBuilder<CounterBloc, CounterState>(
          builder: (context, state) {
            return Text('${state.count}', style: Theme.of(context).textTheme.headlineLarge);
          },
        ),
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: () => context.read<CounterBloc>().add(IncrementCounter()),
            child: const Icon(Icons.add),
          ),
          const SizedBox(height: 8),
          FloatingActionButton(
            onPressed: () => context.read<CounterBloc>().add(DecrementCounter()),
            child: const Icon(Icons.remove),
          ),
        ],
      ),
    );
  }
}
```

### Pattern 2: BLoC with API Calls

```dart
// States with sealed classes
sealed class UserState {}

class UserInitial extends UserState {}

class UserLoading extends UserState {}

class UserLoaded extends UserState {
  final List<User> users;
  UserLoaded(this.users);
}

class UserError extends UserState {
  final String message;
  UserError(this.message);
}

// Events
sealed class UserEvent {}

class LoadUsers extends UserEvent {}

class RefreshUsers extends UserEvent {}

// BLoC with API call
class UserBloc extends Bloc<UserEvent, UserState> {
  final UserRepository repository;

  UserBloc({required this.repository}) : super(UserInitial()) {
    on<LoadUsers>(_onLoadUsers);
    on<RefreshUsers>(_onRefreshUsers);
  }

  Future<void> _onLoadUsers(LoadUsers event, Emitter<UserState> emit) async {
    emit(UserLoading());

    try {
      final users = await repository.getUsers();
      emit(UserLoaded(users));
    } catch (e) {
      emit(UserError(e.toString()));
    }
  }

  Future<void> _onRefreshUsers(RefreshUsers event, Emitter<UserState> emit) async {
    // Keep current state while refreshing
    try {
      final users = await repository.getUsers();
      emit(UserLoaded(users));
    } catch (e) {
      emit(UserError(e.toString()));
    }
  }
}

// UI with BlocBuilder
class UserListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => UserBloc(
        repository: context.read<UserRepository>(),
      )..add(LoadUsers()),
      child: Scaffold(
        appBar: AppBar(title: const Text('Users')),
        body: BlocBuilder<UserBloc, UserState>(
          builder: (context, state) {
            return switch (state) {
              UserInitial() => const Center(child: Text('Press button to load')),
              UserLoading() => const Center(child: CircularProgressIndicator()),
              UserLoaded(users: var users) => ListView.builder(
                itemCount: users.length,
                itemBuilder: (context, index) {
                  final user = users[index];
                  return ListTile(
                    title: Text(user.name),
                    subtitle: Text(user.email),
                  );
                },
              ),
              UserError(message: var message) => Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('Error: $message'),
                    ElevatedButton(
                      onPressed: () => context.read<UserBloc>().add(LoadUsers()),
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            };
          },
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () => context.read<UserBloc>().add(RefreshUsers()),
          child: const Icon(Icons.refresh),
        ),
      ),
    );
  }
}
```

## Riverpod

### Pattern 3: Basic Riverpod Provider

```dart
// Provider
final counterProvider = StateProvider<int>((ref) => 0);

// UI
class CounterPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(
        child: Text('$count', style: Theme.of(context).textTheme.headlineLarge),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.read(counterProvider.notifier).state++,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### Pattern 4: Riverpod with AsyncNotifier

```dart
// Model
class User {
  final String id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});
}

// AsyncNotifier
class UserListNotifier extends AsyncNotifier<List<User>> {
  @override
  Future<List<User>> build() async {
    // Load initial data
    return _fetchUsers();
  }

  Future<List<User>> _fetchUsers() async {
    final repository = ref.read(userRepositoryProvider);
    return repository.getUsers();
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() => _fetchUsers());
  }

  Future<void> addUser(User user) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(userRepositoryProvider);
      await repository.addUser(user);
      return _fetchUsers();
    });
  }
}

// Provider
final userListProvider = AsyncNotifierProvider<UserListNotifier, List<User>>(() {
  return UserListNotifier();
});

// UI
class UserListPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(userListProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Users')),
      body: usersAsync.when(
        data: (users) => ListView.builder(
          itemCount: users.length,
          itemBuilder: (context, index) {
            final user = users[index];
            return ListTile(
              title: Text(user.name),
              subtitle: Text(user.email),
            );
          },
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Error: $error'),
              ElevatedButton(
                onPressed: () => ref.refresh(userListProvider),
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.read(userListProvider.notifier).refresh(),
        child: const Icon(Icons.refresh),
      ),
    );
  }
}
```

### Pattern 5: Riverpod Family and AutoDispose

```dart
// Provider with parameter (family)
final userProvider = FutureProvider.autoDispose.family<User, String>((ref, userId) async {
  final repository = ref.watch(userRepositoryProvider);
  return repository.getUser(userId);
});

// UI
class UserDetailPage extends ConsumerWidget {
  final String userId;

  const UserDetailPage({required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider(userId));

    return Scaffold(
      appBar: AppBar(title: const Text('User Details')),
      body: userAsync.when(
        data: (user) => Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Name: ${user.name}'),
              Text('Email: ${user.email}'),
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Error: $error')),
      ),
    );
  }
}
```

## Provider Pattern

### Pattern 6: ChangeNotifier with Provider

```dart
// Model
class Counter extends ChangeNotifier {
  int _count = 0;

  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }

  void decrement() {
    _count--;
    notifyListeners();
  }
}

// Main app setup
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => Counter(),
      child: MyApp(),
    ),
  );
}

// UI
class CounterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(
        child: Consumer<Counter>(
          builder: (context, counter, child) {
            return Text('${counter.count}', style: Theme.of(context).textTheme.headlineLarge);
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.read<Counter>().increment(),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## GetX

### Pattern 7: GetX Controller

```dart
// Controller
class CounterController extends GetxController {
  final count = 0.obs;

  void increment() => count.value++;
  void decrement() => count.value--;
}

// UI
class CounterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final controller = Get.put(CounterController());

    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(
        child: Obx(() => Text(
          '${controller.count}',
          style: Theme.of(context).textTheme.headlineLarge,
        )),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: controller.increment,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## Testing State Management

### Pattern 8: Testing BLoC

```dart
void main() {
  group('CounterBloc', () {
    late CounterBloc bloc;

    setUp(() {
      bloc = CounterBloc();
    });

    tearDown(() {
      bloc.close();
    });

    test('initial state is 0', () {
      expect(bloc.state.count, 0);
    });

    blocTest<CounterBloc, CounterState>(
      'emits [1] when IncrementCounter is added',
      build: () => CounterBloc(),
      act: (bloc) => bloc.add(IncrementCounter()),
      expect: () => [const CounterState(1)],
    );

    blocTest<CounterBloc, CounterState>(
      'emits [1, 2] when IncrementCounter is added twice',
      build: () => CounterBloc(),
      act: (bloc) {
        bloc.add(IncrementCounter());
        bloc.add(IncrementCounter());
      },
      expect: () => [
        const CounterState(1),
        const CounterState(2),
      ],
    );
  });
}
```

### Pattern 9: Testing Riverpod

```dart
void main() {
  test('counterProvider initial value is 0', () {
    final container = ProviderContainer();
    addTearDown(container.dispose);

    expect(container.read(counterProvider), 0);
  });

  test('counterProvider can be incremented', () {
    final container = ProviderContainer();
    addTearDown(container.dispose);

    container.read(counterProvider.notifier).state++;

    expect(container.read(counterProvider), 1);
  });

  test('userListProvider loads users', () async {
    final container = ProviderContainer(
      overrides: [
        userRepositoryProvider.overrideWithValue(MockUserRepository()),
      ],
    );
    addTearDown(container.dispose);

    // Wait for the provider to load
    await container.read(userListProvider.future);

    final users = container.read(userListProvider).value;
    expect(users, isNotEmpty);
  });
}
```

## Best Practices

### State Management Selection
1. **Use setState** for simple, local widget state
2. **Use InheritedWidget/Provider** for simple dependency injection
3. **Use Riverpod** for modern apps with compile-time safety
4. **Use BLoC** for complex business logic and high testability
5. **Use GetX** for rapid prototyping with minimal boilerplate
6. **Avoid mixing** multiple state management solutions

### Architecture Patterns
- Separate business logic from UI
- Use repositories for data access
- Implement proper error handling
- Make state immutable when possible
- Test business logic independently
- Use dependency injection
- Follow single responsibility principle
- Keep widgets focused on UI

### Performance Tips
- Use const constructors for widgets
- Avoid rebuilding entire widget trees
- Use selectors to listen to specific state
- Implement proper equality for state classes
- Dispose resources properly
- Use AutoDispose in Riverpod
- Profile widget rebuilds with DevTools

## Resources

- **BLoC Library**: https://bloclibrary.dev
- **Riverpod**: https://riverpod.dev
- **Provider**: https://pub.dev/packages/provider
- **GetX**: https://pub.dev/packages/get
- **Flutter State Management**: https://docs.flutter.dev/data-and-backend/state-mgmt
