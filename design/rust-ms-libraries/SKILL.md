---
name: rust-ms-libraries
description: Microsoft Pragmatic Rust Library Guidelines. Use when designing library crates, public APIs, managing dependencies, or creating reusable components.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Microsoft Pragmatic Rust - Library Guidelines

Guidelines for building high-quality, reusable Rust libraries.

## Crate Structure

### Flat vs Nested Modules
```rust
// GOOD - flat structure for small libraries
// src/lib.rs
mod error;
mod types;
mod client;

pub use error::Error;
pub use types::{Config, Options};
pub use client::Client;

// GOOD - nested for large libraries
// src/lib.rs
pub mod http;
pub mod storage;
pub mod auth;

// Re-export common items at root
pub use http::Client;
pub use storage::Store;
```

### Prelude Pattern
```rust
// For libraries with many types
// src/prelude.rs
pub use crate::error::{Error, Result};
pub use crate::types::{Config, Options, Status};
pub use crate::traits::{Execute, Validate};

// Users can import everything
use my_library::prelude::*;
```

## API Design

### Accept Generics, Return Concrete
```rust
// GOOD - flexible input, concrete output
pub fn process(input: impl AsRef<str>) -> String {
    let s = input.as_ref();
    s.to_uppercase()
}

// Can be called with &str, String, Cow<str>, etc.
process("hello");
process(String::from("hello"));
```

### Use Into for Ownership Transfer
```rust
impl Client {
    // Accept anything convertible to String
    pub fn set_name(&mut self, name: impl Into<String>) {
        self.name = name.into();
    }
}

// Both work
client.set_name("name");
client.set_name(string_var);
```

### Builder Pattern for Complex Construction
```rust
#[derive(Default)]
pub struct ClientBuilder {
    host: Option<String>,
    port: Option<u16>,
    timeout: Option<Duration>,
}

impl ClientBuilder {
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
    
    pub fn build(self) -> Result<Client, BuildError> {
        Ok(Client {
            host: self.host.ok_or(BuildError::MissingHost)?,
            port: self.port.unwrap_or(8080),
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
        })
    }
}
```

### Sealed Traits for Extension Prevention
```rust
mod private {
    pub trait Sealed {}
}

/// A trait that cannot be implemented outside this crate.
pub trait MyTrait: private::Sealed {
    fn method(&self);
}

// Implement Sealed for allowed types
impl private::Sealed for MyType {}
impl MyTrait for MyType {
    fn method(&self) { ... }
}
```

## Error Design

### Library-Specific Error Types
```rust
use thiserror::Error;

/// Errors that can occur in this library.
#[derive(Debug, Error)]
#[non_exhaustive]  // Allow adding variants
pub enum Error {
    #[error("connection failed: {0}")]
    Connection(String),
    
    #[error("invalid configuration: {0}")]
    Config(String),
    
    #[error("operation timed out after {duration:?}")]
    Timeout { duration: Duration },
    
    #[error(transparent)]
    Io(#[from] std::io::Error),
}

/// Result type alias for convenience
pub type Result<T> = std::result::Result<T, Error>;
```

### Don't Expose Internal Errors
```rust
// BAD - leaks internal dependency
#[derive(Error)]
pub enum Error {
    #[error(transparent)]
    Database(#[from] sqlx::Error),  // Exposes sqlx
}

// GOOD - wrap internal errors
#[derive(Error)]
pub enum Error {
    #[error("database error: {0}")]
    Database(String),
}

impl From<sqlx::Error> for Error {
    fn from(e: sqlx::Error) -> Self {
        Error::Database(e.to_string())
    }
}
```

## Dependency Management

### Minimal Dependencies
```toml
# Only depend on what you need
[dependencies]
serde = { version = "1.0", optional = true }

[features]
default = []
serde = ["dep:serde"]
```

### Re-export Dependencies Users Need
```rust
// If users need types from your dependencies, re-export them
pub use bytes::Bytes;
pub use http::StatusCode;
```

### Version Policy
```toml
# Use caret requirements for flexibility
serde = "1.0"        # ^1.0 - allows 1.x updates
tokio = "1"          # ^1 - allows 1.x updates

# Pin exact versions only when necessary
some-crate = "=1.2.3"
```

## Resilience

### Avoid Global State
```rust
// BAD - global mutable state
static COUNTER: AtomicU64 = AtomicU64::new(0);

// GOOD - instance state
pub struct Counter {
    value: AtomicU64,
}

impl Counter {
    pub fn new() -> Self {
        Self { value: AtomicU64::new(0) }
    }
    
    pub fn increment(&self) -> u64 {
        self.value.fetch_add(1, Ordering::SeqCst)
    }
}
```

### Avoid Thread-Local Storage
```rust
// BAD - hidden state
thread_local! {
    static CACHE: RefCell<HashMap<String, Value>> = RefCell::new(HashMap::new());
}

// GOOD - explicit state
pub struct Cache {
    data: RwLock<HashMap<String, Value>>,
}
```

### Make Types Send + Sync When Possible
```rust
// Ensure thread safety
pub struct Client {
    inner: Arc<ClientInner>,  // Arc for shared ownership
}

// Verify at compile time
static_assertions::assert_impl_all!(Client: Send, Sync);
```

## Documentation

### Crate-Level Docs
```rust
//! # My Library
//!
//! A brief description of what this library does.
//!
//! ## Quick Start
//!
//! ```rust
//! use my_library::Client;
//!
//! let client = Client::builder()
//!     .host("localhost")
//!     .build()?;
//!
//! client.connect().await?;
//! ```
//!
//! ## Features
//!
//! - Feature 1
//! - Feature 2
//!
//! ## Feature Flags
//!
//! - `serde`: Enable serialization support
```

### Document All Public Items
Every public item needs:
- Brief description
- Examples (that compile and run)
- Error conditions for fallible functions
- Panic conditions if applicable

## Versioning

### Semantic Versioning
- MAJOR: Breaking API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### Breaking Changes
```rust
// Use #[deprecated] before removing
#[deprecated(since = "0.5.0", note = "use new_function instead")]
pub fn old_function() { ... }

// Use #[doc(hidden)] for internal items
#[doc(hidden)]
pub fn internal_detail() { ... }
```

## Testing

### Test Public API
```rust
// tests/integration.rs
use my_library::{Client, Config};

#[test]
fn client_connects_successfully() {
    let client = Client::new(Config::default());
    assert!(client.is_valid());
}
```

### Doc Tests Run by Default
```rust
/// Creates a new instance.
///
/// # Examples
///
/// ```
/// let instance = my_library::Instance::new();
/// assert!(instance.is_valid());
/// ```
pub fn new() -> Self { ... }
```

## Cargo.toml Best Practices

```toml
[package]
name = "my-library"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"  # MSRV - Rust 2024 edition requires 1.85+
description = "A brief description"
documentation = "https://docs.rs/my-library"
repository = "https://github.com/org/my-library"
license = "MIT OR Apache-2.0"
keywords = ["keyword1", "keyword2"]
categories = ["category"]

[package.metadata.docs.rs]
all-features = true
rustdoc-args = ["--cfg", "docsrs"]
```
