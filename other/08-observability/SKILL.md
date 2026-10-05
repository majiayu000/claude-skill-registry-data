---
name: observability
description: Health endpoints, structured logging, correlation IDs, monitoring workflows, and alert hooks.
when_to_use:
  - Production readiness review
  - Incident debugging
  - Adding health checks
  - Setting up alerting
---

# Observability (RESTO BOT)

## Health endpoints

| Service | Endpoint | Check |
| --- | --- | --- |
| gateway | `http://127.0.0.1:8080/healthz` | wget |
| n8n-main | `http://127.0.0.1:5678/healthz` | wget |
| n8n-worker | `pgrep -f 'n8n worker'` | process check |
| postgres | `pg_isready -U n8n -d n8n` | pg_isready |
| redis | `redis-cli ping` | redis-cli |
| cms (Strapi) | `http://127.0.0.1:1337/_health` | wget |
| admin-dashboard | `http://127.0.0.1:80/` | wget |
| kiosk-app | `http://127.0.0.1:80/` | wget |

## Logging configuration

All services use `json-file` driver with rotation:
- Critical services (n8n, postgres, redis, gateway, cms): max-size=10m, max-file=5
- Frontend (admin-dashboard, kiosk-app): max-size=5m, max-file=3

## Log masking

`LOG_MASK_PATTERNS=token,password,secret,api_key,authorization,x-api-token,x-webhook-token,bearer`

## Structured logging schema

Target fields for every log entry:
- timestamp, level, service, correlation_id
- route, status, latency_ms, error_code (where applicable)

## Correlation ID propagation

Flow: gateway (X-Request-ID) -> n8n workflows -> DB writes

## SLO monitoring (n8n env vars)

- `SLO_WINDOW_MIN=15` (sliding window)
- `SLO_INBOUND_TO_OUTBOX_P95_MS=2000` (2s target)
- `SLO_OUTBOX_PENDING_AGE_MAX_SEC=600` (10min max pending)
- `SLO_DLQ_RATE_MAX=0.05` (5% max failure rate)
- `SLO_DLQ_COUNT_MAX=5` (absolute DLQ cap)

## Alert hook

`ALERT_WEBHOOK_URL` env var (can point to Slack, Discord, or monitoring webhook)

## Key files

- `project/docker-compose.hostinger.prod.yml` (healthchecks, logging config)
- `project/.env` (SLO_*, ALERT_*, LOG_MASK_PATTERNS)
- `project/infra/gateway/nginx.conf` (access log format, redaction)
- `project/scripts/smoke_security.sh` (health check validation)

## Required output

- Health endpoints list + expected outputs
- Logging schema documented
- Smoke tests extended to include health checks
- Incident "what to look at first" checklist
