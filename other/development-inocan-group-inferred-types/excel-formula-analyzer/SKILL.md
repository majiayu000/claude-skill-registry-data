---
name: excel-formula-analyzer
description: Analyze Excel spreadsheet formulas to build dependency DAGs (Directed Acyclic Graphs) and understand calculation chains. This skill should be used when the user wants to reverse-engineer Excel formula dependencies, trace how values are calculated from inputs to outputs, validate formula logic, or create reusable calculators from spreadsheet logic.
---

# Excel Formula Analyzer

## Quick Start

To trace formula dependencies in an Excel workbook:

```bash
python .claude/skills/excel-formula-analyzer/scripts/trace-formula-dag.py "Workbook.xlsx" "Sheet Name" \
    --table MyTable \
    --columns 16-36,57,58,59
```

Sample output:
```
[Col 36] End of Harvest
     = =IF([@[Actual End of Harvest]]="",[@[Expected End of Harvest]],[@[Actual ...
  Depends on: ['Actual End of Harvest', 'Expected End of Harvest']
  |- [31] Expected End of Harvest
       = =[@[Expected Beginning of Harvest]]+[@[Harvest Window]]+[@[Additional ...
       |- [28] Expected Beginning of Harvest (calculated)
       |- [59] Harvest Window (INPUT)
       |- [33] Additional Days of Harvest (INPUT)
```

## Overview

This skill enables analysis of Excel spreadsheet formulas to understand how calculations flow from inputs to outputs. It builds dependency graphs (DAGs) from formula references and can help create equivalent code implementations.

## When to Use This Skill

- Tracing how a specific cell's value is calculated
- Building a complete dependency graph of formula relationships
- Reverse-engineering business logic embedded in spreadsheets
- Creating TypeScript/Python implementations that replicate Excel calculations
- Validating that code implementations match Excel behavior

## Core Workflow

### Step 1: Load the Workbook

Load with `data_only=False` to get formulas instead of computed values:

```python
import openpyxl
wb = openpyxl.load_workbook("spreadsheet.xlsx", data_only=False)
ws = wb["SheetName"]
```

### Step 2: Parse Structured Table References

Excel tables use structured references like `TableName[[#This Row],[Column]]`. See `references/structured-refs.md` for complete syntax details.

Key patterns:
- `Table[[#This Row],[Column]]` - Same-row reference
- `Table[Column]` - Full column reference (used in XLOOKUP)

### Step 3: Build the DAG

Run the trace script to analyze dependencies:

```bash
python .claude/skills/excel-formula-analyzer/scripts/trace-formula-dag.py "file.xlsx" "Sheet" --columns 16-36
```

### Step 4: Implement in Code

Translate formulas to TypeScript/Python using patterns in `references/formula-patterns.md`.

## What Didn't Work (Lessons Learned)

### The `formulas` Library

The Python `formulas` library can parse Excel formulas into ASTs, but **fails on structured table references**:

```
Error: Not a valid formula: =MEDIAN(Crops[Revenue - Copy])
```

The library expects A1-style references and cannot handle `TableName[Column]` syntax.

### xlwings COM Interface

xlwings can use Excel's native `DirectPrecedents` API, but:
- Requires Excel to be installed (Windows/Mac only)
- Can timeout on large workbooks
- COM interface can be unreliable

### Converting Table References to A1 Notation

While Excel can convert structured refs to A1 notation (Table menu > Convert to Range), this destroys the semantic meaning and makes the formulas harder to understand.

## Key Nuances

### Excel Date Handling

Excel stores dates as numbers (days since 1900-01-01, with a leap year bug):

```python
from datetime import datetime, timedelta

def excel_to_date(excel_num):
    if excel_num is None or excel_num < 1:
        return None
    return datetime(1899, 12, 30) + timedelta(days=excel_num)
```

### Formula vs Value Reading

- `data_only=True`: Returns calculated values (requires the file was saved with calculations)
- `data_only=False`: Returns formulas as strings

To get both, load the workbook twice.

### COALESCE Patterns

Excel implements COALESCE with `IF(ISBLANK())`. In code, use nullish coalescing:

```typescript
const value = actualValue ?? plannedValue;
```

## Resources

### scripts/

- **trace-formula-dag.py** - Build formula DAGs with CLI arguments for table name and columns
- **validate-calculator.py** - Validate code implementations against Excel values

### references/

- **structured-refs.md** - Complete guide to Excel structured table reference syntax, parsing patterns, and gotchas
- **formula-patterns.md** - Common Excel formulas and their TypeScript/Python equivalents
