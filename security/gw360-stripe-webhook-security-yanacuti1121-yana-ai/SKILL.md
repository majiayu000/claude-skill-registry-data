---
name: stripe-webhook-security
description: Verify and process Stripe webhooks safely against the real-world failure modes. Covers signature verification against the raw body, idempotency keys, replay protection, event-type allowlists, the partial-refund and dual-currency traps, and re-fetching authoritative state from Stripe for real-money actions. Invoke when wiring webhooks for the first time, when adding a new event type, or after a payments incident.
---

# Stripe Webhook Security

Stripe webhooks are how a payment provider tells your backend that things happened. If they are wrong — forged, replayed, or processed twice — you ship product without payment, or charge customers twice, or skip a refund. This skill covers the patterns that prevent that.

Applies to Stripe (and largely to other PSPs with similar webhook designs: Paddle, Mollie, Adyen). Examples are Node/Express; the principles port.

## When to invoke

- Wiring a new Stripe webhook endpoint
- Adding a new event type to an existing handler
- Investigating a payments incident (mismatched orders, double-charge, missing refunds)
- Migrating from test mode to live mode
- Auditing an inherited integration

## The three rules

A webhook handler must do all three of these. Skipping any one is a bug.

1. **Verify the signature** before trusting any field
2. **Be idempotent** — receiving the same event twice does nothing extra
3. **Use the event as a hint, not a source of truth** for high-value actions

## Rule 1 — Signature verification (on raw body)

Stripe signs the request with `STRIPE_WEBHOOK_SECRET`. Verification only works on the **exact raw bytes** Stripe sent — JSON-parsing first destroys the signature.

```ts
// Express — register the raw-body middleware ONLY for the webhook route
import express from 'express';
import Stripe from 'stripe';

const app = express();
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2024-12-18.acacia' });

// IMPORTANT: do not use express.json() ahead of this route
app.post(
  '/webhooks/stripe',
  express.raw({ type: 'application/json', limit: '1mb' }),
  async (req, res) => {
    const sig = req.headers['stripe-signature'] as string;
    let event: Stripe.Event;
    try {
      event = stripe.webhooks.constructEvent(
        req.body,                          // Buffer, NOT parsed
        sig,
        process.env.STRIPE_WEBHOOK_SECRET!
      );
    } catch (err) {
      // Signature invalid — do NOT log the body
      return res.status(400).send('invalid signature');
    }
    await handle(event);
    res.json({ received: true });
  }
);

// Other routes use JSON parsing normally
app.use(express.json());
```

Common mistakes:

- `app.use(express.json())` before the webhook route → body is parsed → signature fails
- Verifying with the wrong secret (test mode vs live mode — each has its own)
- Storing the secret in a place readable by the application but also by other tenants on the same host
- Multiple endpoints registered in Stripe Dashboard, each with a different secret — make sure the env var matches the endpoint URL it serves

## Rule 2 — Idempotency

Stripe will retry webhooks if your endpoint times out or 5xx's. The same `event.id` may arrive 10 times. Your handler must produce the same effect whether it runs once or ten times.

```ts
// Pseudocode: dedup by event.id at the DB layer
async function handle(event: Stripe.Event) {
  const inserted = await db.processedEvents.insertIgnoreConflict({
    id: event.id,
    type: event.type,
    received_at: new Date(),
  });
  if (!inserted) {
    // We've already processed this event — return success without re-running side effects
    return;
  }

  await processSideEffects(event);
}
```

In SQL, the dedup table:

```sql
CREATE TABLE processed_stripe_events (
  id            TEXT PRIMARY KEY,         -- event.id
  type          TEXT NOT NULL,
  received_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  payload_hash  TEXT                       -- optional: SHA256 of event for forensic comparison
);
```

Insert with `ON CONFLICT DO NOTHING`; check whether a row was actually inserted to decide whether to run side effects.

Idempotency at the action layer too:

- **Order fulfillment**: keyed by Stripe `payment_intent.id`, not arbitrary order ID. If retried, fulfillment runs once.
- **Refund issuance**: keyed by the refund event ID. Same.
- **Email sends**: keyed by `event.id + recipient` so a retry does not double-email.

## Rule 3 — Use the event as a hint, then fetch fresh

For anything important, do not trust the event body's amount/status/metadata. The event tells you "something happened with `pi_xxx`"; you then `stripe.paymentIntents.retrieve(pi_xxx)` and read the authoritative current state.

```ts
async function onPaymentIntentSucceeded(event: Stripe.Event) {
  const piFromEvent = event.data.object as Stripe.PaymentIntent;
  // Re-fetch — authoritative state
  const pi = await stripe.paymentIntents.retrieve(piFromEvent.id);
  if (pi.status !== 'succeeded') return;     // Defensive — state changed since event fired

  const amountMinor = pi.amount_received;
  const currency = pi.currency;
  const orderId = pi.metadata.order_id;      // Set during PI creation

  await fulfillOrder({ orderId, amountMinor, currency, paymentIntentId: pi.id });
}
```

Why: an event body is fixed at the moment Stripe sent it, but a payment can be partially refunded, disputed, or otherwise mutated by the time your handler runs. For real-money decisions, fetch fresh.

## Event-type allowlist

Stripe sends many event types you almost never care about. Listen for exactly the ones you handle, ignore the rest cleanly.

```ts
const HANDLED_EVENTS = new Set([
  'payment_intent.succeeded',
  'payment_intent.payment_failed',
  'charge.refunded',
  'charge.dispute.created',
  'customer.subscription.updated',
  'customer.subscription.deleted',
  'invoice.payment_failed',
]);

async function handle(event: Stripe.Event) {
  if (!HANDLED_EVENTS.has(event.type)) {
    // Ignore unknown types — 200 so Stripe doesn't retry
    return;
  }
  switch (event.type) {
    case 'payment_intent.succeeded': return onPaymentIntentSucceeded(event);
    // ...
  }
}
```

In the Stripe Dashboard, also subscribe the endpoint **only** to the events you handle — reduces noise and reduces what an attacker could craft if the endpoint were somehow misconfigured.

## Replay protection

Signature verification with `constructEvent` includes a timestamp check (default tolerance 5 minutes). An old captured webhook will not replay successfully outside that window.

Belt-and-braces: the dedup table above also catches replays of valid events. Together they cover both attack and accident.

## Money — the traps that actually bite

These are the failure modes that show up in real Stripe integrations.

**The cents trap.** Stripe amounts are in the **minor unit** (cents, kobo, etc.). `1234` = €12.34. Comparing `amount > 100` thinking it's euros is a 100x bug.

**The currency trap.** A `payment_intent.succeeded` for an order is only valid if its **currency matches** what you priced the order in. A €10 order paid in JPY at the wrong rate is fraud-shaped.

```ts
if (pi.currency !== order.currency.toLowerCase()) {
  await flagForReview(order.id, 'currency mismatch');
  return;
}
if (pi.amount_received < order.expectedAmountMinor) {
  await flagForReview(order.id, 'underpayment');
  return;
}
```

**The race trap.** Two events for the same order arrive within ms (e.g. `payment_intent.succeeded` and `charge.succeeded`). Both try to fulfill. Without idempotency or row-level locks, the order gets fulfilled twice.

**The partial-refund trap.** `charge.refunded` does not always mean a full refund. Read `charge.amount_refunded` and `charge.refunded` (boolean). Refund-issued ≠ order-fully-refunded.

**The dispute trap.** `charge.dispute.created` is the start of a chargeback. The money is gone from your account immediately, but your fulfillment may continue if you don't act on the event. Pause shipping / access; do not auto-refund (you'll double-refund yourself).

## Stripe Connect specifics

If you are running platform / Connect, additional notes:

- **`account` field** on the event tells you which connected account it belongs to. Use it to scope queries — never assume events are platform-only.
- **Application fees** are charged on the platform's account; refunds and reversals need their own handler logic.
- **Connected-account webhooks vs platform webhooks** are separately configured. Make sure both are signed and both endpoints are protected.

## Endpoint exposure

- **HTTPS only** — Stripe will not send to HTTP in production
- **Endpoint is public by necessity** — Stripe needs to reach it, so you cannot IP-allowlist arbitrarily. If you want extra protection, Stripe publishes a webhook IP list; allowlist those at Cloudflare/WAF.
- **Rate limit defensively** — even though only Stripe should hit it, an attacker who knows the URL will probe. A few rps cap is fine.
- **Do not leak in errors** — if signature verification fails, respond `400` with no detail. Don't echo back what was wrong.

## Testing

- **Stripe CLI** for local testing: `stripe listen --forward-to localhost:3000/webhooks/stripe` — uses a separate test secret you copy from CLI output.
- **Replay an event** from the dashboard to test idempotency: dispatch the same event twice, confirm side effects fire once.
- **Test all the failure paths**: bad signature, malformed body, unknown event type, retry after timeout, currency mismatch, partial refund.

## Audit checklist

For a webhook handler going to production:

- [ ] Raw body middleware applied only to the webhook route, ahead of JSON parser
- [ ] Signature verified with `stripe.webhooks.constructEvent`
- [ ] `STRIPE_WEBHOOK_SECRET` matches the endpoint registered in Stripe Dashboard
- [ ] Live secret and test secret are distinct env vars, not swapped
- [ ] Dedup table keyed on `event.id` is in place
- [ ] For real-money actions, you re-fetch authoritative state via Stripe API
- [ ] Currency and amount cross-checked against the order's expectation
- [ ] Event-type allowlist filters out everything not explicitly handled
- [ ] Partial refunds, disputes, and Connect (if applicable) have specific handlers
- [ ] No PII or secret values in 4xx response bodies or error logs
- [ ] Webhook endpoint is HTTPS, with optional IP allowlist for Stripe ranges
- [ ] Stripe CLI tested locally, dashboard "send test webhook" tested in staging

## What this skill will not do

- Help bypass Stripe authentication or fake webhook signatures
- Recommend trusting webhook payloads for high-value decisions without re-fetch
- Replace Stripe's own integration documentation for product-specific flows
