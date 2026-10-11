---
name: deploy
description: 'Deploy or redeploy a Dokploy application or Docker Compose service Arguments: <app-name-or-id> [--project <project>].'
---

# Deploy Application

Trigger a deployment for an existing Dokploy application.

## Arguments
Format: `<app-name-or-id> [--project <project>]`
- app-name-or-id: Application name or ID (required)
- --project: Project name or ID (helps resolve app by name)

Parse from "$ARGUMENTS".

## Process

1. **Resolve application:**
   - If argument is a UUID, use it directly.
   - If a name, call `project-all` to list projects, then `project-one` on the matching project (or --project) to find the application by name.

2. **Detect Docker Compose build mode:** Call `project-all` (or `project-one`) and check if the project has a compose service alongside the application. If a compose service exists, the production site likely runs from the compose service — NOT the standalone application. In this case:
   - Warn the user: "This project has a Docker Compose service (`<compose-name>`). The site likely runs from compose, not the standalone app. Deploy the compose service instead?"
   - If user confirms, deploy the **compose** service using `compose-deploy` MCP tool (or REST API fallback: `POST /api/compose.deploy` with `{"composeId": "<id>"}` and `x-api-key` header).
   - If `compose-deploy` MCP tool is not available, use the REST API fallback automatically.
   - Do NOT deploy only the standalone application when a compose service exists — this silently succeeds but leaves the site unchanged.

3. **Check current state** using MCP tool `application-one` (or `compose-one` for compose) with the ID. Report current status and last deployment.

4. **Pre-deploy checks (application mode only — skip for compose):**
   - **Environment variables:** MCP redacts `env` by default (since `@dokploy/mcp` 0.30.0): `env: null` still comes back as `null` and means "never set", but `[REDACTED]` means a string — possibly an empty one — so it cannot tell you whether any variable exists. In that case list the variable *names* over REST without printing values (recipe in the `mcp-patterns` skill, "Redaction"), or ask the user. Only if env is genuinely empty, read the project's local `.env.local` or `.env` file and set runtime env vars via `application-saveEnvironment` — it **replaces the whole `env` string**, so never call it to "add one variable" on an application that already has env. Separate build-time vars (e.g. `NEXT_PUBLIC_*`) from runtime-only vars — build-time vars must also go into `buildArgs`.
   - **Build type:** Check `buildType`. If the project has a `Dockerfile`, ask the user which build type to use (`dockerfile` or `nixpacks`). Default recommendation: `dockerfile` when a Dockerfile exists. Set via `application-saveBuildType` with all required fields (`applicationId`, `buildType`, `dockerfile`, `dockerContextPath`, `dockerBuildStage`, `herokuVersion`, `railpackVersion`).

5. **Deploy:**
   - **Compose mode:** Use `compose-deploy` MCP tool or REST API fallback. `compose-deploy` / `compose-redeploy` also accept `freshVolumes: true` (v0.30.5+) — it runs `docker compose down --volumes` first and **permanently deletes the stack's volumes**; use it only when the user explicitly asks for a clean slate, after a backup and an explicit confirmation (`docker-compose` type only, not swarm stacks).
   - **Application mode:** Use `application-deploy` MCP tool.

6. **Monitor until completion:**
   - Poll `deployment.all?applicationId=<id>` every 30-60 seconds to check latest deployment status.
   - If status is `done` — report success and verify the app is reachable (check health endpoint or domain).
   - If status is `error` — read the logs over MCP: build failure → `deployment-readLogs { deploymentId, tail }`; runtime crash → `application-readLogs { applicationId, tail, since, search }` or, for a compose stack, the per-container `compose-readLogs` loop (`/dokploy-dev:compose-logs`). Diagnose, fix it (update env vars, build type, Dockerfile, etc.), and redeploy. Repeat until deployment succeeds.
   - Show the user the build/runtime logs and errors transparently.

## Example Usage
```
/dokploy-dev:deploy web-frontend --project my-saas
/dokploy-dev:deploy abc123-def456
```