---
name: pre-deployment-readonly-checklist
description: Generic read-only checklist for preparing an application deployment by verifying host, artifacts, backups, service state, configuration, dependencies, and rollback readiness before any write action.
---

# Pre-Deployment Read-Only Checklist

## Purpose
Create a deployment readiness picture before any production modification. The workflow inventories artifacts, current runtime state, configuration, dependencies, risk, and rollback prerequisites without touching production files.

## When to use
- Before deploying a new backend, frontend, worker, config bundle, container image, or package.
- Before following a user-provided deployment guide.
- When the target host, artifact source, or rollback path is uncertain.
- Before any action that may replace files, restart services, migrate data, or alter configuration.

## Safety rules
- This skill is strictly read-only by default.
- Do not copy, unpack, edit, delete, chmod, chown, install, restart, reload, migrate, or clean anything without explicit approval.
- Do not print secrets, private logs, customer data, database URLs, tokens, internal IPs, real domains, or service account names.
- Use placeholders: `<PROJECT_NAME>`, `<PROJECT_ROOT>`, `<UPLOAD_DIR>`, `<SERVICE_NAME>`, `<APP_DOMAIN>`, `<SERVER_IP>`, `<DB_NAME>`.
- If the deployment requires code or business-logic changes, stop and ask for explicit approval.

## Read-only workflow
1. Confirm host context: current host, user, working directory, date/time, OS, and whether this is the deployment target or only a control machine.
2. Confirm scope: component list, deployment artifact source, expected target paths, expected service names, and rollback requirements.
3. Inventory candidate artifacts: type, size, timestamp, checksum status, version string if available, and whether upload appears complete.
4. Inventory current deployment: process/service state, active version if visible, target directories, config files, logs directory, data directory, reverse proxy entries, and scheduled tasks.
5. Check resource readiness: disk space, memory pressure, CPU/load, inode availability, and port occupancy summaries.
6. Check dependency readiness: runtime version, virtualenv/container status, package manager availability, database reachability by safe metadata only, external service assumptions, and proxy requirements.
7. Check configuration compatibility: expected ports, env key presence without values, profile selection, feature flags, database migration requirements, static asset layout, and reverse proxy upstreams.
8. Check backup and rollback prerequisites: existing backups, writable backup target, rollback artifact availability, service stop/start requirements, and data protection constraints.
9. Identify risk class: low-risk static update, service restart required, schema/data risk, cross-host risk, or unclear target risk.
10. Produce a go/no-go recommendation and list user approvals required before deployment.

## Evidence to collect
- Host identity and target confirmation.
- Artifact inventory and completeness indicators.
- Current service/process/port state.
- Config presence and expected keys, values redacted.
- Resource summary: disk, memory, load, inodes.
- Backup and rollback readiness.
- Dependency and external connectivity assumptions.
- Risk classification and blockers.

## Stop conditions
- Target host is ambiguous.
- Artifact upload is incomplete or unverified.
- Backup/rollback path is missing for a risky deployment.
- Required config contains secrets that cannot be safely summarized.
- Deployment includes data migration, deletion, or schema changes without approval.
- Current production state cannot be inventoried safely.

## Optional user-approved actions
Only after explicit user approval:
- Create backups.
- Transfer artifacts.
- Stage or unpack packages.
- Stop, start, restart, or reload services.
- Apply migrations.
- Edit configuration.
- Execute deployment or rollback.

## Final report format
```text
Summary: <go/no-go/readiness result>
Host context: <host/user/time/target confirmation>
Scope: <PROJECT_NAME components>
Artifacts: <inventory and completeness>
Current state: <services/ports/config/resources>
Backup/rollback: <ready/blocked/unknown>
Risks: <bullets>
Blockers: <bullets>
Approvals required before deployment: <specific actions>
Recommended next step: <read-only follow-up or approved deployment gate>
```
