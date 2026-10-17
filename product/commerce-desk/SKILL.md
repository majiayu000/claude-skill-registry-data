---
name: commerce-desk
description: WooCommerce store operations through NV oOS Pro — product research, catalog cross-referencing, inventory lookups, and Shopify or Flowhub comparisons where integrations are configured.
---

This skill depends on the Pro and WooCommerce tools being enabled for the
connected assistant. Discover the available tool set from the MCP server first
and adapt; never assume a commerce tool exists.

- **Product research:** `scrape_product_validated` for competitor pages,
  `brave_web_search` for market context.
- **Catalog work:** inspect products with read tools before any bulk update;
  show the user a preview count and ask for confirmation before mutating
  product data.
- **Live inventory:** use connection-aware tools (`flowhub_get_inventory`,
  `flowhub_get_products`, `flowhub_locations`, `flowhub_products`,
  `shopify_catalog`, `shopify_products`, `shopify_orders`,
  `shopify_inventory`) when Remote Sites connections exist.
- **Pricing and stock:** verify against the store before reporting; never
  guess SKUs or quantities.

If a requested operation needs a Pro feature that is not installed on the
site, say so and describe the alternative instead of improvising.
