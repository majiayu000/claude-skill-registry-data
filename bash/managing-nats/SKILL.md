---
name: managing-nats
description: |
  Use when working with Nats — nATS subject management, JetStream stream
  configuration, consumer status, cluster health, and message flow analysis.
connection_type: nats
preload: false
---

# NATS Management Skill

Analyze and manage NATS clusters with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated stream/consumer names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. Server info
nats server info --server "$NATS_URL"

# 2. Account info
nats account info --server "$NATS_URL"

# 3. List JetStream streams
nats stream list --server "$NATS_URL"

# 4. List consumers for a stream
nats consumer list MY_STREAM --server "$NATS_URL"

# 5. Stream info
nats stream info MY_STREAM --server "$NATS_URL"
```

**Phase 1 outputs:**
- Server version and cluster info
- JetStream streams and consumers
- Stream subjects and message counts

### Phase 2: Analysis (only after Phase 1)

Only reference streams, consumers, and subjects confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core NATS CLI helper — always use this
nats_cmd() {
    nats --server "${NATS_URL:-nats://localhost:4222}" "$@"
}

# NATS monitoring API
nats_monitor() {
    local endpoint="$1"
    curl -s "http://${NATS_MONITOR_HOST:-localhost}:8222/$endpoint"
}
```

## Anti-Hallucination Rules

- **NEVER reference a stream** without confirming via `nats stream list`
- **NEVER reference a consumer** without confirming via `nats consumer list`
- **NEVER assume subject names** — always check stream configuration
- **NEVER guess cluster size** — always check server info
- **NEVER assume JetStream is enabled** — verify with account info

## Safety Rules

- **READ-ONLY ONLY**: Use only info, list, report, server commands, monitoring API GET
- **FORBIDDEN**: stream add/edit/delete, consumer add/delete, pub without explicit user request
- **NEVER subscribe to production subjects** for analysis — use monitoring endpoints
- **Use `nats server report`** for cluster-wide analysis

## Common Operations

### Cluster Health Overview

```bash
#!/bin/bash
echo "=== Server Info ==="
nats_cmd server info --json | jq '{server_id, version, go, host, port, max_payload, proto, jetstream, cluster: .connect_urls}'

echo ""
echo "=== Server List ==="
nats_cmd server list

echo ""
echo "=== Account Info ==="
nats_cmd account info --json | jq '{memory, storage, streams, consumers, api: {total, errors}}'

echo ""
echo "=== Connection Report ==="
nats_cmd server report connections
```

### JetStream Stream Analysis

```bash
#!/bin/bash
echo "=== Streams ==="
nats_cmd stream list --json | jq '.[] | {name: .config.name, subjects: .config.subjects, messages: .state.messages, bytes: .state.bytes, consumers: .state.consumer_count, retention: .config.retention, storage: .config.storage}'

echo ""
echo "=== Stream Details ==="
STREAM="${1:-MY_STREAM}"
nats_cmd stream info "$STREAM" --json | jq '{config: {name: .config.name, subjects: .config.subjects, retention: .config.retention, max_msgs: .config.max_msgs, max_bytes: .config.max_bytes, max_age: .config.max_age, replicas: .config.num_replicas}, state: .state}'

echo ""
echo "=== Stream Report ==="
nats_cmd stream report
```

### Consumer Status

```bash
#!/bin/bash
STREAM="${1:-MY_STREAM}"

echo "=== Consumers for $STREAM ==="
nats_cmd consumer list "$STREAM" --json | jq '.[] | {name: .config.name, durable_name: .config.durable_name, deliver_policy: .config.deliver_policy, ack_policy: .config.ack_policy, num_pending: .num_pending, num_redelivered: .num_redelivered, num_ack_pending: .num_ack_pending}'

echo ""
echo "=== Consumer Details ==="
CONSUMER="${2:-MY_CONSUMER}"
nats_cmd consumer info "$STREAM" "$CONSUMER" --json | jq '{config, delivered: .delivered, ack_floor: .ack_floor, num_pending, num_redelivered, num_ack_pending}'

echo ""
echo "=== Consumer Report ==="
nats_cmd consumer report "$STREAM"
```

### Monitoring Endpoints

```bash
#!/bin/bash
echo "=== Varz (general stats) ==="
nats_monitor "varz" | jq '{server_id, version, uptime, mem, cpu, connections, total_connections, subscriptions, slow_consumers, in_msgs, out_msgs, in_bytes, out_bytes}'

echo ""
echo "=== Connz (connections) ==="
nats_monitor "connz?sort=msgs_to&limit=10" | jq '.connections[] | {cid, name, ip, subscriptions, msgs_to, msgs_from, bytes_to, bytes_from, uptime}'

echo ""
echo "=== Routez (cluster routes) ==="
nats_monitor "routez" | jq '.routes[]? | {rid, remote_id, ip, port, in_msgs, out_msgs}' 2>/dev/null

echo ""
echo "=== JetStream Info ==="
nats_monitor "jsz" | jq '{server_id, config, streams, consumers, messages, bytes, api: {total, errors}}'
```

## Output Format

Present results as a structured report:
```
Managing Nats Report
════════════════════
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

- **Core NATS vs JetStream**: Core NATS is fire-and-forget; JetStream provides persistence — know which you need
- **Consumer ack pending**: High ack_pending means consumers are slow — check max_ack_pending limits
- **Stream retention**: Limits (max_msgs, max_bytes, max_age) silently discard old messages
- **Slow consumers**: NATS disconnects slow consumers — monitor slow_consumers metric
- **Subject wildcards**: `>` matches all remaining tokens; `*` matches one token — test patterns carefully
- **Redelivery loops**: Messages failing ack cause redelivery — set max_deliver to prevent infinite loops
