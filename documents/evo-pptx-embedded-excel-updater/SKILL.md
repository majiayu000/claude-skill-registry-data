---
name: evo-pptx-embedded-excel-updater
description: Provides utilities for finding and manipulating embedded Excel OLE objects within PPTX files, reading text boxes for context, modifying Excel cell values while preserving formulas, and saving the updated PPTX. Use when you need to extract embedded Excel spreadsheets from PowerPoint presentations, update exchange rates or other cell values based on text box annotations, replace embedded Excel data while keeping formula integrity, or perform any programmatic modification of OLE-embedded Excel objects in PPTX files.
---

# evo-pptx-embedded-excel-updater

## Overview
End-to-end handling of embedded Excel OLE objects in PPTX files. Covers:
- Identifying OLE shapes and text boxes on slides
- Extracting embedded xlsx blobs via python-pptx
- Reading/modifying Excel data with openpyxl while preserving formula cells
- Writing modified blobs back into the PPTX package
- Parsing text box content for updated exchange rate values

## Requirements
- python-pptx >= 1.0.2
- openpyxl >= 3.1.5

## Key Domain Knowledge

### OLE Object Identification
- Embedded Excel objects have `shape.shape_type == MSO_SHAPE_TYPE.EMBEDDED_OLE_OBJECT` (integer 7)
- The `ole_format.prog_id` contains 'Excel' (typically 'Excel.Sheet.12')
- Do NOT confuse with `MSO_SHAPE_TYPE.TABLE` (native DrawingML tables)

### Excel Blob Access
- Use `shape.ole_format.blob` for direct byte access to the embedded xlsx
- For write-back, get the relationship ID from `shape._element.xpath('.//p:oleObj')` and access `slide.part.rels[r_id].target_part`
- Replace via `target_part._blob = modified_bytes`

### Formula Preservation
- CRITICAL: Load workbook with `data_only=False` to preserve formulas
- Formula cells are strings starting with '='
- Only update non-formula (hardcoded value) cells
- openpyxl strips cached formula values on save; Excel recalculates on open

### Text Box Reading
- Check `shape.has_text_frame` before accessing text
- `shape.text` gives full text content
- Soft line breaks appear as `\x0b` (vertical tab)

### Exchange Rate Table Structure
- Row 1: headers ("Exchange Rate", currency codes...)
- Column A: row currency labels
- Cell at (row_currency_row, col_currency_col) = rate from row_currency to col_currency
- Diagonal cells = 1 (same currency)

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pptx-embedded-excel-updater/scripts')
from utils import (
    find_embedded_ole_excel_shapes,
    extract_excel_blob_from_ole_shape,
    read_text_boxes_from_slide,
    parse_exchange_rate_from_text,
    load_excel_from_blob,
    update_excel_cell_preserve_formulas,
    save_excel_to_blob,
    replace_ole_blob_in_pptx,
    find_cell_by_currency_pair,
    process_pptx_exchange_rate_update
)

# Quick end-to-end usage:
process_pptx_exchange_rate_update('/root/input.pptx', '/root/results.pptx')

# Or step-by-step:
from pptx import Presentation
prs = Presentation('input.pptx')
slide = prs.slides[0]

# Find Excel objects
excel_shapes = find_embedded_ole_excel_shapes(slide)
shape, ole = excel_shapes[0]

# Read text box for updated rate
text_boxes = read_text_boxes_from_slide(slide)
for name, text in text_boxes:
    rate_info = parse_exchange_rate_from_text(text)
    if rate_info:
        from_curr, to_curr, new_rate = rate_info
        break

# Extract and modify Excel
excel_blob, r_id, target_part = extract_excel_blob_from_ole_shape(shape, slide)
wb, ws = load_excel_from_blob(excel_blob)
cell_coord = find_cell_by_currency_pair(ws, from_curr, to_curr)
old_val, updated = update_excel_cell_preserve_formulas(ws, cell_coord, new_rate)

# Save back
modified_blob = save_excel_to_blob(wb)
replace_ole_blob_in_pptx(target_part, modified_blob)
prs.save('output.pptx')
```

## Functions Reference

| Function | Description |
|---|---|
| `find_embedded_ole_excel_shapes(slide)` | Returns list of (shape, ole_format) for Excel OLE objects |
| `extract_excel_blob_from_ole_shape(shape, slide)` | Returns (excel_bytes, r_id, target_part) |
| `read_text_boxes_from_slide(slide)` | Returns list of (shape_name, text) tuples |
| `parse_exchange_rate_from_text(text)` | Returns (from_currency, to_currency, rate) or None |
| `load_excel_from_blob(excel_bytes)` | Returns (workbook, worksheet) with formulas preserved |
| `find_cell_by_currency_pair(ws, from_curr, to_curr)` | Returns cell coordinate string like 'B3' |
| `update_excel_cell_preserve_formulas(ws, cell, value)` | Returns (old_value, was_updated); skips formulas |
| `save_excel_to_blob(wb)` | Returns bytes of modified xlsx |
| `replace_ole_blob_in_pptx(target_part, bytes)` | Replaces blob in-place |
| `process_pptx_exchange_rate_update(in, out)` | End-to-end processing |
