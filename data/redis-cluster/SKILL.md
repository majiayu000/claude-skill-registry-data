---
name: redis-cluster
description: Master Redis Cluster - horizontal scaling, hash slots, resharding, cluster management, and distributed architecture
sasmp_version: "1.3.0"
bonded_agent: 06-redis-clustering
bond_type: PRIMARY_BOND

# Production Configuration
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  cluster_operation:
    type: string
    required: true
    enum: [create, add_node, remove_node, reshard, rebalance, failover]
  node_count:
    type: integer
    required: false
    min: 6
    description: Minimum 6 nodes for production (3 masters + 3 replicas)
  replicas_per_master:
    type: integer
    required: false
    default: 1
    min: 1
    max: 3

# Retry Configuration
retry_config:
  max_retries: 5
  backoff_strategy: exponential
  backoff_base_ms: 2000
  retryable_errors:
    - CLUSTERDOWN
    - MOVED
    - ASK
    - connection_timeout

# Observability
observability:
  logging:
    level: info
    log_redirects: true
  metrics:
    - cluster_state
    - slots_assigned
    - nodes_ok
    - replication_lag_ms

# Validation Rules
validation:
  cluster_health:
    all_slots_covered: true
    min_replicas_per_master: 1
  operations:
    require_backup_before_reshard: true
---

# Redis Cluster Skill

## Overview

Production-grade Redis Cluster management for horizontal scaling. Master hash slot distribution, node management, resharding, and failover procedures.

## Cluster Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REDIS CLUSTER (16384 Hash Slots)                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   Master 1   │  │   Master 2   │  │   Master 3   │               │
│  │ Slots 0-5460 │  │ Slots 5461-  │  │ Slots 10923- │               │
│  │  :6379       │  │   10922      │  │    16383     │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                       │
│         ▼                 ▼                 ▼                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │  Replica 1   │  │  Replica 2   │  │  Replica 3   │               │
│  │  :6380       │  │  :6381       │  │  :6382       │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                     │
│  Key Routing: CRC16(key) % 16384 → Slot → Master                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Cluster Creation

### Prerequisites
```bash
# Each node's redis.conf
port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```

### Create Cluster
```bash
# Create 6-node cluster (3 masters + 3 replicas)
redis-cli --cluster create \
  192.168.1.1:6379 192.168.1.2:6379 192.168.1.3:6379 \
  192.168.1.4:6379 192.168.1.5:6379 192.168.1.6:6379 \
  --cluster-replicas 1

# Confirm with 'yes'
```

## Cluster Commands

### Status & Info
```redis
CLUSTER INFO                         # Cluster state summary
CLUSTER NODES                        # All nodes list
CLUSTER SLOTS                        # Slot assignments
CLUSTER MYID                         # Current node ID
CLUSTER KEYSLOT key                  # Which slot for key
CLUSTER COUNTKEYSINSLOT slot         # Keys in slot
CLUSTER GETKEYSINSLOT slot count     # Get keys from slot
```

### Node Management
```bash
# Add node to cluster
redis-cli --cluster add-node new-node:6379 existing-node:6379

# Add as replica
redis-cli --cluster add-node new-node:6379 existing-node:6379 \
  --cluster-slave --cluster-master-id <master-node-id>

# Remove node (must be empty!)
redis-cli --cluster del-node host:6379 <node-id>

# Check cluster health
redis-cli --cluster check existing-node:6379

# Fix cluster issues
redis-cli --cluster fix existing-node:6379
```

### Resharding
```bash
# Interactive reshard
redis-cli --cluster reshard existing-node:6379

# Scripted reshard
redis-cli --cluster reshard existing-node:6379 \
  --cluster-from <source-node-id> \
  --cluster-to <dest-node-id> \
  --cluster-slots 1000 \
  --cluster-yes

# Rebalance (auto-distribute slots)
redis-cli --cluster rebalance existing-node:6379 \
  --cluster-use-empty-masters
```

### Failover
```bash
# Force failover (from replica)
redis-cli -c -h replica-host CLUSTER FAILOVER

# Force failover (ignore master state)
redis-cli -c -h replica-host CLUSTER FAILOVER FORCE

# Takeover (don't wait for master agreement)
redis-cli -c -h replica-host CLUSTER FAILOVER TAKEOVER
```

## Multi-Key Operations

### Hash Tags
```redis
# Keys with same hash tag go to same slot
SET {user:123}:profile "..."
SET {user:123}:sessions "..."
SET {user:123}:preferences "..."

# Multi-key operations work with hash tags
MGET {user:123}:profile {user:123}:sessions
DEL {user:123}:profile {user:123}:sessions
```

### Hash Tag Patterns
```
Pattern                    Hash Part    Slot
user:123:profile          user:123     varies
{user:123}:profile        user:123     same
user:{123}:profile        123          same
order:{customer:456}:item customer:456 same
```

## Client Connection

### Cluster-Aware Connection
```python
from redis.cluster import RedisCluster

# Connect to cluster
rc = RedisCluster(
    host='node1',
    port=6379,
    decode_responses=True
)

# Auto-follows redirects
rc.set('key', 'value')
rc.get('key')

# Pipeline with hash tags
pipe = rc.pipeline()
pipe.set('{user:1}:name', 'Alice')
pipe.set('{user:1}:email', 'alice@example.com')
pipe.execute()
```

### Handling Redirects
```redis
# MOVED - permanent redirect
GET key
# (error) MOVED 5649 192.168.1.2:6379

# ASK - temporary redirect (during migration)
GET key
# (error) ASK 5649 192.168.1.2:6379
# Must send ASKING before retry
```

## Production Configuration

```conf
# redis.conf for cluster node

# Cluster settings
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-replica-validity-factor 10
cluster-migration-barrier 1
cluster-require-full-coverage yes
cluster-replica-no-failover no

# Network (cluster bus = port + 10000)
port 6379
bind 0.0.0.0
cluster-announce-ip 192.168.1.1
cluster-announce-port 6379
cluster-announce-bus-port 16379

# Persistence
appendonly yes
appendfsync everysec

# Memory
maxmemory 4gb
maxmemory-policy allkeys-lru
```

## Assets

- `cluster-config.conf` - Production cluster node config
- `config.yaml` - Cluster settings

## Scripts

- `cluster-health.sh` - Health check script
- `helper.py` - Python utilities

## References

- `CLUSTER_GUIDE.md` - Complete setup guide
- `GUIDE.md` - Reference documentation

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. CLUSTERDOWN
```
CLUSTERDOWN The cluster is down
```

**Diagnosis:**
```bash
redis-cli -c CLUSTER INFO | grep cluster_state
redis-cli -c CLUSTER NODES | grep -v connected
```

**Causes & Fixes:**
| Cause | Fix |
|-------|-----|
| Slots not covered | Add nodes or assign slots |
| Master down, no replica | Restore node or failover |
| Network partition | Fix network |
| Quorum lost | Restore majority |

```bash
# Check uncovered slots
redis-cli --cluster check node:6379

# Fix automatically
redis-cli --cluster fix node:6379 --cluster-fix-with-unreachable-masters
```

#### 2. MOVED Redirect Loop
**Cause:** Stale cluster topology in client

**Fix:**
```python
# Refresh cluster slots
rc.cluster_nodes()

# Or recreate connection
rc = RedisCluster(host='node1', port=6379)
```

#### 3. CROSSSLOT Error
```
CROSSSLOT Keys in request don't hash to the same slot
```

**Fix:** Use hash tags
```redis
# Before (fails)
MGET user:1:name user:2:name

# After (works)
MGET {user:1}:name {user:1}:email
```

#### 4. Resharding Stuck
```bash
# Check migration status
redis-cli -c -h source-node CLUSTER NODES | grep migrating
redis-cli -c -h dest-node CLUSTER NODES | grep importing

# Force finish
redis-cli -c -h dest-node CLUSTER SETSLOT slot STABLE
redis-cli -c -h source-node CLUSTER SETSLOT slot STABLE
```

### Debug Checklist

```markdown
□ All 16384 slots assigned?
□ All masters have replicas?
□ Cluster bus ports open (port+10000)?
□ cluster-announce-ip set correctly?
□ Network allows all node communication?
□ nodes.conf not corrupted?
□ Using cluster-aware client?
□ Hash tags for multi-key ops?
```

### Cluster Health Script

```bash
#!/bin/bash
# check-cluster-health.sh

NODE=$1
echo "=== Cluster Health Check ==="

# Check state
echo -n "Cluster state: "
redis-cli -c -h $NODE CLUSTER INFO | grep cluster_state

# Check slots
echo -n "Slots OK: "
redis-cli -c -h $NODE CLUSTER INFO | grep cluster_slots_ok

# Check nodes
echo "Nodes:"
redis-cli -c -h $NODE CLUSTER NODES | awk '{print $1, $2, $3}'

# Run check
echo "Running cluster check..."
redis-cli --cluster check $NODE:6379
```

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| C001 | CLUSTERDOWN | Cluster unavailable | Check nodes, fix slots |
| C002 | MOVED | Key on different node | Follow redirect |
| C003 | ASK | Slot being migrated | ASKING + retry |
| C004 | CROSSSLOT | Keys in different slots | Use hash tags |
| C005 | TRYAGAIN | Slot in migration | Retry later |

---

## Test Template

```python
# test_redis_cluster.py
import redis
from redis.cluster import RedisCluster
import pytest

@pytest.fixture
def rc():
    return RedisCluster(host='node1', port=6379, decode_responses=True)

def test_cluster_info(rc):
    info = rc.cluster_info()
    assert info['cluster_state'] == 'ok'
    assert info['cluster_slots_ok'] == 16384

def test_set_get(rc):
    rc.set('cluster:test', 'value')
    assert rc.get('cluster:test') == 'value'
    rc.delete('cluster:test')

def test_hash_tags(rc):
    rc.set('{user:1}:name', 'Alice')
    rc.set('{user:1}:email', 'alice@example.com')
    result = rc.mget('{user:1}:name', '{user:1}:email')
    assert result == ['Alice', 'alice@example.com']
    rc.delete('{user:1}:name', '{user:1}:email')

def test_pipeline_hash_tags(rc):
    pipe = rc.pipeline()
    pipe.set('{order:1}:status', 'pending')
    pipe.set('{order:1}:items', '["item1"]')
    results = pipe.execute()
    assert all(results)
    rc.delete('{order:1}:status', '{order:1}:items')
```
