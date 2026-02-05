---
name: Cassandra SSTable Format Parsing
description: Guide parsing of Cassandra 5.0+ SSTable components (Data.db, Index.db, Statistics.db, Summary.db, TOC) with compression support (LZ4, Snappy, Deflate). Use when working with SSTable files, binary format parsing, hex dumps, compression issues, offset calculations, BTI index, partition layout, or debugging parsing errors.
allowed-tools: Read, Grep, Glob
---

# Cassandra SSTable Format Parsing

This skill helps with parsing and understanding Cassandra 5.0+ SSTable file formats.

## When to Use This Skill

- Parsing Data.db, Index.db, Statistics.db files
- Debugging binary format mismatches
- Analyzing hex dumps of SSTable data
- Working with compression (LZ4, Snappy, Deflate)
- Investigating offset calculation errors
- Understanding BTI (Big Table Index) format
- Validating partition boundaries

## Key SSTable Components

### Data.db
Contains the actual row data with:
- Partition headers
- Row data (clustering + cells)
- Compression blocks
- Checksums

### Index.db
Contains partition index entries with:
- BTI (Big Table Index) format in Cassandra 5.0+
- Partition key → file offset mapping
- Promoted index entries

### Statistics.db
Contains serialization metadata:
- Encoding stats (min/max timestamps, TTLs)
- Column definitions
- Schema information
- Compression parameters

### Summary.db
Contains sampling of index entries for faster lookups

## Format References

**Primary Source of Truth**: `docs/sstables-definitive-guide/`

Key chapters:
- **Ch.5**: Data.db Format - Row layout, flags, V5CompressedLegacy
- **Ch.6**: Index.db and Summary.db - Partition lookups
- **Ch.9**: CompressionInfo.db - Compression metadata, chunking
- **Ch.17**: BTI Formats - Trie-based indexes
- **Appendix B**: Encoding Cheat Sheet - VInt, cell flags
- **Appendix F**: Known Limitations - What doesn't work yet

## Common Debugging Techniques

### Hex Dump Analysis
When debugging parsing errors:

1. **Extract hex at specific offset**:
   ```bash
   hexdump -C Data.db -s <offset> -n 64
   ```

2. **Compare with expected format**:
   - Check magic bytes (if applicable)
   - Verify VInt encoding
   - Validate flag bytes

3. **Look for patterns**:
   - Repeated byte sequences may indicate arrays/collections
   - All zeros may indicate padding
   - Non-zero high bytes suggest multi-byte integers

### Offset Validation
Track byte consumption at each parsing stage:
- Clustering prefix (may be 0 bytes)
- Row sizes (2 VInts)
- Liveness info (conditional)
- Deletion info (conditional)
- Column bitmap (conditional)
- Cell data

### Zero-Copy Considerations
When implementing parsers:
- Use `Bytes` crate for buffer sharing
- Avoid copying large cell values
- Keep references to original buffer
- Use byte slices not owned Vecs

## Integration with Rust Code

Current implementation in `cqlite-core/src/storage/sstable/reader/parsing/`:
- `v5_compressed_legacy.rs` - Main V5 format parser (1997 lines)
- Uses zero-copy patterns with `Bytes`
- Handles compression transparently

## PRD Alignment

**Supports Milestone M1** (Core Reading Library):
- 100% Cassandra 5 SSTable format support
- All compression formats (LZ4, Snappy, Deflate)
- Zero-copy deserialization
- Memory target: <128MB for large files

## Quick Reference

### Flag Bytes (Row)
- `0x01`: HAS_IS_MARKER
- `0x02`: HAS_ALL_COLUMNS (inverted - 0x20 means all present)
- `0x04`: HAS_TIMESTAMP
- `0x08`: HAS_TTL
- `0x10`: HAS_DELETION
- `0x20`: HAS_ALL_COLUMNS (flag set = all columns present)
- `0x40`: IS_STATIC
- `0x80`: EXTENSION_FLAG

### VInt Encoding
Variable-length integer encoding:
- First byte indicates length
- Subsequent bytes contain value
- Used for row sizes, timestamps, offsets

## Next Steps

When parser encounters issues:
1. Log byte offsets at each stage
2. Compare against Java source (UnfilteredSerializer.java)
3. Validate against sstabledump output
4. Check compression block boundaries
5. Verify delta encoding calculations

