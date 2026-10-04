---
name: dart-fix-static-analysis-errors
description: Workflow for identifying and fixing static analysis errors. Use this after modifying code or if `dart analyze` fails.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Fri, 24 Apr 2026 15:12:12 GMT
---

## Contents
- [Diagnostic Execution](#diagnostic-execution)
- [Null Safety & Type Resolution](#null-safety--type-resolution)
- [Flow Analysis & Type Promotion](#flow-analysis--type-promotion)
- [Analyzer Configuration](#analyzer-configuration)
- [Workflow: Static Analysis Remediation](#workflow-static-analysis-remediation)
- [Examples](#examples)

## Diagnostic Execution
Execute the Dart analyzer to identify static errors, warnings, and informational diagnostics across the codebase.

*   Run `$ dart analyze` to evaluate all Dart files in the current directory.
*   Target specific directories or files by appending the path: `$ dart analyze bin` or `$ dart analyze lib/main.dart`.
*   Enforce strictness by failing on info-level issues using the `--fatal-infos` flag.
*   Apply automated quick-fixes for supported diagnostics using `$ dart fix --apply`. Preview changes first with `$ dart fix --dry-run`.

## Null Safety & Type Resolution
Address static errors related to Dart's sound null safety and strict type system.

*   **Nullability:** Append `?` to types to explicitly allow `null` (e.g., `String?`).
*   **Assertion:** Use the postfix bang operator `!` to cast a nullable expression to its underlying non-nullable type when you can guarantee it is not null.
*   **Delayed Initialization:** Apply the `late` modifier to non-nullable top-level or instance variables that are guaranteed to be initialized before their first read.
*   **Named Parameters:** Use the `required` modifier for named parameters that do not have a default value and cannot be null.
*   **Explicit Downcasts:** If static analysis disallows an implicit downcast, use an explicit cast: `as List<Cat>`.
*   **Generic Types:** Always provide explicit type annotations to generic classes (e.g., `List<String>`, `Map<String, dynamic>`).

## Flow Analysis & Type Promotion
Leverage Dart's control flow analysis to safely promote nullable types to non-nullable types without manual casting.

*   **Null Checks:** Check a local variable against `null` (e.g., `if (value != null)`) to automatically promote it.
*   **Type Tests:** Use the `is` operator (e.g., `if (value is String)`) to promote a variable to a specific subclass.
*   **Early Returns:** Use early returns, `break`, or `throw` to exit a control flow path if a variable is null or the wrong type.
*   **Reachability:** Use the `Never` type for functions that unconditionally throw exceptions or terminate the process.

## Analyzer Configuration
Configure the `analysis_options.yaml` file at the package root.

*   Enable `strict-casts: true` to prevent implicit downcasts from `dynamic`.
*   Enable `strict-inference: true` to prevent the analyzer from falling back to `dynamic`.
*   Enable `strict-raw-types: true` to require explicit type arguments on generic types.
*   Suppress specific diagnostics using `// ignore_for_file:` or `// ignore:`.

## Workflow: Static Analysis Remediation

### Task Progress Checklist
- [ ] Run `$ dart analyze` to establish a baseline of errors.
- [ ] Run `$ dart fix --apply` to resolve automatically fixable issues.
- [ ] Address remaining Null Safety errors (`?`, `!`, `late`, `required`).
- [ ] Address remaining Type System errors (explicit `as` casts, generic type annotations).
- [ ] Run `$ dart analyze` to verify all errors are resolved.
- [ ] Execute tests to ensure fixes did not introduce runtime exceptions.

### Feedback Loop
1. **Run Validator:** `$ dart analyze`
2. **Review Errors:** Identify the file, line number, and diagnostic code.
3. **Fix:** Apply the appropriate null safety or type resolution fix.
4. **Repeat:** Continue until `$ dart analyze` returns "No issues found!".

### Type Promotion via Local Variable Assignment
```dart
// Incorrect (Fails Analysis):
class Coffee {
  String? _temperature;
  void checkTemp() {
    if (_temperature != null) {
      print(_temperature.length); // ERROR
    }
  }
}

// Correct:
class Coffee {
  String? _temperature;
  void checkTemp() {
    final temp = _temperature; // Copy to local variable
    if (temp != null) {
      print(temp.length); // SUCCESS
    }
  }
}
```

### Strict Analyzer Configuration
```yaml
include: package:lints/recommended.yaml

analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    invalid_assignment: error
    missing_return: error
    dead_code: info
```
