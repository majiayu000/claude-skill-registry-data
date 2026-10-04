---
name: picqer
description: |
  Picqer integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in Picqer. Routes through Apideck with serviceId "picqer".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: picqer
  unifiedApis: ["ecommerce"]
  authType: basic
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Picqer (via Apideck)

Access Picqer through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to Shopify, BigCommerce, Shopify (Public App) and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Picqer plumbing.

> **Beta connector.** Picqer is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `picqer`
- **Unified API:** Ecommerce
- **Auth type:** basic
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/picqer/gotchas)
- **Picqer docs:** https://picqer.com/en/api
- **Homepage:** https://picqer.com

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication - Each Consumer Creates Their Own Key in Picqer
- **Vendor partnership required:** no ([developer portal](https://picqer.com/en/partners-and-integrations)) — Picqer's partner route adds a free developer account, test data and direct support from Picqer.
- **Apideck-managed credentials:** not available — Each consumer creates their own Picqer API key.
- **Account type required:** Picqer account (any plan).
- **Consumer access level:** A Picqer administrator, since administrators create API keys.
- **Sandbox:** available ([signup](https://picqer.com/en/support/articles/picqer-api)) — Free developer account that does not expire: Picqer support converts a normal account on request and can add sample products and orders.
- **Costs:** Included in every Picqer plan at no extra cost.
- **Rate limits:** 500 requests a minute for each API key, which Picqer may adjust with platform load.
- **Authentication:** Needs the consumer's Picqer account subdomain alongside the key.
- **Webhooks:** Native - order and product events (orders created and closed, products created and changed).

**Important to know:**

- An API key has no scopes: any key gives the connection access to the whole Picqer account. Limiting a key is possible only by tying it to a fulfilment customer, and only on the fulfilment version of Picqer.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/picqer` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Picqer** — for example, "list orders in Picqer" or "sync products in Picqer". This skill teaches the agent:

1. Which Apideck unified API covers Picqer (Ecommerce)
2. The correct `serviceId` to pass on every call (`picqer`)
3. Picqer-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **Ecommerce:** [https://specs.apideck.com/ecommerce.yml](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List orders in Picqer
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "picqer",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from Picqer to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Picqer
await apideck.ecommerce.orders.list({ serviceId: "picqer" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "shopify" });
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
```

This is the compounding advantage of using Apideck over integrating Picqer directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** Basic auth (username/password)
- **Managed by:** Apideck Vault — credentials are collected through the Vault modal and stored encrypted server-side.
- **Note:** basic auth connectors often require manual rotation by the end user. If auth fails persistently, prompt them to re-enter credentials in Vault.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every Ecommerce operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/picqer' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Ecommerce unified API, use Apideck's Proxy to call Picqer directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Picqer's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: picqer" \
  -H "x-apideck-downstream-url: <target endpoint on Picqer>" \
  -H "x-apideck-downstream-method: GET"
```

See [Picqer's API docs](https://picqer.com/en/api) for available endpoints.

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`shopify`](../shopify/) *(beta)*, [`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`ebay`](../ebay/) *(beta)*, [`etsy`](../etsy/) *(beta)*, [`magento`](../magento/) *(beta)*, and 8 more.

## See also

- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Picqer official docs](https://picqer.com/en/api)
