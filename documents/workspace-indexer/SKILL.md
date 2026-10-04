---
name: workspace-indexer
description: |
  Explore a workspace to (1) convert binary documents (PDF, PPTX, DOCX, XLSX) into text/Markdown
  and (2) build an index.md file with a keyword map and file inventory.
  Use when the user asks for binary document conversion, document indexing, index.md generation,
  keyword-map creation, workspace file inventorying, or PDF/PPTX/DOCX/XLSX text extraction.
---

# Workspace Indexer

> **Not this skill**: Wiki linking, catalog.json, backlinks, and `[[slug]]` management → use **repo-wiki**.
> **Not this skill**: Single-file text extraction → use **to-md**.

## Overview

This skill provides two core capabilities:

1. **Binary → Markdown conversion** — Batch-convert PDF, PPTX, DOCX, and XLSX via **MarkItDown** (see **to-md** skill policy)
2. **Index generation** — Build a workspace file inventory and keyword map in `index.md`

## Path conventions

All internal paths mentioned in this skill are **relative to the directory containing this `SKILL.md`**, and **are not the same as the workspace current directory (`./`)**.

- Scripts: `scripts/...`
- Other resources: relative paths inside the skill directory
- `python scripts/...` style references must be resolved against this skill's absolute Base Directory at runtime
- In the examples below, `<skill-base-dir>` means the actual deployed absolute path of this skill
- External workspace targets such as the workspace root must be passed explicitly with flags like `--root` and `--out`

## Script list

| Script | Role |
| --- | --- |
| `run.py` | **Unified entry point** that runs conversion and indexing together |
| `convert_binary_docs.py` | Convert binary documents to Markdown |
| `build_index.py` | Build a file inventory and keyword map into `index.md` |
| `check_status.py` | Report converted and unconverted document status |
| `install_deps.py` | Check for required packages and install them automatically |

## Prerequisites

Conversion follows the **to-md** skill policy. Install MarkItDown only — do not use pymupdf, python-docx, python-pptx, or openpyxl.

```bash
# Automatic install
python <skill-base-dir>/scripts/install_deps.py

# Manual install
pip install "markitdown[all]"
```

## Workflow

### Task A: Binary documents → Markdown conversion

Script: `scripts/convert_binary_docs.py`

```bash
# Preview target files with dry-run
python <skill-base-dir>/scripts/convert_binary_docs.py --root . --dry-run

# Convert everything and create .md files next to the originals
python <skill-base-dir>/scripts/convert_binary_docs.py --root .

# Convert only selected formats
python <skill-base-dir>/scripts/convert_binary_docs.py --root . --formats pdf docx

# Write output to a separate directory
python <skill-base-dir>/scripts/convert_binary_docs.py --root . --out ./converted

# Overwrite existing converted files
python <skill-base-dir>/scripts/convert_binary_docs.py --root . --overwrite
```

**Conversion engine:** All formats use **MarkItDown** (`convert_with_markitdown` in `convert_binary_docs.py`). Output structure (headings, tables, slides) is determined by MarkItDown — see the **to-md** skill for details.

---

### Task B: Build `index.md`

Script: `scripts/build_index.py`

```bash
# Default run (create index.md at the root)
python <skill-base-dir>/scripts/build_index.py --root .

# Preview files and keywords with dry-run
python <skill-base-dir>/scripts/build_index.py --root . --dry-run

# Choose a custom output path
python <skill-base-dir>/scripts/build_index.py --root . --out docs/index.md

# Use a custom keyword file (one keyword per line)
python <skill-base-dir>/scripts/build_index.py --root . --keywords keywords.txt

# Ignore specific directories
python <skill-base-dir>/scripts/build_index.py --root . --ignore-dirs tmp out
```

**`index.md` structure:**

```
# Workspace Index
> Generated at / Root / File count

## File inventory (text)
### 📁 Directory name
- [filename](path) (size in KB)

## Binary document list
| Filename | Path | Size | Converted file |
(Link the converted `.md` when present; otherwise mark it as not converted)

## Keyword map
### Keyword
- [files where it appears]
```

**Keyword extraction behavior:**
- Default: auto-extract from `#`, `##`, and `###` headings in `.md` files
- Custom: map files that contain keywords listed in `--keywords keywords.txt`

---

### Task C: Full workflow (unified runner)

`run.py` automatically executes conversion and indexing in sequence.

```bash
# Full workflow (recommended)
python <skill-base-dir>/scripts/run.py --root .

# Conversion only (skip indexing)
python <skill-base-dir>/scripts/run.py --root . --skip-index

# Indexing only (skip conversion)
python <skill-base-dir>/scripts/run.py --root . --skip-convert

# Preview the full workflow with dry-run
python <skill-base-dir>/scripts/run.py --root . --dry-run
```

### Task D: Check conversion status

```bash
# Show unconverted files in the console
python <skill-base-dir>/scripts/check_status.py --root .

# Show the full status including converted files
python <skill-base-dir>/scripts/check_status.py --root . --show-converted

# Save the status report as Markdown
python <skill-base-dir>/scripts/check_status.py --root . --export conversion_status.md
```

## Notes

- `.git`, `__pycache__`, `node_modules`, `.github`, and `venv` directories are ignored by default
- Existing converted files are not regenerated unless `--overwrite` is set
- Scanned PDFs (image-only) require `markitdown[all]` for OCR support (see **to-md** skill)
- For very large workspaces, use `--max-keyword-files` to cap oversized keyword maps
