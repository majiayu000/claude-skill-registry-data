---
name: flutter-testing
description: "Authors Flutter tests across the three-layer pyramid - unit (`flutter test`), widget (`testWidgets` + `WidgetTester`), integration (`integration_test` on simulator/emulator/device). Picks the right layer per change, mocks via `mockito` + `build_runner`, LCOV coverage, CI with the Flutter Action. Use when the app is Flutter and the team wants its first-party stack. For React Native use detox-testing; for black-box cross-platform use appium-testing; for YAML-declarative flows use maestro-flows."
---

# flutter-testing

## Overview

Per [flutter-testing-doc][ft]:

[ft]: https://docs.flutter.dev/testing/overview

> "Flutter uses a **testing pyramid** approach with three main
> categories":
>
> 1. **Unit Tests** - single function / method / class; mocked
>    dependencies; quick.
> 2. **Widget Tests** - single widget; UI + lifecycle + interactions;
>    quick.
> 3. **Integration Tests** - full app or large sections; on real
>    devices/emulators; highest confidence; slowest.

The framework ships first-party tooling for all three layers.

## When to use

- The app is Flutter (the framework's intended use case).
- The team uses Dart and wants test-stack consistency with
  production code.

## Step 1 - Install

Flutter ships with `flutter_test` (in the SDK). For mocks:

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
  mockito: ^5.4.4
  build_runner: ^2.4.13
```

## Step 2 - Unit tests

Pure-Dart functions with mocked dependencies:

```dart
// test/cart_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/cart.dart';

void main() {
  group('Cart', () {
    test('addItem increments count', () {
      final cart = Cart();
      cart.addItem(Item(sku: 'BOOK-001', qty: 1));
      expect(cart.itemCount, 1);
    });

    test('addItem rejects negative qty', () {
      final cart = Cart();
      expect(
        () => cart.addItem(Item(sku: 'BOOK-001', qty: -1)),
        throwsA(isA<ArgumentError>()),
      );
    });
  });
}
```

Run:

```bash
flutter test test/cart_test.dart
flutter test                       # all tests
flutter test --coverage            # produces coverage/lcov.info
```

The LCOV output feeds `lcov-analysis` (in the qa-test-reporting plugin).

## Step 3 - Widget tests

Per [flutter-testing-doc][ft], widget tests "verify the UI looks
and interacts as expected":

```dart
// test/cart_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/cart_screen.dart';

void main() {
  testWidgets('CartScreen shows item count', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: CartScreen(initialCount: 3)));

    expect(find.text('3 items'), findsOneWidget);
    expect(find.byKey(Key('add-to-cart-button')), findsOneWidget);
  });

  testWidgets('Tapping add button increments count', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: CartScreen(initialCount: 0)));

    await tester.tap(find.byKey(Key('add-to-cart-button')));
    await tester.pump();   // rebuild after state change

    expect(find.text('1 item'), findsOneWidget);
  });
}
```

`tester.pumpWidget(...)` mounts the widget tree. `tester.pump()`
advances the frame; `tester.pumpAndSettle()` advances until no
animations are pending.

Finders:

| Finder                | Use                                              |
|-----------------------|--------------------------------------------------|
| `find.byKey(Key(...))` | By Key (preferred for stable lookups).            |
| `find.text("...")`     | By visible text (translation-fragile).            |
| `find.byType(Widget)`  | By widget type.                                   |
| `find.byIcon(Icons.x)` | By Material icon.                                 |
| `find.descendant(of:, matching:)` | Nested matching.                       |

## Step 4 - Integration tests

Per [flutter-testing-doc][ft], integration tests "test complete app
or large app sections" on real devices.

```dart
// integration_test/checkout_flow_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('checkout flow', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(Key('login-button')));
    await tester.pumpAndSettle();

    await tester.enterText(find.byKey(Key('email-field')), 'qa-test@example.com');
    // ... etc.
  });
}
```

Run:

```bash
# On a connected device or simulator/emulator
flutter test integration_test/checkout_flow_test.dart
```

## Step 5 - Mockito + build_runner

For mocks:

```dart
// test/cart_test.dart
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'cart_test.mocks.dart';   // generated

@GenerateMocks([CartRepo])
void main() {
  test('Cart loads from repo', () async {
    final mockRepo = MockCartRepo();
    when(mockRepo.getCart()).thenAnswer(
      (_) async => Cart(items: [Item(sku: 'BOOK-001', qty: 1)]),
    );

    final cart = await mockRepo.getCart();
    expect(cart.itemCount, 1);
    verify(mockRepo.getCart()).called(1);
  });
}
```

Generate the `*.mocks.dart` files:

```bash
dart run build_runner build --delete-conflicting-outputs
```

## Step 6 - Coverage + reporting

```bash
flutter test --coverage           # writes coverage/lcov.info
genhtml coverage/lcov.info -o coverage/html   # human report
```

The LCOV file feeds the same parser other plugins use
(`lcov-analysis`)
for cross-language coverage aggregation.

## Step 7 - CI integration

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: subosito/flutter-action@v2
        with:
          channel: stable
      - run: flutter pub get
      - run: dart run build_runner build --delete-conflicting-outputs
      - run: flutter test --coverage
      - uses: codecov/codecov-action@v5
        with:
          files: coverage/lcov.info

  integration-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: subosito/flutter-action@v2
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          script: flutter test integration_test/
```

Per [flutter-testing-doc][ft], Flutter supports CI integration via
"Fastlane / Travis CI / Cirrus CI / Codemagic / Bitrise / Appcircle /
Patrol (for native platform interactions)."

## Anti-patterns

| Anti-pattern                                                         | Why it fails                                                              | Fix |
|----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| All tests as integration tests                                        | Slow; fragile; hides per-layer issues per the pyramid.                    | Many unit + widget; few integration (Step 1 pyramid). |
| `find.text("...")` for translatable strings                           | Translation breaks tests.                                                  | `find.byKey(Key("..."))` (Step 3). |
| `tester.pump()` (single frame) for animations                         | Animation isn't done; assertion fires too early.                          | `tester.pumpAndSettle()` for animations. |
| Skipping `IntegrationTestWidgetsFlutterBinding.ensureInitialized()`   | Integration test won't bind; runtime errors.                              | Add as first line in main() (Step 4). |
| Mock without `@GenerateMocks` (manual mock classes)                    | Tedious; drift when the SUT interface changes.                            | Use `@GenerateMocks` + `build_runner` (Step 5). |
| Coverage from integration tests only                                  | Integration coverage is sparse; misses unit-level branches.               | Coverage from `flutter test` (which runs unit + widget). |

## Limitations

- **`flutter drive` deprecated for new projects.** Use
  `integration_test` package (modern; Step 4).
- **Native platform features need extra packages.** For things like
  permissions / camera / push notifications, use `patrol` or
  per-platform native integration.
- **Widget tests use a fake `Stub` for `MediaQuery` etc.** Surface
  varies vs production; widget tests don't cover layout/font issues
  that need a real renderer.
- **Mockito's null safety story.** Generation handles it; manual
  mocks are awkward.

## References

- [ft][ft] - Flutter testing pyramid: unit / widget / integration;
  trade-off matrix (confidence, maintenance, deps, speed); CI
  integration list; `flutter test` / `flutter drive` commands.
- `xcuitest-suite`,
  `espresso-suite`,
  `detox-testing` - alternative
  framework wrappers when the app isn't Flutter.
- `lcov-analysis` - downstream consumer of `flutter test --coverage`.
