---
name: schema-drift-tracker
trigger: /schema-drift
description: >
  Schema drift is the silent erosion of database integrity: a column added to
  production but not to staging, a NOT NULL that became nullable via a hotfix,
  a dev-only index that made it to production. This skill compares two schema
  snapshots (DDL) and the LLM assesses the criticality of each drift.
sprint: 82
cluster: data
version: 1.0.0
author: AGENTS Skill Program
---

# schema-drift-tracker

Compare two SQL DDL schema snapshots, detect drifts (added/removed tables,
columns, indexes, foreign keys; modified types/nullability/defaults), assess
criticality via LLM, and produce a structured report.

## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## Usage

```
/schema-drift
```

The skill runs the collector script then invokes the LLM to classify each
drift entry and produce `schema-drift-report.md`.

## What You Must Do When Invoked

### Step 1

Run `/schema-drift` with the target project directory.

### Step 2

Review the drift report and assess criticality of each entry.

### Step 3

Document findings and recommend remediation steps.

## Parameters

| Parameter    | Position | Description                                    | Default                    |
|-------------|----------|------------------------------------------------|----------------------------|
| -ProjectDir | Mandatory| Base path for schema files or git checkout.    | -                          |
| -OldSchema  | Named    | Path (relative to ProjectDir) or git ref.      | `v1/schema.sql`            |
| -NewSchema  | Named    | Path (relative to ProjectDir) or git ref.      | `v2/schema.sql`            |

## LLM Analysis

Each drift entry from the collector is classified:

- **critical** - breaks existing queries (removed table, removed column,
  type narrowing)
- **major** - may break queries (renamed column, removed index, NOT NULL →
  nullable)
- **minor** - additive changes unlikely to break queries (new nullable column,
  new index)
- **info** - metadata changes (default value change, type widening)

## Output

- `schema-drift-report.md` - human-readable report per drift with severity
  and query-impact assessment.

## Files

```
skills/data/schema-drift-tracker/
  SKILL.md
  README.md
  scripts/
    drift-diff.ps1
  tests/
    fixtures/
      smoke/src/
        v1/schema.sql
        v2/schema.sql
      empty/.gitkeep
```
