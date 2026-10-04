---
name: wave
description: |
  Wave integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Wave. Routes through Apideck with serviceId "wave".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: wave
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Wave (via Apideck)

Access Wave through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Wave plumbing.

> **Beta connector.** Wave is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `wave`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/wave/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/wave/gotchas)
- **Wave docs:** https://developer.waveapps.com
- **Homepage:** https://www.waveapps.com/

## At a glance

- **Implementation difficulty:** moderate — Self-Service OAuth App + Wave Approval Required to Distribute
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Register your own Wave application and add its Client ID and Secret to Apideck.
- **Account type required:** A Wave business in the US or Canada with an active Pro or Advisors subscription. Testing your own app against your own account needs neither.
- **Consumer access level:** Any user with access to the business can authorise the connection; Wave publishes no role requirement.
- **Sandbox:** not available — A free Starter account is a sufficient test environment and exposes the same API surface as Pro; Wave runs no sandbox.
- **Costs:** Wave charges no API access fees and commits to advance notice before introducing any. The subscription requirement sits on the connecting business, not you.
- **Rate limits:** Wave publishes no rate limits; its documented error codes include no throttling or rate-limit code.
- **Authentication:** Authorization Code flow. Wave's API is GraphQL-only, and each connection also needs the consumer's Wave Business ID.
- **Webhooks:** No webhooks — none surfaced by this connector, so poll for changes.

**Important to know:**

- A live connection can break with nothing changing on your side. If a connected business's Wave Pro or Advisors subscription lapses, the next token refresh returns 403 and the integration stops working until the subscription is reactivated.
- Distributing your integration to other Wave businesses requires Wave's approval. Creating the application and testing it against your own account is self-service, but Wave's Permitted Use policy covers any integration that is not direct-to-your-own-business.
- Wave serves the US and Canada only, and signup from elsewhere is geo-blocked. The block sticks to the email address on the first failed attempt, so a European team cannot simply retry behind a VPN.
- Connecting is not purely one-click. Alongside the OAuth authorisation, each consumer must supply their Wave Business ID — a base64 string taken from the business's Wave app URL — so your onboarding needs a step that tells them where to find it.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/wave` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Wave** — for example, "create an invoice in Wave" or "reconcile payments in Wave". This skill teaches the agent:

1. Which Apideck unified API covers Wave (Accounting)
2. The correct `serviceId` to pass on every call (`wave`)
3. Wave-specific auth and coverage caveats

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

// List invoices in Wave
const { data } = await apideck.accounting.invoices.list({
  serviceId: "wave",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Wave to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Wave
await apideck.accounting.invoices.list({ serviceId: "wave" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Wave directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Wave via Apideck Accounting

Wave is a free US/CA accounting platform popular with small businesses and freelancers. Coverage is read-oriented for reporting, and invoicing is the primary write path.

### Entity mapping

| Wave entity | Apideck Accounting resource |
|---|---|
| Invoice | `invoices` |
| Customer | `customers` |
| Vendor | `suppliers` |
| Account | `ledger-accounts` |
| Product | `invoice-items` |
| Sales Tax | `tax-rates` |
| Bank Account | `bank-accounts` |
| Business | `company-info` |
| P&L, Balance Sheet | `profit-and-loss`, `balance-sheet` |
| Bank Feed Statements | `bank-feed-statements` |

### Coverage highlights

- ✅ Invoices (CRUD)
- ✅ Customers, suppliers, products
- ✅ Tax rates and chart of accounts
- ✅ Financial reports (P&L, Balance Sheet)
- ✅ Bank feed statements
- ⚠️ Bill / expense management — limited; use Proxy for Wave's specific bill endpoints
- ❌ Payroll — Wave Payroll is a separate product surface
- ❌ Receipt scanning — Wave-specific feature

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Business binding:** one Wave business per connection. Multi-business users need separate connections.
- **GraphQL upstream:** Wave's API is GraphQL; Apideck translates unified REST calls into GraphQL queries. For complex reads, the Proxy API forwards raw GraphQL.

### Example: list customers with contact details

```typescript
const { data } = await apideck.accounting.customers.list({
  serviceId: "wave",
  fields: "id,display_name,email,phone,addresses",
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Wave directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Wave's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: wave" \
  -H "x-apideck-downstream-url: <target endpoint on Wave>" \
  -H "x-apideck-downstream-method: GET"
```

See [Wave's API docs](https://developer.waveapps.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Apideck connection guide for Wave](https://developers.apideck.com/connectors/wave/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Wave official docs](https://developer.waveapps.com)
