---
name: disk-space-mapper
description: Analyze disk usage across directories, identify large/old directories, and generate storage reports. Use when you need to find directories consuming disk space, identify candidates for cleanup (directories older than X days AND larger than Y MB), sort results by size, or generate disk usage reports. Supports filtering by age and size, automatic sorting by disk space, and file-based report generation.
---

# Disk Space Mapper

## Overview

Quickly analyze disk usage across your filesystem, identify space hogs, and find old directories taking up storage. Perfect for cleanup projects, storage audits, and identifying which projects are consuming the most disk space.

## Quick Start

Analyze a directory to see disk usage sorted by size:

```bash
python3 analyze_disk.py -d /path/to/analyze
```

Find old (>180 days) and large (>20MB) directories:

```bash
python3 analyze_disk.py -d /path/to/analyze -m 180 -s 20 -o report.txt
```

## Common Tasks

### 1. Storage Audit
See what's consuming disk space in a directory tree:

```bash
python3 analyze_disk.py -d /Users/tonytam/git
```

Results automatically sort by size (largest first), showing:
- Directory path
- Size in MB
- Last modification date
- Days since last change

### 2. Find Cleanup Candidates
Identify directories not touched in 6 months that are larger than 20 MB:

```bash
python3 analyze_disk.py -d /Users/tonytam/git -m 180 -s 20 -o candidates.txt
```

### 3. Identify Recent Changes
See active directories (modified recently, largest first):

```bash
python3 analyze_disk.py -d /active/projects
```

Look for low "Days Since Change" values.

### 4. Threshold Filtering
Find anything over 100 MB:

```bash
python3 analyze_disk.py -d /data -s 100
```

Or anything older than 1 year:

```bash
python3 analyze_disk.py -d /archive -m 365
```

## Available Scripts

### Python Version (Recommended)
**File:** `scripts/analyze_disk.py`

Full-featured Python implementation. Use this for most tasks.

**Options:**
- `-d, --dir DIR` - Base directory to analyze
- `-m, --min-days DAYS` - Filter: only dirs older than N days
- `-s, --min-size SIZE_MB` - Filter: only dirs larger than N MB
- `-o, --output FILE` - Save results to file

**Example:**
```bash
python3 analyze_disk.py -d /git -m 180 -s 20 -o old_large.txt
```

### Bash Version
**File:** `scripts/analyze_disk.sh`

Lightweight shell script using standard Unix tools (du, stat, find).

**Options:** Same as Python version with `-` prefix

**Example:**
```bash
./analyze_disk.sh -d /git -m 180 -s 20 -o old_large.txt
```

## Output Format

Results are pipe-delimited (easy to parse or import):

```
Directory|Size (MB)|Last Modified|Days Since Change
==================================================
/path/to/large_dir|554 MB|Feb 23 13:34:56 2025|307 days
/path/to/medium_dir|242 MB|Mar 28 15:34:02 2025|274 days
/path/to/small_dir|37 MB|Dec  2 08:05:07 2023|756 days
```

Always sorted by size (largest first).

## Reference Materials

For detailed usage examples, filtering patterns, and scenario-based workflows, see [usage_guide.md](references/usage_guide.md).

## Tips

- **No filters**: Run without `-m` or `-s` to see all directories
- **Always sorted**: Output automatically sorts by size (largest first)
- **Safe**: Read-only analysis, no files are deleted
- **Fast**: Most directory trees scan in under 30 seconds
- **Flexible**: Use with `grep`, `cut`, or other Unix tools to further process results
