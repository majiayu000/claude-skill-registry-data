---
name: dart-fix-runtime-errors
description: Uses get_runtime_errors and lsp to fetch an active stack trace, locate the failing line, apply a fix, and verify resolution via hot_reload.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Fri, 24 Apr 2026 15:13:22 GMT
---

- [Core Concepts & Guidelines](#core-concepts--guidelines)
- [Workflows](#workflows)
- [Examples](#examples)

### Type System & Soundness
Enforce Dart's sound type system to prevent runtime invalid states. 

*   **Method Overrides:** Maintain sound return types (covariant) and parameter types (contravariant). Never tighten a parameter type in a subclass unless explicitly marked with the `covariant` keyword.
*   **Generics & Collections:** Add explicit type annotations to generic classes (e.g., `List<T>`, `Map<K, V>`). Never assign a `List<dynamic>` to a typed list.
*   **Downcasting:** Avoid implicit downcasts from `dynamic`. Use explicit casts when necessary.
*   **Strict Casts:** Enable `strict-casts: true` in `analysis_options.yaml`.

### Null Safety
*   **Modifiers:** Apply `?` for nullable types, `!` for null assertions, and `required` for named parameters.
*   **Late Initialization:** Use the `late` keyword for non-nullable variables guaranteed to be initialized before use.
*   **Wildcards:** Use the `_` wildcard variable (Dart 3.7+) for non-binding local variables.

### Error Handling
*   **Catching:** Catch `Exception` subtypes for recoverable failures. 
*   **Errors:** Never explicitly catch `Error` or its subtypes. Enable `avoid_catching_errors` linter rule.
*   **Rethrowing:** Use `rethrow` inside a `catch` block to preserve stack trace.

**Task Progress:**
- [ ] 1. Run static analyzer: `dart analyze . --fatal-infos`
- [ ] 2. Apply automated fixes: `dart fix --apply`
- [ ] 3. Resolve remaining errors manually.
- [ ] 4. Verify fixes: `dart analyze .` and `dart test`

### Example: Fixing Dynamic List Assignments
```dart
// Before (fails):
final list = []; // List<dynamic>
printInts(list); // Error

// After (passes):
final list = <int>[]; // Explicitly typed
printInts(list);
```

### Example: Fixing Method Overrides
```dart
// Before: void chase(Mouse a) {} // Error
// After: void chase(covariant Mouse a) {} // OK
```

### Example: Fixing Null Safety with `late`
```dart
// Before: String temperature; // Error
// After: late String temperature; // OK
```
