---
name: mithril-dedup-agent
description: Build mithril-dedup for ML dataset deduplication. Use when implementing MinHash, LSH, clustering, or document I/O.
---

# Mithril Dedup Agent

Build data deduplication for ML training datasets at 100K+ docs/sec.

## Status

Read `crates/mithril-dedup/STATUS.md` for current progress.

## Reference Documentation

- `dedup/SPEC.md` - Full product specification
- `RESEARCH.md` - Papers (Google 2021 dedup paper, LSHBloom, text-dedup)

## Module Responsibilities

### minhash

MinHash signature generation:

```rust
pub struct MinHasher {
    num_permutations: usize,  // 128 default
    seeds: Vec<u64>,
}

impl MinHasher {
    pub fn new(num_permutations: usize) -> Self;
    pub fn signature(&self, tokens: &HashSet<u64>) -> MinHashSignature;
    pub fn similarity(sig1: &MinHashSignature, sig2: &MinHashSignature) -> f64;
}

pub struct MinHashSignature {
    pub values: Vec<u64>,
}
```

Use `mithril_core::hashing::hash_with_seed()` for hashing.

### lsh

Locality-Sensitive Hashing for candidate pair generation:

```rust
pub struct LshIndex {
    num_bands: usize,
    rows_per_band: usize,
    buckets: Vec<HashMap<u64, Vec<DocId>>>,
}

impl LshIndex {
    /// Create with target similarity threshold
    /// For 0.85 threshold: typically b=20, r=5
    pub fn with_threshold(num_permutations: usize, threshold: f64) -> Self;
    pub fn insert(&mut self, doc_id: DocId, signature: &MinHashSignature);
    pub fn candidates(&self) -> impl Iterator<Item = (DocId, DocId)>;
}
```

### cluster

Union-Find for grouping duplicates:

```rust
pub struct UnionFind {
    parent: Vec<usize>,
    rank: Vec<usize>,
}

impl UnionFind {
    pub fn new(n: usize) -> Self;
    pub fn find(&mut self, x: usize) -> usize;  // with path compression
    pub fn union(&mut self, x: usize, y: usize);  // by rank
    pub fn clusters(&mut self) -> HashMap<usize, Vec<usize>>;
}
```

### io

File I/O for JSONL and Parquet:

```rust
pub fn read_jsonl(path: &Path, text_field: &str) -> Result<Vec<Document>>;
pub fn read_parquet(path: &Path, text_column: &str) -> Result<Vec<Document>>;
pub fn write_jsonl(path: &Path, docs: &[Document]) -> Result<()>;
```

### cli (main.rs)

Command-line interface:

```bash
mithril-dedup input.jsonl -o output.jsonl --field text --threshold 0.85
```

## Target Metrics

| Metric | Target |
|--------|--------|
| Throughput | ≥100K docs/sec |
| Precision | ≥0.95 |
| Recall | ≥0.90 |
| Memory (LSH) | <16GB for 1B docs |

## Key Dependencies

```toml
mithril-core = { workspace = true }
xxhash-rust = { workspace = true }
rayon = { workspace = true }
arrow = { workspace = true }
parquet = { workspace = true }
clap = { workspace = true }
```

## Test Fixtures

- `fixtures/datasets/duplicates.jsonl` - 1000 docs with 30% known duplicates

## Testing

```bash
cargo test -p mithril-dedup
cargo bench -p mithril-dedup
```

## Implementation Order

1. Implement `minhash` module with tests
2. Implement `lsh` module
3. Implement `cluster` (UnionFind)
4. Implement `io` for JSONL
5. Wire up CLI
6. Add Parquet support
7. Run benchmarks
8. Update STATUS.md

## Completion Criteria

- [ ] Detects duplicates with Jaccard ≥0.85
- [ ] ≥100K docs/sec throughput
- [ ] CLI works: `mithril-dedup input.jsonl -o output.jsonl`
- [ ] Unit tests pass
- [ ] STATUS.md updated to COMPLETE
