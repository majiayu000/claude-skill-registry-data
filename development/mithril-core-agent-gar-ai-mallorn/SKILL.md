---
name: mithril-core-agent
description: Build mithril-core shared infrastructure. Use when implementing storage, compression, hashing, or common types for the Mithril ML toolkit.
---

# Mithril Core Agent

Build the shared infrastructure layer for Mithril ML tools.

## Status

Read `crates/mithril-core/STATUS.md` for current progress.

## Reference Documentation

- `INTERFACES.md` - Core API contracts
- `ARCHITECTURE.md` - System design

## Module Responsibilities

### storage (StorageBackend)

```rust
pub trait StorageBackend: Send + Sync {
    async fn get(&self, key: &str) -> Result<Bytes>;
    async fn put(&self, key: &str, data: Bytes) -> Result<()>;
    async fn delete(&self, key: &str) -> Result<()>;
    async fn exists(&self, key: &str) -> Result<bool>;
    async fn list(&self, prefix: &str) -> Result<Vec<String>>;
}
```

Implementations: `LocalStorage`, future: S3Storage, GcsStorage

### compression (Compressor)

```rust
pub trait Compressor: Send + Sync {
    fn compress(&self, data: &[u8]) -> Result<Vec<u8>>;
    fn decompress(&self, data: &[u8]) -> Result<Vec<u8>>;
}
```

Implementations: `ZstdCompressor`, `Lz4Compressor`

### hashing (HashFunction)

```rust
pub trait HashFunction: Send + Sync {
    fn hash(&self, data: &[u8]) -> Vec<u8>;
    fn hash_hex(&self, data: &[u8]) -> String;
    fn hash_u64(&self, data: &[u8]) -> u64;
}
```

Implementations: `XxHash3`, `Blake3Hasher`

### types

- `DType` - Tensor data types (Float32, BFloat16, etc.)
- `TensorMeta` - Tensor metadata (name, shape, dtype, offset, size)

### error

- `MithrilError` - Central error type with variants for I/O, compression, storage, etc.
- `Result<T>` - Type alias for `std::result::Result<T, MithrilError>`

## Key Dependencies

```toml
tokio = { version = "1", features = ["full"] }
bytes = "1"
zstd = "0.13"
lz4_flex = "0.11"
xxhash-rust = { version = "0.8", features = ["xxh3"] }
blake3 = "1"
thiserror = "1"
```

## Testing

```bash
cargo test -p mithril-core
```

## Completion Criteria

- [ ] All trait implementations complete
- [ ] Unit tests for each module
- [ ] No clippy warnings
- [ ] STATUS.md updated to COMPLETE
