---
name: consul
description: "Configure Consul service discovery, health checks, key-value settings, and service-mesh intentions."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["consul", "hashicorp", "service-discovery", "service-mesh", "kv", "health-checks"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# HashiCorp Consul AI Skill Guide

## Overview

Consul provides service discovery, health checking, a hierarchical KV store, and (with Consul Service Mesh) mTLS intentions between services. Agents register services; clients resolve healthy instances via DNS (`service.consul`) or HTTP API/Catalog. Operators should separate client agents from server quorum and treat ACLs as mandatory in any shared environment.

```
Consul servers (quorum / Raft)
        ^
        | gossip + RPC
        v
Client agents on nodes
        |
        +--> service registration + health checks
        +--> DNS / API queries
        +--> Connect proxies + intentions (mesh)
```

## When to use

- Registering services with TCP/HTTP health checks
- Resolving healthy backends without hard-coded IPs
- Storing non-secret config in Consul KV (secrets belong in Vault)
- Defining mesh intentions (allow/deny service-to-service)

## Operational directives

1. Run an odd-numbered server quorum (3 or 5); never one server in prod.
2. Enable ACLs; bootstrap once and store the bootstrap token offline.
3. Keep health checks honest - failing checks remove instances from discovery.
4. Do not put passwords in Consul KV; integrate Vault for secrets.
5. Prefer prepared queries / service resolvers for multi-DC failover designs.

## Concrete examples

### Service registration (JSON)

```json
{
  "service": {
    "name": "api",
    "id": "api-1",
    "port": 8080,
    "tags": ["prod", "v1"],
    "check": {
      "http": "http://127.0.0.1:8080/healthz",
      "interval": "10s",
      "timeout": "2s"
    }
  }
}
```

```bash
consul services register api.json
consul catalog services
consul health service api -passing
dig @127.0.0.1 -p 8600 api.service.consul
```

### KV config

```bash
consul kv put apps/api/log_level info
consul kv get apps/api/log_level
consul kv export apps/api/ > api-kv-backup.json
```

### Intention (service mesh allow)

```bash
consul intention create -allow web api
consul intention list
```

### Operator checks

```bash
consul members
consul operator raft list-peers
consul info
```

## Discovery failure matrix

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| Empty DNS answers | Checks failing / not registered | `consul health service` |
| Split views | ACL or stale client | Check token; `consul members` |
| Leader election churn | Server network / disk | Inspect raft peers; stabilize IOPS |
| KV read denied | Missing ACL policy | Grant `key:apps/api/` read |

## Best practices

1. Tag services with environment and version for canary routing.
2. Use health check deregister-after for crash-looping tasks.
3. Backup Raft/KV on a schedule; test restore.
4. Document gossip encryption key rotation separately from ACLs.

## Limitations

- Consul is not a replacement for full east-west observability (pair with metrics/tracing).
- Mesh features add proxy sidecar operational cost.
- Multi-DC WAN federation needs careful network and ACL planning.

## Related skills

- `nomad` - often co-deployed for scheduling with Consul discovery
- `vault` - secrets companion to Consul KV
- `opentelemetry` - telemetry beyond Consul health checks
- `nginx-hardening` - edge proxy in front of discovered backends
