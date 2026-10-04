---
name: freeagent
description: |
  FreeAgent integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in FreeAgent. Routes through Apideck with serviceId "freeagent".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: freeagent
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  status: beta
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: true
---

# FreeAgent (via Apideck)

Access FreeAgent through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant FreeAgent plumbing.

> **Beta connector.** FreeAgent is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `freeagent`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/freeagent/gotchas)
- **FreeAgent docs:** https://dev.freeagent.com
- **Homepage:** https://www.freeagent.com/

## At a glance

- **Implementation difficulty:** straightforward — Self-Service OAuth App + Free Sandbox — No Partnership or App Review
- **Vendor partnership required:** no — Free self-service app registration at the FreeAgent Developer Dashboard: https://dev.freeagent.com/signup
- **Apideck-managed credentials:** available — For testing (Apideck sandbox app; OAuth shows "Apideck"); production requires your own FreeAgent app.
- **Account type required:** Any active FreeAgent subscription
- **Consumer access level:** Any FreeAgent user can authorize; the connection operates at the authorizing user's permission level, so a full-access user is recommended for complete data.
- **Sandbox:** available ([signup](https://signup.sandbox.freeagent.com/signup)) — Free self-service sandbox account.
- **Costs:** API access is free (API Terms v2.1, February 2025; fees possible on 30 days' notice); consumers need an active FreeAgent subscription (30-day free trial).
- **Rate limits:** 120 requests/minute and 3,600 requests/hour, per user.
- **Authentication:** Authorization Code flow.
- **Webhooks:** No webhooks — no native or virtual webhooks; data sync is polling-based.

**Important to know:**

- FreeAgent is UK-centric — optimised for UK tax compliance (VAT, MTD, Self Assessment); confirm fit for non-UK consumers.
- The standard Company API is fully self-serve; the Accountancy Practice API (accountants reading client data across companies) is not — it requires requesting a Practice sandbox from FreeAgent at integrationsrequests@freeagent.com first.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/freeagent` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **FreeAgent** — for example, "create an invoice in FreeAgent" or "reconcile payments in FreeAgent". This skill teaches the agent:

1. Which Apideck unified API covers FreeAgent (Accounting)
2. The correct `serviceId` to pass on every call (`freeagent`)
3. FreeAgent-specific auth and coverage caveats

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

// List invoices in FreeAgent
const { data } = await apideck.accounting.invoices.list({
  serviceId: "freeagent",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from FreeAgent to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — FreeAgent
await apideck.accounting.invoices.list({ serviceId: "freeagent" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating FreeAgent directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## FreeAgent via Apideck Accounting

FreeAgent is a UK-focused cloud accounting platform for freelancers and small businesses, part of NatWest Group. Popular for MTD-compliant VAT and self-assessment flows.

### Entity mapping

| FreeAgent entity | Apideck Accounting resource |
|---|---|
| Invoice | `invoices` |
| Bill | `bills` |
| Credit Note | `credit-notes` |
| Contact (customer) | `customers` |
| Contact (supplier) | `suppliers` |
| Category | `ledger-accounts` |
| Invoice Item | `invoice-items` |
| Journal Set | `journal-entries` |
| Bank Account | `bank-accounts` |
| Company Info | `company-info` |
| P&L, Balance Sheet | `profit-and-loss`, `balance-sheet` |

### Coverage highlights

- ✅ CRUD on invoices, bills, credit notes, customers, suppliers
- ✅ Journal entries
- ✅ Financial reports (P&L, Balance Sheet)
- ✅ Bank accounts
- ⚠️ VAT returns / MTD submission — use Proxy with FreeAgent's `/v2/vat_returns` endpoints
- ❌ Time tracking, project management — use Proxy
- ❌ Self-assessment / Personal tax — use Proxy

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Company binding:** one FreeAgent company per connection.
- **MTD (Making Tax Digital):** FreeAgent is HMRC-recognized. VAT submission requires additional Agent Services Account permissions not covered by the unified API.

### Example: list unpaid invoices

```typescript
const { data } = await apideck.accounting.invoices.list({
  serviceId: "freeagent",
  filter: { status: "open" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call FreeAgent directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on FreeAgent's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: freeagent" \
  -H "x-apideck-downstream-url: <target endpoint on FreeAgent>" \
  -H "x-apideck-downstream-method: GET"
```

See [FreeAgent's API docs](https://dev.freeagent.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [FreeAgent official docs](https://dev.freeagent.com)
