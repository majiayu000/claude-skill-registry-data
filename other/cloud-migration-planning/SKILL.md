---
name: cloud-migration-planning
description: Plan and execute cloud migrations with discovery, wave planning, data moves, cutover, and validation across AWS/Azure/GCP.
---

# Cloud Migration Planning (Concise)

## When to use
- Moving on-prem to cloud, consolidating providers, modernizing legacy apps
- Needing phased moves with rollback + telemetry (OpenTelemetry/OpenLIT) and SkyPilot offloading
- Planning DR/regional failover or cost-optimization migrations

## Fast workflow
1) **Discovery**: inventory apps, data stores, RPO/RTO, deps, latency/SLA, compliance.
2) **Strategy**: choose per workload: lift/shift, replatform, refactor, retire. Define success metrics (perf, error rate, cost delta, SLOs) and rollback gates.
3) **Wave plan**: low-risk first, honor dependencies, add dress rehearsals. Keep canary users and SLO monitors.
4) **Data move**: select path per store:
   - OLTP: DMS/CDC (AWS), Database Migration Service (GCP), DMS MI (Azure), or native logical replication; dual-write only with conflict rules.
   - Analytics: batch rsync + manifest, Snowpipe/BigQuery load jobs; checksum samples.
   - Blobs: parallel sync (S3->GCS/Azure) + versioning; signed-URL/ACL parity.
5) **Infra**: stand up target infra as code (Terraform/CloudFormation/Bicep). Keep secrets in manager (SM/KeyVault/SM+KMS). Enable tracing/logs early.
6) **Cutover**: freeze writes, drain queues, final CDC catch-up, swap DNS/conn strings, run smoke + synthetic, watch error budget; have rollback timer.
7) **Post**: backfill stragglers, decommission safely, cost and perf tune, DR rehearsal.

## Minimal AWS playbook
- **DMS quick start** (conceptual):
  - Create replication instance (private, multi-AZ if needed), source/target endpoints, and task `full-load-and-cdc` with table mappings.
  - Monitor `ReplicationTaskStats` (lag, failures) and CloudWatch alarms; wire OpenTelemetry exporter if available.
- **Terraform shape** (high level): VPC + subnets, DMS subnet group, replication instance, endpoints, task, Secrets Manager for creds, CloudWatch log group + alarm. Keep SG least-privilege.
- **S3/object moves**: `aws s3 sync --delete --exact-timestamps`; enable versioning + checksum validation.
- **Rollback**: keep source writable snapshot/restore plan; DNS/conn string revert procedure pre-written.

## Cutover checklist (short)
- Lag < 1s; last full backup validated; health checks green.
- Freeze writes; drain queues; pause batch jobs.
- Update secrets/conn strings; deploy feature flags for dual-read if used.
- Switch DNS/ALB target; run smoke + key user journeys; verify metrics: p95 latency, error rate, 5xx, DB locks, queue depth.
- Rollback trigger: error budget burn > threshold or data mismatch; revert DNS/traffic and unfreeze writes on source.

## Validation & telemetry
- Data: row counts/hash samples before/after; CDC gap check; checksum object manifests.
- App: synthetic tests, golden path scripts, canary users; log anomaly detection; OpenTelemetry traces to OpenLIT backend.
- Ops: dashboards for DMS task status, replication lag, S3 transfer errors, DNS propagation, cost deltas.

## Security & compliance
- Encrypt in transit (TLS) and at rest (KMS/Key Vault/CMK); rotate creds; least-priv SGs/IAM; redact PII in logs.
- Access via SSO/assumed roles; break-glass separate.
- Audit: trail of changes (IaC), change tickets, approvals.

## Risk mitigations
- Run dress rehearsal in lower env with prod-like data slice.
- Dual-run read-only for a window; enable feature flags to fallback reads.
- Keep source warm until post-cutover validation passes + DR runbook updated.

## Timelines (rule of thumb)
- Assessment 2-4w → Pilot 2-8w → Waves 8-16w → Optimization 4w+ → Closure 1-2w.

## References
- AWS MAP, Azure CAF migrate, GCP Migration Center
- AWS DMS best practices: sizing, LOB handling, task logging
- DNS cutover: low TTL + health-checked targets
