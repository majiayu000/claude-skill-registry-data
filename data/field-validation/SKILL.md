---
name: field-validation
description: Validate data quality in CSV/Excel files for vehicle insurance platform. Use when checking required fields, validating data formats, detecting quality issues, or generating quality reports. Mentions "validate", "check fields", "data quality", "missing values", or "quality score".
allowed-tools: Read, Edit, Grep, Glob
---

# Field Validation and Data Quality

Validate field completeness, format correctness, and data quality for vehicle insurance CSV/Excel files.

## When to Activate

Use this skill when the user:
- Says "validate the data" or "check data quality"
- Mentions "missing fields", "required fields", or "field validation"
- Asks "is the data complete?" or "quality score"
- Wants to "generate quality report"
- Mentions CSV or Excel file validation

## Quick Start Workflow

When activated, follow this 3-step process:

```
Step 1: Load Data
  ↓
Step 2: Run Validation Checks (4 layers)
  ↓
Step 3: Generate Quality Report
```

---

## Step 1: Load and Inspect Data

### 1.1 Identify File Location

```python
# Project data files
data_file = 'data/车险清单_2025年10-11月_合并.csv'
mapping_file = '业务员机构团队归属.json'
```

### 1.2 Load with Pandas

```python
import pandas as pd

# Load main data
df = pd.read_csv(data_file, encoding='utf-8-sig', low_memory=False)

# Quick inspection
print(f"Loaded {len(df)} records, {len(df.columns)} columns")
print(f"Date range: {df['投保确认时间'].min()} to {df['投保确认时间'].max()}")
```

---

## Step 2: Run 4-Layer Validation

### Layer 1: Required Fields (P0 - Blocking)

**Check these 7 critical fields MUST exist and have values:**

| Field | Why Required | Action if Missing |
|-------|-------------|------------------|
| 投保确认时间 | Time dimension | Abort import |
| 三级机构 | Organization filter | Look up from mapping |
| 业务员 | Staff attribution | Abort import |
| 客户类别3 | Customer segmentation | Abort import |
| 签单/批改保费 | Core metric | Abort import |
| 签单数量 | Core metric | Abort import |
| 是否续保 | Renewal analysis | Abort import |

**Validation Code:**

```python
def validate_required_fields(df):
    """P0 validation - blocking errors"""
    required = ['投保确认时间', '三级机构', '业务员', '客户类别3',
                '签单/批改保费', '签单数量', '是否续保']

    missing_cols = [col for col in required if col not in df.columns]
    if missing_cols:
        return {'valid': False, 'missing_columns': missing_cols}

    # Check null values
    null_counts = df[required].isnull().sum()
    problematic = null_counts[null_counts > 0].to_dict()

    return {
        'valid': len(problematic) == 0,
        'null_counts': problematic,
        'total_invalid_rows': df[required].isnull().any(axis=1).sum()
    }
```

### Layer 2: Format Validation (P0 - Blocking)

**Check data types and formats:**

```python
def validate_formats(df):
    """P0 validation - format errors"""
    errors = []

    # Date format
    try:
        df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
        invalid_dates = df['投保确认时间'].isnull().sum()
        if invalid_dates > 0:
            errors.append(f'Invalid dates: {invalid_dates} rows')
    except:
        errors.append('Date column format error')

    # Numeric format
    try:
        df['签单/批改保费'] = pd.to_numeric(df['签单/批改保费'], errors='coerce')
        invalid_premium = df['签单/批改保费'].isnull().sum()
        if invalid_premium > 0:
            errors.append(f'Non-numeric premium: {invalid_premium} rows')
    except:
        errors.append('Premium column format error')

    return {'valid': len(errors) == 0, 'errors': errors}
```

### Layer 3: Range Validation (P1 - Warning)

**Check if values are within reasonable ranges:**

```python
def validate_ranges(df):
    """P1 validation - warnings only"""
    warnings = []

    # Premium range check
    out_of_range = df[
        (df['签单/批改保费'] < -1000000) |
        (df['签单/批改保费'] > 100000)
    ]
    if len(out_of_range) > 0:
        warnings.append(f'Extreme premium values: {len(out_of_range)} rows')

    # Policy count check
    invalid_count = df[(df['签单数量'] < 1) | (df['签单数量'] > 10000)]
    if len(invalid_count) > 0:
        warnings.append(f'Invalid policy count: {len(invalid_count)} rows')

    return {'warnings': warnings}
```

### Layer 4: Consistency Validation (P1 - Warning)

**Check data consistency with staff mapping:**

```python
def validate_consistency(df, staff_mapping):
    """P1 validation - check against mapping table"""
    import re

    # Build name lookup
    name_to_info = {}
    for staff_key, info in staff_mapping.items():
        match = re.search(r'[\u4e00-\u9fa5]+', staff_key)
        if match:
            name_to_info[match.group()] = info

    # Check unmapped staff
    data_staff = df['业务员'].unique()
    unmapped = [s for s in data_staff if s not in name_to_info]

    return {
        'unmapped_staff': unmapped[:10],  # First 10
        'unmapped_count': len(unmapped),
        'coverage_rate': 1.0 - (len(unmapped) / len(data_staff))
    }
```

---

## Step 3: Generate Quality Report

### 3.1 Calculate Quality Score (0-100)

```python
def calculate_quality_score(validation_results):
    """Compute overall quality score"""
    score = 0

    # Required fields (30 points)
    if validation_results['required_fields']['valid']:
        score += 30

    # Format validation (30 points)
    if validation_results['format']['valid']:
        score += 30

    # Range check (20 points)
    if len(validation_results['range']['warnings']) == 0:
        score += 20
    elif len(validation_results['range']['warnings']) <= 2:
        score += 10

    # Consistency (20 points)
    coverage = validation_results['consistency']['coverage_rate']
    if coverage >= 0.98:
        score += 20
    elif coverage >= 0.95:
        score += 15
    elif coverage >= 0.90:
        score += 10

    return score
```

### 3.2 Report Template

```python
def generate_report(df, validation_results, score):
    """Generate human-readable quality report"""
    report = f"""
# Data Quality Report

**File**: {df.attrs.get('filename', 'Unknown')}
**Records**: {len(df):,}
**Quality Score**: {score}/100 {'✅' if score >= 90 else '⚠️' if score >= 75 else '❌'}

## Validation Results

### ✅ Passed Checks:
{_format_passed_checks(validation_results)}

### ⚠️ Warnings:
{_format_warnings(validation_results)}

### ❌ Errors:
{_format_errors(validation_results)}

## Recommendations

{_generate_recommendations(validation_results, score)}
"""
    return report
```

---

## Common Use Cases

### Case 1: "Validate my CSV file"

```python
# Quick validation
df = pd.read_csv('data.csv', encoding='utf-8-sig')

results = {
    'required_fields': validate_required_fields(df),
    'format': validate_formats(df),
    'range': validate_ranges(df)
}

score = calculate_quality_score(results)
print(f"Quality Score: {score}/100")
```

### Case 2: "Check for missing values"

```python
# Focus on Layer 1
result = validate_required_fields(df)

if not result['valid']:
    print(f"❌ Found {result['total_invalid_rows']} rows with missing required fields")
    print(f"Null counts: {result['null_counts']}")
else:
    print("✅ All required fields are complete")
```

### Case 3: "Is my data quality good?"

```python
# Full validation pipeline
df = pd.read_csv('data.csv', encoding='utf-8-sig')
mapping = json.load(open('mapping.json'))

results = {
    'required_fields': validate_required_fields(df),
    'format': validate_formats(df),
    'range': validate_ranges(df),
    'consistency': validate_consistency(df, mapping)
}

score = calculate_quality_score(results)
report = generate_report(df, results, score)
print(report)
```

---

## Quality Score Interpretation

| Score | Level | Meaning | Action |
|-------|-------|---------|--------|
| 90-100 | 🟢 Excellent | Ready for production | Proceed |
| 75-89 | 🟡 Good | Minor issues | Review warnings |
| 60-74 | 🟠 Fair | Data quality concerns | Fix before import |
| <60 | 🔴 Poor | Critical issues | Do not import |

---

## Troubleshooting

### "Many missing required fields"

**Cause**: Column names don't match expected names

**Solution**:
1. Check actual column names: `df.columns.tolist()`
2. Verify encoding: use `encoding='utf-8-sig'` for Excel exports
3. Check for extra spaces in column names: `df.columns = df.columns.str.strip()`

### "Date format validation fails"

**Cause**: Date format inconsistency

**Solution**:
```python
# Try multiple date formats
df['投保确认时间'] = pd.to_datetime(
    df['投保确认时间'],
    format='%Y-%m-%d',  # Adjust format
    errors='coerce'
)
```

### "Low coverage rate for staff mapping"

**Cause**: Mapping table is outdated

**Action**: Alert user to update `业务员机构团队归属.json`

---

## Related Files

**Main data processor**: [backend/data_processor.py](../../backend/data_processor.py)
- Uses these validation functions
- See lines 132-156 for cleaning logic

**Field definitions**: [docs/FIELD_MAPPING.md](../../docs/FIELD_MAPPING.md)
- Complete field dictionary
- Data types and business rules

**Related Skills**:
- `data-cleaning-standards` - What to do after validation fails
- `staff-mapping-management` - How to update mapping table

---

**Skill Version**: v1.0
**Created**: 2025-11-09
**File Size**: ~330 lines
**Focuses On**: Field validation only (not cleaning or mapping)
