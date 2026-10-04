---
name: "trim"
version: "1.0.0"
description: "Data trimming reference — whitespace trimming, string cleanup, data truncation, outlier trimming, and signal processing. Use when cleaning text data, removing noise, or preparing datasets by trimming unwanted elements."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [trim, clean, strip, whitespace, truncate, outlier, data-processing, atomic]
category: "atomic"
---

# Trim — Data Trimming Reference

Quick-reference skill for data trimming techniques across text, numeric, and signal data.

## When to Use

- Trimming whitespace from strings (leading, trailing, internal)
- Cleaning and normalizing text data
- Trimming outliers from statistical datasets
- Truncating data to fit constraints (columns, buffers)
- Signal trimming and noise removal
- Database column trimming and cleanup

## Commands

### `intro`

```bash
scripts/script.sh intro
```

Overview of trimming — concepts, types, and when to use each.

### `string`

```bash
scripts/script.sh string
```

String trimming — whitespace, characters, patterns, normalization.

### `numeric`

```bash
scripts/script.sh numeric
```

Numeric trimming — outliers, percentile clipping, winsorizing.

### `text`

```bash
scripts/script.sh text
```

Text data cleaning — encoding, invisible characters, BOM removal.

### `database`

```bash
scripts/script.sh database
```

Database trimming — SQL functions, column cleanup, data migration.

### `signal`

```bash
scripts/script.sh signal
```

Signal and time-series trimming — noise removal, smoothing, clipping.

### `examples`

```bash
scripts/script.sh examples
```

Practical trimming examples across languages and tools.

### `pitfalls`

```bash
scripts/script.sh pitfalls
```

Common trimming pitfalls and best practices.

### `help`

```bash
scripts/script.sh help
```

### `version`

```bash
scripts/script.sh version
```

## Configuration

| Variable | Description |
|----------|-------------|
| `TRIM_DIR` | Data directory (default: ~/.trim/) |

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
