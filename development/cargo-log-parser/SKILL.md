---
name: cargo-log-parser
description: Parse and filter cargo build logs to extract errors, warnings, and diagnostics with regex-based filtering. Use when debugging Rust projects, analyzing cargo build output, filtering errors by file path or message pattern, or helping users understand compilation failures. Triggers on cargo build errors, rustc diagnostics, Rust compilation issues, or requests to parse .log files from cargo.
---

# Cargo Log Parser

Parse cargo build logs to extract and filter errors/warnings with precise log boundaries.

## Quick Start

```bash
# From file
python scripts/cargo_log_parser.py build.log --errors

# From stdin (pipe from cargo)
cargo build 2>&1 | python scripts/cargo_log_parser.py --errors
```

## Key Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `-e, --errors` | Errors only | `--errors` |
| `-w, --warnings` | Warnings only | `--warnings` |
| `-f, --file PATTERN` | Filter by file path regex | `--file "tests/.*"` |
| `-m, --message PATTERN` | Filter by message regex | `--message "cannot find"` |
| `-c, --code PATTERN` | Filter by error code | `--code "E0425"` |

## Output Modes

| Flag | Output Style |
|------|--------------|
| (default) | Detailed LLM-friendly format with context |
| `--stream` | Compact one-line-per-diagnostic |
| `--raw` | Original log text for matches only |
| `--json` | Structured JSON output |
| `-v, --verbose` | Include raw log text in output |

## Common Patterns

```bash
# Errors in test files only
python scripts/cargo_log_parser.py build.log --errors --file "tests/.*"

# Find "not found" errors
python scripts/cargo_log_parser.py build.log --errors --message "cannot find|not found"

# All E04xx errors (name resolution)
python scripts/cargo_log_parser.py build.log --code "E04\d\d"

# Group errors by file
python scripts/cargo_log_parser.py build.log --errors --group-by-file

# Group by error code
python scripts/cargo_log_parser.py build.log --errors --group-by-code

# Quick summary
python scripts/cargo_log_parser.py build.log --summary
```

## Python API

```python
from cargo_log_parser import CargoLogParser, LogQuery, DiagnosticLevel

parser = CargoLogParser()
parsed = parser.parse_file("build.log")
query = LogQuery(parsed)

# Filter errors
errors = query.find_errors(file_pattern=r"tests/.*", message_pattern=r"cannot find")

# Get exact log boundaries
for error in errors:
    bounds = query.get_error_boundaries(error)
    print(f"Lines {bounds['line_start']}-{bounds['line_end']}")
    print(bounds['raw_text'])

# Group and analyze
by_file = query.group_by_file(level=DiagnosticLevel.ERROR)
by_code = query.group_by_code()
```

## Regex Reference

| Pattern | Matches |
|---------|---------|
| `tests/.*` | Test files |
| `src/.*` | Source files |
| `.*/mod\.rs` | Any mod.rs |
| `E03\d\d` | Borrow checker errors |
| `E04\d\d` | Name resolution errors |
| `unused_.*` | Unused warnings |
