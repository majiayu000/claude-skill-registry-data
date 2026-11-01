---
name: snippe-integration
description: Build integrations with Snippe (api.snippe.sh), a Tanzania payment processing API. Use this skill whenever the user mentions Snippe, is working on payment integrations for Tanzania (mobile money via M-Pesa, Airtel Money, Mixx by Yas, Halotel; credit/debit cards via Visa/Mastercard; dynamic QR codes), needs to accept TZS payments, sends payouts to Tanzanian mobile wallets or banks (CRDB, NMB, NBC, ABSA, Equity, KCB, Stanbic, etc.), verifies Snippe webhooks, or handles Snippe errors and idempotency. Covers the v2026-01-25 API — authentication, payments, hosted checkout sessions, disbursements, webhooks, and error handling.
---

# Snippe Integration

Snippe is a payment processor for Tanzania. This skill helps you build correct integrations: issuing API calls with the right auth, creating payments / sessions / payouts with the correct field shapes, verifying webhook signatures securely, and handling errors — including the subtle ones that are easy to get wrong.

You're writing code that talks to Snippe from the user's application. The user may be in any language (Node.js, Python, PHP, Go, Ruby, etc.); this skill gives you the protocol-level knowledge and you adapt the example code blocks to whatever language the user is already using.

## API basics

- **Base URL**: `https://api.snippe.sh`
- **API version**: `2026-01-25` (current stable)
- **Currency**: `TZS` only — other currencies return a `400 validation_error`. Amounts are integers in the smallest currency unit (no decimals).
- **Authentication**: Bearer token in the `Authorization` header. Keys look like `snp_...` and are shown once on creation in the Snippe Dashboard under Settings → API Keys.

```http
Authorization: Bearer snp_your_api_key_here
```

The API key carries a set of scopes, which the merchant selects when creating the key:

| Scope                 | Allows                    |
| --------------------- | ------------------------- |
| `collection:read`     | View payments and balance |
| `collection:create`   | Create payments           |
| `disbursement:read`   | View payouts              |
| `disbursement:create` | Create payouts            |

If you're building a collection-only service (e.g. a checkout), you only need `collection:*`. Don't request `disbursement:*` unless the app actually sends money out.

## Core concepts

Snippe has four resource families. Understanding which one your task needs is the first decision:

| Resource         | Purpose                                                              | Endpoint prefix    |
| ---------------- | -------------------------------------------------------------------- | ------------------ |
| **Payments**     | Collect money from customers (mobile money, card, QR)                | `/v1/payments`     |
| **Sessions**     | Hosted checkout pages — Snippe renders the UI and handles method selection | `/api/v1/sessions` |
| **Disbursements**| Send money out to mobile wallets or bank accounts                    | `/v1/payouts`      |
| **Webhooks**     | Real-time event delivery to your URL                                 | (your server)      |

**Payments vs Sessions** — this is the most common branching question:

- Use the **Payments API** when you want full control over the UI and you're building the payment form yourself. Every call creates a single payment intent for one channel (mobile / card / QR).
- Use **Sessions** when you want Snippe's hosted, mobile-optimised checkout page — a single URL that handles multiple methods, perfect for sharing via SMS/WhatsApp or embedding in simple apps.

## Quick start: accept a mobile money payment

The simplest end-to-end flow, from request to settlement.

### 1. Create the payment

```http
POST /v1/payments
Authorization: Bearer snp_your_api_key_here
Content-Type: application/json
Idempotency-Key: order-12345-attempt-1
```

```json
{
  "payment_type": "mobile",
  "details": { "amount": 500, "currency": "TZS" },
  "phone_number": "255781000000",
  "customer": {
    "firstname": "FirstName",
    "lastname": "LastName",
    "email": "customer@email.com"
  },
  "webhook_url": "https://yoursite.com/webhooks/snippe",
  "metadata": { "order_id": "ORD-12345" }
}
```

### 2. Response

```json
{
  "status": "success",
  "code": 201,
  "data": {
    "reference": "9015c155-9e29-4e8e-8fe6-d5d81553c8e6",
    "status": "pending",
    "payment_type": "mobile",
    "amount": { "currency": "TZS", "value": 500 },
    "expires_at": "2026-01-25T05:04:54Z"
  }
}
```

The customer's phone receives a USSD push. They enter their PIN, and Snippe posts `payment.completed` (or `payment.failed`) to the `webhook_url`. Payments expire after 4 hours if not authorised.

### 3. (Optional) Poll for status

If you can't receive webhooks — or you want a confirmation path that doesn't depend on them — poll:

```http
GET /v1/payments/{reference}
Authorization: Bearer snp_your_api_key_here
```

Prefer webhooks for real-time status; use polling only as a fallback or reconciliation tool.

## Critical rules (easy to get wrong)

These are the things that break integrations and cause support tickets. Check every one when writing code:

- **Currency is TZS only.** Attempting to send `USD`, `EUR`, or `KES` returns `400 validation_error`. Amounts are integers in the smallest unit — `500` means 500 TZS, not 5.00.
- **Minimum amounts**: 500 TZS for payments, 5,000 TZS for payouts. Values below these return a validation error.
- **Phone format**: `255XXXXXXXXX` (no plus) or `+255XXXXXXXXX` (with plus). Both work; local formats like `0781000000` do not.
- **`Idempotency-Key` must be ≤ 30 characters.** This is the single most common cause of the cryptic `PAY_001` error. If you see `PAY_001`, check the idempotency key length *before* assuming the upstream processor is down. Same-key-plus-different-body returns `422`; same-key-plus-same-body returns the cached response (valid for 24 hours). Always include an idempotency key on `POST /v1/payments` and `POST /v1/payouts/send`.
- **Webhook `data.amount` is an object**, not an integer. In webhook payloads you get `{"value": 50000, "currency": "TZS"}` — parse `.value` and `.currency` separately. This is the opposite of request bodies, where `details.amount` is a plain integer. Mismatched parsing here is a classic bug.
- **Verify webhook signatures against the raw request body** — read bytes as received and do not parse-and-re-serialize the JSON. Re-serialization changes whitespace or key ordering, which breaks the HMAC. In Express, use `express.raw({ type: "application/json" })`; in Flask, use `request.get_data(as_text=True)`; in Go, read `req.Body` with `io.ReadAll` *before* any JSON decode.
- **Reject webhooks with a timestamp older than 5 minutes** to prevent replay attacks. Check `X-Webhook-Timestamp` against current time before trusting the payload.
- **Use constant-time comparison** (`crypto.timingSafeEqual`, `hmac.compare_digest`, `hash_equals`, `hmac.Equal`) for the HMAC check — never `==` on strings. Timing attacks are real and easy to mitigate.
- **Deduplicate webhook events by `id`** — Snippe may deliver the same event more than once, and your handler must be idempotent.
- **Respond 2xx within 30 seconds** to webhooks, then process async. If you hit a database or do heavy work inline, you'll trigger the retry schedule (3 → 6 → 12 → 24 minutes, abandoned after 5 attempts).
- **Rate limit is 60 requests/minute.** Respect the `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, and `X-Ratelimit-Reset` headers. On `429`, back off until the reset time.
- **Webhook and redirect URLs must be HTTPS** and ≤ 500 characters. HTTP URLs are rejected.

## Picking the right reference file

Load only what your current task needs:

| If you're working on...                                 | Read                       |
| ------------------------------------------------------- | -------------------------- |
| Creating a mobile money / card / QR payment            | `references/payments.md`     |
| A hosted checkout page, payment link, or sharing a URL | `references/sessions.md`     |
| Sending money out (payroll, refunds, vendor payouts)   | `references/disbursements.md`|
| Receiving webhooks, verifying signatures, handling retries | `references/webhooks.md`  |
| Diagnosing an error response or validation failure    | `references/errors.md`       |

Each reference file is self-contained — you don't need to chain-read them. If the task touches multiple surfaces (e.g. "create a payment AND handle the webhook"), load both relevant files.

## Checking balance before a payout

Before creating a disbursement, it's a good habit to confirm you have enough balance:

```http
GET /v1/payments/balance
Authorization: Bearer snp_your_api_key_here
```

Returns `available` and `balance` objects in TZS. The fee for a payout is added on top of the amount, so for a 5,000 TZS payout with a 1,500 TZS fee you need at least 6,500 TZS available. Use `GET /v1/payouts/fee?amount=...` to calculate the exact fee first — this is documented in `references/disbursements.md`.

## Further reading

If a problem isn't covered here, the canonical docs are at `https://snippe.sh/docs/2026-01-25`. You can also append `.mdx` to any docs URL to get the raw markdown (e.g. `https://snippe.sh/docs/2026-01-25/payments/mobile-money.mdx`).
