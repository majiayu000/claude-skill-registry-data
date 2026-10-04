---
name: "copy"
version: "1.0.0"
description: "Copy operations reference — file duplication, rsync patterns, CoW, buffer strategies, and cross-platform sync. Use when duplicating files, syncing directories, or implementing copy-on-write."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [copy, file, rsync, sync, duplicate, backup, devtools]
category: "devtools"
---

# Copy — File & Data Copy Operations Reference

Quick-reference skill for file copy strategies, rsync patterns, copy-on-write, and cross-platform synchronization.

## When to Use

- Duplicating files or directory trees with specific filters
- Setting up rsync-based backups or mirrors
- Understanding copy-on-write (CoW) behavior
- Implementing efficient copy strategies for large datasets
- Troubleshooting copy failures and permission issues

## Commands

### `intro`

```bash
scripts/script.sh intro
```

Overview of copy operations — types, semantics, and platform differences.

### `rsync`

```bash
scripts/script.sh rsync
```

Rsync patterns — common flags, partial transfers, and include/exclude rules.

### `cow`

```bash
scripts/script.sh cow
```

Copy-on-Write (CoW) — reflinks, filesystem support, and when to use.

### `patterns`

```bash
scripts/script.sh patterns
```

Common copy patterns — mirroring, incremental, differential, snapshot.

### `filters`

```bash
scripts/script.sh filters
```

File filtering techniques — by extension, date, size, and gitignore integration.

### `performance`

```bash
scripts/script.sh performance
```

Performance optimization — buffer sizes, parallel copy, and I/O tuning.

### `errors`

```bash
scripts/script.sh errors
```

Common copy errors, permissions issues, and troubleshooting guide.

### `checklist`

```bash
scripts/script.sh checklist
```

Pre-copy and post-copy verification checklist.

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
| `COPY_DIR` | Data directory (default: ~/.copy/) |

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
