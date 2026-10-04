---
name: kit-performance
description: Performance guardrails pack — N+1, complexity notes, measure-before/after, unbounded growth, pagination, hot-path I/O. Use when asked for a performance pass or when optimizing/reviewing query and loop cost.
---

Read and apply to the current task, citing rule IDs/rows with one line of evidence as they fire:
- docs/guardrails/PERFORMANCE.md — PERF1–PERF6 (PERF3: no speed claim without before/after numbers)
- docs/guardrails/TRAPS-SQL.md — "Indexes, types, pagination" rows
- docs/guardrails/TRAPS-NOSQL.md — Redis rows (SCAN, TTL)
