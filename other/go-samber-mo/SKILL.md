---
name: go-samber-mo
description: "Monadic types for Go with samber/mo. Covers Option, Result, Either, and functional composition patterns."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 07:10:00 GMT
---

## Core Philosophy

`samber/mo` brings functional programming safety to Go by providing **Monads**. These types help make impossible states (like nil pointer dereferences) unrepresentable at the type level.

- **Option[T]**: Represents a value that may be present (`Some`) or absent (`None`). Replaces the need for `nil` pointers.
- **Result[T]**: Represents a successful result (`Ok`) or a failure (`Err`). Replaces the `(T, error)` pattern with a single value.
- **Either[L, R]**: Represents a value that is either type `L` (Left) or type `R` (Right). Useful for alternative paths.

## Key Types and Usage

### Option[T]
```go
// Create
opt := mo.Some("Alice")
none := mo.None[string]()

// Use
name := opt.OrElse("Guest") // "Alice"
empty := none.OrElse("Guest") // "Guest"

// Map (transform)
upper := opt.Map(func(s string) (string, bool) {
    return strings.ToUpper(s), true
})
```

### Result[T]
```go
// Create
res := mo.Ok(42)
err := mo.Err[int](fmt.Errorf("failed"))

// Wrap existing Go calls
res := mo.TupleToResult(os.ReadFile("config.yaml"))

// Use
data := res.OrElse([]byte("{}"))
```

### Either[L, R]
```go
// Create
left := mo.Left[int, string](404)
right := mo.Right[int, string]("Not Found")

// Match
msg := left.Match(
    func(code int) string { return fmt.Sprintf("Error: %d", code) },
    func(s string) string { return s },
)
```

## Why use Monads?

- **Nil Safety**: `Option` forces you to handle the `None` case explicitly, preventing nil pointer panics.
- **Composability**: You can chain operations (Map, FlatMap) without writing repeated `if err != nil` checks.
- **Clarity**: The return type clearly signals that a value might be missing or an operation might fail.
- **JSON/DB Support**: `Option` and `Result` implement standard interfaces for JSON marshaling and SQL scanning.

## Best Practices

1. **Prefer `OrElse` over `MustGet`** — `MustGet` will panic if the value is missing. Use it only when you are absolutely sure or inside a recovery block.
2. **Use `Do` Notation** — For complex chains of operations that might fail, use `mo.Do` to write imperative-style code that is automatically wrapped in a `Result`.
3. **Accept Monads, Return Monads** — Use these types in your internal service boundaries to propagate safety throughout your application.

## Anti-patterns

- ❌ **Mixing Monads and `nil`** — Don't return `*Option[T]`. The `Option` itself is the safety wrapper.
- ❌ **Over-nesting** — Chaining too many `FlatMap` calls can become hard to follow. Use intermediate variables or `mo.Do`.
- ❌ **Ignoring `Err` in `Result`** — Always handle the error case via `OrElse`, `Match`, or by returning the `Result` to the caller.
- ❌ **Using `Option` for everything** — If a value is logically always required, use a plain type. Only use `Option` for truly optional fields.
