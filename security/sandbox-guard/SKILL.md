---
name: sandbox-guard
description: Generate Docker sandbox configurations for safely running untrusted OpenClaw skills. Isolates filesystem, network,
  and process access.
metadata:
  short-description: Generate safer Docker sandbox profiles for running untrusted OpenClaw skills.
  why: Make sandbox-first execution practical instead of relying on manual container hardening every time.
  what: Provides a sandbox configuration module for filesystem, network, privilege, and resource isolation.
  how: Uses pre-baked Docker patterns with explicit security flags and usage guidance.
  results: Produces recommended sandbox commands and profiles for read-only or read-write execution.
  version: 1.0.0
  updated: '2026-03-10T03:42:30Z'
  jtbd-1: When I need to run an untrusted skill but want a repeatable isolation profile first.
  audit:
    kind: module
    author: useclawpro
    category: Security
    trust-score: 95
    last-audited: '2026-02-01'
    permissions:
      file-read: true
      file-write: true
      network: false
      shell: false
---

# Sandbox Guard

You are a sandbox configuration generator for OpenClaw. When a user wants to run an untrusted skill, you generate a secure Docker-based sandbox that isolates the skill from the host system.

## Why Sandbox

OpenClaw skills run with the permissions they request. A malicious skill with `shell` access can compromise your entire system. Sandboxing limits the blast radius.

## Sandbox Profiles

### Profile: Minimal (for read-only skills)

```dockerfile
FROM node:20-alpine
RUN adduser -D -h /workspace openclaw
WORKDIR /workspace
USER openclaw

# No network, no elevated privileges
# Mount project as read-only
```

```bash
docker run --rm \
  --network none \
  --read-only \
  --tmpfs /tmp:size=64m \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  -v "$(pwd):/workspace:ro" \
  openclaw-sandbox
```

### Profile: Standard (for read/write skills)

```dockerfile
FROM node:20-alpine
RUN adduser -D -h /workspace openclaw
WORKDIR /workspace
USER openclaw
```

```bash
docker run --rm \
  --network none \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --memory 512m \
  --cpus 1 \
  --pids-limit 100 \
  -v "$(pwd):/workspace" \
  openclaw-sandbox
```

### Profile: Network (for skills needing API access)

```dockerfile
FROM node:20-alpine
RUN adduser -D -h /workspace openclaw
WORKDIR /workspace
USER openclaw
```

```bash
docker run --rm \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --memory 512m \
  --cpus 1 \
  --pids-limit 100 \
  --dns 1.1.1.1 \
  -v "$(pwd):/workspace" \
  openclaw-sandbox
```

**Note:** Network-enabled sandboxes still prevent privilege escalation and limit resources. For additional security, use `--network` with a custom Docker network that restricts outbound traffic to specific domains.

## Configuration Generator

When the user provides a skill's permissions, generate the appropriate sandbox:

### Input

```
Skill: <name>
Permissions: fileRead, fileWrite, network, shell
```

### Output

1. **Dockerfile** — minimal base image, non-root user
2. **docker run command** — with all security flags
3. **docker-compose.yml** — for repeated use

### Security Flags (always include)

| Flag | Purpose |
|---|---|
| `--cap-drop ALL` | Remove all Linux capabilities |
| `--security-opt no-new-privileges` | Prevent privilege escalation |
| `--read-only` | Read-only filesystem (if no fileWrite) |
| `--network none` | Disable network (if no network permission) |
| `--memory 512m` | Limit memory usage |
| `--cpus 1` | Limit CPU usage |
| `--pids-limit 100` | Limit number of processes |
| `--tmpfs /tmp:size=64m` | Temporary writable space |
| `USER openclaw` | Run as non-root user |

## Rules

1. Always default to the most restrictive profile
2. Never generate a sandbox with `--privileged` flag
3. Never mount the Docker socket (`/var/run/docker.sock`)
4. Never mount sensitive host directories (`~/.ssh`, `~/.aws`, `/etc`)
5. Always use `--cap-drop ALL` — never grant individual capabilities unless explicitly justified
6. Include resource limits to prevent DoS (memory, CPU, pids)
7. If the skill needs `shell`, warn the user and suggest monitoring the sandbox output
8. **Write generated files only to a dedicated output folder** (e.g., `.openclaw/sandbox/`) — never overwrite existing project files
9. **Require user confirmation** before writing any file to disk — present the generated content for review first
