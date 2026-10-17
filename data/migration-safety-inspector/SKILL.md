---
name: migration-safety-inspector
description: "Database migration safety inspector: scans SQL migration files for 20+ safety rules (table rewrites, missing CONCURRENTLY, destructive DROP, unsafe constraints, missing IF EXISTS, DML on existing tables, missing transaction wrappers), then the LLM assesses blast radius per finding against actual schema and usage patterns, recommending safer alternatives. Read-only. Trigger: /migration-safety"
trigger: /migration-safety
---

## What this is for

Database migrations are the leading cause of production incidents. Missing
CONCURRENTLY, ALTER COLUMN TYPE causing full-table rewrites, destructive DROP
without rollback, unsafe constraint additions with no lock-timeout - every SQL
migration file carries risks that schema review often misses.

This skill automates the safety review: a deterministic collector finds all SQL
migration files, parses every DDL statement, and checks 20+ safety rules. The
LLM then assesses the blast radius of each finding against the actual schema
and usage patterns, and recommends safer alternatives.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1 - `-help`/`-h` check
If `-help` or `-h` is passed, print the `## Usage` block below and stop.

### Step 2 - Confirm project directory
Confirm `-ProjectDir` is provided and the path exists.

### Step 3 - Run collector
```powershell
& "<SKILL_DIR>/scripts/migration-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - LLM reads findings
Read the JSON output. For each finding, note the severity, line, description,
and DDL statement. The collector categorizes findings by safety rule:
- **table-rewrite**: ALTER COLUMN TYPE, ADD COLUMN NOT NULL without DEFAULT
- **missing-concurrently**: CREATE INDEX, REINDEX, VACUUM without CONCURRENTLY
- **destructive**: DROP TABLE, DROP COLUMN, TRUNCATE
- **unsafe-constraint**: ADD FOREIGN KEY without NOT VALID
- **missing-if-exists**: DDL referencing objects without IF EXISTS / IF NOT EXISTS
- **dml-on-migration**: INSERT/UPDATE/DELETE on existing tables in migration
- **missing-transaction**: DDL statements not wrapped in a transaction

### Step 5 - Assess blast radius per finding
For each finding, the LLM should:
- Search the project for the affected table/column/index usage patterns
- Estimate: is this acceptable in a maintenance window?
- Consider: rows affected, locks held, replication lag, rollback cost
- Recommend a safer alternative (e.g. NOT VALID, CONCURRENTLY, multi-step)

### Step 6 - Write report
Write `migration-safety-report.md` to the working directory with:
- Executive summary (files scanned, total findings, by severity)
- Critical findings (destructive, table rewrites on large tables)
- Medium findings (missing CONCURRENTLY, unsafe constraints)
- Low findings (missing IF EXISTS, missing transaction wrappers)
- Safer alternatives per finding
- Open questions (cannot determine table size or usage)

## Usage

```
/migration-safety                           # interactive, prompts for directory
/migration-safety <dir>                     # scan SQL migration files in directory
/migration-safety -help                     # show usage
```

## Report Format

`migration-safety-report.md` with:
- Executive summary (files scanned, statements, total findings by severity)
- Critical findings (destructive operations, table rewrites on referenced columns)
- Medium findings (missing CONCURRENTLY, unsafe constraints, DML on existing tables)
- Low findings (missing IF EXISTS, missing transaction wrappers)
- Per finding: file, line, DDL, blast radius estimate, safer alternative
- Open questions
