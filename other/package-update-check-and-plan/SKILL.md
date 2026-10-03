---
name: package-update-check-and-plan
description: Read-only workflow for discovering uploaded deployment artifacts, comparing them with current deployment state, and preparing a safe update and rollback plan.
---

# Package Update Check and Plan

## Purpose
Identify whether new deployment artifacts exist, compare them with the currently deployed components, and produce a safe update plan with backup, verification, and rollback steps. The default workflow stops before any deployment or file modification.

## When to use
- A user says a new package, build artifact, archive, JAR/WAR, image, or frontend bundle was uploaded.
- A user asks whether a project can be updated.
- Multiple components need coordinated update planning.
- You need a deployment plan before touching production files.

## Safety rules
- Default workflow is read-only.
- Do not copy, unpack, replace, delete, chmod, chown, restart, reload, migrate, or clean files without explicit approval.
- Do not reveal real upload paths, production paths, usernames, domains, IPs, database strings, or service names in public output.
- Replace identifiers with `<PROJECT_NAME>`, `<PROJECT_ROOT>`, `<UPLOAD_DIR>`, `<ARTIFACT_NAME>`, `<SERVICE_NAME>`, and `<APP_DOMAIN>`.
- Never trust a partially uploaded artifact. Size and checksum comparison belong in the plan before replacement.
- Separate current-state verification from deployment action.

## Read-only workflow
1. Clarify the deployment target and artifact source location using placeholders if preparing a public report.
2. List candidate artifacts in the upload/staging area by type, size, and timestamp. Do not unpack them.
3. Identify currently deployed components: backend artifact, frontend bundle, service unit, reverse proxy config, config directory, data directory, and logs directory.
4. Compare current vs candidate metadata: size, timestamp, version string if available, checksum if safe to compute, and component mapping.
5. Check current service and port state without changing anything.
6. Check whether the target machine differs from the current machine. If remote deployment is involved, plan source and target verification separately.
7. Identify configuration compatibility risks: port changes, required environment variables, database migration expectations, reverse proxy upstreams, static asset layout, file ownership needs.
8. Draft an update sequence with explicit approval gates: backup, artifact verification, frontend update, backend update, service restart, health checks, rollback.
9. Draft rollback criteria and rollback steps, but do not execute them.

## Evidence to collect
- Artifact list with redacted names, size, timestamp, and type.
- Current deployed component inventory.
- Version/checksum comparison if available.
- Current service state and listening port summary.
- Reverse proxy/upstream mapping summary without real domains or IPs.
- Config compatibility concerns.
- Backup targets and rollback prerequisites.
- Remote/local machine distinction.

## Stop conditions
- Artifact upload is incomplete or checksum cannot be verified.
- Target host is ambiguous.
- The update requires schema migration, data deletion, or destructive replacement and no approval exists.
- Current state cannot be safely inventoried.
- The package may contain secrets or private customer data.

## Optional user-approved actions
Only after explicit user approval:
- Create backups.
- Transfer artifacts to a target host.
- Verify checksums on source and target.
- Unpack archives into staging.
- Replace deployed files.
- Reload or restart services.
- Run post-deployment health checks that may touch write paths.
- Execute rollback.

## Final report format
```text
Summary: <whether update appears possible>
Project: <PROJECT_NAME>
Candidate artifacts:
- <ARTIFACT_NAME>: <type/size/timestamp/checksum status>
Current deployment:
- Backend: <summary>
- Frontend: <summary>
- Service: <summary>
- Proxy: <summary>
Compatibility risks: <bullets>
Proposed update plan: <numbered approval-gated steps>
Rollback plan: <numbered approval-gated steps>
Read-only conclusion: <ready / blocked / needs more info>
Needs approval: <specific actions>
```
