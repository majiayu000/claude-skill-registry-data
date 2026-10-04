---
name: acumatica
description: |
  Acumatica integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Acumatica. Routes through Apideck with serviceId "acumatica".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: acumatica
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  status: beta
  difficulty: highly_complex
  partnershipRequired: false
  sandboxAvailable: true
---

# Acumatica (via Apideck)

Access Acumatica through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, banqUP, Campfire and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Acumatica plumbing.

> **Beta connector.** Acumatica is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `acumatica`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/acumatica/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/acumatica/gotchas)
- **Acumatica docs:** https://help.acumatica.com
- **Homepage:** https://www.acumatica.com/

## At a glance

- **Implementation difficulty:** highly complex — Every consumer must manually register their own Connected Application (Authorization Code flow, shared secret, redirect URI) inside their Acumatica instance before connecting.
- **Vendor partnership required:** no ([Acumatica Developer Network (ADN)](https://www.acumatica.com/partners/)) — The Acumatica Developer Network (ADN) is not required to build; free Level 1 covers a trial instance and training.
- **Apideck-managed credentials:** not available — Every Acumatica instance registers its own Connected Application; each consumer provides their own Client ID, Secret and instance URL.
- **Account type required:** An Acumatica instance (cloud or self-hosted) with the Web Services API enabled.
- **Consumer access level:** Administrator role, or a custom role granted API/Web Services permissions.
- **Sandbox:** available ([signup](https://builds.acumatica.com/)) — Free local developer instance (Windows required, 2-user demo mode); a cloud trial is also available via ADN.
- **Costs:** Free to build — the local developer instance and ADN Level 1 membership are both free.
- **Rate limits:** Set by the consumer's instance license tier: ~100 req/min, 3 concurrent (standard) or ~150 req/min, 6 concurrent (L-series).
- **Authentication:** Authorization Code flow.
- **Webhooks:** No webhooks — neither native nor virtual.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/acumatica` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Acumatica** — for example, "create an invoice in Acumatica" or "reconcile payments in Acumatica". This skill teaches the agent:

1. Which Apideck unified API covers Acumatica (Accounting)
2. The correct `serviceId` to pass on every call (`acumatica`)
3. Acumatica-specific auth and coverage caveats

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

// List invoices in Acumatica
const { data } = await apideck.accounting.invoices.list({
  serviceId: "acumatica",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Acumatica to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Acumatica
await apideck.accounting.invoices.list({ serviceId: "acumatica" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "banqup" });
```

This is the compounding advantage of using Apideck over integrating Acumatica directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Acumatica via Apideck Accounting

Acumatica is a cloud ERP platform for mid-market businesses, with strong distribution, manufacturing, and services verticals. Apideck coverage targets the core financial management surface.

### Entity mapping

| Acumatica entity | Apideck Accounting resource |
|---|---|
| AR Invoice | `invoices` |
| AP Bill | `bills` |
| Payment | `payments` |
| Credit Memo | `credit-notes` |
| GL Transaction | `journal-entries` |
| Account | `ledger-accounts` |
| Customer | `customers` |
| Vendor | `suppliers` |
| Inventory Item | `invoice-items` |
| Tax | `tax-rates` |
| Purchase Order | `purchase-orders` |

### Coverage highlights

- ✅ Full CRUD on invoices, bills, payments, customers, suppliers
- ✅ Journal entries
- ✅ Purchase orders
- ✅ Credit notes
- ⚠️ Acumatica Generic Inquiries — powerful custom reports; not exposed, use Proxy
- ❌ Manufacturing and distribution modules — use Proxy for BOM, work orders, shipments
- ❌ Payroll

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Tenant + branch binding:** Acumatica supports multi-tenant + multi-branch. The connection is bound to one tenant; branch selection is typically passed per call.
- **Screen-based APIs:** Acumatica has both OData-style REST and "Screen-Based" Contract API. Apideck abstracts this; Proxy calls can hit either.

### Example: create an AR invoice

```typescript
const { data } = await apideck.accounting.invoices.create({
  serviceId: "acumatica",
  invoice: {
    customer_id: "cust_abc",
    invoice_date: "2026-04-18",
    line_items: [
      { description: "Consulting", quantity: 10, unit_price: 150 },
    ],
    currency: "USD",
  },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Acumatica directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Acumatica's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: acumatica" \
  -H "x-apideck-downstream-url: <target endpoint on Acumatica>" \
  -H "x-apideck-downstream-method: GET"
```

See [Acumatica's API docs](https://help.acumatica.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), [`exact-online-nl`](../exact-online-nl/) *(beta)*, and 25 more.

## See also

- [Apideck connection guide for Acumatica](https://developers.apideck.com/connectors/acumatica/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Acumatica official docs](https://help.acumatica.com)
