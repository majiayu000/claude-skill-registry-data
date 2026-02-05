---
name: observability-metrics
description: Operate and validate mjr.wtf observability endpoints (/health, /metrics) and logging-related behavior. Use when adding metrics, changing auth around metrics, or debugging production-like issues.
license: MIT
compatibility: Requires bash and curl; server must be running.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.2
allowed-tools: Bash(git:*) Bash(curl:*) Bash(make:*) Bash(go:*) Read
---

## Tooling assumptions

- Use a terminal runner with bash and git available.
- Prefer `make` targets when available; fall back to direct CLI commands when needed.

## Endpoints

- `GET /health` (public): readiness/liveness check.
- `GET /metrics` (Prometheus): may be optionally protected.

## Validate locally

```bash
curl -i http://localhost:8080/health
curl -i http://localhost:8080/metrics
```

If metrics auth is enabled:

```bash
# Use any token from AUTH_TOKENS
curl -i -H "Authorization: Bearer $YOUR_TOKEN" http://localhost:8080/metrics
```

## Security note

Treat `/metrics` as potentially sensitive (rates, error counts, operational info). Enable protection in production with `METRICS_AUTH_ENABLED=true` or restrict via reverse proxy.
