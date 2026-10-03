---
name: paddle-integration
last_updated: 2026-05-17
description: "Beamix billing patterns using Paddle: webhook signature verification, checkout session creation, customer portal URL generation, price ID conventions, and subscription lifecycle. Stripe is not used — Paddle is the only payment provider."
tags: [billing, beamix-specific, backend, payments]
source: beamix-authored 2026-05-16
risk: low
---

# Paddle Integration

## Quick reference

> Webhook signature verify FIRST. All state transitions in `subscriptions` table. Never trust client-side checkout state. Paddle = source of truth.

## When to use

- Implementing or debugging billing API routes in `apps/web/src/app/api/billing/`
- Writing Paddle webhook handlers
- Generating checkout links or customer portal URLs
- CBO reviewing unit economics from live subscription data

## When NOT to use

- Stripe is not in the Beamix stack. Any Stripe reference is legacy and should be removed.
- For auth flows (Supabase Auth handles user auth)

## Pricing (locked — as of April 15, 2026)

| Tier | plan_tier enum | Monthly | Annual |
|------|---------------|---------|--------|
| Discover | `discover` | $79/mo | $63/mo |
| Build | `build` | $189/mo | $151/mo |
| Scale | `scale` | $499/mo | $399/mo |

Trial: 14-day money-back guarantee. Free one-time scan remains available without signup.

## Environment variables

```bash
PADDLE_API_KEY=...                    # Paddle API key (server-side only, never expose)
PADDLE_WEBHOOK_SECRET=...             # For HMAC signature verification
PADDLE_DISCOVER_PRICE_ID_MONTHLY=...  # Paddle price ID
PADDLE_DISCOVER_PRICE_ID_ANNUAL=...
PADDLE_BUILD_PRICE_ID_MONTHLY=...
PADDLE_BUILD_PRICE_ID_ANNUAL=...
PADDLE_SCALE_PRICE_ID_MONTHLY=...
PADDLE_SCALE_PRICE_ID_ANNUAL=...
```

## Webhook signature verification (mandatory HMAC)

Every webhook endpoint MUST verify the Paddle signature before processing. Never process an unverified webhook.

```typescript
// apps/web/src/app/api/billing/webhook/route.ts
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

export async function POST(req: NextRequest) {
  const rawBody = await req.text();
  const signature = req.headers.get('paddle-signature');

  if (!signature) {
    return NextResponse.json({ error: 'Missing signature' }, { status: 401 });
  }

  // Paddle uses ts= and h1= format: "ts=1234567890;h1=<hmac>"
  const [tsPart, h1Part] = signature.split(';');
  const ts = tsPart.split('=')[1];
  const h1 = h1Part.split('=')[1];

  const signedPayload = `${ts}:${rawBody}`;
  const expectedHash = crypto
    .createHmac('sha256', process.env.PADDLE_WEBHOOK_SECRET!)
    .update(signedPayload)
    .digest('hex');

  if (!crypto.timingSafeEqual(Buffer.from(h1), Buffer.from(expectedHash))) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const event = JSON.parse(rawBody);
  await handlePaddleEvent(event);

  return NextResponse.json({ received: true });
}
```

## Subscription lifecycle events

| Paddle event | Action |
|-------------|--------|
| `subscription.created` | Create/update `subscriptions` row, set `plan_tier`, start trial clock |
| `subscription.updated` | Update `plan_tier`, `subscription_status`, billing dates |
| `subscription.cancelled` | Set `subscription_status = 'cancelled'` (UK spelling — matches enum) |
| `subscription.past_due` | Set `subscription_status = 'past_due'`, send payment-retry email via Resend |
| `transaction.completed` | Update `subscriptions.current_period_end`, log in `credit_transactions` |

DB enum values: `subscription_status` uses UK spelling `'cancelled'` (not `'canceled'`).

## Checkout session creation

```typescript
// apps/web/src/lib/paddle/checkout.ts
import { Paddle } from '@paddle/paddle-node-sdk';

const paddle = new Paddle(process.env.PADDLE_API_KEY!);

export async function createCheckoutUrl(params: {
  priceId: string;
  userId: string;
  userEmail: string;
  successUrl: string;
}): Promise<string> {
  const transaction = await paddle.transactions.create({
    items: [{ priceId: params.priceId, quantity: 1 }],
    customData: { user_id: params.userId },
    customer: { email: params.userEmail },
    checkout: {
      url: params.successUrl,
    },
  });

  return transaction.checkoutUrl!;
}
```

## Customer portal URL generation

Paddle provides a hosted portal for customers to manage their subscription (cancel, update payment).

```typescript
// apps/web/src/lib/paddle/portal.ts
export async function getCustomerPortalUrl(paddleCustomerId: string): Promise<string> {
  const session = await paddle.customerPortalSessions.create({
    customerId: paddleCustomerId,
  });

  return session.urls.general.overview;
}
```

## Supabase subscriptions table (relevant columns)

```sql
-- Key columns in subscriptions table
user_id          uuid references auth.users
paddle_customer_id  text
paddle_subscription_id  text
plan_tier        plan_tier  -- enum: 'discover' | 'build' | 'scale'
subscription_status  subscription_status  -- 'active' | 'trialing' | 'past_due' | 'cancelled'
current_period_start  timestamptz
current_period_end    timestamptz
trial_ends_at    timestamptz
```

## See also

- `supabase-rls-beamix` — [[supabase-rls-beamix]]
- `secrets-management` — [[secrets-management]]
- `error-handling-patterns` — [[error-handling-patterns]]
- `api-design-principles` — [[api-design-principles]]

## Anti-patterns

- Processing webhooks without signature verification (critical security hole)
- Using `'canceled'` (American spelling) for `subscription_status` — DB enum is `'cancelled'`
- Using Stripe (not in stack — any Stripe code is legacy, remove it)
- Hardcoding price IDs in application code (use environment variables)
- Exposing `PADDLE_API_KEY` to the client (server-only — never in `NEXT_PUBLIC_*`)
- Creating checkout sessions server-side with no `customData.user_id` (billing events can't be attributed)
- Running webhook handlers without idempotency check (Paddle may deliver duplicate events)
