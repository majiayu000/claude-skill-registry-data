---
name: schema-query-mismatch
description: "Schema-query mismatch detector: compare every query pattern against the declared DB schema, LLM judges production risk. Read-only. Trigger: /schema-query"
trigger: /schema-query
---
# /schema-query

The DB schema says one thing, the queries say another. This skill finds mismatches before they cause production incidents.

## What this is for

- Queries referencing columns that don't exist (runtime error)
- Missing indexes on WHERE/JOIN columns (slow at scale)
- Assumed NOT NULL when NULL is allowed (silent wrong results)
- **Read-only skill.** No database modifications.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/schema-query -help` or `/schema-query -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/query-schema-diff.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each mismatch:

- **Critical**: runtime error (missing column, type mismatch that causes crash)
- **Major**: performance at scale (missing index on high-volume query)
- **Minor**: cosmetic or low-impact (nullable assumption on low-traffic query)
- **Info**: ORM or framework handles it automatically

### Step 5 - Write report

File `schema-query-report.md` in current working directory:

1. **Summary** - mismatches by risk level.
2. **Mismatch table** - critical first. Per mismatch: query file:line, table.column, schema truth, risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight mismatches that would cause a runtime error in production.

## Usage

```
/schema-query               # interactive
/schema-query <dir>         # scan project
/schema-query -help
```


