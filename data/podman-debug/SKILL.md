---
name: podman-debug
description: Diagnose and troubleshoot Podman container issues. Use when the user says "container crashing", "podman logs", "debug container", "container not starting", "exec into container", or asks why a container is failing.
allowed-tools: Bash, Read, Grep
---

# Podman Debug

Diagnose container issues, inspect logs, and troubleshoot Podman containers.

## Instructions

1. Run `podman ps -a` to see all containers and their states
2. Identify the problematic container by name or ID
3. Check container logs with `podman logs <container>`
4. Inspect container config with `podman inspect <container>`
5. If needed, exec into running container: `podman exec -it <container> /bin/sh`
6. Report findings and suggest fixes

## Common diagnostic commands

```bash
# Container status and health
podman ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
podman healthcheck run <container>

# Logs with timestamps
podman logs -t --since 10m <container>
podman logs -f <container>  # follow

# Resource usage
podman stats --no-stream

# Inspect specific fields
podman inspect -f '{{.State.ExitCode}}' <container>
podman inspect -f '{{.State.Error}}' <container>
podman inspect -f '{{json .NetworkSettings}}' <container>

# Container processes
podman top <container>

# Events
podman events --since 1h --filter container=<name>
```

## Common issues and solutions

| Symptom             | Check                  | Likely Cause                 |
| ------------------- | ---------------------- | ---------------------------- |
| Exit code 137       | `dmesg \| grep -i oom` | OOM killed - increase memory |
| Exit code 1         | `podman logs`          | Application error            |
| Exit code 126       | Entrypoint permissions | `chmod +x` on entrypoint     |
| Exit code 127       | Entrypoint path        | Command not found in image   |
| Network unreachable | `podman network ls`    | Network not attached         |

## Rules

- MUST check logs before suggesting fixes
- MUST report exit codes and their meaning
- Never restart containers without user approval
- Never remove containers or volumes without explicit request
- Always suggest `--rm` flag for debug containers
