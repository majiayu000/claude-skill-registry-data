---
name: n8n_queue_sre
description: Ensure n8n queue mode reliability - idempotency, DLQ, outbox, worker scaling, timeout coherence.
when_to_use:
  - Queue backlog or stuck executions
  - Duplicate processing detected
  - Scaling workers
  - Production readiness review
  - Adding new workflows
---

# n8n Queue SRE (RESTO BOT)

## Current topology

- **n8n-main** (image: n8n:1.80.0): Webhook receiver, queue publisher
  - Resources: 1 CPU, 1GB RAM
  - Health: `wget http://127.0.0.1:5678/healthz`
- **n8n-worker**: Queue consumer, execution engine
  - Resources: 0.75 CPU, 768MB RAM
  - Health: `pgrep -f 'n8n worker'`
  - Concurrency: `QUEUE_BULL_MAX_CONCURRENCY` (default: 2)
- **Redis 7-alpine**: Bull queue backend
  - AOF persistence, 256MB max, allkeys-lru eviction
  - Health: `redis-cli ping`

## Business logic env vars (n8n-main + worker)

- Multi-channel: WA_SEND_URL, IG_SEND_URL, MSG_SEND_URL + API tokens
- Outbox: OUTBOX_MAX_ATTEMPTS=7, BASE_DELAY=30s, MAX_DELAY=3600s
- Fraud: FRAUD_FLOOD_LIMIT_30S=6, HIGH_ORDER_THRESHOLD=3000000
- SLO: INBOUND_TO_OUTBOX_P95=2000ms, PENDING_AGE_MAX=600s, DLQ_RATE_MAX=0.05

## Non-negotiables

- Webhooks respond quickly (ack fast, process async via queue)
- Idempotency gate near ingestion (dedupe key stored in DB)
- Retries with exponential backoff; cap retries at OUTBOX_MAX_ATTEMPTS
- Dead-letter path: error workflow + durable store
- Worker concurrency explicit and measured
- Redis durability: AOF enabled

## Operational checks

- Monitor queue depth and failed executions
- Ensure worker restarts do not cause duplicate side effects
- Ensure timeouts are coherent: Traefik (30s) -> gateway (read_timeout) -> n8n (execution_timeout)
- Verify outbox pattern: pending -> processing -> sent/failed/DLQ

## Key files

- `project/docker-compose.hostinger.prod.yml` (n8n-main, n8n-worker, redis services)
- `project/.env` (QUEUE_*, OUTBOX_*, SLO_*, FRAUD_* vars)
- `project/workflows/` (54 workflow JSON files)
- `project/scripts/n8n-worker-entrypoint.sh` (worker startup)

## Required output

- Queue reliability plan (env + settings)
- Incident playbook: worker crash loop, stuck queue, redis down
- Verification: simulate inbound event -> single DB write -> idempotent re-send
