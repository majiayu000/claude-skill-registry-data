---
name: oscal-validator
description: Validate OSCAL documents for structural integrity, schema compliance, and OSCAL-specific requirements. Use this skill to check if OSCAL documents are properly formatted and meet NIST OSCAL specifications before processing.
---

# OSCAL Validator Skill

Validate OSCAL documents against NIST schemas and perform structural integrity checks to ensure compliance data quality.

## When to Use This Skill

Use this skill when you need to:
- Verify an OSCAL document is properly formatted
- Check for missing required fields
- Validate UUIDs and cross-references
- Ensure metadata completeness
- Identify structural issues before further processing

---

## ✅ Data Source Principle

This skill validates **documents you provide** against structural rules and OSCAL schema requirements. Validation logic is safe — it checks format and syntax, not compliance content.

**Note:** For baseline completeness validation (e.g., "does this SSP cover all FedRAMP Moderate controls?"), you must also provide the baseline profile/catalog.

---

## Validation Severity Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| **ERROR** | Document is invalid | Must fix before use |
| **WARNING** | Potential issues | Should review |
| **INFO** | Suggestions | Optional improvements |

## Validation Rules

### Structure Validation (STRUCT)

| Rule | Description |
|------|-------------|
| STRUCT-001 | Document must not be empty or null |
| STRUCT-002 | Document must have a root element |
| STRUCT-003 | Root element must be a valid OSCAL model type |

### Metadata Validation (META)

| Rule | Description |
|------|-------------|
| META-001 | Metadata section is required |
| META-002 | Title is required |
| META-003 | Last-modified timestamp is required |
| META-004 | Version is required |
| META-005 | OSCAL version should match current spec |

### UUID Validation (UUID)

| Rule | Description |
|------|-------------|
| UUID-001 | Document UUID must be present |
| UUID-002 | UUIDs must be valid RFC 4122 format |
| UUID-003 | UUIDs must be unique within document |

### Reference Validation (REF)

| Rule | Description |
|------|-------------|
| REF-001 | Internal references must resolve |
| REF-002 | Control references must exist |
| REF-003 | Party references must resolve |

## How to Validate an OSCAL Document

### Step 1: Check Basic Structure
1. Verify document is not empty
2. Confirm root element exists
3. Validate root element is a valid OSCAL type

### Step 2: Validate Metadata
1. Check for required `metadata` section
2. Verify `title` is present and non-empty
3. Confirm `last-modified` is valid ISO timestamp
4. Check `version` is present
5. Validate `oscal-version` matches expected format

### Step 3: Validate UUIDs
1. Check document-level UUID exists
2. Validate UUID format (8-4-4-4-12 hexadecimal)
3. Build list of all UUIDs
4. Check for duplicates

### Step 4: Validate References
1. Find all internal references (e.g., `#uuid-value`)
2. Verify each reference resolves to existing element
3. Check control-id references against imported catalogs
4. Validate party-uuid references

### Step 5: Model-Specific Validation

**For Catalogs:**
- Groups should have controls
- Controls should have statements
- Parameters should have values or selections

**For SSPs:**
- Import-profile must reference valid profile
- System-characteristics must include system-ids
- Control-implementation must address all imported controls

**For Component Definitions:**
- Components must have titles
- Control implementations must reference valid controls

## Validation Report Format

Provide validation results as:

```
VALIDATION REPORT
=================
Document: [filename]
Model Type: [type]
Valid: [YES/NO]

Issues Found:
- [SEVERITY] [RULE-ID]: [Message] at [location]

Summary:
- Errors: X
- Warnings: Y
- Info: Z
```

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Missing metadata | Incomplete document | Add required metadata section |
| Invalid UUID | Malformed identifier | Generate new RFC 4122 UUID |
| Unresolved reference | Broken link | Update reference or add target |
| Missing timestamp | Incomplete metadata | Add ISO 8601 timestamp |

## Example Usage

When asked "Validate this SSP for compliance":

1. Parse the document
2. Run all validation checks
3. Collect issues by severity
4. Report findings with specific locations
5. Provide actionable fix recommendations
