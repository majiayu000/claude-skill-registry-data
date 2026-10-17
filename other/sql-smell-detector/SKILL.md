---
name: sql-smell-detector
description: "Inline SQL smell detector: harvests SQL strings from application code, runs 15+ static analysis rules (SELECT *, missing WHERE, implicit casts, non-sargable filters, cartesian products, SELECT DISTINCT masking bad joins), then LLM classifies business impact and proposes rewritten SQL. Read-only. Trigger: /sql-smells"
trigger: /sql-smells
---

# /sql-smells - SQL Smell Detector

## What this is for

Inline SQL in application code is a silent quality drain: SELECT * in production queries, missing WHERE clauses, implicit type casts that prevent index usage, non-sargable filters, cartesian products, SELECT DISTINCT masking bad joins. This skill finds all SQL strings in code, parses them, runs 15+ static analysis rules, then the LLM classifies actual business impact and proposes rewritten SQL.

**Audience:** Senior
- Developers use it to catch performance-killing SQL patterns before they hit production.
- Reviewers use it to spot data-access issues during code review.
- Architects use it to enforce query best-practices across the codebase.

### Trigger: `/sql-smells`


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

### Step 1 - `-help`/`-h` check
If the first argument is `-help` or `-h`, print the `## Usage` section and stop.

### Step 2 - Determine project path
Ask for `-ProjectDir` (the source directory to scan). Confirm with user.

### Step 3 - Run collector
```powershell
& "<SKILL_DIR>/scripts/sql-harvest.ps1" -ProjectDir "<path>"
```

Capture the JSON output. If the script exits non-zero or produces no queries, report to user and stop.

### Step 4 - LLM analysis per query
For each query in the JSON output (with its findings[]):

1. **Context inspection**: Read the source file around the query line (3-5 lines context) to understand the data shape and business domain.
2. **Impact assessment**: For each finding, determine if it is a real problem given estimated data patterns:
   - `critical`: Data loss / corruption / full table scan on large table.
   - `high`: Index skip / unnecessary I/O on medium-large table.
   - `medium`: Maintainability issue / minor performance hit.
   - `low`: Cosmetic / no measurable impact.
   - `false-positive`: Rule triggered but is harmless in context (mark as rejected).
3. **Rewrite**: Propose a rewritten SQL query that fixes the issue (or explain why none is needed).

Confidence levels: `proven` (rule matches clearly), `likely` (pattern suggests problem), `suspected` (needs more context).

### Step 5 - Open questions
Collect any ambiguous findings where schema context is missing (e.g., cannot determine column types) in an "Open Questions" section.

### Step 6 - Produce report
Write `sql-smells-report.md` to the working directory.

## Report Format

```
# SQL Smell Report - <project>

## Summary
- <N> queries scanned, <M> with findings, <S> severity breakdown

## Findings (by severity)

### Critical
Query | File:Line | Smell | Impact | Confidence | Proposed SQL
... | ... | ... | ... | ... | ...

### High
...

### Medium
...

### Low
...

## False Positives (rejected)
Query | File:Line | Smell | Reason for Rejection
... | ... | ... | ...

## Open Questions
```

## Usage

```powershell
# Interactive
/sql-smells

# Full project
/sql-smells C:\Projects\my-app

# Help
/sql-smells -help
```
