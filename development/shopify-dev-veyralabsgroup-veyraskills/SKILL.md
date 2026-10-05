---
name: shopify-dev
description: >
  Shopify Developer. Activate when a user is building or modifying a Shopify theme, app, or integration.
  Triggers on: "add a section to my theme", "create a Shopify app", "Shopify CLI", "Liquid template",
  "Storefront API", "Admin API", "checkout extension", "Hydrogen", "Polaris", "shopify theme dev",
  "metafields", "metaobjects", "app blocks", "Online Store 2.0", "section schema".
  Covers theme development, app development, GraphQL APIs, CLI workflows, and extensions.
---

# Shopify Developer Skill

You are a Shopify development expert. You know the full Shopify stack: Liquid, JSON templates, section schemas, the CLI, GraphQL Storefront and Admin APIs, Remix-based app development, Polaris, checkout extensions, and Hydrogen.

Shopify's APIs and Liquid filters change every quarter. Before answering any question involving API versions, GraphQL schema, CLI flags, or new Liquid syntax — fetch current documentation via Context7 first.

```
Use context7 to get: shopify liquid documentation
Use context7 to get: shopify storefront api graphql
Use context7 to get: shopify admin api graphql
Use context7 to get: shopify cli reference
```

---

## Mode Detection

Infer the mode from context. Ask only if genuinely ambiguous.

| Mode | Triggers |
|------|----------|
| `theme` | Liquid, JSON templates, sections, blocks, Dawn, OS 2.0, theme editor |
| `app` | Remix, Polaris, OAuth, webhooks, app extensions, app bridge |
| `api` | GraphQL queries, Storefront API, Admin API, metafields |
| `cli` | `shopify theme`, `shopify app`, deploy, environments, pull/push |
| `hydrogen` | Headless, Remix routes, cache strategies, Storefront API |
| `debug` | Error messages, unexpected behavior, breaking changes |

---

## Phase 1 — Context Fetch

Before writing code, fetch current docs for the relevant area:

```
shopify liquid → for Liquid filters, tags, objects
shopify sections → for section schema, blocks, settings
shopify storefront api → for cart, products, collections queries
shopify admin api → for mutations, webhooks, metafields
shopify cli → for theme/app commands and flags
shopify checkout extensions → for UI extensions, checkout UI
shopify hydrogen → for headless setup, routes, caching
```

Cross-reference with `references/` files for patterns and decisions not covered by docs.

---

## Mode: Theme Development

### JSON Template Structure (OS 2.0)

```json
{
  "sections": {
    "hero": {
      "type": "hero-banner",
      "settings": {}
    }
  },
  "order": ["hero"]
}
```

### Section Schema Pattern

```liquid
{% schema %}
{
  "name": "Section Name",
  "tag": "section",
  "class": "section-name",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Default heading"
    },
    {
      "type": "image_picker",
      "id": "image",
      "label": "Image"
    },
    {
      "type": "select",
      "id": "layout",
      "label": "Layout",
      "options": [
        { "value": "left", "label": "Left" },
        { "value": "right", "label": "Right" }
      ],
      "default": "left"
    }
  ],
  "blocks": [
    {
      "type": "feature",
      "name": "Feature",
      "settings": [
        { "type": "text", "id": "title", "label": "Title" }
      ]
    }
  ],
  "max_blocks": 6,
  "presets": [
    {
      "name": "Section Name"
    }
  ]
}
{% endschema %}
```

### Key Decision Points

**Sections vs Blocks:**
- Section: top-level structural element, configurable in theme editor
- Block: repeatable element within a section (cards, features, tabs)
- Rule: if it repeats, it's a block; if it's a layout region, it's a section

**Metafields vs Metaobjects:**
- Metafield: extra data attached to existing resource (product, collection, page)
- Metaobject: standalone structured content type (team members, testimonials, FAQs)
- Rule: if it belongs TO something → metafield; if it IS something on its own → metaobject

**Section Rendering API:**
Use for partial updates without full page reload:
```javascript
fetch(`?section_id=cart-items`)
  .then(r => r.text())
  .then(html => {
    document.querySelector('#cart-items').innerHTML =
      new DOMParser()
        .parseFromString(html, 'text/html')
        .querySelector('#cart-items').innerHTML;
  });
```

### AJAX Cart Pattern

```javascript
async function addToCart(variantId, quantity = 1) {
  const res = await fetch('/cart/add.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: variantId, quantity }),
  });
  if (!res.ok) throw new Error('Add to cart failed');
  return res.json();
}

async function getCart() {
  return fetch('/cart.js').then(r => r.json());
}

async function updateCart(updates) {
  return fetch('/cart/update.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ updates }),
  }).then(r => r.json());
}
```

---

## Mode: App Development

### Stack (2025+)

New Shopify apps use the **Dev Dashboard** (not Partner Dashboard). All new apps use OAuth client credentials, not static access tokens.

```bash
npm init @shopify/app@latest
# Choose: Remix template
```

### App Structure

```
app/
  routes/
    app._index.tsx          ← main app page
    app.products.tsx        ← products page
    webhooks.tsx            ← webhook handler
  shopify.server.ts         ← Shopify auth + API client
  db.server.ts              ← Prisma DB
```

### Admin API Call in Remix

```typescript
// app/routes/app._index.tsx
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }) => {
  const { admin } = await authenticate.admin(request);

  const response = await admin.graphql(`
    query {
      products(first: 10) {
        nodes {
          id
          title
          status
        }
      }
    }
  `);

  const { data } = await response.json();
  return json({ products: data.products.nodes });
};
```

### Webhook Handler

```typescript
// app/routes/webhooks.tsx
import { authenticate } from "../shopify.server";
import db from "../db.server";

export const action = async ({ request }) => {
  const { topic, shop, session, payload } = await authenticate.webhook(request);

  switch (topic) {
    case "PRODUCTS_UPDATE":
      await db.product.upsert({
        where: { shopifyId: payload.id.toString() },
        update: { title: payload.title },
        create: { shopifyId: payload.id.toString(), title: payload.title, shop },
      });
      break;

    case "APP_UNINSTALLED":
      if (session) await db.session.deleteMany({ where: { shop } });
      break;
  }

  return new Response();
};
```

### Polaris Component Rules

- Always import from `@shopify/polaris`
- Wrap app in `<AppProvider i18n={translations}>` at root
- Use `Page` + `Layout` + `Card` structure for all pages
- `ResourceList` for lists of items, `DataTable` for tabular data
- `useAppBridge` for redirect and toast

---

## Mode: Extensions

### Checkout UI Extension

```typescript
// extensions/checkout-ui/src/Checkout.tsx
import {
  reactExtension,
  useDeliveryGroups,
  Banner,
  BlockStack,
  Text,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => (
  <Extension />
));

function Extension() {
  const deliveryGroups = useDeliveryGroups();

  return (
    <BlockStack>
      <Banner title="Delivery info">
        <Text>Your order ships in 2-3 business days.</Text>
      </Banner>
    </BlockStack>
  );
}
```

Extension targets — common ones:
- `purchase.checkout.block.render` — block anywhere in checkout
- `purchase.checkout.shipping-option-list.render-after` — after shipping options
- `purchase.checkout.payment-method-list.render-after` — after payment methods
- `purchase.thank-you.block.render` — thank you page

---

## Mode: Hydrogen (Headless)

### Route Pattern

```typescript
// app/routes/products.$handle.tsx
import { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { getPaginationVariables } from "@shopify/hydrogen";

export async function loader({ params, context, request }: LoaderFunctionArgs) {
  const { handle } = params;

  const { product } = await context.storefront.query(PRODUCT_QUERY, {
    variables: { handle },
    cache: context.storefront.CacheLong(),  // cache strategy
  });

  if (!product) throw new Response(null, { status: 404 });
  return { product };
}

const PRODUCT_QUERY = `#graphql
  query Product($handle: String!) {
    product(handle: $handle) {
      id
      title
      handle
      description
      priceRange {
        minVariantPrice { amount currencyCode }
      }
      images(first: 10) {
        nodes { id url altText width height }
      }
      variants(first: 100) {
        nodes {
          id
          title
          availableForSale
          price { amount currencyCode }
          selectedOptions { name value }
        }
      }
    }
  }
` as const;
```

### Cache Strategies

```typescript
context.storefront.CacheNone()       // no cache — dynamic, personalized
context.storefront.CacheShort()      // 1min — semi-dynamic (cart, recently viewed)
context.storefront.CacheLong()       // 1hr — mostly static (product pages)
context.storefront.CacheCustom({ maxAge: 3600, staleWhileRevalidate: 82800 })
```

---

## Debug Mode

When debugging Shopify issues, always:

1. Check the API version in `shopify.server.ts` — Shopify deprecates quarterly
2. Verify scopes match what the operation requires
3. Check if the feature requires a specific Shopify plan
4. Look for `userErrors` in mutations — GraphQL returns 200 even on business errors:

```graphql
mutation {
  productUpdate(input: { id: $id, title: $title }) {
    product { id }
    userErrors {       # ← always check this
      field
      message
    }
  }
}
```

5. Theme errors: check the Shopify admin → Themes → Edit code → inspect the error output

---

## Anti-Patterns

**Don't hardcode API versions.** Read from `shopify.server.ts` config and update quarterly.

**Don't use `accessToken` directly in frontend.** Storefront API token is public-safe; Admin API token never goes to client.

**Don't skip `userErrors` in mutations.** GraphQL Admin API returns HTTP 200 even when the operation fails at the business logic level.

**Don't use `window.location` in app routes.** Use `redirect()` from Remix or `useNavigate()`.

**Don't create sections without `presets`.** Without presets, the section won't appear in the theme editor's "Add section" menu.

---

Reference files:
- `references/liquid-patterns.md` — Liquid syntax, filters, objects, gotchas
- `references/graphql-queries.md` — ready-to-use Storefront + Admin API queries
- `references/cli-workflows.md` — CLI commands, environments, deploy flows
- `references/app-architecture.md` — app structure decisions, auth, billing
