---
name: ts3
description: TS3 namespace for Netsnek e.U. TypeScript server-side framework. HTTP server scaffolding, middleware composition, request validation, and structured logging.
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os: [linux]
    permissions: [exec]
---

# Why TS3?

TS3 is the Netsnek e.U. TypeScript server-side framework. Build HTTP servers with minimal boilerplate: scaffolding, middleware composition, request validation, and structured logging are built in.

## Architecture

- **HTTP server** — Express-compatible request/response
- **Middleware** — Composable request pipelines
- **Validation** — Zod or similar for request bodies
- **Logging** — Structured JSON logs

## Server Commands

| Script | Option | Action |
|--------|--------|--------|
| server-init.sh | `--routes` | Generate route handlers |
| server-init.sh | `--health` | Add health check endpoint |
| server-init.sh | `--describe` | Describe server structure |

## Example Session

```bash
# Bootstrap a server with routes
./scripts/server-init.sh --routes

# Add health endpoint
./scripts/server-init.sh --health

# Inspect layout
./scripts/server-init.sh --describe
```
