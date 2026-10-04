---
name: gcs
description: "Google Cloud Storage service administration and design: storage classes (Rapid, Standard, Nearline, Coldline, Archive), Autoclass, Hierarchical Namespace, lifecycle management, signed URLs, IAM, Pub/Sub notifications, Storage Transfer Service, and cost optimization. Use for \"GCS\", \"Google Cloud Storage\", \"gcloud storage\", \"gsutil\", \"Autoclass\", \"Nearline\", \"Coldline\", \"Archive storage\", \"Rapid storage\", \"signed URL\", \"GCS lifecycle\", \"GCS bucket\", \"HNS bucket\", \"Storage Transfer Service\", \"GCS HMAC\", \"Turbo Replication\". Do NOT use for general GCP project/VPC/multi-service architecture — that's the `cloud-platforms` plugin."
license: MIT
---

# Google Cloud Storage

This skill covers Google Cloud Storage, including:

- Storage classes (Rapid, Standard, Nearline, Coldline, Archive) and Autoclass automatic tiering
- Bucket locations (regional, dual-region with Turbo Replication, multi-region)
- Hierarchical Namespace (HNS) for atomic directory operations and higher QPS
- Lifecycle management rules (SetStorageClass, Delete, AbortIncompleteMultipartUpload)
- Object versioning, soft delete, retention policies, and object holds
- IAM (uniform bucket-level access, POSIX ACLs, IAM Conditions, managed folders)
- Signed URLs (V4), HMAC keys, VPC Service Controls, public access prevention
- Pub/Sub notifications, Compose objects, S3-compatible XML API
- Storage Transfer Service for large-scale migrations
- Batch Operations, Storage Insights, and Object Contexts
- CLI tools: gcloud storage (recommended) and gsutil (legacy)
- Cost optimization: egress management, class selection, soft delete tuning
- Monitoring: Cloud Monitoring metrics, audit logs, RPO tracking

For cross-platform storage comparisons, see the `overview` skill.

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for access denied (403/401), slow transfers, billing analysis, monitoring metrics, audit logs, quota issues
   - **Architecture / design** -- Load `references/architecture.md` for buckets, objects, storage classes, Autoclass, locations, lifecycle, versioning, retention, IAM, notifications
   - **Best practices** -- Load `references/best-practices.md` for bucket design, class selection, security hardening, cost optimization, performance patterns, data lifecycle

2. **Load context** -- Read the relevant reference file.

3. **Analyze** -- Consider location strategy, access patterns, Autoclass fit, GCP ecosystem integration, cost model.

4. **Recommend** -- Provide actionable guidance with gcloud storage commands and JSON lifecycle configs.

## Core Concepts

### Storage Classes

| Class | Min Duration | Retrieval Fee | Best For |
|---|---|---|---|
| Rapid | None | None | AI/ML, analytics (zonal buckets) |
| Standard | None | None | Hot data, streaming, web serving |
| Nearline | 30 days | Yes | Monthly backups |
| Coldline | 90 days | Yes (higher) | Quarterly DR |
| Archive | 365 days | Yes (highest) | Compliance, annual access |

All classes: 11 nines durability, millisecond retrieval latency (no thaw delay for any class).

### Autoclass

Automatic per-object tiering based on access. Objects start Standard, transition through Nearline -> Coldline -> Archive on inactivity. Any GET returns to Standard. No retrieval fees within Autoclass. Objects < 128 KiB stay Standard.

### Bucket Locations

- **Regional**: Single region, lowest latency for co-located compute
- **Dual-region**: Two specific paired regions. Turbo Replication: 15-minute RPO SLA (`--rpo=ASYNC_TURBO`)
- **Multi-region**: US/EU/ASIA, 99.95% availability SLA

### Key Security Defaults

- Uniform bucket-level access (IAM-only, disables ACLs) -- recommended for all
- Public Access Prevention org policy
- VPC Service Controls for perimeter enforcement
- Google-managed AES-256 encryption by default; CMEK/CSEK available

### CLI Tools

- `gcloud storage` (Go-based, recommended, faster)
- `gsutil` (Python-based, legacy, still supported)

## Reference Files

- `references/architecture.md` -- Buckets, objects, storage classes, Autoclass, locations, lifecycle, versioning, retention, IAM/ACLs, HMAC, Pub/Sub, JSON/XML APIs
- `references/best-practices.md` -- Bucket design, class selection, security hardening, cost optimization, performance patterns, data lifecycle
- `references/diagnostics.md` -- Access denied (403/401/412), slow transfers, billing analysis, Cloud Monitoring metrics, audit logs, quota issues, common error codes
