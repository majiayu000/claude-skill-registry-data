---
name: backend-architecture
description: Design backends that survive redeploys, server reboots, and modest scaling. Covers stateless application servers, state placement (object storage, managed databases, Redis), immutable deploy artifacts, health checks, graceful shutdown, database migrations that don't lock the world, and the twelve-factor baseline. Invoke when designing a new backend, when uploads disappear after a redeploy, or when productionizing a vibe-coded prototype.
---

# Backend Architecture — the Solutions Architect Baseline

The most common mistake in vibe-coded backends is treating the application server as if it were a desktop computer: state lives where the code lives, the disk is permanent, restarts are exceptional, one instance runs forever. None of that survives contact with production.

This skill is the **architectural baseline** that makes a backend production-ready. It is not security-specific — but a backend that loses data, drops jobs, or rolls back to a half-state during deploys is also a backend whose incident-response surface looks much larger than it should. Pairs with the hardening skills, but operates at a different layer.

## When to invoke

- "User uploads disappeared after we redeployed"
- "The site went down during deploy and we lost the in-flight orders"
- "I need to scale to a second server but nothing works when there are two"
- "We're moving from prototype to production"
- "We're handing off the codebase to a team that has to run it"
- Designing a new backend from scratch and you want the decisions correct on day one
- Reviewing an inherited backend before scaling user count or revenue

## The single most important rule

> **App servers are cattle. State lives elsewhere.**

Any data that must survive a deploy, reboot, container restart, or instance replacement is **state**. State does not belong on the app server's local disk, in its memory, or anywhere bound to the instance's lifetime. It belongs in a system designed for durability.

This rule, followed consistently, eliminates 80% of "where did my data go?" incidents.

## The state-placement decision matrix

For every piece of data your app handles, decide where it lives **before** writing the code:

| Data type | Right place | Wrong place |
|---|---|---|
| User-uploaded files (images, PDFs, docs) | Object storage (S3, R2, B2, Spaces) behind a CDN | App server's `uploads/` directory |
| Generated thumbnails / derivatives | Object storage, or regenerated on-demand from originals | App server's filesystem |
| Database rows (orders, users, posts) | Managed Postgres / MySQL, or a dedicated DB VM with backups | SQLite next to the app code |
| Session data | Redis, managed cache, or DB-backed sessions | In-process memory (`Map`, `WeakMap`) |
| Cache (computed data, hot reads) | Redis / Memcached / Cloudflare KV | Local memory if and only if loss-tolerant |
| Background-job state | Persistent queue (BullMQ + Redis, AWS SQS, GCP Pub/Sub, NATS JetStream) | `setTimeout` / `setInterval` in the web process |
| Logs | Centralized log destination (Loki, hosted, syslog forwarding) | App server's `/var/log` only |
| Secrets | Env vars from a secret manager, or runtime injection | `.env` checked into the image / repo |
| Search index | Managed search (Algolia, Meilisearch, Elasticsearch, Postgres GIN) | Recomputed from DB on every request |
| Email-sending | Transactional ESP (Postmark, Mailgun, SES, Resend) | Direct SMTP from the app server in production |

Every "Wrong place" row in the table is a real outage waiting to happen. Walk this list against your current codebase — anything misplaced is a refactor candidate.

## The "images disappear on redeploy" trap — concretely

This one bites everyone once. Anatomy:

1. App is built as a Docker image. Image is immutable.
2. App writes uploaded images to `./uploads/` (relative to working directory inside the container).
3. Deploy: new image is pulled, old container stopped, new container started.
4. The new container has a fresh filesystem from the image. The `uploads/` directory exists but is empty.
5. All previously-uploaded user images now return 404.

The same trap occurs without Docker: PaaS platforms (Heroku, Railway, Fly, Render) typically run on ephemeral filesystems. The "disk" is a feature of the container, not the platform.

### Fix — use object storage

```ts
// Bad — writes to local disk that disappears on redeploy
import fs from 'node:fs/promises';
async function saveUpload(file: Buffer, key: string) {
  await fs.writeFile(`./uploads/${key}`, file);
  return `/uploads/${key}`;   // served by app, lost on deploy
}

// Good — write to S3-compatible storage; URL is permanent
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const s3 = new S3Client({
  region: 'auto',
  endpoint: process.env.S3_ENDPOINT,        // R2: https://<acct>.r2.cloudflarestorage.com
  credentials: {
    accessKeyId: process.env.S3_ACCESS_KEY_ID!,
    secretAccessKey: process.env.S3_SECRET_ACCESS_KEY!,
  },
});

async function saveUpload(file: Buffer, key: string) {
  await s3.send(new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    Body: file,
    ContentType: detectMime(file),
  }));
  return `${process.env.CDN_BASE_URL}/${key}`;  // served by CDN, survives redeploy
}
```

**Recommended stack** (cheap and fast for small/medium projects):

- **Cloudflare R2** for storage — zero egress fees, S3-compatible API
- **Cloudflare custom domain** in front of R2 for the public URLs
- **Pre-signed URLs** for uploads if you want the browser to upload directly to R2 (bypasses your app server for big files)

Alternatives: AWS S3 + CloudFront, Backblaze B2, DigitalOcean Spaces, MinIO if you must self-host.

See [`cloudflare-hardening`](../cloudflare-hardening/SKILL.md) for the R2-specific security configuration.

## Sessions — the second redeploy-killer

If your sessions live in-process (Express `express-session` with default `MemoryStore`, Next.js naive session-in-Map), every deploy logs out every user. Same problem if you scale to two instances — half of requests land on the instance that never saw the login.

```ts
// Bad — default Express in-memory session store
import session from 'express-session';
app.use(session({ secret: process.env.SESSION_SECRET! }));  // MemoryStore by default!

// Good — Redis-backed session
import { createClient } from 'redis';
import RedisStore from 'connect-redis';

const redis = createClient({ url: process.env.REDIS_URL });
await redis.connect();

app.use(session({
  store: new RedisStore({ client: redis }),
  secret: process.env.SESSION_SECRET!,
  cookie: { httpOnly: true, secure: true, sameSite: 'lax', maxAge: 7 * 24 * 60 * 60 * 1000 },
}));
```

Stateless alternatives:

- **Signed cookies** (the session payload itself is in the cookie, signed by the server). Works for small sessions; the cookie grows with the data.
- **JWT** with short TTL + refresh tokens. See [`auth-hardening`](../auth-hardening/SKILL.md) for the tradeoffs.

## Background jobs — `setTimeout` is not a queue

```ts
// Bad — process is killed on deploy, job never runs
app.post('/api/sign-up', async (req, res) => {
  await db.users.create(req.body);
  setTimeout(() => sendWelcomeEmail(req.body.email), 60_000);   // ☠️
  res.json({ ok: true });
});

// Good — persistent queue, retries, observability
import { Queue, Worker } from 'bullmq';

const emailQueue = new Queue('emails', { connection: { url: process.env.REDIS_URL }});

app.post('/api/sign-up', async (req, res) => {
  await db.users.create(req.body);
  await emailQueue.add('welcome', { email: req.body.email }, {
    attempts: 5,
    backoff: { type: 'exponential', delay: 1000 },
    removeOnComplete: 1000,
  });
  res.json({ ok: true });
});

// Worker — separate process, can be on the same or different host
new Worker('emails', async (job) => {
  await sendWelcomeEmail(job.data.email);
}, { connection: { url: process.env.REDIS_URL }});
```

What you get:
- Retries with backoff
- Dead-letter queue for poison messages
- Persistence — restarting the worker does not lose jobs
- Observable — BullMQ has an admin UI

For cron-style "every hour" jobs, the right place is **also** the queue (BullMQ has `repeat`, or use a dedicated cron worker), or a managed scheduler (AWS EventBridge, Cloudflare Workers Cron). Not a `setInterval` in the web process.

## Deploys — immutable artifacts, health checks, graceful shutdown

Three patterns that together make deploys boring:

### Immutable artifacts

A deploy is "ship this exact image / artifact to production." Not "pull, install, configure." The same artifact that ran in staging runs in prod. If something breaks in prod, rolling back means pointing at the previous artifact — no re-install, no risk of a different state.

- Docker image with explicit tag (`myapp:1.2.3` or SHA-digest), not `:latest`
- Or built bundle (zip / tarball) checked into a versioned artifact store
- Build once, deploy that exact thing to every environment

### Health checks

Two endpoints, two purposes:

```ts
// Liveness — is the process alive? Cheap, no dependencies.
app.get('/healthz', (req, res) => res.json({ ok: true }));

// Readiness — is the process actually ready to serve traffic?
app.get('/readyz', async (req, res) => {
  try {
    await Promise.all([
      db.$queryRaw`SELECT 1`,
      redis.ping(),
    ]);
    res.json({ ok: true });
  } catch (err) {
    res.status(503).json({ ok: false, err: String(err) });
  }
});
```

The orchestrator (Docker, Kubernetes, your reverse proxy) routes traffic only when `/readyz` returns 200. Without this, new containers get traffic before they have warmed connections to the DB and produce 500s for the first 30 seconds of every deploy.

### Graceful shutdown

When the orchestrator sends `SIGTERM`, stop accepting new requests, finish in-flight ones, close connections, then exit. Most frameworks ship this; some make you wire it.

```ts
const server = app.listen(port);

const shutdown = async (signal: string) => {
  console.log(`${signal} — draining`);
  server.close(async () => {
    await redis.quit();
    await db.$disconnect();
    process.exit(0);
  });
  // Hard cap — if drain takes too long, force exit
  setTimeout(() => process.exit(1), 30_000).unref();
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
```

Combined: zero-downtime rolling deploys become trivial.

## Database operations — migrations and connections

### Migrations

- **Forward-compatible by default**: never break the old code. New code can run against old schema, old code can run against new schema, until both sides have rolled out.
- **Expand-then-contract**: add a new column / table first, deploy code that writes to both, backfill, then remove the old. No "rename column" in a single migration in production.
- **Lock-free for large tables**: in Postgres, prefer `ADD COLUMN ... DEFAULT NULL` (instant) over `ADD COLUMN ... DEFAULT 'x' NOT NULL` (rewrites the table). Use `CREATE INDEX CONCURRENTLY` for indexes on large tables.
- **Run migrations as a separate step**, not at app boot. Two app instances racing to run the same migration at startup is its own incident class.

### Connection pooling

App processes open too many connections to Postgres by default. Postgres struggles past ~100 active connections. Use a pooler:

- **PgBouncer** — battle-tested, transaction-mode for most apps
- **Supabase, Neon, RDS Proxy** — managed pooler in front of managed Postgres
- **Prisma Accelerate** / **Drizzle's pool** — ORM-level pooling

Set per-instance pool size = `(maxConnections / numInstances)` − headroom. For 4 instances and a 100-connection budget, that's ~20 connections per instance with 20 spare.

See [`postgres-hardening`](../postgres-hardening/SKILL.md) for the security side.

## Idempotency — survive retries

Every state-changing operation should produce the same effect whether it runs once or ten times. This is what makes retries, queues, and replays safe.

- **Webhook handlers** dedupe on the provider's event ID. See [`stripe-webhook-security`](../stripe-webhook-security/SKILL.md).
- **Order creation** dedupes on a client-generated idempotency key (`X-Idempotency-Key` header), not on auto-incremented IDs.
- **Email sends** dedupe on `(template, recipient, trigger-id)`.
- **File uploads** dedupe on content hash (compute SHA-256 of the file, use as the object key).

A retry storm should be boring, not catastrophic.

## Observability — three pillars, minimum viable

For a small backend, "observability" is not a buzzword — it is three concrete things:

1. **Centralized logs** — see [`log-strategy`](../log-strategy/SKILL.md). Cloud logging, Loki, hosted. Not "ssh in to read /var/log".
2. **Per-request tracing** — generate a `request_id` at the edge (Cloudflare adds one for free), thread it through every log line and every downstream service call. When something breaks, you can reconstruct the full path.
3. **Error reporting** — Sentry / Rollbar / Highlight / GlitchTip. Each unhandled exception lands with stack trace, breadcrumbs, user context. Without this you only see errors users actively complain about.

Metrics (Prometheus / Grafana / Datadog) are great when traffic grows; not day-one critical.

## The cost-aware tier — when to add complexity

Most vibe-coded projects do not need Kubernetes, microservices, multi-region, or a service mesh. The cost of premature complexity is real: more failure modes, more "why is this not working" hours, more bills.

Reasonable trajectory:

| Stage | Architecture |
|---|---|
| 0–1k users | Single VPS, app + Postgres + Redis colocated, daily off-host backups, Cloudflare in front |
| 1k–10k users | Same, plus object storage for files, separate worker process, managed Postgres or DB on a dedicated VM |
| 10k–100k users | Multiple app instances behind a load balancer, managed Postgres with read replica, queue is its own service, CDN is essential |
| 100k+ users | Dedicated DB nodes, autoscaling app tier, regional split if latency demands, real SRE practices |

Skip stages only if you have a specific reason. "We might need Kubernetes someday" is not a reason for today.

## Twelve-Factor — the canonical reference

Most of this skill is a practical application of [The Twelve-Factor App](https://12factor.net), an excellent guide written in 2011 that has aged remarkably well. The twelve factors:

1. **Codebase** — one codebase tracked in revision control, many deploys
2. **Dependencies** — explicitly declared and isolated (lockfiles)
3. **Config** — stored in the environment, not the code
4. **Backing services** — treated as attached resources (DB, cache, queue are configurable)
5. **Build, release, run** — strictly separate stages
6. **Processes** — execute the app as one or more stateless processes
7. **Port binding** — export services via port binding (no external web server required at the app layer)
8. **Concurrency** — scale out via the process model
9. **Disposability** — fast startup and graceful shutdown
10. **Dev/prod parity** — keep dev, staging, and production as similar as possible
11. **Logs** — treat logs as event streams
12. **Admin processes** — run admin/management tasks as one-off processes

Read it once. Then read it again every six months. Most "production incidents" in small-team backends are violations of one of these twelve.

## Quick architecture review checklist

Before declaring a backend production-ready, walk through:

- [ ] App processes are stateless — restarting an instance loses nothing
- [ ] User uploads go to object storage (S3 / R2 / equivalent), not local disk
- [ ] Sessions are in Redis / DB / signed cookies, not in-process memory
- [ ] Background jobs run via a persistent queue, not `setTimeout` / `setInterval`
- [ ] Cron jobs run via a real scheduler, not the web process
- [ ] Cache is explicit (Redis / KV / CDN), not implicit in-memory hashmaps
- [ ] Database has off-host backups, restore-tested at least once
- [ ] Database migrations are forward-compatible; never "rename + drop" in one step
- [ ] Connection pooling is in place (PgBouncer or equivalent)
- [ ] App has `/healthz` (liveness) and `/readyz` (readiness) endpoints
- [ ] App handles `SIGTERM` gracefully — drains connections, finishes in-flight work
- [ ] Deploys produce immutable artifacts (image tag or SHA digest), no in-place mutation
- [ ] Rollback is a single command pointing at a previous artifact
- [ ] Logs ship to a central destination, with `request_id` threading
- [ ] Unhandled errors land in Sentry / equivalent
- [ ] All state-changing operations are idempotent
- [ ] Configuration is in env vars; no environment-specific values baked into the image
- [ ] `.env` is not in the image, not in the repo

If anything is "no", you have an outage waiting. Fix before scaling, not after.

## What this skill will not do

- Tell you to use Kubernetes / microservices / multi-region for a project that does not need them
- Endorse writing application data to the app server's local disk in production
- Help build a backend whose deploys lose user data because "we'll fix it later"
- Replace experience — architecture is judgment. This skill gives you the patterns; the calls are still yours
