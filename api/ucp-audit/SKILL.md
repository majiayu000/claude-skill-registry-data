---
name: ucp-audit
description: >
  Scans a merchant website and produces a UCP readiness report.
  Checks for existing structured data, payment providers, platform type,
  and /.well-known/ucp presence. Outputs a scored diagnostic with
  actionable fix list. Use when a merchant wants to know how ready
  they are for AI commerce integration.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch
---

# UCP Audit — Merchant Readiness Scanner

Scan a merchant's website and produce a UCP readiness report with a 0-100 score, asset inventory, gap analysis, and recommended integration path.

## Prerequisites
- Python 3.10+ with requests, beautifulsoup4
- Merchant URL must be publicly accessible

## Step 1: Check UCP Profile

1.1. Fetch `{merchant_url}/.well-known/ucp`
- If exists: parse JSON, validate against profile schema, record capabilities found
- If 404: record as "no UCP profile" (this is expected for most merchants)
- If malformed JSON: record as "broken UCP profile"

1.2. Record:
- `has_ucp_profile`: boolean
- `ucp_capabilities`: list of capability names (if profile exists)
- `ucp_version`: version string (if profile exists)
- `profile_errors`: list of validation errors (if any)

## Step 2: Detect Platform

2.1. Check response headers and HTML for platform signatures:

| Platform | Detection Method |
|----------|-----------------|
| Shopify | `x-shopify-stage` header, `/cdn.shopify.com/` in HTML, `Shopify.theme` in JS |
| WooCommerce | `wc-ajax` in HTML, `woocommerce` in body class, `/wp-content/plugins/woocommerce/` |
| Magento | `mage/` in scripts, `Magento_` in HTML comments |
| BigCommerce | `bigcommerce.com` in scripts, `data-content-region` attributes |
| Custom | None of the above detected |

2.2. Record: `platform`, `platform_confidence` (high/medium/low)

## Step 3: Inventory Existing Structured Data

3.1. Parse homepage + 2-3 product pages for:
- **JSON-LD** (`<script type="application/ld+json">`) — look for `@type: Product`, `Offer`, `Organization`
- **Open Graph** (`og:*` meta tags) — title, description, image, price
- **Schema.org microdata** (`itemscope`, `itemprop` attributes)
- **Meta tags** — `product:price:amount`, `product:price:currency`

3.2. For each product page, extract what's already available:
- Product title → maps to UCP `title`
- Price → maps to UCP `price.amount` (note currency and whether minor units)
- Description → maps to UCP `description.plain`
- Images → maps to UCP `media[]`
- SKU → maps to UCP `variants[].sku`
- Availability → maps to UCP `variants[].availability`
- Categories → maps to UCP `categories[]`

3.3. Record:
- `structured_data_types`: list of found types (json-ld, opengraph, microdata)
- `product_fields_available`: dict of {ucp_field: source_field}
- `product_fields_missing`: list of UCP required fields with no source
- `sample_products`: 2-3 parsed product examples

## Step 4: Detect Payment Methods

4.1. Scan for payment provider signatures:

| Provider | Detection |
|----------|-----------|
| Stripe | `js.stripe.com`, `stripe.com/v3` in scripts |
| PayPal | `paypal.com/sdk` in scripts |
| Adyen | `adyen.com` in scripts, `adyen` in form actions |
| Square | `squareup.com`, `square.com` in scripts |
| Braintree | `braintreegateway.com` in scripts |
| Klarna | `klarna.com` in scripts |

4.2. Record:
- `payment_providers`: list of detected providers
- `ucp_payment_handler_ready`: boolean (true if Stripe/Adyen/Square detected — these have known UCP payment handler specs)

## Step 5: Check API Accessibility

5.1. If platform detected, probe for existing API:
- Shopify: `{url}/products.json` (public storefront API)
- WooCommerce: `{url}/wp-json/wc/v3/` (needs auth but check if endpoint exists)

5.2. Record:
- `has_public_api`: boolean
- `api_type`: string (storefront, rest, graphql, none)

## Step 6: Calculate Score & Generate Report

Scoring rubric (100 points total):

| Check | Points | Condition |
|-------|--------|-----------|
| UCP profile exists | 20 | /.well-known/ucp returns valid JSON |
| UCP profile has checkout capability | 10 | dev.ucp.shopping.checkout in capabilities |
| UCP profile has catalog capability | 10 | dev.ucp.shopping.catalog in capabilities |
| Structured product data exists | 15 | JSON-LD or microdata with Product type |
| All required product fields available | 10 | title + price + description + at least 1 image |
| Payment provider detected | 15 | At least one known provider |
| UCP-compatible payment provider | 5 | Stripe, Adyen, or Square specifically |
| Public product API available | 10 | Storefront API or REST API accessible |
| HTTPS enabled | 5 | Site loads over HTTPS |

### Output Contract

Save to `store/clients/{client_name}/`:

- `audit-report.md` - human-readable readiness report
- `audit.json` - machine-readable observations and score

Markdown report format:

```markdown
# UCP Readiness Audit — {merchant_name}

**URL:** {url}
**Date:** {date}
**Score:** {score}/100

## Summary
{1-2 sentence assessment}

## Platform
- **Detected:** {platform} ({confidence})
- **Payment:** {providers}

## What You Already Have (Reusable Assets)
{table of existing data that maps to UCP fields}

## What's Missing
{numbered list of gaps, ordered by impact}

## Recommended Integration Path
{step-by-step plan based on platform + gaps}

## Estimated Effort
- Profile setup: {estimate}
- Catalog mapping: {estimate}
- Checkout API: {estimate}
- Total: {estimate}
```

> **HARD RULE — Never fabricate data.** If a check fails or returns ambiguous results, report it as "inconclusive" with the raw observation. Do not guess platform type or payment provider.

## Scripts

| Script | Purpose | Dependencies |
|--------|---------|-------------|
| `audit_site.py` | Main audit runner | requests, beautifulsoup4, json, re |

## Collaboration

```
ucp-audit (this skill)
    │
    ├── outputs → store/clients/{name}/audit-report.md
    │
    ├── consumed by → ucp-profile (reads platform + payment info)
    └── consumed by → ucp-catalog (reads product field mapping)
```
