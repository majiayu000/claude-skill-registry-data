---
name: deployment
description: "Reference for deploying and configuring this project on Railway — service list, domain routing, environment variables, and the shared Supabase connection. Use this for any deployment task, new service setup, env var changes, domain/DNS configuration, or production issues."
---

# Deployment — Railway

## One Project, Multiple Services

All services live in a single Railway project, each as its own Railway "service" with its own build, its own env vars, and its own runtime — but sharing the project's networking so they can reach each other internally.

| Railway service | Source folder | Runtime | Public domain |
|---|---|---|---|
| store-backend | `store/backend` | Node.js | `mysite.com/api` |
| storefront | `store/storefront` | Node.js | `mysite.com` |
| ai-gateway | `studio/ai-gateway` | Node.js | internal only |
| dubbing | `studio/dubbing` | Python | `studio.mysite.com/api/dub` |
| bot-bridge | `studio/bot-bridge` | Node.js | internal only |
| comment-bot | `studio/comment-bot` | Node.js | `studio.mysite.com/webhooks/comments` |
| tts-service | `studio/tts-service` | Python | internal only |
| chatwoot | `studio/chatwoot` | Docker compose | `studio.mysite.com/chat` |

Railway handles HTTPS automatically for all public domains.

## Domain / Subdomain Setup

1. Point `mysite.com` (apex + www) at the `storefront` service (with `/api/*` routed to `store-backend`)
2. Point `studio.mysite.com` at a routing layer that sends:
   - `/chat/*` → `chatwoot` service
   - `/webhooks/comments` → `comment-bot` service
   - `/api/dub/*` → `dubbing` service

## Environment Variables Per Service

Cross-reference each service's `.env.example` (per `project-architecture` skill) — this table is the deployment-time checklist, not the source of truth for what each var does.

| Service | Needs |
|---|---|
| store-backend | `DATABASE_URL` (Medusa's own), `AI_GATEWAY_URL`, `INTERNAL_API_KEY`, Medusa config |
| storefront | `NEXT_PUBLIC_MEDUSA_BACKEND_URL` |
| bot-bridge | `CHATWOOT_URL`, `CHATWOOT_API_TOKEN`, `AI_GATEWAY_URL`, `INTERNAL_API_KEY` |
| comment-bot | `FB_PAGE_ACCESS_TOKEN`, `FB_APP_SECRET`, `FB_VERIFY_TOKEN`, `AI_GATEWAY_URL`, `INTERNAL_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` |
| dubbing | `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`, `R2_ENDPOINT`, `AI_GATEWAY_URL`, `INTERNAL_API_KEY`, `TTS_SERVICE_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` |
| ai-gateway | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `MINIMAX_API_KEY`, `INTERNAL_API_KEY` |
| tts-service | `MODEL_PATH`, `INTERNAL_API_KEY` |
| chatwoot | standard Chatwoot env vars |

`SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY` are the same values across all services (shared database) — set once, copy to each service's variables in Railway.

## Service-to-Service URLs (internal)

Use Railway's internal networking hostnames for service-to-service calls where possible (faster, doesn't leave Railway's network) — e.g. `AI_GATEWAY_URL=http://ai-gateway.railway.internal:PORT` rather than a public URL, for calls that originate from another Railway service in the same project. Public domains (`studio.mysite.com/...`) are only needed for calls originating from outside Railway (Meta webhooks, Telegram webhooks, browser).

## New Service Checklist

When `architect` or any builder agent introduces a new service:
1. Add it to the table above (this file) and to `project-architecture`'s service table
2. Create the Railway service, pointing at the correct subfolder
3. Copy required env vars from its `.env.example`
4. Add routing rule if it needs a public path under `studio.mysite.com`
5. Confirm it can reach `AI_GATEWAY_URL` and Supabase using internal networking

## Monitoring

- Railway's built-in logs per service are the first stop for crashes/restarts
- The `ai_requests` or `ai_usage_logs` table (written by ai-gateway) is the first stop for AI cost/behavior issues — see `debugging-playbook` skill
- Set up a simple uptime check (even a free external pinger) against `mysite.com` and `studio.mysite.com/chat` — these are the domains real users/customers touch directly

