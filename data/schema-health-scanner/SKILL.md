---
name: schema-health-scanner
description: "Database schema health scanner: parses DDL files (.sql, .prisma, ORM models), extracts per-table structural metrics (columns, PKs, FKs, indexes, naming conventions, type consistency), detects anti-patterns (missing PKs, unbounded strings, mixed naming, god tables, missing timestamps, FK without index), then the LLM judges each finding in domain context. Read-only. Audience: Both. Trigger: /schema-health"
trigger: /schema-health
---

## What this is for

Database schemas accumulate structural debt silently - tables without primary keys, foreign-key fields without indexes, unbounded `VARCHAR(255)` columns, inconsistent naming conventions, mixed timestamp types, and god-tables with 20+ fields. No linter watches DDL the way ESLint watches JavaScript.

This skill reads DDL from raw SQL, Prisma, Drizzle, TypeORM, or SQLAlchemy model files and scores structural health with anti-pattern detection, then the LLM judges each finding in its domain context - because a missing primary key on a logging table may be acceptable, but on a `customers` table it is a design flaw.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` or `-h` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists. If not, print usage and stop.

### Step 3

3. Run the collector script:

### Step 4

scripts/schema-scan.ps1 -ProjectDir "<path>"

### Step 5

4. LLM reads the JSON output. For each table:

### Step 6

- Examine `metrics` (field count, has timestamps, naming style, FK index coverage).

### Step 7

- Read the `antiPatterns[]` list.

### Step 8

5. Per anti-pattern: is this finding justified by domain context?

### Step 9

- "No PK on audit_log" may be acceptable for append-only logs.

### Step 10

- "22 columns on user_settings" may be intentional denormalization.

### Step 11

- Classify: `real-issue` / `acceptable-given-context` / `false-positive`.

### Step 12

- Add confidence: `proven` / `likely` / `suspected`.

### Step 13

6. Per table: assign an overall health score (A = healthy, B = minor issues, C = needs attention, D = critical) with brief reasoning. Write `schema-health-report.md` to the working directory with: executive summary, table-by-table breakdown, cross-cutting concerns, open questions.

## Usage

```
/schema-health                        # interactive, prompts for directory
/schema-health <dir>                  # scan DDL files in directory
/schema-health -help                  # show usage
```

Returns JSON with `tables[]`: each entry `{name, columns[], pk, fk[], indexes[], metrics{fieldCount, hasTimestamps, namingStyle, fkIndexCoverage}, antiPatterns[]}` plus summary `counts: {scannedFiles, tables, antiPatterns}`.

## Report Format

`schema-health-report.md` with:
- Executive summary (files scanned, tables found, anti-pattern counts)
- Table-by-table breakdown (table name, health score, metrics, anti-patterns with verdict)
- Cross-cutting concerns (naming convention drift, type consistency, timestamp coverage)
- Open questions (suspected-confidence findings needing human review)
