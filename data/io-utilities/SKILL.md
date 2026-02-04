---
name: 'io-utilities'
description: 'Guide for using IO utilities in speedy_utils, including fast JSONL reading, multi-format loading, and file serialization.'
---

# IO Utilities Guide

This skill provides comprehensive guidance for using the IO utilities in `speedy_utils`.

## When to Use This Skill

Use this skill when you need to:
- Read and write data in various formats (JSON, JSONL, Pickle, CSV, TXT).
- Efficiently process large JSONL files with streaming and multi-threading.
- Automatically handle file compression (gzip, bz2, xz, zstd).
- Load data based on file extension automatically.
- Serialize Pydantic models and other objects easily.

## Prerequisites

- `speedy_utils` installed.
- Optional dependencies for specific features:
    - `orjson`: For faster JSON parsing.
    - `zstandard`: For `.zst` file support.
    - `pandas`: For CSV/TSV loading.
    - `pyarrow`: For faster CSV reading with pandas.

## Core Capabilities

### Fast JSONL Processing (`fast_load_jsonl`)
- Streams data line-by-line for memory efficiency.
- Supports automatic decompression.
- Uses `orjson` if available for speed.
- Supports multi-threaded processing for large files.
- Shows progress bar with `tqdm`.

### Universal Loading (`load_by_ext`)
- Detects file type by extension.
- Supports glob patterns (e.g., `data/*.json`) and lists of files.
- Uses parallel processing for multiple files.
- Supports memoization via `do_memoize=True`.

### Serialization (`dump_json_or_pickle`, `load_json_or_pickle`)
- Unified interface for JSON and Pickle.
- Handles Pydantic models automatically.
- Creates parent directories if they don't exist.

## Usage Examples

### Example 1: Streaming Large JSONL
Read a large compressed JSONL file line by line.

```python
from speedy_utils import fast_load_jsonl

# Iterates lazily, low memory usage
for item in fast_load_jsonl('large_data.jsonl.gz', progress=True):
    process(item)
```

### Example 2: Loading Any File
Load a file without worrying about the format.

```python
from speedy_utils import load_by_ext

data = load_by_ext('config.json')
df = load_by_ext('data.csv')
items = load_by_ext('dataset.pkl')
```

### Example 3: Parallel Loading
Load multiple files in parallel.

```python
from speedy_utils import load_by_ext

# Returns a list of results, one for each file
all_data = load_by_ext('logs/*.jsonl')
```

### Example 4: Dumping Data
Save data to disk, creating directories as needed.

```python
from speedy_utils import dump_json_or_pickle

data = {"key": "value"}
dump_json_or_pickle(data, 'output/processed/result.json')
```

## Guidelines

1.  **Prefer JSONL for Large Datasets**:
    - Use `fast_load_jsonl` for datasets that don't fit in memory.
    - It handles compression transparently, so keep files compressed (`.jsonl.gz` or `.jsonl.zst`) to save space.

2.  **Use `load_by_ext` for Scripts**:
    - When writing scripts that might accept different input formats, use `load_by_ext` to be flexible.

3.  **Error Handling**:
    - `fast_load_jsonl` has an `on_error` parameter (`raise`, `warn`, `skip`) to handle malformed lines gracefully.

4.  **Performance**:
    - Install `orjson` for significantly faster JSON operations.
    - `load_by_ext` uses `pyarrow` engine for CSVs if available, which is much faster.

## Limitations

- **Memory Usage**: `load_by_ext` loads the entire file into memory. Use `fast_load_jsonl` for streaming.
- **Glob Expansion**: `load_by_ext` with glob patterns loads *all* matching files into memory at once (in a list). Be careful with massive datasets.
