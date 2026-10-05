---
name: sql-analytics-workflow
description: "Design, review, debug, or explain analytical SQL with correct grain, joins, filters, time logic, performance awareness, and validation. Use for SQL analysis, writing or debugging a query, metric SQL, warehouse queries, cohorts, or database reporting. Turkish triggers: SQL analizi, sorgu yaz veya düzelt, veri modeli ve metrik mantığını doğrula."
---

# SQL Analytics Workflow

Make the question and row grain explicit before writing SQL.

1. Confirm dialect, tables, field meaning, row grain, time zone, and access boundaries.
2. Write a plain-language query contract: population, filters, joins, grouping, metric, and expected row count.
3. Build incrementally: inspect a small sample, validate joins, check duplicated entities, then aggregate.
4. Parameterize dates and document assumptions. Prefer safe read-only queries unless writes are explicitly authorized.
5. Validate totals against an independent small check and report limitations.

Do not execute destructive SQL, expose secrets, or assume dialect-specific functions. Flag PII and large-scan cost risks before execution.
