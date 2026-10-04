---
name: analyzing-tidb
description: |
  Use when working with Tidb — tiDB cluster topology, slow query analysis, hot
  region analysis, dashboard monitoring, and SQL optimization.
connection_type: tidb
preload: false
---

# TiDB Analysis Skill

Analyze and optimize TiDB clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated database/table names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. Cluster topology
mysql -h "$TIDB_HOST" -P "$TIDB_PORT" -u "$TIDB_USER" -p"$TIDB_PASSWORD" -e "SELECT * FROM information_schema.cluster_info;"

# 2. List databases
mysql -h "$TIDB_HOST" -P "$TIDB_PORT" -u "$TIDB_USER" -p"$TIDB_PASSWORD" -e "SHOW DATABASES;"

# 3. List tables
mysql -h "$TIDB_HOST" -P "$TIDB_PORT" -u "$TIDB_USER" -p"$TIDB_PASSWORD" -e "SHOW TABLES FROM my_database;"

# 4. Describe table (never assume column names)
mysql -h "$TIDB_HOST" -P "$TIDB_PORT" -u "$TIDB_USER" -p"$TIDB_PASSWORD" -e "DESCRIBE my_database.my_table;"

# 5. Check TiDB version
mysql -h "$TIDB_HOST" -P "$TIDB_PORT" -u "$TIDB_USER" -p"$TIDB_PASSWORD" -e "SELECT tidb_version();"
```

**Phase 1 outputs:**
- Cluster component topology (TiDB, TiKV, PD)
- Databases and tables
- Table schemas with confirmed column names

### Phase 2: Analysis (only after Phase 1)

Only reference databases, tables, and columns confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core TiDB query runner — always use this
tidb_query() {
    local query="$1"
    mysql -h "${TIDB_HOST:-localhost}" -P "${TIDB_PORT:-4000}" \
        -u "${TIDB_USER:-root}" -p"${TIDB_PASSWORD}" \
        -N -B -e "$query"
}

# PD API helper
pd_api() {
    local endpoint="$1"
    curl -s "http://${PD_HOST:-localhost}:2379/pd/api/v1/$endpoint"
}

# TiDB Dashboard API
tidb_dashboard() {
    local endpoint="$1"
    curl -s "http://${TIDB_HOST:-localhost}:10080/$endpoint"
}
```

## Anti-Hallucination Rules

- **NEVER reference a database or table** without confirming via SHOW commands
- **NEVER reference column names** without running DESCRIBE first
- **NEVER assume cluster topology** — always query `cluster_info`
- **NEVER guess store IDs** — always get from PD API
- **NEVER assume TiDB version features** — check version first

## Safety Rules

- **READ-ONLY ONLY**: Use only SELECT, SHOW, EXPLAIN, ADMIN SHOW, information_schema queries
- **FORBIDDEN**: DROP, ALTER, INSERT, UPDATE, DELETE, ADMIN commands that modify state without explicit user request
- **ALWAYS add `LIMIT`** to user table queries
- **Use `EXPLAIN ANALYZE`** carefully — it executes the query

## Common Operations

### Cluster Topology

```bash
#!/bin/bash
echo "=== Cluster Components ==="
tidb_query "SELECT TYPE, INSTANCE, STATUS_ADDRESS, VERSION, GIT_HASH FROM information_schema.cluster_info ORDER BY TYPE, INSTANCE;"

echo ""
echo "=== TiKV Stores ==="
pd_api "stores" | jq '.stores[] | {store_id: .store.id, address: .store.address, state_name: .store.state_name, capacity: .status.capacity, available: .status.available, region_count: .status.region_count}'

echo ""
echo "=== PD Members ==="
pd_api "members" | jq '.members[] | {name, peer_urls, client_urls, is_leader: .is_leader}'
```

### Slow Query Analysis

```bash
#!/bin/bash
echo "=== Slow Queries (last 1h) ==="
tidb_query "SELECT Time, Query_time, Process_time, Mem_max, Disk_max, SUBSTR(Query, 1, 100) as query_preview FROM information_schema.slow_query WHERE Time > DATE_SUB(NOW(), INTERVAL 1 HOUR) ORDER BY Query_time DESC LIMIT 20;"

echo ""
echo "=== Slow Query Statistics ==="
tidb_query "SELECT Digest_text, COUNT(*) as count, AVG(Query_time) as avg_time, MAX(Query_time) as max_time, AVG(Process_time) as avg_process FROM information_schema.slow_query WHERE Time > DATE_SUB(NOW(), INTERVAL 24 HOUR) GROUP BY Digest_text ORDER BY avg_time DESC LIMIT 15;"

echo ""
echo "=== Statements Summary ==="
tidb_query "SELECT DIGEST_TEXT, SUM_LATENCY, AVG_LATENCY, EXEC_COUNT, AVG_MEM, AVG_DISK FROM information_schema.statements_summary ORDER BY SUM_LATENCY DESC LIMIT 15;"
```

### Hot Region Analysis

```bash
#!/bin/bash
echo "=== Hot Read Regions ==="
pd_api "hotspot/regions/read" | jq '.as_peer[0:10] | .[] | {region_id: .region_id, store_id: .store_id, flow_bytes: .flow_bytes}'

echo ""
echo "=== Hot Write Regions ==="
pd_api "hotspot/regions/write" | jq '.as_peer[0:10] | .[] | {region_id: .region_id, store_id: .store_id, flow_bytes: .flow_bytes}'

echo ""
echo "=== Region Distribution ==="
pd_api "stats/region" | jq '{count, empty_count, storage_size, storage_keys}'
```

### Table Analysis

```bash
#!/bin/bash
DB="${1:-my_database}"
TABLE="${2:-my_table}"

echo "=== Table Stats ==="
tidb_query "SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH, INDEX_LENGTH FROM information_schema.tables WHERE TABLE_SCHEMA = '$DB' AND TABLE_NAME = '$TABLE';"

echo ""
echo "=== Table Regions ==="
tidb_query "SHOW TABLE $DB.$TABLE REGIONS;" | head -20

echo ""
echo "=== Index Stats ==="
tidb_query "SHOW STATS_HISTOGRAMS WHERE db_name = '$DB' AND table_name = '$TABLE';" 2>/dev/null
```

## Output Format

Present results as a structured report:
```
Analyzing Tidb Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Auto-increment hotspot**: Sequential auto-increment IDs cause write hotspots — use `AUTO_RANDOM` or SHARD_ROW_ID_BITS
- **GC lifetime**: Long transactions can block GC — check `tidb_gc_life_time`
- **Statistics staleness**: Stale stats cause bad query plans — check stats health
- **Region splitting**: Large tables may need manual region splitting — check region distribution
- **TiFlash vs TiKV**: TiFlash is columnar (analytics), TiKV is row (OLTP) — route queries appropriately
- **Pessimistic vs Optimistic**: Default is pessimistic locking since TiDB 4.0 — check transaction mode
