---
name: paymob-integrator
description: >
  Integrate Paymob (Egypt payment gateway) into Laravel or Next.js applications.
  Covers: token exchange, payment link generation, card/wallet/installment payments,
  HMAC webhook verification, refund processing, and test card setup.
  Triggers when user asks to add Paymob, integrate Egyptian payments, or build
  Paymob checkout for Egypt-focused projects.
---

# Paymob Payment Integrator Agent

## Paymob API Overview

Base URL: `https://accept.paymob.com/v1/`
Test base: `https://accept.staging.paymob.com/v1/`

Key flows:
1. Auth → get token
2. Order → create merchant order
3. Payment Key → generate one-time payment key (for card/wallet)
4. Webhook → verify payment success
5. Refund → process refunds

## Step 1 — Laravel Integration

### Install
```bash
composer require guzzlehttp/guzzle
```

### Service Class
```php
// app/Services/PaymobService.php
class PaymobService
{
    private string $apiKey;
    private string $baseUrl = 'https://accept.paymob.com/v1/';

    public function __construct()
    {
        $this->apiKey = config('services.paymob.api_key');
    }

    public function getAuthToken(): string
    {
        $res = Http::post($this->baseUrl . 'auth/tokens', [
            'api_key' => $this->apiKey,
        ]);
        return $res['token'];
    }

    public function createOrder(int $amountCents, string $merchantOrderId): array
    {
        $token = $this->getAuthToken();
        return Http::withToken($token)->post($this->baseUrl . 'ecommerce/orders', [
            'auth_token' => $token,
            'merchant_id' => config('services.paymob.merchant_id'),
            'merchant_order_id' => $merchantOrderId,
            'amount_cents' => $amountCents,
            'currency' => 'EGP',
            'items' => [],
        ])->json();
    }

    public function getPaymentKey(
        string $orderId,
        int $amountCents,
        string $billingDataHash,
        array $extras = []
    ): string {
        $token = $this->getAuthToken();
        $res = Http::withToken($token)->post($this->baseUrl . 'acceptance/payments/pay', [
            'auth_token' => $token,
            'order_id' => $orderId,
            'amount_cents' => $amountCents,
            'currency' => 'EGP',
            'billing_data' => json_decode($billingDataHash, true),
            'billing_data_hash' => $billingDataHash,
            'extras' => $extras,
        ])->json();
        return $res['token'];
    }

    public function refund(int $transactionId, int $amountCents): array
    {
        $token = $this->getAuthToken();
        return Http::withToken($token)->post(
            $this->baseUrl . 'acceptance/payments/refund',
            [
                'auth_token' => $token,
                'transaction_id' => $transactionId,
                'amount_cents' => $amountCents,
            ]
        )->json();
    }
}
```

### Generate Payment Link (for guest booking)
```php
public function generatePaymentLink(
    string $guestEmail,
    string $guestPhone,
    int $amountEGP,
    string $merchantOrderId,
    string $successCallback,
    string $failCallback
): string {
    $amountCents = $amountEGP * 100;
    $order = $this->createOrder($amountCents, $merchantOrderId);

    $token = $this->getAuthToken();
    $res = Http::withToken($token)->post($this->baseUrl . 'acceptance/payments/pay', [
        'auth_token' => $token,
        'order_id' => $order['id'],
        'amount_cents' => $amountCents,
        'currency' => 'EGP',
        'billing_data' => [
            'email' => $guestEmail,
            'first_name' => 'Guest',
            'last_name' => 'User',
            'phone_number' => $guestPhone,
        ],
        'payment_methods' => [512],
        'redirection_url' => $successCallback,
    ]);

    return "https://accept.paymob.com/v2/choose/payment-methods?token=" . $res['token'];
}
```

## Step 2 — Webhook Handler

```php
// app/Http/Controllers/PaymobWebhookController.php
class PaymobWebhookController extends Controller
{
    public function handle(Request $request)
    {
        $raw = $request->getContent();
        $hmac = $request->input('hmac');

        $expected = hash_hmac('sha512', config('services.paymob.hmac_secret'), $raw);
        if (!hash_equals($expected, $hmac ?? '')) {
            \Log::warning('Paymob invalid signature', ['ip' => $request->ip()]);
            return response('Unauthorized', 401);
        }

        $type = $request->input('type');
        $obj = $request->input('obj');

        match ($type) {
            'TRANSACTION_CREATED' => $this->handleSuccessPayment($obj),
            'TRANSACTION_REFUND' => $this->handleRefund($obj),
            default => response('OK'),
        };
    }

    private function handleSuccessPayment(array $obj)
    {
        // Idempotency: skip if already processed
        if (\App\Models\Payment::where('paymob_tx_id', $obj['id'])->exists()) {
            return response('Already processed');
        }

        // Find booking by merchant_order_id
        $booking = \App\Models\Booking::where('merchant_order_id', $obj['merchant_order_id'])->first();
        if ($booking) {
            $booking->update([
                'status' => 'confirmed',
                'paymob_transaction_id' => $obj['id'],
                'paymob_status' => $obj['success'] ? 'paid' : 'failed',
            ]);
        }

        // Trigger n8n
        app(\App\Services\N8nService::class)->trigger('booking.confirmed', [
            'booking_id' => $booking?->id,
            'amount' => $obj['amount_cents'] / 100,
            'currency' => 'EGP',
        ]);

        return response('OK');
    }
}
```

## Step 3 — Next.js Integration

```typescript
// lib/paymob.ts
const BASE_URL = 'https://accept.paymob.com/v1/';

export async function getPaymobToken(): Promise<string> {
  const res = await fetch(`${BASE_URL}auth/tokens`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key: process.env.PAYMOB_API_KEY }),
  });
  return (await res.json()).token;
}

export async function createPaymobOrder(
  amountCents: number,
  merchantOrderId: string,
  token: string
) {
  const res = await fetch(`${BASE_URL}ecommerce/orders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      auth_token: token,
      merchant_id: process.env.PAYMOB_MERCHANT_ID,
      merchant_order_id: merchantOrderId,
      amount_cents: amountCents,
      currency: 'EGP',
      items: [],
    }),
  });
  return res.json();
}

export async function getPaymentKey(
  orderId: number,
  amountCents: number,
  token: string,
  billingEmail: string
) {
  const res = await fetch(`${BASE_URL}acceptance/payments/pay`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      auth_token: token,
      order_id: orderId,
      amount_cents: amountCents,
      currency: 'EGP',
      billing_data: {
        email: billingEmail,
        first_name: 'Guest',
        last_name: 'User',
        phone_number: '01000000000',
      },
      payment_methods: [512],
    }),
  });
  return (await res.json()).token;
}
```

## Step 4 — Test Cards (Sandbox Mode)
```
Card number:  4200000000000000
Cardholder:   any name
Expiry:        any future date (MM/YY)
CVV:           any 3 digits
OTP:           123456 (or any 6 digits)
3DS:           bypassed in test mode

Test wallet:   VODAFONE_CASH → 01000000000 / any PIN
```

## Step 5 — Go Live Checklist
- [ ] Paymob merchant account active
- [ ] HMAC secret set in Paymob dashboard
- [ ] Webhook URL registered in Paymob dashboard (HTTPS required)
- [ ] Test cards verified in staging
- [ ] Production API key swapped
- [ ] EGP currency enabled
