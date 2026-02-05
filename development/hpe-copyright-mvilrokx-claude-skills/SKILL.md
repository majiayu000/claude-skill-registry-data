---
name: hpe-copyright
description: >
  Check, add, or fix HPE copyright headers in source files. Use this skill when
  (1) Adding copyright headers to new files, (2) Checking if files have valid
  copyright headers, (3) Updating outdated copyright years, (4) Preparing code
  for CI that enforces copyright headers, (5) User mentions "copyright", "HPE
  header", or "copyright check". Format is "Copyright YYYY-YYYY Hewlett Packard
  Enterprise Development LP" as a comment on the first line.
---

# HPE Copyright Header Management

Ensure all source files have the required HPE copyright header to pass CI checks.

## Copyright Format

```
Copyright {start_year}-{end_year} Hewlett Packard Enterprise Development LP
```

- **start_year**: Year the file was created
- **end_year**: Current year (must be updated annually)
- **Placement**: First line of the file, as a comment

### Examples by Language

| Language | Copyright Line |
|----------|----------------|
| Python | `# Copyright 2024-2025 Hewlett Packard Enterprise Development LP` |
| JavaScript/TypeScript | `// Copyright 2024-2025 Hewlett Packard Enterprise Development LP` |
| Go | `// Copyright 2024-2025 Hewlett Packard Enterprise Development LP` |
| SQL | `-- Copyright 2024-2025 Hewlett Packard Enterprise Development LP` |
| HTML/XML | `<!-- Copyright 2024-2025 Hewlett Packard Enterprise Development LP -->` |
| CSS | `/* Copyright 2024-2025 Hewlett Packard Enterprise Development LP */` |

## Quick Reference

### Check all files (dry run)

```bash
python scripts/copyright_check.py /path/to/repo --dry-run
```

### Fix all files

```bash
python scripts/copyright_check.py /path/to/repo
```

### CI check mode (fails if issues found)

```bash
python scripts/copyright_check.py /path/to/repo --check-only
```

## Rules

1. **Missing header**: Add `Copyright CURRENT_YEAR-CURRENT_YEAR Hewlett Packard Enterprise Development LP`
2. **Outdated year**: Update only the second year to current year (e.g., `2024-2024` → `2024-2025`)
3. **Exclusions**: Respects both `.gitignore` and `.copyrightignore` files (gitignore-style patterns)

## Manual Fixes

When manually adding or fixing a copyright header:

1. Determine the correct comment syntax for the file type
2. Add as the **very first line** of the file
3. Use current year for both years if creating new: `Copyright 2025-2025 Hewlett Packard Enterprise Development LP`
4. If updating existing, only change the second year

## Supported File Types

The script supports 50+ file extensions including:

- **Hash (#)**: `.py`, `.sh`, `.rb`, `.pl`, `.r`, `.jl`
- **Double-slash (//)**: `.js`, `.ts`, `.jsx`, `.tsx`, `.go`, `.c`, `.cpp`, `.java`, `.kt`, `.swift`, `.rs`
- **Dash-dash (--)**: `.sql`, `.lua`, `.hs`
- **Block comments**: `.html`, `.xml`, `.css`, `.vue`

## Exclusion Patterns

The script automatically reads patterns from both `.gitignore` and `.copyrightignore` in the repo root. Use `.copyrightignore` for additional exclusions specific to copyright checking:

```
# Directories
vendor/**
third_party/**

# File types not in .gitignore
*.generated.go

# Specific files
Makefile
```
