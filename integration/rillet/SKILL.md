---
name: rillet
description: |
  Rillet integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Rillet. Routes through Apideck with serviceId "rillet".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: rillet
  unifiedApis: ["accounting"]
  authType: apiKey
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Rillet (via Apideck)

Access Rillet through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Rillet plumbing.

> **Beta connector.** Rillet is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `rillet`
- **Unified API:** Accounting
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/rillet/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/rillet/gotchas)
- **Rillet docs:** https://rillet.com
- **Homepage:** https://rillet.com/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication + API Access Enabled per Organisation by Rillet
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer connects with their own Rillet organisation API key; there is no app to register.
- **Account type required:** A Rillet account. Any plan works; there is no edition gate on API access.
- **Consumer access level:** Admin access to Organization Settings, which is where API keys are created.
- **Sandbox:** available — A separate sandbox environment at sandbox.api.rillet.com with its own API keys, arranged through your Rillet team.
- **Costs:** No API-specific fee. Rillet itself is a paid platform and does not publish pricing.
- **Rate limits:** 60 requests per rolling one-minute window; requests above it return HTTP 429.
- **Authentication:** Presented as a Bearer token in the Authorization header; not OAuth. Keys are scoped to a single Rillet organisation.
- **Webhooks:** No webhooks

**Important to know:**

- API access is not self-service. Rillet has to enable it for each organisation before any API key can be created, so your consumer starts by contacting their Rillet team rather than by opening a settings page.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/rillet` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Rillet** — for example, "create an invoice in Rillet" or "reconcile payments in Rillet". This skill teaches the agent:

1. Which Apideck unified API covers Rillet (Accounting)
2. The correct `serviceId` to pass on every call (`rillet`)
3. Rillet-specific auth and coverage caveats

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

// List invoices in Rillet
const { data } = await apideck.accounting.invoices.list({
  serviceId: "rillet",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Rillet to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Rillet
await apideck.accounting.invoices.list({ serviceId: "rillet" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Rillet directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Rillet via Apideck Accounting

Rillet is a modern SaaS finance platform (general ledger + revenue recognition) targeting B2B SaaS companies. Deep coverage via Apideck.

### Entity mapping

| Rillet entity | Apideck Accounting resource |
|---|---|
| Invoice | `invoices` |
| Bill | `bills` |
| Bill Payment | `bill-payments` |
| Credit Note | `credit-notes` |
| Payment | `payments` |
| Journal Entry | `journal-entries` |
| Account | `ledger-accounts` |
| Customer | `customers` |
| Supplier | `suppliers` |
| Item | `invoice-items` |
| Tax Rate | `tax-rates` |
| Expense | `expenses` |
| Subsidiary | `subsidiaries` |
| Bank Account | `bank-accounts` |
| Bank Feed Statement | `bank-feed-statements` |
| Company Info | `company-info` |
| P&L, Balance Sheet | `profit-and-loss`, `balance-sheet` |

### Coverage highlights

- ✅ Full CRUD on invoices, bills, payments
- ✅ Credit notes
- ✅ Journal entries
- ✅ Expenses
- ✅ Multi-subsidiary
- ✅ Bank feeds for reconciliation
- ✅ Financial reports (P&L, Balance Sheet)
- ⚠️ Revenue recognition schedules (Rillet's signature feature) — not in unified; use Proxy
- ❌ SaaS metrics (ARR, MRR) — Rillet-specific; use Proxy

### Auth notes

- **Type:** API key, managed by Apideck Vault
- **Organization binding:** one Rillet organization per connection.
- **B2B SaaS focus:** Rillet's model assumes subscription revenue. Customers without subscription semantics may not use all features.

### Example: fetch P&L for YTD

```typescript
const { data } = await apideck.accounting.profitAndLoss.get({
  serviceId: "rillet",
  filter: { start_date: "2026-01-01", end_date: "2026-04-18" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Rillet directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Rillet's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: rillet" \
  -H "x-apideck-downstream-url: <target endpoint on Rillet>" \
  -H "x-apideck-downstream-method: GET"
```

See [Rillet's API docs](https://rillet.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Apideck connection guide for Rillet](https://developers.apideck.com/connectors/rillet/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Rillet official docs](https://rillet.com)
