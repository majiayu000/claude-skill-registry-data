---
name: "architecture-and-stack"
description: "Cloudflare-first platform selection. Decision trees for Workers, D1, R2, KV, DO, Queues, Vectorize, Containers, Sandboxes, Flagship, Agent Memory, Workflows v2. Default stack, override conditions, auth, data patterns, reliability."
metadata:
  version: "2.1.0"
  updated: "2026-05-03"
  effort: "high"
  model: "opus"
license: "Rutgers"
compatibility:
  claude-code: ">=2.0.0"
  agentskills: ">=1.0.0"
submodules:
  - ai-technology-integration.md
  - api-design-and-documentation.md
  - auth-and-session-management.md
  - background-jobs-and-workflows.md
  - cf-2026-updates.md
  - cf-auto-provision.md
  - coolify-docker-proxmox.md
  - drizzle-orm-and-migrations.md
  - enterprise-multi-tenancy.md
  - heartbeat-polling.md
  - mcp-and-cloud-integrations.md
  - openapi-generation.md
  - shared-api-pool.md
priority: 2
pack: "backend"
stage: stable
triggers:
  - "architecture"
  - "stack"
  - "cloudflare"
  - "d1"
  - "workers"
paths:
  - "concern:cloudflare-workers"
---

# 05 — Architecture and Stack

Default stack: `_kernel/standards.md#stack`. Override conditions below.

## Cloudflare-first decision tree

**Compute**: Workers (default, every HTTP/cron/queue) · Pages (static-only marketing, rare) · Containers (non-JS runtimes: Playwright headful, ffmpeg, Python ML, build orchestration) · Sandbox SDK (generated/risky code before live promotion)

**State**: D1 (default relational, ≤10GB/db, Sessions API read-replicas, Time Travel 30-day PIT) · KV (eventually-consistent, cache/sessions/feature-flags) · R2 (object storage, lifecycle Standard→IA after 30d) · Durable Objects (coordination + strongly-consistent SQLite storage since Apr 2025, chat rooms/builder sessions/rate-limiting) · Hyperdrive (front external Postgres/MySQL) · Vectorize (semantic search/RAG, 5M dim/index, topK 100, 10 metadata indexes)

**Async**: Queues (best-effort, 5000 msg/sec, R2 event notifications) · Workflows v2 (deterministic, 50K concurrent, 300 creates/sec, 2M queued/workflow, `step.do` + `step.sleep` + `step.waitForEvent`) · Inngest (event-driven, better DX/observability)

**AI**: Workers AI (Llama 3.3 70B FP8 free, Llama 3.1 8B FP8, Llama 4 Scout 17B vision) · AI Gateway (caching + rate-limit + fallback + logging for every LLM call) · Vectorize (embeddings + ANN search)

## Override conditions (when CF isn't enough)

| Need | Fallback | Adapter |
|---|---|---|
| Advanced SQL (RLS, OLAP, partial indexes) | Neon Postgres via Hyperdrive | `SqlPort` |
| Redis primitives at scale (sorted sets, streams) | Upstash Redis | `KvPort` |
| Sub-millisecond global state | Upstash QStash | `QueuePort` |
| Specific provider (OpenAI assistants, Anthropic batch) | Direct API via AI Gateway | `AiPort` |
| Vector + SQL co-located | Neon pgvector | `VectorPort` |

Adapters live in `libs/core/ports/`. Product code imports port, never vendor SDK directly. See `rules/cloudflare-hostable-supervisor.md`.

## Auth (default Clerk M2M JWT)

- **Clerk** — M2M JWT (free, networkless verification), passkeys, OAuth, magic links; **Better Auth** when Clerk pricing doesn't fit (rare)
- Hash API keys at rest. Audit log every sensitive action.
- Tenant isolation: every table carries `org_id`, every query filters by it (404 on mismatch, never 403)

## Data patterns

**D1**

```toml
[[d1_databases]]
binding = "DB"
database_name = "myapp"
```

- `wrangler types` against `compatibility_date` + bindings (preferred over hand-maintained Env interface)
- Drizzle v1 RQBv2 + Zod for query + validation; batch via `db.batch([...])` (no transactions in D1)
- Sessions API: `db.withSession(bookmark)` · Time Travel: `wrangler d1 time-travel restore`

**R2**: per-extension content-type on upload · lifecycle Standard→IA after 30d · event notifications → Queues at 5000 msg/sec for thumbnailing/indexing · versioning for asset rollback

**Durable Objects**: one DO per stateful entity · SQLite-backed, 10GB per DO · direct stub `env.MY_DO.getByName(name)` · alarm misfires → idempotent handler

## Reliability

- Workers CPU 10ms free / 50ms paid default (configurable 5min); wall time 30s paid
- `ctx.waitUntil()` for async post-response work; `ctx.passThroughOnException()` for graceful degradation
- WebSocket + JSRPC payload up to 32 MiB

## Cost discipline

- Workers free tier: 100k req/day; Workers Paid: $5/mo (10M req + 30M CPU-ms) + $0.30/M extra req + $0.02/M extra CPU-ms
- D1 on Workers Paid: 5GB + 25B rows-read + 50M rows-written/mo; then $0.75/GB-mo + $0.001/M rows-read + $1/M rows-written; no egress; read replication included (verified 2026-09-24 against developers.cloudflare.com — Workers/D1/R2 rates all unchanged)
- R2: 10GB free, $0.015/GB-mo, $0/egress · Workers AI Llama 3.3 70B FP8 FREE · AI Gateway free
- Solo SaaS <$100k/mo MRR stays 10-100× cheaper than AWS-equivalent on CF

## Default config (`wrangler.jsonc`)

```jsonc
{
  "name": "myapp",
  "main": "src/worker/index.ts",
  "compatibility_date": "2026-04-15",
  "compatibility_flags": ["nodejs_compat"],
  "observability": { "enabled": true },
  "secrets_required": ["CLERK_SECRET_KEY", "RESEND_API_KEY"],
  "d1_databases": [{ "binding": "DB", "database_name": "myapp" }],
  "kv_namespaces": [{ "binding": "CACHE", "id": "..." }],
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "myapp-assets" }],
  "ai": { "binding": "AI" }
}
```

## Decision template (use for every architecture call)

1. Can CF primitive do this? → Use it.
2. Does this need adapter for portability? → Adapter only if real business case.
3. Cost projection at 10× current scale → Still affordable?
4. Failure mode → Graceful degradation defined?
5. Migration path → If we have to leave CF, what does it cost?

## See submodules: cloudflare-primitives.md, data-patterns.md, reliability.md, auth-patterns.md.
