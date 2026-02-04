---
name: Rust Performance & Safety Patterns
description: Zero-copy deserialization, async I/O patterns, lifetime management, memory-efficient parsing, and safe handling of unsafe code for SSTable parsing. Use when working with performance optimization, memory efficiency, async/await, borrowing/lifetimes, zero-copy patterns, or memory usage under 128MB target.
---

# Rust Performance & Safety Patterns

This skill provides guidance on Rust patterns for high-performance, memory-efficient SSTable parsing.

## When to Use This Skill

- Implementing zero-copy deserialization
- Managing lifetimes for borrowed data
- Async I/O patterns with tokio
- Memory optimization (<128MB target)
- Safe handling of unsafe code
- Borrow checker issues
- Performance bottlenecks

## Documentation Resources

For latest crate documentation, use Context7 MCP:

### bytes crate (`/tokio-rs/bytes`)
Zero-copy buffer types, Bytes/BytesMut API
```
Ask: "Fetch bytes crate documentation using Context7"
```

### tokio (`/tokio-rs/tokio`)
Async runtime, I/O patterns, task management
```
Ask: "Fetch tokio documentation using Context7"
```

### serde (`/serde-rs/serde`)
Serialization framework patterns
```
Ask: "Fetch serde documentation using Context7"
```

## Zero-Copy Patterns

### Core Principle
Avoid copying data unnecessarily. Use `Bytes` for shared buffer references.

See [zero-copy-patterns.md](zero-copy-patterns.md) for detailed patterns from existing codebase.

### Buffer Sharing with Bytes
```rust
use bytes::Bytes;

// Share buffer without copying
fn parse_partition(buffer: Bytes, offset: usize, len: usize) -> Result<Partition> {
    // Slice creates new Bytes pointing to same underlying buffer
    let partition_data = buffer.slice(offset..offset + len);
    
    // Pass slices to child parsers
    let header = parse_header(partition_data.slice(0..10))?;
    let rows = parse_rows(partition_data.slice(10..))?;
    
    Ok(Partition { header, rows })
}
```

### Avoiding Unnecessary Clones
```rust
// ❌ BAD: Copies data
fn parse_text(data: &[u8]) -> Result<String> {
    let bytes = data.to_vec();  // COPY 1
    String::from_utf8(bytes)    // COPY 2 (if validation needed)
}

// ✅ GOOD: Minimal copying
fn parse_text(data: Bytes) -> Result<String> {
    // Only copy if UTF-8 validation requires it
    let s = std::str::from_utf8(&data)?;
    Ok(s.to_string())  // Single copy only when needed
}

// ✅ BETTER: Keep as Bytes if possible
fn parse_blob(data: Bytes) -> Result<Bytes> {
    // No copy at all
    Ok(data)
}
```

## Lifetime Management

### Borrowing vs Owning
```rust
// Struct with borrowed data (careful with lifetimes)
struct Row<'a> {
    key: &'a [u8],
    values: Vec<&'a [u8]>,
}

// Struct with owned data (simpler, but copies)
struct RowOwned {
    key: Bytes,      // Shared ownership, no copy
    values: Vec<Bytes>,
}
```

### Lifetime Elision
```rust
// Explicit lifetimes
fn parse_row<'a>(data: &'a [u8]) -> Result<Row<'a>> { ... }

// Elided (compiler infers)
fn parse_row(data: &[u8]) -> Result<Row> { ... }
```

### Common Lifetime Patterns
```rust
// Pattern 1: Return borrowed data
fn find_cell<'a>(row: &'a Row, column: &str) -> Option<&'a [u8]> {
    row.cells.get(column).map(|c| c.value.as_ref())
}

// Pattern 2: Return owned data (use Bytes for zero-copy)
fn find_cell_owned(row: &Row, column: &str) -> Option<Bytes> {
    row.cells.get(column).map(|c| c.value.clone())  // Bytes::clone is cheap
}
```

## Async Patterns

### Async File I/O
```rust
use tokio::fs::File;
use tokio::io::AsyncReadExt;

async fn read_sstable(path: &Path) -> Result<Bytes> {
    let mut file = File::open(path).await?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer).await?;
    Ok(Bytes::from(buffer))
}
```

### Async Decompression
```rust
use tokio::task;

async fn decompress_chunk(compressed: Bytes) -> Result<Bytes> {
    // CPU-intensive work in blocking task
    task::spawn_blocking(move || {
        let decompressed = lz4::block::decompress(&compressed, None)?;
        Ok(Bytes::from(decompressed))
    }).await?
}
```

### Async Iteration
```rust
use futures::stream::{Stream, StreamExt};

async fn parse_rows<S>(row_stream: S) -> Result<Vec<Row>>
where
    S: Stream<Item = Result<Bytes>>,
{
    let mut rows = Vec::new();
    tokio::pin!(row_stream);
    
    while let Some(row_data) = row_stream.next().await {
        let row = parse_row(row_data?)?;
        rows.push(row);
    }
    
    Ok(rows)
}
```

## Memory Management

### PRD Target: <128MB
Track memory usage for large SSTables:

```rust
// Don't hold entire SSTable in memory
struct SstableReader {
    file: File,
    index: Vec<IndexEntry>,  // Keep index in memory
    cache: LruCache<u64, Bytes>,  // Cache hot blocks
}

// Read only what's needed
async fn read_partition(&mut self, offset: u64) -> Result<Partition> {
    // Check cache first
    if let Some(block) = self.cache.get(&offset) {
        return parse_partition(block.clone(), 0, block.len());
    }
    
    // Read minimal block
    let block = self.read_block(offset).await?;
    self.cache.put(offset, block.clone());
    parse_partition(block, 0, block.len())
}
```

### Streaming Instead of Buffering
```rust
// ❌ BAD: Buffer everything
async fn process_sstable(path: &Path) -> Result<Vec<Row>> {
    let data = tokio::fs::read(path).await?;  // Load entire file
    parse_all_rows(&data)
}

// ✅ GOOD: Stream rows
async fn process_sstable(path: &Path) -> Result<()> {
    let reader = SstableReader::open(path).await?;
    
    while let Some(row) = reader.next_row().await? {
        process_row(row)?;
        // Row dropped here, memory freed
    }
    
    Ok(())
}
```

## Error Handling

### Result Propagation
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ParseError {
    #[error("Not enough bytes: need {need}, have {have}")]
    NotEnoughBytes { need: usize, have: usize },
    
    #[error("Invalid UTF-8: {0}")]
    InvalidUtf8(#[from] std::str::Utf8Error),
    
    #[error("Compression error: {0}")]
    Compression(String),
}

// Use ? operator for clean propagation
fn parse_row(data: &[u8]) -> Result<Row, ParseError> {
    let flags = data.get(0).ok_or(ParseError::NotEnoughBytes { 
        need: 1, 
        have: data.len() 
    })?;
    
    let text = std::str::from_utf8(&data[1..])?;  // Auto-converts Utf8Error
    
    Ok(Row { flags: *flags, text: text.to_string() })
}
```

## Safe Unsafe Code

### When Unsafe is Necessary
```rust
// Reading fixed-size integers from buffer
fn read_u32_be(data: &[u8]) -> u32 {
    // Safe version (bounds check)
    u32::from_be_bytes([data[0], data[1], data[2], data[3]])
    
    // Unsafe version (skip bounds check if you're certain)
    unsafe {
        u32::from_be_bytes(*(data.as_ptr() as *const [u8; 4]))
    }
}
```

### Safety Documentation
```rust
/// # Safety
/// 
/// `data` must be at least 4 bytes long, and properly aligned.
/// Caller must ensure this invariant.
unsafe fn read_u32_unchecked(data: &[u8]) -> u32 {
    debug_assert!(data.len() >= 4);
    u32::from_be_bytes(*(data.as_ptr() as *const [u8; 4]))
}
```

### Prefer Safe Alternatives
```rust
// ✅ BEST: Safe with slice pattern matching
fn read_u32_safe(data: &[u8]) -> Option<u32> {
    match data {
        [a, b, c, d, ..] => Some(u32::from_be_bytes([*a, *b, *c, *d])),
        _ => None,
    }
}
```

## Performance Profiling

### Cargo Flamegraph
```bash
cargo install flamegraph
cargo flamegraph --bin cqlite -- parse large-file.db
```

### Criterion Benchmarks
```rust
use criterion::{criterion_group, criterion_main, Criterion};

fn parse_row_benchmark(c: &mut Criterion) {
    let data = generate_test_row();
    
    c.bench_function("parse_row", |b| {
        b.iter(|| parse_row(&data))
    });
}

criterion_group!(benches, parse_row_benchmark);
criterion_main!(benches);
```

### Memory Profiling
```bash
cargo install cargo-instruments
cargo instruments -t Allocations --bin cqlite -- parse large-file.db
```

## PRD Alignment

**Supports Milestone M1** (Core Reading Library):
- Zero-copy deserialization
- Memory target: <128MB for large files
- Type-safe parsing

**Supports Milestone M6** (Performance Validation):
- Parse 1GB files in <10 seconds
- Sub-millisecond partition lookups

## Common Patterns from Codebase

See [zero-copy-patterns.md](zero-copy-patterns.md) for patterns extracted from:
- `v5_compressed_legacy.rs` (1997 lines)
- Bytes usage
- Async decompression
- Buffer management

## Anti-Patterns to Avoid

### 1. Unnecessary Allocations
❌ `Vec::new()` then `push` in loop with unknown size
✅ `Vec::with_capacity(known_size)`

### 2. Clone Everything
❌ `.clone()` on every data structure
✅ Use `&` references or `Bytes` for shared ownership

### 3. Blocking in Async
❌ CPU-intensive work in async fn
✅ `tokio::task::spawn_blocking` for CPU work

### 4. Ignoring Capacity
❌ `String::new()` then many `push_str` calls
✅ `String::with_capacity(estimated_size)`

## Next Steps

When optimizing performance:
1. Profile first (don't guess)
2. Use flamegraph to find hotspots
3. Check allocations with Instruments/heaptrack
4. Benchmark changes with Criterion
5. Validate memory usage stays <128MB

## References

- [zero-copy-patterns.md](zero-copy-patterns.md) - Patterns from codebase
- Context7: `/tokio-rs/bytes`, `/tokio-rs/tokio`, `/serde-rs/serde`
- Rust Performance Book: https://nnethercote.github.io/perf-book/

