---
name: stripe
description: >
  Knowledge base loaded by the stripe-integrator and revenue-optimizer agents, also consumable directly.
  TRIGGER WHEN: working with the Stripe API (Payment Intents, Customers, Subscriptions, Checkout Sessions, Connect, webhooks, tax, usage-based billing), Firebase integration, pricing strategy, or revenue modeling.
---

# Stripe Knowledge Base

Unified reference for Stripe integrations. Content is split across `references/` (topic-specific patterns) and `scripts/` (ready-to-run helpers).

## When to load which reference

- **Any Stripe API work** -> start with `references/api-cheatsheet.md` and `references/stripe.md`
- **TypeScript / Next.js integration (Route Handlers, Server Actions)** -> `references/typescript-nextjs.md`
- **Embedded Checkout (React mount instead of redirect)** -> `references/embedded-checkout.md`
- **Webhooks in production (signature, idempotency, event catalog)** -> `references/webhooks-production.md`
- **Usage-based billing / metered pricing** -> `references/billing-meters.md` (legacy `usage_type=metered` was removed in 2025-03-31.basil)
- **Feature gating from Stripe products** -> `references/entitlements.md`
- **LLM agents calling Stripe (OpenAI Agents SDK / Vercel AI / LangChain / CrewAI / MCP)** -> `references/stripe-agent-toolkit.md`
- **Simulating subscription lifecycle in tests** -> `references/test-clocks.md`
- **PCI DSS 4.0 / 4.0.1 compliance (SAQ-A, SAQ-A-EP)** -> `references/pci-dss-4-checklist.md`
- **Subscription lifecycle** -> `references/subscription-patterns.md`, `references/usage-revenue-modeling.md`
- **Checkout conversion optimization** -> `references/checkout-optimization.md`
- **Pricing strategy and tier design** -> `references/pricing-patterns.md`
- **Firebase + Stripe integration** -> `references/firebase-integration.md`
- **Stripe-idiomatic patterns (reusable code)** -> `references/stripe-patterns.md`
- **Cost analysis / unit economics** -> `references/cost-analysis.md`

**Reference style note:** the newer references (`billing-meters`, `entitlements`, `webhooks-production`, `typescript-nextjs`, `embedded-checkout`, `stripe-agent-toolkit`, `test-clocks`, `pci-dss-4-checklist`) intentionally link to official Stripe docs for canonical code samples instead of mirroring them locally. Local content is limited to non-obvious gotchas and decision criteria.

## Scripts

Ready-to-run Python helpers (adapt to your project; require `STRIPE_SECRET_KEY` env var):

- `scripts/setup_products.py` -- bootstrap Products and Prices for a new project
- `scripts/stripe_utils.py` -- shared utility functions used by the other scripts
- `scripts/sync_subscriptions.py` -- reconcile local DB vs Stripe subscription state
- `scripts/webhook_handler.py` -- signature-verified webhook receiver template with idempotency
- `scripts/webhook_audit.py` -- report gaps between configured webhook endpoints and the must-have event catalog
- `scripts/simulate_subscription.py` -- walk a test-clock subscription through trial end, renewal, failed payment, and recovery

All scripts live at `${CLAUDE_PLUGIN_ROOT}/skills/stripe/scripts/<name>.py`. Agents should reference them by that path.

## API version notes

Stripe's current version (May 2026) is `2026-05-27.dahlia`. Versions follow the pattern `YYYY-MM-DD.<release>` where the release name (`acacia`, `basil`, `dahlia`, ...) signals major-release boundaries. Monthly point releases are backwards-compatible within a release name.

Pin an explicit version in all server-side code:

```python
import stripe
stripe.api_version = "2026-05-27.dahlia"
```

```typescript
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2026-05-27.dahlia',
});
```

The modern Node and Python SDKs bake a default API version into each SDK release, so the SDK itself pins requests unless you override. Prefer explicit pinning on the constructor anyway -- it's the one line that documents which version your integration was written against.

**Breaking changes to know about:**

- `2025-03-31.basil` removed the legacy usage records API (`SubscriptionItem.create_usage_record` and bare `usage_type=metered` prices). All metered prices must now be backed by a Meter. See `billing-meters.md`.
- `subscription.current_period_end` moved to `subscription.items.data[0].current_period_end`. If your code reads the top-level field, you'll break on any modern version.

Dashboard -> Workbench shows your account's default version. Account defaults lag major releases; never rely on the default -- pin explicitly.

## Webhook reliability checklist

- Verify signature with `stripe.Webhook.construct_event` on every event
- Use the raw body, not re-serialized JSON
- Idempotency: deduplicate by `event.id` (Stripe retries within a 3-day window)
- Always respond `2xx` within 10 seconds; defer heavy work to a queue
- Replay past events via `stripe events resend` during development
- Test signature failures -- attackers spoof webhooks

See `references/webhooks-production.md` for the full treatment (event catalog by use-case, multi-environment strategy, audit checklist) and `scripts/webhook_handler.py` for a working implementation.

## Common pitfalls

- Using `subscription.current_period_end` at top level -- it moved to `subscription.items.data[0].current_period_end` in newer API versions; verify against your pinned version
- Caching `customer.default_source` -- deprecated in favor of `invoice_settings.default_payment_method`
- Treating `price.id` as the product identifier -- `price.id` changes on any price update; use `product.id` for stable references
- Forgetting `automatic_payment_methods: { enabled: true }` on Payment Intents -- customers get a default payment-method list that often excludes wallets and BNPL
- Still calling `SubscriptionItem.create_usage_record` -- removed in API `2025-03-31.basil`. Migrate to `stripe.billing.MeterEvent.create` (see `references/billing-meters.md`).
- Rolling your own `plan.features` map when your billing lives in Stripe -- use Stripe Entitlements and cache via the `entitlements.active_entitlement_summary.updated` webhook (see `references/entitlements.md`).

## Integration

- Pricing, tier design, revenue projections -> `revenue-optimizer` agent (same plugin)
- API implementation, webhooks, Connect, subscriptions -> `stripe-integrator` agent (same plugin)
- Webhook audit (Stripe account + codebase) -> `stripe-webhooks-auditor` agent + `/stripe:audit-webhooks` command
- GDPR / PCI posture around payment data -> `business:privacy-doc-generator`
- Cross-platform token/auth handling in a payment flow -> `platform-engineering:platform-reviewer`
