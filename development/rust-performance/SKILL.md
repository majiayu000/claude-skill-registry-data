---
name: rust-performance
description: Rust performance optimization. Use when optimizing code, reducing allocations, improving cache locality, profiling, or benchmarking.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Rust Performance Optimization

## Profiling First

**Never optimize without measuring.** Profile first, then optimize the actual bottlenecks.

### Profiling Tools

```bash
# CPU profiling with flamegraph
cargo install flamegraph
cargo flamegraph --bin nebula -- <args>

# Memory profiling
cargo install cargo-bloat
cargo bloat --release --crates

# DHAT for heap profiling
cargo install cargo-valgrind
cargo valgrind --bin nebula

# Benchmarking
cargo bench -p <crate>
```

### Criterion Benchmarks

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn benchmark_function(c: &mut Criterion) {
    c.bench_function("function_name", |b| {
        b.iter(|| {
            black_box(function_to_benchmark(black_box(input)))
        })
    });
}

criterion_group!(benches, benchmark_function);
criterion_main!(benches);
```

## Memory Allocation

### Avoid Unnecessary Allocations

```rust
// BAD - allocates on every call
fn process(items: Vec<Item>) -> Vec<Result> {
    items.into_iter().map(|i| transform(i)).collect()
}

// GOOD - reuse allocation
fn process(items: &[Item], results: &mut Vec<Result>) {
    results.clear();
    results.extend(items.iter().map(transform));
}

// GOOD - preallocate
fn process(items: &[Item]) -> Vec<Result> {
    let mut results = Vec::with_capacity(items.len());
    results.extend(items.iter().map(transform));
    results
}
```

### Use Stack When Possible

```rust
// BAD - heap allocation for small data
let data: Box<[u8; 32]> = Box::new([0u8; 32]);

// GOOD - stack allocation
let data: [u8; 32] = [0u8; 32];

// For variable-size small data, use SmallVec
use smallvec::SmallVec;
let items: SmallVec<[Item; 8]> = SmallVec::new();
```

### String Optimization

```rust
// BAD - multiple allocations
let result = format!("{}-{}-{}", a, b, c);

// GOOD - single allocation with capacity hint
let mut result = String::with_capacity(a.len() + b.len() + c.len() + 2);
result.push_str(a);
result.push('-');
result.push_str(b);
result.push('-');
result.push_str(c);

// GOOD - use write! macro
use std::fmt::Write;
let mut result = String::with_capacity(64);
write!(&mut result, "{}-{}-{}", a, b, c).unwrap();
```

### Cow for Conditional Ownership

```rust
use std::borrow::Cow;

fn process_name(name: &str) -> Cow<'_, str> {
    if name.contains(' ') {
        Cow::Owned(name.replace(' ', "_"))
    } else {
        Cow::Borrowed(name)  // No allocation
    }
}
```

## Data Structures

### Choose the Right Collection

```rust
// HashMap vs BTreeMap
// - HashMap: O(1) average, unordered
// - BTreeMap: O(log n), ordered, cache-friendly for iteration

// Vec vs VecDeque
// - Vec: fast push/pop at end
// - VecDeque: fast push/pop at both ends

// HashSet vs BTreeSet
// Similar trade-offs to Map variants

// For small sets, Vec might be faster due to cache locality
const SMALL_THRESHOLD: usize = 16;
if items.len() < SMALL_THRESHOLD {
    // Linear search in Vec is faster
    items.iter().find(|x| **x == target)
} else {
    // Use HashSet for larger collections
    set.contains(&target)
}
```

### Avoid Clone When Possible

```rust
// BAD - unnecessary clone
fn process(data: &Data) {
    let owned = data.clone();
    use_data(&owned);
}

// GOOD - borrow
fn process(data: &Data) {
    use_data(data);
}

// When clone is needed, use Arc for shared ownership
use std::sync::Arc;
let shared = Arc::new(expensive_data);
let clone1 = Arc::clone(&shared);  // Cheap reference count increment
```

## Iteration

### Prefer Iterators Over Indexing

```rust
// BAD - bounds checking on each access
for i in 0..items.len() {
    process(&items[i]);
}

// GOOD - iterator, no bounds checking
for item in &items {
    process(item);
}

// GOOD - parallel iteration
use rayon::prelude::*;
items.par_iter().for_each(|item| process(item));
```

### Chain Operations

```rust
// BAD - multiple passes and allocations
let filtered: Vec<_> = items.iter().filter(|x| x.valid).collect();
let mapped: Vec<_> = filtered.iter().map(|x| x.value).collect();
let sum: i32 = mapped.iter().sum();

// GOOD - single pass, no intermediate allocations
let sum: i32 = items.iter()
    .filter(|x| x.valid)
    .map(|x| x.value)
    .sum();
```

## Numeric Helpers (Rust 1.85+)

```rust
// midpoint() - avoids overflow, useful for binary search
let a: u32 = 10;
let b: u32 = 20;
let mid = a.midpoint(b);  // 15, no overflow risk

// Works with floats too
let x: f64 = 1.0;
let y: f64 = 3.0;
let mid = x.midpoint(y);  // 2.0

// Binary search example
fn binary_search(arr: &[i32], target: i32) -> Option<usize> {
    let mut low = 0usize;
    let mut high = arr.len();
    
    while low < high {
        // Use midpoint to avoid overflow on large indices
        let mid = low.midpoint(high);
        match arr[mid].cmp(&target) {
            std::cmp::Ordering::Less => low = mid + 1,
            std::cmp::Ordering::Greater => high = mid,
            std::cmp::Ordering::Equal => return Some(mid),
        }
    }
    None
}
```

## Inlining

```rust
// For small, hot functions
#[inline]
fn small_hot_function(x: i32) -> i32 {
    x * 2
}

// For functions that should always be inlined
#[inline(always)]
fn trivial_getter(&self) -> i32 {
    self.value
}

// Let compiler decide (default)
fn normal_function(x: i32) -> i32 {
    // Complex logic
}
```

## SIMD and Vectorization

```rust
// Help the compiler vectorize
fn sum_array(arr: &[f32]) -> f32 {
    arr.iter().sum()  // Compiler can auto-vectorize
}

// Explicit SIMD with portable-simd (NIGHTLY ONLY - not for Nebula)
// Nebula uses stable Rust (MSRV 1.90), so prefer auto-vectorization above
// or use stable crates like `wide` for explicit SIMD
#![feature(portable_simd)]
use std::simd::*;

fn sum_simd(arr: &[f32]) -> f32 {
    let chunks = arr.chunks_exact(4);
    let remainder = chunks.remainder();
    
    let sum = chunks.fold(f32x4::splat(0.0), |acc, chunk| {
        acc + f32x4::from_slice(chunk)
    });
    
    sum.reduce_sum() + remainder.iter().sum::<f32>()
}
```

## Compile-Time Optimization

### Const Evaluation

```rust
// Compute at compile time
const TABLE: [u32; 256] = {
    let mut table = [0u32; 256];
    let mut i = 0;
    while i < 256 {
        table[i] = compute_value(i as u32);
        i += 1;
    }
    table
};
```

### LTO and Codegen Options

In `Cargo.toml`:
```toml
[profile.release]
lto = "thin"           # Link-time optimization
codegen-units = 1      # Better optimization, slower compile
panic = "abort"        # Smaller binary, no unwinding
```

## Verification Commands

```bash
# Build in release mode
cargo build --release

# Benchmark
cargo bench -p <crate>

# Profile-guided optimization
RUSTFLAGS="-Cprofile-generate=/tmp/pgo" cargo build --release
# Run representative workload
RUSTFLAGS="-Cprofile-use=/tmp/pgo" cargo build --release

# Check binary size
cargo bloat --release --crates
cargo bloat --release -n 20

# Assembly output
cargo rustc --release -- --emit asm
```

## Nebula-Specific Performance

- Use connection pooling for database access
- Batch operations where possible
- Cache computed values with memoization
- Use async for I/O-bound operations
- Consider object pools for frequently allocated types
