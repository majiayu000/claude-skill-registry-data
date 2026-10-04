---
name: orbit-pay-stripe
description: Stripe API integration audit — fetches Stripe's CURRENT API reference + recommended primitives + SCA rules AT RUNTIME. Auto-stays-current when Stripe ships new API versions / new primitives (e.g. Payment Element). Use when the user says "Stripe integration", "Stripe API", "PaymentIntent", "Payment Element", "Stripe webhook", "SCA / 3DS".
---

# 🪐 orbit-pay-stripe — Runtime-evergreen Stripe SDK audit

> Stripe ships major API versions yearly + new primitives quarterly. This skill fetches what Stripe currently recommends, not a 2024 snapshot.

---

## Runtime — fetch live before auditing (DO THIS FIRST)

When this skill is invoked:

1. **Fetch in parallel**:
   - https://docs.stripe.com/api → current API version + reference
   - https://docs.stripe.com/payments → current Payments doc
   - https://docs.stripe.com/payments/payment-intents → PaymentIntents reference
   - https://docs.stripe.com/payments/payment-element → Payment Element (newer alternative)
   - https://docs.stripe.com/strong-customer-authentication → SCA / 3DS
   - https://docs.stripe.com/webhooks/signatures → signature verification
   - https://docs.stripe.com/security/guide → PCI-DSS compliance

2. **Synthesize current state**:
   - "What's Stripe's currently-recommended UI primitive? Card Element / Payment Element / something newer?"
   - "What's the current API version date Stripe pins?"
   - "Have any patterns been deprecated since this skill was last run?"
   - "What's the current SCA/3DS rule for the user's payment flow?"

3. **Audit the plugin** against fetched current rules.

---

## What gets checked

### A. API key handling
- ❌ Hardcoded `sk_live_*` in source
- ❌ Secret keys committed to git
- ❌ Secret keys in client-side JS (only `pk_live_*` publishable should be there)
- ❌ Secret keys in plain log output

```php
// ✅
$stripe = new \Stripe\StripeClient( get_option( 'my_plugin_stripe_secret_key' ) );
```

### B. Idempotency keys (prevent double-charges)
```php
$stripe->paymentIntents->create([
  'amount' => 2000,
  'currency' => 'usd',
], [
  'idempotency_key' => 'order_' . $order_id,
]);
```

### C. Webhook signature verification
```php
try {
  $event = \Stripe\Webhook::constructEvent( $payload, $sig_header, $endpoint_secret );
} catch ( \Stripe\Exception\SignatureVerificationException $e ) {
  http_response_code( 400 ); exit;
}
```

### D. Payment Element vs Card Element
**Per fetched Stripe docs:** Payment Element (newer) replaces Card Element for most flows. Single drop-in supports cards + wallets + bank methods. Card Element still works but Stripe recommends Payment Element for new code.

```js
// ✅ Modern (per current Stripe docs):
const elements = stripe.elements({ clientSecret });
const paymentElement = elements.create('payment');  // ← not 'card'
paymentElement.mount('#payment-element');
```

If the plugin uses `elements.create('card')`, the audit suggests migrating to Payment Element (citing today's Stripe doc).

### E. SCA / 3DS handling
EU customers require SCA for transactions > 30 EUR. PaymentIntents handle this automatically; Charges API doesn't. Plugins still using Charges API will fail SCA on EU cards.

### F. PCI-DSS scope minimisation
Card data must NEVER touch your server.
```js
// ✅ Tokenise client-side, send token to your server
const { paymentMethod } = await stripe.createPaymentMethod({ type: 'card', card });
// Send paymentMethod.id to server — your server NEVER sees the card number
```

### G. Test mode vs live mode environment guard
```php
$is_live = strpos( get_option( 'stripe_secret_key' ), 'sk_live_' ) === 0;
if ( $is_live && wp_get_environment_type() !== 'production' ) {
  wp_die( 'Live keys on non-production — refusing.' );
}
```

### H. Subscription lifecycle (if applicable)
- Renewal: handle `invoice.payment_succeeded`
- Failed renewal: handle `invoice.payment_failed`, retry via Smart Retries or Stripe's dunning
- Cancel: `customer.subscription.deleted`

### I. Webhook event timestamp (replay attack)
Reject events older than 5 minutes:
```php
if ( time() - $event->created > 300 ) {
  http_response_code( 400 ); exit;
}
```

---

## Output

```markdown
# Stripe Integration — my-plugin · 2026-04-30

> Per docs.stripe.com (fetched 2026-04-30 14:32 UTC):
> Current recommended UI primitive: Payment Element
> SCA: required for EU transactions > 30 EUR

## Static checks
- ✓ Secret key in option (not source)
- ✓ Webhook signature verified
- ⚠ Plugin uses Card Element — Payment Element is newer Stripe recommendation
- ❌ No idempotency_key on PaymentIntent create — double-charge risk
- ⚠ No replay guard on webhook (event.created not checked)
- ✓ Test/live mode guarded by wp_get_environment_type
- ✓ Stripe Elements used for card capture (no PCI scope on plugin side)

## Severity: HIGH (idempotency + webhook replay)
```

---

## Pair with

- `/orbit-pay-paypal` — peer payment SDK
- `/orbit-pay-edd` / `-freemius` — license-server (often paired with Stripe billing)
- `/orbit-wp-security` — secret handling
- `/orbit-uat-membership` — subscription-lifecycle UAT
- `/orbit-vdp` — disclose vulns in payment code responsibly

---

## Smoke test

Input: a plugin that calls `paymentIntents->create` without `idempotency_key`.
Expected:
- ❌ HIGH — idempotency_key missing
- Cites docs.stripe.com/api/idempotent_requests with today's fetch timestamp

---

## Embedded fallback rules (offline)
- Secret key in option, NEVER in code
- Idempotency key on PaymentIntent create
- Webhook signature verified + replay-guard < 5 min
- Use PaymentIntents (not Charges) for SCA
- Tokenise client-side; server never sees card number
- Environment guard for test vs live keys

## Sources & Evergreen References

### Live sources (fetched on every run)
- [Stripe API Reference](https://docs.stripe.com/api)
- [Payments doc](https://docs.stripe.com/payments)
- [Payment Element](https://docs.stripe.com/payments/payment-element)
- [PaymentIntents](https://docs.stripe.com/payments/payment-intents)
- [SCA / 3DS](https://docs.stripe.com/strong-customer-authentication)
- [Webhook Signatures](https://docs.stripe.com/webhooks/signatures)
- [PCI-DSS Guide](https://docs.stripe.com/security/guide)

### Last reviewed
2026-04-30 — runtime-evergreen
