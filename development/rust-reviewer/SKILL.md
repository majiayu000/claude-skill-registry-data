---
name: rust-reviewer
description: |
  WHEN: Rust project review, ownership/borrowing, error handling, unsafe code, performance
  WHAT: Ownership patterns + Lifetime analysis + Error handling (Result/Option) + Unsafe audit + Idiomatic Rust
  WHEN NOT: Rust API → rust-api-reviewer, Go → go-reviewer
---

# Rust Reviewer Skill

## Purpose
Reviews Rust code for ownership, lifetimes, error handling, safety, and idiomatic patterns.

## When to Use
- Rust project code review
- Ownership/borrowing review
- Lifetime annotation review
- Unsafe code audit
- Error handling patterns

## Project Detection
- `Cargo.toml` in project root
- `.rs` files
- `src/lib.rs` or `src/main.rs`
- `tests/` directory

## Workflow

### Step 1: Analyze Project
```
**Rust Edition**: 2021
**Type**: Library / Binary
**Dependencies**: Key crates
**Testing**: cargo test
**Linter**: clippy
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full Rust review (recommended)
- Ownership and borrowing
- Lifetimes and references
- Error handling (Result/Option)
- Unsafe code audit
multiSelect: true
```

## Detection Rules

### Ownership & Borrowing
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Unnecessary clone() | Borrow instead | MEDIUM |
| &String parameter | Use &str | MEDIUM |
| Vec ownership transfer | Consider slice | MEDIUM |
| Excessive Rc/Arc | Restructure ownership | MEDIUM |

```rust
// BAD: Unnecessary clone
fn process(data: Vec<String>) {
    for item in data.clone().iter() {  // Clone not needed!
        println!("{}", item);
    }
}

// GOOD: Borrow
fn process(data: &[String]) {
    for item in data {
        println!("{}", item);
    }
}

// BAD: &String parameter
fn greet(name: &String) {
    println!("Hello, {}", name);
}

// GOOD: &str parameter (more flexible)
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// BAD: Taking ownership unnecessarily
fn sum(numbers: Vec<i32>) -> i32 {
    numbers.iter().sum()
}

// GOOD: Borrow slice
fn sum(numbers: &[i32]) -> i32 {
    numbers.iter().sum()
}
```

### Lifetimes
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Missing lifetime annotation | Add explicit lifetime | HIGH |
| 'static overuse | Use specific lifetime | MEDIUM |
| Lifetime in struct | Consider ownership | MEDIUM |
| Complex lifetime bounds | Simplify if possible | LOW |

```rust
// BAD: Missing lifetime
struct Parser {
    input: &str,  // Error: missing lifetime
}

// GOOD: Explicit lifetime
struct Parser<'a> {
    input: &'a str,
}

impl<'a> Parser<'a> {
    fn new(input: &'a str) -> Self {
        Parser { input }
    }

    fn parse(&self) -> Result<Ast<'a>, Error> {
        // ...
    }
}

// BAD: 'static when not needed
fn process(data: &'static str) {
    // Requires static lifetime!
}

// GOOD: Generic lifetime
fn process(data: &str) {
    // Works with any lifetime
}

// Consider: Ownership instead of lifetime
struct Config {
    name: String,  // Owned, no lifetime needed
}
```

### Error Handling
| Check | Recommendation | Severity |
|-------|----------------|----------|
| unwrap() in library | Return Result | HIGH |
| expect() without message | Add descriptive message | MEDIUM |
| panic! for recoverable | Return Err | HIGH |
| No custom error type | Define error enum | MEDIUM |

```rust
// BAD: unwrap in library code
pub fn parse_config(path: &str) -> Config {
    let content = fs::read_to_string(path).unwrap();  // Will panic!
    serde_json::from_str(&content).unwrap()
}

// GOOD: Return Result
pub fn parse_config(path: &str) -> Result<Config, ConfigError> {
    let content = fs::read_to_string(path)
        .map_err(|e| ConfigError::IoError(e))?;
    serde_json::from_str(&content)
        .map_err(|e| ConfigError::ParseError(e))
}

// GOOD: Custom error type
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("failed to read config file: {0}")]
    IoError(#[from] std::io::Error),

    #[error("failed to parse config: {0}")]
    ParseError(#[from] serde_json::Error),

    #[error("missing required field: {0}")]
    MissingField(String),
}

// BAD: expect without message
let value = map.get("key").expect("failed");

// GOOD: Descriptive expect
let value = map.get("key")
    .expect("config must contain 'key' field");
```

### Option Handling
| Check | Recommendation | Severity |
|-------|----------------|----------|
| if let Some + else | Use map_or/unwrap_or | LOW |
| Nested Options | Use and_then/flatten | MEDIUM |
| match for single case | Use if let | LOW |

```rust
// BAD: Verbose Option handling
let result = match value {
    Some(v) => v.to_string(),
    None => "default".to_string(),
};

// GOOD: Using combinators
let result = value
    .map(|v| v.to_string())
    .unwrap_or_else(|| "default".to_string());

// Or even simpler
let result = value.map_or("default".to_string(), |v| v.to_string());

// BAD: Nested Options
let result: Option<Option<i32>> = Some(Some(42));
let value = match result {
    Some(Some(v)) => v,
    _ => 0,
};

// GOOD: Flatten
let value = result.flatten().unwrap_or(0);

// Using and_then for chaining
let value = get_user(id)
    .and_then(|user| user.profile)
    .and_then(|profile| profile.avatar)
    .map(|avatar| avatar.url);
```

### Unsafe Code
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Unnecessary unsafe | Remove if safe alternative | HIGH |
| No safety comment | Document invariants | HIGH |
| Raw pointer dereference | Validate pointer | CRITICAL |
| Transmute usage | Use safe cast if possible | CRITICAL |

```rust
// BAD: Unsafe without documentation
unsafe fn get_value(ptr: *const i32) -> i32 {
    *ptr
}

// GOOD: Documented unsafe
/// Gets the value at the given pointer.
///
/// # Safety
///
/// - `ptr` must be valid and properly aligned
/// - `ptr` must point to initialized memory
/// - The memory must not be mutated while this reference exists
unsafe fn get_value(ptr: *const i32) -> i32 {
    debug_assert!(!ptr.is_null(), "ptr must not be null");
    *ptr
}

// BAD: Transmute for casting
let bytes: [u8; 4] = unsafe { std::mem::transmute(value) };

// GOOD: Safe alternative
let bytes = value.to_ne_bytes();

// Encapsulating unsafe in safe API
pub struct Buffer {
    ptr: *mut u8,
    len: usize,
}

impl Buffer {
    /// Creates a new buffer. Safe because we control allocation.
    pub fn new(size: usize) -> Self {
        let ptr = unsafe { alloc(Layout::array::<u8>(size).unwrap()) };
        Self { ptr, len: size }
    }

    /// Safe accessor - bounds checked
    pub fn get(&self, index: usize) -> Option<u8> {
        if index < self.len {
            // SAFETY: index is bounds-checked above
            Some(unsafe { *self.ptr.add(index) })
        } else {
            None
        }
    }
}
```

### Idiomatic Rust
| Check | Recommendation | Severity |
|-------|----------------|----------|
| C-style loop | Use iterators | LOW |
| Manual index tracking | Use enumerate() | LOW |
| Return in match | Return match expression | LOW |
| Redundant type annotation | Use inference | LOW |

```rust
// BAD: C-style loop
let mut i = 0;
while i < items.len() {
    process(&items[i]);
    i += 1;
}

// GOOD: Iterator
for item in &items {
    process(item);
}

// With index
for (i, item) in items.iter().enumerate() {
    println!("{}: {}", i, item);
}

// BAD: Redundant type
let numbers: Vec<i32> = vec![1, 2, 3];
let sum: i32 = numbers.iter().sum();

// GOOD: Type inference
let numbers = vec![1, 2, 3];
let sum: i32 = numbers.iter().sum();  // Only needed here

// BAD: Return in match arms
fn classify(n: i32) -> &'static str {
    match n {
        0 => { return "zero"; }
        _ if n > 0 => { return "positive"; }
        _ => { return "negative"; }
    }
}

// GOOD: Match as expression
fn classify(n: i32) -> &'static str {
    match n {
        0 => "zero",
        _ if n > 0 => "positive",
        _ => "negative",
    }
}
```

## Response Template
```
## Rust Code Review Results

**Project**: [name]
**Rust Edition**: 2021 | **Clippy**: Enabled

### Ownership & Borrowing
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | parser.rs:45 | Unnecessary clone() |

### Lifetimes
| Status | File | Issue |
|--------|------|-------|
| HIGH | cache.rs:23 | Missing lifetime on struct field |

### Error Handling
| Status | File | Issue |
|--------|------|-------|
| HIGH | lib.rs:67 | unwrap() in public function |

### Unsafe
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | ffi.rs:12 | Unsafe block without safety comment |

### Recommended Actions
1. [ ] Replace clone() with borrowing
2. [ ] Add lifetime annotations to Cache struct
3. [ ] Return Result instead of panicking
4. [ ] Document all unsafe blocks with safety invariants
```

## Best Practices
1. **Ownership**: Borrow when possible, clone when needed
2. **Lifetimes**: Explicit > implicit, owned > referenced
3. **Errors**: thiserror for libs, anyhow for apps
4. **Unsafe**: Minimize, document, encapsulate in safe API
5. **Clippy**: Run with `cargo clippy -- -W clippy::pedantic`

## Integration
- `rust-api-reviewer`: Web framework patterns
- `security-scanner`: Rust security audit
- `perf-analyzer`: Performance profiling
