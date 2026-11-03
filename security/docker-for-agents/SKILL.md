---
name: docker-for-agents
description: "Use when containerising an agent with Docker Compose. Compose template with env_file, restart policy, healthcheck, volumes and log limits, a .dockerignore, secrets kept out of images, pinned tags, and the daily compose commands."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, docker, compose, containers, server]
    related_skills: [server-agent-service, backups-restore, watchdog-keepalive, server-troubleshooting, consent]
---

# Docker for agents — small, pinned, non-root containers

## When to use
- The owner wants an agent, bot or tool isolated in a container, or runs several services on one server.
- A container restarts in a loop, fills the disk with logs, or leaks a secret into an image.

Docker is not bundled with iclone os: every command here is an example and `docker compose --help` plus the Compose spec are the truth. A plain systemd unit (`server-agent-service`) is lighter when one service is all you run.

## Prerequisites
- Installing Docker needs `installSoftware`; building, starting or removing containers needs `terminal`. Ask through the consent door (`~/.iclone-os/bin/acp consent request installSoftware --reason "…"`), name the host and the service, and wait for the owner's yes.

## Quick reference
| Rule | Why |
|---|---|
| `image: <name>:<version>` (or `@sha256:` digest), never `latest` | same bits on every restart |
| `restart: unless-stopped` + `healthcheck` | comes back, and you can see when it is sick |
| `user:` non-root, `read_only: true`, `cap_drop: [ALL]` | a compromised agent cannot own the host |
| `env_file:` 0600, outside git | secrets never in the image or the compose file |
| log `max-size` / `max-file` | json logs otherwise grow until the disk is full |

## Procedure
1. `.dockerignore` next to the Dockerfile, at least: `.git`, `.env*`, `*.log`, `node_modules`, `__pycache__`, `*.pem`, `*.key`.
2. Dockerfile: pinned base image, dependencies first, `USER` non-root at the end. Never pass secrets with `ARG` or `ENV`: they stay in the layers (`docker history`).
3. `compose.yaml`:
```yaml
# example
services:
  <service>:
    image: <registry>/<service>:<version>
    build: .
    env_file: ./<service>.env
    restart: unless-stopped
    user: "10001:10001"
    read_only: true
    tmpfs: [/tmp]
    cap_drop: [ALL]
    security_opt: ["no-new-privileges:true"]
    volumes:
      - <service>-data:/data
    healthcheck:
      test: ["CMD", "<health-command>"]
      interval: 30s
      timeout: 5s
      retries: 3
    logging:
      driver: json-file
      options: { max-size: "10m", max-file: "3" }
volumes:
  <service>-data:
```
4. Secrets file, then validate and start:
```sh
chmod 600 <service>.env && docker compose config --quiet && docker compose up -d --build  # example
```
5. Daily commands:
```sh
docker compose ps && docker compose logs -f --tail 200 <service>  # example
```
6. Update: bump the tag in `compose.yaml`, then:
```sh
docker compose pull --ignore-buildable && docker compose up -d  # example
```
7. Stop: `docker compose down` keeps named volumes. `down -v` deletes the data: owner's yes, after `backups-restore`.

## Pitfalls
- Published ports skip ufw: Docker writes its own firewall rules. Publish only what must be public; for a reverse proxy on the same host, bind with `host_ip` set to the loopback address.
- A loop of restarts with no logs: the healthcheck command itself is missing in the image.
- A new named volume copies the owner of the image's mount dir; if `/data` does not exist in the image it is root-owned and `user: "10001:10001"` cannot write it. Create it in the Dockerfile owned by that uid (`RUN mkdir /data && chown 10001:10001 /data`) before the first `up`.
- `read_only: true` breaks programs that write into their install dir; give them a volume or `tmpfs`.
- Disk full: `docker system df`, then prune unused images with the owner's yes (`server-troubleshooting`).

## Never
- Never mount `/var/run/docker.sock` into an agent container or run it `privileged`: both equal root on the host.
- Never add an untrusted user to the `docker` group (same as root).
- Never bake `.env`, keys or tokens into an image or push such an image.

## Verification
```sh
docker compose ps --format '{{.Name}} {{.Status}}'  # example
```
Pass = every service shows `Up` with `(healthy)`, and `docker history <registry>/<service>:<version>` shows no secret values.
