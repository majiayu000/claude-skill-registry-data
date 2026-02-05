---
name: twelve-factor
description: 12 Factor App methodology for web applications and microservices.
---

# The Twelve-Factor App

## Factors

| #    | Factor              | Principle                                    |
| ---- | ------------------- | -------------------------------------------- |
| I    | Codebase            | One codebase tracked in VCS, many deploys    |
| II   | Dependencies        | Explicitly declare and isolate dependencies  |
| III  | Config              | Store config in environment variables        |
| IV   | Backing services    | Treat backing services as attached resources |
| V    | Build, release, run | Strictly separate build and run stages       |
| VI   | Processes           | Execute app as stateless processes           |
| VII  | Port binding        | Export services via port binding             |
| VIII | Concurrency         | Scale out via the process model              |
| IX   | Disposability       | Fast startup and graceful shutdown           |
| X    | Dev/prod parity     | Keep development and production similar      |
| XI   | Logs                | Treat logs as event streams                  |
| XII  | Admin processes     | Run admin tasks as one-off processes         |

## Checklist

- [ ] No hardcoded config (use env vars)
- [ ] Dependencies in manifest (package.json, go.mod, etc.)
- [ ] Stateless processes (no local session state)
- [ ] Logs to stdout (no local log files)
- [ ] Graceful shutdown handling
- [ ] Health check endpoints
