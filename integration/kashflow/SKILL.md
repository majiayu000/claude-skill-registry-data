---
name: kashflow
description: |
  Kashflow integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Kashflow. Routes through Apideck with serviceId "kashflow".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: kashflow
  unifiedApis: ["accounting"]
  authType: basic
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Kashflow (via Apideck)

Access Kashflow through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Kashflow plumbing.

> **Beta connector.** Kashflow is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `kashflow`
- **Unified API:** Accounting
- **Auth type:** basic
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/kashflow/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/kashflow/gotchas)
- **Kashflow docs:** https://developer.kashflow.com
- **Homepage:** https://www.kashflow.com/

## At a glance

- **Implementation difficulty:** moderate — Basic Authentication — consumers must enable the SOAP API in their account first
- **Vendor partnership required:** no ([KashFlow App Partner Programme](https://www.kashflow.com/become-an-app-partner/)) — The KashFlow App Partner programme is optional co-marketing, not a prerequisite for API access.
- **Apideck-managed credentials:** not available — Every consumer supplies their own KashFlow credentials.
- **Account type required:** Any KashFlow account on the Business package
- **Consumer access level:** A KashFlow user who can change the account's API settings — typically the account owner.
- **Sandbox:** available ([signup](https://www.kashflow.com/try-kashflow/)) — A free 14-day KashFlow trial on the Business package is enough to build against, and KashFlow issues a dedicated developer test account on request.
- **Costs:** KashFlow subscription required — the API needs the Business package, RRP £27.50/month. API access itself carries no separate charge.
- **Rate limits:** Not published by KashFlow — no per-minute or per-day limit is documented for this API.
- **Authentication:** The consumer's own KashFlow username and password (not OAuth).
- **Webhooks:** No webhooks — KashFlow publishes no events, so keep the integration on polling.

**Important to know:**

- KashFlow is read-only through Apideck: every mapped operation is a read, so there is no create, update or delete path for any resource.
- KashFlow lets each account choose whether the API accepts the web login password or a separate API password — sending the wrong one is the most common connection failure.
- The connector runs on KashFlow's SOAP/XML API. KashFlow also publishes a newer REST API, but its own documentation says it is not ready for public use, so it is not an alternative here.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/kashflow` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Kashflow** — for example, "create an invoice in Kashflow" or "reconcile payments in Kashflow". This skill teaches the agent:

1. Which Apideck unified API covers Kashflow (Accounting)
2. The correct `serviceId` to pass on every call (`kashflow`)
3. Kashflow-specific auth and coverage caveats

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

// List invoices in Kashflow
const { data } = await apideck.accounting.invoices.list({
  serviceId: "kashflow",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Kashflow to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Kashflow
await apideck.accounting.invoices.list({ serviceId: "kashflow" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Kashflow directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Kashflow via Apideck Accounting

Kashflow is a UK-focused cloud accounting platform for SMB, owned by IRIS Software Group. Straightforward coverage of the standard UK accounting entity set.

### Entity mapping

| Kashflow entity | Apideck Accounting resource |
|---|---|
| Invoice | `invoices` |
| Bill / Purchase Invoice | `bills` (partial) |
| Credit Note | `credit-notes` |
| Customer | `customers` |
| Supplier | `suppliers` |
| Item | `invoice-items` |
| Nominal Code | `ledger-accounts` |
| Journal | `journal-entries` |
| VAT | `tax-rates` |
| Payment | `payments` |
| Company Info | `company-info` |

### Coverage highlights

- ✅ Full CRUD on invoices, customers, suppliers
- ✅ Credit notes
- ✅ Journal entries
- ✅ Tax rates (UK VAT)
- ✅ Payments
- ⚠️ Payroll integration (Kashflow Payroll) — separate product surface; use Proxy
- ❌ Bank feeds — limited; use Proxy
- ❌ MTD-specific VAT return submissions — use Proxy

### Auth notes

- **Type:** Basic auth (API username + password), managed by Apideck Vault
- **Company binding:** one Kashflow company per connection.
- **Legacy flavor:** Kashflow's API is SOAP-based under the hood; Apideck abstracts this. Proxy calls still use SOAP envelopes.

### Example: list recent invoices

```typescript
const { data } = await apideck.accounting.invoices.list({
  serviceId: "kashflow",
  filter: { updated_since: "2026-04-01T00:00:00Z" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Kashflow directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Kashflow's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: kashflow" \
  -H "x-apideck-downstream-url: <target endpoint on Kashflow>" \
  -H "x-apideck-downstream-method: GET"
```

See [Kashflow's API docs](https://developer.kashflow.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Apideck connection guide for Kashflow](https://developers.apideck.com/connectors/kashflow/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Kashflow official docs](https://developer.kashflow.com)
