---
name: gleam
description: Develop with Gleam using idiomatic patterns, TDD, and type-driven design. Activate when working with .gleam files, gleam.toml, or user mentions Gleam, BEAM, or Erlang.
---

# Gleam Development

Idiomatic Gleam with **type-driven design** and **TDD**.

## Workflow

```
1. MODEL    → Define domain types first (make illegal states unrepresentable)
2. RED      → Write failing test
3. GREEN    → Minimal implementation
4. REFACTOR → Clean up, use pipelines
5. RUN      → gleam test && gleam run
```

## CLI

```bash
gleam check                    # Fast type feedback (use often)
gleam test                     # Run tests
gleam run                      # Execute main
gleam format                   # Format all
gleam add pkg --dev            # Dev dependency
```

## Patterns

### Error Propagation with `use`

```gleam
pub fn process(path: String) -> Result(Data, Error) {
  use content <- result.try(read(path))
  use parsed <- result.try(parse(content))
  use valid <- result.try(validate(parsed))
  Ok(transform(valid))
}

// Wrap external errors
use raw <- result.map_error(read(path), FileError)

// Early return
use <- bool.guard(string.is_empty(name), Error(EmptyName))
```

### Opaque Types (Enforce Invariants)

```gleam
pub opaque type Email {
  Email(String)
}

pub fn from_string(s: String) -> Result(Email, String) {
  case string.contains(s, "@") {
    True -> Ok(Email(s))
    False -> Error("Invalid email")
  }
}
```

### Make Illegal States Unrepresentable

```gleam
// BAD: allows invalid combinations
pub type Request {
  Request(status: String, data: Option(Data), error: Option(Error))
}

// GOOD: impossible states are unrepresentable
pub type Request {
  Pending
  Success(Data)
  Failed(Error)
}
```

### Subject-First for Pipelines

```gleam
pub fn add(to num: Int, value: Int) -> Int

items
|> list.filter(fn(x) { x > 0 })
|> list.map(fn(x) { x * 2 })
|> int.sum
```

### Pattern Matching

```gleam
// Multi-subject
case x, y {
  0, 0 -> "origin"
  _, 0 -> "x-axis"
  0, _ -> "y-axis"
  _, _ -> "plane"
}

// List destructuring
case items {
  [] -> empty()
  [only] -> single(only)
  [first, ..rest] -> many(first, rest)
}

// Guards
case n {
  x if x > 0 -> "positive"
  x if x < 0 -> "negative"
  _ -> "zero"
}

// let assert for guaranteed matches only
let assert Ok(config) = load_required_config()
```

### Custom Error Types

```gleam
pub type UserError {
  InvalidEmail(String)
  InvalidAge(Int)
  NotFound(UserId)
}

// Wrap externals
pub type AppError {
  DbError(postgres.Error)
  ValidationError(UserError)
}
```

### Labelled Arguments

Proactively use labels for readability.

```gleam
pub fn create(name name: String, email email: String) -> User

// Shorthand when var matches label
let name = "Alice"
create(name:, email: "a@b.com")
```

## Project Structure

```
app/
├── gleam.toml
├── src/
│   ├── app.gleam           # Entry
│   └── app/
│       ├── domain/         # Types + constructors
│       └── internal/       # Private (configure in gleam.toml)
└── test/
    └── app_test.gleam
```

```toml
# gleam.toml
internal_modules = ["app/internal", "app/internal/*"]

[dependencies]
...

[dev-dependencies]
...
```

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| `import gleam/io.{println}` | `io.println(...)` |
| `panic` for expected failures | Return `Result` |
| `let assert` on user input | Pattern match + handle |
| `list.at(items, n)` indexing | Pattern match or fold |
| Nested `result.try` callbacks | `use` expressions |
| Boolean flags for states | Sum types |

