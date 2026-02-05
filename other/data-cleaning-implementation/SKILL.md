---
name: data-cleaning-implementation
description: Update data-cleaning-implementation skill with critical pandas patterns and testing learnings from vp-e62a
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T22:42:09.137Z"
  updated_at: "2026-01-29T22:42:09.137Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Implement Data Cleaning Utilities for Vibe Piper transformations.

# When To Use
- User asks to implement data cleaning features
- Ticket requires deduplication, null handling, outlier detection, type normalization, or text cleaning

# Architecture
Create `src/vibe_piper/transformations/cleaning.py` with:

## Configuration Types
- `NullStrategy` enum (DROP, FILL_DEFAULT, FILL_MEAN, FILL_MEDIAN, FILL_MODE, FILL_FORWARD, FILL_BACKWARD, INTERPOLATE, KEEP)
- `OutlierMethod` enum (IQR, ZSCORE, MODIFIED_ZSCORE, PERCENTILE, ISOLATION_FOREST)
- `OutlierAction` enum (DROP, CAP, FLOOR, MEAN_REPLACE, MEDIAN_REPLACE, FLAG)
- `CleaningConfig` dataclass: dedup_columns, null_strategy, null_fill_value, null_columns, outlier_method, outlier_action, outlier_threshold, outlier_columns, normalize_text, trim_whitespace, case_normalization, standardize_columns, generate_report, strict

## Reporting
- `CleaningReport` dataclass: original_count, final_count, duplicates_removed, nulls_filled, outliers_handled, text_normalized, types_converted, operations (tuple), duration_ms, timestamp, details (dict)
- `records_removed` property
- `to_dict()` method
- `summarize_report()` function for human-readable output

## Decorator
- `@clean_data(config: CleaningConfig | None = None)` decorator:
- Wraps functions returning `list[DataRecord]`
- Returns `(cleaned_data, report)` tuple
- Applies all configured cleaning operations in order

## Main Entry Point
- `clean_dataset(data: list[DataRecord], config: CleaningConfig | None = None) -> tuple[list[DataRecord], CleaningReport]`
- Operations order: deduplication → null handling → outlier treatment → text cleaning → standardization
- Each operation updates report

## Deduplication
- `remove_duplicates(data, columns=None, keep='first') -> tuple[list[DataRecord], dict]`
- `find_duplicates(data, columns=None) -> list[int]` (indices of duplicates)

## Null Handling
- `handle_nulls(data, strategy, fill_value=None, columns=None) -> tuple[list[DataRecord], dict]`
- `drop_nulls(data, columns=None) -> list[DataRecord]`
- `fill_nulls(data, value, columns=None) -> list[DataRecord]`

## Outlier Detection/Treatment
- `detect_outliers(data, method=OutlierMethod, threshold, columns=None) -> dict[str, list[int]]` (column → indices)
- `handle_outliers(data, method, action, threshold, columns=None) -> tuple[list[DataRecord], dict]`
- `cap_outliers(data, method, threshold, columns=None) -> list[DataRecord]`

## Type Normalization
- `normalize_types(data, type_mapping=None, infer=False) -> tuple[list[DataRecord], dict]`
- `convert_column_type(data, column, target_type) -> list[DataRecord]`

## Standardization
- `standardize_columns(data, columns, method='zscore') -> tuple[list[DataRecord], dict]`
- `normalize_minmax(data, columns) -> list[DataRecord]`
- `normalize_zscore(data, columns) -> list[DataRecord]`

## Text Cleaning
- `clean_text(data, trim=True, normalize=False, case_normalization=None, columns=None) -> tuple[list[DataRecord], dict]`
- `trim_whitespace(data, columns=None) -> list[DataRecord]`
- `normalize_case(data, case='lower', columns=None) -> list[DataRecord]`
- `remove_special_chars(data, columns=None, keep_alphanumeric=True, keep_spaces=True) -> list[DataRecord]`

## Utilities
- `get_null_counts(data) -> dict[str, int]`
- `get_value_counts(data, column, top_n=10) -> dict[Any, int]`
- `get_data_profile(data) -> dict[str, Any]`

# Pandas Integration
Use pandas DataFrame internally for performance:
- Convert `list[DataRecord]` to DataFrame: `pd.DataFrame([r.data for r in data])`
- Apply transformations efficiently
- Reconstruct DataRecords: `[DataRecord(data=row.to_dict(), schema=data[0].schema) for _, row in df.iterrows()]`

# String Operations - CRITICAL PATTERN
Prefer vectorized Series.str operations for pandas 2.x text cleaning:
```python
# CORRECT
df[col] = df[col].str.strip()
df[col] = df[col].str.lower()
df[col] = df[col].str.upper()
df[col] = df[col].str.title()

# Avoid Python-level per-row string munging when possible (slower, easier to get NaN/None edge cases wrong)
# df[col] = df[col].apply(lambda x: x.strip())
```

## Outlier Replacement - Type Safety
When replacing outliers (always float mean/median) into integer columns:
```python
# Option 1: Convert column to float first
df[col] = df[col].astype(float)  # Then replacement works

# Option 2: Cast replacement value to int
df.loc[indices, col] = int(mean_val)  # Explicit int cast
```

# Testing Pattern
Create comprehensive test fixtures:
- `sample_schema` with nullable=True for fields that may contain None
- `sample_data`, `data_with_nulls`, `data_with_duplicates`, `data_with_outliers`, `data_with_text_issues`
- Test classes: TestCleaningConfig, TestCleaningReport, TestCleanDataDecorator, TestCleanDataset, TestRemoveDuplicates, TestFindDuplicates, TestHandleNulls, TestDropNulls, TestFillNulls, TestDetectOutliers, TestHandleOutliers, TestCapOutliers, TestNormalizeTypes, TestConvertColumnType, TestStandardizeColumns, TestNormalizeMinMax, TestNormalizeZscore, TestCleanText, TestTrimWhitespace, TestNormalizeCase, TestRemoveSpecialChars, TestGetNullCounts, TestGetValueCounts, TestGetDataProfile, TestSummarizeReport

# Exports
Update `src/vibe_piper/transformations/__init__.py`:
```python
from vibe_piper.transformations.cleaning import (
    clean_data, clean_dataset, CleaningConfig, CleaningReport,
    NullStrategy, OutlierMethod, OutlierAction,
    remove_duplicates, find_duplicates, handle_nulls, drop_nulls, fill_nulls,
    detect_outliers, handle_outliers, cap_outliers,
    normalize_types, convert_column_type, standardize_columns, normalize_minmax, normalize_zscore,
    clean_text, trim_whitespace, normalize_case, remove_special_chars,
    get_null_counts, get_value_counts, get_data_profile, summarize_report
)

__all__ = [
    # Cleaning - Main
    'clean_data', 'clean_dataset',
    # Cleaning - Config & Report
    'CleaningConfig', 'CleaningReport', 'NullStrategy', 'OutlierMethod', 'OutlierAction',
    # Cleaning - Deduplication
    'remove_duplicates', 'find_duplicates',
    # Cleaning - Nulls
    'handle_nulls', 'drop_nulls', 'fill_nulls',
    # Cleaning - Outliers
    'detect_outliers', 'handle_outliers', 'cap_outliers',
    # Cleaning - Type Normalization
    'normalize_types', 'convert_column_type',
    # Cleaning - Standardization
    'standardize_columns', 'normalize_minmax', 'normalize_zscore',
    # Cleaning - Text
    'clean_text', 'trim_whitespace', 'normalize_case', 'remove_special_chars',
    # Cleaning - Utilities
    'get_null_counts', 'get_value_counts', 'get_data_profile', 'summarize_report'
]
```

# Coverage Target
Aim for 85%+ coverage. Write tests for:
- All strategies for each function type
- Edge cases (empty data, single record, all nulls)
- Error conditions (invalid inputs, wrong types)

# Acceptance Criteria
- [x] @clean_data() decorator implemented
- [x] 20+ functions implemented
- [x] Deduplication with remove_duplicates and find_duplicates
- [x] Null handling with 6 strategies (DROP, FILL_DEFAULT, FILL_MEAN, FILL_MEDIAN, FILL_MODE, FILL_FORWARD, FILL_BACKWARD, INTERPOLATE)
- [x] Outlier detection (IQR, Z-score, modified Z-score, percentile)
- [x] Outlier treatment (cap, drop, mean replace, median replace, flag)
- [x] Type normalization (normalize_types, convert_column_type)
- [x] Standardization (zscore, minmax, robust)
- [x] Text cleaning (trim, case normalization, special chars)
- [x] Cleaning report with comprehensive metrics
- [ ] 85%+ test coverage (achieved 73% - needs fixes)

# Known Issues to Address
- Pandas 2.x string accessor pattern (17 tests failing)
- Test fixture nullable fields need adjustment
- Float-to-int type conversion in outlier replacement

# Dependencies
None - standalone transformation module
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
