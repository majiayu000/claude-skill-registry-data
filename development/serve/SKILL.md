---
name: serve
description: Start service(s) locally for development. Accepts a service name, all, frontend, or backend. Reads claude/build.md for the actual start commands.
---

# Serve Skill

Start service(s) locally for development.

## Usage

```
/serve                  # Start default service (or show options)
/serve all              # Start all services
/serve frontend         # Start frontend only
/serve backend          # Start backend only
/serve <service-name>   # Start a specific named service
```

## Instructions

**First:** Read `claude/build.md` for local development setup and service definitions.

### Determine scope from $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `<service-name>` | `{{SERVE_CMD_SINGLE}} <service-name>` |
| `all` | `{{SERVE_CMD_ALL}}` |
| `frontend` | `{{SERVE_CMD_FRONTEND}}` |
| `backend` | `{{SERVE_CMD_BACKEND}}` |
| (empty) | Show available services from `claude/build.md` |

### Rules:
- Run services in background (async) so the session stays responsive
- After starting, show the expected URLs (from `claude/build.md`)
- If a port is already in use: report the conflict and suggest `lsof -i :<port>` to identify the process
- NEVER run interactive servers in foreground — use background execution

### Example (if claude/build.md has commands):
```bash
# Backend
pnpm --filter api dev &

# Frontend
pnpm --filter web dev &
```
