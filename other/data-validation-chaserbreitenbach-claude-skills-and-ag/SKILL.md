---
name: data-validation
description: |
  Comprehensive data validation framework for testing schema compliance, data quality, and
  referential integrity. Validates databases, APIs, data pipelines, and file formats. Generates
  data quality scorecards with anomaly detection across completeness, accuracy, and consistency.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
compatibility:
  claude-code: ">=1.0.0"
metadata:
  version: "1.0.0"
  author: "QuantQuiver AI R&D"
  category: "testing"
  tags:
    - data-quality
    - schema-validation
    - etl-testing
    - anomaly-detection
---

# Data Validation Framework

## Purpose

Comprehensive data validation framework for testing schema compliance, data quality, and referential integrity. Validates databases, APIs, data pipelines, and file formats. Generates data quality scorecards with anomaly detection.

## Triggers

Use this skill when:

- "validate data quality"
- "check data integrity"
- "schema validation"
- "test data pipeline"
- "data quality report"
- "validate CSV"
- "check for data anomalies"
- "test ETL output"

## When to Use

- Data pipeline deployment
- Database migration
- API response validation
- Report generation systems
- Data warehouse testing
- ML training data validation

## When NOT to Use

- API endpoint testing (use api-contract-validator)
- Security testing (use security-test-suite)
- Performance testing (use performance-benchmark)

---

## Core Instructions

### Data Quality Dimensions

| Dimension | Description | Weight |
| --------- | ----------- | ------ |
| **Completeness** | Missing values, required fields | 25% |
| **Accuracy** | Type conformance, format validation | 25% |
| **Consistency** | Cross-field rules, referential integrity | 20% |
| **Uniqueness** | Duplicate detection, key uniqueness | 15% |
| **Freshness** | Timestamp validation, staleness | 10% |
| **Anomaly** | Statistical outlier detection | 5% |

### Validation Categories

| Category | Description | Severity |
| -------- | ----------- | -------- |
| **Schema** | Structure and type compliance | Critical |
| **Completeness** | Missing/null value detection | High |
| **Accuracy** | Value correctness and format | High |
| **Consistency** | Cross-field/cross-table rules | Medium |
| **Uniqueness** | Duplicate detection | Medium |
| **Freshness** | Timeliness of data | Medium |
| **Anomaly** | Statistical outlier detection | Low |

### Schema Definition

```yaml
schema:
  tables:
    transactions:
      columns:
        - name: transaction_id
          type: string
          required: true
          unique: true
          pattern: "^TXN-[A-Z0-9]{10}$"

        - name: amount
          type: float
          required: true
          min: 0.01
          max: 1000000

        - name: status
          type: string
          required: true
          enum: [pending, completed, failed]
```

---

## Templates

### Data Quality Report

```markdown
# Data Quality Report

**Source:** {source_type}
**Table:** {table_name}
**Generated:** {timestamp}

## Quality Scorecard

**Overall Score:** {score}/100 ({grade})

| Dimension | Score | Status |
| --------- | ----- | ------ |
| Completeness | {completeness} | {status_icon} |
| Accuracy | {accuracy} | {status_icon} |
| Consistency | {consistency} | {status_icon} |
| Uniqueness | {uniqueness} | {status_icon} |
| Freshness | {freshness} | {status_icon} |

## Data Summary

| Metric | Value |
| ------ | ----- |
| Total Rows | {total_rows} |
| Valid Rows | {valid_rows} ({valid_percent}%) |
| Invalid Rows | {invalid_rows} ({invalid_percent}%) |

## Issue Details

### {category} Issues

**{issue_id}:** {message}

- Column: `{column}`
- Affected rows: {row_count}
- Sample values: `{samples}`
```

---

## Example

**Input**: Validate transactions CSV against schema

**Output**:

```markdown
## Quality Scorecard

**Overall Score:** 87.3/100 (B)

| Dimension | Score | Status |
| --------- | ----- | ------ |
| Completeness | 95.0 | Pass |
| Accuracy | 88.5 | Pass |
| Consistency | 82.0 | Pass |
| Uniqueness | 100.0 | Pass |
| Freshness | 75.0 | Warn |

## Issue Details

### Accuracy Issues

**TYPE-amount:** Expected float, got string

- Column: `amount`
- Affected rows: 45
- Sample values: `"N/A", "pending", "TBD"`
```

---

## Validation Checklist

- [ ] Schema definition matches expected structure
- [ ] All required columns validated
- [ ] Null thresholds appropriately set
- [ ] Foreign key references checked (if applicable)
- [ ] Anomaly detection parameters tuned
- [ ] Sample data reviewed for false positives
- [ ] Report includes actionable remediation

---

## Related Skills

- `api-contract-validator` - For API response validation
- `unit-test-generator` - For data processing function tests
- `test-health-monitor` - For tracking validation trends
