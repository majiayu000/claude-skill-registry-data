---
name: evo-pdf-excel-extraction
description: Extracts tabular data from PDF files using pdfplumber and reads Excel files using pandas/openpyxl, returning normalized pandas DataFrames with proper data types.
---

# evo-pdf-excel-extraction

Extracts tabular data from PDF files and Excel files, returning normalized DataFrames.

## Key Functions

### extract_table_from_pdf(pdf_path, table_settings=None)
Extracts a multi-page table from a PDF. Handles:
- Multi-page concatenation (iterates all pages)
- Header detection from first page
- Repeated header detection on subsequent pages
- Cell cleaning (whitespace, newlines)

### read_excel_file(excel_path, id_column='ID', sheet_name=0, dtype_map=None)
Reads .xlsx files with openpyxl engine. Preserves string IDs.

### normalize_dataframe(df, id_column='ID', numeric_columns=None)
Normalizes a DataFrame for comparison:
- Strips whitespace from strings
- Preserves ID as string (removes .0 suffix)
- Removes commas from numeric strings and coerces to numeric
- Replaces empty/'nan'/'None' with NaN
- Drops rows with invalid IDs

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pdf-excel-extraction/scripts')
from utils import extract_table_from_pdf, read_excel_file, normalize_dataframe

# Extract from PDF
df_pdf = extract_table_from_pdf('/root/employees_backup.pdf')

# Read Excel
df_excel = read_excel_file('/root/employees_current.xlsx', id_column='ID')

# Normalize both
numeric_cols = ['Salary', 'Years', 'Score']
df_pdf_norm = normalize_dataframe(df_pdf, id_column='ID', numeric_columns=numeric_cols)
df_excel_norm = normalize_dataframe(df_excel, id_column='ID', numeric_columns=numeric_cols)
```

## Domain Knowledge

- pdfplumber extracts text as strings; all values need type coercion
- PDF cells may contain commas in numbers (e.g., "112,000")
- Employee IDs format: "EMP00002" (alphanumeric, 8 chars)
- Numeric columns: Salary (int), Years (int), Score (float)
- Text columns: First, Last, Dept, Position, Location
