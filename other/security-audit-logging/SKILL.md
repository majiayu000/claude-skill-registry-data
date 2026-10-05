---
name: security-audit-logging
description: Build structured security audit logging with required events, schemas, retention, alerting, and SIEM/OTel export.
---

# Security Audit Logging (Concise)

## When to use
- Compliance (SOC2/PCI/HIPAA), forensics, incident response, change tracking, access reviews.
- Need consistent audit schema across services with SIEM/OTel export and least-privilege storage.

## Core requirements
- **Events**: authN (success/fail, MFA), authZ decisions, data access (who/what/why), admin actions, config changes, key/secrets ops, code deploys, P0 security events.
- **Schema** (structured): timestamp (UTC), actor {id,type}, action, target {type,id}, resource, ip/ua, request_id/trace_id/span_id, result (allow/deny/error), reason, severity, mfa_used, geo (if allowed), tags (env/service/version).
- **Delivery**: JSON lines to stdout + file; forward to SIEM (Elastic/Splunk/CloudWatch Logs/CloudTrail Lake) and OTel exporter.
- **Retention**: hot (30-90d), archive (1-7y per compliance), WORM/immutability for regulated data.
- **Integrity**: append-only store, checksum/hmac, restricted write roles, periodic validation.

## Minimal implementation pattern
- **App level**: middleware hook to emit audit events with correlation IDs; never sample audit logs. Redact secrets/PII; allow hashed identifiers when permitted.
- **Central collector**: sidecar/daemonset or log driver to ship to SIEM; enforce TLS + auth; backpressure handling.
- **OTel export**: use `logs` or convert to traces with `trace_id/span_id` linkage so investigations can pivot.
- **Alerting**: feed SIEM rules (e.g., impossible travel, repeated auth failures, privilege escalation, disabled logging, config tampering).

## Quick examples (vendor-agnostic)
- **HTTP filter**: capture method, path template, status, duration, user id, scope/roles, authz result, request_id/trace_id.
- **DB access**: log CRUD with table/schema, row count, query shape (no raw values), tool/user, source IP.
- **Admin/ops**: log IAM role changes, policy edits, key rotations, feature flag changes, deploys, infra mutations.

## AWS-focused notes
- Prefer CloudTrail Lake for API events; S3 access logs/CloudTrail data events for sensitive buckets; GuardDuty for findings; Security Hub for rollup.
- Centralize to CloudWatch Logs or Firehose -> S3 with object lock + KMS; set lifecycle + Glacier.
- Least privilege: dedicated IAM role for log shipping; deny deletes on audit buckets; enable MFA delete where allowed.

## Quality & testing
- Unit tests: required fields present; redaction; PII guard.
- Integration: emit a sample event per category, ensure it reaches sink/SIEM with trace_id.
- Chaos: simulate sink outage -> ensure local buffering/backoff; simulate tamper attempt -> detect.

## What good looks like
- Traceability: every sensitive action links to user, auth method, device/IP, request/trace ID.
- Coverage: all services emit audit events; gaps documented and tracked.
- Observability: dashboards for volume, error rate, missing fields; alerts for drops or disabled logging.
- Compliance: retention policy enforced; access to logs is audited; WORM for regulated data.

## References
- OTel logs spec; AWS CloudTrail Lake; Elastic/Splunk HTTP Event Collector; CIS benchmarks for logging.
