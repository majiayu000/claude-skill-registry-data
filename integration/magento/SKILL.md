---
name: magento
description: |
  Magento integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in Magento. Routes through Apideck with serviceId "magento".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: magento
  unifiedApis: ["ecommerce"]
  authType: custom
  tier: "1c"
  verified: true
  status: beta
  difficulty: involved
  partnershipRequired: false
  sandboxAvailable: true
---

# Magento (via Apideck)

Access Magento through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to Shopify, BigCommerce, Shopify (Public App) and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Magento plumbing.

> **Beta connector.** Magento is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `magento`
- **Unified API:** Ecommerce
- **Auth type:** custom
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/magento/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/magento/gotchas)
- **Magento docs:** https://developer.adobe.com/commerce/webapi/
- **Homepage:** https://magento.com/

## At a glance

- **Implementation difficulty:** involved — Custom Auth + Manual Per-Consumer Integration Setup
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer creates an integration in their own Magento store.
- **Account type required:** Magento Open Source 2.x, or Adobe Commerce 2.x on-premises or on Adobe's cloud infrastructure (PaaS).
- **Consumer access level:** A Magento Admin user with permission to manage integrations.
- **Sandbox:** available ([signup](https://experienceleague.adobe.com/en/docs/commerce-operations/installation-guide/overview)) — Install Magento Open Source on your own server or container and create an integration there; Adobe hosts no test store, so this takes server skills.
- **Costs:** Integration tokens are a built-in Admin feature of the store; Adobe publishes no separate API fee.
- **Rate limits:** No general REST quota is published; Adobe's opt-in rate limiting covers checkout and payment endpoints only.
- **Authentication:** Four credentials from a Magento integration sign each request, OAuth 1.0a style; no redirect flow.
- **Webhooks:** Virtual webhooks - order, product and customer events (created, updated, deleted)

**Important to know:**

- Check the store's edition before you commit: Adobe Commerce as a Cloud Service (SaaS) offers no integration tokens and uses Adobe IMS OAuth 2 instead, which this connector does not use, so SaaS stores cannot connect.
- The store's /rest endpoints must be reachable from the internet. Stores behind Cloudflare, a WAF or bot protection need Apideck's requests let through; otherwise calls fail with an HTML error while the connection still shows as connected.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/magento` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Magento** — for example, "list orders in Magento" or "sync products in Magento". This skill teaches the agent:

1. Which Apideck unified API covers Magento (Ecommerce)
2. The correct `serviceId` to pass on every call (`magento`)
3. Magento-specific auth and coverage caveats

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

// List orders in Magento
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "magento",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from Magento to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Magento
await apideck.ecommerce.orders.list({ serviceId: "magento" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "shopify" });
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
```

This is the compounding advantage of using Apideck over integrating Magento directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** custom (connector-specific)
- **Managed by:** Apideck Vault — setup may involve extra fields beyond a single token. The Vault modal will prompt for everything required.
- **Refer to:** the Apideck dashboard or [apideck-best-practices](../../skills/apideck-best-practices/) for auth troubleshooting.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Magento — see [https://developers.apideck.com/connectors/magento/docs/consumer+connection](https://developers.apideck.com/connectors/magento/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every Ecommerce operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/magento' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Ecommerce unified API, use Apideck's Proxy to call Magento directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Magento's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: magento" \
  -H "x-apideck-downstream-url: <target endpoint on Magento>" \
  -H "x-apideck-downstream-method: GET"
```

See [Magento's API docs](https://developer.adobe.com/commerce/webapi/) for available endpoints.

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`shopify`](../shopify/) *(beta)*, [`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`ebay`](../ebay/) *(beta)*, [`etsy`](../etsy/) *(beta)*, [`bol-com`](../bol-com/) *(beta)*, and 8 more.

## See also

- [Apideck connection guide for Magento](https://developers.apideck.com/connectors/magento/docs/consumer+connection)
- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Magento official docs](https://developer.adobe.com/commerce/webapi/)
