---
name: stripe
description: "Integrate Stripe Checkout, PaymentIntents, subscriptions, and signed webhooks with idempotency and test-mode checks."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["stripe", "payments", "webhooks", "subscriptions", "checkout", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Stripe Payments Integration AI Skill Guide

## Overview & Engine Architecture

Stripe provides payment APIs, Checkout UI, Customers, and Billing subscriptions. Clients never trust browser-reported amounts; the server creates PaymentIntents/Checkout Sessions and verifies **webhook signatures**. Agents design idempotent webhook handlers, store Stripe customer/subscription IDs, and keep secret keys server-side only.

```
Browser / app
   -> Your API (secret key)
       -> Stripe API (Checkout / PaymentIntents / Billing)
Stripe  ->  webhooks  ->  Your API (verify signature, update DB)
```

## When to use this skill

- Adding one-time Checkout or PaymentIntent flows
- Building subscription start/cancel/upgrade paths
- Implementing webhook receivers safely
- Debugging test-mode events in the Stripe Dashboard / CLI

## Operational directives

1. Use **test mode** keys until go-live; never mix live keys in local `.env` committed to git.
2. Verify `Stripe-Signature` on every webhook; reject on failure.
3. Process webhook events idempotently (store `event.id`).
4. Pass `Idempotency-Key` on creating PaymentIntents and other critical POSTs.
5. Authorize using your own user session; Stripe customer ID is not proof of login alone.

## Checkout Session sketch (server)

```js
const session = await stripe.checkout.sessions.create({
  mode: "payment",
  line_items: [{ price: "price_123", quantity: 1 }],
  success_url: "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
  cancel_url: "https://example.com/cancel",
  customer: stripeCustomerId,
});
```

## Webhook verification sketch

```js
const event = stripe.webhooks.constructEvent(
  rawBody, // must be raw bytes, not parsed JSON
  signatureHeader,
  webhookSecret
);

if (await alreadyProcessed(event.id)) return;
switch (event.type) {
  case "checkout.session.completed":
    await fulfill(event.data.object);
    break;
  default:
    break;
}
await markProcessed(event.id);
```

## Commands

```bash
stripe listen --forward-to localhost:3000/webhooks/stripe
stripe trigger payment_intent.succeeded
```

## Common pitfalls

| Pitfall | Result | Fix |
| --- | --- | --- |
| Parsed JSON body for webhooks | Signature verify fails | Use raw body parser |
| Fulfill on client redirect only | Missed payments / fraud | Fulfill on webhook |
| No idempotency | Double charge / double fulfill | Keys + event.id store |
| Price defined only on client | Price tampering | Server-side price IDs |

## Best practices

- Map Stripe objects to internal order rows with clear states (`pending`, `paid`, `failed`).
- Log event type + id, never full card payloads (you should not receive PANs with Checkout/Elements properly configured).
- Use Customer Portal for self-serve billing changes when appropriate.
- Review Radar rules before high-risk launches.

## Limitations

- Tax, VAT, and compliance requirements vary by jurisdiction (Stripe Tax may apply).
- Connect / marketplace money-flows need additional onboarding and payout logic.
- API versions are pinned per account - read changelogs when upgrading.

## Related skills

- `@nodejs` / `@fastapi` - webhook HTTP servers
- `@postgresql` - durable order state
- `@playwright` - checkout UI smoke tests in test mode
