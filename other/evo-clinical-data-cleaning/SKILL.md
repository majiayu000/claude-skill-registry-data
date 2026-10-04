---
name: evo-clinical-data-cleaning
description: Utility functions for cleaning raw clinical lab CSV data - handling decimal comma formats, scientific notation normalization, missing value detection, and numeric coercion of mixed-type columns.
---

# evo-clinical-data-cleaning

Reusable utility functions for parsing and cleaning structural data quality issues in clinical lab CSV files.

## Key Functions

- `load_clinical_csv(filepath)` - Load CSV as strings to preserve formatting for manual cleaning
- `replace_decimal_commas(value)` - Convert European decimal commas to dots in a single value
- `replace_decimal_commas_df(df, skip_cols)` - Apply decimal comma fix to entire DataFrame
- `coerce_to_numeric(df, skip_cols)` - Convert all columns to float64, handling scientific notation
- `drop_incomplete_rows(df)` - Drop rows with any missing values
- `format_output_csv(df, output_filepath, skip_cols)` - Round to 2 decimal places, write CSV without scientific notation

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-clinical-data-cleaning/scripts')
from utils import (
    load_clinical_csv, replace_decimal_commas_df,
    coerce_to_numeric, drop_incomplete_rows, format_output_csv
)

# Load data
df = load_clinical_csv('/root/environment/data/ckd_lab_data.csv')

# Fix decimal commas
df = replace_decimal_commas_df(df, skip_cols=['patient_id'])

# Convert to numeric (handles scientific notation)
df = coerce_to_numeric(df, skip_cols=['patient_id'])

# Drop rows with missing values
df = drop_incomplete_rows(df)

# After harmonization, format and save
df = format_output_csv(df, '/root/output.csv', skip_cols=['patient_id'])
```

## Data Quality Issues Handled

1. **Decimal commas**: European format '12,34' -> '12.34'
2. **Scientific notation**: '1.23e2' -> 123.0 (handled by pd.to_numeric)
3. **Missing values**: Rows with any NaN are dropped
4. **Output formatting**: All values rounded to 2 decimal places, no scientific notation in output
