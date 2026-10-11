---
name: debug
description: 'Debug a failed or stuck Dokploy deployment with full decision-tree analysis Arguments: app-name-or-id|compose-id.'
---

# Debug Failed Deployment

Run the full `debug-deploy` workflow against an application or compose stack — locate the failed run, read build logs, inspect container state, check Traefik, optionally AI-summarise, and recover.

## Arguments

Format: `[app-name-or-id|compose-id]` (optional)

- If a UUID is passed, treat it as either an `applicationId` or `composeId` and disambiguate by calling `application-one` first, falling back to `compose-one`.
- If a name is passed, call `project-all` to resolve.
- If **no argument** is passed, call `mcp__plugin_dokploy-dev_dokploy__deployment-allCentralized` and `mcp__plugin_dokploy-dev_dokploy__deployment-queueList`, list the recent `error` / stuck deployments, and ask the user which to investigate.

Parse from "$ARGUMENTS".

## Process

Read `${CLAUDE_PLUGIN_ROOT}/skills/debug-deploy/SKILL.md` and follow every step in order. Do not skip.

Key checkpoints:

1. **Step 0 — Platform health.** Run `settings-health`, `checkInfrastructureHealth` (returns `postgres` / `traefik` status), `getDockerDiskUsage`, and on v0.30+ the read-only host check `docker-getServerHealth` (disk, memory, inotify, network IP pools, daemon errors) plus `docker-getEvents { minutes }` for recent daemon activity. If any fail, fix server before deploy issue.
2. **Step 1 — Locate the failed run.** Use `deployment-all` filtered by the resource ID. Save `deploymentId`.
3. **Step 2 — Read the logs (Dokploy v0.29.0+ — runtime logs are first-class over MCP/REST/CLI; see the `read-logs` skill).** Build failure → `deployment-readLogs { deploymentId, tail }`. Runtime crash → `application-readLogs { applicationId, tail, since, search }` for an app, or **read every container** of a compose stack: `docker-getContainersByAppNameMatch { appName, appType: "docker-compose" }` then `compose-readLogs { composeId, containerId, tail, since, search }` per container (or `/dokploy-dev:compose-logs`). Match against the build-failure pattern table.
4. **Step 3 — Container introspection.** `docker-getContainersByAppLabel { appName, type: "standalone" }` for state/health. `docker-getConfig` for command/mounts/networks (its `Env` is `[REDACTED]` by default since `@dokploy/mcp` 0.30.0 — diagnose env problems from the logs, see the `debug-deploy` skill "Env and credentials"). Use `docker-restartContainer` / `killContainer` if wedged.
5. **Step 4 — Request path.** Only if container is running but HTTP requests fail. `application-readTraefikConfig`, check port, network, listen address.
6. **Step 5 — Recovery.** Use the smallest action that unblocks: `killBuild` / `cancelDeployment` / `cleanQueues` / `deployment-removeDeployment` / `rollback-rollback`. Confirm destructive ops with the user.
7. **Step 6 — AI summary.** If `ai-getEnabledProviders` is non-empty, pass the log text from Step 2 to `ai-analyzeLogs { aiId, logs, context: "build" | "runtime" }` and present the result. Otherwise note that AI is not configured and continue manually.
8. **Step 7 — Verify the fix.** After applying a fix, `application-redeploy` (or `compose-redeploy`), poll `deployment-all` until `status: done`, validate domains, hit the endpoint with curl.

## Output format

Report findings in this structure:

```
## Diagnosis: <appName / composeName>

**Failed deployment:** <deploymentId> (status: error, started: <timestamp>)
**Build log:** <logPath>

### Root cause
<one-paragraph plain-language explanation>

### Evidence
- <log excerpt 1>
- <container state observation>
- <traefik / domain observation if relevant>

### AI summary (if available)
<ai-analyzeLogs output, condensed>

### Recommended fix
<concrete action, with the exact MCP call(s) needed>

### Recovery commands
<list of MCP calls to apply the fix and redeploy>
```

After applying a fix, re-verify before declaring the issue resolved.

## Example Usage

```
/dokploy-dev:debug
/dokploy-dev:debug web-frontend
/dokploy-dev:debug abc123-def456
```