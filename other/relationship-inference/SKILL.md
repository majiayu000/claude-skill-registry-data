---
name: relationship-inference
description: "Relationship inference: scans DDL and code for missing foreign key relationships, infers relationships from naming patterns and query join patterns, and validates each inference against business logic. Read-only. Audience: Senior. Trigger: /infer-rels"
trigger: /infer-rels
---

## What this is for

Most production databases have missing FK constraints - dropped for performance,
never declared in the first place, or only implied by naming conventions
(order.customer_id -> customer.id). This skill infers relationships from naming
patterns + query join patterns + ORM relation declarations, then the LLM
validates each inference against business logic.

The dominant failure mode is the implicit relationship that nobody documented,
leading to orphaned data, broken queries, and confused developers.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/relation-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each candidate:

### Step 5

- Read the `evidence` (naming, join, orm) and `confidence` score.

### Step 6

- Is this a real business relationship? What is its cardinality?

### Step 7

- Is there a reason it was not declared as FK (performance, cross-schema, legacy)?

### Step 8

- Should it be promoted to a declared FK?

### Step 9

5. Confidence: `proven` (declared FK), `likely` (naming + join evidence),

### Step 10

`suspected` (naming only).

### Step 11

6. Write `relationship-report.md` to the working directory.

## Usage

```
/infer-rels                         # interactive, prompts for directory
/infer-rels <dir>                   # scan project directory
/infer-rels -help                   # show usage
```

Returns JSON with `declaredFKs[]` and `inferredCandidates[]`: each candidate
entry `{fromCol, fromTable, toCol, toTable, evidence, confidence}`.

## Report Format

`relationship-report.md` with:
- Executive summary (declared FKs vs inferred candidates)
- Declared relationships (baseline)
- Inferred candidates (naming + join evidence)
- Ambiguous candidates (naming only, needs review)
- Recommendation matrix (promote to FK / leave as-is / investigate)
- Confidence column for every finding
- Open questions (suspected, needs human review)
