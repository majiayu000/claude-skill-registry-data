---
name: bol-com
description: |
  bol.com integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in bol.com. Routes through Apideck with serviceId "bol-com".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: bol-com
  unifiedApis: ["ecommerce"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# bol.com (via Apideck)

Access bol.com through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to Shopify, BigCommerce, Shopify (Public App) and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant bol.com plumbing.

> **Beta connector.** bol.com is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `bol-com`
- **Unified API:** Ecommerce
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/bol-com/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/bol-com/gotchas)
- **bol.com docs:** https://api.bol.com
- **Homepage:** https://www.bol.com

## At a glance

- **Implementation difficulty:** moderate — Each Seller Creates Client Credentials in the bol.com Seller Dashboard
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each seller creates their own Client ID and Client Secret.
- **Account type required:** A bol.com seller account: a business registered in the Netherlands or Belgium with a VAT number.
- **Consumer access level:** Someone with access to the seller account's API settings in the bol.com Seller Dashboard.
- **Sandbox:** not available — bol.com's demo environment returns fixed example responses, not your own shop's data.
- **Costs:** No fee (Retailer API Terms of Service, article 4.1).
- **Rate limits:** Set per endpoint: listing orders allows 25 requests a minute and retrieving a single order 25 a second.
- **Authentication:** Client credentials flow; no user consent step.
- **Webhooks:** No webhooks - data is read by polling.

**Important to know:**

- bol.com only issues API credentials after the seller registers a technical contact in the Seller Dashboard. bol.com contacts that person about API use, expects an answer within 2 working days, and may block API access if they cannot be reached.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/bol-com` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **bol.com** — for example, "list orders in bol.com" or "sync products in bol.com". This skill teaches the agent:

1. Which Apideck unified API covers bol.com (Ecommerce)
2. The correct `serviceId` to pass on every call (`bol-com`)
3. bol.com-specific auth and coverage caveats

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

// List orders in bol.com
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "bol-com",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from bol.com to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — bol.com
await apideck.ecommerce.orders.list({ serviceId: "bol-com" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "shopify" });
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
```

This is the compounding advantage of using Apideck over integrating bol.com directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for bol.com — see [https://developers.apideck.com/connectors/bol-com/docs/consumer+connection](https://developers.apideck.com/connectors/bol-com/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every Ecommerce operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/bol-com' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Ecommerce unified API, use Apideck's Proxy to call bol.com directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on bol.com's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: bol-com" \
  -H "x-apideck-downstream-url: <target endpoint on bol.com>" \
  -H "x-apideck-downstream-method: GET"
```

See [bol.com's API docs](https://api.bol.com) for available endpoints.

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`shopify`](../shopify/) *(beta)*, [`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`ebay`](../ebay/) *(beta)*, [`etsy`](../etsy/) *(beta)*, [`magento`](../magento/) *(beta)*, and 8 more.

## See also

- [Apideck connection guide for bol.com](https://developers.apideck.com/connectors/bol-com/docs/consumer+connection)
- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [bol.com official docs](https://api.bol.com)
