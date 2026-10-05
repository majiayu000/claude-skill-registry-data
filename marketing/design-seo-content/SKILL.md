---
type: Skill
name: design-seo-content
description: Optimize WooCommerce product pages, category pages, and site content for search engines. Covers keyword research, meta tags, product descriptions, schema markup, internal linking, and local SEO. Use when writing product titles/descriptions, conducting keyword research, auditing pages for SEO gaps, setting up internal linking, adding schema markup, or optimizing for local search visibility.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# SEO Content Optimization

Use this skill when writing or optimizing product pages, category pages, or any site content for search engine visibility. Focused on WooCommerce e-commerce SEO.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for content optimisation. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai content` | Search and manage SEO-optimized content |
| `wp mcp-ai bulk` | Batch update meta tags across posts |
| `wp mcp-ai harness` | Semantic search for content gaps |

## When to use this skill

Trigger when ANY of the following is true:

- Writing or revising WooCommerce product titles, descriptions, or meta tags.
- The task asks to "optimize for SEO", "improve search ranking", or "write meta descriptions".
- Conducting keyword research for products or categories.
- Auditing existing product pages for SEO gaps.
- Setting up category page content and descriptions.
- Planning internal linking between products and categories.
- The task mentions "Google ranking", "organic traffic", "product page SEO", or "search visibility".
- Optimizing for local search (Sri Lanka-specific queries).

## Available Tools

| Research Task | Tool Name |
|---|---|
| Keyword research | `web_search_validated`, `brave_web_search` |
| Competitor analysis | `brave_web_search` (search competitor URLs and titles) |
| Site content audit | `search_content` (use `search_type: "hybrid"` for combined keyword + semantic search) |
| Semantic content search | `semantic_content_search` (find related content by meaning) |
| Product data retrieval | `remote_wp_connection` (get live products) |
| Image alt text | `generate_image_alt_text_validated` |
| Post/page creation | `create_post_validated`, `save_post_validated` |

## The WooCommerce SEO Pyramid

```
                        ┌─────────┐
                        │  SALES  │  ← The goal
                        └────┬────┘
                    ┌────────┴────────┐
                    │  CONVERSION UX   │  ← Reviews, trust signals, CTAs
                    └────────┬────────┘
              ┌──────────────┴──────────────┐
              │     ON-PAGE CONTENT          │  ← Descriptions, images, headings
              └──────────────┬──────────────┘
        ┌────────────────────┴────────────────────┐
        │           META & TECHNICAL               │  ← Titles, descriptions, schema, speed
        └────────────────────┬────────────────────┘
  ┌──────────────────────────┴──────────────────────────┐
  │                  KEYWORD FOUNDATION                  │  ← Research, intent, targeting
  └─────────────────────────────────────────────────────┘
```

## Keyword Research

### Keyword Intent Types

| Intent | Query Pattern | Match With |
|---|---|---|
| **Informational** | "what is", "how to", "difference between" | Blog posts, guides |
| **Commercial** | "best", "top", "review", "vs" | Buying guides, comparison pages |
| **Transactional** | "buy", "price", "shop", "order online" | Product pages, category pages |
| **Navigational** | Brand names, store names | Homepage, brand pages |

### Research Process

```
1. SEED KEYWORDS
   Start with product categories and brand names.
   Example: "buy perfume Sri Lanka", "Carolina Herrera price Sri Lanka",
            "luxury fragrance online Sri Lanka", "Swarovski jewelry Colombo"

2. EXPAND WITH SEARCH
   Use web_search_validated to find related queries:
   → "luxury perfume online Sri Lanka"
   → "best perfume for men Sri Lanka"
   → "buy original perfume Sri Lanka online"
   → "perfume shop Colombo delivery"

3. PRIORITIZE BY INTENT + VOLUME
   Transactional > Commercial > Informational
   "buy Carolina Herrera Good Girl Sri Lanka" > "what is eau de parfum"

4. MAP TO PAGES
   Each high-value keyword → specific page
   Each page → 1 primary keyword + 2–3 secondary keywords
```

### Keyword Usage in Page Elements

| Element | Primary Keyword | Secondary Keywords |
|---|---|---|
| **Page title (H1)** | ✅ Must include | ❌ No |
| **Meta title** | ✅ Beginning | ✅ If natural |
| **Meta description** | ✅ Early | ✅ 1–2 |
| **URL slug** | ✅ (3–5 words) | ❌ No |
| **H2 headings** | ❌ (unless natural) | ✅ 1 per H2 |
| **Body copy** | ✅ 1–2 times | ✅ Naturally |
| **Image alt text** | ❌ (describe image) | ✅ If relevant |
| **Image filename** | ✅ (descriptive) | ❌ |

## Product Page SEO (WooCommerce)

### Product Title Optimization

```
FORMAT: [Brand] [Product Name] – [Key Differentiator] ([Size/Volume])

Good: "Carolina Herrera Good Girl Eau de Parfum – 80ml"
Bad:  "Good Girl" (no brand, no type, no size)

Good: "Conatural Lavender & Chamomile Face Wash – 150ml"
Bad:  "CN29" (SKU-only — means nothing to search engines)
```

**Rules:**
- Front-load the most important words (brand + product name)
- Include size/volume for variants
- Include product type (EDP, EDT, face wash, serum)
- 50–70 characters max for meta title display
- Never use ALL CAPS or excessive punctuation

### Meta Description Template

```
FORMAT (155–160 characters):
[Emotional hook / problem]. [Product name] by [brand] — [1–2 key benefits].
[Trust signal]. ✓ [Unique selling point]. Shop online at The Parfumerie.

Example:
"Calm irritated skin with Conatural's Lavender & Chamomile Face Wash — a
sulfate-free, pH-balanced daily cleanser for all skin types. Vegan, halal-
certified & organic. ✓ Islandwide delivery."
```

**Rules:**
- 155–160 characters (longer gets truncated in search results)
- Include primary keyword naturally
- End with a soft CTA or differentiator
- Write for humans first, search engines second
- Every product page MUST have a unique meta description

### Product URL / Permalink

```
FORMAT: /shop/[category]/[brand-product-name]/

Good: /shop/conatural/lavender-chamomile-face-wash-150ml/
Bad:  /shop/product/cn29/
Bad:  /shop/conatural-organic-natural-face-wash-lavender-chamomile-150ml-sulfate-free/
      (keyword-stuffed — looks spammy)
```

**Rules:**
- 3–5 words max after category
- Include brand and product name
- Remove stop words (and, the, for, a)
- Use hyphens between words, never underscores
- Never include SKU or ID numbers
- Set once and never change (or use 301 redirects)

### Product Description SEO (Long Description)

The long description serves both conversion AND SEO:

```
STRUCTURE:
  <h2>Primary benefit or emotional hook</h2>
    ← Contains secondary keywords
  <p>Contextual opening — connect to customer needs</p>
    ← Natural keyword placement

  <h3>Why You'll Love It</h3>
  <ul>
    <li><strong>Feature</strong> — Benefit to you</li>
    ← Each line is a scannable value proposition
  </ul>

  <h3>Ingredients / Specifications</h3>
    ← Rich, specific details (search engines reward depth)

  <h3>How to Use</h3>
    ← Practical, helpful content (increases dwell time)
```

**Rules:**
- Minimum 300 words for product pages (SEO best practice)
- Use H2 and H3 headings with secondary keywords
- Break text into scannable chunks (bullets, short paragraphs)
- Include specifications, ingredients, dimensions — search engines love structured data
- Don't copy manufacturer descriptions verbatim (duplicate content penalty)
- Write unique descriptions for every product variant

### Image SEO

```
File name:    carolina-herrera-good-girl-edp-80ml-bottle.jpg
              (not: IMG_4829.jpg or product-shot-final-v2.jpg)

Alt text:     "Carolina Herrera Good Girl Eau de Parfum 80ml stiletto-shaped
              bottle on marble surface"
              → Use generate_image_alt_text_validated (MCP)

Caption:      Optional — visible below image in some themes.
              Keep to one line if used.
```

## Category Page SEO

Category pages are high-value SEO real estate. They often rank for high-volume commercial keywords like "buy perfume online Sri Lanka."

### Category Title & Meta

```
Title: [Category Name] – Buy Online Sri Lanka | The Parfumerie

Meta: "Shop premium [category] online at The Parfumerie. ✓ 100% authentic
       [sub-categories]. Islandwide delivery, complimentary gift wrapping.
       Browse our collection today."

Example:
Title: "Luxury Fragrances – Buy Perfume Online Sri Lanka | The Parfumerie"
Meta:  "Discover authentic luxury fragrances at The Parfumerie. Shop Carolina
       Herrera, Prada, Givenchy & more. ✓ Islandwide delivery. ✓ Free gift
       wrapping. Browse our perfume collection."
```

### Category Description

Place a 150–300 word description at the **top** of the category page (before products) and a shorter version at the bottom:

```
TOP (SEO-rich, 150–300 words):
  H1: Category name
  P:  Overview — what's in this category, who it's for, why shop here
  P:  Sub-category links (internal linking!)
  P:  Trust signals — authenticity, delivery, service

BOTTOM (Short, 50–100 words):
  P:  Call to action — "Browse our full range of ___"
  Optional FAQ: "How to choose a fragrance?" (accordion, good for SEO)
```

## Content Strategy for SEO

Beyond product and category pages, build topical authority with supporting content:

| Content Type | Purpose | Keywords Targeted |
|---|---|---|
| **Buying Guides** | Capture commercial intent | "best perfume for", "how to choose" |
| **Brand Spotlights** | Brand-name search traffic | "[Brand] Sri Lanka", "[Brand] collection" |
| **Gifting Guides** | Seasonal + gifting intent | "gifts for her Sri Lanka", "Valentine's gift" |
| **How-To Articles** | Informational traffic | "how to apply perfume", "fragrance layering" |
| **Comparison Posts** | Decision-making queries | "EDP vs EDT", "[Product A] vs [Product B]" |
| **Local Content** | Sri Lanka searches | "perfume shop Colombo", "luxury shopping Sri Lanka" |

### Blog Post SEO Checklist

```
- [ ] Target keyword in title (H1)
- [ ] Target keyword in first 100 words
- [ ] Target keyword in at least one H2
- [ ] Meta description written (155–160 chars)
- [ ] URL slug = 3–5 words, includes keyword
- [ ] Internal links to 2–3 product/category pages
- [ ] External link to 1 authoritative source
- [ ] Images have descriptive filenames + alt text
- [ ] Post is 800+ words (depth signals quality)
- [ ] Category and tags assigned
```

## Internal Linking Strategy

Internal links distribute authority across your site:

```
Category Pages ←→ Product Pages
       ↑               ↑
       └── Blog Posts ──┘

Rules:
  ● Every product page links to its parent category
  ● Category pages link to 3–5 featured products
  ● Blog posts link to 2–3 relevant products or categories
  ● Related products section links within the same category
  ● Breadcrumbs on every page (good for SEO + UX)
  ● Never use "click here" as anchor text — use descriptive text
```

### Anchor Text Examples

```
BAD:  "Click here to see our Carolina Herrera collection"
GOOD: "Browse our Carolina Herrera fragrance collection"

BAD:  "Buy now"
GOOD: "Shop Carolina Herrera Good Girl — 80ml EDP"
```

## Local SEO (Sri Lanka)

Optimize for local search queries:

```
Key local keywords to target:
  ● "perfume shop Sri Lanka"
  ● "buy perfume online Sri Lanka"
  ● "luxury fragrance Colombo"
  ● "perfume delivery Sri Lanka"
  ● "[Brand] Sri Lanka" (for every brand carried)
  ● "gift delivery Sri Lanka"
  ● "online perfume shop Sri Lanka islandwide delivery"
```

### Local SEO Checklist

- [ ] NAP (Name, Address, Phone) consistent across site
- [ ] Google Maps link on Contact page
- [ ] "Sri Lanka", "Colombo", "islandwide" in key meta descriptions
- [ ] Delivery areas listed (city names = local keywords)
- [ ] Google My Business profile claimed and optimized
- [ ] Sri Lankan English spelling and terminology (not US/UK specific)
- [ ] Local currency (LKR) prominently displayed
- [ ] Local phone numbers and WhatsApp contact

## Technical SEO Checklist

```
PER PRODUCT PAGE:
  ✅ Unique meta title
  ✅ Unique meta description
  ✅ Canonical URL set
  ✅ Open Graph (og:title, og:image, og:description) for social sharing
  ✅ Product schema markup (price, availability, rating)
  ✅ Breadcrumb schema markup
  ✅ Image alt text on ALL product images
  ✅ Descriptive image filenames
  ✅ H1 = product title (only one H1 per page)
  ✅ H2/H3 for section headings (not styled text)

SITE-WIDE:
  ✅ XML sitemap submitted to Google Search Console
  ✅ robots.txt not blocking important pages
  ✅ SSL certificate active (HTTPS everywhere)
  ✅ Mobile-responsive (Google Mobile-First Index)
  ✅ Fast load times (optimize images — see design-image-optimization)
  ✅ No broken internal links
  ✅ Pagination handled correctly (rel="next" / rel="prev")
```

## Product Schema Markup (WooCommerce)

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Carolina Herrera Good Girl Eau de Parfum – 80ml",
  "image": "https://theparfumerie.lk/wp-content/uploads/...jpg",
  "description": "Luxury eau de parfum with notes of...",
  "sku": "CH-GG-EDP-80",
  "brand": {
    "@type": "Brand",
    "name": "Carolina Herrera"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://theparfumerie.lk/shop/carolina-herrera/good-girl-edp-80ml/",
    "priceCurrency": "LKR",
    "price": "27500",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
```

Most WooCommerce themes handle basic schema. Verify with Google's Rich Results Test that price, availability, and rating show correctly.

## Common Mistakes

```
WRONG:
  ● Product title = "Good Girl" (no brand, no type, no size)
  ● Meta description = blank or auto-generated (missed opportunity)
  ● Same meta description across 50 products (duplicate content)
  ● Image filenames = IMG_4829.jpg (zero SEO value)
  ● Copy-pasting manufacturer's product description (duplicate)
  ● Keyword stuffing: "buy perfume, perfume Sri Lanka, best perfume,
    cheap perfume, luxury perfume, perfume online..."
  ● Missing alt text on product images (accessibility + SEO fail)
  ● No internal links between related products
  ● Category pages with zero descriptive content

RIGHT:
  ✅ "Carolina Herrera Good Girl Eau de Parfum – 80ml"
  ✅ Unique meta description per product (written, not generated)
  ✅ Descriptive filenames: carolina-herrera-good-girl-80ml.jpg
  ✅ Original product descriptions (300+ words, unique)
  ✅ Natural keyword placement (1–2 primary, 2–3 secondary)
  ✅ Alt text on every image via generate_image_alt_text_validated
  ✅ Internal links: related products, parent category, blog posts
  ✅ Category pages with 150–300 word descriptions
```

## Critical Rules

- **One primary keyword per page** — target one main search query per product or category page.
- **Unique meta for every page** — no duplicates, no auto-generation, write every description.
- **300+ words on product pages** — thin content doesn't rank. Add depth with ingredients, usage, brand story.
- **Descriptive image filenames + alt text** — use `generate_image_alt_text_validated` for alt text. Rename files before uploading.
- **Internal links are free SEO** — every product links to its category, related products, and at least one blog post.
- **Write for humans, optimize for search** — readable, helpful content ranks better than keyword-stuffed spam.
- **Sri Lanka keywords in key positions** — "Sri Lanka", "islandwide delivery", "Colombo" where relevant.
- **Don't change URLs** — permalinks are permanent. If you must change, use 301 redirects.

## What This Skill Does NOT Cover

- Technical server-side SEO (caching, CDN, SSL configuration)
- Backlink building and off-page SEO strategies
- Google Search Console or Analytics setup and configuration
- Image file-size optimization and format conversion → `design-image-optimization`
- Social media SEO and platform-specific ranking → `design-social-content`
- Rank Math / Yoast plugin configuration and settings
- Paid search (Google Ads) campaign management

## Cross-references

- Run **`design-product-research`** to gather product information before writing SEO copy.
- Run **`design-image-optimization`** to create properly named, optimized images — use `resize_image` (MCP).
- Run **`design-content-calendar`** to schedule blog posts and buying guides that support SEO.
- Run **`design-social-content`** to repurpose SEO content for social media.
- Run **`design-brand-kit`** to ensure consistent brand naming and terminology across all pages.
- Use **`generate_image_alt_text_validated`** (MCP) for alt text on every product image.
- Use **`web_search_validated`** for keyword research and competitor title analysis.
