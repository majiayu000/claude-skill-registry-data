---
name: rust-error-handling
description: Rust error handling patterns and best practices. Use when designing error types, implementing error propagation, adding error context, converting between error types, or debugging error handling issues.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Rust Error Handling

Comprehensive guide to error handling in Rust projects.

## Choosing the Right Approach

### Library Crates: Use thiserror

```rust
use thiserror::Error;

/// Errors that can occur in this library.
#[derive(Debug, Error)]
pub enum Error {
    /// Input validation failed.
    #[error("invalid input: {message}")]
    InvalidInput { message: String },
    
    /// Resource was not found.
    #[error("{resource_type} not found: {id}")]
    NotFound {
        resource_type: &'static str,
        id: String,
    },
    
    /// Operation timed out.
    #[error("operation timed out after {duration:?}")]
    Timeout { duration: std::time::Duration },
    
    /// Wraps IO errors.
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    /// Wraps serialization errors.
    #[error("serialization error: {0}")]
    Serialization(#[from] serde_json::Error),
}

/// Convenient Result alias.
pub type Result<T> = std::result::Result<T, Error>;
```

### Application Binaries: Use anyhow

```rust
use anyhow::{anyhow, bail, ensure, Context, Result};

fn main() -> Result<()> {
    let config = load_config()
        .context("failed to load configuration")?;
    
    run_app(config)
        .context("application error")?;
    
    Ok(())
}

fn load_config() -> Result<Config> {
    let path = std::env::var("CONFIG_PATH")
        .context("CONFIG_PATH environment variable not set")?;
    
    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("failed to read config from {path}"))?;
    
    let config: Config = toml::from_str(&content)
        .context("failed to parse configuration")?;
    
    // Use ensure! for validations
    ensure!(config.workers > 0, "workers must be greater than 0");
    ensure!(config.port != 0, "port cannot be 0");
    
    Ok(config)
}

fn validate_input(input: &str) -> Result<()> {
    if input.is_empty() {
        bail!("input cannot be empty");
    }
    
    if input.len() > 1000 {
        bail!("input too long: {} bytes (max 1000)", input.len());
    }
    
    Ok(())
}
```

## Error Design Patterns

### Structured Error Data

```rust
#[derive(Debug, Error)]
pub enum ValidationError {
    #[error("field '{field}' is required")]
    Required { field: &'static str },
    
    #[error("field '{field}' must be between {min} and {max}, got {value}")]
    OutOfRange {
        field: &'static str,
        min: i64,
        max: i64,
        value: i64,
    },
    
    #[error("field '{field}' has invalid format: {reason}")]
    InvalidFormat {
        field: &'static str,
        reason: String,
    },
}

// Usage
fn validate_age(age: i32) -> Result<(), ValidationError> {
    if age < 0 || age > 150 {
        return Err(ValidationError::OutOfRange {
            field: "age",
            min: 0,
            max: 150,
            value: age as i64,
        });
    }
    Ok(())
}
```

### IO Error Kinds (Rust 1.85+)

```rust
use std::io::{Error, ErrorKind};

fn handle_io_error(err: Error) {
    match err.kind() {
        // New in Rust 1.85
        ErrorKind::QuotaExceeded => {
            eprintln!("Disk quota exceeded");
        }
        ErrorKind::CrossesDevices => {
            eprintln!("Cannot move across filesystems, will copy instead");
        }
        // Common kinds
        ErrorKind::NotFound => {
            eprintln!("File not found");
        }
        ErrorKind::PermissionDenied => {
            eprintln!("Permission denied");
        }
        ErrorKind::TimedOut => {
            eprintln!("Operation timed out");
        }
        _ => {
            eprintln!("IO error: {err}");
        }
    }
}
```

### Error Categorization

```rust
#[derive(Debug, Error)]
pub enum Error {
    // Client errors (4xx equivalent)
    #[error("validation error: {0}")]
    Validation(#[from] ValidationError),
    
    #[error("not found: {0}")]
    NotFound(String),
    
    #[error("unauthorized: {0}")]
    Unauthorized(String),
    
    // Server errors (5xx equivalent)
    #[error("internal error: {0}")]
    Internal(String),
    
    #[error("service unavailable: {0}")]
    Unavailable(String),
}

impl Error {
    /// Returns true if this is a client error (retrying won't help).
    pub fn is_client_error(&self) -> bool {
        matches!(self, 
            Error::Validation(_) | 
            Error::NotFound(_) | 
            Error::Unauthorized(_)
        )
    }
    
    /// Returns true if this error is retryable.
    pub fn is_retryable(&self) -> bool {
        matches!(self, Error::Unavailable(_))
    }
}
```

### Opaque vs Transparent Wrapping

```rust
// Transparent: expose source error type
#[derive(Debug, Error)]
pub enum Error {
    #[error(transparent)]
    Io(#[from] std::io::Error),
}

// Opaque: hide implementation details
#[derive(Debug, Error)]
pub enum Error {
    #[error("storage error: {0}")]
    Storage(String),
}

impl From<sqlx::Error> for Error {
    fn from(e: sqlx::Error) -> Self {
        // Don't expose sqlx types to consumers
        Error::Storage(e.to_string())
    }
}
```

## Error Propagation

### The ? Operator

```rust
fn process() -> Result<Output, Error> {
    let input = read_input()?;      // Propagates Error
    let parsed = parse(input)?;      // Propagates Error
    let result = compute(parsed)?;   // Propagates Error
    Ok(result)
}
```

### Converting Error Types

```rust
fn process() -> Result<Output, MyError> {
    // Using From trait (via #[from] or manual impl)
    let data = read_file()?;  // io::Error -> MyError
    
    // Using map_err for custom conversion
    let parsed = parse(&data)
        .map_err(|e| MyError::Parse(e.to_string()))?;
    
    // Using ok_or for Option -> Result
    let value = parsed.get("key")
        .ok_or(MyError::MissingField("key"))?;
    
    Ok(value)
}
```

### Adding Context

```rust
use anyhow::Context;

fn load_workflow(id: &str) -> anyhow::Result<Workflow> {
    let path = get_workflow_path(id)
        .with_context(|| format!("invalid workflow id: {id}"))?;
    
    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("failed to read workflow file: {}", path.display()))?;
    
    let workflow: Workflow = serde_json::from_str(&content)
        .with_context(|| format!("failed to parse workflow: {id}"))?;
    
    workflow.validate()
        .with_context(|| format!("workflow validation failed: {id}"))?;
    
    Ok(workflow)
}

// Error output:
// Error: workflow validation failed: my-workflow
// 
// Caused by:
//     0: field 'steps' cannot be empty
```

## Error Handling Patterns

### Match on Error Variants

```rust
match do_operation() {
    Ok(result) => use_result(result),
    Err(Error::NotFound(id)) => {
        log::warn!("Resource not found: {id}");
        create_default()
    }
    Err(Error::Timeout { duration }) => {
        log::error!("Operation timed out after {duration:?}");
        Err(Error::Timeout { duration })
    }
    Err(e) => Err(e),  // Propagate other errors
}
```

### Fallback Values

```rust
// Default on error
let config = load_config().unwrap_or_default();

// Specific fallback
let port = parse_port(input).unwrap_or(8080);

// Fallback with logging
let value = compute()
    .inspect_err(|e| log::warn!("Computation failed: {e}, using default"))
    .unwrap_or_default();
```

### Collecting Results

```rust
// Fail fast: stop on first error
let results: Result<Vec<_>, Error> = items
    .into_iter()
    .map(process_item)
    .collect();

// Collect all: gather successes and failures (requires itertools)
use itertools::Itertools;
let (successes, failures): (Vec<_>, Vec<_>) = items
    .into_iter()
    .map(process_item)
    .partition_result();  // From itertools crate

// Partition manually (no external dependencies)
let mut successes = Vec::new();
let mut failures = Vec::new();
for item in items {
    match process_item(item) {
        Ok(result) => successes.push(result),
        Err(e) => failures.push(e),
    }
}
```

## Async Error Handling

```rust
use anyhow::{Context, Result};

async fn fetch_data(url: &str) -> Result<Data> {
    let response = reqwest::get(url)
        .await
        .with_context(|| format!("failed to fetch {url}"))?;
    
    let status = response.status();
    if !status.is_success() {
        anyhow::bail!("request failed with status {status}");
    }
    
    let data = response
        .json::<Data>()
        .await
        .context("failed to parse response")?;
    
    Ok(data)
}

// With timeout
use tokio::time::{timeout, Duration};

async fn fetch_with_timeout(url: &str) -> Result<Data> {
    timeout(Duration::from_secs(10), fetch_data(url))
        .await
        .context("request timed out")?
}
```

## Testing Errors

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn returns_error_on_invalid_input() {
        let result = process("");
        assert!(result.is_err());
        
        let error = result.unwrap_err();
        assert!(matches!(error, Error::InvalidInput { .. }));
    }
    
    #[test]
    fn error_message_contains_details() {
        let error = Error::NotFound {
            resource_type: "workflow",
            id: "test-123".into(),
        };
        
        let message = error.to_string();
        assert!(message.contains("workflow"));
        assert!(message.contains("test-123"));
    }
    
    #[test]
    fn error_source_chain() {
        let io_error = std::io::Error::new(
            std::io::ErrorKind::NotFound,
            "file not found"
        );
        let error = Error::Io(io_error);
        
        // Check source chain
        use std::error::Error as _;
        assert!(error.source().is_some());
    }
}
```

## Nebula Error Conventions

1. **Each crate defines its own Error type** - no shared error crate
2. **Use thiserror** for all library crates
3. **Use anyhow** only in binaries and tests
4. **Add context** at API boundaries
5. **Don't expose internal dependencies** in public error types
6. **Include actionable information** in error messages

```rust
// Nebula pattern
// crates/nebula-scheduler/src/error.rs
use thiserror::Error;

#[derive(Debug, Error)]
pub enum SchedulerError {
    #[error("workflow '{workflow_id}' not found")]
    WorkflowNotFound { workflow_id: String },
    
    #[error("schedule '{schedule_id}' is invalid: {reason}")]
    InvalidSchedule {
        schedule_id: String,
        reason: String,
    },
    
    #[error("executor error: {0}")]
    Executor(#[from] nebula_executor::Error),
}

pub type Result<T> = std::result::Result<T, SchedulerError>;
```
