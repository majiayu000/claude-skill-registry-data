---
name: shopify
description: |
  Shopify integration via Apideck's Ecommerce unified API — same methods work across every connector in Ecommerce, switch by changing `serviceId`. Use when the user wants to read, write, or sync orders, products, customers, and stores in Shopify. Routes through Apideck with serviceId "shopify".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: shopify
  unifiedApis: ["ecommerce"]
  authType: custom
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Shopify (via Apideck)

Access Shopify through Apideck's **Ecommerce** unified API — one of 17 Ecommerce connectors that share the same method surface. Code you write here ports to BigCommerce, Shopify (Public App), WooCommerce and 13 other Ecommerce connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Shopify plumbing.

> **Beta connector.** Shopify is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `shopify`
- **Unified API:** Ecommerce
- **Auth type:** custom
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/shopify/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/ecommerce/shopify/gotchas)
- **Shopify docs:** https://shopify.dev/docs/api
- **Homepage:** https://www.shopify.com/

## At a glance

- **Implementation difficulty:** moderate — Merchant Self-Service Custom App via Shopify Dev Dashboard (Client Credentials) — No Partnership or App Review Required
- **Vendor partnership required:** no — No Shopify Partner account needed: custom distribution skips the app-store review process that public apps must pass.
- **Apideck-managed credentials:** not available — There is no shared Apideck-managed Shopify app; every connection uses the merchant's own app credentials.
- **Account type required:** Any paid Shopify plan; reading customer name, address, phone or email needs the merchant's store on Grow or higher (Level 2 protected customer data).
- **Consumer access level:** Store owner, or a staff member granted the App development > Develop permission; collaborator accounts cannot reach the Dev Dashboard.
- **Sandbox:** available ([signup](https://shopify.dev/docs/apps/build/stores/development-stores)) — Free Shopify development store via the Dev Dashboard or Shopify CLI — fully featured, but it cannot take real payments or become a production store.
- **Costs:** No separate charge for API access: it is included in every paid Shopify plan (Basic $39/month through Plus from $2,300/month). Free trial available.
- **Rate limits:** GraphQL Admin API: 100 to 2,000 cost points per second by plan. Legacy REST Admin API: 2 to 40 requests per second by plan.
- **Authentication:** Client Credentials against the merchant's own store; Shop, Client ID and Client Secret are entered per connection.
- **Webhooks:** Native — order, product and customer created, updated and deleted events.

**Important to know:**

- This is Shopify's custom-app route: every merchant creates and owns the app for their own store, so you register nothing centrally. Shopify's Protected Customer Data review applies to public apps, not here; custom apps meet that same protection through the store's plan instead.
- Apideck's separate Shopify (Public App) connector is the other route, where one app you own serves every merchant through a standard OAuth authorize. Pick that connector instead when you do not want each merchant creating an app.
- Shopify stopped allowing new custom apps to be created inside the Shopify admin on January 1, 2026. This connector already targets the current Dev Dashboard route, so there is nothing to migrate and no legacy credential to carry over.
- A custom app installs on one store. Covering several of a merchant's storefronts means either an app and connection per store, or stores that all sit inside a single Shopify Plus organization.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/shopify` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Shopify** — for example, "list orders in Shopify" or "sync products in Shopify". This skill teaches the agent:

1. Which Apideck unified API covers Shopify (Ecommerce)
2. The correct `serviceId` to pass on every call (`shopify`)
3. Shopify-specific auth and coverage caveats

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

// List orders in Shopify
const { data } = await apideck.ecommerce.orders.list({
  serviceId: "shopify",
});
```

## Portable across 17 Ecommerce connectors

The Apideck **Ecommerce** unified API exposes the same methods for every connector in its catalog. Switching from Shopify to another Ecommerce connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Shopify
await apideck.ecommerce.orders.list({ serviceId: "shopify" });

// Tomorrow — same code, different connector
await apideck.ecommerce.orders.list({ serviceId: "bigcommerce" });
await apideck.ecommerce.orders.list({ serviceId: "shopify-public-app" });
```

This is the compounding advantage of using Apideck over integrating Shopify directly: code against the unified Ecommerce API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Shopify via Apideck Ecommerce

Shopify is the reference Ecommerce connector. Strong coverage for orders, products, customers, and stores.

### Entity mapping

| Shopify entity | Apideck Ecommerce resource |
|---|---|
| Order | `orders` |
| Product | `products` |
| Variant | exposed via `products[].variants[]` |
| Customer | `customers` |
| Shop | `stores` |
| Fulfillment | exposed via `orders[].fulfillments[]` |
| Transaction | exposed via `orders[].payments[]` |
| Inventory Level | ❌ use Proxy |
| Discount / Price Rule | ❌ use Proxy |
| Webhook subscriptions | use Apideck Webhooks, not Shopify's |
| Metafields | `custom_fields[]` on orders/products |

### Coverage highlights

- ✅ Read orders, products, customers, stores
- ✅ Filter orders by status, date range, customer
- ✅ Filter products by vendor, status, published state
- ✅ Variants flattened into product responses
- ✅ Multi-currency orders — `currency` and `total_price` surface correctly
- ⚠️ Create / update are available for products and customers; orders are typically read-only (Shopify strongly prefers order creation through checkout, not API)
- ❌ Inventory adjustments — use Proxy with `/inventory_levels/adjust.json`
- ❌ Discount codes — use Proxy
- ❌ Draft orders — use Proxy
- ❌ Shopify Functions / App Bridge — out of scope for a backend API

### Shopify-specific auth notes

- **Two app models:**
  - **Custom app** (single store): store owner generates an admin API token and pastes it into Vault. Use `shopify` serviceId.
  - **Public app** (many stores): OAuth install flow from the Shopify App Store. Use `shopify-public-app` serviceId (separate connector).
- **Shop binding:** each connection is bound to one shop (`myshop.myshopify.com`). Multi-shop = multi-connection.
- **Merchant app review (public app only):** if you're a Shopify App Store app, Apideck's Vault app must pass Shopify's review process before install. Existing Apideck customers typically use the custom-app route to avoid the review.

### Common Shopify quirks handled by Apideck

- **GraphQL vs REST** — Shopify is pushing customers to GraphQL. Apideck currently routes through REST Admin API for most endpoints. If you need GraphQL (for large reads, bulk queries), use Proxy with the GraphQL endpoint.
- **Line items on orders** — nested with variant refs. Apideck surfaces as `order.line_items[]` with resolved product/variant names.
- **Order financial_status / fulfillment_status** — Apideck normalizes to `order.payment_status` and `order.status`.
- **Metafields** — exposed as `custom_fields[]`; write access requires additional scopes.
- **Deprecation tracking** — Shopify deprecates API versions twice a year. Apideck tracks the current stable version; raw Proxy calls should pin a version.

### Example: list orders from the last 30 days

```typescript
const since = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();

let cursor;
const orders = [];

do {
  const { data, pagination } = await apideck.ecommerce.orders.list({
    serviceId: "shopify",
    cursor,
    filter: { updated_since: since, status: "any" },
    limit: 100,
  });
  orders.push(...data);
  cursor = pagination?.cursors?.next;
} while (cursor);
```

### Example: create a product

```typescript
const { data } = await apideck.ecommerce.products.create({
  serviceId: "shopify",
  product: {
    name: "Linen Shirt — Navy",
    description_html: "<p>100% European linen. Pre-washed.</p>",
    vendor: "Acme Apparel",
    status: "active",
    variants: [
      {
        sku: "LIN-NVY-S",
        price: 89.0,
        inventory_quantity: 42,
        options: [{ name: "Size", value: "S" }],
      },
      {
        sku: "LIN-NVY-M",
        price: 89.0,
        inventory_quantity: 35,
        options: [{ name: "Size", value: "M" }],
      },
    ],
  },
});
```

### Example: GraphQL bulk query via Proxy

```bash
curl 'https://unify.apideck.com/proxy' \
  -X POST \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: shopify" \
  -H "x-apideck-downstream-url: https://{shop}.myshopify.com/admin/api/2026-01/graphql.json" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ shop { name currencyCode } }"}'
```

## Sibling connectors

Other **Ecommerce** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bigcommerce`](../bigcommerce/) *(beta)*, [`shopify-public-app`](../shopify-public-app/) *(beta)*, [`woocommerce`](../woocommerce/) *(beta)*, [`amazon-seller-central`](../amazon-seller-central/) *(beta)*, [`ebay`](../ebay/) *(beta)*, [`etsy`](../etsy/) *(beta)*, [`magento`](../magento/) *(beta)*, [`bol-com`](../bol-com/) *(beta)*, and 8 more.

## See also

- [Apideck connection guide for Shopify](https://developers.apideck.com/connectors/shopify/docs/consumer+connection)
- [Ecommerce OpenAPI spec](https://specs.apideck.com/ecommerce.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ecommerce)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Shopify official docs](https://shopify.dev/docs/api)
