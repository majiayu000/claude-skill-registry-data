---
name: flutter-testing
description: Guides writing unit tests, widget tests, and integration tests in Flutter using flutter_test, WidgetTester, Mockito/Mocktail, and integration_test.
version: 1.0.0
---

# Flutter Testing Best Practices

Comprehensive testing strategies for Flutter apps across unit, widget, and integration levels.

## 1. Widget Testing (`flutter_test`)

Use `testWidgets` to render UI components in an isolated test environment without a physical device or emulator.

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:myapp/ui/counter_widget.dart';

void main() {
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    // 1. Pump the widget inside a MaterialApp
    await tester.pumpWidget(
      const MaterialApp(home: Scaffold(body: CounterWidget())),
    );

    // 2. Verify initial state
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // 3. Perform tap interaction
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump(); // Trigger frame redraw

    // 4. Verify updated state
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });
}
```

### Key Tester Methods
- `tester.pumpWidget(widget)`: Renders the given widget tree.
- `tester.pump()`: Re-renders the frame (synchronous setState).
- `tester.pumpAndSettle()`: Repeatedly pumps until there are no more scheduled frames or animations.
- `find.byKey(Key('myKey'))`: Most stable selector for testing.
- `find.byType(ElevatedButton)`: Selects by widget type.

---

## 2. Unit Testing Business Logic & State

Test ViewModels, Repositories, or Bloc without UI:

```dart
import 'package:test/test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:myapp/data/repositories/auth_repository.dart';
import 'package:myapp/ui/auth_viewmodel.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  late MockAuthRepository mockRepo;
  late AuthViewModel viewModel;

  setUp(() {
    mockRepo = MockAuthRepository();
    viewModel = AuthViewModel(repository: mockRepo);
  });

  test('login success updates state to authenticated', () async {
    when(() => mockRepo.login('user@test.com', 'secret'))
        .thenAnswer((_) async => const User(id: '123', email: 'user@test.com'));

    await viewModel.login('user@test.com', 'secret');

    expect(viewModel.isAuthenticated, isTrue);
    expect(viewModel.currentUser?.id, equals('123'));
  });
}
```

---

## 3. Running Tests via CLI

```bash
# Run all tests
flutter test

# Run tests with code coverage output (creates coverage/lcov.info)
flutter test --coverage

# Run a specific test file
flutter test test/ui/counter_test.dart
```
