---
name: spreadsheet-manager
description: Expert in managing Google Sheets spreadsheets. Use when user mentions "spreadsheet", "Google Sheets", "sheets", or requests spreadsheet operations (create, format, style, import CSV, export data, add formulas). Provides comprehensive operations for data manipulation, cell formatting (currency, dates, percentages), styling (colors, fonts), CSV import/export.
---

# Spreadsheet Manager

## Overview

Manage Google Sheets spreadsheets programmatically with operations for creation, data manipulation, formatting, styling, and import/export.

## Authentication Setup

First-time setup requires Google OAuth credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Sheets API and Google Drive API
3. Create OAuth 2.0 Client ID (Desktop application)
4. Download credentials JSON
5. Save to `~/.claude/credentials/google_credentials.json`

The skill auto-authenticates on first use and saves token at `~/.claude/credentials/google_token.json`.

## Core Operations

All commands run via: `~/.claude/skills/spreadsheet-manager/scripts/spreadsheet-manager [COMMAND] [OPTIONS]`

### Create Spreadsheet

```bash
# Blank spreadsheet
spreadsheet-manager create "Report 2025"

# From template
spreadsheet-manager create "Q1 Report" --template "1abc...xyz" --folder "1def...uvw"
```

Returns JSON with spreadsheet ID and URL.

### Add Data

```bash
# Add values (formulas parsed by default)
spreadsheet-manager add-data "1abc...xyz" "Sheet1" "A1:B2" '[["Name","Amount"],["Item1",100]]'

# Add raw text (no formula parsing)
spreadsheet-manager add-data "1abc...xyz" "Sheet1" "A1" '[["=SUM(1+1)"]]' --formula=false
```

### Import CSV

```bash
spreadsheet-manager import-csv "1abc...xyz" "Data" "/path/to/data.csv" --start "A1"
```

### Format Cells

```bash
# Currency (French format: space separator, € suffix, with decimals)
# Pattern supports up to billions: # ### ### ##0.00 €
spreadsheet-manager format-cells "1abc...xyz" "Sheet1" "B2:B100" "CURRENCY" --pattern "# ### ### ##0.00 €"

# Currency (French format: no decimals)
# Pattern supports up to billions: # ### ### ##0 €
spreadsheet-manager format-cells "1abc...xyz" "Sheet1" "B2:B100" "CURRENCY" --pattern "# ### ### ##0 €"

# Currency (US format: comma separator, $ prefix)
spreadsheet-manager format-cells "1abc...xyz" "Sheet1" "B2:B100" "CURRENCY" --pattern "$#,##0.00"

# Date
spreadsheet-manager format-cells "1abc...xyz" "Sheet1" "C2:C100" "DATE" --pattern "yyyy-mm-dd"

# Percentage
spreadsheet-manager format-cells "1abc...xyz" "Sheet1" "D2:D100" "PERCENT" --pattern "0.00%"
```

**Default currency format:** Use French format `# ### ### ##0.00 €` (space as thousand separator, € suffix, with decimals) unless otherwise specified.

**Important:** The pattern `# ### ### ##0.00 €` properly supports millions and billions with correct space separators. Each group of three `#` represents a thousands group:
- Thousands: `1 000.00 €`
- Millions: `1 000 000.00 €`
- Billions: `1 000 000 000.00 €`

For whole numbers without decimals, use `# ### ### ##0 €` instead.

Format types: NUMBER, CURRENCY, DATE, PERCENT, TIME, TEXT. See `references/format_patterns.md` for pattern examples.

### Style Cells

```bash
# Header row styling
spreadsheet-manager style-cells "1abc...xyz" "Sheet1" "A1:Z1" \
  --bg-color "#4285F4" \
  --font-color "#FFFFFF" \
  --font-size 12 \
  --bold \
  --italic
```

### List Sheets

```bash
# List all sheets in a spreadsheet
spreadsheet-manager list-sheets "1abc...xyz"
```

Returns JSON with sheet information (sheet_id, title, index).

### Create Sheet

```bash
# Create a new sheet in an existing spreadsheet
spreadsheet-manager create-sheet "1abc...xyz" "Costs"
```

### Rename Sheet

```bash
# Rename a sheet
spreadsheet-manager rename-sheet "1abc...xyz" "Sheet1" "Total cost"
```

### Add Note

```bash
# Add a note/comment to a cell
spreadsheet-manager add-note "1abc...xyz" "Costs" "A1" "This is a note with additional information"
```

Notes appear as small indicators in cells and show when hovering over the cell.

### Export

```bash
# Export to CSV
spreadsheet-manager export-csv "1abc...xyz" "Sheet1" "output.csv"
```

## Common Workflows

### Create Formatted Report

```bash
# 1. Create spreadsheet
RESULT=$(spreadsheet-manager create "Monthly Report")
ID=$(echo "$RESULT" | jq -r '.id')

# 2. Import data
spreadsheet-manager import-csv "$ID" "Sheet1" "data.csv" --start "A2"

# 3. Style header
spreadsheet-manager style-cells "$ID" "Sheet1" "A1:E1" --bg-color "#4285F4" --font-color "#FFFFFF" --bold

# 4. Format currency columns
spreadsheet-manager format-cells "$ID" "Sheet1" "C:E" "CURRENCY"

# 5. Export
spreadsheet-manager export-csv "$ID" "Sheet1" "report.csv"
```

### Copy Template and Populate

```bash
# Copy template
RESULT=$(spreadsheet-manager create "Project X" --template "TEMPLATE_ID")
ID=$(echo "$RESULT" | jq -r '.id')

# Add data
spreadsheet-manager add-data "$ID" "Data" "A2:B10" "[[...]]"
```

## Advanced Operations

For operations beyond core script (sheet management, borders, conditional formatting, charts, etc.), see `references/advanced_operations.md`.

These require direct use of Google Sheets API `batchUpdate` method with specific request types.

## Performance Tips

- Batch operations: Combine multiple API calls when possible
- CSV import: Use for large datasets (more efficient than cell-by-cell)
- Template copying: Faster than creating + formatting
- Format after data: Add data first, then apply formatting

## API Limits

- Rate limit: 100 requests per 100 seconds per user
- Max cells per spreadsheet: 10,000,000
- Max columns per sheet: 18,278

Batch multiple operations in single `batchUpdate` call to reduce API usage.

## Troubleshooting

**Authentication errors**: Verify `google_credentials.json` exists and has correct scopes

**Permission errors**: Ensure user has edit access to spreadsheet

**Invalid range**: Use A1 notation (e.g., "A1:B10"), verify sheet name is correct

**API quota exceeded**: Wait and retry, or batch operations to reduce calls

## References

- [Format Patterns](references/format_patterns.md) - Number, currency, date format patterns
- [Advanced Operations](references/advanced_operations.md) - Sheet management, borders, charts, pivots
