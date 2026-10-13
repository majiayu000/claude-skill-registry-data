---
name: instrumenting-production-stack
version: "3.0.1"
description: >
  Sets up observability for the Vercel + Supabase + n8n + Anthropic stack.
  Live operational path runs through PostHog (MCP connected). Datadog is NOT
  connected — all Datadog steps are static setup references only, clearly
  labeled, and not executable via MCP. Activates on PostHog instrumentation,
  production monitoring, health dashboard, alert setup, stack observability,
  what to monitor, are things working in production. Not for cost tracking or
  budget alerts (use governing-stack-costs) and not for agent behavioral
  telemetry (use instrumenting-agent-telemetry).
allowed-tools: Read Write Bash
---

## When to Use / When NOT

**Use when** — "set up observability for my production stack." "I don't know what's happening in production." "Wire PostHog to track Vercel errors and Anthropic costs."

**Do NOT use when** — "why is my Anthropic bill so high" → governing-stack-costs. "Set up telemetry for my AI agent's behavior" → instrumenting-agent-telemetry.

---

# Production Stack Observability

Covers: Vercel (frontend), Cloudflare Workers (edge), Supabase (database + auth), n8n (workflows), Anthropic API (AI).

**Live operational path: PostHog MCP ✅**
**Datadog: ❌ NOT connected — sections marked [STATIC REFERENCE] are manual setup guides only.**

---

## DEPENDENCY_DECLARATION

| Tool | Status | Operational Path | Notes |
|------|--------|-----------------|-------|
| PostHog | MCP ✅ CONNECTED | Live event queries, insight creation, alert configuration | Primary observability path |
| Supabase | MCP ✅ CONNECTED | Schema queries, log table creation and querying | Ask before write ops |
| n8n | MCP ✅ CONNECTED | Execution status, workflow health check | Read-only preferred |
| Vercel | MCP ✅ CONNECTED | Deployment status | Limited log access |
| Datadog | ❌ NOT_CONNECTED | Static reference only — no MCP execution possible | All Datadog steps require manual setup |

**Rule:** Any step in a [STATIC REFERENCE] section cannot be executed via MCP. Do not attempt Datadog API calls, dashboard creation, or monitor creation in a Claude session — Datadog is not connected. Any result would be fabricated.

---

## FAIL_IF

- **FAIL_IF** you attempt to create Datadog monitors, dashboards, or log pipelines via MCP — Datadog is not connected; results would be fabricated.
- **FAIL_IF** you claim the Datadog log drain, Postgres integration, or Datadog dashboards are "active and flowing" — they require manual setup.
- **FAIL_IF** you embed a Datadog API key, PostHog server key, or Supabase service_role key in any code block — these belong in environment variables only.
- **FAIL_IF** you log PII (user emails, message content, auth tokens) into PostHog events — use anonymized identifiers only.
- **FAIL_IF** you set alert thresholds with no stated baseline — collect at minimum 1 week of production data before finalizing thresholds.
- **FAIL_IF** you instrument only the happy path — error branches, retries, and timeouts must be instrumented explicitly.

**"Just do it" override:** proceed with the PostHog-only live path and label Datadog items as manual follow-ups if the user requests immediate action.

---

## Evals

**Should trigger:**
1. "Set up observability for my production stack"
2. "Wire PostHog to track Vercel web vitals and Anthropic API costs"
3. "I don't know what's happening in production — what should I monitor?"
4. "Build a production health dashboard in PostHog"

**Should NOT trigger:**
1. "Why is my Anthropic bill so high?" → use governing-stack-costs
2. "Set up telemetry for my AI agent's behavior" → use instrumenting-agent-telemetry

---

## Observability Architecture

```
Service          → What it produces      → LIVE PATH (MCP ✅)       → [STATIC REF] Datadog
─────────────────────────────────────────────────────────────────────────────────────────────
Vercel           → Function logs,         → PostHog (web vitals,     → Log drain to Datadog
                   web vitals               error events)
Cloudflare       → Worker logs,           → PostHog (custom events   → Datadog Cloudflare
                   edge metrics             via fetch)                  integration
Supabase         → Query logs,            → Supabase built-in dash   → Datadog Postgres
                   auth events,             + PostHog custom events     integration
                   API latency
n8n              → Execution logs,        → n8n MCP + Error          → Datadog log
                   credential errors        Trigger → Slack             shipping
Anthropic API    → Token usage,           → PostHog wrapper          → [STATIC] statsd
                   cost, latency           (server-side)                custom metric
```

---

## Vercel Setup

### Web vitals → PostHog (LIVE ✅)

Add to your Next.js `_app.tsx` or `layout.tsx`:

```typescript
import posthog from 'posthog-js'
import { useReportWebVitals } from 'next/web-vitals'

export function reportWebVitals(metric) {
  posthog.capture('web_vital', {
    name: metric.name,     // LCP, FID, CLS, TTFB, FCP
    value: metric.value,
    rating: metric.rating, // good / needs-improvement / poor
    page: window.location.pathname
    // Do NOT include: auth tokens, user IDs, email addresses
  })
}
```

**PostHog insight to build:** filter `event = 'web_vital'`, breakdown by `name`, trend `value` over time.

### Error tracking → PostHog (LIVE ✅)

```typescript
// Add to error boundary or _app.tsx — client-side only (posthog-js)
window.addEventListener('unhandledrejection', (event) => {
  posthog.capture('js_error', {
    error_message: event.reason?.message ?? 'unknown',
    error_type:    'unhandled_rejection',
    page:          window.location.pathname
    // Do NOT include: event.reason stack trace if it may contain secrets or PII
  })
})
```

### Alerts to configure in PostHog (LIVE ✅)

PostHog Insights → Alerts:
- `js_error` count exceeds threshold per hour → alert
- `web_vital` where `name = LCP` and `value` rolling average exceeds 2500ms → alert

### Vercel function alert thresholds (configure in Vercel project settings)

- Function error rate >1% over 5 minutes → email notification
- Build failure → Vercel built-in notification (enable in project settings)

---

### [STATIC REFERENCE] Vercel Log Drain → Datadog

> ⚠️ Datadog is NOT connected via MCP. Execute these steps manually in Vercel and Datadog dashboards.

1. Vercel Dashboard → project → Settings → Log Drains
2. Add log drain: select Datadog, paste Datadog API key (store key in Bitwarden, never in source)
3. Select environments: Production (minimum), optionally Preview
4. Verify: Datadog → Logs → search `source:vercel` and confirm events appear

---

## Supabase Setup

### Supabase built-in dashboard (no MCP needed for viewing)

- Supabase Dashboard → Database → Query Performance → identifies slow queries
- Supabase Dashboard → Auth → monitor authentication events
- Supabase Dashboard → Logs Explorer → filter by service, level, or function name

### Persistent log table for Edge Functions (LIVE ✅ — create via Supabase MCP)

Edge Function logs are retained 7 days on the free plan. For longer retention:

```sql
CREATE TABLE function_logs (
  id           uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  function_name text NOT NULL,
  status_code  int,
  duration_ms  int,
  error        text,
  created_at   timestamptz DEFAULT now()
);

-- Restrict to service role only — blocks anon and authenticated reads
ALTER TABLE function_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "deny_all_non_service" ON function_logs
  FOR ALL USING (false);
-- Service role bypasses RLS automatically
```

### Auth events → PostHog (LIVE ✅)

```typescript
// server-side only — posthog-node, not posthog-js
import { PostHog } from 'posthog-node'
// Key loaded from environment variable — never hardcoded
const ph = new PostHog(process.env.POSTHOG_SERVER_KEY!)

supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    ph.capture({
      distinctId: session?.user?.id ?? 'anonymous', // UUID only — not email
      event: 'auth_signed_in',
      properties: {
        method: session?.user?.app_metadata?.provider ?? 'email'
        // Do NOT include: session.access_token, user.email, user.phone
      }
    })
  }
  if (event === 'SIGNED_OUT') {
    ph.capture({ distinctId: 'anonymous', event: 'auth_signed_out', properties: {} })
  }
})
```

### Supabase metrics to monitor

| Metric | Alert threshold | Where to see it |
|--------|----------------|----------------|
| Active connections | >80% of connection limit | Supabase Dashboard |
| Query P95 latency | >500ms on indexed queries | Query Performance tab |
| DB size growth | >20% week-over-week | Supabase Dashboard |
| Failed auth attempts | >50 in 10 minutes | Logs Explorer → Auth |
| RLS policy errors | Any spike | Logs Explorer → `level = error` |

---

### [STATIC REFERENCE] Supabase → Datadog Postgres Integration

> ⚠️ Datadog is NOT connected via MCP. Execute these steps manually in Datadog.

1. Datadog → Integrations → Postgres → Configure
2. Enter Supabase DB connection string — use a **read-only monitoring role**, never the `service_role` key
3. Enable: query metrics, connection pool metrics, replication lag
4. Create a dedicated monitoring role if one does not exist:
   ```sql
   CREATE ROLE datadog_monitor WITH LOGIN PASSWORD '[set in Bitwarden]';
   GRANT SELECT ON pg_stat_activity TO datadog_monitor;
   GRANT SELECT ON pg_stat_database TO datadog_monitor;
   ```

---

## Anthropic API Cost Monitoring → PostHog (LIVE ✅)

Anthropic provides no webhook-based cost alerts. Instrument a server-side wrapper:

```typescript
// server-side only — never import posthog-node in client bundles
import { PostHog } from 'posthog-node'
// All keys loaded from environment variables
const ph = new PostHog(process.env.POSTHOG_SERVER_KEY!)

async function callClaude(
  params: MessageParams,
  context: string,
  sessionId: string  // anonymized session UUID — not email, not user name
): Promise<Anthropic.Message> {
  const start = Date.now()
  const response = await anthropic.messages.create(params)

  const inputTokens  = response.usage.input_tokens
  const outputTokens = response.usage.output_tokens
  const model        = params.model

  // Pricing reference — update when Anthropic publishes rate changes
  const costs: Record<string, { input: number; output: number }> = {
    'claude-sonnet-4-20250514':  { input: 3.00,  output: 15.00 },
    'claude-haiku-4-5-20251001': { input: 0.80,  output:  4.00 },
  }
  const rate    = costs[model] ?? costs['claude-sonnet-4-20250514']
  const costUsd = (inputTokens / 1e6 * rate.input) + (outputTokens / 1e6 * rate.output)

  ph.capture({
    distinctId: sessionId,
    event: 'anthropic_api_call',
    properties: {
      context,
      model,
      input_tokens:  inputTokens,
      output_tokens: outputTokens,
      cost_usd:      costUsd,
      latency_ms:    Date.now() - start,
      // Do NOT include: prompt content, response content, user data
    }
  })

  return response
}
```

**PostHog insights to build:**
- Daily cost trend: `anthropic_api_call` → sum `cost_usd` by day, breakdown by `context`
- Token volume trend: sum `input_tokens + output_tokens` over time
- Latency: avg `latency_ms` by model

**PostHog alerts:**
- Daily `sum(cost_usd)` exceeds budget threshold → alert
- Any single `input_tokens` value exceeds 50,000 (runaway context indicator)

---

### [STATIC REFERENCE] Anthropic → Datadog Custom Metrics

> ⚠️ Datadog is NOT connected via MCP. This is a reference pattern for when you manually connect Datadog.

Replace the PostHog `ph.capture()` block above with the following when Datadog agent is running:

```typescript
// Requires hot-shots (StatsD client) — install: npm install hot-shots
// DD_AGENT_HOST set via environment variable — never hardcoded
import StatsD from 'hot-shots'
const statsd = new StatsD({ host: process.env.DD_AGENT_HOST })

statsd.gauge('anthropic.cost_usd',    costUsd,           [`context:${context}`, `model:${model}`])
statsd.gauge('anthropic.latency_ms',  Date.now() - start, [`context:${context}`])
statsd.increment('anthropic.requests.total',              [`context:${context}`, `model:${model}`])
```

`DD_AGENT_HOST` and any Datadog API key belong in environment variables only. Do not include them in source code.

---

## n8n Execution Monitoring (LIVE ✅)

**Real-time failure alerts:** use the Error Trigger node in n8n → sends to Slack webhook on any workflow failure. See `operating-n8n-production` for the Error Trigger pattern.

**Health check via n8n MCP or REST API:**

```
GET /api/v1/executions?status=error&limit=50
```

Write error counts to a Supabase `n8n_metrics` table. Query via PostHog connected source or Supabase SQL.

**n8n MCP query to run in session:**
> "Pull the last 20 failed executions from n8n and list the workflow names and error messages"

---

### [STATIC REFERENCE] n8n → Datadog Log Shipping

> ⚠️ Datadog is NOT connected via MCP. Execute these steps manually.

- **n8n paid plans:** Settings → Log streaming → enable Datadog endpoint, set `DD_API_KEY` (from Bitwarden)
- **n8n Cloud free/starter:** schedule a workflow to call `GET /api/v1/executions` and ship results to Datadog HTTP log intake via HTTP Request node

---

## Dashboard: Unified Production Health

### PostHog dashboard (LIVE ✅ — build this now)

Create one PostHog dashboard with four sections:

**Section 1: User-Facing Health**
- `web_vital` avg value by metric name (trend)
- `js_error` count per day
- `auth_signed_in` and `auth_signed_out` per day

**Section 2: AI Costs**
- `anthropic_api_call` sum `cost_usd` by day
- Cost breakdown by `context`
- `input_tokens` trend over time

**Section 3: Automation Health**
- n8n error count (from `n8n_metrics` Supabase table, if wired)
- Agent session outcomes (if `agent_session_completed` events are flowing)

**Section 4: Auth & Funnel**
- User funnel: `pageview` → `auth_signed_in` → key action event
- Failed auth rate (if instrumented)

---

### [STATIC REFERENCE] Datadog Unified Dashboard

> ⚠️ Datadog is NOT connected. This is a reference for when you manually configure Datadog.

Build one Datadog dashboard with four sections: (1) Vercel error rate and P95 latency, (2) Supabase active connections and query latency, (3) Anthropic daily cost and token volume, (4) n8n execution error count. Set as Datadog account default landing page.

---

## Self-Verification Checklist

- [ ] `reportWebVitals` function added to Next.js app and `web_vital` events visible in PostHog Live Events — **FAIL** if no events appear after a page load
- [ ] `js_error` PostHog events captured — **FAIL** if unhandled rejections produce no telemetry
- [ ] `anthropic_api_call` PostHog events visible after at least one API call — **FAIL** if events are missing
- [ ] Supabase `function_logs` table created (if using Edge Functions) — **FAIL** if Edge Functions have no retention beyond 7 days
- [ ] PostHog dashboard with 4 sections created and populated — **FAIL** if dashboard is empty or not saved
- [ ] n8n Error Trigger configured and tested — **FAIL** if a deliberate workflow failure produces no Slack alert
- [ ] PostHog cost alert configured — **FAIL** if no daily `cost_usd` threshold exists
- [ ] All keys and secrets loaded from environment variables only — **FAIL** if any secret appears in source code
- [ ] [STATIC — when ready] Datadog log drain setup steps documented in Notion for future reference

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

**CLAIMS**
- [GENERATED] A per-call cost tracking wrapper on the Anthropic API client provides more granular per-feature attribution than Anthropic's billing dashboard, which aggregates at the API key level only.
- [GENERATED] PostHog combined with Supabase's built-in dashboard provides adequate production observability for early-stage FlashFusion deployments without requiring Datadog.

**COUNTEREXAMPLE**
- PostHog's alerting for infrastructure-layer metrics (Postgres connection count, Worker latency) is less capable than Datadog. If you need sub-minute P95 latency alerts on every Supabase query, Datadog + Postgres integration is the better choice and is worth the cost at meaningful scale.

**CONTRADICTIONS**
- Complete observability of every request conflicts with user privacy expectations. Resolution: use 10–25% sampling for detailed request tracing, explicit PII deny-lists on all event payloads, and never log raw request bodies containing auth headers.
- ! CONTRADICTION: the previous version of this skill (v2.0.0) listed Datadog as the primary observability path and included `statsd` calls as live operational steps. Datadog is NOT connected — those steps cannot execute via MCP. PostHog is the live path. All Datadog content is now clearly labeled [STATIC REFERENCE].

---

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- **Cloudflare Workers observability** is incomplete. Workers have no PostHog client SDK; you must use `fetch` to emit events to the PostHog `/capture` endpoint from within a Worker. This pattern is not covered here — extend when needed.
- **Datadog connection.** When Datadog connects via MCP, the [STATIC REFERENCE] sections should be promoted to live operational steps and the DEPENDENCY_DECLARATION updated. File a Linear issue to track this.
- **`POSTHOG_SERVER_KEY` rotation.** Must be rotated per `managing-credential-lifecycle` schedule. No auto-rotation is in place.
- **n8n Cloud REST API rate limits** may apply to the execution export polling pattern. Verify plan limits before scheduling high-frequency polls.
- **Supabase free plan log retention is 7 days.** If the `function_logs` table pattern is not implemented and the plan is not upgraded, log data beyond 7 days is unrecoverable.
- **SELF-REVIEW:** Verified no live Datadog MCP calls present. All statsd references moved to [STATIC REFERENCE] sections. All keys use environment variables. PostHog wrapper is server-side only. DEPENDENCY_DECLARATION and FAIL_IF blocks added. Version bumped to 3.0.0 (major — Datadog demoted from live path, PostHog promoted; gate logic changed).
