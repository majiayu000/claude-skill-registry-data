---
name: logs
description: 'Read runtime or build logs for a Dokploy application, compose stack, database, or deployment Arguments: <resource-name-or-id> [--type <app|compose|db|deployment>] [--tail <N>] [--since <1h>] [--search <term>].'
---

# Read Dokploy Logs

Unified log reader. Resolves the resource type and reads logs **directly over MCP/REST** (Dokploy v0.29.0+ — runtime logs are first-class over MCP/REST/CLI; no SSH/Beszel needed). For a multi-container compose stack, use `/dokploy-dev:compose-logs` instead — it reads every container.

Follow the `read-logs` skill (`${CLAUDE_PLUGIN_ROOT}/skills/read-logs/SKILL.md`) — load it first.

## Arguments

Format: `<resource-name-or-id> [--type <app|compose|db|deployment>] [--tail <N>] [--since <1h>] [--search <term>]`

- `resource-name-or-id` — required. Name or id of the app / compose / database / deployment.
- `--type` — optional. Force a resource type. If omitted, auto-detect: `application-one` → `compose-one` → `{type}-one` (postgres/mysql/mariadb/mongo/redis/libsql) → `deployment-allCentralized`.
- `--tail` — recent lines, `1`–`10000` (default `200`).
- `--since` — time window: `all` or `<n>{s|m|h|d}` (e.g. `30m`, `2h`). Default `all`.
- `--search` — server-side substring filter (e.g. `error`, `ECONNREFUSED`).

Parse from "$ARGUMENTS".

## Process

1. **Resolve the resource** (see arg notes for the auto-detect chain).

2. **Pick the right tool and read the log:**

   | Resource type | MCP call | Log kind |
   |---|---|---|
   | Application | `application-readLogs { applicationId, tail, since, search }` | runtime stdout/stderr |
   | Compose | per-container — **redirect to `/dokploy-dev:compose-logs <name>`** (enumerate containers, then `compose-readLogs { composeId, containerId, tail, since, search }` for each) | runtime, per container |
   | Database (any of 6) | `{type}-readLogs { {type}Id, tail, since, search }` | runtime stdout/stderr |
   | Deployment | `deployment-readLogs { deploymentId, tail }` (find the id via `deployment-all`/`deployment-allCentralized`) | build log |

   - The runtime-log `.data` is a newline-joined string, each line prefixed with an RFC3339 timestamp.
   - If a single `compose` resource is passed without `/compose-logs`, resolve `composeId` then read the **first** container but tell the user to run `/dokploy-dev:compose-logs <name>` to see all containers.

3. **Format the output:**
   - Show the last `--tail` lines.
   - Surface ERROR / FATAL / panic / exited / ECONNREFUSED / unauthorized lines first (see skill §6).
   - If a deployment is `status: error`, show the last 30 build-log lines up top.

4. **Suggest the next step** when an error pattern is found: `/dokploy-dev:analyze` (AI triage) or `/dokploy-dev:debug <id>` (full decision tree).

## Example Usage

```
/dokploy-dev:logs web-frontend --since 1h
/dokploy-dev:logs web-frontend --tail 500 --search error
/dokploy-dev:logs pg-main --type db --tail 500
/dokploy-dev:logs <deploymentId> --type deployment
# multi-container stack → use the dedicated command:
/dokploy-dev:compose-logs my-stack
```