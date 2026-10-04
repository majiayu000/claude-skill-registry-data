---
name: flutter-patterns
description: Provides production Flutter and Dart 3 patterns covering widget composition, state management choice (Riverpod, BLoC, plain ChangeNotifier), immutability with freezed and records, sealed-class state, async and streams, Firebase usage (Auth, Firestore, Functions), navigation, and widget/integration testing. Use when writing, reviewing, or architecting Flutter apps or Dart packages.
---

# Flutter Patterns

Small const widgets, immutable state modelled with sealed types, side effects in a thin layer
above the UI, and tests at the widget boundary. Dart 3 features (records, patterns, sealed
classes) are assumed.

## When to use

- Starting a Flutter feature and choosing how to structure widgets and state.
- Reviewing Dart for null safety, immutability, async correctness, or rebuild scope.
- Integrating Firebase services in a Flutter app.
- Writing widget, unit, or integration tests.

## Null safety and Dart idioms

```dart
// Avoid `!`; use `?.`, `??`, guards, or pattern matching
final name = user?.name ?? 'Guest';

String describe(User? user) => switch (user) {
  User(:final name, :final email) => '$name <$email>',
  null => 'Guest',
};

// `late` only when initialisation is guaranteed before first read (initState)
late final AnimationController _controller;
```

- Prefer `final` everywhere; `var` only when reassignment is intended.
- `firstWhereOrNull` (package:collection) instead of `firstWhere` with a throwing `orElse`.
- Exhaustive `switch` expressions over `if` chains for sealed types and enums.
- Records for lightweight multi-value returns: `(int count, double total) summarise(...)`.

## Immutability

### Sealed classes for state

```dart
sealed class LoadState<T> {
  const LoadState();
}
final class Loading<T> extends LoadState<T> { const Loading(); }
final class Loaded<T> extends LoadState<T> { const Loaded(this.data); final T data; }
final class Failed<T> extends LoadState<T> { const Failed(this.error); final Object error; }

Widget render(LoadState<List<Item>> state) => switch (state) {
  Loading() => const CircularProgressIndicator(),
  Loaded(:final data) => ItemList(items: data),
  Failed(:final error) => ErrorView(message: '$error'),
};
```

The compiler enforces every branch; adding a state variant breaks every incomplete switch at
build time, which is exactly what you want.

### freezed for data classes

```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    @Default(false) bool isAdmin,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

final updated = user.copyWith(name: 'New name');   // never mutate, always copy
```

Use freezed for models that cross a boundary (JSON, Firestore documents, state objects with
several fields). Use a plain `const` class with `final` fields for two- or three-field values,
and records for ad-hoc tuples. Run `dart run build_runner build --delete-conflicting-outputs`
after model changes; commit the generated files.

## Widget composition

**Extract to classes, not methods.** A `_buildHeader()` method rebuilds with its parent and
cannot be `const`; a `_Header` widget can be skipped by the framework.

```dart
class _Header extends StatelessWidget {
  const _Header(this.title);
  final String title;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.all(16),
    child: Text(title, style: Theme.of(context).textTheme.headlineMedium),
  );
}
```

**Push rebuilds to the leaves.** The widget that watches state should be as small as possible.

```dart
class CounterPage extends StatelessWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context) => const Scaffold(
    body: Column(children: [
      ExpensiveHeader(),   // const: never rebuilt
      _CounterText(),      // only this watches the provider
      ExpensiveFooter(),
    ]),
  );
}

class _CounterText extends ConsumerWidget {
  const _CounterText();
  @override
  Widget build(BuildContext context, WidgetRef ref) => Text('${ref.watch(counterProvider)}');
}
```

- `const` constructors and `const` child trees wherever the values are compile-time constants.
- Widgets take data and callbacks; they do not fetch, persist, or navigate on their own.
- Keep `build` free of side effects and heavy work; compute in the state layer.
- Use `Theme.of(context)` tokens, not hardcoded colours and sizes.
- `ListView.builder` / `SliverList` for anything longer than a screen; never a `Column` of
  hundreds of children.

## State management

Pick one approach per app and hold to it.

| Situation | Choice |
|---|---|
| Local, ephemeral UI state (a toggle, a text field, an animation) | `StatefulWidget` + `setState` |
| App or feature state, most new apps | Riverpod (code-generated providers) |
| Teams that want explicit event -> state transitions and event logs | BLoC / Cubit |
| Tiny app or package with no dependency budget | `ChangeNotifier` + `ListenableBuilder` |

### Riverpod

```dart
@riverpod
Future<List<Product>> products(Ref ref) async {
  final repo = ref.watch(productRepositoryProvider);
  return repo.fetchAll();
}

@riverpod
class Cart extends _$Cart {
  @override
  List<CartItem> build() => const [];

  void add(Product product) {
    final existing = state.firstWhereOrNull((i) => i.productId == product.id);
    state = existing == null
        ? [...state, CartItem(productId: product.id, quantity: 1)]
        : [for (final i in state) i.productId == product.id ? i.copyWith(quantity: i.quantity + 1) : i];
  }
}

@riverpod
int cartCount(Ref ref) => ref.watch(cartProvider).length;   // derived, cached
```

`ref.watch` in build, `ref.read` in callbacks, `ref.listen` for one-shot reactions (snackbars,
navigation). Derived providers replace manual selectors.

### Cubit

```dart
class AuthCubit extends Cubit<AuthState> {
  AuthCubit(this._auth) : super(const AuthState.initial());
  final AuthService _auth;

  Future<void> signIn(String email, String password) async {
    emit(const AuthState.loading());
    try {
      emit(AuthState.authenticated(await _auth.signIn(email, password)));
    } on AuthException catch (e) {
      emit(AuthState.error(e.message));
    }
  }
}
```

## Async and streams

```dart
// Concurrent futures with record destructuring
final (users, orders) = await (userRepo.fetchAll(), orderRepo.recent()).wait;

// Always guard BuildContext after an await
Future<void> _submit() async {
  setState(() => _busy = true);
  try {
    await _service.save(_draft);
    if (!mounted) return;
    context.go('/done');
  } on ServiceException catch (e) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
  } finally {
    if (mounted) setState(() => _busy = false);
  }
}

// Streams: expose from the repository, consume declaratively
Stream<List<Message>> watchThread(String id) => _source.watch(id).map(Message.listFrom);

StreamBuilder<List<Message>>(
  stream: repo.watchThread(threadId),
  builder: (context, snapshot) => switch (snapshot) {
    AsyncSnapshot(connectionState: ConnectionState.waiting) => const Loader(),
    AsyncSnapshot(:final error?) => ErrorView(message: '$error'),
    AsyncSnapshot(:final data?) => MessageList(messages: data),
    _ => const SizedBox.shrink(),
  },
)
```

- Never store a `StreamSubscription` without cancelling it in `dispose`; prefer `StreamBuilder`
  or a provider that manages the lifecycle.
- Wrap external failures in typed exceptions at the repository layer; the UI never catches
  `FirebaseException` directly.
- Cancel or debounce user-driven async work (search-as-you-type) so stale results cannot
  overwrite fresh ones.

## Firebase usage patterns

Keep Firebase behind repository interfaces so widgets and state classes depend on your types,
not on the SDK, and tests can substitute fakes.

```dart
abstract interface class NotesRepository {
  Stream<List<Note>> watchAll(String uid);
  Future<void> upsert(Note note);
}

class FirestoreNotesRepository implements NotesRepository {
  FirestoreNotesRepository(this._db);
  final FirebaseFirestore _db;

  CollectionReference<Note> _notes(String uid) => _db
      .collection('users').doc(uid).collection('notes')
      .withConverter<Note>(
        fromFirestore: (snap, _) => Note.fromJson({...snap.data()!, 'id': snap.id}),
        toFirestore: (note, _) => note.toJson()..remove('id'),
      );

  @override
  Stream<List<Note>> watchAll(String uid) => _notes(uid)
      .orderBy('updatedAt', descending: true)
      .snapshots()
      .map((s) => s.docs.map((d) => d.data()).toList());

  @override
  Future<void> upsert(Note note) => _notes(note.ownerId).doc(note.id).set(note, SetOptions(merge: true));
}
```

- **Auth**: expose `authStateChanges()` as a provider; derive a sealed `AuthStatus` from it and
  drive router redirects from that, not from widgets checking `currentUser` directly.
- **Firestore**: always `withConverter`; model documents with freezed; keep per-user data under
  `users/{uid}/...` so security rules stay simple; paginate with `limit` + `startAfterDocument`;
  never query unbounded collections into memory.
- **Security rules are the real authorisation layer.** Client checks are UX, not security. Test
  rules with the emulator.
- **Cloud Functions**: call via `FirebaseFunctions.instance.httpsCallable('name')`, wrap the
  result in a typed model, and map `FirebaseFunctionsException` codes to your own exceptions.
- **Emulators** for local development and integration tests: `firebase emulators:start`, then
  `useAuthEmulator`, `useFirestoreEmulator` behind a `kDebugMode` or `--dart-define` flag.
- **Crashlytics**: hook `FlutterError.onError` and `PlatformDispatcher.instance.onError` in
  `main()`; record handled exceptions from the repository layer with context.

## Navigation

Use `go_router` with a `refreshListenable` bound to the auth stream so redirects re-evaluate
when auth changes. Typed routes (`go_router_builder`) remove string paths from widgets. Keep
route definitions in one file; widgets call `context.go`/`context.push` with route objects.

## Error handling

```dart
void main() {
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    crashReporter.recordFlutterError(details);
  };
  PlatformDispatcher.instance.onError = (error, stack) {
    crashReporter.record(error, stack, fatal: true);
    return true;
  };
  runApp(const ProviderScope(child: App()));
}
```

- Repository layer converts SDK exceptions into a small app exception hierarchy.
- State layer turns exceptions into `Failed` states; the UI renders them.
- Replace the red `ErrorWidget` in release builds with `ErrorWidget.builder`.

## Testing

```dart
// Unit: pure logic and notifiers, with fakes
test('cart total sums price times quantity', () {
  final cart = Cart()..add(product(price: 250))..add(product(price: 250));
  expect(cart.total, 500);
});

// Widget: render with overrides, assert on what the user sees
testWidgets('shows item count badge', (tester) async {
  await tester.pumpWidget(ProviderScope(
    overrides: [cartProvider.overrideWith(() => FakeCart(count: 3))],
    child: const MaterialApp(home: CartBadge()),
  ));
  expect(find.text('3'), findsOneWidget);
});

// Golden: visual regression for design-system widgets
await expectLater(find.byType(PrimaryButton), matchesGoldenFile('primary_button.png'));

// Integration (integration_test/app_test.dart): a real flow on a device or emulator
testWidgets('sign in and reach home', (tester) async {
  await tester.pumpWidget(const App());
  await tester.enterText(find.byKey(const Key('email')), 'user@example.com');
  await tester.tap(find.text('Sign in'));
  await tester.pumpAndSettle();
  expect(find.text('Home'), findsOneWidget);
});
```

- Fakes over mocks: a `FakeNotesRepository` backed by a list is easier to reason about than a
  mock with stubbed calls.
- `pumpAndSettle` for animations; plain `pump` with a duration when something never settles
  (an infinite spinner).
- Find by `Key`, semantics label, or visible text; not by widget type when the type is generic.
- Firebase-backed flows run against the emulator suite in `integration_test`, never production.
- Commands: `flutter test`, `flutter test --coverage`, `flutter test integration_test`,
  `flutter test --update-goldens`.

## Anti-patterns

- `user!.name` where `user?.name ?? default` was possible.
- Widget-returning private methods instead of widget classes.
- `setState` for anything read outside the widget.
- `context` used after an `await` without a `mounted` check.
- Firestore queries or `FirebaseAuth.instance` calls inside `build`.
- A `Column` inside `SingleChildScrollView` for a long list.
- Catching `Exception` in the UI and showing `e.toString()`.
- Tests that pump the whole app to check one widget.

## Review checklist

- [ ] `dart analyze` clean; `flutter test` green.
- [ ] State is sealed/immutable; updates create new objects.
- [ ] Rebuild scope is minimal; `const` used where possible.
- [ ] Every `await` in a widget is followed by a `mounted` guard before using `context`.
- [ ] Firebase is behind repositories with `withConverter`; rules cover every access.
- [ ] Subscriptions and controllers are disposed.
- [ ] New behaviour has a widget or unit test that fails without it.

## Related skills

- `opm:tdd-workflow` - `flutter test` RED/GREEN cycle.
- `opm:verification-loop` - `dart analyze` and `flutter test` as the release gate.

<!-- Adapted from affaan-m/ecc (MIT) -->
