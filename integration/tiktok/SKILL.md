---
name: tiktok
description: |
  TikTok Shop integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in TikTok Shop. Routes through Apideck with serviceId "tiktok".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: tiktok
  unifiedApis: ["ecommerce"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: involved
  partnershipRequired: true
  sandboxAvailable: true
---

# TikTok Shop (via Apideck)

Access TikTok Shop through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to Shopify, BigCommerce, Shopify (Public App) and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant TikTok Shop plumbing.

> **Beta connector.** TikTok Shop is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `tiktok`
- **Unified API:** Ecommerce
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/tiktok/gotchas)
- **TikTok Shop docs:** https://partner.tiktokshop.com/doc
- **Homepage:** https://www.tiktok.com/

## At a glance

- **Implementation difficulty:** involved — Partner Center App-Developer Registration + Mandatory Compliance and Legal Review
- **Vendor partnership required:** yes ([TikTok Shop Partner Center](https://partner.tiktokshop.com/account/sign-up)) — Register as an App developer (ISV), not a Seller developer. US partners sign up at partner.us.tiktokshop.com instead. A compliance and legal review follows.
- **Apideck-managed credentials:** not available — You bring your own TikTok Shop Partner Center app key and secret, for testing as well as production.
- **Account type required:** A TikTok Shop Partner Center account with an app created, and the shop, order and product APIs enabled on it.
- **Consumer access level:** Any TikTok Shop seller who can approve the authorization for their own shop; TikTok documents no separate staff permission level.
- **Sandbox:** available — TikTok Shop's Developer Guide covers development shops and an API testing tool; the access route is not documented publicly.
- **Rate limits:** No fixed published figure — TikTok allocates request capacity dynamically per shop and per endpoint. Check an endpoint's own reference doc for a stated limit.
- **Authentication:** OAuth-style code exchange, then a custom access-token header and mandatory request signing on every call rather than Bearer. Apideck handles all of it.
- **Webhooks:** No webhooks — neither native nor virtual, so TikTok Shop data is kept in sync by polling.

**Important to know:**

- Each connection currently asks the connecting seller for your app key, secret and service id in Vault, rather than those being set once for the integration, so plan to supply them per connection.
- TikTok releases dated API versions about monthly and guarantees a previous version stays callable for only two months after its successor ships, with retirements announced in its changelog, so integrations need an upgrade habit.
- TikTok ties the refresh token's expiry to the authorization period the seller granted rather than to a fixed lifetime, so a connection can lapse on the seller's schedule and need re-authorizing.
- One seller authorization can cover several shops, and each connection is bound to the single shop chosen after authorizing, so a seller running more than one shop needs a connection per shop.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/tiktok` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **TikTok Shop** — for example, "list orders in TikTok Shop" or "sync products in TikTok Shop". This skill teaches the agent:

1. Which Apideck unified API covers TikTok Shop (Ecommerce)
2. The correct `serviceId` to pass on every call (`tiktok`)
3. TikTok Shop-specific auth and coverage caveats

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

// List orders in TikTok Shop
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "tiktok",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from TikTok Shop to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — TikTok Shop
await apideck.ecommerce.orders.list({ serviceId: "tiktok" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "shopify" });
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
```

This is the compounding advantage of using Apideck over integrating TikTok Shop directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every Ecommerce operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/tiktok' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Ecommerce unified API, use Apideck's Proxy to call TikTok Shop directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on TikTok Shop's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: tiktok" \
  -H "x-apideck-downstream-url: <target endpoint on TikTok Shop>" \
  -H "x-apideck-downstream-method: GET"
```

See [TikTok Shop's API docs](https://partner.tiktokshop.com/doc) for available endpoints.

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`shopify`](../shopify/) *(beta)*, [`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`ebay`](../ebay/) *(beta)*, [`etsy`](../etsy/) *(beta)*, [`magento`](../magento/) *(beta)*, and 8 more.

## See also

- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [TikTok Shop official docs](https://partner.tiktokshop.com/doc)
