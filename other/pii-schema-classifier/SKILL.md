---
name: pii-schema-classifier
description: "PII schema classifier: scans DDL/ORM models for columns that may contain sensitive data, classifies by sensitivity level using naming patterns, and flags ambiguous columns for LLM domain review. Read-only. Audience: Senior. Trigger: /pii-scan"
trigger: /pii-scan
---

## What this is for

Every column name is a hint about sensitivity: email, ssn, phone, address,
ip_address, credit_card, passport, birth_date. But what about customer_id (public
key or PII?), notes (free text with embedded PII?), metadata_json (unknown
sensitivity?). This skill classifies schema columns by sensitivity using naming
patterns, then the LLM validates and adjusts based on application domain.

The dominant failure mode is the unclassified sensitive column that gets logged,
exported, or exposed in an API response without protection.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/pii-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each column:

### Step 5

- Check the `patternClass` and `confidence` from the deterministic scan.

### Step 6

- For `ambiguous` columns: judge sensitivity based on table context and domain.

### Step 7

- For all columns: validate pattern classifications, correct false positives/negatives.

### Step 8

5. Confidence: `proven` (exact pattern match), `likely` (substring match),

### Step 9

`suspected` (ambiguous column needing domain judgment).

### Step 10

6. Write `pii-classification-report.md` to the working directory.

## Usage

```
/pii-scan                         # interactive, prompts for directory
/pii-scan <dir>                   # scan project directory
/pii-scan -help                   # show usage
```

Returns JSON with `columns[]`: each entry `{table, column, type, patternClass,
sensitivity, confidence, ambiguous}` plus `counts: {scannedFiles, totalColumns,
bySensitivity}`.

## Report Format

`pii-classification-report.md` with:
- Executive summary (total columns, breakdown by sensitivity level)
- High-sensitivity columns (require masking/encryption)
- Medium-sensitivity columns (review access controls)
- Low-sensitivity columns (monitor for context changes)
- Ambiguous columns (need domain review)
- Confidence column for every finding
- Open questions (suspected, needs human review)
