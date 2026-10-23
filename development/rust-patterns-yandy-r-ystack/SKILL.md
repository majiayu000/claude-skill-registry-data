---
name: rust-patterns
description: 'Guides idiomatic Rust ownership, errors, and concurrency. Use when resolving borrow or lifetime design, structuring crates, or choosing traits and error types.'
---

# Rust Development Patterns

Idiomatic Rust patterns and best practices for building safe, performant, and maintainable applications.

## When to Use

- Writing new Rust code
- Reviewing Rust code
- Refactoring existing Rust code
- Designing crate structure and module layout

## How It Works

This skill enforces idiomatic Rust conventions across six key areas: ownership and borrowing to prevent data races at compile time, `Result`/`?` error propagation with `thiserror` for libraries and `anyhow` for applications, enums and exhaustive pattern matching to make illegal states unrepresentable, traits and generics for zero-cost abstraction, safe concurrency via `Arc<Mutex<T>>`, channels, and async/await, and minimal `pub` surfaces organized by domain.

## Critical Rules

- Borrow by default; take ownership only to store or consume; avoid clones to appease the borrow checker.
- Use `Result` with `?` for error propagation — no `unwrap()` in production or library code.
- `thiserror` for libraries, `anyhow` for applications; avoid `Box<dyn Error>` in library APIs.
- Match exhaustively on business-critical enums — no wildcard `_` arms.
- Use newtypes to wrap primitives and prevent argument mix-ups.
- Seal closed extension points with a private supertrait so downstream crates cannot implement the trait.
- Keep `pub` surface minimal; `pub(crate)` for internal APIs.
- Every `unsafe` block needs a `// SAFETY:` comment stating the invariant.

## References

Paths are relative to this SKILL.md's directory. Read only the file that matches the task. If a file cannot be read, say so.

- [references/ownership-errors-types.md](references/ownership-errors-types.md)
  Read when: ownership and borrowing, lifetimes, `Cow`; error handling with `Result`, `?`, `thiserror`/`anyhow`; enums and exhaustive pattern matching; traits, generics, trait objects; sealed traits; serde-tagged response envelopes.

- [references/concurrency-unsafe-modules.md](references/concurrency-unsafe-modules.md)
  Read when: structs and data modeling, newtypes; iterators and closures; concurrency (`Arc`, `Mutex`, channels, async); unsafe code with SAFETY invariants; module system and crate structure; tooling (clippy, rustfmt, cargo commands).

## Quick Reference: Rust Idioms

| Idiom                               | Description                                                |
| ----------------------------------- | ---------------------------------------------------------- |
| Borrow, don't clone                 | Pass `&T` instead of cloning unless ownership is needed    |
| Make illegal states unrepresentable | Use enums to model valid states only                       |
| `?` over `unwrap()`                 | Propagate errors, never panic in library/production code   |
| Parse, don't validate               | Convert unstructured data to typed structs at the boundary |
| Newtype for type safety             | Wrap primitives in newtypes to prevent argument swaps      |
| Sealed trait for closed extension   | Private supertrait blocks downstream implementations       |
| Prefer iterators over loops         | Declarative chains are clearer and often faster            |
| `#[must_use]` on Results            | Ensure callers handle return values                        |
| `Cow` for flexible ownership        | Avoid allocations when borrowing suffices                  |
| Exhaustive matching                 | No wildcard `_` for business-critical enums                |
| Minimal `pub` surface               | Use `pub(crate)` for internal APIs                         |

## Anti-Patterns to Avoid

```rust
// Bad: .unwrap() in production code
let value = map.get("key").unwrap();

// Bad: .clone() to satisfy borrow checker without understanding why
let data = expensive_data.clone();
process(&original, &data);

// Bad: Using String when &str suffices
fn greet(name: String) { /* should be &str */ }

// Bad: Box<dyn Error> in libraries (use thiserror instead)
fn parse(input: &str) -> Result<Data, Box<dyn std::error::Error>> { todo!() }

// Bad: Ignoring must_use warnings
let _ = validate(input); // Silently discarding a Result

// Bad: Blocking in async context
async fn bad_async() {
    std::thread::sleep(Duration::from_secs(1)); // Blocks the executor!
    // Use: tokio::time::sleep(Duration::from_secs(1)).await;
}
```

**Remember**: If it compiles, it's probably correct — but only if you avoid `unwrap()`, minimize `unsafe`, and let the type system work for you.
