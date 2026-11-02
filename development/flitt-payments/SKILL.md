---
name: flitt-payments
description: Flitt payment API implementation guidance for auth, SHA1 request/callback signatures, sandbox testing, hosted checkout, Payment (redirect), Payment (direct), saved-card /api/recurring charges, card token saving, scheduled subscriptions, reversals/refunds, captures for preauth payments, reservation_data payloads, supported currencies, callback/webhook handling, response codes, 3DS steps, order status polling, and response handling. Use when Codex needs to integrate or debug Flitt payments, create payment requests, build or verify signatures, attach reservation_data, validate currency support, implement callback handlers, interpret response codes, obtain or charge a rectoken, create/cancel subscriptions, reverse/refund through /api/reverse/order_id, capture through /api/capture/order_id, poll status, or troubleshoot Flitt API failures.
paths:
  - "**/*payment*"
  - "**/*checkout*"
  - "**/*flitt*"
  - "**/*billing*"
  - "**/*subscription*"
---

# Flitt Payments

## Core Workflow

Use this skill for Flitt payment API work, starting with authentication and testing.

1. Read `references/testing-auth.md` when the task involves sandbox credentials, test cards, request shape, response interpretation, or signature troubleshooting.
2. Read `references/sending-request.md` when the task involves checkout flow design, redirect endpoints, request/response envelopes, callback handling, or choosing between browser form POST and host-to-host checkout URL creation.
3. Read `references/payment-redirect.md` when the task involves Payment (redirect) parameters, checkout URL creation, HTML form redirect creation, embedded checkout token creation, or `/api/status/order_id` polling.
4. Read `references/payment-direct.md` when the task involves Payment (direct), raw card parameters, PCI DSS merchant flows, or `/api/3dsecure_step1` and `/api/3dsecure_step2`.
5. Read `references/payment-saved-card.md` when the task involves Payment with saved card, `rectoken`, recurring/tokenized charges, or `/api/recurring`.
6. Read `references/saving-cards.md` when the task involves obtaining `rectoken`, `required_rectoken=Y`, verification-based tokenization, or the first-purchase card-save flow.
7. Read `references/reversal.md` when the task involves refunds, reversals, partial/full reverse, `reverse_id`, `/api/reverse/order_id`, or reversal status.
8. Read `references/capture.md` when the task involves capture, preauth hold completion, partial capture, `/api/capture/order_id`, or capture status.
9. Read `references/subscriptions.md` when the task involves scheduled subscriptions, `subscription=Y`, `recurring_data`, `/api/subscription`, or starting/stopping subscriptions.
10. Read `references/additional-data.md` when the task involves `reservation_data`, checkout custom fields, fiscalisation products, payer metadata, or forcing/relaxing 3DS behavior through additional data.
11. Read `references/currencies.md` when the task involves validating the `currency` field, merchant-country currency support, or payment currency selection.
12. Read `references/callbacks.md` when the task involves `server_callback_url`, webhook endpoints, retries, firewall/IP allowlists, or verifying asynchronous payment notifications.
13. Read `references/signature.md` when the task is specifically about Flitt signature generation, verification failures, lowercasing, empty parameters, `/api/recurring` signing, or callback/redirect signature mismatches.
14. Read `references/response-codes.md` when the task involves `response_code`, API failures, embedded-checkout JavaScript error codes, decline interpretation, or deciding whether merchant, issuer, or Flitt must solve the problem.
15. Use `scripts/flitt_signature.py` instead of hand-writing SHA1 signature code for flat request/response parameters.
16. Keep public Flitt test credentials out of production code. Use environment variables or the app's secret manager for real merchant credentials.
17. Treat `response_status` as the HTTP/API processing status, not the payment result. Inspect payment-specific fields such as `order_status`, `reverse_status`, `reversal_amount`, `capture_status`, subscription `status`, and `response_code` for operation outcome.

## Authentication

Flitt API requests are HTTPS `POST` requests. Every signed request includes a `signature` parameter inside the root `request` object.

Generate the signature from:

1. The merchant payment secret key.
2. All non-empty request or response parameters except `signature` and `response_signature_string`.
3. Parameters sorted alphabetically by key.
4. Values joined with `|`, encoded as UTF-8, then hashed with SHA1.

Use the helper:

```bash
python3 ~/.codex/skills/flitt-payments/scripts/flitt_signature.py \
  --secret test \
  --params '{"merchant_id":1549901,"amount":1000,"currency":"GEL","order_desc":"Test payment","order_id":"TestOrder2","server_callback_url":"http://myshop/callback/"}'
```

To verify a received signature:

```bash
python3 ~/.codex/skills/flitt-payments/scripts/flitt_signature.py \
  --secret "$FLITT_PAYMENT_KEY" \
  --params-file response.json \
  --verify "$FLITT_RESPONSE_SIGNATURE"
```

If `response.json` has a root `response` or `request` object, the helper signs that inner object automatically.

## Testing

Use Flitt test merchant data only for sandbox work:

- Purchase merchant: `merchant_id=1549901`, secret key `test`
- Payout secret key: `testcredit`
- Test card data: load `references/testing-auth.md`

For manual test flows, choose cards deliberately:

- Use an approve card for happy-path checkout.
- Use a decline card when verifying failure UI and webhook handling.
- Use 3DS challenge/frictionless cards when validating redirect and callback handling.
- Use Open Banking `payment_method=x` only for Demo Bank testing.

## Sending Requests

Use the hosted checkout flow unless the user explicitly needs direct card entry or another specialized Flitt API.

- Scheme A: create an HTML form and submit the customer browser to `https://pay.flitt.com/api/checkout/redirect/` with HTTPS `POST`.
- Scheme B: send a server-to-server JSON request to `https://pay.flitt.com/api/checkout/url/`, read `checkout_url` from the response, then redirect the customer there.
- Always include Flitt parameters under a root `request` object for JSON requests.
- Always handle both customer return (`response_url`) and server-to-server callback (`server_callback_url`) when available; use the callback as the reliable status update.

For Payment (redirect) details, load `references/payment-redirect.md`.

## Direct Payments

Use Payment (direct) only when the merchant is intentionally PCI DSS compliant and the app is allowed to collect/process card data directly.

- Direct card requests include raw `card_number`, `cvv2`, and `expiry_date` values; never log or persist those values unless the project has explicit compliant storage controls.
- Start direct 3DS authentication with `POST /api/3dsecure_step1`.
- If 3DS is required, submit the customer to `acs_url` with `PaReq`, `MD`, and `TermUrl`.
- Complete the transaction with `POST /api/3dsecure_step2` using returned `pares` and `md`.
- For details, load `references/payment-direct.md`.

## Saved Card Payments

Use Payment with saved card when charging a previously issued Flitt `rectoken`.

- Create saved-card charges with `POST /api/recurring`.
- Send JSON with root `request`; the endpoint is always host-to-host.
- Redirect and 3DS flows are not available on `/api/recurring`; use Payment (direct) if 3DS is required.
- Treat `rectoken` as sensitive payment data and avoid logging it.
- For details, load `references/payment-saved-card.md`.

## Saving Cards

Use the saving-cards reference when the task is about obtaining a new `rectoken`, not charging an existing one.

- Request token issuance with `required_rectoken=Y` during create-order flow.
- Option 1: save card during verification with `verification=Y` and a small amount that is held then reversed.
- Option 2: save card during the first real purchase and return the token alongside the purchase result.
- `rectoken` is returned to `response_url` and `server_callback_url`.
- For details, load `references/saving-cards.md`.

## Reversals

Use reversals to refund or reverse an approved payment fully or partially.

- Create a reversal with `POST /api/reverse/order_id`.
- For a full reversal, send `amount` equal to the original order `actual_amount`.
- Multiple partial reversals are allowed while their sum is less than or equal to `actual_amount`.
- Use `reverse_id` as an idempotency key for safe retry of partial reversals.
- Check reversal status through `POST /api/status/order_id`; compare accumulated `reversal_amount` with `actual_amount`.
- For details, load `references/reversal.md`.

## Captures

Use capture to charge funds previously held by a card preauthorization.

- Create the original payment with `preauth=Y`.
- Capture with `POST /api/capture/order_id`.
- Card payments support preauth/capture; other payment methods use one-stage charge behavior.
- Multiple captures are not allowed. A single full or partial capture is available.
- Check capture status through `POST /api/status/order_id`; parse `additional_info.capture_status` and `additional_info.capture_amount`.
- For details, load `references/capture.md`.

## Subscriptions

Use subscriptions for fixed scheduled charges such as daily, weekly, monthly, or yearly billing.

- Create subscription checkout by adding `subscription=Y` and `recurring_data` to `/api/checkout/redirect`, `/api/checkout/token`, or `/api/checkout/url`.
- Do not use subscriptions with Payment (direct) integration or Open Banking.
- Supported methods are Visa/MasterCard/Amex cards, Apple Pay, and Google Pay.
- Start or stop an existing subscription with `POST /api/subscription` and `action=start` or `action=stop`.
- For details, load `references/subscriptions.md`.

## Additional Data

Use `reservation_data` when the merchant needs to attach extra payer, device, checkout-field, or product/fiscalisation metadata to a purchase request.

- `reservation_data` is BASE64-encoded JSON attached to create-purchase requests.
- Keep keys and values ASCII/Latin-alphanumeric plus separator symbols as documented.
- Use it for customer metadata, `fields_custom[]`, `products[]`, `settlement_id`, and risk/fiscalisation-related extras.
- Be careful with `3ds_mandatory`: the docs say it can be used only after approval from the Flitt risk team.
- For details, load `references/additional-data.md`.

## Currencies

Use the currency matrix before wiring or validating the Flitt `currency` field.

- Supported bank-card processing currencies depend on merchant country.
- Do not assume `USD` or `EUR` are available for every merchant geography.
- For details, load `references/currencies.md`.

## Callbacks

Use Flitt callbacks as the reliable asynchronous status source for payments and follow-up operations.

- Flitt sends JSON `POST` callbacks to `server_callback_url`.
- Treat the callback as successfully processed only when your endpoint returns HTTP `200 OK`.
- Flitt does not follow redirects, so callback endpoints must respond directly.
- Verify callback signatures before trusting payment state, and process callbacks idempotently by `order_id` and/or `payment_id`.
- For details, load `references/callbacks.md`.

## Signatures

Use the dedicated signature reference when implementing or debugging request, response, callback, or redirect signature handling.

- Flitt signs request and response data with SHA1 over `secret|sorted-nonempty-values`.
- Exclude `signature` and, for verification, `response_signature_string`.
- Keep SHA1 hex lowercase.
- Be especially careful with zero values, empty values, UTF-8 encoding, and endpoint-specific parameter sets such as `/api/recurring`.
- For details, load `references/signature.md`.

## Response Codes

Use the response-code reference when deciding whether a failure is caused by merchant input, issuer decline, or Flitt/platform configuration.

- API `response_code` values and embedded-checkout JavaScript codes have different ranges and meanings.
- Many codes are operationally actionable only after you classify ownership: merchant, issuer bank, or Flitt.
- For details, load `references/response-codes.md`.

## Troubleshooting

When Flitt returns `Invalid signature`:

1. Confirm the secret key belongs to the same merchant and environment.
2. Log the exact pre-hash signature string locally, redacting the secret in shared logs.
3. Ensure empty values are omitted completely, including their `|` separator.
4. Ensure numeric zero is preserved as `0`, not converted to empty or null.
5. Ensure `signature` and `response_signature_string` are excluded.
6. Ensure non-Latin text is sent and hashed as UTF-8.
7. Ensure the final SHA1 hex digest is lowercase.

When testing callbacks or redirects in test mode, Flitt may return `response_signature_string`; use it only as a diagnostic hint and never include it in verification.
