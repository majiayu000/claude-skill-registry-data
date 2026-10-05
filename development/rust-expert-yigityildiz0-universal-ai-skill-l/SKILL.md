---
name: rust-expert
description: Deep Rust expertise for systems programming with ownership, borrowing, and lifetimes. Use when writing Rust code, understanding ownership errors.
---

# Rust Expert

Specialized expertise in Rust programming, providing deep guidance on ownership and borrowing, lifetime annotations, error handling patterns, async programming, and idiomatic Rust development.

## When to Use This Skill

Use this skill for:

- Understanding ownership and borrowing errors
- Writing idiomatic Rust code
- Implementing traits and generics
- Async/await programming
- FFI and unsafe Rust
- Performance optimization
- Memory safety patterns

**Trigger phrases**: "rust", "ownership", "borrowing", "lifetime", "borrow checker", "cargo", "trait", "impl"

## What This Skill Does

Provides Rust expertise including:

- **Ownership System**: Ownership, borrowing, and lifetime management
- **Type System**: Traits, generics, associated types
- **Error Handling**: Result, Option, and error propagation
- **Concurrency**: Async/await, threads, channels
- **Performance**: Zero-cost abstractions, optimization
- **Safety**: Unsafe Rust guidelines, FFI

## Instructions

### Step 1: Understand Rust's Ownership Model

**Ownership Rules**:

1. Each value has exactly one owner
2. When the owner goes out of scope, the value is dropped
3. Values can be moved or borrowed

**Ownership Examples**:

```rust
// MOVE - ownership transfers
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;  // s1 is moved to s2
    // println!("{}", s1);  // ERROR: s1 no longer valid
    println!("{}", s2);     // OK: s2 owns the string
}

// COPY - types that implement Copy are duplicated
fn main() {
    let x = 5;
    let y = x;  // x is copied, not moved
    println!("{} {}", x, y);  // Both valid
}

// CLONE - explicit deep copy
fn main() {
    let s1 = String::from("hello");
    let s2 = s1.clone();  // Explicit deep copy
    println!("{} {}", s1, s2);  // Both valid
}
```

### Step 2: Master Borrowing and References

**Borrowing Rules**:

1. You can have either ONE mutable reference OR any number of immutable references
2. References must always be valid (no dangling references)

```rust
// Immutable borrowing - multiple allowed
fn main() {
    let s = String::from("hello");
    let r1 = &s;     // OK
    let r2 = &s;     // OK - multiple immutable refs allowed
    println!("{} {}", r1, r2);
}

// Mutable borrowing - only one allowed
fn main() {
    let mut s = String::from("hello");
    let r1 = &mut s;  // OK
    // let r2 = &mut s;  // ERROR: cannot borrow as mutable twice
    r1.push_str(" world");
    println!("{}", r1);
}

// Cannot mix mutable and immutable
fn main() {
    let mut s = String::from("hello");
    let r1 = &s;      // Immutable borrow
    // let r2 = &mut s;  // ERROR: cannot borrow as mutable
    println!("{}", r1);
    // After last use of r1, we can borrow mutably (NLL)
    let r2 = &mut s;  // OK due to Non-Lexical Lifetimes
    r2.push_str(" world");
}
```

### Step 3: Work with Lifetimes

**Lifetime Annotations**:

```rust
// Lifetime tells compiler how long references are valid
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with references needs lifetime annotations
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    // Method that returns reference to self doesn't need annotation
    fn level(&self) -> i32 {
        3
    }

    // Method returning reference needs to specify lifetime
    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention please: {}", announcement);
        self.part  // Lifetime 'a is inferred
    }
}
```

**Lifetime Elision Rules**:

```rust
// Rule 1: Each input reference gets its own lifetime
fn foo(x: &str) -> &str  // Becomes: fn foo<'a>(x: &'a str) -> &'a str

// Rule 2: If one input lifetime, output gets same lifetime
fn first_word(s: &str) -> &str  // Works without annotation

// Rule 3: If &self, output gets lifetime of self
impl MyStruct {
    fn get_name(&self) -> &str { &self.name }  // Works
}
```

### Step 4: Implement Error Handling

**Result and Option Patterns**:

```rust
use std::fs::File;
use std::io::{self, Read};

// Using Result for fallible operations
fn read_file_contents(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;  // ? propagates errors
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Custom error types
#[derive(Debug)]
enum AppError {
    IoError(io::Error),
    ParseError(String),
    NotFound,
}

impl From<io::Error> for AppError {
    fn from(error: io::Error) -> Self {
        AppError::IoError(error)
    }
}

// Using thiserror crate (recommended)
use thiserror::Error;

#[derive(Error, Debug)]
enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] io::Error),

    #[error("Parse error: {message}")]
    Parse { message: String },

    #[error("Not found: {0}")]
    NotFound(String),
}

// Option for optional values
fn find_user(id: u64) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// Combining Option and Result
fn process_user(id: u64) -> Result<String, AppError> {
    let user = find_user(id).ok_or(AppError::NotFound(format!("User {}", id)))?;
    Ok(user.name)
}
```

### Step 5: Write Async Rust

**Async/Await Patterns**:

```rust
use tokio;

// Basic async function
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

// Running async code
#[tokio::main]
async fn main() {
    let result = fetch_data("https://api.example.com").await;
    match result {
        Ok(data) => println!("Data: {}", data),
        Err(e) => eprintln!("Error: {}", e),
    }
}

// Concurrent execution
async fn fetch_multiple() -> Vec<String> {
    let urls = vec![
        "https://api.example.com/1",
        "https://api.example.com/2",
        "https://api.example.com/3",
    ];

    // Run all requests concurrently
    let futures: Vec<_> = urls.iter().map(|url| fetch_data(url)).collect();
    let results = futures::future::join_all(futures).await;

    results.into_iter().filter_map(|r| r.ok()).collect()
}

// Spawning tasks
async fn background_task() {
    tokio::spawn(async {
        // This runs in the background
        loop {
            tokio::time::sleep(Duration::from_secs(60)).await;
            cleanup_old_data().await;
        }
    });
}
```

### Step 6: Implement Traits and Generics

**Trait Patterns**:

```rust
// Defining traits
trait Summary {
    fn summarize(&self) -> String;

    // Default implementation
    fn summarize_author(&self) -> String {
        String::from("(Anonymous)")
    }
}

// Implementing traits
struct Article {
    title: String,
    author: String,
    content: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{}, by {}", self.title, self.author)
    }

    fn summarize_author(&self) -> String {
        format!("@{}", self.author)
    }
}

// Trait bounds
fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

// Multiple trait bounds
fn notify<T: Summary + Display>(item: &T) { ... }

// Where clause for complex bounds
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{ ... }

// Associated types
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}

impl Iterator for Counter {
    type Item = u32;
    fn next(&mut self) -> Option<Self::Item> {
        // ...
    }
}
```

### Step 7: Write Safe Unsafe Code

**Unsafe Rust Guidelines**:

```rust
// When to use unsafe
// 1. Dereferencing raw pointers
// 2. Calling unsafe functions
// 3. Accessing mutable statics
// 4. Implementing unsafe traits
// 5. Accessing union fields

// Raw pointer example
fn raw_pointer_example() {
    let mut num = 5;
    let r1 = &num as *const i32;      // Immutable raw pointer
    let r2 = &mut num as *mut i32;    // Mutable raw pointer

    unsafe {
        println!("r1: {}", *r1);
        *r2 = 10;
        println!("r2: {}", *r2);
    }
}

// Safe abstraction over unsafe code
fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = values.len();
    let ptr = values.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (
            std::slice::from_raw_parts_mut(ptr, mid),
            std::slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}

// FFI example
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        println!("Absolute value: {}", abs(-3));
    }
}
```

**Unsafe Best Practices**:

| Do | Don't |
|----|-------|
| Minimize unsafe blocks | Put entire functions in unsafe |
| Document safety invariants | Assume caller handles safety |
| Use safe abstractions | Expose raw unsafe APIs |
| Test thoroughly | Skip testing unsafe code |
| Review carefully | Blindly trust unsafe code |

## Best Practices

- **Embrace ownership** - Don't fight the borrow checker
- **Clone sparingly** - Understand the performance cost
- **Use iterators** - More idiomatic than indexing
- **Prefer &str over String** - When you don't need ownership
- **Handle all Results** - Don't use unwrap() in production
- **Use clippy** - Catches common mistakes
- **Minimize unsafe** - Keep it small and documented
- **Write tests** - Especially for unsafe code

## Common Patterns

### Pattern 1: Builder Pattern

```rust
#[derive(Default)]
struct RequestBuilder {
    url: String,
    method: String,
    headers: Vec<(String, String)>,
    body: Option<String>,
}

impl RequestBuilder {
    fn new() -> Self {
        Self::default()
    }

    fn url(mut self, url: impl Into<String>) -> Self {
        self.url = url.into();
        self
    }

    fn method(mut self, method: impl Into<String>) -> Self {
        self.method = method.into();
        self
    }

    fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.push((key.into(), value.into()));
        self
    }

    fn body(mut self, body: impl Into<String>) -> Self {
        self.body = Some(body.into());
        self
    }

    fn build(self) -> Request {
        Request {
            url: self.url,
            method: self.method,
            headers: self.headers,
            body: self.body,
        }
    }
}

// Usage
let request = RequestBuilder::new()
    .url("https://api.example.com")
    .method("POST")
    .header("Content-Type", "application/json")
    .body(r#"{"key": "value"}"#)
    .build();
```

### Pattern 2: Type State Pattern

```rust
// Compile-time state machine
struct Locked;
struct Unlocked;

struct Door<State> {
    _state: std::marker::PhantomData<State>,
}

impl Door<Locked> {
    fn unlock(self) -> Door<Unlocked> {
        Door { _state: std::marker::PhantomData }
    }
}

impl Door<Unlocked> {
    fn lock(self) -> Door<Locked> {
        Door { _state: std::marker::PhantomData }
    }

    fn open(&self) {
        println!("Door is open");
    }
}

// Compile-time enforcement
let door: Door<Locked> = Door { _state: std::marker::PhantomData };
// door.open();  // ERROR: no method `open` for Door<Locked>
let door = door.unlock();
door.open();  // OK
```

## Quality Checklist

- [ ] No unwrap() in production code
- [ ] All Results handled properly
- [ ] Clippy warnings addressed
- [ ] Unsafe code minimized and documented
- [ ] Lifetimes explicit where needed
- [ ] Tests cover edge cases
- [ ] Documentation includes examples
- [ ] Cargo fmt applied

## Related Skills

- `performance-testing` - Benchmarking Rust code
- `security-review` - Unsafe code review
- `cicd-architect` - Rust CI/CD pipelines
- `code-quality` - Rust code standards

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: The Rust Book, awesome-claude-code-subagents patterns


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
