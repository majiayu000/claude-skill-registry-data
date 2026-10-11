---
name: status
description: 'Check Dokploy application or deployment status Arguments: <app-name-or-id> [--project <project>].'
---

# Check Status

Check the current status of a Dokploy application and its recent deployments.

## Arguments
Format: `<app-name-or-id> [--project <project>]`
- app-name-or-id: Application name or ID (required)
- --project: Project name or ID (helps resolve app by name)

Parse from "$ARGUMENTS".

## Process

1. **Resolve application** (same as deploy command).

2. **Detect Docker Compose build mode:** Call `project-all` (or `project-one`) and check if the project has a compose service alongside the application. If a compose service exists, warn the user: "This project also has a Docker Compose service (`<compose-name>`) — the production site may run from compose, not the standalone app. Showing status of both."

3. **Get application details** using MCP tool `application-one`. Show:
   - Application status (running/stopped/error)
   - Build type
   - Git repository and branch (if connected)
   - Environment: through MCP `env` is redacted (default since `@dokploy/mcp` 0.30.0) — `null` means never set, `[REDACTED]` means a string (possibly empty), so say only "configured" for `[REDACTED]` and never report a count or values; the names-only REST recipe is in the `mcp-patterns` skill ("Redaction")
   - Domains attached (v0.30+: note any with `enabled: false` — switched off via `domain-toggleEnable`)

4. **Get compose details** (if compose service exists) using MCP tool `compose-one`. Show:
   - Compose status
   - Source type (GitHub/Git)
   - Domains attached
   - Flag if auto-deploy is connected to the application but NOT to compose — this is a common misconfiguration

5. **Get recent deployments** using MCP tool `deployment-all` filtered by application. Show last 5 deployments:
   - Deployment ID, status, trigger type, start time, duration

6. **Get monitoring data** using MCP tool `application-readAppMonitoring` if available. Show CPU/memory usage.

7. **Instance overview (optional, v0.30+):** for "what is running overall?" call `overview-services` (and `overview-backups` / `overview-domains` if asked), or `server-getServices { serverId }` for one remote server, instead of walking every project. For host health use `docker-getServerHealth`.

## Example Usage
```
/dokploy-dev:status web-frontend --project my-saas
/dokploy-dev:status abc123-def456
```