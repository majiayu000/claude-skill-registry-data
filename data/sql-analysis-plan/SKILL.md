---
name: sql-analysis-plan
description: Plan SQL analyses without assuming direct database access. Use when Codex is asked to design SQL queries, outline joins, filters, CTEs, aggregations, validation checks, or data quality steps for analytics and BI questions.
license: MIT
---

# SQL Analysis Plan

## Core Workflow

1. Identify business question, grain, tables, fields, filters, time window,
   segments, and expected output.
2. Outline query logic with joins, CTEs, aggregations, window functions, and
   validation checks.
3. Define data quality checks for duplicates, missing values, timezone, late
   events, and source mismatches.
4. Include expected result shape and interpretation caveats.
5. Keep database access read-only unless the user explicitly approves otherwise.
6. Flag missing schema information before writing final SQL.

## Safety Rules

- Do not run write queries, destructive queries, or production-impacting
  operations.
- Do not invent table or field names when schema is missing.
- Do not expose sensitive data in query output examples.

## Deliverable Shape

For SQL analysis plans, provide:

- Business question
- Tables and fields needed
- Query outline
- Filters and segments
- Validation checks
- Expected output shape
- Caveats and assumptions
- Optional SQL draft when schema is known

## References

- Read `references/sql-analysis-plan-checklist.md` when planning analytics SQL.
