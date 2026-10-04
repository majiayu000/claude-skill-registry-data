---
name: orbit-pay-paypal
description: PayPal integration audit — Smart Buttons (client SDK), REST API v2 (Orders + Payments), webhook signature verification (PAYPAL-AUTH-ALGO + PAYPAL-CERT-URL), IPN deprecation (use webhooks), sandbox vs live, currency restrictions per region. Use when the user says "PayPal integration", "Smart Buttons", "PayPal webhook", "IPN".
---

# 🪐 orbit-pay-paypal — PayPal SDK integration

PayPal's API is messier than Stripe's — multiple auth flows, multiple SDKs, IPN deprecation in progress. This skill enforces the modern (v2 REST + Webhooks) path.

---

## What this skill checks

### 1. Use REST API v2, not v1
**Whitepaper intent:** PayPal v1 (older Express Checkout, Adaptive Payments) is feature-frozen. New plugins should use v2 REST + Smart Buttons. Plugins still using v1 will eventually break.

### 2. Smart Buttons (client SDK)
```html
<div id="paypal-button-container"></div>
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
<script>
  paypal.Buttons({
    createOrder: (data, actions) => actions.order.create({
      purchase_units: [{ amount: { value: '20.00' } }],
    }),
    onApprove: (data, actions) => actions.order.capture().then(details => {
      // POST capture details to your server for verification
    }),
  }).render('#paypal-button-container');
</script>
```

### 3. Server-side verification (don't trust client)
After `onApprove`, your server must call:
```php
$response = wp_remote_get(
  "https://api.paypal.com/v2/checkout/orders/{$order_id}",
  [ 'headers' => [ 'Authorization' => "Bearer $access_token" ] ]
);
$body = json_decode( wp_remote_retrieve_body( $response ) );
if ( $body->status !== 'COMPLETED' ) wp_die( 'Order not complete.' );
```

### 4. Webhook signature verification
PayPal webhooks include `PAYPAL-AUTH-ALGO`, `PAYPAL-CERT-URL`, `PAYPAL-TRANSMISSION-ID`, `PAYPAL-TRANSMISSION-SIG`, `PAYPAL-TRANSMISSION-TIME` headers.

```php
$verified = verify_paypal_webhook(
  $headers,
  $raw_body,
  $webhook_id  // from PayPal dashboard
);
if ( ! $verified ) {
  http_response_code( 400 );
  exit;
}
```

### 5. IPN deprecation (don't use for new code)
IPN (Instant Payment Notification) is deprecated. Use webhooks (`/v1/notifications/webhooks-events`). Plugins still using IPN are tech-debt.

### 6. OAuth2 token caching
Don't request a new access token per API call — cache for 9 hours (token TTL).
```php
$token = get_transient( 'my_plugin_paypal_token' );
if ( ! $token ) {
  $token = request_paypal_token();
  set_transient( 'my_plugin_paypal_token', $token, 9 * HOUR_IN_SECONDS );
}
```

### 7. Sandbox vs live
```php
$base = $is_sandbox ? 'https://api.sandbox.paypal.com' : 'https://api.paypal.com';
```

Don't ship sandbox-only credentials to production.

### 8. Currency support varies by country
Some currencies are unavailable in some PayPal countries. Validate before showing the button.

---

## Output

```markdown
# PayPal Integration — my-plugin

✓ Uses REST v2 (Orders + Payments)
✓ Server-side verification after onApprove
❌ Webhook signature NOT verified — handler trusts incoming POST
   → Add verify_paypal_webhook before processing
⚠ Still uses IPN (deprecated) — migrate to webhooks
✓ OAuth2 token cached 9h via transient
⚠ Sandbox + live keys both stored in same option — risk of crossover
```

---

## Pair with

- `/orbit-pay-stripe` — for plugins offering both
- `/orbit-wp-security` — secret-handling

---

## Sources & Evergreen References

### Canonical docs
- [PayPal Developer](https://developer.paypal.com/) — root
- [REST API v2](https://developer.paypal.com/docs/api/orders/v2/) — Orders + Payments
- [Smart Buttons](https://developer.paypal.com/docs/checkout/) — client SDK
- [Webhooks](https://developer.paypal.com/api/rest/webhooks/) — server events
- [IPN Deprecation](https://developer.paypal.com/api/nvp-soap/ipn/) — migrate notice

### Last reviewed
- 2026-04-29 — PayPal makes API changes ~yearly; re-check before each release
