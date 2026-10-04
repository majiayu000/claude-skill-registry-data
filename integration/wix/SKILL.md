---
name: wix
description: |
  Wix  integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in Wix . Routes through Apideck with serviceId "wix".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: wix
  unifiedApis: ["ecommerce"]
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Wix  (via Apideck)

Access Wix  through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to Shopify, BigCommerce, Shopify (Public App) and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Wix  plumbing.

> **Beta connector.** Wix  is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `wix`
- **Unified API:** Ecommerce
- **Auth type:** apiKey
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/wix/gotchas)
- **Homepage:** https://wix.com

## At a glance

- **Implementation difficulty:** moderate — API Key Created by the Wix Account Owner
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer creates their own Wix API key.
- **Account type required:** Wix site with the Wix Stores app installed.
- **Consumer access level:** Account owner or co-owner, the only roles that can create an API key.
- **Sandbox:** available ([signup](https://dev.wix.com/docs/build-apps/develop-your-app/development-sites/about-development-sites)) — Free development site with Premium capabilities, created from a Wix developer app dashboard.
- **Costs:** Wix documents no separate fee for API keys.
- **Authentication:** Account-level key, supplied together with the Site ID and Shop Domain; not OAuth.
- **Webhooks:** Virtual webhooks - order, product and customer created, updated and deleted events

**Important to know:**

- The API key has to come from the Wix account that owns the site, and its site access must include that site. A key from an agency or another account, or one restricted to other sites, is rejected even with the right permissions.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/wix` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Wix ** — for example, "list orders in Wix " or "sync products in Wix ". This skill teaches the agent:

1. Which Apideck unified API covers Wix  (Ecommerce)
2. The correct `serviceId` to pass on every call (`wix`)
3. Wix -specific auth and coverage caveats

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

// List orders in Wix 
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "wix",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from Wix  to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Wix 
await apideck.ecommerce.orders.list({ serviceId: "wix" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "shopify" });
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
```

This is the compounding advantage of using Apideck over integrating Wix  directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Wix  API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every Ecommerce operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/wix' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Ecommerce unified API, use Apideck's Proxy to call Wix  directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Wix 's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: wix" \
  -H "x-apideck-downstream-url: <target endpoint on Wix >" \
  -H "x-apideck-downstream-method: GET"
```

See [Wix 's API docs](#) for available endpoints.

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`shopify`](../shopify/) *(beta)*, [`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`ebay`](../ebay/) *(beta)*, [`etsy`](../etsy/) *(beta)*, [`magento`](../magento/) *(beta)*, and 8 more.

## See also

- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
