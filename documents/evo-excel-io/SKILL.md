---
name: evo-excel-io
description: Provides utility functions for loading, scanning, and saving Excel workbooks with openpyxl 3.1.5, including handling merged cells, detecting placeholder markers, and preserving formatting when writing numeric values back.
---

# evo-excel-io

Utility functions for safe Excel I/O with openpyxl 3.1.5.

## Key Features
- Monkey-patches openpyxl 3.1.5 AppVersion bug to prevent chart corruption
- Safe cell value reading that handles MergedCell objects
- Scanning all sheets for "???" placeholder markers
- Writing recovered numeric values with proper type casting
- Preserving cell formatting during value replacement

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-excel-io/scripts')
from utils import (
    load_workbook_safe,
    find_missing_cells,
    get_cell_value_safe,
    write_recovered_value,
    save_workbook_safe,
    is_numeric,
    is_missing
)

# Load workbook (data_only=True for cached formula values)
wb = load_workbook_safe('input.xlsx')

# Find all ??? cells
missing = find_missing_cells(wb)  # Returns list of {sheet, row, col, coordinate}

# Safely read a cell (handles merged cells)
val = get_cell_value_safe(ws, row=5, col=3)

# Write recovered value
write_recovered_value(ws, row=5, col=3, 1534)

# Save with AppVersion fix
save_workbook_safe(wb, 'output.xlsx')
```

## Functions

- `load_workbook_safe(filepath, data_only=True)` - Load workbook with safe defaults
- `find_missing_cells(wb, marker="???")` - Find all cells with marker across all sheets
- `get_cell_value_safe(ws, row, col)` - Read cell value handling MergedCell
- `write_recovered_value(ws, row, col, value)` - Write numeric value preserving format
- `save_workbook_safe(wb, output_path)` - Save with AppVersion monkey-patch
- `is_numeric(value)` - Check if value is int/float (not bool)
- `is_missing(value, marker="???")` - Check if value is the missing marker
