---
name: analytics-query
description: Write or explain a SQL query against a schema the user gives, in their dialect, using the project's metric definitions when they exist, and name the traps — fan-out joins, time zones, nulls in filters. Use when the user needs a query to compute a metric or wants to understand one they have. Not for checking a reported number against data; see /analytics-number-check.
metadata:
  argument-hint: "<what to compute or the query> [project]"
---

# Query

Write, or explain, the SQL query in "$ARGUMENTS". Never run a query against a live database; the user runs it.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The schema: DDL, a column list or a sample of rows, and the SQL dialect (PostgreSQL, BigQuery, Snowflake, MySQL, SQLite, DuckDB); ask once for either if missing. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/analytics/` (create it when you write). With no project named: with exactly one folder there, use it; with several, ask which; with no folder at all, read none and continue.

Read `.singularskills/analytics/<project>/02-metrics.md` for the metric definitions when it exists.

## Process

1. **To write a query:** restate what it computes as a formula, following the `02-metrics.md` definition when the metric is defined there; then write the query in the named dialect, with a comment on each step. Prefer one CTE per step over nested subqueries.

2. **To explain a query:** walk through it clause by clause in plain words, then say what it actually computes and whether that matches what the user thinks it computes.

3. **Name the traps** that apply:
   - joins that fan out (one-to-many) and inflate sums or counts
   - time zones and day boundaries in date filters and grouping
   - nulls dropped by `WHERE col <> 'x'` or by inner joins
   - `COUNT(*)` versus `COUNT(DISTINCT …)`
   - integer division in ratios
   - averages of averages

4. **Check it with a small example:** when a sample of rows is given, compute the expected result for it with a script, so the user can compare with the query's result.

## Output

In chat: the query (or the explanation), the formula it computes, the traps that apply and how the query avoids them, and the expected result on the sample when one was given. This skill writes no file and runs nothing against a database.
