---
name: shopify-builder
description: 自动化 Shopify 商店的搭建与装饰，支持产品上架、横幅与跑马灯更新以及复活节、黑五等节日主题快速切换，仅需提供店铺域名与 API 凭证即可全自动操作。
title: Shopify建站
example: 用户：“请在我的 Shopify 商店 `my-store.myshopify.com` 上架 5 款宠物用品，并为首页更换黑五促销横幅，同时在顶部公告栏添加‘全场
  5 折’跑马灯。” 技能将自动通过 GraphQL API 完成产品创建、媒体上传、主题文件修改，并确保产品已发布到在线商店销售渠道。
version: 1.0.0
---
# Shopify Builder

This skill provides automated workflows for building and decorating a Shopify store. It leverages the Shopify Admin API (REST and GraphQL) to handle product management, theme assets, and global settings.

## Store Registration & Setup

Before any API work, ensure the merchant has a live store and valid API credentials.

**Access Token (`shpat_*`) — source of truth:** The only supported procedure for obtaining an Access Token (Dev Dashboard, install, client-credentials exchange) is documented in [references/oauth-client-credentials.md](references/oauth-client-credentials.md). **Do not** infer token steps from memory or from fragments elsewhere in this file; **read that reference** whenever you need to acquire or refresh a token.

1. Go to [shopify.com](https://www.shopify.com) → click **Start free trial**.
2. Enter email, set a password, choose a store name and region.
3. Open Admin at `https://[your-store].myshopify.com/admin`.
4. Configure **Settings → Payments**, **Shipping**, and **Domains** as needed.

### Getting API Credentials — Client Credentials OAuth

> **Mandatory — read the reference, not a summary:** To **obtain** an Access Token (`shpat_*`), you **must** read [references/oauth-client-credentials.md](references/oauth-client-credentials.md) **from start to finish**. This SKILL file intentionally omits the step-by-step token flow; **all** concrete steps (app creation, version release, install, credential retrieval, `curl` token exchange, validation, troubleshooting) live only in that reference. If you do **not** already hold a valid `shpat_*`, do **not** create apps, exchange credentials, or call the Admin API until you have read it. Skipping it causes predictable failures (e.g. `shop_not_permitted`, wrong `Content-Type` on token exchange).

Canonical procedure: [references/oauth-client-credentials.md](references/oauth-client-credentials.md).

### Credential Detection Logic

When the user provides credentials, determine how to proceed:

| User provides | Action |
|---|---|
| Store domain + Client ID + Client Secret (`shpss_*`) | **Immediately run token exchange** — Windows: `Invoke-RestMethod` with `client_credentials` grant (see Step 5 of oauth-client-credentials.md)；macOS/Linux: `curl` with `client_credentials` grant. Do NOT ask the user to run this themselves. Do NOT open a browser first — try CLI exchange first, only investigate app installation if it fails with 400. |
| A single `shpat_*` token | Use directly (already an Access Token) |
| Nothing / partial | Ask for the following three values only — do NOT mention `shpat_*` to the user, do NOT ask them to run curl: `store domain (xxx.myshopify.com)`, `Client ID`, `Client Secret (shpss_*)`. Walk them through Dev Dashboard Steps 1–4 to obtain these, then exchange the token yourself. |

**Gate**: Do NOT attempt any API operation until a valid Access Token (`shpat_*`) is confirmed. If the token is missing or uncertain, **stop** and follow [references/oauth-client-credentials.md](references/oauth-client-credentials.md) to obtain it — do not substitute ad-hoc OAuth steps.

## API Execution Rules

**Tool hierarchy (strictly follow this order):**
1. **Shopify GraphQL Admin API** (primary) — use for all reads and writes via `Invoke-RestMethod` (Windows) or `curl` (macOS/Linux) with the Access Token.
2. **Manual click-path instructions** — only for destructive or human-confirmation actions (e.g. deleting billing info).
3. **Browser tool** (fallback) — only if the API returns consistent errors, the action is not exposed via API, or platform restrictions block automation.

**Prefer GraphQL over REST** for all new development. REST endpoints are legacy; use them only when a GraphQL equivalent is unavailable.

**API call pattern — all requests use the exchanged/provided token:**

**Windows（PowerShell）：**
```powershell
# GraphQL
$headers = @{ "X-Shopify-Access-Token" = "{ACCESS_TOKEN}"; "Content-Type" = "application/json" }
$body = '{"query": "...", "variables": {...}}'
Invoke-RestMethod -Uri "https://{STORE_NAME}.myshopify.com/admin/api/2026-01/graphql.json" -Method Post -Headers $headers -Body $body

# REST（legacy, use only when GraphQL unavailable）
$headers = @{ "X-Shopify-Access-Token" = "{ACCESS_TOKEN}" }
Invoke-RestMethod -Uri "https://{STORE_NAME}.myshopify.com/admin/api/2026-01/{resource}.json" -Headers $headers
```

**macOS/Linux（bash）：**
```bash
# GraphQL
curl -s -X POST "https://{STORE_NAME}.myshopify.com/admin/api/2026-01/graphql.json" \
  -H "X-Shopify-Access-Token: {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "...", "variables": {...}}'

# REST（legacy, use only when GraphQL unavailable）
curl -s "https://{STORE_NAME}.myshopify.com/admin/api/2026-01/{resource}.json" \
  -H "X-Shopify-Access-Token: {ACCESS_TOKEN}" \
  -H "Content-Type: application/json"
```

## Instructions

### 1. Supplier contact sourcing (CRITICAL — read first)

**Do not** attempt to find supplier email addresses on Alibaba product or detail URLs. Those pages do **not** expose usable supplier email.

**Primary method — Google search (run in this session; do not spawn a subagent):** For each supplier, search Google with the supplier or company name plus `email`, e.g. `{supplier_or_company_name} email` (quote the name if it helps disambiguate). Open **several** results across the first page(s)—**alibaba.com** listings often still lack a public email, so deliberately check non-Alibaba hits (official site, LinkedIn, trade directories, PDF/catalog pages, contact pages). Extract only **publicly visible** addresses from those pages; do not invent or guess addresses.

**Expectation:** It is **not** required to discover an email for every supplier or SKU. **Partial** coverage is acceptable—proceed with whatever verified contact you can find; do not block the workflow on 100% email coverage.

### 2. Shopify API Validation Protocol (Critical)
For every modification:
1.  **Inspect Response**: Check for `errors` or `userErrors` in the API response — a 200 OK does NOT mean the write succeeded.
2.  **Publication State**: Ensure products are `status: active` and explicitly published to the "Online Store" channel.
3.  **Media Success**: Verify images are correctly assigned after upload.
4.  **Read-Back**: Execute a GET request after any write to verify storefront-facing values.
5.  **API Documentation Fallback**: When a GraphQL schema, field, or endpoint behaviour is uncertain, consult `shopify-dev-mcp` for live documentation lookup before retrying blindly.

### 3. Product Listing Workflow

1.  **Product Data**: Products must come from a prior sourcing stage. If no products have been selected yet, read and follow the `market-insight-product-selection` skill to run sourcing first — do NOT proceed with listing until at least one product with a confirmed supplier URL is available.
2.  **Optimize**: Rewrite descriptions into a structured format (Headline -> 3-5 Benefit Bullets -> Specs -> Care instructions).
3.  **Pricing**: Set retail price (3-5x markup of Landed Cost) and `compare_at_price` (1.5x of retail).
4.  **API Upload (REST)**:
    - **Endpoint**: `POST /admin/api/2026-01/products.json`
    - **Payload**:
      ```json
      {
        "product": {
          "title": "SEO Optimized Title",
          "body_html": "<h3>Headline</h3><ul><li>Feature</li></ul>",
          "vendor": "Brand Name",
          "product_type": "Category",
          "status": "active",
          "images": [{ "src": "https://..." }],
          "options": [{ "name": "Size", "values": ["S", "M"] }],
          "variants": [{ "option1": "S", "price": "39.99", "compare_at_price": "59.99" }]
        }
      }
      ```

### 4. Homepage Hero Banner Deployment
1.  **Generate Asset**: Use `image_generate` (16:9).
2.  **Upload to Shopify Media (GraphQL)**:
    - **Mutation**: `fileCreate`
    - **Query**:
      ```graphql
      mutation fileCreate($files: [FileCreateInput!]!) {
        fileCreate(files: $files) {
          files { id alt ... on MediaImage { image { url } } }
        }
      }
      ```
3.  **Resolve Path**: Extract filename from the returned URL to use the `shopify://shop_images/{filename}` format.
4.  **Update Template**: Use `PUT /admin/api/2026-01/themes/{theme_id}/assets.json` to update `templates/index.json`.

### 5. Seasonal Branding (Easter, BFCM, etc.)
1.  **Global Color Schemes**: Patch `config/settings_data.json` using a Python/JQ script to update hex codes in `color_schemes` (e.g., `scheme-1`, `scheme-6`).
2.  **Announcement Bar**: Update `sections/header-group.json` with the seasonal promo text.
    - **Constraint**: Maintain block IDs; only modify `text` and `link`.

### 6. Marquee (Scrolling Text) Injection
1.  **Section Injection**: Add a block with `type: marquee` to `sections` in `templates/index.json`.
2.  **Update Order**: Add the marquee ID to the `order` array.
3.  **HTML Constraint**: Wrap marquee text blocks in valid HTML tags (e.g., `<p>EASTER SALE IS LIVE!</p>`).


## Store Preview (Password-Protected Stores)

New Shopify stores are locked by default. To preview:
1. Admin → **Online Store → Preferences → Storefront password** — copy the password shown.
2. Open the store URL, click **"Enter using password"**, enter the password.

Always check `password_enabled` in `GET /admin/api/2026-01/shop.json` before screenshotting.


## GraphQL Admin API

Use GraphQL (not REST) for all new development. REST remains available but receives fewer updates.

**Endpoint:**
```
POST https://{store}.myshopify.com/admin/api/2026-01/graphql.json
```

**Headers:**
```json
{
  "X-Shopify-Access-Token": "shpat_...",
  "Content-Type": "application/json"
}
```

**Key mutations for store building:**

Create product:
```graphql
mutation CreateProduct($input: ProductInput!) {
  productCreate(input: $input) {
    product { id title handle }
    userErrors { field message }
  }
}
```

Upload media (banner images, product images):
```graphql
mutation fileCreate($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files { id alt ... on MediaImage { image { url } } }
  }
}
```

Register webhook:
```graphql
mutation CreateWebhook($input: WebhookSubscriptionInput!) {
  webhookSubscriptionCreate(input: $input) {
    webhookSubscription { id topic }
    userErrors { field message }
  }
}
```

**Rate limiting:** 50 cost points/second. Check `X-Shopify-GraphQL-Admin-Api-Call-Limit` header; use exponential backoff on HTTP 429.

**Always check `userErrors`** in every mutation response — a 200 OK does not mean the write succeeded.

Full reference: [references/api-admin.md](references/api-admin.md)

---

## Storefront API

Public GraphQL API for headless storefronts and theme-side data fetching.

**Endpoint:**
```
POST https://{store}.myshopify.com/api/2026-01/graphql.json
```

**Authentication:** `X-Shopify-Storefront-Access-Token: {public_token}` (safe for client-side; cannot access admin or customer PII).

**Key operations:**

Query products (public):
```graphql
query GetProducts($first: Int!) {
  products(first: $first) {
    edges {
      node {
        id title handle description
        priceRange { minVariantPrice { amount currencyCode } }
        images(first: 3) { edges { node { url altText } } }
        variants(first: 10) { edges { node { id title price { amount } availableForSale } } }
      }
    }
  }
}
```

Cart create + add-to-cart mutations are supported via `cartCreate` / `cartLinesAdd`. The Ajax API (`/cart/add.js`, `/cart/change.js`) is the simpler alternative for standard Liquid themes.

Full reference: [references/api-storefront.md](references/api-storefront.md)
