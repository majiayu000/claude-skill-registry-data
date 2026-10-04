---
name: saas
description: SaaS state-of-the-art — multi-tenancy, usage-based billing, PLG, AI feature integration, modern observability, compliance, and security for production Software-as-a-Service products.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 2.0.0
---

# saas

SaaS state-of-the-art — multi-tenancy, usage-based billing, PLG, AI feature integration, modern observability, compliance, and security for production Software-as-a-Service products.

## Instructions

### Multi-Tenancy

Choose the right isolation model for your use case:

| Model | Description | When to use |
|-------|-------------|-------------|
| **Shared schema** | All tenants share tables; rows tagged with `tenant_id` | Early stage, cost-sensitive, straightforward compliance |
| **Schema-per-tenant** | Separate DB schema per tenant | Medium isolation, easy per-tenant migrations |
| **DB-per-tenant** | Separate database per tenant | Enterprise, strict data residency, high compliance (SOC 2, HIPAA) |
| **Hybrid** | Core data shared; sensitive data siloed | Regulated industries with mixed-tier offerings |

**Rules for shared-schema tenancy:**
- Every query **must** filter by `tenant_id` — enforce via a base repository or ORM middleware, not developer discipline
- Use PostgreSQL **Row-Level Security (RLS)** as a second layer of defence:
  ```sql
  ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
  CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.current_tenant')::uuid);
  ```
- Index `tenant_id` on every tenant-scoped table
- Write integration tests that assert cross-tenant data isolation
- Scope all object storage paths: `s3://bucket/{tenantId}/uploads/{fileId}`
- Never expose predictable sequential IDs — use UUIDs (v7 for sortability)

### Subscription & Billing

#### Flat-rate subscriptions
- Delegate billing to a provider (Stripe, Paddle, LemonSqueezy) — never implement payment processing in-house
- Store only `customerId` and `subscriptionId` in your DB; never card data
- Sync state via webhooks — treat your DB as an eventually-consistent read replica of the billing provider's truth:
  ```
  customer.subscription.created  → activate plan
  customer.subscription.updated  → upgrade / downgrade / seat change
  customer.subscription.deleted  → cancel + start grace period
  invoice.payment_failed         → dunning: notify → restrict → cancel
  ```
- Use the webhook event `id` as an idempotency key — store it before processing; skip if already seen
- Store raw webhook payloads for audit and replay

#### Usage-based / metered billing (modern default)
- Track usage events as they happen (API calls, seats, tokens consumed, storage GB):
  ```ts
  await stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
    quantity: tokensUsed,
    timestamp: Math.floor(Date.now() / 1000),
    action: 'increment',
  });
  ```
- Expose a live usage dashboard to customers — surprises on invoice day cause churn
- Implement soft limits (warn at 80%) and hard limits (block at 100%) per billing period
- Consider a free tier + usage-based upsell as a Product-Led Growth (PLG) on-ramp

### Product-Led Growth (PLG)

- **Free tier / freemium** — let users experience value before asking for payment; set limits that make paid plans obviously worthwhile
- **Time-to-value (TTV)** — measure and minimise the time from signup to first meaningful action ("aha moment")
- **In-app upgrade prompts** — surface upgrade CTAs contextually at the moment a plan limit is hit, not in a generic settings page
- **Product-qualified leads (PQL)** — score users by product usage signals (not just demo requests) to route to sales
- **Viral / collaborative features** — invite teammates, share reports, public pages — each action is a distribution channel

### AI Feature Integration

Modern SaaS products are expected to ship AI-native capabilities. Apply these patterns:

**AI assistants and copilots:**
- Use streaming responses (SSE / `ReadableStream`) so users see tokens as they arrive — never make them wait for a full response
- Always make AI output editable — users need to correct, refine, and own the output
- Show confidence signals and cite sources (RAG) to build trust

**Retrieval-Augmented Generation (RAG):**
- Store per-tenant vector embeddings in an isolated namespace (Pinecone, pgvector, Qdrant) — never mix tenant data
- Embed content on write; query on read with cosine similarity
- Chunk documents intelligently (512–1024 tokens with overlap); re-embed when source content changes

**Usage and cost controls:**
- Track LLM token consumption per tenant — bill or rate-limit accordingly
- Cache deterministic prompts (same input → same output) to cut costs
- Use cheaper models for classification/triage; reserve frontier models for generation tasks

**Data privacy:**
- Offer a data-processing addendum (DPA) that explicitly states whether tenant data is used for model training
- Provide an opt-out; enterprise customers will require it

### Feature Flags & Plan Gating

- Gate features at the **service layer** — client-side hiding is UI polish, not security
- Centralise entitlement logic in a single `can(tenant, feature)` helper:
  ```ts
  function can(tenant: Tenant, feature: Feature): boolean {
    return tenant.plan.features.includes(feature);
  }
  ```
- Decouple feature **deployment** from feature **release** using a flag system (LaunchDarkly, Unleash, GrowthBook, or a simple DB-backed table)
- Use flags for: gradual rollouts (% of tenants), beta programs, A/B tests, kill switches

### Onboarding

- **Minimise TTV**: guide users to their first meaningful action in < 5 minutes
- Use a checklist-driven onboarding flow with clear progress indicators
- Pre-populate sample / demo data so the product doesn't feel empty on first use
- Collect the absolute minimum data upfront; defer everything else
- Trigger onboarding emails based on **product events** (not just time): welcome on signup, nudge if they haven't completed step 2 after 24h, celebrate first milestone
- Offer an interactive product tour (not a video) so users learn by doing

### Observability & Operations

**Structured logging** — every log line must include:
```json
{ "level": "info", "msg": "...", "tenantId": "...", "userId": "...", "requestId": "...", "timestamp": "..." }
```

**Distributed tracing with OpenTelemetry:**
- Instrument at the framework level (Next.js `instrumentation.ts`, Express middleware)
- Propagate trace context across service boundaries (`traceparent` header)
- Export to your backend of choice (Jaeger, Honeycomb, Datadog, Grafana Tempo)

**Per-tenant metrics to track:**
- Active users (DAU/MAU), API call volume, error rate, p50/p95/p99 latency, feature adoption, storage consumed

**Alerting:**
- Alert on tenant-level anomalies — sudden error spike, usage drop, billing failures
- Define SLOs per tier: free (best-effort), pro (99.5%), enterprise (99.9%)

**Admin tooling (internal):**
- Impersonate a tenant for support (audit every impersonation)
- View audit log, manage subscriptions, override feature flags, trigger re-onboarding
- Build a health dashboard: per-tenant status, recent errors, usage trends

### Data, Analytics & Compliance

**Event tracking:**
- Emit structured product events (`user.signed_up`, `feature.used`, `subscription.upgraded`) to a data warehouse (Snowflake, BigQuery) or CDP (Segment, PostHog, RudderStack)
- Use these events for churn prediction, cohort analysis, and PLG scoring

**GDPR / privacy:**
- Provide a data export endpoint and an account deletion endpoint — required by GDPR and expected by enterprise buyers
- Document your data retention policy; implement automated purges
- Use consent management for marketing cookies and analytics

**SOC 2 / compliance hygiene (enterprise readiness):**
- Maintain an audit log of all state-changing user actions (who, what, when, from which IP)
- Implement role-based access control (RBAC) with least-privilege defaults
- Enforce MFA for all admin accounts; offer SSO (SAML/OIDC) for enterprise tenants
- Conduct regular dependency vulnerability scans and penetration tests
- Maintain a vulnerability disclosure policy

### Data Isolation & Security

- Validate `tenant_id` on every API call against the **authenticated session** — never trust the request body
- Rate-limit per tenant to prevent noisy-neighbour effects
- Hash API keys in the DB (bcrypt or Argon2); never store plaintext
- Require HTTPS; set `Strict-Transport-Security` with a long `max-age`
- Use `HttpOnly; Secure; SameSite=Lax` for session cookies

## Examples

```ts
// Tenant-scoped repository with RLS context
class TenantRepository<T> {
  constructor(
    private readonly tenantId: string,
    private readonly db: PrismaClient,
  ) {}

  protected async withTenantContext<R>(fn: () => Promise<R>): Promise<R> {
    return this.db.$transaction(async (tx) => {
      await tx.$executeRaw`SELECT set_config('app.current_tenant', ${this.tenantId}, true)`;
      return fn();
    });
  }

  async findById(id: string): Promise<T | null> {
    return this.withTenantContext(() =>
      (this.db as any).findFirst({ where: { id, tenantId: this.tenantId } })
    );
  }
}

// AI streaming endpoint with per-tenant usage metering
export async function POST(req: Request) {
  const session = await getSession(req);
  const { prompt } = await req.json();

  const stream = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }],
    stream: true,
  });

  let tokensUsed = 0;
  const readable = new ReadableStream({
    async start(controller) {
      for await (const chunk of stream) {
        const text = chunk.choices[0]?.delta?.content ?? '';
        controller.enqueue(new TextEncoder().encode(text));
        tokensUsed += chunk.usage?.completion_tokens ?? 0;
      }
      controller.close();
      // meter usage after streaming completes
      await meteringService.record(session.tenantId, 'ai_tokens', tokensUsed);
    },
  });

  return new Response(readable, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}

// Stripe webhook with idempotency
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const event = stripe.webhooks.constructEvent(
    req.body, req.headers['stripe-signature']!, process.env.STRIPE_WEBHOOK_SECRET!
  );

  const seen = await db.webhookEvent.findUnique({ where: { stripeEventId: event.id } });
  if (seen) return res.sendStatus(200);
  await db.webhookEvent.create({ data: { stripeEventId: event.id, payload: event } });

  switch (event.type) {
    case 'customer.subscription.updated':
      await subscriptionService.sync(event.data.object);
      break;
    case 'customer.subscription.deleted':
      await subscriptionService.cancel(event.data.object.metadata.tenantId);
      break;
  }

  res.sendStatus(200);
});
```

## References

- [Stripe Billing](https://stripe.com/docs/billing)
- [Stripe Usage-Based Billing](https://stripe.com/docs/billing/subscriptions/usage-based)
- [PostgreSQL Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [OpenTelemetry](https://opentelemetry.io/)
- [PostHog — Product Analytics](https://posthog.com/)
- [GrowthBook — Feature Flags](https://www.growthbook.io/)
- [The SaaS Playbook – Rob Walling](https://saasplaybook.com/)
- [Twelve-Factor App](https://12factor.net/)
- [pgvector — Vector similarity search for Postgres](https://github.com/pgvector/pgvector)
