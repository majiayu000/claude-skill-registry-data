---
name: redis-replication
description: Master Redis replication - master-replica setup, Sentinel for HA, failover handling, and read scaling patterns
sasmp_version: "1.3.0"
bonded_agent: 06-redis-clustering
bond_type: PRIMARY_BOND

# Production Configuration
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  mode:
    type: string
    required: true
    enum: [basic_replication, sentinel]
  replica_count:
    type: integer
    required: false
    default: 2

# Retry Configuration
retry_config:
  max_retries: 5
  backoff_strategy: exponential
  backoff_base_ms: 1000

# Observability
observability:
  metrics:
    - replication_lag_seconds
    - connected_replicas
    - master_link_status
---

# Redis Replication Skill

## Master-Replica Setup

### Replica Configuration
```conf
replicaof master_ip 6379
masterauth your_password
replica-read-only yes
replica-serve-stale-data yes
```

### Commands
```redis
REPLICAOF master_ip 6379   # Set master
REPLICAOF NO ONE           # Promote to master
INFO replication           # Check status
```

## Sentinel (Auto-Failover)

### Architecture
```
  Sentinel 1     Sentinel 2     Sentinel 3
      ↓              ↓              ↓
      └──────── Monitor ───────────┘
                   ↓
   Master ←──→ Replica 1 ←──→ Replica 2
```

### Configuration
```conf
# sentinel.conf
port 26379
sentinel monitor mymaster 192.168.1.10 6379 2
sentinel auth-pass mymaster password
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
```

### Commands
```redis
# On Sentinel port
SENTINEL masters
SENTINEL get-master-addr-by-name mymaster
SENTINEL failover mymaster
SENTINEL replicas mymaster
```

## Monitoring

```redis
INFO replication
# role:master|slave
# connected_slaves:2
# slave0:ip=...,port=...,state=online,offset=...,lag=0
```

## Assets
- `sentinel.conf` - Sentinel configuration
- `docker-compose-ha.yml` - HA Docker setup

## References
- `REPLICATION_GUIDE.md` - Setup guide

---

## Troubleshooting

### Replica Not Syncing
```redis
INFO replication  # Check master_link_status
```
**Fix:** Check network, password, and firewall

### Split-Brain Prevention
```conf
min-replicas-to-write 1
min-replicas-max-lag 10
```

### Failover Not Triggering
**Check:** Quorum (need majority of Sentinels)

---

## Error Codes

| Code | Name | Recovery |
|------|------|----------|
| R001 | MASTERDOWN | Check master or failover |
| R002 | SYNC_FAILED | Check network/auth |
| R003 | QUORUM_LOST | Restore Sentinel majority |
