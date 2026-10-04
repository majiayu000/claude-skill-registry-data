---
name: moneybird
description: |
  Moneybird integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Moneybird. Routes through Apideck with serviceId "moneybird".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: moneybird
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  status: beta
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: true
---

# Moneybird (via Apideck)

Access Moneybird through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Moneybird plumbing.

> **Beta connector.** Moneybird is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `moneybird`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/moneybird/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/moneybird/gotchas)
- **Moneybird docs:** https://developer.moneybird.com
- **Homepage:** https://www.moneybird.com/

## At a glance

- **Implementation difficulty:** straightforward — Self-Service OAuth App + Free Sandbox — No Partnership or App Review
- **Vendor partnership required:** no ([developer portal](https://developer.moneybird.com/)) — No partner programme; register an OAuth application yourself from the developer portal, free and without approval, for an immediate Client ID and Secret.
- **Apideck-managed credentials:** available — For testing: Apideck's shared app shows "Apideck" on the consent screen. Register your own Moneybird application for production.
- **Account type required:** An active Moneybird administration on any paid tier; API access is not documented as gated to a specific plan.
- **Consumer access level:** The owner of the administration — Moneybird requires this during authorization; a regular user cannot connect.
- **Sandbox:** available ([signup](https://moneybird.com/administrations/sandboxes/new)) — Free sandbox administrations with full feature access, creatable from any Moneybird account; invoices carry watermarks.
- **Costs:** No API-specific cost — included in the consumer's Moneybird subscription. App registration and sandbox administrations are free.
- **Rate limits:** 150 requests per 5 minutes per IP address; 50 per 5 minutes for reports endpoints. 429 responses carry a Retry-After header.
- **Authentication:** Authorization Code flow.
- **Webhooks:** No webhooks

**Important to know:**

- Rate limits are counted per IP address, not per application or per administration — every consumer you connect shares your integration's outbound IPs, so heavy use by one can throttle the rest.
- Plan for the account owner to be personally involved in every connection. Where bookkeeping is delegated to an accountant or a colleague, that person cannot complete the authorisation on the owner's behalf.
- Each connection covers one administration. A consumer running several companies in Moneybird needs one connection per administration, selected during setup.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/moneybird` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Moneybird** — for example, "create an invoice in Moneybird" or "reconcile payments in Moneybird". This skill teaches the agent:

1. Which Apideck unified API covers Moneybird (Accounting)
2. The correct `serviceId` to pass on every call (`moneybird`)
3. Moneybird-specific auth and coverage caveats

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

// List invoices in Moneybird
const { data } = await apideck.accounting.invoices.list({
  serviceId: "moneybird",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Moneybird to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Moneybird
await apideck.accounting.invoices.list({ serviceId: "moneybird" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Moneybird directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Moneybird via Apideck Accounting

Moneybird is a popular Dutch SMB accounting platform favored by freelancers and small businesses. Strong coverage of the core invoicing + expense workflow, plus banking integration.

### Entity mapping

| Moneybird entity | Apideck Accounting resource |
|---|---|
| SalesInvoice | `invoices` |
| PurchaseInvoice / Receipt | `bills` |
| Payment | `payments` |
| Bill Payment | `bill-payments` |
| Journal (BookingEntry) | `journal-entries` |
| Ledger Account | `ledger-accounts` |
| Contact (customer) | `customers` |
| Contact (supplier) | `suppliers` |
| Product | `invoice-items` |
| Tax Rate | `tax-rates` |
| Bank Account | `bank-accounts` |
| Administration | `subsidiaries` |
| Expense | `expenses` |
| Tracking Category | `tracking-categories` |

### Coverage highlights

- ✅ CRUD on invoices, bills, payments, customers, suppliers
- ✅ Expense management (Moneybird's first-class "expense" workflow)
- ✅ Journal entries and tax rates (Dutch BTW)
- ✅ Multi-administration (Moneybird's term for tenants/subsidiaries)
- ✅ Bank accounts for reconciliation
- ⚠️ OCR receipt processing — Moneybird-specific; not in unified API
- ❌ Quote/proposal flows — use Proxy
- ❌ Time tracking — use Proxy

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Administration selection:** Moneybird accounts can contain multiple administrations. The connection is bound to one — for multi-admin access, create separate connections with different consumer IDs, or pass administration ID through pass-through.
- **Dutch-only UI:** Moneybird itself is Dutch-market. Users outside NL rarely have accounts here.

### Example: list overdue invoices

```typescript
const { data } = await apideck.accounting.invoices.list({
  serviceId: "moneybird",
  filter: { status: "overdue" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Moneybird directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Moneybird's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: moneybird" \
  -H "x-apideck-downstream-url: <target endpoint on Moneybird>" \
  -H "x-apideck-downstream-method: GET"
```

See [Moneybird's API docs](https://developer.moneybird.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Apideck connection guide for Moneybird](https://developers.apideck.com/connectors/moneybird/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Moneybird official docs](https://developer.moneybird.com)
