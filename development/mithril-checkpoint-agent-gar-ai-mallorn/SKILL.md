---
name: mithril-checkpoint-agent
description: Build mithril-checkpoint compression for PyTorch models. Use when implementing byte grouping, compression pipeline, or checkpoint I/O.
---

# Mithril Checkpoint Agent

Build checkpoint compression for PyTorch models with 10-20x lossless compression.

## Status

Read `crates/mithril-checkpoint/STATUS.md` for current progress.

## Reference Documentation

- `SPEC.md` - Full product specification
- `checkpoint/SPEC.md` - Detailed implementation spec (if exists)
- `RESEARCH.md` - Papers and prior art (LMC, ZipNN, Check-N-Run)

## Module Responsibilities

### bytegroup

bfloat16 byte grouping for better compression:

```rust
/// Group bf16 bytes: [h0,l0,h1,l1,...] → [h0,h1,...,l0,l1,...]
pub fn byte_group_bf16(data: &[u8]) -> Vec<u8> {
    let n = data.len() / 2;
    let mut grouped = Vec::with_capacity(data.len());
    for i in 0..n { grouped.push(data[i * 2]); }     // high bytes
    for i in 0..n { grouped.push(data[i * 2 + 1]); } // low bytes
    grouped
}

/// Ungroup: [h0,h1,...,l0,l1,...] → [h0,l0,h1,l1,...]
pub fn byte_ungroup_bf16(data: &[u8]) -> Vec<u8>;
```

Why: High bytes (exponent) compress better together. ~20% better ratio.

### pipeline

Compression pipeline combining byte grouping + zstd:

```rust
pub struct CheckpointCompressor {
    compressor: ZstdCompressor,
}

impl CheckpointCompressor {
    pub fn compress(&self, data: &[u8], dtype: DType) -> Result<Vec<u8>> {
        let grouped = match dtype {
            DType::BFloat16 | DType::Float16 => byte_group_bf16(data),
            _ => data.to_vec(),
        };
        self.compressor.compress(&grouped)
    }

    pub fn decompress(&self, data: &[u8], dtype: DType, size: usize) -> Result<Vec<u8>>;
}
```

### formats

Read PyTorch checkpoint formats:

- `state_dict` - PyTorch pickle format
- `safetensors` - HuggingFace format (preferred)

## Target Metrics

| Metric | Target |
|--------|--------|
| Compression ratio | ≥10x (lossless) |
| Throughput | ≥2.5 GiB/s |
| Memory overhead | ≤2x checkpoint size |

## Key Dependencies

```toml
mithril-core = { workspace = true }
zstd = { workspace = true }
rayon = { workspace = true }  # Parallel compression
```

## Test Fixtures

- `fixtures/checkpoints/small_model.bin` - 10MB bf16 test data

## Testing

```bash
cargo test -p mithril-checkpoint
cargo bench -p mithril-checkpoint
```

## Implementation Order

1. Implement `bytegroup` module with tests
2. Implement `pipeline` module
3. Add format readers (safetensors first)
4. Run benchmarks, optimize for throughput
5. Update STATUS.md

## Completion Criteria

- [ ] Compress/decompress roundtrip is bit-exact
- [ ] ≥10x compression on bf16 data
- [ ] ≥2.5 GiB/s throughput
- [ ] Unit tests pass
- [ ] STATUS.md updated to COMPLETE
