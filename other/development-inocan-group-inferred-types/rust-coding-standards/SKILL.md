---
name: rust-coding-standards
description: >-
  Master Rust's ownership system, type safety, and zero-cost abstractions
  for building safe, concurrent, and performant systems. Covers borrowing,
  lifetimes, traits, error handling, async/await, and testing patterns.
category: coding-standards
difficulty: intermediate
estimated_time: 45 minutes
version: 1.0.0
tags:
  - rust
  - ownership
  - borrowing
  - memory-safety
  - performance
dependencies: []
---

# Rust Coding Standards

> **Purpose**: Master Rust's ownership system, type safety, and zero-cost abstractions for building safe, concurrent, and performant systems.

## Level 1: Quick Reference

### Core Principles

- **Ownership**: Each value has exactly one owner
- **Borrowing**: References allow multiple readers XOR one writer
- **Zero-cost abstractions**: High-level code compiles to optimal machine code
- **Explicit over implicit**: No hidden allocations or control flow

### Ownership & Borrowing Cheat Sheet

```rust
// Ownership transfer (move)
let s1 = String::from("hello");
let s2 = s1; // s1 is now invalid

// Immutable borrow (multiple allowed)
let s = String::from("hello");
let r1 = &s;
let r2 = &s;
println!("{} and {}", r1, r2); // OK

// Mutable borrow (exclusive)
let mut s = String::from("hello");
let r1 = &mut s;
r1.push_str(" world");

// Copy types (stack-only)
let x = 5;
let y = x; // x is still valid (i32 implements Copy)
```

### Result & Option

```rust
// Option: value may be absent
let name = find_user(42).map(|u| u.name).unwrap_or("Anonymous".into());

// Early return with ?
fn process() -> Result<(), Error> {
    let config = parse_config("app.toml")?;
    Ok(())
}
```

### Essential Checklist

- [ ] `cargo clippy -- -D warnings`
- [ ] `cargo fmt -- --check`
- [ ] `cargo test`
- [ ] `cargo doc --no-deps`
- [ ] `cargo audit`
- [ ] Document all `unsafe` blocks

### Memory Safety Rules

1. **No data races**: Compiler enforces at compile time
2. **No null pointers**: Use `Option<T>` instead
3. **No dangling pointers**: Borrow checker prevents
4. **No use-after-free**: Ownership system prevents
5. **No buffer overflows**: Bounds checking

---

## Level 2: Implementation Guide

### Ownership System

#### The Three Rules

1. Each value has a variable that's its owner
2. There can only be one owner at a time
3. When the owner goes out of scope, the value is dropped

```rust
fn takes_ownership(s: String) {
    println!("{}", s);
} // s dropped here

fn main() {
    let s = String::from("hello");
    takes_ownership(s); // s moved
    // println!("{}", s); // Error: value borrowed after move
}

// Return ownership
fn gives_ownership() -> String {
    String::from("hello")
}
```

### Borrowing & References

```rust
// Multiple immutable borrows allowed
fn calculate_length(s: &String) -> usize {
    s.len()
}

// Only one mutable borrow allowed
fn change(s: &mut String) {
    s.push_str(", world");
}

// Non-lexical lifetimes
let mut s = String::from("hello");
let r1 = &s;
let r2 = &s;
println!("{} and {}", r1, r2); // last use of r1 and r2
let r3 = &mut s; // OK: r1 and r2 no longer used
```

### Lifetime Annotations

```rust
// Specify reference relationships
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime
struct Excerpt<'a> {
    part: &'a str,
}

// Lifetime elision: compiler infers in common patterns
fn first_word(s: &str) -> &str { /* elided lifetimes */ }
```

### Traits & Generics

```rust
pub trait Summary {
    fn summarize(&self) -> String;

    // Default implementation
    fn full_summary(&self) -> String {
        format!("Read more: {}", self.summarize())
    }
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.headline, self.author)
    }
}

// Trait bounds
pub fn notify<T: Summary + Display>(item: &T) {
    println!("Breaking: {}", item.summarize());
}

// where clause for readability
pub fn process<T, U>(t: &T, u: &U) -> String
where
    T: Display + Clone,
    U: Clone + Debug,
{
    format!("{:?}", u)
}
```

### Common Derived Traits

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
pub struct User {
    pub id: u32,
    pub name: String,
}
```

### Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Not found: {0}")]
    NotFound(String),
}

pub type Result<T> = std::result::Result<T, AppError>;

// With anyhow for context
use anyhow::Context;

fn read_config() -> anyhow::Result<Config> {
    let content = fs::read_to_string("config.toml")
        .context("Failed to read config file")?;
    Ok(toml::from_str(&content)?)
}
```

### Async/Await

```rust
use tokio;

#[tokio::main]
async fn main() -> Result<()> {
    let result = fetch_data().await?;
    process(result).await?;
    Ok(())
}

// Concurrent execution
let futures = urls.iter().map(|url| fetch_url(url));
let results = futures::future::join_all(futures).await;

// Spawn tasks
let handle = tokio::spawn(async move {
    expensive_computation().await
});
let result = handle.await?;
```

### Channels

```rust
use tokio::sync::mpsc;

let (tx, mut rx) = mpsc::channel(32);

// Producer
tokio::spawn(async move {
    tx.send(work).await.unwrap();
});

// Consumer
while let Some(result) = rx.recv().await {
    process(result).await;
}
```

### Shared State

```rust
use std::sync::Arc;
use tokio::sync::{Mutex, RwLock};

#[derive(Clone)]
struct AppState {
    counter: Arc<Mutex<u64>>,
    cache: Arc<RwLock<HashMap<String, String>>>,
}

async fn increment(state: AppState) {
    let mut counter = state.counter.lock().await;
    *counter += 1;
}
```

### Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    #[should_panic(expected = "divide by zero")]
    fn test_panic() {
        divide(10, 0);
    }

    #[test]
    fn test_result() -> Result<()> {
        let result = parse_number("42")?;
        assert_eq!(result, 42);
        Ok(())
    }

    #[tokio::test]
    async fn test_async() {
        let result = fetch_data().await;
        assert!(result.is_ok());
    }
}
```

### Performance Patterns

```rust
// Prefer slices over owned strings
fn count_words(text: &str) -> usize {
    text.split_whitespace().count()
}

// Use Cow for conditional cloning
use std::borrow::Cow;

fn process_text(text: &str) -> Cow<str> {
    if text.contains("bad") {
        Cow::Owned(text.replace("bad", "good"))
    } else {
        Cow::Borrowed(text)
    }
}

// Reuse buffers
let mut buffer = String::with_capacity(1024);
for item in items {
    buffer.clear();
    write!(&mut buffer, "{}", item)?;
    send(&buffer)?;
}
```

### Iterators

```rust
// Transformation pipeline (zero-cost)
let sum: i32 = vec![1, 2, 3, 4, 5]
    .iter()
    .filter(|&x| x % 2 == 0)
    .map(|x| x * 2)
    .sum();

// Collect into different types
let doubled: Vec<i32> = numbers.iter().map(|x| x * 2).collect();
let set: HashSet<i32> = numbers.into_iter().collect();
```

---

## Level 3: Deep Dive Resources

For comprehensive coverage of advanced topics, see **[REFERENCE.md](./REFERENCE.md)**:

### Advanced Patterns

- **Newtype Pattern**: Type safety via wrapper types
- **Typestate Pattern**: Encode state machines in types
- **Builder Pattern**: Fluent API construction

### Unsafe Code Guidelines

- Documenting safety invariants
- Minimizing unsafe scope
- Testing with Miri

### Complete Examples

- Full async service implementation
- Property-based testing with proptest
- Mocking with mockall
- Integration test patterns

### Configuration Files

- `config/rustfmt.toml` - Formatter configuration
- `config/clippy.toml` - Linter rules
- `templates/` - Project templates

### Performance Deep Dive

- Profiling with flamegraph
- Compiler optimization flags
- Memory profiling with valgrind

### Learning Path

1. **Start**: [Rust Book](https://doc.rust-lang.org/book/)
2. **Practice**: [Rustlings](https://github.com/rust-lang/rustlings)
3. **Patterns**: [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
4. **Async**: [Tokio Tutorial](https://tokio.rs/tokio/tutorial)

### Common Pitfalls

1. Fighting the borrow checker - design with ownership in mind
2. Over-using `.clone()` - profile before optimizing
3. Ignoring Clippy warnings - they're usually right
4. Not using `?` operator - makes error handling cleaner
5. Premature unsafe - try safe abstractions first
6. String vs &str confusion - prefer &str for parameters

---

**Skill Complete**: Comprehensive Rust coding standards covering ownership, traits, error handling, concurrency, testing, and performance. See REFERENCE.md for advanced patterns and complete examples.
