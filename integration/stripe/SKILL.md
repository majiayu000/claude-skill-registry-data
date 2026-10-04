---
name: stripe
description: |
  Stripe integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Stripe. Routes through Apideck with serviceId "stripe".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: stripe
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Stripe (via Apideck)

Access Stripe through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Stripe plumbing.

## Quick facts

- **Apideck serviceId:** `stripe`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/stripe/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/stripe/gotchas)
- **Stripe docs:** https://stripe.com/docs/api
- **Homepage:** https://stripe.com/

## At a glance

- **Implementation difficulty:** moderate — Self-Service OAuth + Stripe App Marketplace Review Required to Scale
- **Vendor partnership required:** no — None: no partner programme, contract or fee.
- **Apideck-managed credentials:** not available — Apideck holds no shared Stripe App, so you supply your own app's credentials.
- **Account type required:** Any activated Stripe account
- **Consumer access level:** Administrator on the Stripe account (required to install a Stripe App)
- **Sandbox:** available ([signup](https://docs.stripe.com/sandboxes)) — Free and built in: every Stripe account includes test mode plus up to 5 isolated sandboxes.
- **Costs:** Free: Stripe charges no API, setup or monthly fees. Its per-transaction payment processing fees do not apply to API access.
- **Rate limits:** 100 requests/second per connected Stripe account in live mode; 25/second in test mode and sandboxes, and on most individual endpoints.
- **Authentication:** Authorization Code flow through a Stripe App that you build and own.
- **Webhooks:** Native — customer, invoice, credit note, invoice item, payment, expense, refund, tax rate and company info events (21 Stripe events mapped).

**Important to know:**

- Consumers connect through your Stripe App's External test install link, the route this connector uses today. Stripe caps external testing at 25 tester accounts per app, badges the app as a test version, and requires you to tell users it has not been reviewed by Stripe.
- Stripe's route past external testing is publishing the app on the Stripe App Marketplace: Stripe reviews it and replies within 4 business days, the account must be activated, one public app is allowed per Stripe account, and the name cannot contain Stripe, app, free or paid.
- Creating that app is a small build rather than a portal form: you create and upload it with the Stripe CLI and configure it through a JSON manifest, so this step needs a developer.
- Stripe is a payments and billing platform rather than a general ledger, so what the connector exposes is Stripe's billing data mapped onto accounting resources: expect invoicing and payments coverage rather than bookkeeping.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/stripe` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Stripe** — for example, "create an invoice in Stripe" or "reconcile payments in Stripe". This skill teaches the agent:

1. Which Apideck unified API covers Stripe (Accounting)
2. The correct `serviceId` to pass on every call (`stripe`)
3. Stripe-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **Accounting:** [https://specs.apideck.com/accounting.yml](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List invoices in Stripe
const { data } = await apideck.accounting.invoices.list({
  serviceId: "stripe",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Stripe to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Stripe
await apideck.accounting.invoices.list({ serviceId: "stripe" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Stripe directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Stripe via Apideck Accounting

Stripe is the dominant online payments platform. Apideck surfaces Stripe's accounting-adjacent resources (customers, invoices, payments, refunds) through the unified Accounting API — not the full Stripe surface.

> **Scope:** use this connector when you want to read Stripe data as part of an accounting workflow (invoices, payments, tax). For subscription management, Stripe Elements, Connect, or Terminal, go direct to Stripe's API or use the Proxy.

### Entity mapping

| Stripe entity | Apideck Accounting resource |
|---|---|
| Invoice | `invoices` |
| Customer | `customers` |
| PaymentIntent / Charge | `payments` |
| Refund | `refunds` |
| Credit Note | `credit-notes` |
| Tax Rate | `tax-rates` |
| Invoice Item | `invoice-items` |
| Account | `company-info` |
| Bank Account | `bank-accounts` |
| Expense | `expenses` |

### Coverage highlights

- ✅ Invoices and invoice items
- ✅ Customers
- ✅ Payments / charges
- ✅ Refunds (critical for reconciliation workflows)
- ✅ Tax rates
- ⚠️ Bills / supplier AP concepts — not meaningful in Stripe (no AP); treat as empty
- ❌ Subscriptions, plans, pricing — use Proxy or the Stripe SDK directly
- ❌ Connect (multi-party) flows — complex; use Proxy
- ❌ Webhooks — use Stripe's webhook endpoints directly, not the Apideck unified webhook

### Auth notes

- **Type:** OAuth 2.0 (Stripe Connect flow) — managed by Apideck Vault
- **Account binding:** one Stripe account per connection. Connect-based marketplaces need per-seller connections.
- **Test vs live mode:** Stripe distinguishes test and live keys. Ensure the user authorizes the intended mode during Vault OAuth.
- **Alternative for accounting reconciliation:** many teams already use Stripe's own data sync to QuickBooks/Xero. Apideck via Stripe is best when you need unified data across multiple providers (e.g., Stripe + QuickBooks).

### Example: list customers with payment totals

```typescript
const { data } = await apideck.accounting.customers.list({
  serviceId: "stripe",
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Stripe directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Stripe's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: stripe" \
  -H "x-apideck-downstream-url: <target endpoint on Stripe>" \
  -H "x-apideck-downstream-method: GET"
```

See [Stripe's API docs](https://stripe.com/docs/api) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Apideck connection guide for Stripe](https://developers.apideck.com/connectors/stripe/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Stripe official docs](https://stripe.com/docs/api)
