---
name: webhook-security
description: >
  Build webhook signature verification for Paymob, Stripe, Resend, and generic HMAC.
  Triggers when user asks to verify webhook signatures, add HMAC validation, handle
  payment webhooks (Paymob/Stripe), implement replay attack prevention, or set up
  webhook security middleware.
---

# Webhook Security Agent

## Step 1 — Identify the Platform
- Laravel (PHP) → middleware + controller approach
- Next.js (Node) → API route approach
- Go → http.Handler approach
- Generic → all approaches with stack-specific sections

## Step 2 — Choose the Gateway

### Paymob (Egypt)
- HMAC-SHA512 signature in `hmac` query param
- Raw body must be verified: `hash(hmac_secret, raw_body)`
- Verify: transaction `success` field + merchant order ID
- Refund: POST /v1/cashout/transactions/{id}/refund
- Idempotency key: merchant_order_id

### Stripe
- HMAC-SHA256 with `Stripe-Signature` header, `t=` timestamp + `v1=` signature
- Verify: `timing_safe_equal` to prevent timing attacks
- Replay protection: check timestamp within 300s window
- Idempotency key: Stripe-Idempotency-Key header

### Resend
- HMAC-SHA256 with `Resend-Signature` header
- Verify: raw body, `Resend-Webhook-Secret` env var
- Replay protection: same timestamp window as Stripe

### Generic HMAC
- Any string secret, any hash algorithm
- Verify: constant-time comparison
- Replay protection: optional timestamp validation

## Step 3 — Implement in Laravel

```php
// routes/web.php
Route::post('/webhook/paymob', [WebhookController::class, 'paymob']);
Route::post('/webhook/stripe', [WebhookController::class, 'stripe']);
Route::post('/webhook/resend', [WebhookController::class, 'resend']);

// app/Http/Middleware/VerifyWebhookSignature.php
class VerifyWebhookSignature {
    public function handle($request, $next, $secret, $algo = 'sha512') {
        $signature = $request->input('hmac') ?? $request->header('Stripe-Signature');
        $payload = $request->getContent();
        $expected = hash_hmac($algo, $payload, $secret);
        if (!hash_equals($expected, $signature)) {
            abort(401, 'Invalid signature');
        }
        return $next($request);
    }
}
```

## Step 4 — Implement in Next.js

```typescript
// app/api/webhook/paymob/route.ts
export async function POST(req: Request) {
  const raw = await req.text();
  const sig = req.headers.get('paymob-hmac') ?? '';
  const expected = crypto.createHmac('sha512', process.env.PAYMOB_HMAC_SECRET!)
    .update(raw).digest('hex');
  if (!timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) {
    return Response.json({ error: 'Invalid signature' }, { status: 401 });
  }
  const body = JSON.parse(raw);
  // process...
  return Response.json({ received: true });
}
```

## Step 5 — Idempotency + Replay Prevention
- Store processed `event_id` in Redis/DB with 24h TTL
- Skip if already processed
- Use merchant_order_id as idempotency key for Paymob
- Use Stripe-Idempotency-Key for Stripe

## Step 6 — Error Handling
- Return 200 only after processing is complete
- Queue failures → return 202 Accepted (processing async)
- Return 500 only for critical failures (trigger retry from provider)
- Log all webhook events to a webhook_events table

## Step 7 — Testing
- Use ngrok/Cloudflare Tunnel for local webhook testing
- Stripe: `stripe listen --forward-to localhost:3000/api/webhook/stripe`
- Paymob: set test mode in dashboard, use Paymob test cards
