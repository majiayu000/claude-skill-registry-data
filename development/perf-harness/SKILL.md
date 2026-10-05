---
name: creo-perf-harness
description: >
  Tooling for the creo-perf skill: deterministic benchmark scripts (scenario
  captures with EXPLAIN medians and p50/p95 HTTP loops, Lighthouse initial-load
  audit, platform and schema audits, pg_stat_statements workload discovery,
  auto-rebuilt before/after dashboard) plus the project scaffolder used by
  /creo perf init. Not invoked directly; creo-perf routes to it.
allowed-tools:
  - Read
  - Bash
---

# creo-perf-harness

This directory holds the executable half of the `creo-perf` skill. It has no
commands of its own: `/creo perf ...` loads `creo-perf` (the playbook), which
runs these scripts.

| Script | Role |
|---|---|
| `scripts/init-project.sh` | scaffold `.claude/skills/creo-perf/` in a project from `templates/` |
| `scripts/preflight.sh` | tools, targets, scenarios, SQL mode sanity |
| `scripts/audit-all.sh <label>` | every capture in the configured order + workload window |
| `scripts/audit-scenario.sh <id> <label>` | one scenario: EXPLAIN medians, HTTP loops, wire bytes, ETag replay, FE probe |
| `scripts/audit-fe.sh <label>` | served assets, production build, bundle composition, Lighthouse xN |
| `scripts/audit-platform.sh <label>` | backend process facts + PostgreSQL settings (context, not metrics) |
| `scripts/audit-schema.sh <label>` | tables, columns, indexes, hypopg verdicts, PostGIS shape |
| `scripts/observability-setup.sh` | pg_stat_statements + auto_explain (+hypopg); restarts the DB |
| `scripts/workload-{pre,drive,post}.sh` | discovery window: reset, drive scenario traffic, rank hot queries |
| `scripts/common/build-dashboard.py` | pivot all captures into `results/dashboard.md` with deltas |
| `scripts/common/sql-runners.py` | psql runner files from hand-written SQL (compile) or real app code (record) |
| `scripts/common/fe-interactions.mjs` | Playwright interaction probe: requests fired, rows held, long tasks |

Every script reads the project's `.claude/skills/creo-perf/perf.config.sh`.
See `README.md` for requirements and `creo-perf/references/scenario-spec.md`
for the scenario file contract.
