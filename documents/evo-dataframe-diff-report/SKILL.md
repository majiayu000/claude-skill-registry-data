---
name: evo-dataframe-diff-report
description: Compares two pandas DataFrames (old vs new) by a key column to identify deleted rows and modified fields, then exports results as a properly formatted JSON report with NumPy-safe serialization.
---

# evo-dataframe-diff-report

Compares old vs new DataFrames to find deletions and modifications, exports as JSON.

## Key Functions

### find_deleted_employees(df_old, df_new, id_column='ID')
Finds IDs in old but not in new. Returns sorted list of ID strings.

### find_modified_employees(df_old, df_new, id_column='ID', numeric_columns=None, float_tolerance=1e-4)
Finds field-level changes for employees in both DataFrames.
Returns list of dicts: {"id": "EMP00003", "field": "Salary", "old_value": 50020, "new_value": 55010}
Sorted by (id, field).

### build_diff_report(deleted, modified)
Builds the final report dict with 'deleted_employees' and 'modified_employees'.

### export_diff_to_json(report, output_path, indent=2)
Writes report to JSON file using NumpyTypeEncoder for safe serialization.

## Value Type Rules
- Salary, Years: output as integers
- Score: output as float (e.g., 4.3)
- Text fields (First, Last, Dept, Position, Location): output as strings
- NaN values: output as null

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-dataframe-diff-report/scripts')
from utils import find_deleted_employees, find_modified_employees, build_diff_report, export_diff_to_json

deleted = find_deleted_employees(df_old, df_new, id_column='ID')
modified = find_modified_employees(df_old, df_new, id_column='ID',
                                   numeric_columns=['Salary', 'Years', 'Score'])
report = build_diff_report(deleted, modified)
export_diff_to_json(report, '/root/diff_report.json')
```

## Dependencies
- Requires normalized DataFrames from evo-pdf-excel-extraction
- Both DataFrames must share the same column names and ID format
