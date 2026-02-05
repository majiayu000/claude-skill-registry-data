---
name: rust-performance-analyzer
description: Analyzes Rust code for performance bottlenecks, memory inefficiencies, and optimization opportunities. Use when discussing performance, slow code, memory usage, profiling, benchmarks, or optimization.
---

# Rust Performance Analyzer

Expert skill for analyzing and optimizing Rust application performance.

## When to Use

Activate this skill when the user:
- Mentions "slow", "performance", "optimize", "bottleneck"
- Asks about memory usage or allocation patterns
- Wants to profile or benchmark code
- Reports laggy UI or frame drops
- Discusses cache efficiency or data layout

## Analysis Process

### 1. Identify Hot Paths

Look for:
- Frequent allocations (`Vec::new()`, `String::new()` in loops)
- Unnecessary cloning (`.clone()` where borrow would work)
- Hash map lookups in tight loops
- Box/Arc indirection overhead

### 2. Memory Layout Analysis

Check:
- Struct field ordering (largest first for alignment)
- Use of `#[repr(C)]` where needed
- Option<T> niche optimization usage
- Cache line friendliness

### 3. Concurrency Patterns

Evaluate:
- Lock contention (`Mutex`, `RwLock` usage)
- parking_lot vs std sync primitives
- Atomic operations appropriateness
- Send/Sync bounds efficiency

### 4. FLUI-Specific Patterns

Focus on:
- Signal update frequency
- Rebuild triggering patterns
- Layout phase efficiency
- Paint layer caching

## Optimization Techniques

### Allocation Reduction
```rust
// Bad: Allocates on every call
fn process(items: &[Item]) -> Vec<ProcessedItem> {
    items.iter().map(|i| process_one(i)).collect()
}

// Good: Reuse buffer
fn process_into(items: &[Item], buffer: &mut Vec<ProcessedItem>) {
    buffer.clear();
    buffer.extend(items.iter().map(|i| process_one(i)));
}
```

### Clone Elimination
```rust
// Bad: Unnecessary clone
let data = self.data.clone();
process(&data);

// Good: Borrow directly
process(&self.data);
```

### Interior Mutability
```rust
// Use RefCell/Cell for single-threaded
// Use parking_lot::{Mutex, RwLock} for multi-threaded
// Use atomics for simple counters/flags
```

## Profiling Commands

```bash
# Build with debug symbols
cargo build --release

# CPU profiling (requires cargo-flamegraph)
cargo flamegraph --example <name>

# Memory profiling
RUSTFLAGS="-Z sanitizer=address" cargo +nightly run --example <name>

# Benchmarking
cargo bench
```

## Output Format

Provide:
1. **Identified Issues**: List of performance problems found
2. **Impact Assessment**: Severity (High/Medium/Low)
3. **Optimization Suggestions**: Specific code changes
4. **Metrics**: Before/after estimates where possible
