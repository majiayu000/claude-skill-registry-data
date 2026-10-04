---
name: ceph
description: "Ceph distributed storage across all supported versions (Squid 19.2 through Tentacle 20.2): RADOS, CRUSH, BlueStore, RBD, CephFS, RGW, and cluster operations. Use for \"Ceph\", \"RADOS\", \"CRUSH map\", \"OSD\", \"BlueStore\", \"RBD\", \"CephFS\", \"RGW\", \"radosgw\", \"ceph health\", \"ceph status\", \"placement group\", \"PG\", \"erasure coding\", \"Ceph pool\", \"ceph-volume\", \"Cephadm\", \"Rook\", \"ceph osd\", \"ceph mon\", \"MDS\", \"Ceph dashboard\"."
license: MIT
---

# Ceph

This skill covers Ceph distributed storage across all supported versions (Squid 19.2 through Tentacle 20.2). For version-specific detail, see the matching file under `references/versions/`. Core knowledge areas:

- RADOS fundamentals, cluster maps, and the Paxos-based monitor consensus
- CRUSH algorithm, hierarchy design, failure domains, and OSD weight management
- BlueStore backend, RocksDB, WAL/DB device separation, checksumming, and compression
- RBD block storage, layering, mirroring, live migration, and Kubernetes CSI
- CephFS distributed filesystem, MDS scaling, snapshots, quotas, and client capabilities
- RGW S3/Swift-compatible object storage, multi-site replication, IAM, and bucket management
- Placement groups, autoscaling, state machine, recovery, and backfill
- Erasure coding profiles, FastEC (Tentacle), and ISA-L optimization
- Cephadm and Rook orchestration, monitoring with Prometheus/Grafana
- Upgrade paths between major releases

When a question is version-specific, see the matching `references/versions/<v>.md` file. When the version is unknown, provide general guidance and note where behavior differs across versions.

For cross-platform storage comparisons or technology selection, see the `overview` skill.

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for health checks, OSD failures, PG states, slow ops, and recovery workflows
   - **Architecture / design** -- Load `references/architecture.md` for RADOS internals, CRUSH, BlueStore, RBD, CephFS, RGW, and data flow
   - **Best practices** -- Load `references/best-practices.md` for sizing, CRUSH design, pool config, BlueStore tuning, Rook/K8s, CephFS, and monitoring

2. **Identify version** -- Determine which Ceph release the user runs. Key version-gated features:
   - Squid 19.2: LZ4 RocksDB compression default, RBD diff-iterate local exec, CephFS crash-consistent snapshots, RGW IAM APIs
   - Tentacle 20.2: FastEC, mgmt-gateway, oauth2-proxy, certmgr, SMB Manager, instant RBD live migration, per-directory case insensitivity

3. **Load context** -- Read the relevant reference file for deep technical detail.

4. **Analyze** -- Apply Ceph-specific reasoning. Consider pool type (replicated vs EC), backend (BlueStore), failure domain, workload profile.

5. **Recommend** -- Provide actionable guidance with CLI commands and configuration examples.

6. **Verify** -- Suggest validation steps (`ceph health detail`, `ceph status`, `ceph osd tree`, `ceph pg stat`).

## Core Architecture

### How Ceph Works

```
                    ┌──────────────┐
                    │  Client App  │
                    └──────┬───────┘
                           │  CRUSH(hash(object), OSDMap)
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼──────┐ ┌───▼─────┐
       │  Primary OSD │ │Replica  │ │Replica  │
       │  (BlueStore) │ │ OSD     │ │ OSD     │
       └─────────────┘ └─────────┘ └─────────┘
              │
       ┌──────▼──────┐
       │  Monitors    │  Paxos consensus, cluster map
       └─────────────┘
```

1. **Compute** -- Client hashes the object name to a placement group (PG), then CRUSH maps the PG to an ordered list of OSDs
2. **Write** -- Primary OSD writes to BlueStore, fans out to replicas in parallel, waits for acks, then acknowledges to client
3. **Read** -- Client reads from primary OSD (or any shard for EC pools); checksums validated on every read

### Key Components

| Component | Role |
|---|---|
| **Monitors (MON)** | Maintain cluster map via Paxos consensus; authenticate via CephX; odd count (3 or 5) |
| **OSDs** | Store data on BlueStore; handle replication, recovery, scrub; one per device |
| **Managers (MGR)** | Prometheus metrics, Dashboard, PG autoscaler, balancer; active/standby pair |
| **MDS** | CephFS metadata namespace; directory tree, inodes, client caps; multiple active ranks |
| **RGW** | S3/Swift HTTP gateway over RADOS; multi-site replication; bucket management |

### Storage Interfaces

| Interface | Protocol | Use Case |
|---|---|---|
| **RBD** | Block (librbd, krbd, NBD) | VM disks, Kubernetes PVs, databases |
| **CephFS** | File (POSIX via FUSE/kernel) | Shared filesystems, NFS/SMB gateway |
| **RGW** | Object (S3/Swift REST) | Backups, archives, cloud-native apps |
| **RADOS** | Native librados | Custom applications needing direct object access |

## CRUSH and Data Placement

### CRUSH Hierarchy

```
root (default)
├── datacenter (dc1)
│   ├── rack (rack1)
│   │   ├── host (node1)
│   │   │   ├── osd.0 (weight 4.0 = 4TB)
│   │   │   └── osd.1 (weight 4.0)
│   │   └── host (node2)
│   │       ├── osd.2 ...
```

**Failure domain** in a CRUSH rule determines replica placement separation. Common: `host` (each replica on a different server), `rack` (each on a different rack).

### Pool Types

| Type | Data Protection | Space Efficiency | Best For |
|---|---|---|---|
| Replicated (size=3) | 3 copies, tolerate 2 failures | 33% usable | General workloads, low latency |
| Erasure coded (k=4,m=2) | 6 shards, tolerate 2 failures | 67% usable | Cold data, object storage, archives |

## Placement Groups

Objects map to PGs via hash; PGs map to OSDs via CRUSH. This indirection enables efficient rebalancing.

**Target:** 100-200 PGs per OSD across all pools. The PG autoscaler (enabled by default) manages this automatically.

**Key PG states:** `active+clean` (healthy), `active+degraded` (replicas missing, I/O continues), `peering` (negotiating, I/O blocked), `inactive` (all OSDs down, no I/O).

## BlueStore

Default OSD backend. Manages raw block devices directly without an intermediate filesystem.

- **RocksDB** stores object metadata (onodes), PG logs, and omap data
- **WAL/DB separation**: Offload RocksDB to NVMe for HDD-backed clusters (WAL: 1-2 GB, DB: 1-4% of data device)
- **Checksumming**: crc32c on all data and metadata; validated on every read
- **Compression**: Per-pool inline (snappy, lz4, zlib, zstd)

## Version-specific guidance

| Version | Reference | What's version-specific |
|---|---|---|
| Squid 19.2 | `references/versions/19.2.md` | BlueStore LZ4 RocksDB compression default, RBD diff-iterate local execution, CephFS crash-consistent snapshots, RGW IAM APIs, Crimson/SeaStore tech preview |
| Tentacle 20.2 | `references/versions/20.2.md` | FastEC erasure coding, mgmt-gateway, oauth2-proxy, certmgr, integrated SMB Manager, instant RBD live migration, per-directory case insensitivity |

## Reference Files

- `references/architecture.md` -- RADOS internals, CRUSH algorithm, BlueStore, RBD, CephFS, RGW, data flow, erasure coding, Cephadm
- `references/best-practices.md` -- Cluster sizing, CRUSH design, pool config, BlueStore tuning, Rook/K8s, CephFS, Prometheus monitoring
- `references/diagnostics.md` -- Health checks, OSD failures, slow ops, PG states, recovery, clock skew, network partitions, log analysis

## Diagnostic Scripts

Ready-made CLI bundles (admin/readonly keyring; prepend `cephadm shell --` if containerized) in `scripts/`, numbered by investigation order. All read-only.

- `scripts/01-cluster-status.sh` -- Status, health detail, capacity, monitor quorum
- `scripts/02-osd-health.sh` -- OSD tree, fill skew, latency outliers, balancer state
- `scripts/03-pg-troubleshoot.sh` -- Stuck/degraded PG triage and recovery reading
