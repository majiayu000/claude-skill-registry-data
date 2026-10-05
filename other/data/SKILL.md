---
name: data
description: Use when raw data storage layer for 1ai-skills. Provides structured data
  persistence, query interface, and data pipeline support for skill operations. history.
  Use when working with data.
domain: meta
author: oyi77
license: Apache-2.0
subdomain: meta-skills
tags:
- data
- meta-learning
- self-improvement
- skill-evolution
persona:
  name: Database Architect
  expertise: SQLite, data modeling, query optimization
  philosophy: Data is the foundation of intelligence
version: 1.0.0
category: meta
---

# Data

## When to Use

**Trigger phrases:**
- "data"
- "Help me with data"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

```
record_execution - record one skill execution
/meta-datastore record-execution --skill seo-optimizer --latency 245 --success

# Query performance
/meta-datastore query "SELECT AVG(latency_ms) FROM skill_executions WHERE skill_name='seo-optimizer'"

# Get improvement candidates
/meta-datastore get-improvements --min-impact 0.7 --status proposed
```

## Code Examples

### Storing a skill execution record

```python
import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = "~/.1ai/data/store.sqlite"

def _expand_path(p: str) -> str:
    return p.replace("~", str(Path.home())) if "~" in p else p

def record_execution(skill_name: str, latency_ms: float, success: bool,
                     error_class: str = "", output_summary: str = "",
                     session_id: str = "") -> str:
    """Insert one skill execution record. Returns the execution_id."""
    ts = datetime.now(timezone.utc).isoformat()
    exec_id = hashlib.sha256(
        f"{skill_name}{ts}{latency_ms}".encode()
    ).hexdigest()[:16]
    conn = sqlite3.connect(_expand_path(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        conn.execute("""
            INSERT INTO skill_executions
                (execution_id, skill_name, timestamp, latency_ms,
                 success, error_class, output_summary, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (exec_id, skill_name, ts, latency_ms,
              1 if success else 0, error_class,
              output_summary[:200], session_id))
        conn.commit()
    finally:
        conn.close()
    return exec_id

# record_execution("seo-optimizer", 245.0, True, session_id="sess_abc123")
```

### Querying average latency by skill

```python
def avg_latency_by_skill(skill_name: str, days: int = 7) -> float | None:
    """Return average execution latency in ms for a skill over N days."""
    conn = sqlite3.connect(_expand_path(DB_PATH))
    try:
        row = conn.execute("""
            SELECT AVG(latency_ms) FROM skill_executions
            WHERE skill_name = ?
              AND timestamp >= datetime('now', ?)
        """, (skill_name, f"-{days} days")).fetchone()
        return round(row[0], 2) if row and row[0] else None
    finally:
        conn.close()

# p50 = avg_latency_by_skill("seo-optimizer")
# print(f"7-day avg latency: {p50}ms")
```

### Retrieving improvement candidates with high impact

```python
def get_candidates(min_impact: float = 0.7, status: str = "proposed"):
    """Fetch improvement candidates above a minimum impact score."""
    conn = sqlite3.connect(_expand_path(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("""
            SELECT skill_name, title, impact_score, effort_score,
                   status, created_at
            FROM improvement_candidates
            WHERE impact_score >= ? AND status = ?
            ORDER BY impact_score DESC
        """, (min_impact, status)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

# improvements = get_candidates(0.7, "proposed")
# for c in improvements:
#     print(f"{c['skill_name']}: {c['title']} (impact={c['impact_score']})")
```


### Integration

Connects to:
- performance-monitor (writes metrics)
- feedback-collector (stores feedback)
- pattern-recognition (queries patterns)
- skill-evolution (tracks versions)


## When NOT to Use

- When the skill is stable and not changing
- For skills with fewer than 10 invocations (not enough data)
- When manual curation produces better results


## Overview

Data is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

It serves as the persistence backbone for the entire 1ai-skills ecosystem: execution metrics, feedback records, improvement proposals, and skill version histories all flow through the data skill's SQLite-backed store. Without it, the self-improvement loop that drives skill evolution would have no memory.

### Storage Model

The data layer uses a hybrid architecture. A primary SQLite database holds structured records — skill execution entries, latency metrics, success/failure counts, feedback items, and improvement candidates. Each record is tagged with skill name, timestamp, and execution context for precise querying. Read-heavy dashboards and trend queries are served by materialized aggregation tables refreshed on write.

### Lifecycle

Data enters through instrumentation hooks embedded in every skill's execution path. The payload is validated against a schema, enriched with session metadata, and committed transactionally. A background maintenance process periodically compacts old records, prunes data beyond the retention window (90 days for raw execution logs, 18 months for aggregated metrics), and updates summary tables. This keeps the store lean while preserving historical trends.

## Workflow

1. **Define Schema** — Establish the record format for each data type (skill execution, feedback, improvement candidate). Declare columns, types, indexes, and constraints in a schema registry before any data flows.
2. **Collect Instrumentation** — Hooks at skill entry/exit points emit structured payloads: skill name, duration, success/failure, error class, input hash, and output summary. Payloads are batched and sent to the data store asynchronously.
3. **Validate and Normalize** — Incoming records are checked against schema rules. Malformed entries are rejected with a detailed error logged. Valid records are normalized — timestamps converted to UTC, enums standardized to lowercase, null fields filled with sensible defaults.
4. **Store Transactionally** — Records are inserted in a single SQLite transaction per batch. WAL journal mode allows concurrent reads during writes. Duplicate detection uses a composite key of (skill_name, timestamp, execution_id).
5. **Index and Aggregate** — After each write batch, summary tables are updated: rolling 7-day averages, p50/p95/p99 latency percentiles, and hourly/daily success rates. Indexes on (skill_name, timestamp) enable fast filtered queries.
6. **Query and Analyze** — The query layer exposes parameterized SQL and convenience methods: average latency by skill, success rate over time, top-N slowest executions, improvement impact scores, and trend direction indicators.
7. **Archive and Prune** — A scheduled maintenance job rotates raw data beyond the retention window to a compressed cold-storage archive, then deletes the source rows. Aggregated summaries are compacted into weekly/monthly rollups before the raw rows are dropped.


## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for skill management
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

### Database Schema

The core schema includes these tables:

- **skill_executions** — One row per skill invocation. Columns: skill_name, timestamp, latency_ms, success (boolean), error_class, input_hash, output_summary, session_id, execution_id. Indexed on (skill_name, timestamp) for time-series range queries.
- **feedback_items** — Linked to executions. Columns: execution_id (FK), feedback_type (success/failure/suggestion/issue), score (1-5), detail_text, source, created_at.
- **improvement_candidates** — Generated improvement proposals. Columns: skill_name, title, description, impact_score (0.0-1.0), effort_score (0.0-1.0), status (proposed/approved/implemented/rejected/rolled_back), evidence_path, created_at, implemented_at.
- **skill_versions** — Version tracking per skill. Columns: skill_name, version, checksum (SHA-256 of SKILL.md), lines_count, summary, deployed_at.
- **aggregations** — Materialized summary data. Columns: skill_name, period_type (hourly/daily/weekly), period_start, total_executions, avg_latency, p50_latency, p95_latency, p99_latency, success_rate, failure_count, created_at.

### Data Integrity

Foreign keys are enforced when the source system guarantees referential integrity. All timestamp columns use ISO-8601 text format for portability. A checksum column on each raw execution row detects corruption during archival and restore. Schema migrations use a versioned migration table with forward-only numeric IDs and a rollback script per migration.


## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

### Data-Specific Configuration

- **DATA_DB_PATH** — Path to the primary SQLite database file. Default: `~/.1ai/data/store.sqlite`.
- **DATA_RETENTION_DAYS** — Days to retain raw execution logs before archival. Default: 90.
- **DATA_AGGREGATION_RETENTION_DAYS** — Days to retain aggregated summaries. Default: 547 (18 months).
- **DATA_WAL_MODE** — Enable SQLite WAL journal mode for concurrent read/write. Default: true.
- **DATA_BATCH_SIZE** — Number of records per insert transaction. Default: 100.
- **DATA_AUTO_MAINTENANCE** — Enable automatic pruning and compaction on startup. Default: true.
- **DATA_COLD_STORAGE_PATH** — Path for compressed archives of pruned raw data. Default: `~/.1ai/data/archive/`.


## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Common Issues and Troubleshooting

| Issue | Root Cause | Solution |
|---|---|---|
| `sqlite3.OperationalError: database is locked` | Concurrent write contention on the same database file. | Enable WAL mode (`DATA_WAL_MODE=true`). Batch writes into transactions. Retry with exponential backoff. |
| Query latency degrades over time | Missing indexes on frequently filtered columns. | Run `ANALYZE` after bulk inserts. Verify query plans with `EXPLAIN QUERY PLAN`. Add composite indexes for common WHERE patterns. |
| Disk usage grows unbounded | Raw data exceeding the retention window before archival runs. | Lower `DATA_RETENTION_DAYS`. Increase `DATA_AUTO_MAINTENANCE` frequency. Enable aggressive cold-storage compression. |
| Schema migration conflicts | Concurrent process instances applying migrations at different versions. | Use a migration lock table with advisory lock. Make migrations idempotent. Avoid concurrent migration runs. |
| Corrupted database file | Unexpected power loss or filesystem error during write. | Enable `PRAGMA integrity_check` on startup. Maintain hourly WAL checkpoints. Keep the most recent automated backup. |
| `UNIQUE constraint` failed on insert | Duplicate execution_id or composite key collision. | Use `INSERT OR IGNORE` for idempotent inserts. Verify the caller generates unique execution IDs per batch. |
| Aggregation tables stale after write | Maintenance job runs on a fixed schedule, not after every batch. | Trigger aggregation refresh on write via a callback. Reduce the aggregation interval to 5 minutes. |


## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Data Analytics Service | 2-4 weeks | Offer skill execution analytics as a paid service for teams running custom skill sets. Provide dashboards for latency trends, failure rates, and improvement velocity. |
| Benchmark Reports | 1-2 weeks | Generate comparative performance benchmarks across skill categories. Sell as one-off reports to enterprise users evaluating the ecosystem. |
| Managed Data Pipeline | 4-8 weeks | Deploy the data storage layer as a managed cloud service with replication, automated backups, and SLA-backed availability. Charge per-skill per-month. |
| Anomaly Detection Add-on | 3-6 weeks | Build anomaly detection on top of historical execution data — flag skills whose latency or failure rate deviates significantly from their baseline. License as an add-on module. |
| Migration Consulting | Per engagement | Help teams migrate from ad-hoc logging to the structured data layer. Includes schema design, data migration scripts, and integration with existing instrumentation. |


## Process
### Preparation

- Identify the data types that need persistence: execution metrics, feedback, versions, improvement candidates.
- Define schema for each type: columns, types, constraints, indexes, default values.
- Set up the SQLite database file and run initial migrations to create all tables.
- Configure retention policies and archival paths before the first write.
- Instrument the calling code with entry/exit hooks that emit structured payloads.

### Execution

- Route incoming data payloads through the validation layer before any write.
- Use batched transactions with WAL mode for write performance.
- Update aggregation tables after each batch to keep summary queries fast.
- Run the query interface for analysis: latency percentiles, success rates, trend detection.
- Schedule maintenance tasks (pruning, compaction, backup) via cron or the built-in scheduler.

### Stewardship

- Monitor database file size daily. Sudden growth indicates a retention policy gap.
- Run `PRAGMA integrity_check` weekly to detect corruption early.
- Test restore from cold-storage archives monthly.
- Review query patterns quarterly and add or remove indexes accordingly.
- Keep a migration log with timestamps and rollback instructions for every schema change.


## Verification
- [ ] Retention policies enforced — no stale data beyond configured window
- [ ] Aggregation tables match raw data totals (spot-check with COUNT queries)
- [ ] Backup created before any schema migration
- [ ] Query response time under 100ms for 95th percentile on indexed queries
- [ ] Error paths produce actionable log messages, not silent failures

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Skills do not need to evolve" | Static skills become outdated. Self-evolving skills improve continuously. |
| "Manual skill management is fine" | With 1000+ skills, manual management is impossible. Automate. |
| "Performance does not matter" | Skill performance directly impacts agent effectiveness. Track it. |
| "More data always helps" | Uncurated records inflate storage and slow queries. Only collect what drives decisions. |
| "SQLite cannot scale" | WAL mode + batched transactions sustain 10K+ writes/s on a single file for skill-store workloads. |
| "Schema design is over-engineering" | A poorly normalized schema causes migration pain for every new data type. Invest up front. |


