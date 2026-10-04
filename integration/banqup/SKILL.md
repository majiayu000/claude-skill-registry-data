---
name: banqup
description: |
  banqUP integration via Apideck's Accounting unified API — same methods work across every connector in Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in banqUP. Routes through Apideck with serviceId "banqup".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: banqup
  unifiedApis: ["accounting"]
  authType: oauth2
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# banqUP (via Apideck)

Access banqUP through Apideck's **Accounting** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, Campfire and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant banqUP plumbing.

> **Beta connector.** banqUP is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `banqup`
- **Unified API:** Accounting
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/accounting/banqup/gotchas)
- **banqUP docs:** https://banqup.com
- **Homepage:** https://banqup.com/

## At a glance

- **Implementation difficulty:** moderate — Self-Service OAuth Credentials + Per-Business App Whitelisting Required
- **Vendor partnership required:** no — No partnership or certification gates API access; developer-portal registration is self-service. Banqup Group's reseller programme is unrelated.
- **Apideck-managed credentials:** not available — You register your own app on the Banqup Developer Portal and supply its credentials.
- **Account type required:** A banqUP business account for the data, plus a free Banqup Developer Portal account to register the app.
- **Consumer access level:** The banqUP space's legal representative, or a space admin acting for them.
- **Sandbox:** available — Self-service: register on banqUP's separate CVE sandbox developer portal, documented at docs.cve.btx.banqup.com, to obtain sandbox credentials.
- **Costs:** Developer-portal access and API use carry no separate charge; they come with the consumer's banqUP subscription.
- **Rate limits:** No published numeric limit. Limits apply per credential set; raising one is arranged with a banqUP contact and may require a higher plan.
- **Authentication:** Client-credentials flow: the app authenticates as itself, so consumers never see a login screen.
- **Webhooks:** No webhooks — banqUP publishes none for this API, so changes are picked up by polling.

**Important to know:**

- banqUP is read-only through Apideck: there is no create, update or delete path, so plan a one-way sync out of banqUP.
- Access is granted inside banqUP, not by the credentials alone: your app has to be whitelisted in the connected business's own space before it can retrieve anything. Until that happens, a correctly configured connection returns no data rather than an error.
- Each connection is scoped to a single seller. banqUP requires a seller id, which the list operations use as a path parameter, so your consumer needs to know which seller their credentials represent, and each additional seller is its own connection.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/banqup` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **banqUP** — for example, "create an invoice in banqUP" or "reconcile payments in banqUP". This skill teaches the agent:

1. Which Apideck unified API covers banqUP (Accounting)
2. The correct `serviceId` to pass on every call (`banqup`)
3. banqUP-specific auth and coverage caveats

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

// List invoices in banqUP
const { data } = await apideck.accounting.invoices.list({
  serviceId: "banqup",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from banqUP to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — banqUP
await apideck.accounting.invoices.list({ serviceId: "banqup" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating banqUP directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## banqUP via Apideck Accounting

banqUP is a Belgian cloud invoicing and business banking platform targeting SMBs and accountants. Apideck coverage is invoice-focused.

### Entity mapping

| banqUP entity | Apideck Accounting resource |
|---|---|
| Invoice | `invoices` |
| Customer | `customers` |

### Coverage highlights

- ✅ Invoices (CRUD)
- ✅ Customers
- ⚠️ AP / bills — not in current Apideck mapping; use Proxy
- ❌ Payments, journal entries, ledger accounts — use Proxy
- ❌ Business banking features — separate banqUP API surface

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Organization binding:** one banqUP organization per connection.
- **Belgium-focused:** Belgian compliance (PEPPOL e-invoicing, Belgian VAT) built-in.
- **Coverage is narrow:** this connector currently exposes only invoices + customers. If you need full accounting breadth, pick a different Belgian connector (e.g. [`exact-online`](../exact-online/)).

### Example: create an invoice

```typescript
const { data } = await apideck.accounting.invoices.create({
  serviceId: "banqup",
  invoice: {
    customer_id: "cust_abc",
    invoice_date: "2026-04-18",
    line_items: [
      { description: "Consulting", quantity: 5, unit_price: 120 },
    ],
    currency: "EUR",
  },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call banqUP directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on banqUP's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: banqup" \
  -H "x-apideck-downstream-url: <target endpoint on banqUP>" \
  -H "x-apideck-downstream-method: GET"
```

See [banqUP's API docs](https://banqup.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), [`exact-online-nl`](../exact-online-nl/) *(beta)*, and 25 more.

## See also

- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [banqUP official docs](https://banqup.com)
