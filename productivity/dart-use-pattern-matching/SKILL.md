---
name: dart-use-pattern-matching
description: Use switch expressions and pattern matching where appropriate
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Fri, 24 Apr 2026 15:08:55 GMT
---

## Contents
- [Pattern Selection Strategy](#pattern-selection-strategy)
- [Switch Statements vs. Expressions](#switch-statements-vs-expressions)
- [Core Pattern Implementations](#core-pattern-implementations)
- [Workflows](#workflows)
- [Examples](#examples)

## Pattern Selection Strategy
*   **If validating/extracting from JSON:** Use Map and List patterns.
*   **If handling multiple return values:** Use Record patterns.
*   **If executing type-specific behavior (ADTs):** Use Object patterns with `sealed` classes.
*   **If matching numeric ranges:** Use Relational (`>=`, `<=`) and Logical-and (`&&`) patterns.
*   **If multiple cases share logic:** Use Logical-or (`||`) patterns.
*   **If ignoring specific values:** Use the Wildcard (`_`) or Rest (`...`) patterns.

## Switch Statements vs. Expressions
*   **Switch expression (produce a value):** `switch (value) { pattern => expression, }`
*   **Switch statement (execute statements):** `switch (value) { case pattern: statements; }`

## Core Pattern Implementations
*   **Logical-or (`||`):** Both branches must define the exact same set of variables.
*   **Logical-and (`&&`):** Branches must *not* define overlapping variables.
*   **Relational:** `==`, `!=`, `<`, `>`, `<=`, `>=` followed by a constant.
*   **Cast (`as`):** Throws if the value does not match the type.
*   **Null-check (`?`):** Fails the match if the value is null.
*   **Null-assert (`!`):** Throws if the value is null.
*   **Variable:** `var name` or `Type name`. Binds the matched value.
*   **Wildcard (`_`):** Matches any value and discards it.
*   **List:** `[pattern1, pattern2]`. Matches lists of exact length unless Rest used.
*   **Map:** `{"key": pattern}`. Matches maps containing the specified keys.
*   **Record:** `(pattern1, named: pattern2)`. Matches records of the exact shape.
*   **Object:** `ClassName(field: pattern)`. Matches instances of `ClassName`.

### Task Progress: Implementing Pattern Matching
- [ ] Identify the data structure being evaluated.
- [ ] Select the appropriate switch construct.
- [ ] Define the required patterns.
- [ ] Extract data using Variable patterns.
- [ ] Apply Guard clauses (`when condition`).
- [ ] Handle unmatched cases using Wildcard (`_`) or `default`.
- [ ] Run exhaustiveness validator: `dart analyze`.

### Example: JSON Validation and Destructuring
```dart
var data = {'user': ['Lily', 13]};

if (data case {'user': [String name, int age]}) {
  print('User $name is $age years old.');
} else {
  print('Invalid JSON structure.');
}
```

### Example: Algebraic Data Types (Sealed Classes)
```dart
sealed class Shape {}
class Square implements Shape {
  final double length;
  Square(this.length);
}
class Circle implements Shape {
  final double radius;
  Circle(this.radius);
}

double calculateArea(Shape shape) => switch (shape) {
  Square(length: var l) => l * l,
  Circle(:var radius)   => math.pi * radius * radius,
};
```

### Example: Variable Swapping
```dart
var (a, b) = ('left', 'right');
(b, a) = (a, b); // Swap values

var (name, age) = getUserInfo(); // Destructuring
```

### Example: Guard Clauses and Logical-or
```dart
switch (shape) {
  case Square(size: var s) || Circle(size: var s) when s > 0:
    print('Valid symmetric shape with size $s');
  case Square() || Circle():
    print('Invalid or empty shape');
  default:
    print('Unknown shape');
}
```
