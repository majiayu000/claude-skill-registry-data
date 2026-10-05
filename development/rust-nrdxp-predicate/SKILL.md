---
name: rust
description: |
  Idiomatic programming style, patterns, and conventions for Rust development.
  Trigger when:
  - Writing, refactoring, reviewing, or debugging Rust code.
  - Files matching the pattern **/*.rs (including Cargo.toml, Cargo.lock) are in the workspace or referenced.
  - Tasks involve: cargo build, cargo clippy, cargo test, cargo check, rustc.
  - Prompt contains keywords: rust, cargo, clippy, borrow checker, lifetime, struct, enum, impl, Option, Result, match, unwrap, unsafe.
---

# Rust Language Idioms

Work _with_ the language, not against it. Embrace ownership, the borrow checker, and the type system.

---

## Core Values

- **Safety:** Lean on the compiler's guarantees. Avoid `unsafe` unless absolutely necessary.
- **Memory Efficiency:** Zero-cost abstractions. Avoid unnecessary allocations.
- **Ergonomics:** APIs should be intuitive and hard to misuse.

---

## API Design

### Naming Conventions

| Prefix  | Semantics                    | Cost      | Example                       |
| :------ | :--------------------------- | :-------- | :---------------------------- |
| `as_`   | Borrowed view, no allocation | Cheap     | `as_ref()`, `as_slice()`      |
| `to_`   | Creates new owned value      | Expensive | `to_string()`, `to_vec()`     |
| `into_` | Consumes self, transforms    | Cheap     | `into_iter()`, `into_inner()` |

### Argument Flexibility

Accept generic bounds instead of concrete types:

```rust
// ❌ Inflexible
fn read_file(path: &PathBuf) -> Result<String>

// ✅ Accepts &str, String, PathBuf, &Path
fn read_file(path: impl AsRef<Path>) -> Result<String>
```

Common patterns:

- `impl AsRef<Path>` — for paths
- `impl AsRef<str>` — for string-like types
- `impl Into<String>` — when ownership is needed

### Constructors

- **Simple:** `T::new()` for basic instantiation
- **Configured:** `T::with_capacity(n)` for single-option variants
- **Complex:** Use the **Builder pattern** for 3+ optional fields

```rust
let config = ConfigBuilder::new()
    .port(8080)
    .timeout(Duration::from_secs(30))
    .build()?;
```

### Monomorphization Control

For widely-used generic functions, consider splitting:

```rust
// Public generic wrapper (thin)
pub fn process(path: impl AsRef<Path>) -> Result<()> {
    process_inner(path.as_ref())
}

// Private concrete implementation (bulk of logic)
fn process_inner(path: &Path) -> Result<()> {
    // ...
}
```

This reduces binary bloat and compile times.

---

## Error Handling

### The `?` Operator

Use `?` to propagate errors. It:

1. Unwraps `Ok(value)` or returns `Err(e)` early
2. Automatically converts via `From` trait

### Library vs. Application Errors

| Context          | Approach                  | Crate       |
| :--------------- | :------------------------ | :---------- |
| **Libraries**    | Custom enum error types   | `thiserror` |
| **Applications** | Boxed errors with context | `anyhow`    |

```rust
// Library: structured, matchable errors
#[derive(Debug, thiserror::Error)]
pub enum ParseError {
    #[error("invalid header at byte {0}")]
    InvalidHeader(usize),
    #[error("unexpected EOF")]
    UnexpectedEof,
}

// Application: rich context chains
fn main() -> anyhow::Result<()> {
    let config = load_config()
        .context("failed to load configuration")?;
    Ok(())
}
```

### Parse, Don't Validate

Encode invariants in the type system:

```rust
// ❌ Stringly-typed, requires repeated validation
fn send_email(to: &str) -> Result<()>

// ✅ Invalid states are unrepresentable
fn send_email(to: EmailAddress) -> Result<()>
```

The constructor for `EmailAddress` validates once; all downstream code operates with a compile-time guarantee.

---

## Iterators

Iterators are **lazy** and **zero-cost**. Build declarative pipelines:

```rust
let result: Vec<_> = items
    .iter()
    .filter(|x| x.is_valid())
    .map(|x| x.transform())
    .collect();
```

### Key Adapters

| Adapter         | Purpose                           |
| :-------------- | :-------------------------------- |
| `map`           | Transform each element            |
| `filter`        | Keep elements matching predicate  |
| `filter_map`    | Filter and transform in one step  |
| `flat_map`      | Map then flatten nested iterators |
| `zip`           | Combine two iterators into pairs  |
| `chain`         | Concatenate iterators             |
| `take` / `skip` | Limit or offset elements          |
| `inspect`       | Debug: observe without modifying  |

### Pitfalls

- Iterators are lazy—no work until consumed (`collect`, `sum`, `for_each`)
- Avoid side effects in `map`; use `for_each` or explicit loops
- Use `inspect()` to debug intermediate pipeline stages

---

## Concurrency

### Thread Safety Markers

| Trait  | Meaning                                         |
| :----- | :---------------------------------------------- |
| `Send` | Ownership can transfer between threads          |
| `Sync` | References (`&T`) can be shared between threads |

Most types are automatically `Send + Sync`. Types containing raw pointers or interior mutability may not be.

### Common Primitives

- `Mutex<T>` — mutual exclusion
- `RwLock<T>` — multiple readers OR single writer
- `Arc<T>` — atomic reference counting for shared ownership
- `mpsc::channel` — message passing

### Anti-Pattern: `if let` Deadlock (pre-2024 edition)

```rust
// ❌ Lock held through else block in older editions
if let Some(x) = mutex.lock().unwrap().get("key") {
    // ...
} else {
    mutex.lock().unwrap().insert("key", value); // DEADLOCK
}

// ✅ Extract lock explicitly
let guard = mutex.lock().unwrap();
let result = guard.get("key").cloned();
drop(guard); // Release before else
```

Fixed in Rust 2024 edition.

---

## Type System

### Newtypes

Wrap primitives to create distinct types:

```rust
struct UserId(u64);
struct PostId(u64);

// Now UserId and PostId are incompatible at compile time
```

### `#[must_use]`

Apply to functions/types where ignoring the result is almost always a bug:

```rust
#[must_use = "this returns a new value and does not modify self"]
fn sorted(&self) -> Vec<T>
```

### `impl Trait` in Return Position

Hide concrete types when they're implementation details:

```rust
fn make_iter() -> impl Iterator<Item = u32> {
    (0..10).filter(|x| x % 2 == 0)
}
```

---

## Anti-Patterns

| Anti-Pattern               | Description                                                  | Remedy                                              |
| :------------------------- | :----------------------------------------------------------- | :-------------------------------------------------- |
| **Overengineering**        | Complex abstractions, premature `unsafe`, macro abuse        | Prefer simple, direct solutions                     |
| **Simplistic Design**      | Failing to leverage type system (stringly-typed, bool-blind) | Use enums/newtypes to encode invariants             |
| **Premature Optimization** | Optimizing without profiling                                 | Write clear code first; measure, then optimize      |
| **Documentation Neglect**  | Missing or stale docs                                        | Doc-comments (`///`) with examples; run `cargo doc` |

---

## Blessed Crates

| Domain              | Crate                  | Notes                      |
| :------------------ | :--------------------- | :------------------------- |
| Serialization       | `serde` + `serde_json` | De facto standard          |
| Async Runtime       | `tokio`                | Most widely supported      |
| CLI Parsing         | `clap`                 | Feature-rich, fast         |
| Error (Library)     | `thiserror`            | Derive for custom errors   |
| Error (Application) | `anyhow`               | Context chains, backtraces |
| HTTP Client         | `reqwest`              | Built on `tokio`           |
| Logging             | `tracing`              | Structured, async-aware    |

---

## Quick Reference

- **No `.unwrap()` in library code** — propagate `Result`
- **No `.clone()` without justification** — prefer references
- **No `panic!` in library code** — return errors
- **Use `clippy`** — `cargo clippy -- -D warnings`
- **Format with `rustfmt`** — `cargo fmt`
- **Document public APIs** — `///` with examples

> These idioms refine but are subordinate to the [Code-Edit Constraints](../../ambient.md#code-edit-constraints).