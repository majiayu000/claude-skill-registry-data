---
name: yuki
description: |
  Yuki integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Yuki. Routes through Apideck with serviceId "yuki".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: yuki
  unifiedApis: ["accounting"]
  authType: apiKey
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Yuki (via Apideck)

Access Yuki through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Yuki plumbing.

> **Beta connector.** Yuki is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `yuki`
- **Unified API:** Accounting
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/yuki/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/yuki/gotchas)
- **Yuki docs:** https://api.yukiworks.nl
- **Homepage:** https://www.yuki.nl/

## At a glance

- **Implementation difficulty:** moderate — API key authentication over SOAP
- **Vendor partnership required:** no — There is no app registration, review or partner agreement for Yuki's web services.
- **Apideck-managed credentials:** not available — Each consumer connects with their own web service key, so there is no shared Apideck application.
- **Account type required:** Yuki account on any bundle, including the free Minimal bundle, with web service access activated on the domain.
- **Consumer access level:** A user with the Portal administrator or Management role — only those roles can create web service keys.
- **Sandbox:** not available — Yuki's free Minimal bundle is a real account, not a test environment; there is no developer sandbox or demo administration.
- **Costs:** Free to 1,000 calls/day. Above that: EUR 10.50/month for 1,001-5,000 calls/day, EUR 105/month for 5,001-10,000 — added by the consumer's accountant.
- **Rate limits:** 1,000 web service calls per day per domain; paid add-ons raise the ceiling.
- **Authentication:** A WebserviceAccessKey; not OAuth, and no redirect for your consumer to complete.
- **Webhooks:** No webhooks — Yuki documents no event or subscription mechanism, and this connector adds no virtual webhooks, so poll for changes.

**Important to know:**

- Turning on web service access is not something your consumer does alone — it is a domain feature their accountant or administrative office switches on. Build that hand-off into onboarding and confirm it is enabled before a consumer tries to connect.
- Each operation opens a Yuki session before the request itself, so one Unify call becomes two calls to Yuki. Yuki does not document whether the session call counts against the daily quota, so size capacity conservatively.
- On the free Minimal bundle the Sales web service has to be added as an accountant feature on top of general web service access; the paid bundles include it. Worth confirming with a Minimal-bundle consumer before you plan an invoicing flow.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/yuki` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Yuki** — for example, "create an invoice in Yuki" or "reconcile payments in Yuki". This skill teaches the agent:

1. Which Apideck unified API covers Yuki (Accounting)
2. The correct `serviceId` to pass on every call (`yuki`)
3. Yuki-specific auth and coverage caveats

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

// List invoices in Yuki
const { data } = await apideck.accounting.invoices.list({
  serviceId: "yuki",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Yuki to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Yuki
await apideck.accounting.invoices.list({ serviceId: "yuki" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Yuki directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Yuki via Apideck Accounting

Yuki is a Dutch cloud accounting and bookkeeping platform, strong in automated document processing and NL/BE SMB markets.

### Entity mapping

| Yuki entity | Apideck Accounting resource |
|---|---|
| Sales Invoice | `invoices` |
| Purchase Invoice | `bills` |
| Journal Entry (GB-mutation) | `journal-entries` |
| GL Account | `ledger-accounts` |
| Customer (Debtor) | `customers` |
| Supplier (Creditor) | `suppliers` |
| BTW code | `tax-rates` |
| Cost centre | `tracking-categories` |
| Company (Administration) | `company-info` |
| Attachments | `attachments` |

### Coverage highlights

- ✅ CRUD on invoices, bills, customers, suppliers
- ✅ Journal entries and Dutch BTW handling
- ✅ Tracking categories (cost centres)
- ✅ Document attachments (Yuki's OCR output)
- ❌ Automated document recognition workflow (Yuki's signature feature) — not exposed; use Proxy
- ❌ Bank reconciliation rules — use Proxy

### Auth notes

- **Type:** API key, managed by Apideck Vault
- **Administration-scoped:** Yuki API keys are tied to a single administration (tenant). Multi-admin customers need one connection per admin.
- **Permission scope:** key inherits the generator's role — admin-level access recommended for full coverage.

### Example: list invoices for a specific period

```typescript
const { data } = await apideck.accounting.invoices.list({
  serviceId: "yuki",
  filter: { updated_since: "2026-01-01T00:00:00Z" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Yuki directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Yuki's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: yuki" \
  -H "x-apideck-downstream-url: <target endpoint on Yuki>" \
  -H "x-apideck-downstream-method: GET"
```

See [Yuki's API docs](https://api.yukiworks.nl) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Apideck connection guide for Yuki](https://developers.apideck.com/connectors/yuki/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Yuki official docs](https://api.yukiworks.nl)
