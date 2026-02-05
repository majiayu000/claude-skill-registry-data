---
name: google-sheets-formula-builder
version: 1.0.0
category: coordination
tags: [google-sheets, formulas, templates, formula-validation]
status: approved
author: CFN Team
description: Constructs and validates Google Sheets formulas from templates with syntax checking
dependencies: [jq, bash]
created: 2025-11-18
updated: 2025-11-18
complexity: Medium
keywords: [formula-generation, formula-validation, sheets-api, syntax-validation]
triggers: [loop-3-formula-application, formula-creation, data-calculation]
performance_targets:
  execution_time_ms: 1000
  success_rate: 0.98
---

# Google Sheets Formula Builder Skill

## Purpose

Constructs Google Sheets formulas from templates and validates syntax before application. Enables safe formula generation with type checking, cell reference validation, and error prevention.

## Problem Solved

Manual formula creation is error-prone. Formulas with syntax errors, invalid references, or circular logic cause cascading failures in spreadsheets. This skill provides template-based formula generation with comprehensive validation ensuring only correct formulas are applied.

## When to Use

- During formula application sprint phase
- When generating aggregate calculations (SUM, AVERAGE, COUNT)
- For conditional logic (IF, IFS, SWITCH)
- When building lookup operations (VLOOKUP, INDEX/MATCH)
- For array formula generation
- Before applying formulas to production sheets

## Interface

### Primary Script: `build-formula.sh`

**Required Parameters:**
- `--formula-type`: Type of formula to build: SUM, AVERAGE, VLOOKUP, IF, ARRAY (required)
- `--range`: Cell range for formula, e.g., A2:C10
- `--target-cell`: Target cell for formula placement, e.g., D2

**Optional Parameters:**
- `--condition`: Condition for IF formulas, e.g., "A2>100"
- `--criteria`: Criteria for formula, e.g., "Status=Complete"
- `--output-only`: Output formula only, don't apply (default: true)
- `--validate-only`: Validate formula syntax without applying

**Usage:**

```bash
# Generate SUM formula
./.claude/cfn-extras/skills/google-sheets-formula-builder/build-formula.sh \
  --formula-type SUM \
  --range A2:C10 \
  --target-cell D2

# Generate IF formula
./.claude/cfn-extras/skills/google-sheets-formula-builder/build-formula.sh \
  --formula-type IF \
  --range A2:C10 \
  --condition "A2>100" \
  --target-cell D2

# Generate VLOOKUP formula
./.claude/cfn-extras/skills/google-sheets-formula-builder/build-formula.sh \
  --formula-type VLOOKUP \
  --range A2:C10 \
  --criteria "Lookup" \
  --target-cell D2

# Validate syntax only
./.claude/cfn-extras/skills/google-sheets-formula-builder/build-formula.sh \
  --formula-type SUM \
  --range A2:C10 \
  --validate-only
```

## Supported Formula Types

### SUM
Sums values in a range with optional conditions.

```json
{
  "type": "SUM",
  "formula": "=SUM(A2:C10)",
  "description": "Sum of range A2:C10",
  "complexity": "basic"
}
```

### AVERAGE
Calculates average of values in range.

```json
{
  "type": "AVERAGE",
  "formula": "=AVERAGE(A2:C10)",
  "description": "Average of range A2:C10",
  "complexity": "basic"
}
```

### VLOOKUP
Looks up value in first column of range.

```json
{
  "type": "VLOOKUP",
  "formula": "=VLOOKUP(\"Lookup\",A2:C10,2,FALSE)",
  "description": "Lookup value in range",
  "complexity": "intermediate"
}
```

### IF
Conditional formula with true/false branches.

```json
{
  "type": "IF",
  "formula": "=IF(A2>100,\"High\",\"Low\")",
  "description": "If A2>100 then High else Low",
  "complexity": "intermediate"
}
```

### ARRAY
Array formula with multiple return values.

```json
{
  "type": "ARRAY",
  "formula": "=ARRAYFORMULA(IF(A2:A>0,B2:B*C2:C,\"\"))",
  "description": "Array formula calculating range",
  "complexity": "advanced"
}
```

## Output Format

```json
{
  "success": true,
  "confidence": 0.96,
  "formula": "=SUM(A2:C10)",
  "formula_type": "SUM",
  "target_cell": "D2",
  "syntax_valid": true,
  "validation": {
    "syntax": true,
    "references": true,
    "circular_refs": false,
    "error_cells": 0
  },
  "deliverables": ["formula_definition"],
  "errors": []
}
```

## Validation Rules

1. **Syntax validation** - Formula parses correctly
2. **Reference validation** - Cell references exist and are valid
3. **Circular reference detection** - No self-referencing formulas
4. **Type checking** - Function arguments match expected types
5. **Range validation** - Ranges are properly formatted
6. **Function existence** - All functions are Google Sheets functions

## Integration with CFN Loop

### Loop 3 Agents (Formula Phase)

```bash
# Generate formula
FORMULA=$(./.claude/cfn-extras/skills/google-sheets-formula-builder/build-formula.sh \
  --formula-type SUM \
  --range A2:C100 \
  --target-cell D2)

# Validate formula
if echo "$FORMULA" | jq -e '.syntax_valid == true' >/dev/null; then
  echo "Formula generated and validated successfully"
else
  echo "Formula validation failed"
fi
```

### Loop 2 Validators

```bash
# Review generated formulas
VALIDATION=$(./.claude/cfn-extras/skills/google-sheets-formula-builder/build-formula.sh \
  --formula-type VLOOKUP \
  --range A2:C100 \
  --validate-only)

if echo "$VALIDATION" | jq -e '.validation.syntax == true' >/dev/null; then
  echo "Formula syntax valid, passing validation"
fi
```

## Best Practices

1. **Validate before applying** - Always validate formula syntax first
2. **Use templates** - Leverage formula templates for consistency
3. **Test ranges** - Verify cell ranges exist before formula generation
4. **Document formulas** - Include comment explaining complex formulas
5. **Version formulas** - Track formula changes in progress state

## Anti-Patterns

❌ **Manual formula strings** - Always use builder script
❌ **Skipping validation** - Always validate before applying
❌ **Hardcoded ranges** - Use parameterized ranges
❌ **Complex nested formulas** - Break into helper columns
❌ **No error handling** - Check for error cells in results

## Success Criteria

- **Pass rate**: ≥0.98 (standard mode)
- **Syntax accuracy**: 100% correct Google Sheets syntax
- **Reference validation**: 0 false negatives on invalid references
- **Performance**: Formula generation <1000ms
- **Error detection**: Catches all syntax errors

## References

- **Google Sheets API**: https://developers.google.com/sheets/api/reference/rest
- **Formula Validation**: `google-sheets-validation` skill
- **CFN Loop Guide**: `.claude/commands/CFN_LOOP_TASK_MODE.md`
