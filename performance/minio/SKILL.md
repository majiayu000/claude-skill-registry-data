---
name: minio
description: "MinIO high-performance S3-compatible object storage: erasure coding, mc client, KES encryption, site replication, ILM, IAM, Kubernetes Operator, and AIStor. Use for \"MinIO\", \"minio\", \"mc client\", \"mc admin\", \"MinIO erasure\", \"MinIO operator\", \"KES\", \"MinIO bucket\", \"MinIO replication\", \"MinIO healing\", \"S3-compatible\", \"AIStor\", \"MinIO console\". Do NOT use for AWS S3, Azure Blob, or GCS specifics — use the `aws-s3`, `azure-blob`, or `gcs` skill instead."
license: MIT
---

# MinIO

This skill covers MinIO S3-compatible object storage, including:

- Erasure coding (Reed-Solomon), drive quorums, and inline bitrot protection
- Server pool architecture, erasure set sizing, and horizontal scaling
- mc client for S3 operations and mc admin for cluster management
- KES key encryption service and SSE-S3/SSE-KMS/SSE-C modes
- Site replication (active-active multi-site), bucket replication, and batch operations
- ILM lifecycle policies, tiering, and object expiration
- IAM (built-in users, LDAP, OIDC, STS) and AWS-compatible policy engine
- MinIO Operator for Kubernetes with Tenant CRD management
- Performance tuning for NVMe, AVX-512, and high-throughput workloads
- Licensing landscape (AGPLv3 archived community vs AIStor commercial)

For cross-platform storage comparisons, see the `overview` skill.

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for drive failures, healing, performance benchmarks, replication lag, and common issues
   - **Architecture / design** -- Load `references/architecture.md` for erasure coding, storage hierarchy, request pipeline, KES, site replication, and Operator
   - **Best practices** -- Load `references/best-practices.md` for hardware sizing, EC selection, bucket design, security hardening, K8s deployment, and backup strategy

2. **Assess edition** -- Determine if the user runs archived community edition or AIStor. Key differences: community (AGPLv3, archived Feb 2026, no patches) vs AIStor Free/Enterprise (active, proprietary/commercial).

3. **Load context** -- Read the relevant reference file.

4. **Analyze** -- Consider erasure set size, drive count, quorum rules, network topology.

5. **Recommend** -- Provide actionable guidance with mc commands and configuration examples.

## Core Architecture

### Storage Hierarchy

```
Server Pools
  └── Erasure Sets (4-16 drives, up to 32 in AIStor 2026+)
        └── Physical Drives (NVMe recommended)
```

- Each pool manages its own erasure sets independently
- Pool expansion is the only supported horizontal scale-out path
- Object placement: `hash(object_key) -> erasure set index`

### Erasure Coding

For each write: object split into K data shards + M parity shards, written in parallel. Default: K = M = N/2 where N is drives per erasure set.

| Operation | Minimum Drives Required |
|-----------|------------------------|
| Write | (N/2) + 1 |
| Read | N/2 |

AVX-512 SIMD acceleration for near wire-speed erasure coding. Inline bitrot protection via HighwayHash-256 on every shard.

### Request Pipeline

```
Client HTTP/S -> TLS -> Auth (IAM) -> S3 API Handler -> ObjectLayer
  -> ErasurePoolsObjects -> ErasureObjects -> Physical Drives
```

## Key Capabilities

| Feature | Detail |
|---|---|
| S3 API compatibility | Near-complete AWS S3 API coverage |
| Object versioning | UUID version IDs, delete markers, noncurrent version management |
| Object locking (WORM) | COMPLIANCE and GOVERNANCE modes |
| Server-side encryption | SSE-S3, SSE-KMS (via KES), SSE-C |
| Site replication | Active-active multi-site, IAM + data + metadata sync |
| ILM / Lifecycle | Expiration, tiering/transition to warm/cold targets |
| Batch operations | Server-side replicate, expire, keyrotate via YAML jobs |
| Bucket notifications | Kafka, AMQP, NATS, PostgreSQL, Redis, Webhook, and more |
| Kubernetes Operator | Tenant CRD, auto-TLS, declarative management |

## Licensing (April 2026)

| Edition | Status | License |
|---|---|---|
| Community (OSS) | Archived Feb 13, 2026 | AGPLv3 |
| AIStor Free | Active | Proprietary |
| AIStor Enterprise | Active | Commercial (~$96K/year) |

The archived community repository remains functional but receives no patches.

## Reference Files

- `references/architecture.md` -- Erasure coding, storage hierarchy, request pipeline, KES, site replication, Operator, notifications, ILM, IAM
- `references/best-practices.md` -- Hardware sizing, EC selection, bucket design, security hardening, K8s deployment, performance tuning, backup strategy
- `references/diagnostics.md` -- mc admin commands, health checks, drive failures, healing, performance benchmarks, network diagnostics, common issues
