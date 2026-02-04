---
name: gcp-troubleshoot
description: "Troubleshoot GCP services using tool-first access (via MCP when available), falling back to the CLI only when necessary. Focus on Firestore, Cloud Run, networking, load balancers, IAM, Pub/Sub, Cloud SQL, and Storage."
---

# GCP Troubleshooting Skill

## General Guidance

Always attempt to investigate issues using **tool-based access first** (MCP tools if configured).  
Only fall back to the **GCP CLI (gcloud)** when the tool cannot access required logs, metrics, or audit data.

All investigations should:

1. Scope queries by service/resource type  
2. Restrict by time window  
3. Prefer targeted logs/metrics, not full dumps  
4. Diagnose root cause based on error type  
5. Suggest minimal, safe remediation steps

---

## Core Services Covered

### Firestore

Common issues:

- PERMISSION_DENIED
- Missing indexes
- Transaction contention
- Quota exceeded

Investigations:

- Query Firestore logs filtered by `resource.type="firestore_database"`
- Check latency, retries, aborted transactions

### Cloud Run

Common issues:

- Startup failures
- Crash loops
- IAM failures calling other services
- Cold starts

Investigations:

- Query Cloud Run logs (`resource.type="cloud_run_revision"`)
- Check revision rollout history
- Look for Cloud SQL connector errors or storage access failures

### Networking & Load Balancers

Common issues:

- 5xx responses
- Backend connection errors
- Firewall denies

Investigations:

- Query load balancer logs (`resource.type="http_load_balancer"`)
- Inspect backend health logs
- Check VPC routes + firewall rules

### IAM

Common issues:

- PermissionDenied
- Missing service account roles

Investigations:

- Query audit logs: `protoPayload.status.code != 0`
- Identify the principal, resource, and role mismatch

### Pub/Sub

Common issues:

- Failed push deliveries
- Ack deadlines exceeded
- DLQ accumulation

Investigations:

- Filter subscription logs
- Inspect subscriber errors and endpoint failures

### Cloud SQL

Common issues:

- Connection limit reached
- Auth failures
- Private network routing failures

Investigations:

- Cloud SQL logs (`resource.type="cloudsql_database"`)
- Check database flags, failover events, connection counts

### Storage Buckets

Common issues:

- 403 Forbidden
- Precondition checks
- Signed URL failures

Investigations:

- Inspect Storage logs (`resource.type="gcs_bucket"`)
- Check IAM, bucket policies, object existence

---

## Workflow

1. Identify target resource
2. Query scoped logs
3. Query metrics
4. Query audit logs if access or permission failures occur
5. Interpret patterns
6. Suggest actionable fixes

---

## When to Warn

- Unscoped log queries
- Very wide time ranges
- Requests requiring IAM escalation
