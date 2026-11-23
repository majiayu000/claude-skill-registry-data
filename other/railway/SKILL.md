---
name: railway
description: >-
  Deploys and operates apps on Railway: create or link projects and services, railway up, add
  Postgres, Redis, MySQL or MongoDB, variables and build config, domains, logs and failed builds,
  metrics, PR deploys and templates, plus answers from Railway docs and Central Station. Use when
  the user mentions Railway, railway up, Railpack or Central Station, or asks how a Railway
  feature works. Not for Vercel (use deploy-to-vercel).
---

# Railway

One skill for everything on Railway. Read the topic file that matches the request, then follow it. Load only the topics you need.

## Prerequisites

```bash
command -v railway && railway whoami
```

If the CLI is missing or logged out, follow the install and login steps in [references/new.md](references/new.md). The GraphQL helper `scripts/railway-api.sh` (path relative to this skill folder) is used by the database, metrics, projects, service and templates topics.

## Routing

| The user wants to… | Topic |
|---|---|
| Set up Railway for the first time, "deploy to railway" when nothing is linked, create a project or service, deploy from a GitHub repo, link a directory | [new](references/new.md) |
| Push code that is already linked ("railway up", "ship", "redeploy my changes") | [deploy](references/deploy.md) |
| Manage existing deployments: list, logs, build errors, why a deploy failed, restart, redeploy, stop, remove | [deployment](references/deployment.md) |
| Ask "is it running", "what's deployed", deployment status or uptime | [status](references/status.md) |
| Add a database (Postgres, Redis, MySQL, MongoDB) and wire `DATABASE_URL` / `REDIS_URL` | [database](references/database.md) |
| Add any other template service (n8n, Ghost, Strapi, Minio, Uptime Kuma…) | [templates](references/templates.md) |
| View or change variables, build/start commands, root directory, replicas, repo source, delete a service | [environment](references/environment.md) |
| Service status, rename, icon, link services, create a service from a Docker image | [service](references/service.md) |
| Add, generate, list or remove domains; get a service URL | [domain](references/domain.md) |
| CPU, memory, network, disk usage; "is my service slow" | [metrics](references/metrics.md) |
| List, switch, rename projects; PR deploys; public/private | [projects](references/projects.md) |
| How a Railway feature works, or a docs.railway.com link | [docs](references/docs.md) |
| Search Central Station community threads or support questions | [central-station](references/central-station.md) |

When two topics could apply, use this order. If the directory is not linked yet, use **new**. If it is linked and the user only wants to ship code, use **deploy**. If something already deployed is broken, use **deployment** (and **metrics** for performance).

## Shared references

- [variables.md](references/variables.md): variable syntax, references between services, wiring patterns.
- [environment-config.md](references/environment-config.md): every environment/service config field.
- [monorepo.md](references/monorepo.md): root directories and multi-service repos.
- [railpack.md](references/railpack.md): how Railway builds code and how to fix build or start commands.

## Rules

- Never print secret variable values back to the user.
- Confirm before destructive actions: deleting services or volumes, removing deployments, detaching domains.
- After any deploy, report the deployment status and the service URL. If it fails, read the logs (deployment topic) before guessing.
