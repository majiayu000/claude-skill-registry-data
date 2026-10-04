---
name: etsy
description: |
  Etsy integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in Etsy. Routes through Apideck with serviceId "etsy".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: etsy
  unifiedApis: ["ecommerce"]
  authType: oauth2
  tier: "1c"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Etsy (via Apideck)

Access Etsy through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to Shopify, BigCommerce, Shopify (Public App) and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Etsy plumbing.

> **Beta connector.** Etsy is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `etsy`
- **Unified API:** Ecommerce
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/etsy/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/etsy/gotchas)
- **Etsy docs:** https://developers.etsy.com
- **Homepage:** https://etsy.com

## At a glance

- **Implementation difficulty:** moderate — Self-Service App Registration + Etsy App Review
- **Vendor partnership required:** no ([Etsy developer portal](https://www.etsy.com/developers/register)) — Etsy runs no partner programme; any Etsy account holder can register an app.
- **Apideck-managed credentials:** not available — Each connection supplies its own Etsy app's Keystring and Shared Secret.
- **Account type required:** Etsy account with an active shop
- **Consumer access level:** Sign-in to the Etsy account that holds the shop being connected
- **Sandbox:** not available — Etsy's testing policy is to test on production with a real shop, where listing fees apply.
- **Rate limits:** Per-app QPS and QPD limits, shown in the Etsy Developer Portal.
- **Authentication:** Authorization Code flow with PKCE; requests also carry the app's key in the x-api-key header.
- **Webhooks:** No webhooks - data is read by polling.

**Important to know:**

- Etsy gates access by app type. A Seller App is approved within minutes but can only ever connect the shop of the person who registered it; connecting other sellers' shops needs a Personal App and, at scale, Commercial Access, which Etsy reviews manually.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/etsy` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Etsy** — for example, "list orders in Etsy" or "sync products in Etsy". This skill teaches the agent:

1. Which Apideck unified API covers Etsy (Ecommerce)
2. The correct `serviceId` to pass on every call (`etsy`)
3. Etsy-specific auth and coverage caveats

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

// List orders in Etsy
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "etsy",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from Etsy to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Etsy
await apideck.ecommerce.orders.list({ serviceId: "etsy" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "shopify" });
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
```

This is the compounding advantage of using Apideck over integrating Etsy directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Etsy — see [https://developers.apideck.com/connectors/etsy/docs/consumer+connection](https://developers.apideck.com/connectors/etsy/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every Ecommerce operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/etsy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Ecommerce unified API, use Apideck's Proxy to call Etsy directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Etsy's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: etsy" \
  -H "x-apideck-downstream-url: <target endpoint on Etsy>" \
  -H "x-apideck-downstream-method: GET"
```

See [Etsy's API docs](https://developers.etsy.com) for available endpoints.

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`shopify`](../shopify/) *(beta)*, [`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`ebay`](../ebay/) *(beta)*, [`magento`](../magento/) *(beta)*, [`bol-com`](../bol-com/) *(beta)*, and 8 more.

## See also

- [Apideck connection guide for Etsy](https://developers.apideck.com/connectors/etsy/docs/consumer+connection)
- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Etsy official docs](https://developers.etsy.com)
