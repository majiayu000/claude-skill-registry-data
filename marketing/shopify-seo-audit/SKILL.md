---
name: shopify-seo-audit
description: AI 驱动的 Shopify 店铺 SEO 诊断技能，审计产品页、集合页等页面的元标签、内容深度、图片优化、重复内容、结构化数据及 Core
  Web Vitals 影响因子，输出按影响排序的优先级修复清单。
allowed-tools: Bash
metadata:
  manai:
    homepage: https://github.com/mguozhen/shopify-seo-audit
title: Shopify SEO审计
example: |-
  执行命令 `seo audit`，然后提供需要审计的页面地址或店铺描述，例如：
  ```
  https://yourstore.com/products/handmade-ceramic-mug
  https://yourstore.com/collections/kitchenware
  ```
  或者直接说明“店铺有 200 个产品、12 个集合，使用 Dawn 主题，安装了 9 个 App”，即可获得包含 SEO 健康评分、关键问题、高影响修复项和逐页备注的完整审计报告。
version: 1.0.0
---
# Shopify SEO Audit

AI-powered Shopify SEO audit agent — identifies on-page issues, Shopify-specific technical problems, thin content, and structured data gaps, then delivers a prioritized fix list organized by impact.

Paste your product page URLs, collection page content, meta tags, image data, or describe your store setup. The agent runs through a comprehensive checklist and returns issues ranked by SEO impact — not just a list of problems, but a clear action queue.

## Commands

```
seo audit                          # full store SEO audit (paste URLs, content, or describe setup)
seo product pages                  # audit product pages for content depth and on-page signals
seo collections                    # audit collection pages for SEO structure and duplicate issues
seo meta check                     # check meta titles and descriptions across provided pages
seo images                         # audit image alt text, file names, and size signals
seo speed                          # assess page speed signals and Core Web Vitals impact factors
seo internal links                 # check internal link structure and anchor text patterns
seo score                          # generate overall SEO health score with per-category breakdown
seo fix list                       # output prioritized fix list sorted by estimated impact
seo save                           # save audit results to ~/shopify-seo/
```

## What Data to Provide

The agent works with:
- **URLs** — paste product page, collection page, or home page URLs
- **Source HTML or content** — paste page source, meta tags, or product descriptions
- **GA4 / Search Console data** — paste crawl errors, page performance, or coverage reports
- **Product descriptions** — paste text for depth and uniqueness analysis
- **Image data** — file names, alt text, sizes if known
- **Store description** — "I have 120 products in 8 collections, using Dawn theme, 12 apps installed"

No Shopify API access required. Works from pasted data and verbal descriptions.

## Workspace

Creates `~/shopify-seo/` containing:
- `memory.md` — saved store profile, theme, and past audit findings
- `audits/` — audit reports saved as markdown (audit-YYYY-MM-DD.md)
- `fix-queue.md` — running prioritized fix list updated across sessions

## Analysis Framework

### 1. On-Page Checklist

**Meta Title**
- Optimal length: 50-60 characters (truncated in Google SERPs beyond 60)
- Must contain primary keyword, ideally near the start
- Unique across all pages — no duplicate titles
- Format recommendation: Primary Keyword - Product Name | Brand Name

**Meta Description**
- Optimal length: 150-160 characters
- Must include primary keyword and a call to action
- Not a ranking factor but directly impacts click-through rate from SERPs
- Unique per page — duplicate descriptions signal thin content

**H1 Tag**
- One H1 per page only — multiple H1s dilute signal
- Must match or closely match the meta title keyword
- Shopify default: product title becomes H1 — verify theme is not overriding this

**Keyword in Title, Description, and Body**
- Primary keyword should appear: in title, in first 100 words, in at least one H2, and naturally throughout body
- Keyword stuffing (more than 3-4% density) is a negative signal — flag if present

### 2. Shopify-Specific Technical Issues

**Duplicate URL Patterns**
- Shopify generates both `/products/product-slug` and `/collections/collection-name/products/product-slug`
- The collection-scoped URL is a duplicate unless properly canonicalized
- Verify canonical tags point to `/products/` URL as the canonical version

**Pagination Canonicals**
- Collection pages with pagination (?page=2, ?page=3) must use canonical tags pointing to page 1
- Or use rel="next" / rel="prev" pagination signals (older approach, still valid)
- Missing canonicals on paginated collection pages causes duplicate content indexing

**Theme Bloat from Unused Apps**
- Each installed Shopify app may inject CSS and JavaScript on every page load
- Unused apps that still load scripts are a Core Web Vitals liability
- Flag when more than 8 apps are installed — audit which apps load globally vs. on specific pages

**Default Shopify URLs that Cannot Be Changed**
- `/collections/`, `/products/`, `/pages/`, `/blogs/` prefixes are fixed — do not attempt to remove
- Focus SEO effort on the slug portion (after the prefix) — this is controllable

### 3. Product Page Content Depth

**Word Count**
- Minimum: 300 words of unique body content per product page
- Under 300 words is classified as thin content by most SEO tools
- Manufacturer copy (identical text across multiple sellers) is treated as duplicate content

**Unique Descriptions**
- Never use manufacturer-provided product descriptions verbatim
- Rewrite descriptions with buyer-intent language, use-case details, and category-specific keywords
- Add FAQs, size guides, care instructions, or comparison tables to boost depth

**Variant Pages**
- Shopify creates separate URLs for product variants by default in some themes
- Audit whether variant URLs are indexable and whether they have unique content
- If variants lack unique content, canonicalize to the main product URL

### 4. Image Optimization

**Alt Text**
- Every product image must have descriptive alt text containing the primary keyword naturally
- Format: "[Keyword] - [Product Name] - [Key Feature or Color]"
- Empty alt text is an indexability miss; decorative images should use alt=""

**File Names**
- Rename before uploading: `red-ceramic-coffee-mug-12oz.jpg` not `IMG_4821.jpg`
- Shopify preserves the original filename in the CDN URL — this is a minor ranking signal

**File Size**
- Target: under 500KB per image; under 200KB is ideal for Core Web Vitals
- Use WebP format when possible (Shopify supports WebP delivery via CDN)
- Large images are the most common cause of poor Largest Contentful Paint (LCP) scores

### 5. Core Web Vitals Impact on Rankings

Google uses Core Web Vitals as a ranking signal. Shopify-specific factors that affect scores:

**Largest Contentful Paint (LCP) — target under 2.5 seconds**
- Hero image size is the primary LCP element on most product pages
- Third-party app scripts that block rendering delay LCP

**Cumulative Layout Shift (CLS) — target under 0.1**
- Images without explicit width/height attributes cause layout shift
- Shopify review apps loading asynchronously commonly cause CLS

**Interaction to Next Paint (INP) — target under 200ms**
- Excessive JavaScript from apps increases INP
- Audit app script load with Google PageSpeed Insights on key pages

### 6. Structured Data (Schema Markup)

**Product Schema**
- Must include: name, description, image, price, currency, availability, brand
- Strongly recommended: aggregateRating (average rating + review count), sku, gtin
- Shopify themes include basic Product schema by default — verify it is populated correctly

**BreadcrumbList Schema**
- Helps Google understand collection hierarchy
- Verify breadcrumb schema matches visible breadcrumb navigation on page

**Organization Schema**
- Include on homepage: name, url, logo, contactPoint, sameAs (social profiles)
- Not a direct ranking factor but improves Knowledge Panel eligibility

## Output Format

Every `seo audit` outputs:
1. **SEO Health Score** — overall score /100 with per-category breakdown (on-page, technical, content, images, structured data)
2. **Critical Issues** — items causing active ranking suppression (fix immediately)
3. **High-Impact Fixes** — issues with significant ranking upside (fix within 30 days)
4. **Quick Wins** — low-effort, moderate-impact improvements (fix this week)
5. **Shopify-Specific Issues** — duplicate URL, canonical, and theme issues
6. **Prioritized Fix List** — numbered action queue ordered by estimated impact
7. **Page-by-Page Notes** — per-URL findings when multiple URLs are provided

## Rules

1. Always distinguish between Shopify platform constraints (cannot change) and configurable issues (can fix) before recommending changes
2. Never flag the `/products/` or `/collections/` URL prefix as an SEO issue — these are Shopify defaults and cannot be removed
3. Score each audit category independently — do not let one strong area mask weaknesses in another
4. When word count is under 300 words, classify as thin content and flag as high priority regardless of other signals
5. Always check for canonical tag correctness on collection-scoped product URLs before recommending other duplicate content fixes
6. Flag any page with a duplicate meta title or description as a critical issue — uniqueness is non-negotiable
7. Save all audit reports to `~/shopify-seo/audits/` and update `~/shopify-seo/fix-queue.md` when the user requests `seo save`
