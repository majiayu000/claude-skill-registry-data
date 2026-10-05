---
name: factory-observability
description: Observability conventions across builds. PostHog + Sentry on day one (non-negotiable per the factory thesis — easiest to start early, most expensive to backfill). Request tracing with propagated trace IDs, structured logging, activity-log audit table, event tagging by tool/feature for per-tool usage queryability, PostHog ingest-URL rewrite to avoid ad-blocker breakage. What to log, what NOT to log (PII).
---

# Factory observability

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the PostHog / Sentry / pino / structlog shape we use), and **Failure mode** when there's one to name.

## Day-one stack — observability before features

**Principle.** PostHog + Sentry + trace IDs + structured logs go in on day one, before the first feature ships.

**Why.** Observability is the build's most asymmetric cost-vs-value: cheap on day one (an SDK install and a config block), expensive to backfill (every event needs a redeploy, session-replay data starts empty, six months of usage history is lost). The trap is treating it as "we'll add when we need it" — by the time you need it, the data you'd want doesn't exist.

**Recipe.**

| Layer | Tool | Purpose |
|---|---|---|
| Product analytics | **PostHog** | Per-feature usage, funnels, session replay |
| Error tracking | **Sentry** | Exceptions, performance, source maps |
| Audit log | DB table (`admin_actions` or `audit_log`) | Mutation provenance, regulatory compliance |
| Request tracing | Trace ID middleware + logs | Cross-service debugging |
| Structured logs | `pino` (Node) / `structlog` (Python) | Searchable, machine-parseable |

## PostHog — client setup with ingest rewrite

**Principle.** PostHog ingest goes through your own domain via Next.js rewrites; ad-blockers drop direct PostHog calls.

**Why.** Browser-level ad-blockers (uBlock, Brave's shield) recognize `i.posthog.com` and drop ~30% of events in aggregate. Routing through `/ingest` on your own domain bypasses the blocklist — the events arrive, the analytics are accurate. The cost is one rewrite block; the savings are ~30% of every funnel calculation you'll ever do.

**Recipe.**

```tsx
// src/components/PostHogProvider.tsx
'use client';

import posthog from 'posthog-js';
import { PostHogProvider } from 'posthog-js/react';
import { useEffect } from 'react';

if (typeof window !== 'undefined') {
  posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
    api_host: '/ingest',                  // proxied — see rewrites below
    capture_pageview: false,              // we call manually with route context
    person_profiles: 'identified_only',
  });
}

export function PHProvider({ children }: { children: React.ReactNode }) {
  return <PostHogProvider client={posthog}>{children}</PostHogProvider>;
}
```

```js
// next.config.js — rewrite ingest URL to bypass ad-blockers
async rewrites() {
  return [
    { source: '/ingest/static/:path*', destination: 'https://us-assets.i.posthog.com/static/:path*' },
    { source: '/ingest/:path*',         destination: 'https://us.i.posthog.com/:path*' },
  ];
}
```

## Event tagging — feature + surface, always

**Principle.** Every event carries a `feature` and `surface` tag; per-feature usage queries depend on it.

**Why.** Six months in, the question is "which features earn their maintenance cost?" That question is a `GROUP BY feature` away if the events are tagged, and a complete loss if they're not. Tagging on every event is one extra line; not tagging is a year of usage data that can't be sliced.

**Recipe.**

```ts
posthog.capture('customer_created', {
  feature: 'customers',          // which feature folder
  surface: 'customers_drawer',   // which surface
  org_id: orgId,
  source: 'manual',              // vs 'import' vs 'api'
});
```

Later: `SELECT feature, count(*) FROM events GROUP BY feature ORDER BY 2 DESC` is the answer to "which features earn their maintenance cost?"

## Sentry — exception capture with user scope after auth

**Principle.** Exceptions are scoped to the user that triggered them; user context is attached after auth, not before.

**Why.** An exception without user context is a haystack — "something broke for someone." With user context, the same exception is "this broke for user X, here's their session." Attaching context after auth (rather than at module init) keeps anonymous traffic anonymous in the error stream and identified traffic identified.

**Recipe.**

```ts
// sentry.client.config.ts / sentry.server.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,                  // 10% perf sampling
  replaysSessionSampleRate: 0.0,
  replaysOnErrorSampleRate: 1.0,          // capture session on error
  environment: process.env.VERCEL_ENV ?? 'development',
});
```

```py
# Python — Sentry SDK
import sentry_sdk
sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    traces_sample_rate=0.1,
    environment=os.environ.get('ENV', 'development'),
)
```

## Trace ID — propagate, don't regenerate

**Principle.** Every request carries a trace ID; if the caller sent one, propagate it; if not, generate it. Always echo it in the response.

**Why.** Trace IDs lose half their value if they break across service boundaries. A request that hits Next.js → Cloud Run service A → Cloud Run service B should carry the same ID through all three. Regenerating at each hop forces the support engineer to align three IDs by hand; propagating means one ID lines up across all three logs.

**Recipe.**

```py
# Python / FastAPI
@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response
```

```ts
// Next.js middleware
export function middleware(req: NextRequest) {
  const requestId = req.headers.get('x-request-id') ?? crypto.randomUUID();
  const res = NextResponse.next();
  res.headers.set('x-request-id', requestId);
  return res;
}
```

Log the request ID with every structured log line.

**Failure mode.** Generating a new trace ID at every service hop — cross-service debugging requires manual log alignment, and the support conversation becomes "approximately what time?"

## Structured logging — never `console.log` strings

**Principle.** Every log line is a structured record (JSON or equivalent); never raw string concatenation.

**Why.** A grep over `pino` JSON logs lets you filter by `user_id`, `action`, `request_id`, `duration_ms`. A grep over string-concatenated logs is "did the substring match?" — every new query is a new regex, no aggregation is possible. The cost of structured logging is one logger import; the benefit is every future incident investigation.

**Recipe.**

```ts
// Node — pino
import pino from 'pino';
export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  formatters: { level: (label) => ({ level: label }) },
  base: { service: 'web', env: process.env.VERCEL_ENV },
});

logger.info({ user_id, request_id, action: 'customer.create' }, 'created customer');
```

```py
# Python — structlog
import structlog
log = structlog.get_logger().bind(service='fleetsim')

log.info('simulation_started', request_id=request_id, fleet_id=fleet_id)
```

## Activity log — DB-backed audit trail, fire-and-forget

**Principle.** Audit logging at the mutation boundary is fire-and-forget; same principle as the API layer.

**Why.** See `factory-api.md §audit logging at mutation boundary` and `factory-data-layer.md §activity log table`.

**Recipe.**

```ts
// fire-and-forget — never blocks mutations
export async function logAdminAction(input: {
  actor_id: string;
  action: string;
  subject_type?: string;
  subject_id?: string;
  metadata?: Record<string, unknown>;
}): Promise<void> {
  try {
    await db.insert(adminActions).values(input);
  } catch (err) {
    logger.error({ err, input }, 'audit_log_write_failed');
  }
}
```

Schema in `factory-data-layer.md`. Use for regulatory compliance, support investigations, customer-facing "who changed this?" displays.

## What to log

**Recipe only** — the inclusion list.

- **Actions and IDs**: `{ user_id: 'u_xyz', action: 'updated_ssn', subject_id: 'c_abc' }`
- **Request context**: trace ID, user agent (high-level), feature/surface tag
- **Counts and durations**: `{ duration_ms: 142, rows_affected: 3 }`
- **External system call results**: status code, request ID echoed back (Stripe, Twilio, etc.)

## What NOT to log

**Principle.** Log actions and IDs, never payloads. PII in logs creates compliance scope creep.

**Why.** Same principle as `factory-security.md §logging — log actions and IDs, not payloads`. Once payloads with PII land in the log stream, the log stream inherits the PII's protection requirements.

**Recipe.** Don't log:

- **Raw PII / PHI payloads**: full SSN, government IDs, financial account numbers
- **Auth tokens / API keys**: at any layer, ever
- **Full request bodies**: redact at the logger layer if you need to debug
- **Decrypted ciphertext**: see `factory-security.md`

## Source patterns

Encode/monorepo (PostHog setup, ingest URL rewrite, PHProvider component), cothon (request logging middleware with trace ID propagation, x-request-id response header), kairos (`adminActions` table, fire-and-forget `logAdminAction`), fleet-advisor (activity logging at router-layer with action/object metadata), Obsidian software-factory-idea (PostHog + Sentry day-one commitment, per-tool usage queryability as layer-10 thesis).
