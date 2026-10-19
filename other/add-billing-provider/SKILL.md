---
name: add-billing-provider
description: Implement a real payment provider adapter (Stripe, Paddle) behind Mathiz's billing.Provider interface, wire it into serve, and verify the money loop. Use when adding a payment provider, changing webhook handling, or touching checkout flows.
---

# Adding a billing provider adapter

Read `specs/14-monetisation.md` first — §4 (the abstraction) and the
"Provider decision: Stripe" section are binding. The interface is
deliberately thin: if your adapter seems to need more than the three
methods, the answer is almost always "keep it private to the adapter
file", not "widen `billing.Provider`".

## The contract (`internal/saas/billing/billing.go`)

`Provider`: `Name` / `CreateCheckout` / `PortalURL` / `ParseWebhook` →
`[]Event` with types `subscription_activated | subscription_renewed |
subscription_canceled | topup_purchased`. Everything downstream —
credit grants, plan-credit expiry on renewal, `billing_states` updates —
is `billing.Service.Apply`'s job. **An adapter never touches the credits
ledger directly**, and entitlements never live provider-side.

`Event.EventID` becomes the ledger idempotency `source` (`sub:<id>` /
`topup:<id>`), so it must be the provider's stable event ID — never a
generated UUID, or webhook retries double-grant.

## Recipe (Stripe as the worked example)

1. `internal/saas/billing/stripe.go` — implement the four methods:
   - `CreateCheckout`: Checkout Session — `mode=subscription` when
     `Plan.Subscription()`, `mode=payment` for top-ups. Price from
     `Plan.ProviderPriceID` (env `MATHIZ_BILLING_PRICE_<PLAN>`). Put
     `FamilySpaceID` + `PlanID` in session metadata (you need them back in
     the webhook). Success/cancel URLs = `CheckoutParams` paths resolved
     against `MATHIZ_PUBLIC_BASE_URL`.
   - `PortalURL`: a Billing Portal session for the stored customer ID.
   - `ParseWebhook`: verify the `Stripe-Signature` header against a new
     `MATHIZ_STRIPE_WEBHOOK_SECRET` env var — reject unsigned/tampered
     payloads with an error (the handler turns that into 400). Map:
     `checkout.session.completed` → activated/topup (by mode),
     `invoice.paid` → renewed, `customer.subscription.deleted` → canceled.
     Ignore (return zero events for) event types we don't model.
   - Per the spec: **no metered billing, no Stripe credit grants.**
2. Wire it: extend the `MATHIZ_BILLING_PROVIDER` switch in `cmd/serve.go`
   (the `fake` arm is the template — remove `stripe` from the "unsupported"
   error message). New env vars go in `internal/saas/server/config.go`,
   `.env.example`, `docker-compose.yml`, and CLAUDE.md's env list.
3. Leave the `fake` provider untouched — it is the dev UX and the test
   double for everything above the adapter.

## Tests / verification

- Unit-test `ParseWebhook` with synthesized payloads: valid signature,
  tampered signature (rejected), each mapped event type, unmapped types
  ignored.
- Replay safety: apply the same event twice through `billing.Service.Apply`
  and assert the balance is unchanged the second time. The lifecycle
  pattern to copy is `TestBillingLifecycle` in
  `internal/saas/server/billing_api_test.go`.
- `go test -race ./internal/saas/...`, then the `verify` skill matrix.
- Live smoke (needs user-supplied Stripe **test-mode** keys; never commit
  them): checkout a plan, confirm the webhook lands and
  `GET /api/v1/family/{id}/billing` shows the new balance/plan/status,
  then resend the webhook from the Stripe dashboard and confirm no
  double-grant. `stripe listen --forward-to localhost:8080/api/v1/billing/webhook`
  bridges webhooks to a local server.

## Invariant checklist before committing

- [ ] Adapter never grants/debits credits itself — only `Service.Apply` does
- [ ] Every `Event.EventID` is the provider's stable event ID
- [ ] Invalid/unsigned webhook → error → 400 (never a silent 2xx)
- [ ] Kid surfaces untouched: no prices/balances outside the parent dashboard
- [ ] Empty `MATHIZ_BILLING_PROVIDER` still boots with billing off (free)
- [ ] Secrets via env only; test keys never committed
