---
name: docker
description: Docker workflow helpers — list containers, build, run, logs, compose up/down, prune. Non-interactive only.
---

# Docker Skill

Run Docker operations in non-interactive mode.

## Usage

```
/docker ps                    # List running containers
/docker logs service-name     # Tail logs for a service
/docker build                 # Build the project image
/docker up                    # docker compose up -d
/docker down                  # docker compose down
/docker restart service       # Restart a specific service
/docker prune                 # docker system prune -f (no named volumes)
/docker shell service         # Open a shell in a running container
```

## Instructions

### Determine action from $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `ps` or (empty) | `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" \| cat` |
| `logs <service>` | `docker logs <service> --tail 50 \| cat` |
| `build` | Read `claude/build.md` for build command |
| `up` | `docker compose up -d 2>&1 \| tail -20` |
| `down` | `docker compose down 2>&1` |
| `restart <service>` | `docker compose restart <service> 2>&1` |
| `prune` | `docker system prune -f 2>&1` (confirm first) |
| `shell <service>` | `docker exec <container-id> /bin/sh` (non-interactive: run a command) |
| `images` | `docker images \| cat` |
| `stats` | `docker stats --no-stream \| cat` |

### ⚠️ Rules:
- NEVER use `docker exec -it` (interactive — hangs terminal)
- For `shell`: run a specific command instead: `docker exec <id> /bin/sh -c "ls /app"`
- For `prune`: warn about consequences before running
- For `logs`: always `--tail N` to limit output
- Read `claude/build.md` for project-specific Docker compose file paths and service names
