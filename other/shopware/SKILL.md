---
name: shopware
description: |
  Shopware integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in Shopware. Routes through Apideck with serviceId "shopware".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: shopware
  unifiedApis: ["ecommerce"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Shopware (via Apideck)

Access Shopware through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to Shopify, BigCommerce, Shopify (Public App) and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Shopware plumbing.

> **Beta connector.** Shopware is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `shopware`
- **Unified API:** Ecommerce
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/shopware/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/shopware/gotchas)
- **Shopware docs:** https://developer.shopware.com
- **Homepage:** https://en.shopware.com/

## At a glance

- **Implementation difficulty:** moderate — Consumer Creates Integration Credentials in Shopware
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Credentials belong to each shop's own Integration, so there is no shared app to lend.
- **Account type required:** A Shopware 6 shop, self-hosted or Shopware cloud.
- **Consumer access level:** An admin user in the shop's Administration who can create an Integration.
- **Sandbox:** available ([signup](https://docs.shopware.com/en/shopware-account-en/general/cloud-sandbox)) — Free 30-day Developer Cloud Environment from a Shopware Account; one at a time, limited capacity, not extendable.
- **Costs:** Admin API access comes with the shop, including the free self-hosted Community Edition.
- **Rate limits:** No general cap documented for Admin API requests; on Shopware SaaS the token endpoint allows 10 requests per minute per IP address.
- **Authentication:** Client credentials grant with an Integration's Access key ID and Secret access key; no consent screen.
- **Webhooks:** Native - order, customer and product update and delete events

**Important to know:**

- Every Shopware shop runs on its own domain, so a connection only works if that domain serves the Admin API and can be reached from outside. Shops behind Cloudflare protections, a WAF or a firewall must allow Apideck's static IPs.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/shopware` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Shopware** — for example, "list orders in Shopware" or "sync products in Shopware". This skill teaches the agent:

1. Which Apideck unified API covers Shopware (Ecommerce)
2. The correct `serviceId` to pass on every call (`shopware`)
3. Shopware-specific auth and coverage caveats

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

// List orders in Shopware
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "shopware",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from Shopware to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Shopware
await apideck.ecommerce.orders.list({ serviceId: "shopware" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "shopify" });
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
```

This is the compounding advantage of using Apideck over integrating Shopware directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Shopware — see [https://developers.apideck.com/connectors/shopware/docs/consumer+connection](https://developers.apideck.com/connectors/shopware/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every Ecommerce operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/shopware' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Ecommerce unified API, use Apideck's Proxy to call Shopware directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Shopware's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: shopware" \
  -H "x-apideck-downstream-url: <target endpoint on Shopware>" \
  -H "x-apideck-downstream-method: GET"
```

See [Shopware's API docs](https://developer.shopware.com) for available endpoints.

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`shopify`](../shopify/) *(beta)*, [`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`ebay`](../ebay/) *(beta)*, [`etsy`](../etsy/) *(beta)*, [`magento`](../magento/) *(beta)*, and 8 more.

## See also

- [Apideck connection guide for Shopware](https://developers.apideck.com/connectors/shopware/docs/consumer+connection)
- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Shopware official docs](https://developer.shopware.com)
