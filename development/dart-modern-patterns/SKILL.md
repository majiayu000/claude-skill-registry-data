---
name: dart-modern-patterns
description: Leverages modern Dart 3+ language features including pattern matching, switch expressions, records, and sealed class hierarchies for expressive, type-safe Flutter code.
version: 1.0.0
---

# Modern Dart 3+ Patterns

Idiomatic Dart 3 features to write concise, safe, and expressive Flutter code.

## 1. Records (Anonymous Typed Tuples)

Return multiple values without creating boilerplate data classes:

```dart
// Function returning a Record with positional and named fields
(String name, int age, {bool isActive}) getUserSummary() {
  return ('Alice', 30, isActive: true);
}

// Destructuring records
final (name, age, isActive: active) = getUserSummary();
```

---

## 2. Pattern Matching & Switch Expressions

Use switch expressions for exhaustive state mapping in UI:

```dart
// Switch expression returning a Widget directly
Widget buildStateWidget(AsyncValue<UserData> state) {
  return switch (state) {
    AsyncData(:final value) => UserProfileView(user: value),
    AsyncError(:final error) => ErrorBanner(message: error.toString()),
    AsyncLoading() => const CircularProgressIndicator(),
  };
}
```

### Relational & Logical Patterns
```dart
String getDiscountLabel(int points) => switch (points) {
  >= 1000 => 'VIP (30% off)',
  >= 500 && < 1000 => 'Gold (20% off)',
  > 0 => 'Standard (10% off)',
  _ => 'No discount',
};
```

---

## 3. Sealed Classes for Finite State Machines

`sealed` classes ensure exhaustive compile-time checking:

```dart
sealed class AuthState {
  const AuthState();
}

class AuthInitial extends AuthState {
  const AuthInitial();
}

class Authenticated extends AuthState {
  final User user;
  const Authenticated(this.user);
}

class AuthError extends AuthState {
  final String message;
  const AuthError(this.message);
}

// Compiler errors if any AuthState subtype is unhandled:
String getGreeting(AuthState state) => switch (state) {
  AuthInitial() => 'Please sign in',
  Authenticated(:final user) => 'Welcome back, ${user.name}!',
  AuthError(:final message) => 'Error: $message',
};
```
