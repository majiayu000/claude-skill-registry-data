---
name: "storefront-payment-check"
description: "Review or build a storefront's Paystack payment flow and check price, kobo, webhook signature, amount match and once-only fulfilment before going live."
---

# Storefront payment check (Paystack)

Use this when the user is building, reviewing or debugging a Paystack checkout for a storefront (for example Better Style), or asks whether their payment flow is safe to go live. It checks the flow against Paystack's documented rules and reports what was verified, what was tested, and what was not checked.

## Ground rules
- Never ask for, print or store secret keys. Keys live in environment variables or the host's secret settings. If a key appears in code, chat or a file, flag it and recommend rotating it.
- Use test mode only unless the user says they are going live and has confirmed the checklist below.
- Do not call live payment endpoints. Test with fake data and a fake HTTP client.
- Before quoting any Paystack behaviour that may have changed (fees, test cards, webhook IPs, retry timing), re-read Paystack's current docs (payments/accept-payments, payments/webhooks, payments/test-payments) and state the date read. Do not copy test card numbers from memory.

## The flow to check
Initialize on the server -> customer pays (redirect or popup) -> Paystack sends a signed webhook -> server verifies and fulfils once -> thank-you page shows the real status.

## Checklist (report each as PASS / FAIL / NOT CHECKED, with file and line as evidence)
1. **Price comes from the server's catalogue.** The browser sends SKUs and quantities only. Reject unknown SKUs, non-integer or out-of-range quantities, and empty carts.
2. **Amount is in the lowest denomination.** For naira, kobo: multiply by 100 and round to an integer. Currency is set explicitly.
3. **Initialization is server-side.** `POST /transaction/initialize` with `Authorization: Bearer <secret key>` read from an environment variable. Required fields: `email` and `amount`. The secret key never reaches front-end code.
4. **Order id equals the Paystack `reference`.** One unique reference per order. The cart may also be stored in `metadata` as a backup.
5. **Callback is not proof.** Reaching `callback_url` only shows a status page. The thank-you page calls the verify endpoint server-side.
6. **Webhook signature.** Compute HMAC SHA512 of the raw request body (bytes, not re-serialised JSON) with the secret key; compare to the `x-paystack-signature` header in constant time. Reject mismatches with 401 and do nothing else.
7. **Optional second check.** Compare the sender IP with Paystack's published webhook IPs (read them from current docs). Treat as defence in depth, not a replacement for the signature.
8. **Only act on the right event.** Handle `charge.success`; acknowledge other events with 200 and no action.
9. **Amount, currency and status match.** Fulfil only if `data.status` is success, `data.amount` equals the expected kobo stored when the order was created, and the currency matches. On mismatch, do not fulfil and alert the owner.
10. **Once-only fulfilment.** Webhooks are retried (live: every 3 minutes for the first 4 attempts, then hourly for 72 hours, per Paystack docs read 2026-10-18; re-check). Fulfilment must be idempotent: a second delivery of the same event changes nothing.
11. **Respond fast.** Return 200 promptly; move slow work (email, stock updates, notifications) to a background step.
12. **Public webhook URL.** localhost cannot receive events. Registered in the Paystack dashboard for the right environment (test vs live URL).
13. **Persistent order store.** Orders live in a database, not in memory, and survive restarts. Opt-in and payment events are timestamped.
14. **Logging without secrets.** Logs include references and statuses, never keys or full card or personal data.
15. **Secrets hygiene.** Run secret scanning on the repository before pushing. Test and live keys are separate and only live keys are set in production settings.
16. **Failure paths.** Declined, abandoned and failed payments leave the order unpaid and show a clear message. Refund and dispute events have an owner and a process.

## How to test (no network)
Build or reuse a small pure-Python core with these functions and unit-test them: `build_initialize_body(cart, email, callback_url)`, `signature_ok(raw_body, header, secret)`, `handle_webhook(raw_body, header, secret, orders)`. Cover at least: correct kobo total; bad carts rejected; valid signature accepted; wrong key, altered body and missing header rejected; first delivery fulfils; second delivery reports already fulfilled; wrong amount not fulfilled; other events ignored; unknown reference ignored. Run the tests and report the real output.

## Test-mode run (only with the user's own test keys)
Walk through one successful payment and one declined payment using the cards on Paystack's current test-payments page. Confirm the order status changes only after the signed webhook, and that replaying the same webhook does not fulfil twice.

## Output format
1. One-line verdict: safe to go live / not yet, and why.
2. Table of the 16 checks with PASS / FAIL / NOT CHECKED and evidence.
3. Origin labels for claims: verified here (read in docs today, with date), tested here (test run output), source claim, our inference, unchecked.
4. Top three fixes in order, each with the smallest change.
5. A reminder that human review is the final layer before any live-money release.

## Go-live gate
Do not recommend going live until: checks 1-6 and 8-10 pass, the test-mode run is done, secret scanning is clean, Paystack business verification is complete, and the user has confirmed live keys are set only in production settings.