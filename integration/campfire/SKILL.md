---
name: campfire
description: |
  Campfire integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Campfire. Routes through Apideck with serviceId "campfire".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: campfire
  unifiedApis: ["accounting"]
  authType: apiKey
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Campfire (via Apideck)

Access Campfire through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Campfire plumbing.

> **Beta connector.** Campfire is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `campfire`
- **Unified API:** Accounting
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/campfire/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/campfire/gotchas)
- **Campfire docs:** https://www.campfire.com
- **Homepage:** https://campfire.ai/

## At a glance

- **Implementation difficulty:** moderate — API Key authentication — the consumer creates a dedicated API user and key in Campfire
- **Vendor partnership required:** no ([developer portal](https://hi.meetcampfire.com/partnerships)) — The Campfire Partner Program is a commercial referral programme, unrelated to API access.
- **Apideck-managed credentials:** not available — Each consumer supplies their own Campfire API key.
- **Account type required:** Campfire account (any plan)
- **Consumer access level:** Admin role on a dedicated API user (full read and write); clerk or view only for narrower integrations.
- **Sandbox:** available — On request — Campfire has publicly said it provisions evaluation sandboxes; there is no documented self-service signup, so ask Campfire.
- **Costs:** No public price list — Campfire pricing is quote-based and no free tier is documented. No separate fee for API access is documented either.
- **Rate limits:** 5 requests/second per API user, shared across all endpoints; exceeding it returns 429 with a Retry-After header.
- **Authentication:** The consumer supplies a token sent as an Authorization: Token <key> header. Not OAuth; the key is static with no documented expiry.
- **Webhooks:** No webhooks — neither native nor virtual; poll for changes. Campfire's own API offers webhook subscriptions, but this connector does not use them.

**Important to know:**

- Consumers generate their own API key in Campfire account settings, and it is displayed only once — it must be copied immediately.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/campfire` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Campfire** — for example, "create an invoice in Campfire" or "reconcile payments in Campfire". This skill teaches the agent:

1. Which Apideck unified API covers Campfire (Accounting)
2. The correct `serviceId` to pass on every call (`campfire`)
3. Campfire-specific auth and coverage caveats

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

// List invoices in Campfire
const { data } = await apideck.accounting.invoices.list({
  serviceId: "campfire",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Campfire to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Campfire
await apideck.accounting.invoices.list({ serviceId: "campfire" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Campfire directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Campfire via Apideck Accounting

Campfire is a modern accounting platform designed for fast-growing companies with multi-entity and multi-dimensional tracking needs. Very broad Apideck coverage.

### Entity mapping

| Campfire entity | Apideck Accounting resource |
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
| Department | `departments` |
| Subsidiary | `subsidiaries` |
| Tracking Category | `tracking-categories` |
| Bank Feed Account | `bank-feed-accounts` |
| Bank Feed Statement | `bank-feed-statements` |
| Company Info | `company-info` |
| P&L, Balance Sheet | `profit-and-loss`, `balance-sheet` |

### Coverage highlights

- ✅ Full CRUD on invoices, bills, payments (incl. bill payments)
- ✅ Credit notes
- ✅ Journal entries
- ✅ Departments, subsidiaries, tracking categories (deep multi-dim support)
- ✅ Bank feeds
- ✅ Financial reports (P&L, Balance Sheet)
- ⚠️ Revenue recognition — not in unified; use Proxy
- ❌ Audit trail detail beyond `updated_at` — use Proxy

### Auth notes

- **Type:** API key, managed by Apideck Vault
- **Organization binding:** one Campfire organization per connection.
- **Multi-entity:** subsidiaries exposed as a first-class resource; scale to dozens of entities per org.

### Example: list bills with department filter

```typescript
const { data } = await apideck.accounting.bills.list({
  serviceId: "campfire",
  filter: { department_id: "dept_marketing" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Campfire directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Campfire's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: campfire" \
  -H "x-apideck-downstream-url: <target endpoint on Campfire>" \
  -H "x-apideck-downstream-method: GET"
```

See [Campfire's API docs](https://www.campfire.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), [`exact-online-nl`](../exact-online-nl/) *(beta)*, and 25 more.

## See also

- [Apideck connection guide for Campfire](https://developers.apideck.com/connectors/campfire/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Campfire official docs](https://www.campfire.com)
