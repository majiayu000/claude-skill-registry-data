---
name: google-sheets-validation
version: 1.0.0
category: coordination
tags: [google-sheets, validation, data-integrity, quality-assurance]
status: approved
author: CFN Team
description: Validates data integrity and state consistency between Google Sheets operation sprints
dependencies: [jq, bash, curl]
created: 2025-11-18
updated: 2025-11-18
complexity: Medium
keywords: [validation, data-integrity, sheets-api, state-verification]
triggers: [loop-2-validation, sprint-completion-check, data-integrity-audit]
performance_targets:
  execution_time_ms: 2000
  success_rate: 0.98
---

# Google Sheets Validation Skill

## Purpose

Validates data integrity and state consistency across Google Sheets operations during CFN Loop execution. Provides objective verification that schema exists, data is properly populated, formulas are correct, and no errors exist in the spreadsheet.

## Problem Solved

Google Sheets operations fail silently when data is malformed, formulas contain errors, or API calls return unexpected results. Without validation, invalid intermediate states propagate to subsequent phases, causing cascading failures. This skill provides comprehensive validation gates preventing invalid state progression.

## When to Use

- After schema creation phase completes (verify structure)
- After data population phase completes (verify data consistency)
- After formula application phase completes (verify calculation correctness)
- During Loop 2 validation (verify overall integrity)
- For audit trails and compliance reporting
- Before proceeding to next sprint phase

## Interface

### Primary Script: `validate-state.sh`

**Required Parameters:**
- `--spreadsheet-id`: Google Sheets spreadsheet ID
- `--sheet-name`: Name of sheet to validate

**Optional Parameters:**
- `--check`: Specific validation check to run: schema, data, formulas, all (default: all)
- `--api-key`: Google Sheets API key (or use GOOGLE_API_KEY env var)
- `--verbose`: Enable detailed validation reporting
- `--output-format`: json, report, brief (default: json)

**Usage:**

```bash
# Validate all aspects of sheet
./.claude/cfn-extras/skills/google-sheets-validation/validate-state.sh \
  --spreadsheet-id "abc123def456" \
  --sheet-name "Operations"

# Validate schema only
./.claude/cfn-extras/skills/google-sheets-validation/validate-state.sh \
  --spreadsheet-id "abc123def456" \
  --sheet-name "Operations" \
  --check schema

# Validate with detailed reporting
./.claude/cfn-extras/skills/google-sheets-validation/validate-state.sh \
  --spreadsheet-id "abc123def456" \
  --sheet-name "Operations" \
  --verbose \
  --output-format report
```

## Validation Rules

### Schema Validation

Checks:
1. **Sheet exists** - Named sheet is present in spreadsheet
2. **Header row present** - First row contains column headers
3. **Column count consistent** - All rows have same number of columns
4. **Header uniqueness** - No duplicate column names
5. **Data types correct** - Columns match expected types

```json
{
  "check": "schema",
  "passed": true,
  "details": {
    "sheet_exists": true,
    "header_row_present": true,
    "column_count": 5,
    "columns": ["id", "name", "value", "status", "timestamp"],
    "data_type_matches": true
  }
}
```

### Data Validation

Checks:
1. **Data present** - Sheet contains at least 1 data row
2. **No empty required fields** - Required columns have values
3. **Data format correctness** - Values match expected formats
4. **Row count within limits** - Sheet hasn't exceeded size limits
5. **Uniqueness constraints** - No duplicate primary keys
6. **Referential integrity** - Foreign keys reference valid rows

```json
{
  "check": "data",
  "passed": true,
  "details": {
    "row_count": 100,
    "rows_with_errors": 0,
    "empty_fields_found": 0,
    "format_errors": 0,
    "referential_integrity_errors": 0,
    "sample_rows": [{...}]
  }
}
```

### Formula Validation

Checks:
1. **Formula syntax correct** - All formulas parse without errors
2. **Cell references valid** - Formulas reference existing cells
3. **No circular references** - Formulas don't create loops
4. **Calculations accurate** - Results match expected calculations
5. **Error cells** - No #ERROR, #REF!, #DIV/0! values
6. **Range references valid** - Array formulas reference correct ranges

```json
{
  "check": "formulas",
  "passed": true,
  "details": {
    "formula_count": 12,
    "syntax_errors": 0,
    "reference_errors": 0,
    "circular_references": 0,
    "error_cells": [],
    "formulas": [{"cell": "D2", "formula": "=SUM(A2:C2)", "valid": true}]
  }
}
```

## Output Format

JSON structure for validation results:

```json
{
  "success": true,
  "confidence": 0.96,
  "validation_timestamp": "2025-11-18T10:30:00Z",
  "spreadsheet_id": "abc123def456",
  "sheet_name": "Operations",
  "validations": {
    "schema": {
      "passed": true,
      "errors": [],
      "warnings": []
    },
    "data": {
      "passed": true,
      "errors": [],
      "warnings": []
    },
    "formulas": {
      "passed": true,
      "errors": [],
      "warnings": []
    }
  },
  "overall_status": "valid",
  "error_count": 0,
  "warning_count": 0,
  "deliverables": ["validation_report.json"],
  "errors": []
}
```

## Error Messages

### Schema Errors

```
ERROR: Sheet 'Operations' not found in spreadsheet
ERROR: Header row missing in sheet
ERROR: Column count mismatch: row 5 has 4 columns, expected 5
ERROR: Duplicate column name 'status' found
ERROR: Data type mismatch in column 'timestamp': expected date, got text
```

### Data Errors

```
ERROR: No data rows found in sheet
ERROR: Empty required field in column 'id', row 5
ERROR: Date format error in column 'created_at', row 12: "invalid-date"
ERROR: Duplicate primary key value '42' in rows 5 and 12
ERROR: Foreign key reference invalid: row 8 references non-existent user_id '999'
```

### Formula Errors

```
ERROR: Syntax error in cell D2: "=SUM(A2:C2" missing closing parenthesis
ERROR: Cell reference error in E5: references deleted column 'old_column'
ERROR: Circular reference detected: C2 → D2 → C2
ERROR: Error value in cell F3: #DIV/0! (division by zero)
ERROR: Invalid range in array formula L2: "={A1:B}" malformed range
```

## Integration with CFN Loop

### Loop 3 Agents (Implementers)

After each operation phase completes:

```bash
# Validate schema after creation
VALIDATION=$(./.claude/cfn-extras/skills/google-sheets-validation/validate-state.sh \
  --spreadsheet-id "$SHEET_ID" \
  --sheet-name "Operations" \
  --check schema)

PASSED=$(echo "$VALIDATION" | jq -r '.validations.schema.passed')
if [ "$PASSED" = "true" ]; then
  echo "Schema validation passed, proceeding to data population"
else
  ERRORS=$(echo "$VALIDATION" | jq -r '.validations.schema.errors[]')
  echo "Schema validation failed: $ERRORS"
  exit 1
fi
```

### Loop 2 Validators

Comprehensive validation of completed work:

```bash
# Run full validation on agent deliverables
VALIDATION=$(./.claude/cfn-extras/skills/google-sheets-validation/validate-state.sh \
  --spreadsheet-id "$SHEET_ID" \
  --sheet-name "Operations" \
  --verbose \
  --output-format report)

OVERALL_STATUS=$(echo "$VALIDATION" | jq -r '.overall_status')
ERROR_COUNT=$(echo "$VALIDATION" | jq -r '.error_count')

if [ "$OVERALL_STATUS" = "valid" ] && [ "$ERROR_COUNT" -eq 0 ]; then
  echo "Validation passed with 0.96 confidence"
else
  echo "Validation failed: $ERROR_COUNT errors found"
fi
```

### Product Owner Decision

Use validation results to inform go/no-go decision:

```bash
# Get validation results
VALIDATION=$(./.claude/cfn-extras/skills/google-sheets-validation/validate-state.sh \
  --spreadsheet-id "$SHEET_ID" \
  --sheet-name "Operations")

if [ "$(echo "$VALIDATION" | jq -r '.success')" = "true" ]; then
  echo "PROCEED - All validations passed"
else
  echo "ITERATE - Validation failures require fixes"
fi
```

## Success Criteria

- **Pass rate**: ≥0.95 (standard mode)
- **Validation time**: <2000ms for typical spreadsheets
- **Error detection**: 0 false negatives (catches all real issues)
- **False positive rate**: <0.05 (max 5% of validation failures invalid)
- **API reliability**: 0 timeouts, graceful rate limit handling

## Configuration

### Environment Variables

```bash
export GOOGLE_API_KEY="your-api-key-here"
export GOOGLE_SHEETS_QUOTA_LIMIT=100  # Requests per minute
export VALIDATION_TIMEOUT_MS=5000      # Max validation time
```

### Rate Limiting

The skill implements rate limiting to respect Google Sheets API quotas:

```bash
# Automatic rate limiting with exponential backoff
# Quota: 60 requests per minute per user
# Delays: 100ms initial, doubles on quota exceed (max 5s)
```

## Best Practices

1. **Validate early**: Run validation after each phase completes
2. **Use specific checks**: Run only needed validations (--check schema)
3. **Capture results**: Store validation JSON for audit trails
4. **Handle errors gracefully**: Use validation errors to inform retry logic
5. **Log everything**: Enable --verbose for troubleshooting

## Anti-Patterns

❌ **Skipping validation** - Assuming upstream operations are correct
❌ **Ignoring warnings** - Warnings often indicate data quality issues
❌ **One-time validation** - Validate after each phase, not just at end
❌ **No error context** - Implement proper error handling and logging
❌ **API quota ignorance** - Don't exceed Google Sheets API limits

## Testing

Comprehensive test suite included:

```bash
# Run all validation tests
./.claude/cfn-extras/skills/google-sheets-validation/test.sh

# Run specific test category
./.claude/cfn-extras/skills/google-sheets-validation/test.sh --category schema

# Validate skill itself
./.claude/cfn-extras/skills/google-sheets-validation/validate.sh
```

### Test Categories

1. **Schema validation tests** - Header presence, column consistency
2. **Data validation tests** - Format correctness, referential integrity
3. **Formula validation tests** - Syntax, circular references, calculations
4. **Error handling tests** - Missing sheets, malformed data, API errors
5. **Performance tests** - Execution time under load

## References

- **Google Sheets API**: https://developers.google.com/sheets/api
- **Data Integrity Patterns**: `.claude/skills/cfn-defense-in-depth/SKILL.md`
- **CFN Loop Validation**: `.claude/skills/cfn-loop-validation/SKILL.md`
- **Agent Output Standards**: `docs/AGENT_OUTPUT_STANDARDS.md`
