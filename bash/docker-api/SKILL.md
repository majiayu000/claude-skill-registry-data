---
name: Docker API
description: Inspect and control local Docker containers.
requires:
  bins: [docker]
  env: []
---

# Docker API

Wraps the `docker` CLI so kate can report on and control containers.
Read operations are unrestricted; lifecycle actions (start/stop/restart)
are gated by `DOCKER_API_ALLOW_WRITE=true`.

## Tools
- `status`
- `ps(all?, filter?)` — list containers
- `inspect(target)` — full metadata
- `logs(target, lines?, since?)` — last N lines
- `stats(target)` — one-shot CPU/mem/net
- `start†(target)`, `stop†(target, timeout_secs?)`, `restart†(target, timeout_secs?)`

Container names are regex-validated as `[A-Za-z0-9][A-Za-z0-9_.-]*` to block shell injection.
