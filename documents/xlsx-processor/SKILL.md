---
name: XLSX Processor
description: This skill should be used when the user asks to "read an Excel file", "open xlsx", "process spreadsheet", "read xlsx tabs", "list sheets", "extract data from Excel", "convert xlsx to csv", "convert xlsx to json", "read xlsx file", or mentions .xlsx files that need to be read or processed. Handles multi-sheet workbooks with flexible output formats.
---

# XLSX Processor

Read and process Excel (.xlsx) files with multiple sheets/tabs. Outputs data as Markdown tables, CSV, or JSON for further processing.

## When to Use

Activate when a user provides an `.xlsx` file and needs to:
- List sheets/tabs in a workbook
- Read data from one or more sheets
- Extract specific cell ranges
- Convert spreadsheet data to CSV, JSON, or Markdown

## Core Script

The bundled `scripts/xlsx_reader.py` handles all XLSX operations. It auto-installs `openpyxl` on first run if not present.

**Script location**: `scripts/xlsx_reader.py` (relative to this skill directory)

### Commands

The script uses PEP 723 inline metadata. Run via `uv run` for automatic dependency management. Falls back to a local venv if `uv` is not available.

```bash
SCRIPT="~/.claude/skills/xlsx-processor/scripts/xlsx_reader.py"

# List all sheets with dimensions
uv run $SCRIPT <file.xlsx> --list-sheets

# Read first sheet as Markdown table (default)
uv run $SCRIPT <file.xlsx>

# Read a specific sheet by name
uv run $SCRIPT <file.xlsx> --sheet "Sheet1"

# Read a specific sheet by index (1-based)
uv run $SCRIPT <file.xlsx> --sheet 2

# Read all sheets
uv run $SCRIPT <file.xlsx> --all

# Read a specific cell range
uv run $SCRIPT <file.xlsx> --sheet "Sales" --range A1:D10

# Output as CSV
uv run $SCRIPT <file.xlsx> --all --format csv

# Output as JSON (structured with headers as keys)
uv run $SCRIPT <file.xlsx> --sheet "Data" --format json

# Specify header row (1-based)
uv run $SCRIPT <file.xlsx> --sheet "Report" --header-row 1

# Limit rows (useful for large sheets)
uv run $SCRIPT <file.xlsx> --sheet "BigData" --max-rows 50
```

### Output Formats

| Format     | Flag              | Best for                                  |
|------------|-------------------|-------------------------------------------|
| Markdown   | `--format markdown` (default) | Direct display in conversation   |
| CSV        | `--format csv`    | Data processing, import to other tools     |
| JSON       | `--format json`   | Structured data, API consumption           |

### Options Reference

| Flag              | Description                              |
|-------------------|------------------------------------------|
| `--list-sheets`   | List all sheet names with row/col counts |
| `--sheet`, `-s`   | Sheet name or 1-based index to read      |
| `--all`, `-a`     | Read all sheets                          |
| `--range`, `-r`   | Cell range (e.g., `A1:D10`)              |
| `--format`, `-f`  | Output: `markdown`, `csv`, or `json`     |
| `--header-row`    | Row number to use as column headers      |
| `--max-rows`      | Max rows to output per sheet             |

## Workflow

### Standard: Read an XLSX File

1. **Locate the file** — confirm the `.xlsx` path exists
2. **List sheets** — run with `--list-sheets` to understand workbook structure
3. **Read target sheet(s)** — use `--sheet` or `--all` with the appropriate format
4. **Process data** — use the output for the user's specific need

### Large Workbooks

For workbooks with many rows, start with `--max-rows 30` to preview, then expand as needed. Use `--range` to target specific sections.

### Multi-Sheet Processing

Use `--all --format json` to get all sheets as structured JSON. Each sheet appears as a separate object with its name and data array.

## Exit Codes

| Code | Meaning              |
|------|----------------------|
| 0    | Success              |
| 1    | File not found       |
| 2    | Invalid input/format |
| 3    | Processing error     |

## Dependencies

The script auto-installs `openpyxl` via pip on first use. No manual setup required. Supports `.xlsx`, `.xlsm`, `.xltx`, and `.xltm` formats.

## Limitations

- Does not support `.xls` (legacy Excel format) — only `.xlsx` and variants
- Formulas return calculated values (not the formula text) by default
- Merged cells may show the value only in the top-left cell
- Very large files (100k+ rows) should use `--max-rows` to avoid excessive output
