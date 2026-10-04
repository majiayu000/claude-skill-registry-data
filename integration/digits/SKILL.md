---
name: digits
description: |
  Digits integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Digits. Routes through Apideck with serviceId "digits".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: digits
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Digits (via Apideck)

Access Digits through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Digits plumbing.

> **Beta connector.** Digits is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `digits`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/digits/gotchas)
- **Digits docs:** https://digits.com
- **Homepage:** https://www.digits.com/

## At a glance

- **Implementation difficulty:** moderate — Self-service signup and sandbox — app approval required before other organisations can install your app
- **Vendor partnership required:** no — No partner programme, certification or marketplace listing to complete — a free developer account is all you need.
- **Apideck-managed credentials:** available — OAuth consent shows "Apideck" as the requesting application. Register your own Digits app for production.
- **Account type required:** Digits account (the connecting organisation's own Digits ledger)
- **Consumer access level:** Any user who can authorise third-party access to the Digits organisation — Digits documents no minimum role.
- **Sandbox:** available ([signup](https://developer.digits.com/docs/developer-sandbox-testing-your-app)) — Free, resettable Developer Sandbox with demo data, one per developer account. No live bank connections, and collaborator invites are disabled.
- **Costs:** No cost for API access — Digits charges no fees, usage paywalls or marketplace commissions (verified June 2026).
- **Rate limits:** 180 requests/minute per client ID and 60 requests/minute per access token. Approved production apps can request higher limits.
- **Authentication:** Authorization Code flow.
- **Webhooks:** No webhooks — neither native nor virtual; poll for changes. Digits has a webhook contract of its own, but it is in private beta and unused here.

**Important to know:**

- Connecting your own Digits businesses works from day one. Installing your app into any organisation outside your own requires Digits to approve it first, requested by email.
- The Digits Connect API launched publicly in October 2025 and its surface is still expanding, so expect capability to grow between releases.
- Uninstalling your app from an organisation revokes its tokens — that connection stops working until the consumer authorises again.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/digits` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Digits** — for example, "create an invoice in Digits" or "reconcile payments in Digits". This skill teaches the agent:

1. Which Apideck unified API covers Digits (Accounting)
2. The correct `serviceId` to pass on every call (`digits`)
3. Digits-specific auth and coverage caveats

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

// List invoices in Digits
const { data } = await apideck.accounting.invoices.list({
  serviceId: "digits",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Digits to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Digits
await apideck.accounting.invoices.list({ serviceId: "digits" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Digits directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Digits via Apideck Accounting

Digits is a modern US-focused accounting platform built for real-time financial visibility, popular with startups and venture-backed companies. Apideck coverage focuses on reporting and ledger views.

### Entity mapping

| Digits entity | Apideck Accounting resource |
|---|---|
| Account | `ledger-accounts` |
| Journal Entry | `journal-entries` |
| Customer | `customers` |
| Vendor | `suppliers` |
| Dimension | `tracking-categories` |
| P&L, Balance Sheet | `profit-and-loss`, `balance-sheet` |

### Coverage highlights

- ✅ Ledger accounts (chart of accounts)
- ✅ Journal entries
- ✅ Customers, suppliers
- ✅ Financial reports (P&L, Balance Sheet)
- ✅ Dimensions (tracking categories)
- ❌ Invoices, bills, payments — Digits is primarily a reporting/analytics layer on top of QuickBooks/Xero; transactional writes go through those source systems
- ❌ AI-driven insights — Digits' signature feature; proprietary, not exposed

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Workspace binding:** one Digits workspace per connection.
- **Upstream source:** Digits typically syncs from QuickBooks or Xero. For transactional writes, use those connectors directly; use Digits for unified reporting views.

### Example: fetch P&L for the quarter

```typescript
const { data } = await apideck.accounting.profitAndLoss.get({
  serviceId: "digits",
  filter: { start_date: "2026-01-01", end_date: "2026-03-31" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Digits directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Digits's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: digits" \
  -H "x-apideck-downstream-url: <target endpoint on Digits>" \
  -H "x-apideck-downstream-method: GET"
```

See [Digits's API docs](https://digits.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), [`exact-online-nl`](../exact-online-nl/) *(beta)*, and 25 more.

## See also

- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Digits official docs](https://digits.com)
