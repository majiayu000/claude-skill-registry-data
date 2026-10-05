---
name: stripe
description: Stripe — payment processing with Checkout, PaymentIntents, webhooks, Connect, subscriptions.
---

## stripe

### Checkout
- `stripe.checkout.sessions.create({ line_items: [{ price: 'price_xxx', quantity: 1 }], mode: 'payment' })`.
- `success_url` / `cancel_url` — redirect after completion.
- Mode: `payment` (one-time), `subscription` (recurring), `setup` (save payment method).
- Prefilled fields: `customer_email`, `client_reference_id`, `metadata`.

### PaymentIntents
- `stripe.paymentIntents.create({ amount: 2000, currency: 'usd', automatic_payment_methods: { enabled: true } })`.
- `confirm: true` for client-side confirmation with Stripe.js.
- `setup_future_usage: 'off_session'` — save card for recurring charges.
- Status flow: `requires_payment_method` → `processing` → `succeeded` / `requires_action`.

### Webhooks
- Verify signature: `stripe.webhooks.constructEvent(body, signature, endpointSecret)`.
- Endpoint: `https://your-site.com/api/webhooks/stripe`.
- Common events: `checkout.session.completed`, `payment_intent.succeeded`, `invoice.paid`.
- Idempotency key: `stripe.webhookEndpoints.create({ enabled_events: [...] })`.

### Connect
- Platform accounts: `stripe.accounts.create({ type: 'express' })`.
- Onboarding: `stripe.accountLinks.create({ account, refresh_url, return_url, type: 'account_onboarding' })`.
- Direct charges: `stripe.paymentIntents.create({ ..., application_fee_amount: 100 })`.
- Transfers: `stripe.transfers.create({ amount, currency, destination: 'acct_xxx' })`.

### Subscriptions & Products
- Products: `stripe.products.create({ name: 'Pro Plan' })`; Prices: `stripe.prices.create({ product, unit_amount: 999, currency: 'usd', recurring: { interval: 'month' } })`.
- `stripe.subscriptions.create({ customer, items: [{ price: 'price_xxx' }] })`.
- `stripe.subscriptionItems.update(...)` — mid-cycle plan changes.
