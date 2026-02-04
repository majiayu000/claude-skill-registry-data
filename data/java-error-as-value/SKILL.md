---
name: java-error-as-value
description: Implement error-as-value pattern in Java using Result type for type-safe error handling. Use this skill when implementing error handling without exceptions, converting try-catch to Result pattern, or designing type-safe error handling in Java applications. Particularly useful for functional programming style, API design, and when errors are expected and recoverable.
---

# Java Error-as-Value Pattern

## Overview

This skill enables error-as-value pattern in Java using the Result<T, E> type, an alternative to exception-based error handling. The Result type represents either success (Ok) or failure (Err), making errors explicit in the type system and enabling functional composition of fallible operations.

Inspired by Rust's Result type and Haskell's Either type, this pattern provides:
- **Type-safe error handling**: Errors are values in the type system
- **Explicit error flow**: No hidden control flow via exceptions
- **Composable operations**: Chain fallible operations with map, andThen, etc.
- **No stack unwinding overhead**: Better performance for expected errors

## When to Use This Skill

Invoke this skill when:

1. **Implementing new error-handling code** where errors are expected and recoverable
   - Examples: "Parse this user input using Result pattern", "Add validation with error-as-value"

2. **Refactoring exception-based code** to Result pattern
   - Examples: "Convert this try-catch to Result", "Refactor this method to return Result instead of throwing"

3. **Designing APIs** that make error handling explicit
   - Examples: "Design a configuration parser using Result", "Create a validation pipeline with Result"

4. **Working with functional-style code** that chains operations
   - Examples: "Chain these database operations using Result", "Compose these validation steps"

5. **User explicitly mentions** error-as-value, Result type, or functional error handling
   - Examples: "Use error-as-value pattern", "Implement this with Result<T, E>"

## Quick Start

### 1. Copy the Result Type

The Result<T, E> implementation is provided in `assets/Result.java`. Copy this file to the project:

```java
// Copy assets/Result.java to src/main/java/Result.java
// or appropriate package directory
```

### 2. Define Error Types

Create domain-specific error enums or sealed interfaces:

```java
// Simple enum errors (recommended for most cases)
enum ValidationError {
    INVALID_EMAIL,
    WEAK_PASSWORD,
    USERNAME_TAKEN
}

// Rich sealed interface errors (for complex error data)
sealed interface ConfigError {
    record FileNotFound(String path) implements ConfigError {}
    record InvalidJson(String reason) implements ConfigError {}
    record MissingField(String field) implements ConfigError {}
}
```

### 3. Return Result from Methods

Replace exception-throwing methods with Result-returning methods:

```java
// Before: Exception-based
public User getUser(String id) throws UserNotFoundException {
    // ...
}

// After: Result-based
public Result<User, UserError> getUser(String id) {
    if (!userExists(id)) {
        return Result.err(UserError.NOT_FOUND);
    }
    return Result.ok(fetchUser(id));
}
```

### 4. Handle Results at Call Sites

Use pattern matching or combinators to handle results:

```java
// Pattern matching
String message = getUser(id).match(
    user -> "Found: " + user.getName(),
    error -> "Error: " + error
);

// Chaining operations
Result<String, UserError> userName = getUser(id)
    .map(user -> user.getName())
    .mapErr(error -> handleError(error));

// Side effects
getUser(id)
    .ifOk(user -> processUser(user))
    .ifErr(error -> logError(error));
```

## Core Capabilities

### 1. Generate Result Boilerplate

When asked to implement error-as-value pattern, copy the Result<T, E> class from `assets/Result.java` to the appropriate location in the project.

The Result type provides:
- `ok(value)` and `err(error)` - constructors
- `isOk()` and `isErr()` - type checking
- `unwrap()`, `unwrapOr()`, `unwrapOrElse()` - value extraction
- `map()`, `mapErr()` - transformations
- `andThen()` - monadic chaining (flatMap)
- `ifOk()`, `ifErr()` - side effects
- `match()` - pattern matching
- `toOptional()` - conversion to Optional
- `of()` - exception wrapping

### 2. Design Error Types

When implementing error handling, design appropriate error types based on the use case:

**Use String errors** for prototyping or simple cases:
```java
Result<Integer, String> parse(String input) {
    return Result.of(
        () -> Integer.parseInt(input),
        e -> "Invalid number: " + e.getMessage()
    );
}
```

**Use enum errors** for production code with discrete error cases:
```java
enum ParseError {
    INVALID_FORMAT,
    OUT_OF_RANGE,
    EMPTY_INPUT
}

Result<Integer, ParseError> parseAge(String input) {
    if (input.isEmpty()) {
        return Result.err(ParseError.EMPTY_INPUT);
    }
    // ...
}
```

**Use sealed interface errors** when errors need to carry data:
```java
sealed interface ValidationError {
    record Required(String field) implements ValidationError {}
    record TooShort(String field, int min, int actual) implements ValidationError {}
    record InvalidFormat(String field, String pattern) implements ValidationError {}
}
```

See `references/guidelines.md` for detailed error type design guidance.

### 3. Convert Exception-Based Code to Result

When refactoring try-catch blocks to Result pattern:

**Step 1**: Identify the error types that can be thrown
**Step 2**: Create an appropriate error enum or sealed interface
**Step 3**: Use `Result.of()` to wrap exception-throwing code
**Step 4**: Update the method signature to return Result
**Step 5**: Update all call sites to handle Result

Example transformation:

```java
// Before
public Config loadConfig(String path) throws IOException, ParseException {
    String content = Files.readString(Paths.get(path));
    return parseConfig(content);
}

// After
public Result<Config, ConfigError> loadConfig(String path) {
    return Result.of(
        () -> Files.readString(Paths.get(path)),
        e -> new ConfigError.FileNotFound(path)
    ).andThen(content -> parseConfig(content));
}
```

### 4. Chain Fallible Operations

Use `andThen()` for operations that return Result (monadic chaining):

```java
Result<Order, String> result = validateCart(cart)
    .andThen(validCart -> calculateTotal(validCart))
    .andThen(total -> createOrder(cart, total))
    .andThen(order -> saveToDatabase(order))
    .andThen(order -> sendConfirmation(order));

// First error short-circuits the chain
```

Use `map()` for transforming success values:

```java
Result<String, Error> upperName = getUser(id)
    .map(user -> user.getName())
    .map(name -> name.toUpperCase());
```

### 5. Implement Validation Pipelines

For multi-field validation, accumulate errors or fail fast:

```java
// Fail fast (stop at first error)
Result<UserInput, ValidationError> result = validateUsername(input.username())
    .andThen(u -> validateEmail(input.email()))
    .andThen(e -> validatePassword(input.password()))
    .map(p -> input);

// Accumulate all errors
public Result<UserInput, List<ValidationError>> validate(UserInput input) {
    List<ValidationError> errors = new ArrayList<>();

    validateUsername(input.username()).ifErr(errors::add);
    validateEmail(input.email()).ifErr(errors::add);
    validatePassword(input.password()).ifErr(errors::add);

    if (errors.isEmpty()) {
        return Result.ok(input);
    }
    return Result.err(errors);
}
```

### 6. Generate Practical Examples

When requested to demonstrate the pattern, use realistic scenarios from `references/examples.md`:

- **User registration** with validation and database operations
- **Configuration parsing** with file I/O and JSON parsing
- **HTTP client** with retry logic and error mapping
- **Database transactions** with rollback on error
- **File processing** pipelines with multi-step transformations

Always include:
- Domain-specific error types
- Proper error handling at boundaries (e.g., HTTP responses)
- Functional composition when appropriate

## Best Practices

When implementing error-as-value pattern:

1. **Consult guidelines first**: Reference `references/guidelines.md` for:
   - When to use Result vs exceptions
   - Error type design patterns
   - Common patterns and anti-patterns
   - Migration strategies
   - Performance considerations

2. **Design error types carefully**:
   - Use enums for discrete error cases
   - Use sealed interfaces when errors need data
   - Make errors domain-specific and meaningful

3. **Avoid mixing patterns**:
   - Don't throw exceptions from Result-returning methods
   - Don't silently ignore errors with unwrap()
   - Be consistent within a module or layer

4. **Preserve error information**:
   - Don't convert errors to generic strings too early
   - Map errors at boundaries (e.g., DB error → HTTP status)
   - Include context in error types when needed

5. **Use appropriate combinators**:
   - `andThen()` for operations returning Result
   - `map()` for pure transformations
   - `match()` for exhaustive handling
   - `ifOk()`/`ifErr()` for side effects only

6. **Test both paths**:
   - Test success cases with `isOk()` and `unwrap()`
   - Test error cases with `isErr()` and `unwrapErr()`
   - Test chaining behavior and short-circuiting

## Workflow

When a user requests error-as-value implementation:

1. **Understand the context**:
   - Is this new code or refactoring?
   - What are the error conditions?
   - How should errors be handled?

2. **Copy Result type** (if not already in project):
   - Copy `assets/Result.java` to appropriate package
   - Adjust package name if needed

3. **Design error types**:
   - Define enum or sealed interface for domain errors
   - Consult `references/guidelines.md` for design patterns

4. **Implement the logic**:
   - Use `Result.ok()` and `Result.err()` for explicit returns
   - Use `Result.of()` to wrap exception-throwing code
   - Use `andThen()` to chain fallible operations
   - Use `map()` to transform success values

5. **Handle at boundaries**:
   - Use `match()` or `ifOk()`/`ifErr()` at API boundaries
   - Convert errors to appropriate formats (HTTP status, log messages, etc.)

6. **Provide examples** when helpful:
   - Show before/after for refactoring
   - Demonstrate chaining for complex flows
   - Reference `references/examples.md` for realistic patterns

7. **Write tests**:
   - Test both success and error paths
   - Verify chaining and short-circuit behavior

## Resources

### assets/Result.java

The complete Result<T, E> implementation ready to copy into any project. This file includes:
- Sealed interface with Ok and Err records (requires Java 17+)
- Complete API: constructors, type checks, extraction, transformation, chaining
- Exception wrapping utility (`Result.of()`)
- Comprehensive JavaDoc documentation

**Usage**: Copy this file to the project's source directory and adjust the package name as needed.

### references/guidelines.md

Comprehensive guidelines for using the error-as-value pattern effectively:
- When to use Result vs exceptions
- Error type design patterns (String, enum, sealed interface)
- Common usage patterns with code examples
- Naming conventions for methods and error types
- Migration strategy from exception-based code
- Performance considerations
- Testing approaches
- Common pitfalls and how to avoid them

**Usage**: Reference this document when designing error types, making architectural decisions, or helping users understand best practices.

### references/examples.md

Real-world examples demonstrating the pattern in various scenarios:
- User registration service with validation and database operations
- Configuration parser with file I/O and JSON parsing
- HTTP client with retry logic and error mapping
- Database transaction handling with rollback
- Multi-step validation pipeline with error accumulation
- File processing pipeline with transformations

**Usage**: Use these examples as templates for common scenarios. Show relevant examples to users when implementing similar functionality.

---

**Note**: This skill requires Java 17+ for sealed interfaces and records. For older Java versions, the Result type can be adapted to use regular classes instead of records.
