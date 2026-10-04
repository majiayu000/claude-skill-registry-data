---
name: ebay
description: |
  eBay integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in eBay. Routes through Apideck with serviceId "ebay".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: ebay
  unifiedApis: ["ecommerce"]
  authType: oauth2
  tier: "1c"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# eBay (via Apideck)

Access eBay through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to Shopify, BigCommerce, Shopify (Public App) and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant eBay plumbing.

> **Beta connector.** eBay is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `ebay`
- **Unified API:** Ecommerce
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/ebay/gotchas)
- **eBay docs:** https://developer.ebay.com
- **Homepage:** https://www.ebay.com/

## At a glance

- **Implementation difficulty:** moderate — Self-Service OAuth Keyset + Production Activation Requirement
- **Vendor partnership required:** no ([eBay Developers Program](https://developer.ebay.com/join)) — Joining the eBay Developers Program gives you sandbox and production keysets for the Sell APIs this connector calls.
- **Apideck-managed credentials:** not available — You register your own eBay keyset.
- **Account type required:** An eBay seller account holding the listings and orders to sync.
- **Consumer access level:** The account owner signs in to eBay and grants read access to their selling data.
- **Sandbox:** available ([signup](https://developer.ebay.com/join)) — It returns no orders and none can be created through the API, so eBay advises testing on production with a seller account that has test listings.
- **Costs:** eBay publishes no API access fee. The Stores resource needs an active eBay store subscription on the seller's account.
- **Rate limits:** Default daily quotas: 100,000 calls on the Fulfillment API order resource, 5,000 on the Trading API; higher after eBay's Application Growth Check.
- **Authentication:** Authorization Code flow; eBay uses a RuName in place of a redirect URL.
- **Webhooks:** No webhooks - orders, listings and the store are read on request.

**Important to know:**

- Before your keyset's first production call, eBay requires you to subscribe to its marketplace account deletion notifications or apply for an exemption; eBay's guide states that non-compliance can end or reduce API access.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/ebay` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **eBay** — for example, "list orders in eBay" or "sync products in eBay". This skill teaches the agent:

1. Which Apideck unified API covers eBay (Ecommerce)
2. The correct `serviceId` to pass on every call (`ebay`)
3. eBay-specific auth and coverage caveats

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

// List orders in eBay
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "ebay",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from eBay to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — eBay
await apideck.ecommerce.orders.list({ serviceId: "ebay" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "shopify" });
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
```

This is the compounding advantage of using Apideck over integrating eBay directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every Ecommerce operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/ebay' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Ecommerce unified API, use Apideck's Proxy to call eBay directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on eBay's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: ebay" \
  -H "x-apideck-downstream-url: <target endpoint on eBay>" \
  -H "x-apideck-downstream-method: GET"
```

See [eBay's API docs](https://developer.ebay.com) for available endpoints.

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`shopify`](../shopify/) *(beta)*, [`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`etsy`](../etsy/) *(beta)*, [`magento`](../magento/) *(beta)*, [`bol-com`](../bol-com/) *(beta)*, and 8 more.

## See also

- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [eBay official docs](https://developer.ebay.com)
