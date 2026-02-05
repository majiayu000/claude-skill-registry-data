---
name: rust-safety
description: Rust safety patterns and secure coding. Use when writing code that handles untrusted input, uses unsafe blocks, deals with memory safety, or requires security review.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Rust Safety Guidelines

Based on Microsoft Pragmatic Rust Guidelines and Rust security best practices.

## Unsafe Code Guidelines

### When to Use Unsafe

Only use `unsafe` when:
1. FFI (Foreign Function Interface) calls
2. Performance-critical code where safe alternatives are too slow
3. Implementing low-level abstractions that can't be expressed safely

### Unsafe Block Requirements

```rust
// ALWAYS document safety invariants
/// # Safety
///
/// - `ptr` must be valid and properly aligned
/// - `ptr` must point to initialized memory
/// - The memory must not be accessed through any other pointer during this call
unsafe fn process_raw(ptr: *mut u8, len: usize) {
    // SAFETY: Caller guarantees ptr validity and exclusive access
    let slice = unsafe { std::slice::from_raw_parts_mut(ptr, len) };
    // ...
}
```

### Minimize Unsafe Scope

```rust
// BAD - too much in unsafe block
unsafe {
    let ptr = get_pointer();
    let len = calculate_length();  // Safe operation in unsafe block
    let slice = std::slice::from_raw_parts(ptr, len);
    process(slice);  // Safe operation in unsafe block
}

// GOOD - minimal unsafe scope
let ptr = get_pointer();
let len = calculate_length();
// SAFETY: ptr is valid for len bytes per get_pointer contract
let slice = unsafe { std::slice::from_raw_parts(ptr, len) };
process(slice);
```

## Input Validation

### File Existence Check (Rust 1.81+)

```rust
use std::fs;

// GOOD - explicit existence check
if fs::exists("config.toml")? {
    let config = fs::read_to_string("config.toml")?;
}

// For optional files
let config = if fs::exists(&path)? {
    Some(fs::read_to_string(&path)?)
} else {
    None
};
```

### Validate at Boundaries

```rust
/// Parses user-provided workflow configuration.
///
/// # Errors
///
/// Returns error if input exceeds size limits or contains invalid data.
pub fn parse_config(input: &str) -> Result<Config, ParseError> {
    // Validate size first
    if input.len() > MAX_CONFIG_SIZE {
        return Err(ParseError::TooLarge { 
            size: input.len(), 
            max: MAX_CONFIG_SIZE 
        });
    }
    
    // Parse with timeout protection
    let config: Config = serde_json::from_str(input)
        .map_err(ParseError::InvalidJson)?;
    
    // Validate parsed values
    config.validate()?;
    
    Ok(config)
}
```

### Numeric Overflow Protection

```rust
// BAD - can panic or wrap
let result = a + b;

// GOOD - explicit handling
let result = a.checked_add(b).ok_or(Error::Overflow)?;

// Or use saturating for counters
let count = count.saturating_add(1);

// Or wrapping when intentional
let hash = hash.wrapping_mul(PRIME);
```

### String Handling

```rust
// BAD - potential DoS with large allocations
let repeated = input.repeat(count);

// GOOD - validate first
if count > MAX_REPEAT || input.len().saturating_mul(count) > MAX_SIZE {
    return Err(Error::TooLarge);
}
let repeated = input.repeat(count);
```

## Memory Safety

### Avoid Use-After-Free

```rust
// BAD - reference may outlive data
struct Handler<'a> {
    data: &'a str,
}

// GOOD - owned data
struct Handler {
    data: String,
}

// OR - explicit lifetime with clear ownership
struct Handler<'a> {
    data: &'a str,
    _marker: PhantomData<&'a ()>,
}
```

### Prevent Data Races

```rust
use std::sync::Arc;
use parking_lot::RwLock;  // Prefer over std::sync::Mutex

// Thread-safe shared state
struct SharedState {
    data: Arc<RwLock<Data>>,
}

impl SharedState {
    fn update(&self, new_data: Data) {
        let mut guard = self.data.write();
        *guard = new_data;
        // Lock released here
    }
    
    fn read(&self) -> Data {
        self.data.read().clone()
    }
}
```

## Error Handling Safety

### Don't Expose Internal Details

```rust
// BAD - leaks internal paths and structure
#[error("Failed to read {path}: {source}")]
ReadError { path: PathBuf, source: std::io::Error }

// GOOD - sanitized error (user sees generic message, details for logging)
#[error("Failed to read configuration file")]
ConfigReadError {
    path: PathBuf,  // Keep for internal logging
    #[source]
    source: std::io::Error,
}

impl ConfigReadError {
    /// Returns internal details for logging (not user-facing).
    pub fn internal_details(&self) -> String {
        format!("path: {:?}, error: {}", self.path, self.source)
    }
}
```

### Fail Securely

```rust
// BAD - returns partial data on error
fn load_secrets() -> Vec<Secret> {
    let mut secrets = Vec::new();
    for path in paths {
        if let Ok(s) = load_secret(path) {
            secrets.push(s);
        }
        // Silently ignores errors
    }
    secrets
}

// GOOD - fail completely or succeed completely
fn load_secrets() -> Result<Vec<Secret>, Error> {
    paths.iter()
        .map(load_secret)
        .collect::<Result<Vec<_>, _>>()
}
```

## Cryptography

### Use High-Level Libraries

```rust
// GOOD - use established libraries
use argon2::{Argon2, PasswordHash, PasswordVerifier};
use rand::rngs::OsRng;

fn hash_password(password: &str) -> Result<String, Error> {
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    Ok(argon2.hash_password(password.as_bytes(), &salt)?.to_string())
}

fn verify_password(password: &str, hash: &str) -> Result<bool, Error> {
    let parsed = PasswordHash::new(hash)?;
    Ok(Argon2::default().verify_password(password.as_bytes(), &parsed).is_ok())
}
```

### Secure Random Generation

```rust
use rand::{rngs::OsRng, RngCore};

fn generate_token() -> [u8; 32] {
    let mut token = [0u8; 32];
    OsRng.fill_bytes(&mut token);
    token
}
```

## Denial of Service Prevention

### Resource Limits

```rust
/// Process with bounded resource usage.
pub async fn process_with_limits(
    input: &[u8],
    limits: &Limits,
) -> Result<Output, Error> {
    // Size limit
    if input.len() > limits.max_input_size {
        return Err(Error::InputTooLarge);
    }
    
    // Time limit
    tokio::time::timeout(limits.max_duration, async {
        process_inner(input).await
    })
    .await
    .map_err(|_| Error::Timeout)?
}
```

### Prevent Regex DoS

```rust
use regex::Regex;

// BAD - user-provided regex
let re = Regex::new(user_input)?;

// GOOD - pre-compiled patterns or validated
use std::sync::LazyLock;
use regex::Regex;

const ALLOWED_PATTERN: &str = r"^[a-zA-Z0-9_-]+$";
static NAME_REGEX: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(ALLOWED_PATTERN).unwrap()
});

fn validate_name(name: &str) -> bool {
    NAME_REGEX.is_match(name)
}
```

## Verification Commands

```bash
# Security audit
cargo audit

# Check for unsafe code
cargo geiger

# Clippy security lints
cargo clippy -- -W clippy::unwrap_used -W clippy::expect_used

# Miri for undefined behavior (nightly)
cargo +nightly miri test
```

## Common Safety Issues Reference

### Memory Safety Issues
- **Stack/Heap overflow** - exceeding memory limits
- **Integer overflow/underflow** - use `checked_*`, `saturating_*`, `wrapping_*`
- **Null pointer dereference** - Rust prevents via Option, but watch for FFI
- **Out-of-bounds access** - use safe slice methods, avoid unsafe indexing
- **Uninitialized memory** - use `MaybeUninit` carefully in unsafe
- **Type confusion** - ensure proper type casting, avoid transmute abuse

### Rust-Specific Issues to Watch
- **RefCell panic** - borrow checking at runtime can panic
- **Mutex poisoning** - handle `PoisonError` from panicked threads
- **Drop order dependencies** - be explicit about destruction order
- **Async runtime blocking** - never use `std::thread::sleep` in async
- **Pin projection issues** - use `pin-project` crate for safe projections
- **Send/Sync violations** - ensure types are thread-safe if shared

### Concurrency Issues
- **Race condition** - use proper synchronization (Mutex, RwLock, atomics)
- **Deadlock** - consistent lock ordering, avoid nested locks
- **Livelock** - ensure progress in retry loops
- **Starvation** - use fair locks (parking_lot), avoid long critical sections
- **False sharing** - pad cache lines with `#[repr(align(64))]`
- **ABA problem** - use epoch-based reclamation for lock-free code

### Performance Anti-patterns
- **Excessive cloning** - use references, Cow, or Arc where possible
- **String concatenation in loops** - preallocate with `String::with_capacity`
- **Unnecessary boxing** - prefer stack allocation for small types
- **N+1 queries** - batch database operations
- **Busy waiting** - use proper async or condvar waiting

### Error Handling Anti-patterns
- **Silent failures** - never ignore errors with `let _ = ...`
- **Error swallowing** - log or propagate all errors
- **Panic in libraries** - return Result, don't panic
- **Unwrap/expect abuse** - only use in tests or with documented invariants
- **Context loss** - chain errors with `.context()` or `#[from]`

### Resource Management
- **Resource leaks** - use RAII, implement Drop properly
- **Connection pool exhaustion** - bound pools, add timeouts
- **Unbounded growth** - use bounded channels and collections
- **File descriptor exhaustion** - close handles promptly

## Nebula-Specific Safety

- Never log credentials or secrets
- Validate all external input at API boundaries
- Use timeouts for all external calls
- Sanitize error messages before returning to users
- Use `secrecy` crate for sensitive data in memory
