---
name: drift-detection-implementation
description: Implement drift detection features for data quality monitoring including baseline storage, history tracking, thresholds, and validation wrappers
license: MIT
compatibility: [object Object]
metadata:
  created_at: "2026-01-29T23:54:28.547Z"
  updated_at: "2026-01-29T23:54:28.547Z"
  version: "1"
  tags: "validation,drift,data-quality,testing,baseline,history"
  complexity: "medium"
  lines_estimate: "~350"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Implement drift detection with baseline storage, history tracking, configurable thresholds, and validation check wrappers.

# When To Use
- User asks to implement drift detection features
- Ticket requires KS/PSI tests, baseline storage, history tracking, or validation wrappers

# Architecture
Implement in src/vibe_piper/validation/drift_detection.py:

## Configuration Types
- DriftThresholds dataclass: warning, critical, psi_warning, psi_critical, ks_significance
- BaselineMetadata dataclass: baseline_id, created_at, sample_size, columns, description
- DriftHistoryEntry dataclass: timestamp, baseline_id, method, drift_score, max_drift_score, drifted_columns, alert_level

## Result Types
- DriftResult dataclass: method, drift_score, drifted_columns, p_values, statistics, recommendations, timestamp
- ColumnDriftResult dataclass: column_name, drift_score, p_value, is_significant, baseline_distribution, new_distribution, recommendation

## Storage Classes
- BaselineStore class:
  - __init__(storage_dir)
  - _baseline_path(baseline_id) -> Path
  - add_baseline(baseline_id, data, description) -> BaselineMetadata
  - get_baseline(baseline_id, schema=None) -> Sequence[DataRecord]
  - get_metadata(baseline_id) -> BaselineMetadata
  - list_baselines() -> list[BaselineMetadata]
  - delete_baseline(baseline_id)
  - JSON file storage with metadata and data list

## History Tracking
- DriftHistory class:
  - __init__(storage_dir)
  - _history_path(baseline_id) -> Path
  - add_entry(result, baseline_id, thresholds) -> DriftHistoryEntry
  - get_entries(baseline_id, limit=None) -> list[DriftHistoryEntry]
  - get_trend(baseline_id, window=10) -> dict[str, Any]
  - clear_history(baseline_id)
  - JSONL append-only storage (one line per entry)

## Alerting
- check_drift_alert(result, thresholds) -> tuple[bool, str] (should_alert, alert_level)

## Validation Check Wrappers
- check_drift_ks(column, baseline, thresholds=None) -> Callable[[Sequence[DataRecord]], ValidationResult]
- check_drift_psi(column, baseline, thresholds=None) -> Callable[[Sequence[DataRecord]], ValidationResult]
  - Convert DriftResult to ValidationResult based on alert_level
  - Map errors (critical drift), warnings (recommendations, drifted columns)

# Dependencies
- scipy (optional) - Import inside functions with TYPE_CHECKING guard
- datetime.utcnow (deprecation warning - consider datetime.now(datetime.UTC))
- json, pathlib, dataclasses

# Testing Pattern
- Create test fixtures with sample_schema
- Test BaselineStore: add, get, get_metadata, list, delete operations
- Test DriftHistory: add_entry, get_entries, get_trend, clear_history
- Test thresholds validation
- Test validation wrappers with stable/drifted data
- Test alerting logic
- Use tempfile for BaselineStore/DriftHistory storage
- Aim for 85%+ coverage

# Exports
Update src/vibe_piper/validation/__init__.py to export new classes and functions.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
