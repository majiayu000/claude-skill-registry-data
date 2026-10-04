---
name: pennylane
description: |
  Pennylane integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Pennylane. Routes through Apideck with serviceId "pennylane".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: pennylane
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: true
  sandboxAvailable: true
---

# Pennylane (via Apideck)

Access Pennylane through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Pennylane plumbing.

> **Beta connector.** Pennylane is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `pennylane`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/pennylane/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/pennylane/gotchas)
- **Pennylane docs:** https://pennylane.readme.io
- **Homepage:** https://www.pennylane.com/

## At a glance

- **Implementation difficulty:** moderate — Partner-Issued Credentials Required — OAuth apps are provisioned manually by Pennylane's Partnerships team (no self-service portal); otherwise a standard OAuth authorization-code connect.
- **Vendor partnership required:** yes ([developer portal](https://www.pennylane.com/fr/contact-demande-de-partenariat/)) — OAuth Client ID and Secret are issued by Pennylane's Partnerships team after manual validation. No fee.
- **Apideck-managed credentials:** not available — Consumers supply their own partnership-issued OAuth credentials in every environment.
- **Account type required:** Active Pennylane account (app.pennylane.com) with at least one company set up.
- **Consumer access level:** A user with permission to authorize third-party (OAuth) apps for the company.
- **Sandbox:** available — Existing accounts self-serve a developer API token for testing. OAuth partner-app credentials still require the Partnerships team. Same limits as production.
- **Costs:** No partnership or API fees; consumers need a Pennylane subscription that includes API access.
- **Rate limits:** 25 requests per 5 seconds per token (production and sandbox).
- **Authentication:** Authorization Code flow.
- **Webhooks:** Virtual webhooks — created and updated events for customers, suppliers, invoices, invoice items and bills.

**Important to know:**

- There is no stated turnaround for OAuth credential issuance, so provisioning can gate your go-live — budget an unpredictable lead time rather than assuming instant self-service access.
- Pennylane is available in France and Germany, so confirm your consumers are in one of those markets before committing.
- Access tokens last 24 hours and refresh tokens are valid for 90 days, rotating on every refresh; both are refreshed automatically by Apideck, but a connection left dormant beyond 90 days must be re-authorized by the consumer.
- The partner onboarding journey is French-first — the partnership request form and parts of Pennylane's documentation are in French.
- API access requires the consumer's own Pennylane subscription to be on the Essentiel plan (24 EUR/month) or above for independents — confirm this before assuming a lower-tier account can connect; pricing for other business sizes may differ.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/pennylane` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Pennylane** — for example, "create an invoice in Pennylane" or "reconcile payments in Pennylane". This skill teaches the agent:

1. Which Apideck unified API covers Pennylane (Accounting)
2. The correct `serviceId` to pass on every call (`pennylane`)
3. Pennylane-specific auth and coverage caveats

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

// List invoices in Pennylane
const { data } = await apideck.accounting.invoices.list({
  serviceId: "pennylane",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Pennylane to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Pennylane
await apideck.accounting.invoices.list({ serviceId: "pennylane" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Pennylane directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Pennylane via Apideck Accounting

Pennylane is a French/European cloud accounting and finance platform blending bookkeeping with modern UX. Fast-growing in France; expanding across the EU.

### Entity mapping

| Pennylane entity | Apideck Accounting resource |
|---|---|
| Customer Invoice | `invoices` |
| Supplier Invoice | `bills` |
| Journal Entry | `journal-entries` |
| Ledger (Compte) | `ledger-accounts` |
| Customer | `customers` |
| Supplier | `suppliers` |
| Product / Service | `invoice-items` |
| VAT rate | `tax-rates` |
| Purchase Order | `purchase-orders` |
| Quote | `quotes` |
| Bank Account | `bank-accounts` |
| Analytic dimension | `tracking-categories` |
| Attachments | `attachments` |
| Bank Feed Statements | `bank-feed-statements` |

### Coverage highlights

- ✅ CRUD on invoices, bills, customers, suppliers
- ✅ Purchase orders and quotes (France-typical sales workflow)
- ✅ Analytic dimensions (cost centre / project tracking)
- ✅ Bank feed statements for reconciliation
- ✅ Attachments on invoices / bills (Pennylane's document-centric model)
- ⚠️ French-specific VAT declaration (CA3) — not exposed; use Proxy
- ❌ Payroll features — separate Pennylane surface
- ❌ Bill automation rules — use Proxy

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Company binding:** one Pennylane company per connection.
- **French market focus:** defaults to French-specific tax codes and reporting; users outside France may see reduced functionality.

### Example: create a purchase order

```typescript
const { data } = await apideck.accounting.purchaseOrders.create({
  serviceId: "pennylane",
  purchaseOrder: {
    supplier_id: "supplier_abc",
    line_items: [{ description: "Widgets", quantity: 10, unit_price: 25.5 }],
    currency: "EUR",
  },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Pennylane directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Pennylane's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: pennylane" \
  -H "x-apideck-downstream-url: <target endpoint on Pennylane>" \
  -H "x-apideck-downstream-method: GET"
```

See [Pennylane's API docs](https://pennylane.readme.io) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Apideck connection guide for Pennylane](https://developers.apideck.com/connectors/pennylane/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Pennylane official docs](https://pennylane.readme.io)
