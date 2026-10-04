---
name: evo-excel-workbook-formula-io
description: Load existing workbooks with openpyxl, validate required sheets and ranges, write Excel formulas into existing cells, save safely, and trigger headless recalculation while preserving formatting.
---

This skill handles workbook I/O and formula injection only.

Knowledge internalized:
- Use `openpyxl.load_workbook(filename=..., read_only=False, data_only=False, keep_vba=False, keep_links=True)` for editable `.xlsx` workbooks.
- Access sheets with `wb['Task']` style, not deprecated APIs.
- Write formulas as English Excel formulas beginning with `=` and using comma separators.
- Preserve workbook structure by modifying only existing sheets/cells; do not create/remove sheets.
- `openpyxl` does not calculate formulas; for reliable cached values on Linux, start LibreOffice headless with a UNO socket, open the workbook, call `calculateAll()`, and save/close it. Use plain `--convert-to` only as fallback.
- Validation should confirm required sheets exist before writing.
- When multiple skills have `utils.py`, use importlib file-based loading to avoid module-name collisions.

Functions:
- `load_editable_workbook(path)`
- `load_cached_workbook(path)`
- `verify_required_sheets(wb, required_sheets)`
- `write_formula_block(ws, formula_map)`
- `save_workbook(wb, path)`
- `force_recalculate_libreoffice(file_path, out_dir=None)`

Portable import example:
```python
import importlib.util

def load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

io_utils = load_module('excel_io_utils', '/app/environment/skills/evo-excel-workbook-formula-io/scripts/utils.py')
wb = io_utils.load_editable_workbook('/root/gdp.xlsx')
```
