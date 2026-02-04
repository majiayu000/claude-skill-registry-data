---
name: fix_notebook
description: ノートブックのエラーを、そのノートブック自体の修正（セル内容・JSONスキーマ）またはソースコードの修正により解決する
---

# Fix Notebook Errors

This skill handles fixing errors encountered during notebook execution, ranging from Python code bugs to Jupyter JSON schema violations.

## Instructions

1. **Analyze the Failure**:
    * Examine the traceback to determine if the error is in the notebook cell's logic, a JSON schema violation, or the underlying library.

2. **Strategy A: Fix Code Cell (Local)**:
    * If the usage is wrong, imports are missing, or data paths are incorrect, edit the `.ipynb` cells.
    * Modify the `"source"` field of the failing code cell in the notebook JSON.
    * **Unit-Safe Assignment**: When updating `astropy.units` objects, prefer `series.value[:] = new_data` to keep metadata.

3. **Strategy B: Fix JSON Schema**:
    * If `nbconvert` or validators fail with "Additional properties are not allowed ('id' was unexpected)":
    * **Remove Cell IDs**: Delete the `"id"` key from all cells in the JSON.
    * **Normalize nbformat_minor**: Set `nbformat_minor` to `4` (if `nbformat` is 4) to prevent auto-adding IDs.

4. **Strategy C: Fix Library Source Code**:
    * If the bug is in the `gwexpy/` package, trace it to the source file and apply the fix.

5. **Verification**:
    * Re-run the notebook using `jupyter nbconvert --execute` or `test_notebooks` to confirm it passes.

```python
# Utility for Strategy B
import json
def fix_nb_schema(path):
    with open(path, 'r') as f:
        data = json.load(f)
    for cell in data.get('cells', []):
        cell.pop('id', None)
    if data.get('nbformat') == 4 and data.get('nbformat_minor', 0) >= 5:
        data['nbformat_minor'] = 4
    with open(path, 'w') as f:
        json.dump(data, f, indent=1)
```
