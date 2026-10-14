---
name: gcp
description: "GCP essentials: IAM, VPC, Compute/GKE/Cloud Run, Cloud SQL/Firestore/Memorystore, Pub/Sub, Cloud Monitoring. Use for GCP decisions and deploys; research current docs per configured version."
---

# gcp

Same foundations as `../foundations/`, resolved against current GCP docs.

## Activate when

- Choosing or operating GCP services; wiring GCP IAM, networking, data, or deploys.

## Do NOT activate for

- AWS/Azure specifics (see aws-foundations, azure).

## Procedure

1. Identity: IAM roles per workload (no user keys on servers), Workload Identity for GKE, audit logs on.
2. Network: VPC with private clusters/services, firewall rules as narrow allowlists, no public databases.
3. Compute: Cloud Run for request-driven, GKE for steady/containerized, staged rollouts with health checks.
4. Data: Cloud SQL with backups + pooling, Firestore per documented access patterns, Memorystore for hot reads, Pub/Sub decoupling slow work.
5. Observe: Cloud Monitoring metrics/alarms, structured logs, tracing, SLOs.
6. Research: https://cloud.google.com/docs for the configured API versions (registry: `../../research/documentation-search/references/framework-registry.yaml` — gcp). Never invent service behavior; resolve against docs.
7. Verify: scratch deploy, kill-and-recover, restore drill, billing alert confirmed.

## References
- `../foundations/`, `../aws-foundations/` (procedure pattern).
