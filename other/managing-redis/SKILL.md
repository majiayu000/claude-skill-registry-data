---
name: managing-redis
description: |
  Use when working with Redis — redis in-memory data store analysis, performance
  monitoring, memory optimization, and key management. Covers memory usage
  analysis, keyspace inspection, slow log investigation, replication health,
  cluster status, eviction policy review, and connection management. Read this
  skill before any Redis operations — it enforces discovery-first patterns,
  anti-hallucination rules, and safety constraints.
connection_type: redis
preload: false
---

# Redis Management Skill

Monitor, analyze, and optimize Redis instances safely.

## MANDATORY: Discovery-First Pattern

**Always run `INFO ALL` and `DBSIZE` before any key inspection. Never guess key patterns.**

### Phase 1: Discovery

```bash
#!/bin/bash

redis_cmd() {
    redis-cli -h "$REDIS_HOST" -p "${REDIS_PORT:-6379}" \
              ${REDIS_PASSWORD:+-a "$REDIS_PASSWORD"} \
              --no-auth-warning "$@"
}

echo "=== Redis Server Info ==="
redis_cmd INFO server | grep -E 'redis_version|uptime_in_days|tcp_port|config_file'

echo ""
echo "=== Memory Overview ==="
redis_cmd INFO memory | grep -E 'used_memory_human|used_memory_peak_human|maxmemory_human|mem_fragmentation_ratio|maxmemory_policy'

echo ""
echo "=== Keyspace ==="
redis_cmd INFO keyspace

echo ""
echo "=== Database Sizes ==="
for db in $(redis_cmd INFO keyspace | grep -o 'db[0-9]*' | sort -u); do
    redis_cmd SELECT "${db#db}" > /dev/null 2>&1
    count=$(redis_cmd DBSIZE)
    echo "$db: $count keys"
done

echo ""
echo "=== Clients ==="
redis_cmd INFO clients
```

**Phase 1 outputs:** Key count per database, memory usage, version, keyspace namespaces

### Phase 2: Analysis

Only query key patterns confirmed in Phase 1 keyspace output.

## Anti-Hallucination Rules

- **NEVER assume key names** — always use `SCAN` with patterns from Phase 1 discovery
- **NEVER use `KEYS *`** — this blocks Redis for the entire scan on large keyspaces
- **NEVER assume TTLs** — always check with `TTL key_name`
- **NEVER assume data types** — always `TYPE key_name` before accessing
- **ALWAYS use `SCAN`** over `KEYS` — `KEYS *` is O(N) blocking

## Safety Rules

- **READ-ONLY by default**: Use INFO, SCAN, TYPE, TTL, OBJECT, DEBUG OBJECT
- **FORBIDDEN without explicit request**: FLUSHDB, FLUSHALL, DEL, UNLINK, CONFIG SET
- **SCAN in batches**: Use `COUNT 100` with SCAN — never large COUNT values on production
- **AVOID `KEYS *`**: Always blocked in production — use `SCAN 0 COUNT 100` instead
- **Large value safety**: Use `STRLEN` or `LLEN` before retrieving entire values

## Core Helper Functions

```bash
#!/bin/bash

redis_cmd() {
    redis-cli -h "$REDIS_HOST" -p "${REDIS_PORT:-6379}" \
              ${REDIS_PASSWORD:+-a "$REDIS_PASSWORD"} \
              --no-auth-warning "$@"
}

# Safe key scanner (uses SCAN, never KEYS *)
scan_keys() {
    local pattern="${1:-*}"
    local db="${2:-0}"
    local limit="${3:-100}"
    redis_cmd -n "$db" SCAN 0 MATCH "$pattern" COUNT "$limit" | tail -n +2
}

# Get key info without fetching value
key_info() {
    local key="$1"
    local db="${2:-0}"
    local type=$(redis_cmd -n "$db" TYPE "$key")
    local ttl=$(redis_cmd -n "$db" TTL "$key")
    local size=$(redis_cmd -n "$db" OBJECT ENCODING "$key" 2>/dev/null)
    echo "$key | type=$type | ttl=${ttl}s | encoding=$size"
}
```

## Common Operations

### Memory Analysis

```bash
#!/bin/bash
echo "=== Memory Usage Summary ==="
redis_cmd INFO memory | awk -F: '{
    if ($1 == "used_memory_human") print "Used:", $2
    if ($1 == "used_memory_peak_human") print "Peak:", $2
    if ($1 == "maxmemory_human") print "Max:", $2
    if ($1 == "mem_fragmentation_ratio") print "Fragmentation:", $2
    if ($1 == "maxmemory_policy") print "Eviction policy:", $2
}'

echo ""
echo "=== Top Keys by Memory (sample from db0) ==="
# Use OBJECT FREQ (LFU) or OBJECT IDLETIME for access patterns
redis_cmd -n 0 MEMORY USAGE --help > /dev/null 2>&1 && \
    redis_cmd -n 0 SCAN 0 COUNT 100 | tail -n +2 | while read key; do
        size=$(redis_cmd -n 0 MEMORY USAGE "$key" 2>/dev/null)
        echo "${size:-0} $key"
    done | sort -rn | head -10 || echo "MEMORY USAGE command not available (Redis < 4.0)"

echo ""
echo "=== Eviction Stats ==="
redis_cmd INFO stats | grep -E 'evicted_keys|expired_keys|keyspace_hits|keyspace_misses'

echo ""
echo "=== Hit Rate ==="
redis_cmd INFO stats | awk -F: '
    /keyspace_hits/ { hits=$2 }
    /keyspace_misses/ { misses=$2 }
    END {
        total = hits + misses
        if (total > 0) printf "Hit rate: %.1f%% (%s hits, %s misses)\n", hits/total*100, hits, misses
    }'
```

### Slow Log Analysis

```bash
#!/bin/bash
echo "=== Slow Log Config ==="
redis_cmd CONFIG GET slowlog-log-slower-than
redis_cmd CONFIG GET slowlog-max-len

echo ""
echo "=== Recent Slow Commands ==="
redis_cmd SLOWLOG GET 20 | awk '
    /^[0-9]+\)$/ { entry++ }
    /[0-9]+\) \(integer\)/ {
        if (entry % 4 == 1) id=$3
        if (entry % 4 == 2) ts=strftime("%Y-%m-%d %H:%M:%S", $3)
        if (entry % 4 == 3) { us=$3; printf "%s | %dms | ", ts, us/1000 }
    }
' 2>/dev/null

# Better format using SLOWLOG GET
redis_cmd SLOWLOG GET 20 | python3 -c "
import sys, datetime
lines = sys.stdin.read().strip().split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.isdigit() or (line.endswith(')') and i == 0):
        if i + 3 < len(lines):
            ts_line = lines[i+2] if i+2 < len(lines) else ''
            us_line = lines[i+3] if i+3 < len(lines) else ''
            print(f'Entry {line}: {ts_line.strip()}, latency: {us_line.strip()} us')
    i += 1
" 2>/dev/null || redis_cmd SLOWLOG GET 10
```

### Connection Analysis

```bash
#!/bin/bash
echo "=== Client Connections ==="
redis_cmd INFO clients

echo ""
echo "=== Connected Clients by IP ==="
redis_cmd CLIENT LIST | awk -F'[ =]' '{for(i=1;i<=NF;i++) if($i=="addr") print $(i+1)}' | \
    cut -d: -f1 | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== Clients in Blocked State ==="
redis_cmd CLIENT LIST | grep -E 'flags=.*b' | wc -l | xargs -I{} echo "Blocked clients: {}"

echo ""
echo "=== Max Clients Config ==="
redis_cmd CONFIG GET maxclients
```

### Keyspace Analysis

```bash
#!/bin/bash
DB_NUM="${1:-0}"
KEY_PATTERN="${2:-*}"

echo "=== Keyspace Stats for DB $DB_NUM ==="
redis_cmd -n "$DB_NUM" INFO keyspace

echo ""
echo "=== Key Type Distribution (sampling 500 keys) ==="
redis_cmd -n "$DB_NUM" SCAN 0 COUNT 500 | tail -n +2 | while read key; do
    redis_cmd -n "$DB_NUM" TYPE "$key"
done | sort | uniq -c | sort -rn

echo ""
echo "=== Keys with No Expiry (first 100) ==="
expired=0; total=0
cursor=0
while true; do
    result=$(redis_cmd -n "$DB_NUM" SCAN "$cursor" MATCH "$KEY_PATTERN" COUNT 100)
    cursor=$(echo "$result" | head -1)
    keys=$(echo "$result" | tail -n +2)
    for key in $keys; do
        total=$((total+1))
        ttl=$(redis_cmd -n "$DB_NUM" TTL "$key")
        [ "$ttl" = "-1" ] && expired=$((expired+1))
        [ "$total" -ge 100 ] && break 2
    done
    [ "$cursor" = "0" ] && break
done
echo "Keys without TTL: $expired out of $total sampled"
```

### Replication Health

```bash
#!/bin/bash
echo "=== Replication Info ==="
redis_cmd INFO replication

echo ""
echo "=== Replication Lag ==="
redis_cmd INFO replication | awk -F: '
    /role/ { print "Role:", $2 }
    /connected_slaves/ { print "Slaves:", $2 }
    /master_last_io_seconds_ago/ { print "Last sync:", $2, "sec ago" }
    /slave_repl_offset/ { print "Slave offset:", $2 }
    /master_repl_offset/ { print "Master offset:", $2 }
'
```

### Cluster Status

```bash
#!/bin/bash
echo "=== Cluster Status ==="
redis_cmd CLUSTER INFO 2>/dev/null | grep -E 'cluster_enabled|cluster_state|cluster_slots_ok|cluster_known_nodes' || echo "Cluster mode not enabled"

echo ""
echo "=== Cluster Nodes ==="
redis_cmd CLUSTER NODES 2>/dev/null | awk '{print $1, $2, $3, $9}' || echo "Standalone mode"
```

### Performance Metrics

```bash
#!/bin/bash
echo "=== Operations Per Second ==="
# Sample stats 5 seconds apart
redis_cmd INFO stats | grep total_commands_processed | awk -F: '{print "Start:", $2}'
sleep 5
redis_cmd INFO stats | grep total_commands_processed | awk -F: '{print "After 5s:", $2}'

echo ""
echo "=== Persistence Stats ==="
redis_cmd INFO persistence | grep -E 'rdb_last_save_time|rdb_last_bgsave_status|aof_enabled|aof_current_size'

echo ""
echo "=== Network Stats ==="
redis_cmd INFO stats | grep -E 'total_net_input_bytes|total_net_output_bytes|instantaneous_ops_per_sec|instantaneous_input_kbps'
```

## Output Format

Present results as a structured report:
```
Managing Redis Report
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

- **`KEYS *` is O(N) blocking**: NEVER use on production — always `SCAN` with small COUNT
- **Password in command line**: The `-a` flag may appear in `ps` output — use `REDISCLI_AUTH` env var in production scripts
- **`DEBUG SLEEP`**: Never run on production — it blocks all clients
- **Memory fragmentation > 1.5**: Indicates Redis needs restart with `CONFIG SET activedefrag yes` (Redis 4+)
- **`OBJECT FREQ`**: Only available when `maxmemory-policy` is set to `allkeys-lfu` or `volatile-lfu`
- **Cluster vs standalone**: Many commands differ — always check `CLUSTER INFO` in Phase 1
- **Sentinel vs cluster**: Different failover mechanisms — check `INFO server` for mode
- **Large LRANGE/SMEMBERS**: Always check `LLEN`/`SCARD` before fetching — collections can have millions of items
