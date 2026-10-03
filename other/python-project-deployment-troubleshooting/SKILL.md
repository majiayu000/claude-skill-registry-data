---
name: python-project-deployment-troubleshooting
description: Read-only first troubleshooting workflow for Python project deployments, including systemd startup failures, dependency issues, encoding problems, permissions, proxy setup, and readiness gates.
---

# Python Project Deployment Troubleshooting

## Purpose
Diagnose Python deployment failures safely before changing code, packages, files, permissions, service units, or runtime configuration. This skill turns common failure patterns into a read-only evidence collection workflow.

## When to use
- A Python service fails under systemd or another process supervisor.
- Startup exits with import errors, syntax errors, invalid arguments, readiness blockers, or dependency failures.
- A deployment package may have Windows line endings, BOM, path separator, or archive layout issues.
- The service has proxy, external API, permission, virtualenv, or readiness problems.

## Safety rules
- Default workflow is read-only.
- Do not install packages, edit files, chmod/chown, restart services, unpack archives into production, or modify systemd without explicit approval.
- Do not print `.env`, credentials, API keys, database URLs, tokens, private endpoints, or raw logs containing user data.
- Replace real names and paths with `<PROJECT_NAME>`, `<PROJECT_ROOT>`, `<SERVICE_NAME>`, `<VENV_PATH>`, `<UPLOAD_DIR>`, and `<EXTERNAL_ENDPOINT>`.
- Prefer summarizing traceback types and module names over dumping full logs.

## Read-only workflow
1. Establish the failed component, time window, deployment method, and expected startup path.
2. Check service status and recent journal summaries without restarting.
3. Identify the actual command, working directory, service user, virtualenv, and environment keys present.
4. Inspect package/archive metadata in staging only: file names, size, timestamp, and whether archive layout looks plausible. Do not unpack into production.
5. Check script encoding indicators safely: file type, first bytes if needed, line-ending class, shebang, and shell syntax validity plan. Do not modify the file.
6. Check dependency failure class: missing module, incompatible version, optional extra missing, mirror/source issue, or wrong virtualenv.
7. Check permissions by summarizing ownership and mode of key directories, especially project root, virtualenv, logs, data, and package directories.
8. Check proxy/network requirements and whether the service runtime sees only the required environment variable names, not values.
9. Check readiness gates and current artifact timestamps to avoid treating stale failures as current truth.
10. Produce a remediation plan grouped by approval level: safe checks, package install, permission fix, config edit, restart, or rollback.

## Evidence to collect
- Service active/substate, exit code, restart count, and main PID if present.
- Safe traceback summary: exception type, module name, top-level failing area.
- Entrypoint, working directory, and virtualenv summary.
- Artifact metadata and archive layout concerns.
- Encoding/line-ending/shebang classification.
- Dependency/import failure matrix.
- Permissions summary for required directories.
- Proxy/environment key presence without values.
- Readiness artifact status and freshness.

## Stop conditions
- The next step requires modifying source, installing packages, changing permissions, restarting services, or unpacking deployment artifacts.
- Logs or config contain secrets that cannot be summarized safely.
- It is unclear whether the inspected machine is the deployment target.
- The failure may require code changes and the user has not approved development work.

## Optional user-approved actions
Only after explicit user approval:
- Convert line endings or remove BOM.
- Install missing dependencies or change package indexes.
- Change permissions or ownership.
- Edit systemd unit or environment file.
- Unpack artifacts to staging or production.
- Restart/reload services.
- Add or run diagnostic tests.
- Roll back to a previous deployment artifact.

## Final report format
```text
Summary: <deployment diagnosis>
Project: <PROJECT_NAME>
Service state: <state/exit/restarts>
Failure class: <encoding/dependency/permission/proxy/readiness/archive/unknown>
Evidence:
- Logs: <safe summary>
- Entrypoint: <summary>
- Dependencies: <summary>
- Files/permissions: <summary>
- Readiness: <summary>
Likely cause: <ranked hypothesis>
Recommended remediation: <approval-gated steps>
Needs approval: <specific changes>
```
