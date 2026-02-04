---
name: zstd-compression-engineer
description: Expert guide for implementing Zstandard (zstd) compression and decompression. Use when working with zstd library for data compression tasks including simple compression, streaming operations, dictionary-based compression, or when users need help with compression performance optimization, error handling, or choosing the right API for their use case.
---

# Zstd Compression Engineer

Expert guidance for implementing Zstandard (zstd) compression in any programming language.

## Quick Decision Tree

Choose your API based on the use case:

1. **Simple one-off compression** → Use `ZSTD_compress()` / `ZSTD_decompress()`
2. **Large files or unknown sizes** → Use streaming API (`ZSTD_compressStream2()` / `ZSTD_decompressStream()`)
3. **Many small similar files** → Use dictionary compression (`ZSTD_compress_usingCDict()`)
4. **Repeated operations** → Reuse contexts (`ZSTD_compressCCtx()` / `ZSTD_decompressDCtx()`)

## Core Implementation Patterns

### Pattern 1: Simple Compression

```c
// Allocate destination buffer
size_t dstCapacity = ZSTD_compressBound(srcSize);
void* dst = malloc(dstCapacity);

// Compress
size_t compressedSize = ZSTD_compress(dst, dstCapacity, src, srcSize, compressionLevel);

// Always check for errors
if (ZSTD_isError(compressedSize)) {
    fprintf(stderr, "Compression failed: %s\n", ZSTD_getErrorName(compressedSize));
    // Handle error
}
```

**Key points:**
- Use `ZSTD_compressBound()` to calculate required buffer size
- Default compression level is 3 (balance of speed/ratio)
- Levels 1-3: fast, 4-9: balanced, 10-19: high compression, 20-22: ultra (memory intensive)

### Pattern 2: Context Reuse for Multiple Operations

```c
// Create context once
ZSTD_CCtx* cctx = ZSTD_createCCtx();

// Use for multiple compressions
for (each file) {
    size_t result = ZSTD_compressCCtx(cctx, dst, dstCapacity, src, srcSize, level);
    // Process result
}

// Cleanup
ZSTD_freeCCtx(cctx);
```

**Benefits:**
- Reuses allocated memory across operations
- Better performance than creating new contexts
- No impact on compression ratio

### Pattern 3: Streaming for Large Data

See `references/streaming-api.md` for complete streaming implementation guide.

**Use streaming when:**
- Source data doesn't fit in memory
- Decompressed size is unknown
- Processing data incrementally (network streams, pipes)

**Buffer size recommendations:**
- Input: `ZSTD_CStreamInSize()` / `ZSTD_DStreamInSize()`
- Output: `ZSTD_CStreamOutSize()` / `ZSTD_DStreamOutSize()`

### Pattern 4: Dictionary Compression

See `references/dictionary-compression.md` for complete dictionary usage guide.

**Use dictionaries when:**
- Compressing many small similar files (< 100KB each)
- Data has repeated patterns across files
- Working with structured data (JSON, XML, logs)

**Critical rule:** Pre-digest dictionaries with `ZSTD_createCDict()` for repeated use. Loading raw dictionaries repeatedly kills performance.

## Error Handling

**Always check results:**
```c
size_t result = ZSTD_compress(...);
if (ZSTD_isError(result)) {
    const char* errMsg = ZSTD_getErrorName(result);
    // Handle error
}
```

**Context recovery after errors:**
- Contexts may be in undefined state after errors
- Reset before reuse: `ZSTD_CCtx_reset()` or `ZSTD_DCtx_reset()`

**Untrusted data validation:**
- Always validate decompressed sizes from untrusted sources
- Use `ZSTD_getFrameContentSize()` to check size before allocating
- Implement application-specific size limits
- Prefer streaming decompression for untrusted data

## Thread Safety

**Per-thread contexts:**
- Maintain separate `ZSTD_CCtx` per thread
- Never share contexts across threads

**Shared thread pools (optional):**
```c
ZSTD_threadPool* pool = ZSTD_createThreadPool(numThreads);
ZSTD_CCtx_refThreadPool(cctx, pool);
```

## Common Pitfalls

1. **Forgetting to check `ZSTD_compressBound()`** → Buffer overflow
2. **Loading dictionaries repeatedly** → Performance degradation
3. **Not checking `ZSTD_isError()`** → Silent failures
4. **Sharing contexts across threads** → Undefined behavior
5. **Trusting decompressed sizes** → Memory exhaustion attacks

## Performance Tuning

**Compression level selection:**
- Level 1-3: Real-time compression, minimal CPU
- Level 4-9: General purpose (recommended starting point)
- Level 10-19: Offline compression, archival
- Level 20-22: Maximum compression, high memory usage

**Advanced parameters:**
- Window log: Controls memory usage and compression ratio
- Strategy: fast, dfast, greedy, lazy, btopt (automatic selection usually best)
- See `references/api-reference.md` for complete parameter list

## Language-Specific Notes

**C/C++:** Direct library access, use patterns above
**Python:** Use `zstandard` package (python-zstandard)
**Node.js:** Use `@mongodb-js/zstd` or `node-zstd`
**Go:** Use `github.com/klauspost/compress/zstd`
**Rust:** Use `zstd` crate
**Java:** Use `com.github.luben:zstd-jni`

All language bindings follow the same conceptual patterns: simple compression, streaming, dictionary support.

## Reference Documentation

For detailed API specifications:
- **Streaming API guide**: `references/streaming-api.md`
- **Dictionary compression**: `references/dictionary-compression.md`
- **Complete API reference**: `references/api-reference.md`
- **Official docs**: https://facebook.github.io/zstd/doc/api_manual_latest.html

## Implementation Checklist

When implementing zstd compression:
- [ ] Choose correct API (simple/streaming/dictionary)
- [ ] Calculate buffer sizes with `ZSTD_compressBound()`
- [ ] Select appropriate compression level
- [ ] Implement error checking with `ZSTD_isError()`
- [ ] Reuse contexts for multiple operations
- [ ] Handle context reset after errors
- [ ] Validate untrusted data sizes
- [ ] Test with actual data to verify correctness
