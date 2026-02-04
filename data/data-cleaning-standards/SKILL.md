---
name: data-cleaning-standards
description: Clean and standardize vehicle insurance CSV/Excel data. Use when handling missing values, fixing data formats, removing duplicates, or standardizing fields. Mentions "clean data", "handle nulls", "standardize", "duplicates", or "normalize".
allowed-tools: Read, Edit, Grep, Glob
---

# Data Cleaning Standards

Clean and standardize vehicle insurance data following established business rules.

## When to Activate

Use this skill when the user:
- Says "clean the data" or "standardize data"
- Mentions "missing values", "null handling", or "fill missing"
- Asks "remove duplicates" or "deduplicate"
- Wants to "normalize dates" or "standardize formats"
- Mentions data preparation or preprocessing

## Quick Start Workflow

```
Step 1: Handle Missing Values
  ↓
Step 2: Remove Duplicates
  ↓
Step 3: Standardize Formats
  ↓
Step 4: Handle Outliers
```

---

## Step 1: Handle Missing Values

### 1.1 Missing Value Strategy by Field Type

| Field Type | Strategy | Fill Value | Why |
|-----------|----------|------------|-----|
| 三级机构 | Lookup from mapping | From mapping table | Authoritative source |
| 团队简称 | Keep null | `''` (empty string) | Optional field |
| 签单/批改保费 | Delete row | N/A | Critical metric |
| 手续费含税 | Fill zero | `0` | Legitimate zero commission |
| 是否续保 | Keep null | `''` | Display as "Unknown" |
| String fields | Fill empty | `''` | Avoid None errors |
| Numeric fields | Delete or 0 | Depends on field | Case by case |

### 1.2 Implementation

```python
def handle_missing_values(df, staff_mapping):
    """Apply missing value strategy"""

    # 1. 三级机构 - lookup from mapping
    if '三级机构' in df.columns:
        for idx in df[df['三级机构'].isnull()].index:
            staff = df.at[idx, '业务员']
            mapped_info = lookup_staff_info(staff, staff_mapping)
            if mapped_info:
                df.at[idx, '三级机构'] = mapped_info['三级机构']

    # 2. 手续费 - fill zero
    if '手续费含税' in df.columns:
        df['手续费含税'] = df['手续费含税'].fillna(0)

    # 3. 签单保费 - delete missing rows
    before = len(df)
    df = df[df['签单/批改保费'].notnull()]
    after = len(df)
    if before > after:
        print(f"Deleted {before - after} rows with missing premium")

    # 4. String fields - fill empty
    string_cols = df.select_dtypes(include=['object']).columns
    df[string_cols] = df[string_cols].fillna('')

    return df
```

---

## Step 2: Remove Duplicates

### 2.1 Deduplication Rules

**Composite Key**: `保单号` + `投保确认时间`

**Keep Strategy**: `keep='last'` (most recent record)

**Why**: Same policy may have multiple updates (批改)

### 2.2 Implementation

```python
def remove_duplicates(df):
    """Remove duplicate records"""

    # Ensure date is datetime
    df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

    # Use duplicated() to avoid type issues
    before = len(df)
    dup_mask = df.duplicated(subset=['保单号', '投保确认时间'], keep='last')
    df = df[~dup_mask]
    after = len(df)

    if before > after:
        print(f"Removed {before - after} duplicates")

    return df
```

---

## Step 3: Standardize Formats

### 3.1 Date Standardization

**Target Format**: `datetime64[ns]`

```python
def standardize_dates(df):
    """Convert all date fields to datetime"""
    date_cols = ['刷新时间', '投保确认时间', '保险起期']

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            invalid = df[col].isnull().sum()
            if invalid > 0:
                print(f"⚠️  {col}: {invalid} invalid dates converted to NaT")

    return df
```

### 3.2 Numeric Standardization

**Target Format**: `float64`

```python
def standardize_numerics(df):
    """Convert numeric fields to float"""
    numeric_cols = ['签单/批改保费', '签单数量', '手续费', '手续费含税', '增值税']

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df
```

### 3.3 String Standardization

**Rules**:
- Strip leading/trailing whitespace
- Map variations (Y/N → 是/否)

```python
def standardize_strings(df):
    """Clean string fields"""

    # Strip whitespace
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    # Standardize yes/no fields
    yes_no_cols = ['是否续保', '是否新能源', '是否过户车', '是否异地车']
    for col in yes_no_cols:
        if col in df.columns:
            df[col] = df[col].map({
                'Y': '是', 'N': '否',
                'y': '是', 'n': '否',
                '1': '是', '0': '否'
            }).fillna(df[col])

    return df
```

---

## Step 4: Handle Outliers

### 4.1 Outlier Detection Rules

**Important**: **NEVER delete negative premiums** (legitimate business data)

| Outlier Type | Detection Rule | Action |
|-------------|---------------|---------|
| Negative premium | `< 0` | ✅ **KEEP** (refunds/adjustments) |
| Extreme premium | `< -1M or > 100K` | ⚠️ Flag only |
| Zero commission | `== 0` | ✅ KEEP (normal) |
| Negative amount | `保额 < 0` | ⚠️ Flag only |

### 4.2 Implementation

```python
def detect_outliers(df):
    """Detect outliers but DO NOT delete"""
    outliers = {}

    # 1. Extreme premium (flag only)
    if '签单/批改保费' in df.columns:
        extreme = df[
            (df['签单/批改保费'] < -1000000) |
            (df['签单/批改保费'] > 100000)
        ]
        if len(extreme) > 0:
            outliers['extreme_premium'] = {
                'count': len(extreme),
                'samples': extreme['保单号'].head(5).tolist()
            }

    # 2. Negative amounts (flag only)
    if '签单/批改保额' in df.columns:
        negative_amt = df[df['签单/批改保额'] < 0]
        if len(negative_amt) > 0:
            outliers['negative_amount'] = {
                'count': len(negative_amt),
                'samples': negative_amt['保单号'].head(5).tolist()
            }

    # Report outliers without deleting
    if outliers:
        print("⚠️  Detected outliers (kept in data):")
        for key, info in outliers.items():
            print(f"  - {key}: {info['count']} records")

    return df, outliers
```

**Critical Rule**: Never filter out negative premiums:
```python
# ❌ WRONG - DO NOT DO THIS
df = df[df['签单/批改保费'] > 0]

# ✅ CORRECT - Keep all values
total_premium = df['签单/批改保费'].sum()  # May be negative
```

---

## Complete Cleaning Pipeline

### All-in-One Function

```python
def clean_data(df, staff_mapping):
    """Complete cleaning pipeline"""

    print("Starting data cleaning pipeline...")
    initial_count = len(df)

    # Step 1: Handle missing values
    df = handle_missing_values(df, staff_mapping)
    print(f"✓ Step 1: Handled missing values")

    # Step 2: Remove duplicates
    df = remove_duplicates(df)
    print(f"✓ Step 2: Removed duplicates")

    # Step 3: Standardize formats
    df = standardize_dates(df)
    df = standardize_numerics(df)
    df = standardize_strings(df)
    print(f"✓ Step 3: Standardized formats")

    # Step 4: Detect outliers (no deletion)
    df, outliers = detect_outliers(df)
    print(f"✓ Step 4: Detected outliers")

    final_count = len(df)
    print(f"\nCleaning complete: {initial_count} → {final_count} records")

    return df, outliers
```

---

## Common Use Cases

### Case 1: "Clean my CSV file"

```python
import pandas as pd
import json

# Load data
df = pd.read_csv('data.csv', encoding='utf-8-sig')
mapping = json.load(open('staff_mapping.json'))

# Run full pipeline
df_clean, outliers = clean_data(df, mapping)

# Save cleaned data
df_clean.to_csv('data_cleaned.csv', index=False, encoding='utf-8-sig')
```

### Case 2: "Handle missing institution fields"

```python
# Focus on Step 1 - missing value handling
df = handle_missing_values(df, staff_mapping)

# Check results
missing_before = df_original['三级机构'].isnull().sum()
missing_after = df['三级机构'].isnull().sum()
print(f"Fixed {missing_before - missing_after} missing institutions")
```

### Case 3: "Remove duplicate policies"

```python
# Focus on Step 2 - deduplication
df_unique = remove_duplicates(df)
print(f"Removed {len(df) - len(df_unique)} duplicates")
```

---

## Cleaning Checklist

Before cleaning:
- [ ] Backup original data
- [ ] Load staff mapping file
- [ ] Check file encoding (use `utf-8-sig` for Excel exports)

During cleaning:
- [ ] Handle missing values (Step 1)
- [ ] Remove duplicates (Step 2)
- [ ] Standardize formats (Step 3)
- [ ] Detect outliers (Step 4)

After cleaning:
- [ ] Verify record count change is reasonable
- [ ] Check critical fields are complete
- [ ] Review outlier report
- [ ] Save cleaned data with new filename

---

## Troubleshooting

### "Many records deleted"

**Check**: Are you accidentally deleting negative premiums?

```python
# Check negative premium count
negative_count = (df['签单/批改保费'] < 0).sum()
print(f"Negative premiums: {negative_count} (should be kept)")
```

### "Date conversion creates many NaT"

**Solution**: Check date format

```python
# Inspect date column
print(df['投保确认时间'].head())

# Try different format
df['投保确认时间'] = pd.to_datetime(
    df['投保确认时间'],
    format='%Y/%m/%d',  # Adjust format
    errors='coerce'
)
```

### "Duplicates not removed"

**Check**: Ensure date column is datetime type

```python
print(df['投保确认时间'].dtype)  # Should be datetime64[ns]
```

---

## Related Files

**Data processor**: [backend/data_processor.py](../../backend/data_processor.py)
- See `_clean_data()` method (lines 132-156)
- See `merge_with_existing()` method (lines 158-192)

**Field definitions**: [docs/FIELD_MAPPING.md](../../docs/FIELD_MAPPING.md)

**Related Skills**:
- `field-validation` - Run this BEFORE cleaning
- `staff-mapping-management` - Update mapping table

---

**Skill Version**: v1.0
**Created**: 2025-11-09
**File Size**: ~310 lines
**Focuses On**: Data cleaning only (not validation or mapping)
