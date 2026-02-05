---
name: rust-best-practices
description: Rust development best practices, patterns, and conventions. Use when writing Rust code, reviewing .rs files, discussing ownership, lifetimes, borrowing, or Cargo configuration. Triggers on mentions of Rust, Cargo, ownership, borrowing, lifetimes, traits, async Rust, tokio.
---

# Rust Best Practices

## Ownership and Borrowing

### Prefer Borrowing Over Ownership
```rust
// Bad - takes ownership unnecessarily
fn print_name(name: String) {
    println!("{}", name);
}

// Good - borrows immutably
fn print_name(name: &str) {
    println!("{}", name);
}
```

### Use References Appropriately
```rust
// Immutable borrow for reading
fn calculate_length(s: &String) -> usize {
    s.len()
}

// Mutable borrow for modification
fn push_char(s: &mut String, c: char) {
    s.push(c);
}
```

## Error Handling

### Use Result and Option
```rust
fn find_user(id: u32) -> Option<User> {
    users.get(&id).cloned()
}

fn parse_config(path: &str) -> Result<Config, ConfigError> {
    let content = fs::read_to_string(path)?;
    toml::from_str(&content).map_err(ConfigError::Parse)
}
```

### Custom Error Types
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("not found: {0}")]
    NotFound(String),

    #[error("validation error: {field}")]
    Validation { field: String },
}
```

### Propagate with ?
```rust
fn process_file(path: &str) -> Result<Data, Error> {
    let content = fs::read_to_string(path)?;
    let parsed = serde_json::from_str(&content)?;
    let validated = validate(parsed)?;
    Ok(validated)
}
```

## Structs and Enums

### Builder Pattern
```rust
#[derive(Default)]
pub struct ServerBuilder {
    port: Option<u16>,
    host: Option<String>,
}

impl ServerBuilder {
    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn build(self) -> Result<Server, BuildError> {
        Ok(Server {
            port: self.port.unwrap_or(8080),
            host: self.host.unwrap_or_else(|| "localhost".into()),
        })
    }
}
```

### Newtype Pattern
```rust
pub struct UserId(u64);
pub struct Email(String);

impl Email {
    pub fn new(email: String) -> Result<Self, ValidationError> {
        if email.contains('@') {
            Ok(Self(email))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }
}
```

### Enums for State
```rust
enum ConnectionState {
    Disconnected,
    Connecting { attempt: u32 },
    Connected { session_id: String },
    Error { message: String },
}
```

## Traits

### Implement Standard Traits
```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct User {
    pub id: u64,
    pub name: String,
}
```

### Trait Objects vs Generics
```rust
// Static dispatch (monomorphization)
fn process<T: Handler>(handler: T) { ... }

// Dynamic dispatch (trait object)
fn process(handler: &dyn Handler) { ... }
fn process(handler: Box<dyn Handler>) { ... }
```

### Extension Traits
```rust
pub trait StringExt {
    fn truncate_ellipsis(&self, max_len: usize) -> String;
}

impl StringExt for str {
    fn truncate_ellipsis(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len - 3])
        }
    }
}
```

## Lifetimes

### Elision Rules
```rust
// Lifetimes elided - single input reference
fn first_word(s: &str) -> &str { ... }

// Explicit when multiple inputs
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str { ... }
```

### Struct Lifetimes
```rust
struct Parser<'a> {
    input: &'a str,
    position: usize,
}

impl<'a> Parser<'a> {
    fn new(input: &'a str) -> Self {
        Self { input, position: 0 }
    }
}
```

## Async Rust

### Tokio Patterns
```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let result = fetch_data().await?;
    Ok(())
}

async fn fetch_data() -> Result<Data, Error> {
    let client = reqwest::Client::new();
    let response = client.get(URL).send().await?;
    response.json().await.map_err(Into::into)
}
```

### Concurrent Operations
```rust
use futures::future::join_all;

async fn fetch_all(urls: Vec<String>) -> Vec<Result<Response, Error>> {
    let futures: Vec<_> = urls.into_iter()
        .map(|url| fetch_one(url))
        .collect();

    join_all(futures).await
}
```

## Testing

### Unit Tests
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn test_divide_by_zero() {
        divide(1, 0);
    }
}
```

### Integration Tests
```rust
// tests/integration_test.rs
use mylib::process;

#[test]
fn test_full_workflow() {
    let result = process("input");
    assert!(result.is_ok());
}
```

## Performance

### Avoid Unnecessary Allocations
```rust
// Bad - allocates new String
fn process(s: &str) -> String {
    s.to_uppercase()
}

// Good when possible - use Cow
use std::borrow::Cow;
fn process(s: &str) -> Cow<str> {
    if s.chars().any(|c| c.is_lowercase()) {
        Cow::Owned(s.to_uppercase())
    } else {
        Cow::Borrowed(s)
    }
}
```

### Use Iterators
```rust
// Good - lazy, zero-cost
let sum: i32 = numbers.iter()
    .filter(|n| **n > 0)
    .map(|n| n * 2)
    .sum();
```

## Anti-Patterns to Avoid

- `.unwrap()` in production code
- Excessive `.clone()` to "fix" borrow checker
- `unsafe` without clear justification
- Ignoring compiler warnings
- Not using `clippy`
- Global mutable state (`lazy_static` with `Mutex`)
