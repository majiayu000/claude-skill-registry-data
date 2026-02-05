---
name: format_validation
description: "Comprehensive validation of FTD analysis output files. Checks JSONL format, field completeness, score validity, and structural requirements for TALD scale evaluations."
version: 1.0.0
---

# FTD Analysis Output Validation

## Overview

This skill provides comprehensive validation for FTD (Formal Thought Disorder) analysis output files generated using the TALD scale. It ensures that all output records meet structural, semantic, and clinical requirements.

## Validation Requirements

### Critical Checks

1. **File Format**: Valid JSONL (one JSON object per line)
2. **Completeness**: All input IDs have corresponding output records
3. **Uniqueness**: No duplicate IDs in output
4. **Score Validity**: All severity scores are integers in [0-4]
5. **Domain Coverage**: All 16 TALD domains present in every record
6. **Screening Structure**: Valid screening object with required fields
7. **Rationale Completeness**: Appropriate rationale entries for scored/flagged domains
8. **Scratchpad/Exclusion**: Present only for flagged domains
9. **Timestamp Format**: Valid ISO 8601 timestamps
10. **Data Consistency**: Logical relationships between fields

## Validation Code

### Python Validation Script

```python
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

# TALD domain codes
REQUIRED_DOMAINS = {
    'CIR', 'CLA', 'CON', 'DER', 'DOT', 'ECH', 'MAN', 'NEO',
    'PER', 'POC', 'POS', 'POT', 'RES', 'SEM', 'TAN', 'VER'
}

VALID_DECISIONS = {'everything_looks_good', 'needs_analysis'}
VALID_SCORES = {0, 1, 2, 3, 4}


def validate_output_file(output_path: str, input_path: str = None) -> Tuple[bool, List[str]]:
    """
    Validate FTD analysis output file.

    Args:
        output_path: Path to output.jsonl
        input_path: Optional path to input.jsonl for completeness checking

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    output_path = Path(output_path)

    # Check file exists
    if not output_path.exists():
        return False, [f"Output file not found: {output_path}"]

    # Load and parse records
    records = []
    seen_ids = set()
    line_num = 0

    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    record = json.loads(line)
                    records.append((line_num, record))

                    # Check for duplicate IDs
                    record_id = record.get('id')
                    if record_id in seen_ids:
                        errors.append(f"Line {line_num}: Duplicate ID '{record_id}'")
                    seen_ids.add(record_id)

                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: Invalid JSON - {e}")

    except Exception as e:
        return False, [f"Error reading file: {e}"]

    if not records:
        return False, ["Output file is empty"]

    # Validate each record
    for line_num, record in records:
        errors.extend(validate_record(record, line_num))

    # Check completeness against input if provided
    if input_path:
        input_ids = load_input_ids(input_path)
        if input_ids:
            missing_ids = input_ids - seen_ids
            extra_ids = seen_ids - input_ids

            if missing_ids:
                errors.append(f"Missing output for input IDs: {sorted(missing_ids)}")
            if extra_ids:
                errors.append(f"Extra output IDs not in input: {sorted(extra_ids)}")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_record(record: Dict, line_num: int) -> List[str]:
    """Validate a single output record."""
    errors = []
    prefix = f"Line {line_num}"

    # Check required top-level fields
    required_fields = ['id', 'screening', 'analyzed_at', 'rationale',
                      'scratchpad', 'exclusion_checklist']
    for field in required_fields:
        if field not in record:
            errors.append(f"{prefix}: Missing required field '{field}'")

    # Validate ID
    if 'id' not in record:
        errors.append(f"{prefix}: Missing 'id' field")
    elif not isinstance(record['id'], str) or not record['id']:
        errors.append(f"{prefix}: ID must be non-empty string")

    # Validate all 16 TALD domains present with valid scores
    missing_domains = REQUIRED_DOMAINS - set(record.keys())
    if missing_domains:
        errors.append(f"{prefix}: Missing TALD domains: {sorted(missing_domains)}")

    for domain in REQUIRED_DOMAINS:
        if domain in record:
            score = record[domain]
            if not isinstance(score, int):
                errors.append(f"{prefix}: {domain} score must be integer, got {type(score).__name__}")
            elif score not in VALID_SCORES:
                errors.append(f"{prefix}: {domain} score must be 0-4, got {score}")

    # Validate screening object
    if 'screening' in record:
        errors.extend(validate_screening(record['screening'], prefix))

    # Validate rationale object
    if 'rationale' in record:
        errors.extend(validate_rationale(record, prefix))

    # Validate scratchpad and exclusion_checklist
    if 'scratchpad' in record and 'screening' in record:
        errors.extend(validate_scratchpad_exclusion(
            record, 'scratchpad', prefix
        ))

    if 'exclusion_checklist' in record and 'screening' in record:
        errors.extend(validate_scratchpad_exclusion(
            record, 'exclusion_checklist', prefix
        ))

    # Validate timestamp
    if 'analyzed_at' in record:
        try:
            datetime.fromisoformat(record['analyzed_at'].replace('Z', '+00:00'))
        except (ValueError, AttributeError) as e:
            errors.append(f"{prefix}: Invalid ISO 8601 timestamp - {e}")

    return errors


def validate_screening(screening: Dict, prefix: str) -> List[str]:
    """Validate screening object structure."""
    errors = []

    if not isinstance(screening, dict):
        errors.append(f"{prefix}: 'screening' must be an object")
        return errors

    # Required fields
    if 'decision' not in screening:
        errors.append(f"{prefix}: screening missing 'decision'")
    elif screening['decision'] not in VALID_DECISIONS:
        errors.append(f"{prefix}: screening decision must be {VALID_DECISIONS}, got '{screening['decision']}'")

    if 'flagged_ftds' not in screening:
        errors.append(f"{prefix}: screening missing 'flagged_ftds'")
    elif not isinstance(screening['flagged_ftds'], list):
        errors.append(f"{prefix}: screening 'flagged_ftds' must be array")
    else:
        # Validate flagged FTD codes
        for ftd in screening['flagged_ftds']:
            if ftd not in REQUIRED_DOMAINS:
                errors.append(f"{prefix}: Invalid FTD code in flagged_ftds: '{ftd}'")

    if 'screening_rationale' not in screening:
        errors.append(f"{prefix}: screening missing 'screening_rationale'")
    elif not isinstance(screening['screening_rationale'], str):
        errors.append(f"{prefix}: screening_rationale must be string")
    elif not screening['screening_rationale'].strip():
        errors.append(f"{prefix}: screening_rationale cannot be empty")

    # Consistency check
    if 'decision' in screening and 'flagged_ftds' in screening:
        decision = screening['decision']
        flagged = screening['flagged_ftds']

        if decision == 'everything_looks_good' and flagged:
            errors.append(f"{prefix}: Decision 'everything_looks_good' but flagged_ftds is not empty")
        elif decision == 'needs_analysis' and not flagged:
            errors.append(f"{prefix}: Decision 'needs_analysis' but flagged_ftds is empty")

    return errors


def validate_rationale(record: Dict, prefix: str) -> List[str]:
    """Validate rationale object completeness."""
    errors = []
    rationale = record.get('rationale', {})

    if not isinstance(rationale, dict):
        errors.append(f"{prefix}: 'rationale' must be an object")
        return errors

    # Check for scored domains (score > 0)
    scored_domains = {domain for domain in REQUIRED_DOMAINS
                     if record.get(domain, 0) > 0}

    # Check for flagged domains (from screening)
    flagged_domains = set()
    if 'screening' in record and isinstance(record['screening'], dict):
        flagged_ftds = record['screening'].get('flagged_ftds', [])
        if isinstance(flagged_ftds, list):
            flagged_domains = set(flagged_ftds)

    # Domains that should have rationale entries
    required_rationale_domains = scored_domains | flagged_domains

    # Check each required domain has rationale
    for domain in required_rationale_domains:
        if domain not in rationale:
            errors.append(f"{prefix}: Missing rationale for domain '{domain}' (scored or flagged)")
        elif not isinstance(rationale[domain], str):
            errors.append(f"{prefix}: Rationale for '{domain}' must be string")
        elif not rationale[domain].strip():
            errors.append(f"{prefix}: Rationale for '{domain}' cannot be empty")
        elif len(rationale[domain].split()) < 10:
            errors.append(f"{prefix}: Rationale for '{domain}' too brief (<10 words)")

    # Warn about unexpected rationale entries (not scored and not flagged)
    unexpected = set(rationale.keys()) - required_rationale_domains
    if unexpected:
        errors.append(f"{prefix}: Unexpected rationale entries for non-scored/non-flagged domains: {sorted(unexpected)}")

    return errors


def validate_scratchpad_exclusion(record: Dict, field_name: str, prefix: str) -> List[str]:
    """Validate scratchpad or exclusion_checklist structure."""
    errors = []
    field_data = record.get(field_name, {})

    if not isinstance(field_data, dict):
        errors.append(f"{prefix}: '{field_name}' must be an object")
        return errors

    # Get flagged domains from screening
    flagged_domains = set()
    if 'screening' in record and isinstance(record['screening'], dict):
        flagged_ftds = record['screening'].get('flagged_ftds', [])
        if isinstance(flagged_ftds, list):
            flagged_domains = set(flagged_ftds)

    # Only flagged domains should have entries
    if not flagged_domains and field_data:
        errors.append(f"{prefix}: {field_name} should be empty when no FTDs flagged")

    # Check each flagged domain has entry
    for domain in flagged_domains:
        if domain not in field_data:
            errors.append(f"{prefix}: Missing {field_name} entry for flagged domain '{domain}'")
        elif not isinstance(field_data[domain], dict):
            errors.append(f"{prefix}: {field_name}['{domain}'] must be an object")
        elif not field_data[domain]:
            errors.append(f"{prefix}: {field_name}['{domain}'] cannot be empty")

    # Check for unexpected domains
    unexpected = set(field_data.keys()) - flagged_domains
    if unexpected:
        errors.append(f"{prefix}: {field_name} has entries for non-flagged domains: {sorted(unexpected)}")

    return errors


def load_input_ids(input_path: str) -> Set[str]:
    """Load all IDs from input.jsonl file."""
    input_ids = set()
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    record = json.loads(line)
                    if 'id' in record:
                        input_ids.add(record['id'])
    except Exception as e:
        print(f"Warning: Could not load input IDs: {e}")
    return input_ids


def print_validation_report(is_valid: bool, errors: List[str], output_path: str):
    """Print formatted validation report."""
    print("\n" + "="*70)
    print(f"VALIDATION REPORT: {output_path}")
    print("="*70)

    if is_valid:
        print("\n✓ VALIDATION PASSED")
        print("  All checks completed successfully.")
    else:
        print(f"\n✗ VALIDATION FAILED")
        print(f"  Found {len(errors)} error(s):\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")

    print("\n" + "="*70 + "\n")


# Main execution
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python validate.py <output.jsonl> [input.jsonl]")
        sys.exit(1)

    output_path = sys.argv[1]
    input_path = sys.argv[2] if len(sys.argv) > 2 else None

    is_valid, errors = validate_output_file(output_path, input_path)
    print_validation_report(is_valid, errors, output_path)

    sys.exit(0 if is_valid else 1)
```

## Usage Instructions

### Basic Validation

Validate output file only:
```bash
python validate.py results/40010_fu1/output_sonnet45.jsonl
```

### Validation with Completeness Check

Validate output against input to ensure all interventions were processed:
```bash
python validate.py results/40010_fu1/output_sonnet45.jsonl results/40010_fu1/input.jsonl
```

### In-Script Usage

```python
from validate import validate_output_file, print_validation_report

# Validate
is_valid, errors = validate_output_file(
    "results/40010_fu1/output_sonnet45.jsonl",
    "results/40010_fu1/input.jsonl"
)

# Print report
print_validation_report(is_valid, errors, "results/40010_fu1/output_sonnet45.jsonl")

# Handle errors programmatically
if not is_valid:
    for error in errors:
        print(f"ERROR: {error}")
```

## Quick Validation Checklist

After completing FTD analysis, verify:

- [ ] **File exists**: `output.jsonl` created in results directory
- [ ] **Valid JSONL**: Each line is valid JSON
- [ ] **Complete**: All input IDs have output records
- [ ] **No duplicates**: Each ID appears exactly once
- [ ] **All domains**: All 16 TALD codes present in each record
- [ ] **Valid scores**: All scores are integers 0-4
- [ ] **Screening valid**: Decision matches flagged_ftds (empty if everything_looks_good)
- [ ] **Rationale complete**: Entries for all scored domains (>0) and all flagged domains
- [ ] **Scratchpad/exclusion**: Present only for flagged domains
- [ ] **Timestamps**: Valid ISO 8601 format

## Common Validation Errors

### Missing Rationale Entries

**Error**: `Missing rationale for domain 'POC' (scored or flagged)`

**Cause**: Domain has score > 0 or was flagged in screening, but no rationale entry exists

**Fix**: Ensure rationale object includes entry for this domain with detailed explanation

### Inconsistent Screening Decision

**Error**: `Decision 'everything_looks_good' but flagged_ftds is not empty`

**Cause**: Screening decision doesn't match flagged_ftds array

**Fix**: If everything_looks_good, flagged_ftds must be empty array `[]`

### Invalid Severity Score

**Error**: `POC score must be 0-4, got 5`

**Cause**: Severity score outside valid range

**Fix**: All TALD domain scores must be integers from 0 to 4 (inclusive)

### Scratchpad for Non-Flagged Domain

**Error**: `scratchpad has entries for non-flagged domains: ['DER']`

**Cause**: Scratchpad entry exists for domain not in flagged_ftds

**Fix**: Only flagged domains should have scratchpad and exclusion_checklist entries

## Validation Statistics

The validation script can be extended to provide statistics:

```python
def compute_statistics(output_path: str) -> Dict:
    """Compute statistics from output file."""
    stats = {
        'total_interventions': 0,
        'everything_looks_good': 0,
        'needs_analysis': 0,
        'domain_scores': {domain: [] for domain in REQUIRED_DOMAINS},
        'flagged_domains': {domain: 0 for domain in REQUIRED_DOMAINS}
    }

    with open(output_path, 'r') as f:
        for line in f:
            record = json.loads(line.strip())
            stats['total_interventions'] += 1

            # Screening stats
            decision = record.get('screening', {}).get('decision')
            if decision == 'everything_looks_good':
                stats['everything_looks_good'] += 1
            elif decision == 'needs_analysis':
                stats['needs_analysis'] += 1

            # Domain scores
            for domain in REQUIRED_DOMAINS:
                if domain in record:
                    stats['domain_scores'][domain].append(record[domain])

            # Flagged domains
            flagged = record.get('screening', {}).get('flagged_ftds', [])
            for domain in flagged:
                stats['flagged_domains'][domain] += 1

    return stats
```

## Integration with Analysis Workflow

After completing FTD analysis:

1. **Run validation immediately**:
   ```python
   is_valid, errors = validate_output_file(output_path, input_path)
   ```

2. **Fix errors if any**:
   - Review error messages
   - Correct output records
   - Re-run validation

3. **Generate summary statistics**:
   ```python
   stats = compute_statistics(output_path)
   print(f"Total interventions: {stats['total_interventions']}")
   print(f"Required analysis: {stats['needs_analysis']}")
   ```

4. **Proceed with downstream analysis** only after validation passes

## Notes

- Validation is **non-destructive** - it only reads files, never modifies them
- Run validation after each transcript to catch errors early
- Use input.jsonl comparison to ensure no interventions were skipped
- Brief rationales (<10 words) trigger warnings - aim for 2-4 sentence paragraphs
- The validation script can be extended for additional domain-specific checks
