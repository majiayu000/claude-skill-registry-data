---
name: paypal-best-practices
description: >-
  PayPal integration guidance, code examples, and best practices.
  Use for checkout, card fields, BNPL, Pay Later, Venmo, subscriptions,
  invoicing, disputes, payouts, webhooks, APMs, JS SDK v5, JS SDK v6,
  createInstance, payment sessions, web components, Fastlane, payment links,
  donations, 3D Secure, vaulting, iDEAL, bank redirects, agentic commerce,
  or any PayPal architecture decision or code generation question.
when_to_use: >-
  "how do I integrate PayPal", "PayPal checkout example", "PayPal best
  practices", "PayPal subscriptions guide", "PayPal webhook setup",
  "PayPal error handling", "PayPal SDK code", "add Pay Later", "add Venmo",
  "PayPal card fields", "PayPal disputes", "PayPal invoices",
  "PayPal docs link", or any PayPal code generation request.
allowed-tools: Read, WebFetch, WebSearch
metadata:
  version: "1.1.0"
  category: payments-integration
  tags: checkout bnpl venmo subscriptions disputes apm fastlane webhooks
---

# PayPal Best Practices

Before answering, read the relevant reference file from the table below. The reference files contain current documentation URLs, country availability, and verified code examples.

## Integration Routing

| Developer intent | Reference file |
|-----------------|----------------|
| Accept payments, add PayPal button, checkout flow, Orders API, payment link, payment links, pay link, React PayPal, @paypal/react-paypal-js, authorize vs capture, deferred capture, donate button, donations | [references/checkout.md](references/checkout.md) (v5) or [references/js-sdk-v6.md](references/js-sdk-v6.md) (v6) |
| Advanced Card Fields, Apple Pay, Google Pay, APMs, Expanded Checkout, bank redirect, iDEAL, Bancontact, BLIK, Przelewy24, Pay upon Invoice, Ratepay, domain association, regional payment methods | [references/expanded-checkout.md](references/expanded-checkout.md) (v5) or [references/js-sdk-v6.md](references/js-sdk-v6.md) (v6) |
| Add Venmo, Venmo button, Venmo eligibility, isFundingEligible, eligibility check, Venmo app | [references/venmo.md](references/venmo.md) (v5) or [references/js-sdk-v6.md](references/js-sdk-v6.md) (v6) |
| Pay Later, installments, BNPL messaging, Pay in 4, financing, BNPL banner, Pay Later banner, Pay Later eligibility | [references/bnpl.md](references/bnpl.md) (v5) or [references/js-sdk-v6.md](references/js-sdk-v6.md) (v6) |
| Recurring billing, subscriptions, plan management, free trial, trial period, upgrade plan, downgrade plan, plan revision | [references/subscriptions.md](references/subscriptions.md) (v5) or [references/js-sdk-v6.md](references/js-sdk-v6.md) (v6) |
| Disputes, chargebacks, refunds, evidence, provide evidence, dispute lifecycle, dispute stage, INQUIRY, CLAIM | [references/disputes-refunds.md](references/disputes-refunds.md) |
| Send money, batch payouts, seller payments, Venmo payout, 1099, tax reporting, prepaid cards | [references/payouts.md](references/payouts.md) |
| Invoices, billing, send invoice, invoice reminder, partial payment, line items | [references/invoicing.md](references/invoicing.md) |
| OAuth, access tokens, credentials, idempotency, token caching, token refresh, idempotency key, PayPal-Request-Id | [references/authentication.md](references/authentication.md) |
| Webhook verification, event handling, signature check, webhook simulator, test webhooks, event types, PAYMENT.CAPTURE | [references/webhooks.md](references/webhooks.md) |
| Fastlane, accelerated guest checkout, auto-fill, prefill, single-use token, Braintree Fastlane, `braintree-web`, `BraintreeGateway`, `gateway.clientToken.generate`, `braintree.fastlane.create`, paymentMethodNonce | **Pick exactly one — three variants, do not mix.** Braintree gateway (`braintree-web`, `BraintreeGateway`, `paymentMethodNonce`): [references/fastlane-braintree.md](references/fastlane-braintree.md). PayPal-direct v5 (`paypal.Fastlane({})`, `data-sdk-client-token`): [references/fastlane.md](references/fastlane.md). PayPal-direct v6 (`sdkInstance.createFastlane()`): [references/js-sdk-v6.md](references/js-sdk-v6.md). If unclear which variant, ask before generating code. |
| 3D Secure, liability shift, SCA, PSD2, Strong Customer Authentication, enrollment status, authentication status | [references/3d-secure.md](references/3d-secure.md) |
| AI shopping agents, Store Sync, Agent Ready, agentic commerce, ChatGPT, product discovery, delegated payment token | [references/agentic-commerce.md](references/agentic-commerce.md) |
| MCP server tools, tool inventory, product catalog, merchant insights, reporting | [references/mcp-tools.md](references/mcp-tools.md) |
| JS SDK v6, v6 Web SDK, createInstance, payment sessions, web components, migrate from v5, card fields, vault, save card, save payment method, vaulting, CSP, Content Security Policy | [references/js-sdk-v6.md](references/js-sdk-v6.md) |

## Code Generation Directive

Before writing any PayPal code, detect SDK version and read the correct reference:

1. **v5** — `sdk/js?client-id=` script tag, `paypal.Buttons()`, Hosted Fields → use `checkout.md` / `expanded-checkout.md`
2. **v6** — `web-sdk/v6/core` script tag, `createInstance`, `<paypal-button>` web components → use `js-sdk-v6.md`
3. **New project** (no existing SDK) — default to v6, use `js-sdk-v6.md`
4. **Unclear** — ask the user which version they are using

## MCP Boundary

When the PayPal MCP server is connected, prefer MCP tools for live operations (creating orders, managing subscriptions, fetching disputes). Use this skill for architecture decisions, code generation, and integration guidance — not for executing API calls that MCP tools can handle directly.

## Out of Scope

This skill does NOT cover:
- PayPal Commerce Platform (multi-party marketplaces) — see [Commerce Platform docs](https://developer.paypal.com/platforms/overview.md)
- PayPal Mobile SDKs (iOS/Android native) — see [Mobile SDK docs](https://developer.paypal.com/developer-resources.md#sdks)
- Braintree direct integration (non-Agentic) — see [Braintree docs](https://developer.paypal.com/braintree/docs)
- Zettle POS / PayPal Here — see [Zettle developer docs](https://developer.zettle.com)
- Tax calculation or compliance
- PayPal Marketing Solutions

## Post-Generation Environment Check

After generating PayPal integration code, proactively scan the project to verify the environment is correctly configured for the code you just wrote.

- Identify what credentials the generated code needs (e.g. `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, client token endpoint)
- Look for env files (`.env`, `.env.sample`, `.env.example`, `.env.local`) in the project root and `server/`/`client/` subdirectories
- If `.env.sample` or `.env.example` exists but no `.env` — flag it
- If `.env` exists — check the required keys are present and non-empty
- For frontend projects, read the source files to determine how `clientId` reaches the client before checking — do not assume a pattern
- Flag missing or incomplete env setup inline after the code; confirm briefly if everything looks good
- If the env setup cannot be determined, ask: "How is `PAYPAL_CLIENT_ID` configured in this project?" before flagging anything as missing

## Pre-Delivery Validation Checklist

Before presenting generated PayPal integration code, verify:
1. Credentials are not hardcoded (use env vars)
2. `PayPal-Request-Id` included on all POST requests
3. Sandbox URLs used (not production) in examples
4. Webhook signature verification is present
5. `intent` matches the use case (CAPTURE vs AUTHORIZE)
6. BNPL messaging only rendered for eligible countries/currencies
7. Venmo eligibility check before rendering Venmo button
8. Server-side order creation (not client-side `actions.order.create()`)
9. Error handling for INSTRUMENT_DECLINED (422)
10. Retry logic with exponential backoff for 429
11. `debug_id` logged from error responses
12. No deprecated or legacy APIs recommended — never use NVP/SOAP, v1/payments, Hosted Fields, or Adaptive Payments
13. Token caching implemented; Apple Pay domain verification mentioned if Apple Pay is used