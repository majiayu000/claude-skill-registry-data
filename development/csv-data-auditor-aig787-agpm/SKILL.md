---
name: csv-data-auditor
description: Validate and audit CSV data for quality, consistency, and completeness. Use when you need to check CSV files for data issues, missing values, or format inconsistencies.
---

# CSV Data Auditor

## Instructions

When auditing CSV data, perform these validation checks systematically:

### 1. File Structure Validation
- Verify the file exists and is readable
- Check if the file is a valid CSV format
- Ensure consistent delimiter usage
- Verify proper quoting and escaping
- Check for balanced quotes

### 2. Header Analysis
- Confirm headers exist (unless headerless CSV)
- Check for duplicate header names
- Validate header naming conventions
- Ensure headers are descriptive and consistent
- Check for special characters in headers

### 3. Row Consistency
- Count total rows and columns
- Verify all rows have the same number of columns
- Check for empty rows or rows with only whitespace
- Identify truncated rows
- Detect corrupted or malformed rows

### 4. Data Type Validation
For each column, validate the expected data type:

#### Numeric Fields
- Check for non-numeric values
- Validate decimal point usage
- Look for negative values where inappropriate
- Check for extremely large/small values

#### Date/Time Fields
- Verify date format consistency (ISO 8601, US, EU, etc.)
- Check for invalid dates (e.g., February 30th)
- Validate time zone handling
- Look for future dates where inappropriate

#### Text Fields
- Check for encoding issues
- Look for unexpected special characters
- Verify string length constraints
- Check for leading/trailing whitespace

#### Boolean Fields
- Validate true/false representations
- Check for 1/0, Y/N, Yes/No consistency
- Look for ambiguous values

### 5. Data Quality Checks

#### Missing Values
- Count NULL/empty values per column
- Calculate missing value percentages
- Identify patterns in missing data
- Check for placeholders like "N/A", "null", "-"

#### Duplicates
- Find exact duplicate rows
- Check for duplicate IDs or keys
- Identify near-duplicates (typos, variations)
- Validate uniqueness constraints

#### Outliers
- Identify statistical outliers in numeric columns
- Check for values outside expected ranges
- Look for anomalies in categorical data
- Validate business logic constraints

#### Consistency Checks
- Cross-validate related columns
- Check referential integrity
- Validate business rules
- Look for logical contradictions

### 6. Validation Script (Python)

Create a Python script to perform automated checks:

```python
import pandas as pd
import numpy as np
from datetime import datetime

def audit_csv(file_path, delimiter=','):
    """Perform comprehensive CSV audit"""

    # Load CSV
    try:
        df = pd.read_csv(file_path, delimiter=delimiter)
    except Exception as e:
        return {"error": f"Failed to load CSV: {str(e)}"}

    audit_report = {
        "file_info": {
            "rows": len(df),
            "columns": len(df.columns),
            "headers": list(df.columns)
        },
        "issues": []
    }

    # Check for missing values
    missing_counts = df.isnull().sum()
    for col, count in missing_counts.items():
        if count > 0:
            percentage = (count / len(df)) * 100
            audit_report["issues"].append({
                "type": "missing_values",
                "column": col,
                "count": count,
                "percentage": round(percentage, 2)
            })

    # Check for duplicates
    duplicate_rows = df.duplicated().sum()
    if duplicate_rows > 0:
        audit_report["issues"].append({
            "type": "duplicates",
            "count": duplicate_rows
        })

    # Data type validation
    for col in df.columns:
        # Check for mixed types in object columns
        if df[col].dtype == 'object':
            sample_values = df[col].dropna().head(10)
            # Add specific type checks based on column name patterns

    return audit_report
```

### 7. Report Format

Generate a structured audit report:

```markdown
# CSV Audit Report

## File Information
- File: data.csv
- Size: 15.2 MB
- Rows: 50,000
- Columns: 12
- Headers: id, name, email, age, join_date, salary, department, ...

## Issues Found

### Critical Issues
1. **Missing Values**:
   - `email`: 2,500 missing (5.0%)
   - `salary`: 150 missing (0.3%)

### Warnings
1. **Inconsistent Date Format**:
   - `join_date`: Mix of ISO and US formats detected
   - Examples: 2023-01-15, 01/15/2023, 15-Jan-2023

2. **Potential Outliers**:
   - `age`: Values 0 and 150 detected
   - `salary`: Extremely high values > $1M

### Recommendations
1. Clean up email field - contact data source
2. Standardize date format to ISO 8601
3. Validate age and salary ranges
4. Remove or investigate duplicate rows

## Summary
- Overall Quality: Good
- Issues to Fix: 3 critical, 5 warnings
- Estimated Fix Time: 2-3 hours
```

### 8. Common Issues and Solutions

#### Encoding Problems
- Try different encodings (UTF-8, Latin-1, Windows-1252)
- Use `chardet` library to detect encoding
- Handle BOM (Byte Order Mark) if present

#### Large Files
- Process in chunks for memory efficiency
- Use Dask for out-of-core processing
- Sample data for quick validation

#### Complex CSVs
- Handle quoted fields with embedded delimiters
- Process multi-line records carefully
- Validate escape character usage

## Usage

1. Provide the CSV file path
2. Specify delimiter if not comma
3. Configure validation rules based on your data
4. Review the generated audit report
5. Address issues systematically

## Tips

- Always keep a backup of original data
- Document any data transformations
- Create validation rules based on business requirements
- Consider using schema validation tools like Great Expectations
- Automate regular audits for production data