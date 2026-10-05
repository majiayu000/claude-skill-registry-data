---
type: Skill
name: design-product-research
description: Research products via AI tools, cross-reference live stock, generate WooCommerce-ready copy, and extract marketing angles. Covers the full research-to-copy pipeline with remote_wp_connection stock checks and paper_store persistence. Use when researching products by SKU/name/category, generating WooCommerce descriptions, preparing product data for campaigns, or cross-referencing catalog files against live inventory.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Product Research & Copy Generation

Use this skill when researching products, generating WooCommerce descriptions, or preparing marketing-ready product data for e-commerce.

## MCP Tool Discovery

The plugin provides research and product tools that may be agent-prefixed or bare. Always check your tool list for the correct names:

```
Pattern: nv_oos_{AGENT_NAME}_agent_{TOOL_NAME}
Example: nv_oos_sophie_agent_web_search_validated
         research_product  (bare — usually registered as-is)
```

| Research Task | Tool Name |
|---|---|
| Deep product research | `research_product` |
| Broad topic research | `deep_research` |
| Quick web search | `web_search_validated` or `brave_web_search` |
| Product price lookup | `lookup_product_price` |
| Live stock check | `remote_wp_connection` (action: `get_wc_products`) |
| Product catalog search | `woo_products` |
| Persist findings (on request) | `paper_store_write` / `paper_store_read` |
| Content search (site) | `nv_oos_*_agent_search_content_validated` |

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for product research. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai harness` | Semantic search across product catalogs |
| `wp mcp-ai content` | Search existing product content |
| `wp ezuite low-stock-report` | ERP inventory research |

## When to use this skill

Trigger when ANY of the following is true:

- Researching a specific product by SKU, name, or category.
- The task asks to "find out about", "research", or "look up" a product.
- Generating WooCommerce product copy (title, short description, long description).
- Cross-referencing stock levels between a catalog file and the live website.
- Preparing product data for marketing campaigns or content creation.
- The task mentions "product research", "WooCommerce copy", or "product page content".
- Building a product knowledge base for later reference.

## Product Data Retrieval Priority

Always follow this order when looking up product details:

```
Step 1: remote_wp_connection → get_wc_products (live stock, current price)
        └─ Check instock items from the website WooCommerce API

Step 2: Product catalog file (if available — e.g., Products_Export_Converted.json)
        └─ Main source for title, categories, SKU, size, price, permalink

Step 3: research_product — structured product research
        └─ Fill gaps: product descriptions, ingredients, specifications, market context
        └─ For broader brand or market research, see design-deep-research and design-web-research
```

**Cross-check rule:** Always verify Step 1 vs Step 2 before making recommendations. If a product is in the catalog but not on the live site, flag it as "not yet published."

## Research Tool Selection

### `research_product` — Best for single products

Use when you have a specific product to research. Provides structured data: title, description, specifications, pricing, images, SEO keywords, and source URLs.

```
Parameters:
  query           — Product name/brand (required)
  depth           — "basic", "standard", "comprehensive" (default: "standard")
  focus_areas     — Specific aspects: ["specifications", "reviews", "pricing", "alternatives"]
  include_pricing — Include pricing info (default: true)
  include_images  — Include image URLs (default: true)
  include_specs   — Include specs and attributes (default: true)
```

**Example:**
```
query: "Conatural Lavender and Chamomile Face Wash 150ml"
depth: "standard"
include_pricing: true
include_specs: true
include_images: true
```



Use when you need to find current market prices across retailers. Supports image recognition, document parsing, and URL comparison.

## Cross-Referencing Live Stock

Use `remote_wp_connection` to verify product availability on the live site:

```
1. List connections:
   remote_wp_connection { action: "list_connections" }
   → Find the connection ID for the target site

2. Check by SKU:
   remote_wp_connection {
     connection_id: "conn_8srcad8zylhe",
     action: "get_wc_products",
     sku: "CN29"
   }

3. Check by search:
   remote_wp_connection {
     connection_id: "conn_8srcad8zylhe",
     action: "get_wc_products",
     search: "Lavender Chamomile",
     per_page: 10
   }

4. Check by category:
   remote_wp_connection {
     connection_id: "conn_8srcad8zylhe",
     action: "get_wc_products",
     category: "conatural",
     per_page: 20
   }
```

**Key fields from live products:** `id`, `name`, `permalink`, `price`, `stock_status`, `stock_quantity`, `categories`, `type`, `status`.

## Generating WooCommerce Copy

### Short Description Formula

The short description should hook, inform, and sell in 2–3 sentences:

```
[Hook — emotional or problem-aware opening]
[Value — what it does and who it's for, with key differentiators]
[Trust signals — certifications, free-from claims, guarantees]
[Availability — delivery/shipping note]
```

**Example:**
```
A soothing, sulfate-free daily cleanser infused with calming lavender and
chamomile — crafted for skin that deserves a moment of calm. This gentle,
pH-balanced gel face wash cleanses without stripping, perfect for sensitive
or combination skin. 100% SLS-free, paraben-free & vegan. Cruelty-free &
halal-certified. Available with islandwide delivery.
```

### Long Description Structure

```
<h2>Emotional/aspirational headline</h2>
<p>Contextual opening — connect to customer's life/needs</p>

<h3>Key Benefits (Why)</h3>
<ul>
  <li>Feature → Benefit for the customer</li>
  <li>Feature → Benefit for the customer</li>
</ul>

<h3>Brand/Product Values (Trust)</h3>
<ul>
  <li>Certifications, ethical claims, manufacturing standards</li>
</ul>

<h3>How to Use</h3>
<ol>
  <li>Step-by-step instructions</li>
</ol>

<h3>Store/Service Promise</h3>
<ul>
  <li>Delivery, gift wrapping, authenticity guarantees</li>
</ul>
```

### Product Meta Checklist

| Field | Required? | Source |
|---|---|---|
| Title | ✅ Yes | Catalog file or research |
| Regular Price | ✅ Yes | Catalog file or live site |
| SKU | ✅ Yes | Catalog file |
| Categories | ✅ Yes | Catalog file |
| Tags | Recommended | Research + keyword extraction |
| Brand attribute | Recommended | Research |
| Stock quantity | ✅ Yes | Live site (most current) |
| Permalink | ✅ Yes | Catalog file |
| Short Description | ✅ Yes | Generated from research |
| Long Description | ✅ Yes | Generated from research |

## Marketing Angle Extraction

After research, extract marketable hooks from the product data:

1. **Scarcity/urgency** — Is stock low? "Only X units available"
2. **Local relevance** — How does this fit the target market? (climate, culture, lifestyle)
3. **Price positioning** — Affordable luxury? Premium? Entry-level?
4. **Differentiators** — Certifications, ingredients, ethical claims, exclusivity
5. **Seasonal fit** — Does this align with current campaigns or weather?
6. **Cross-sell opportunities** — What else in the catalog complements this?

Organize findings into:
- **Key selling points** (bullet list for ad copy)
- **Marketing angles** (thematic hooks for campaigns)
- **Content formats** (Reel, static post, story, carousel)

## Paper Store Integration (on request only)

When explicitly asked to save research, use `paper_store_write`. To target
a specific WordPress site, pass `connection_id` (discover IDs via
`remote_wp_connection` with action `"list_connections"`):

```
paper_store_write {
  collection: "product-research"
  id: "sku-XXX-product-slug"
  title: "SKU — Product Name (Full Research)"
  connection_id: "conn_8srcad8zylhe"  ← Target specific site
  ...
}
```

Without `connection_id`, the operation defaults to the local WordPress site.
Use `paper_store_read` and `paper_store_list` with `connection_id` to
retrieve prior research from the correct site.

## Source Citation

Always track where information came from:

| Source Type | Examples |
|---|---|
| **Manufacturer** | Brand's official product page |
| **Retailer** | Other stores carrying the product |
| **Live API** | WooCommerce API response from the site |
| **Catalog file** | Products_Export_Converted.json |

Cite URLs and retrieval dates. Flag data that may be stale (e.g., "stock levels from catalog file — live updates not reflected").

## Critical Rules

- **Live stock beats catalog data** — always verify with `remote_wp_connection` first.
- **Only recommend in-stock products** — flag out-of-stock items clearly.
- **Link to product permalinks** — use the `Permalink` column from the catalog file or the live site URL.
- **Match brand/category to sitemap** — only reference brands in the approved brand list.
- **Use proper URL formats** — luxury brands use `/luxury/{category}/{brand}/` format.
- **No cash on delivery** — don't mention COD in copy.
- **Store research when asked** — paper_store is for explicit persistence requests, not automatic saves.
- **Be transparent about data freshness** — note when catalog data may be outdated vs live API data.

## Common Mistakes

```
WRONG:
- Recommending a product that's out of stock on the live site
- Using catalog permalink when product isn't published yet
- Including cash on delivery in copy
- Referencing brands not in the approved brand list
- Using manufacturer's international pricing instead of local price
- Saving to paper_store without being asked

RIGHT:
- Cross-checking stock via remote_wp_connection before any recommendation
- Flagging "not yet live on website" for unpublished products
- Using local pricing and Sri Lanka-specific context
- Citing sources with URLs and retrieval dates
- Presenting copy in the brand's established tone of voice
- Only persisting to paper_store when the user explicitly requests it
```

## What This Skill Does NOT Cover

- Deep multi-source market or brand research → `design-deep-research`
- Creating WordPress post drafts from research → `design-content-research`
- Image generation for products → `design-image-generation`
- Pricing strategy, margin analysis, or financial modeling
- Inventory management beyond stock-level checks
- EZuite ERP operations → `ezuite_erp` / `ezuite_erp_get_products`
- Social media content writing from product data → `design-social-content`

## Cross-references

- Run **`design-content-calendar`** to schedule product launch content.
- Run **`design-social-content`** to create social posts from product research.
- Run **`design-image-generation`** to create product visuals — check your tool list for the Gemini image tool.
- Run **`design-brand-kit`** to ensure product copy aligns with brand guidelines.
- Run **`design-campaign-orchestration`** to integrate product launches into monthly campaigns.
- Run **`design-deep-research`** for broader brand or market research — use `deep_research`.
- Run **`design-web-research`** for quick fact checks and trend lookups — use `web_search`.
- Run **`design-content-research`** to convert product research into WordPress drafts.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` documentation.
