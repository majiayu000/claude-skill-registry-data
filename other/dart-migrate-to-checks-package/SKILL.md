---
name: dart-migrate-to-checks-package
description: Replace the usage of `expect` and similar functions from `package:matcher` to `package:checks` equivalents.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Fri, 24 Apr 2026 15:15:22 GMT
---

## Contents
- [Dependency Management](#dependency-management)
- [Syntax Migration Guidelines](#syntax-migration-guidelines)
- [Migration Workflow](#migration-workflow)
- [Examples](#examples)

## Dependency Management
- Add `package:checks` as a `dev_dependency` using `dart pub add dev:checks`.
- Remove `package:matcher` if explicitly listed (often transitively included by `package:test`).
- Import `package:checks/checks.dart` in all test files undergoing migration.

## Syntax Migration Guidelines
- **Basic Equality:** `expect(actual, equals(expected))` → `check(actual).equals(expected)`.
- **Type Checking:** `expect(actual, isA<Type>())` → `check(actual).isA<Type>()`.
- **Property Extraction:** `expect(actual.property, expected)` → `check(actual).has((a) => a.property, 'property name').equals(expected)`.
- **Cascades:** Use `..` to chain multiple expectations on a single subject.
- **Async Futures:** `await check(someFuture).completes((r) => r.equals(expected));`
- **Async Streams:** Wrap in `StreamQueue` or use `.withQueue`.

## Migration Workflow
- [ ] Add `package:checks` as a dev dependency.
- [ ] Identify all test files using `package:matcher` (`expect` calls).
- [ ] Import `package:checks/checks.dart` in target test files.
- [ ] Rewrite all `expect(...)` statements to `check(...)` statements.
- [ ] Run static analyzer.
- [ ] Run tests.

### Examples

**Basic Assertions:**
```dart
// Before (matcher):
expect(someList.length, 1);
expect(someString, startsWith('a'));
expect(someObject, isA<Map>());

// After (checks):
check(someList).length.equals(1);
check(someString).startsWith('a');
check(someObject).isA<Map>();
```

**Composed Expectations:**
```dart
// Before:
expect('foo,bar,baz', allOf([contains('foo'), isNot(startsWith('bar')), endsWith('baz')]));

// After:
check('foo,bar,baz')
  ..contains('foo')
  ..not((s) => s.startsWith('bar'))
  ..endsWith('baz');
```

**Async:**
```dart
// Before:
expect(Future.value(10), completion(equals(10)));
expect(Future.error('oh no'), throwsA(equals('oh no')));

// After:
await check(Future.value(10)).completes((it) => it.equals(10));
await check(Future.error('oh no')).throws<String>().equals('oh no');
```
