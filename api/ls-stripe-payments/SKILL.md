---
name: ls-stripe-payments
description: Guide Stripe payments integration. Use for Checkout, PaymentIntents,
  subscriptions, webhooks, Connect, billing, and payment security review.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/stripe/ai
    source_path: skills/stripe-best-practices/SKILL.md
    source_commit: b8d7e28d0cc5690fb0c0be54c84cbfdd7df6e4cd
    source_ref: main
    source_sha256: 4a5a79e2fc54dab3c0de5e6c58b87c70f2d40b0fb08b07732b1bf19713a59fab
    license: MIT
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Stripe Payments

Use this skill when working on Stripe payments tasks.

## Workflow

- Choose the Stripe integration surface before coding: Checkout, Payment Element, Billing, Connect, or direct API.
- Keep secret keys server-side, verify webhook signatures, handle idempotency, and test with Stripe test mode.
- Validate tax, currency, refunds, disputes, subscription lifecycle, and customer data handling for the business model.
- Prefer Checkout for hosted payment flows with minimal PCI and UI ownership; prefer Payment Element with PaymentIntents when the app must own the payment UI.
- Use Billing for subscriptions, invoices, trials, and recurring lifecycle logic; use Connect for marketplaces or platform money movement; use Treasury only for eligible financial-account workflows.
- Avoid hard-coding volatile API-version claims. Confirm the account API version, SDK behavior, changelog notes, and current endpoint docs before changing integration shape.
- Keep webhook handlers idempotent, signature-verified, and event-type explicit; avoid trusting client-return URLs as payment confirmation.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.
- Primary Stripe docs for current routing decisions:
  - https://docs.stripe.com/payments/checkout
  - https://docs.stripe.com/payments/payment-element
  - https://docs.stripe.com/connect
  - https://docs.stripe.com/billing
  - https://docs.stripe.com/treasury
  - https://docs.stripe.com/api/versioning

## Provenance

- Source: `https://github.com/stripe/ai`
- Ref: `main` at `b8d7e28d0cc5690fb0c0be54c84cbfdd7df6e4cd`
- Source path: `skills/stripe-best-practices/SKILL.md`
- License classification: `MIT`
- Source SHA-256: `4a5a79e2fc54dab3c0de5e6c58b87c70f2d40b0fb08b07732b1bf19713a59fab`
