---
name: rust-code-organization
description: Structure Rust code using modules, traits, builders, and newtypes. Use when designing APIs, abstracting behavior, or preventing type confusion.
---

# Code Organization

Patterns for structuring maintainable Rust code.

## Module Structure

Organize by feature/domain, not by type:

```
src/
├── lib.rs              # Public API exports
├── error.rs            # Error types
├── config.rs           # Configuration
├── db/
│   ├── mod.rs          # Module exports
│   ├── repo.rs         # Repository implementation
│   └── models.rs       # Database models
├── pipeline/
│   ├── mod.rs
│   ├── processor.rs
│   └── prefetch.rs
└── scheduler/
    ├── mod.rs
    ├── manager.rs
    └── queue.rs
```

## Module Visibility

```rust
// mod.rs - Control what's public
mod internal;           // Private to this module
pub mod public;         // Public to external crates
pub(crate) mod shared;  // Public within crate only
pub(super) mod parent;  // Public to parent module only

// Re-export for clean API
pub use self::repo::VideoRepository;
pub use self::models::{VideoRecord, VideoStatus};
```

## Traits for Abstraction

```rust
// Define behavior as trait
pub trait Repository {
    type Record;
    type Error;

    async fn get(&self, id: &str) -> Result<Self::Record, Self::Error>;
    async fn save(&self, record: &Self::Record) -> Result<(), Self::Error>;
}

// Business logic depends on trait, not concrete type
pub async fn process<R: Repository>(repo: &R, id: &str) -> Result<()> {
    let record = repo.get(id).await?;
    // Process...
    repo.save(&record).await
}

// Easy to mock in tests
#[cfg(test)]
struct MockRepository;

#[cfg(test)]
impl Repository for MockRepository {
    // Test implementation
}
```

## Builder Pattern

```rust
pub struct Config {
    host: String,
    port: u16,
    timeout: Duration,
}

#[derive(Default)]
pub struct ConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    timeout: Option<Duration>,
}

impl ConfigBuilder {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }

    pub fn build(self) -> Result<Config, ConfigError> {
        Ok(Config {
            host: self.host.ok_or(ConfigError::MissingHost)?,
            port: self.port.unwrap_or(8080),
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
        })
    }
}

// Usage
let config = ConfigBuilder::new()
    .host("localhost")
    .port(3000)
    .build()?;
```

## Newtype Pattern

Prevent mixing up types that have the same underlying representation:

```rust
// Without newtype - easy to mix up!
fn process_user(user_id: Uuid, order_id: Uuid) { ... }
process_user(order_id, user_id);  // Compiles but wrong!

// With newtype - compile-time safety
pub struct UserId(Uuid);
pub struct OrderId(Uuid);

fn process_user(user_id: UserId, order_id: OrderId) { ... }
process_user(order_id, user_id);  // Compile error!

// Derive common traits
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct VideoId(pub i64);

impl VideoId {
    pub fn new(id: i64) -> Self {
        Self(id)
    }

    pub fn inner(&self) -> i64 {
        self.0
    }
}

// Implement Display for logging
impl std::fmt::Display for VideoId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "video:{}", self.0)
    }
}
```

## Function Composition

```rust
fn process_user_data(data: &str) -> Result<User> {
    parse_user_data(data)
        .and_then(validate_user)
        .map(transform_user)
}

// With ? operator for early return
fn process_video(path: &Path) -> Result<Video> {
    let data = read_file(path)?;
    let parsed = parse_video(&data)?;
    let validated = validate_video(parsed)?;
    Ok(transform_video(validated))
}
```

## Struct Update Syntax

```rust
#[derive(Clone)]
pub struct Options {
    pub timeout: Duration,
    pub retries: u32,
    pub verbose: bool,
}

impl Default for Options {
    fn default() -> Self {
        Self {
            timeout: Duration::from_secs(30),
            retries: 3,
            verbose: false,
        }
    }
}

// Create with partial overrides
let options = Options {
    timeout: Duration::from_secs(60),
    ..Default::default()
};
```

## Extension Traits

```rust
// Add methods to external types
pub trait StringExt {
    fn truncate_to(&self, max_len: usize) -> &str;
}

impl StringExt for str {
    fn truncate_to(&self, max_len: usize) -> &str {
        if self.len() <= max_len {
            self
        } else {
            &self[..max_len]
        }
    }
}

// Usage
let short = long_string.truncate_to(100);
```

## Guidelines

- Organize modules by domain, not by type
- Use `pub(crate)` for internal APIs
- Define traits for testable abstractions
- Use builders for complex configuration
- Use newtypes to prevent type confusion
- Prefer composition over inheritance
- Keep public API surface minimal

## Examples

See `hercules-local-algo/src/` for production module organization.
