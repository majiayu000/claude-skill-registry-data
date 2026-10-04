---
name: myob
description: |
  MYOB integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in MYOB. Routes through Apideck with serviceId "myob".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: myob
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# MYOB (via Apideck)

Access MYOB through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant MYOB plumbing.

## Quick facts

- **Apideck serviceId:** `myob`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/myob/gotchas)
- **MYOB docs:** https://developer.myob.com
- **Homepage:** https://myob.com

## At a glance

- **Implementation difficulty:** moderate — Requires registering for MYOB API access before credentials can be generated — no partnership or paid program required.
- **Vendor partnership required:** no ([MYOB Developer Program](https://apisupport.myob.com/hc/en-us/requests/new?ticket_form_id=13228298199055)) — No partner program gates API access; the optional Developer Program adds software entitlements and an App Marketplace listing.
- **Apideck-managed credentials:** available — For testing: the OAuth consent screen shows "Apideck".
- **Account type required:** Active MYOB Business subscription (formerly Essentials); AccountRight is also supported.
- **Consumer access level:** Account holder, or any user with access to the company file.
- **Sandbox:** available ([signup](https://developer.myob.com/developer-program-details/)) — Shared sandbox company file, included with Developer Program membership.
- **Costs:** API access is free. The optional Developer Program costs AUD $110, $220, or $630 per month incl. GST (2026 pricing).
- **Rate limits:** Not published — MYOB shows the current per-API-key limits on the app registration page after you register.
- **Authentication:** Authorization Code flow.
- **Webhooks:** No webhooks — MYOB Business exposes no native webhook API and virtual webhooks are not enabled for this connector; sync by polling.

**Important to know:**

- One connection covers one company file — consumers running several MYOB company files need a separate connection for each.
- MYOB Business fits Australian and New Zealand entities — each MYOB company file is AU/NZ-based.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/myob` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **MYOB** — for example, "create an invoice in MYOB" or "reconcile payments in MYOB". This skill teaches the agent:

1. Which Apideck unified API covers MYOB (Accounting)
2. The correct `serviceId` to pass on every call (`myob`)
3. MYOB-specific auth and coverage caveats

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

// List invoices in MYOB
const { data } = await apideck.accounting.invoices.list({
  serviceId: "myob",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from MYOB to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — MYOB
await apideck.accounting.invoices.list({ serviceId: "myob" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating MYOB directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## MYOB via Apideck Accounting

MYOB is a major Australian/New Zealand accounting platform for SMB and mid-market. Apideck coverage focuses on invoicing and sales, with limited AP coverage currently.

### Entity mapping

| MYOB entity | Apideck Accounting resource |
|---|---|
| Sale Invoice | `invoices` |
| Item Invoice | `invoices` |
| Customer | `customers` |
| Item | `invoice-items` |
| Account | `ledger-accounts` |
| TaxCode | `tax-rates` |
| Payment | `payments` |
| Company File | `company-info` |

### Coverage highlights

- ✅ Invoices (CRUD)
- ✅ Customers
- ✅ Items / products
- ✅ Chart of accounts
- ✅ Tax codes (GST handling for AU/NZ)
- ✅ Customer payments
- ⚠️ Bills / supplier invoices — not in current Apideck mapping; use Proxy
- ⚠️ Journal entries — use Proxy
- ❌ Payroll — MYOB Payroll is a separate product surface
- ❌ Inventory management — use Proxy

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Company file binding:** MYOB uses "company files" as the multi-tenant boundary. Each connection is bound to one company file. Multi-file access = multi-connection.
- **Cloud vs desktop:** Apideck targets MYOB AccountRight Live (cloud) and MYOB Business. Desktop-only company files aren't accessible.
- **API rate limit:** MYOB applies per-file rate limits; Apideck handles 429s with backoff.

### Example: create an invoice for an AU customer

```typescript
const { data } = await apideck.accounting.invoices.create({
  serviceId: "myob",
  invoice: {
    customer_id: "cust_abc",
    invoice_date: "2026-04-18",
    line_items: [
      { description: "Consulting", quantity: 10, unit_price: 220, tax_rate: { id: "GST" } },
    ],
    currency: "AUD",
  },
});
```

### Example: reach bills via Proxy

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: myob" \
  -H "x-apideck-downstream-url: /{company-file-id}/Purchase/Bill" \
  -H "x-apideck-downstream-method: GET"
```

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [MYOB official docs](https://developer.myob.com)
