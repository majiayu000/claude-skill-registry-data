---
name: mithril-cache-agent
description: Build mithril-cache for torch.compile caching. Use when implementing content-addressable storage, cache keys, eviction, or framework hooks.
---

# Mithril Cache Agent

Build compilation caching to reduce torch.compile cold starts from 67s to <1s.

## Status

Read `crates/mithril-cache/STATUS.md` for current progress.

## Reference Documentation

- `cache/SPEC.md` - Full product specification
- `RESEARCH.md` - References (sccache, PyTorch codecache, Triton cache)

## Module Responsibilities

### cas (Content-Addressable Storage)

Store artifacts by content hash:

```rust
pub struct ContentStore {
    root: PathBuf,
    hasher: Blake3Hasher,
}

impl ContentStore {
    pub fn new(root: impl AsRef<Path>) -> Result<Self>;

    /// Store content, return its address (hash)
    pub async fn put(&self, content: &[u8]) -> Result<String>;

    /// Retrieve content by address
    pub async fn get(&self, address: &str) -> Result<Option<Vec<u8>>>;

    /// Check if address exists
    pub async fn exists(&self, address: &str) -> Result<bool>;
}
```

### keys

Cache key generation (machine-independent):

```rust
pub struct CacheKey {
    pub graph_hash: [u8; 32],
    pub inputs: Vec<InputSpec>,
    pub device: DeviceClass,
}

impl CacheKey {
    pub fn to_storage_key(&self) -> String;
}

pub struct InputSpec {
    pub shape: Vec<i64>,
    pub dtype: DType,
}

pub enum DeviceClass {
    CudaAny,
    CudaCompute { major: u8, minor: u8 },
    Cpu,
}
```

### eviction

LRU eviction for local cache:

```rust
pub struct LruCache {
    max_size_bytes: u64,
    entries: LinkedHashMap<String, CacheEntry>,
    current_size: u64,
}

impl LruCache {
    pub fn new(max_size_bytes: u64) -> Self;
    pub fn get(&mut self, key: &str) -> Option<&CacheEntry>;
    pub fn put(&mut self, key: String, entry: CacheEntry);
    fn evict_if_needed(&mut self);
}
```

### hooks

Framework integration via environment variables:

```rust
pub fn init(config: CacheConfig) -> Result<CacheManager> {
    let manager = CacheManager::new(config)?;

    // Intercept via environment variables
    std::env::set_var("TORCHINDUCTOR_CACHE_DIR", manager.inductor_dir());
    std::env::set_var("TRITON_CACHE_DIR", manager.triton_dir());

    Ok(manager)
}
```

**MVP Strategy**: Don't hook internal PyTorch APIs. Just redirect cache directories.

## Target Metrics

| Metric | Target |
|--------|--------|
| Local lookup | <10ms |
| Cold start (cache hit) | <1s |
| Cache hit rate | ≥80% |

## Key Dependencies

```toml
mithril-core = { workspace = true }
blake3 = { workspace = true }
tokio = { workspace = true }
```

## Testing

```bash
cargo test -p mithril-cache
cargo bench -p mithril-cache
```

## Implementation Order

1. Implement `cas` module (content-addressable storage)
2. Implement `keys` module (cache key generation)
3. Implement `eviction` (LRU)
4. Implement `hooks` (env var interception)
5. Integration test with synthetic data
6. Update STATUS.md

## Completion Criteria

- [ ] CAS stores/retrieves artifacts correctly
- [ ] LRU eviction works
- [ ] <10ms local lookup
- [ ] Unit tests pass
- [ ] STATUS.md updated to COMPLETE

## Notes

- **Don't integrate deeply with PyTorch internals** - they're unstable
- Start with env var interception (shallow integration)
- Remote cache (S3/GCS) is post-MVP
