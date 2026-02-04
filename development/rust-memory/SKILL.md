---
name: rust-memory
description: Minimize allocations and cloning using references, Cow, and smart pointers. Use when optimizing hot paths or memory-constrained code.
---

# Memory Efficiency

Patterns to minimize allocations and copies in Rust.

## Avoid Unnecessary Cloning

```rust
// BAD: Cloning when not needed
fn process(data: Vec<String>) -> Vec<String> {
    data.clone().iter().map(|s| s.to_uppercase()).collect()
}

// GOOD: Take ownership or borrow
fn process(data: Vec<String>) -> Vec<String> {
    data.into_iter().map(|s| s.to_uppercase()).collect()
}

// GOOD: Return iterator for lazy evaluation
fn process(data: &[String]) -> impl Iterator<Item = String> + '_ {
    data.iter().map(|s| s.to_uppercase())
}
```

## Prefer &str over String

```rust
// BAD: Requires allocation
fn greet(name: String) {
    println!("Hello, {}!", name);
}

// GOOD: Accepts any string-like type
fn greet(name: &str) {
    println!("Hello, {}!", name);
}

// BEST: Generic for flexibility
fn greet(name: impl AsRef<str>) {
    println!("Hello, {}!", name.as_ref());
}
```

## Pre-allocate Collections

```rust
// BAD: Multiple reallocations as vector grows
let mut v = Vec::new();
for i in 0..1000 {
    v.push(i);
}

// GOOD: Single allocation
let mut v = Vec::with_capacity(1000);
for i in 0..1000 {
    v.push(i);
}

// Also works for String and HashMap
let mut s = String::with_capacity(4000);
let mut map = HashMap::with_capacity(100);
```

## Copy-on-Write (Cow)

```rust
use std::borrow::Cow;

// Return borrowed if no modification needed, owned if modified
fn normalize_path(path: &str) -> Cow<'_, str> {
    if path.contains("//") {
        Cow::Owned(path.replace("//", "/"))
    } else {
        Cow::Borrowed(path)
    }
}

// Usage - no allocation if already normalized
let normalized = normalize_path("/home/user");  // Borrowed
let fixed = normalize_path("/home//user");      // Owned

// Cow in structs
struct Config<'a> {
    name: Cow<'a, str>,
}

impl<'a> Config<'a> {
    fn new(name: &'a str) -> Self {
        Self { name: Cow::Borrowed(name) }
    }

    fn with_prefix(mut self, prefix: &str) -> Self {
        self.name = Cow::Owned(format!("{}{}", prefix, self.name));
        self
    }
}
```

## Smart Pointers

```rust
use std::sync::Arc;
use std::rc::Rc;

// Arc - Shared ownership across threads (atomic reference counting)
let data = Arc::new(expensive_data);
let data_clone = Arc::clone(&data);  // Cheap clone, shares data

// Rc - Single-threaded shared ownership
let data = Rc::new(expensive_data);
let data_clone = Rc::clone(&data);

// Box - Heap allocation for large data or recursive types
let large_data = Box::new([0u8; 1_000_000]);

// Arc::clone is explicit about what it does
// Prefer Arc::clone(&x) over x.clone() for clarity
```

## Zero-Copy with Bytes

```rust
use bytes::Bytes;

// Bytes: Reference-counted, immutable bytes
let data = Bytes::from(vec![0u8; 1024]);
let slice = data.slice(0..512);  // No copy, shares underlying buffer

// BytesMut for building buffers
use bytes::BytesMut;

let mut buf = BytesMut::with_capacity(1024);
buf.extend_from_slice(b"hello");
buf.extend_from_slice(b" world");
let frozen = buf.freeze();  // Convert to immutable Bytes
```

## SmallVec for Small Collections

```rust
use smallvec::SmallVec;

// Stack-allocated if <= 8 items, heap otherwise
let mut results: SmallVec<[Result; 8]> = SmallVec::new();
results.push(Ok(1));
results.push(Ok(2));
// No heap allocation for common case
```

## Avoid Intermediate Collections

```rust
// BAD: Creates intermediate Vec
let sum: i32 = data
    .iter()
    .filter(|&&x| x > 2)
    .collect::<Vec<_>>()  // Unnecessary allocation
    .iter()
    .map(|&&x| x * 2)
    .sum();

// GOOD: Chain iterators, single pass
let sum: i32 = data
    .iter()
    .filter(|&&x| x > 2)
    .map(|&x| x * 2)
    .sum();
```

## String Building

```rust
// BAD: Multiple allocations
let s = String::new() + "hello" + " " + "world";

// GOOD: Pre-allocate and push
let mut s = String::with_capacity(11);
s.push_str("hello");
s.push(' ');
s.push_str("world");

// GOOD: Use format! for clarity (single allocation)
let s = format!("hello {} world", name);

// BEST for loops: Join
let parts = vec!["hello", "world"];
let s = parts.join(" ");
```

## Take and Replace

```rust
// Extract value without cloning
struct Container {
    data: Option<Vec<u8>>,
}

impl Container {
    fn take_data(&mut self) -> Option<Vec<u8>> {
        self.data.take()  // Replaces with None, returns original
    }
}

// Replace and get old value
let mut value = 5;
let old = std::mem::replace(&mut value, 10);
assert_eq!(old, 5);
assert_eq!(value, 10);
```

## Guidelines

- Use `&str` instead of `String` for parameters
- Pre-allocate with `with_capacity()` when size is known
- Use `Cow` for "maybe modified" returns
- Prefer `Arc::clone(&x)` over `x.clone()` for clarity
- Use `Bytes` for zero-copy buffer sharing
- Chain iterators instead of collecting intermediates
- Use `take()` and `replace()` to avoid cloning

## Examples

See `hercules-local-algo/src/pipeline/` for memory-efficient patterns.
