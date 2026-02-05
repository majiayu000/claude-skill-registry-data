---
name: rust-ms-universal
description: Microsoft Pragmatic Rust Universal Guidelines. Use when reviewing naming conventions, code style, import organization, or applying foundational Rust idioms like Option/Result combinators and destructuring.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Microsoft Pragmatic Rust - Universal Guidelines

These guidelines apply to ALL Rust code regardless of context.

## Naming Conventions

### Types and Traits
```rust
// PascalCase for types, traits, enums
struct WorkflowExecutor;
trait Executable;
enum ExecutionState;

// Type parameters: single uppercase or descriptive PascalCase
fn process<T>(item: T);
fn map<Input, Output>(f: impl Fn(Input) -> Output);
```

### Functions and Variables
```rust
// snake_case for functions, methods, variables, modules
fn execute_workflow();
let execution_count = 0;
mod workflow_engine;

// Prefix unused variables with underscore
let _unused = compute();
```

### Constants and Statics
```rust
// SCREAMING_SNAKE_CASE
const MAX_RETRIES: u32 = 3;
static GLOBAL_CONFIG: LazyLock<Config> = LazyLock::new(|| Config::load());
```

### Acronyms
```rust
// Treat acronyms as words
struct HttpClient;      // Not HTTPClient
struct JsonParser;      // Not JSONParser
fn parse_xml();         // Not parse_XML
```

## Code Style

### Imports
```rust
// Group imports: std, external crates, internal modules
use std::collections::HashMap;
use std::sync::Arc;

use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;

use crate::error::Error;
use crate::types::{WorkflowId, ExecutionId};
```

### Visibility
```rust
// Default to private, expose minimum necessary
pub struct Config {
    pub name: String,           // Public field
    pub(crate) internal: Data,  // Crate-visible
    secret: Secret,             // Private
}

// Use pub(crate) for internal APIs
pub(crate) fn internal_helper() {}
```

### Function Design
```rust
// Prefer &self over self when possible
impl Config {
    pub fn name(&self) -> &str { &self.name }
    
    // Use self when consuming
    pub fn into_builder(self) -> ConfigBuilder { ... }
}

// Prefer impl Trait over generics for simple cases
fn process(items: impl Iterator<Item = u32>) -> u32 {
    items.sum()
}

// Use generics when type appears multiple times
fn compare<T: Ord>(a: &T, b: &T) -> Ordering {
    a.cmp(b)
}
```

## Idioms

### Option and Result
```rust
// Prefer combinators over match
let value = option.unwrap_or_default();
let value = option.map(|x| x * 2);
let result = result.map_err(Error::from)?;

// Use ok_or for Option -> Result
let value = option.ok_or(Error::NotFound)?;

// Use transpose for Option<Result<T>> <-> Result<Option<T>>
let result: Result<Option<i32>, Error> = option_result.transpose();

// is_none_or (Rust 1.82+) - cleaner than matches!
if option.is_none_or(|x| x > 10) { /* None or > 10 */ }

// Result::flatten (Rust 1.89+)
let nested: Result<Result<i32, E>, E> = Ok(Ok(42));
let flat = nested.flatten();  // Ok(42)

// get_or_insert_default (Rust 1.83+)
let value = option.get_or_insert_default();
```

### Iteration
```rust
// Prefer iterators over indexing
for item in &items { process(item); }

// Use enumerate when index needed
for (i, item) in items.iter().enumerate() { ... }

// Chain operations
let result: Vec<_> = items.iter()
    .filter(|x| x.valid)
    .map(|x| x.value)
    .collect();
```

### Destructuring
```rust
// Destructure in function parameters
fn process_point(&(x, y): &(i32, i32)) { ... }

// Destructure in match
match result {
    Ok(value) => use_value(value),
    Err(Error::NotFound) => handle_not_found(),
    Err(e) => return Err(e),
}

// Destructure structs
let Config { name, timeout, .. } = config;
```

## Type Design

### Prefer Strong Types
```rust
// BAD - primitive obsession
fn create_user(name: String, email: String, age: u32);

// GOOD - newtype wrappers
struct UserName(String);
struct Email(String);
struct Age(u32);

fn create_user(name: UserName, email: Email, age: Age);
```

### Implement Standard Traits
```rust
// Always derive when possible
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct WorkflowId(Uuid);

// Implement Display for user-facing output
impl std::fmt::Display for WorkflowId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}
```

### Use #[must_use]
```rust
// For functions where ignoring result is likely a bug
#[must_use]
pub fn validate(&self) -> bool { ... }

#[must_use = "iterator adaptors are lazy"]
pub fn filter_valid(self) -> impl Iterator<Item = Item> { ... }
```

## Error Handling

### Use thiserror for Libraries
```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ProcessError {
    #[error("invalid input: {0}")]
    InvalidInput(String),
    
    #[error("operation failed: {source}")]
    OperationFailed {
        #[from]
        source: std::io::Error,
    },
}
```

### Propagate with ?
```rust
fn process() -> Result<Output, Error> {
    let data = load_data()?;
    let validated = validate(data)?;
    let result = transform(validated)?;
    Ok(result)
}
```

### Add Context
```rust
use anyhow::Context;

fn load_config(path: &Path) -> anyhow::Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("failed to read config from {}", path.display()))?;
    
    toml::from_str(&content)
        .context("failed to parse config")
}
```

## Documentation

### Document Public Items
```rust
/// Brief one-line description.
///
/// Longer explanation if needed.
///
/// # Examples
///
/// ```
/// let result = function(42)?;
/// assert_eq!(result, 84);
/// ```
pub fn function(input: i32) -> Result<i32, Error> { ... }
```

### Use Semantic Line Breaks
```rust
/// This is a long description that explains the function behavior.
/// Each sentence starts on a new line for better diffs.
/// This makes code review easier.
```

## Testing

### Unit Tests in Same File
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_case() {
        assert_eq!(function(2), 4);
    }
}
```

### Test Names Describe Behavior
```rust
#[test]
fn returns_none_when_key_not_found() { ... }

#[test]
fn panics_on_invalid_input() { ... }

#[test]
fn handles_empty_collection_gracefully() { ... }
```

## Clippy Compliance

Always run with warnings as errors:
```bash
cargo clippy --workspace -- -D warnings
```

Common lints to enable:
```rust
#![warn(clippy::pedantic)]
#![warn(clippy::unwrap_used)]
#![warn(clippy::expect_used)]
#![allow(clippy::module_name_repetitions)]  // If needed
```
