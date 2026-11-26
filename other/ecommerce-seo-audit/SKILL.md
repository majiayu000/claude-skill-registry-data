---
name: ecommerce-seo-audit
description: Audit an online shop's category and product pages, Product and Offer markup, merchant listings, faceted navigation, out-of-stock items and variant URLs. Use for "ecommerce SEO audit", "why don't my products show in Google Shopping", "should filter pages be indexed" or before adding filters, a new theme or new markets.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/ecommerce-seo-audit
---

# Ecommerce SEO audit

Audits an online shop one page type at a time: category pages, product pages, the product data Google reads (structured data and Merchant Center), and the URL sprawl shops create (filters, sorting, tracking parameters, internal search, pagination, variants, out-of-stock items). Hands back a fix list grouped by page type, every item labelled with a priority, evidence and example URLs.

> **Romeo's rule:** Index the filter pages people actually search for and nothing else; nobody needs 40,000 ways to sort socks, least of all Googlebot.

## Use this when

- Category or product pages don't rank, or products don't appear in the Shopping tab or with price and stock in results.
- Search Console's Page indexing report is full of filter, sort or parameter URLs ("Crawled - currently not indexed", "Duplicate without user-selected canonical", "Alternate page with proper canonical tag").
- New products take weeks to get indexed.
- Before or after adding filters, a new theme, a new platform app, or a new country or currency.
- Many products are going out of stock or being discontinued.

## Don't use this for

- Moving to a new platform or domain → `site-migration-check`; country and language versions and hreflang → `hreflang-international`
- Writing and validating the Product JSON-LD itself → `schema-markup`
- One product or category page in depth against its target query → `on-page-seo-review`
- Getting products recommended in ChatGPT shopping, Google AI Mode and Gemini, or Perplexity → `ai-shopping-visibility`

## What you need

### Required
- Shop URL, platform (Shopify, WooCommerce, Adobe Commerce, BigCommerce, custom) and the countries and currencies it sells in.
- 6 to 10 sample URLs: home, the top 2 categories, a filtered category, a sorted category, page 2 of a category, a product with variants, an out-of-stock product, an internal search results page.
- Top categories and products by revenue (or the owner's best guess, labelled as a guess).

### Helpful
- Search Console: Page indexing, Performance by page, Merchant listings and Product snippets reports, Crawl stats, Core Web Vitals.
- Merchant Center diagnostics (read-only) and the product feed.
- A crawl export (Screaming Frog, Sitebulb) that includes parameter URLs; server logs showing Googlebot requests.
- Keyword data for filter values (brand, colour, size, material plus category).

### No tools?
Click through the shop like a customer and write down the URL every filter, sort option and page number creates. Read `/robots.txt` in the browser. Use view-source on each sample URL for canonicals, robots meta tags and JSON-LD, and paste product URLs into the Rich Results Test, which says whether it found merchant listing or product snippet markup. PageSpeed Insights shows field data for a category and a product URL when the shop has enough traffic. Search Console and Merchant Center are free; export their reports as CSV.

## Ground rules

- For most non-brand searches ("women's trail running shoes") a category page is what ranks; product pages win model names and the long tail. Fix categories first.
- Index a filter page only when people search for that combination and the shop has enough products to make the page useful. Prove demand with keyword data or Search Console queries; never guess.
- Pick the right control. robots.txt stops crawling but doesn't remove URLs already indexed; `noindex` only works if Google can crawl the page to see it; a canonical is a hint Google may ignore. Never block a URL in robots.txt when you need Google to see its `noindex`.
- Search Console's URL Parameters tool was retired in 2022. Parameter handling now lives entirely on the site: links, canonicals, robots.txt and status codes.
- Manufacturer descriptions aren't penalised, but they give Google no reason to pick you over every other retailer with the same text. Rewrite top sellers first, not all 20,000 SKUs.
- Markup, visible page and feed must agree on price, currency and availability. Mismatches get products disapproved in Merchant Center and teach Google to distrust the markup.
- A discontinued product redirected to the homepage is usually treated as a soft 404. Redirect only to something genuinely close.
- Learn the platform's defaults before "fixing" them. Shopify, for example, serves products at `/collections/<collection>/products/<product>` as well as `/products/<product>` and canonicalises to the second; the real fix is making the theme link to `/products/` URLs directly.

## Steps

1. **Map page types and URL patterns.**
   - For each type (home, category, subcategory, filtered, sorted, paginated, product, variant, internal search, brand, blog, cart and account), record the URL pattern, a rough count (from the crawl, sitemaps or a Page indexing export) and whether it should be indexed. The gap between "should be" and "is" drives the rest of the audit.
   - Sitemaps: products and categories listed with canonical, indexable 200 URLs only, discontinued items removed. Deeper checks go to `xml-sitemap-check`.
   - Known URLs far above products plus categories (5,000 products, 200,000 crawled URLs) means parameter sprawl. `Fix now` if new products are slow to index or Crawl stats show most Googlebot requests going to parameter URLs.
2. **Category pages.**
   - Title and H1 name the category the way people search for it ("Men's waterproof hiking boots", not "Collection 14").
   - A short, useful intro near the top (2 to 4 sentences: who it's for, how to choose), with longer buying advice below the products or in a linked guide. Walls of text that push products below the fold hurt shoppers and don't rescue a weak category: move them down.
   - Products present in the server HTML with plain `<a href>` links to each product, not injected only after a click or scroll.
   - Links to subcategories and to the filter pages chosen for indexing (step 6), plus breadcrumbs. Key categories within about 3 clicks of the homepage.
   - Empty categories: `noindex` while empty (Google's own suggestion). Categories with 1 or 2 products usually belong merged into the parent; permanently dead ones 301 to the parent.
   - Overlapping categories ("Sale" and "Clearance", the same category at two paths): merge, or pick one and canonicalise the other.
3. **Product pages.**
   - Unique copy for top sellers and products with search demand: what it's for, who it suits, sizing or fit, materials, compatibility, what's in the box, care. Manufacturer copy on the long tail: `Leave it` for now.
   - First-party reviews rendered in the HTML (not only inside an iframe), product Q&A, and a specs table with brand, model and GTIN or MPN where customers search for them.
   - Price, stock status, delivery cost and time, and the returns policy visible near the buy button.
   - Breadcrumb back to the category, related products, and a variant selector that doesn't break the URL (step 11).
   - Images: several real photos, large enough to zoom. Alt text, formats and sizes go to `image-seo`.
4. **Product structured data (Product and Offer).**
   - Know which result you're aiming for. Merchant listings: pages where the shopper buys from you; the Offer must be yours, with a price above zero. Product snippets: pages that review or compare products without selling them. The Rich Results Test shows which one Google detected.
   - Required for merchant listings: Product `name`, `image` and `offers` with `price` and `priceCurrency`. Add `availability`, `itemCondition`, `brand`, `gtin` or `mpn`, `sku`, and `aggregateRating` or `review` only from real reviews shown on that page.
   - Sale prices: the current price in `price`, the old one in a `priceSpecification` with `priceType` set to `StrikethroughPrice`. Member-only prices use `validForMemberTier`.
   - Shipping (`shippingDetails` with rate, destination and delivery time) and returns (`hasMerchantReturnPolicy` with `applicableCountry`, `returnPolicyCategory` and, for a fixed window, `merchantReturnDays`). Google recommends one shop-wide policy in Organization markup or in the Merchant Center or Search Console settings, with offer-level markup only for exceptions. When sources disagree, Merchant Center wins over page markup. Missing everywhere: `Fix next`.
   - Put Product markup in the server-rendered HTML. Google's documentation warns that JavaScript-generated Product markup can make Shopping crawls less frequent and less reliable, which matters for prices and stock that change.
   - Markup price or availability that contradicts the page: `Fix now` (disapprovals, lost listings). Required fields missing on every product: `Fix now`. Recommended fields missing: `Fix next`.
   - Read Search Console's Merchant listings and Product snippets reports for errors grouped by template.
5. **Merchant Center and free listings.**
   - Free listings put products in the Shopping tab and other Google surfaces without ad spend. Check for a Merchant Center account with a verified and claimed website, and products approved for free listings.
   - Products can come from a feed, a platform app, or Merchant Center reading the site's structured data. Whatever the source, compare feed price and availability with the live page for 5 products.
   - Diagnostics to read: price or availability mismatch, missing identifiers, image problems, policy disapprovals. An account-level misrepresentation suspension usually traces back to missing contact details, missing shipping or returns information, or claims the site can't back up: `Fix now`, and only the owner can request a review.
   - Merchant Center auto-tagging adds `srsltid=` to URLs clicked from free listings. Those URLs need a canonical to the clean URL; if the shop errors on unknown parameters, fix the shop or switch auto-tagging off.
6. **Faceted navigation (filters).**
   - List every filter and how it builds URLs (query parameter, path segment, fragment). For each, decide: index; crawl but don't index; or don't crawl.
   - Index single-filter pages (occasionally two filters) with proven demand and enough products: usually brand plus category, or a colour, material or style people actually type ("black leather sofa"). Give each a clean, stable URL, a self-referencing canonical, its own title, H1 and intro, and a link from the category page.
   - Keep everything else out of the crawl: price ranges, multi-select combinations, in-stock toggles, ratings, most sizes. In order of strength: don't create crawlable links for them (apply the filter with JavaScript or after a `#`, which Google ignores); block the parameters in robots.txt; canonical to the unfiltered category as a weaker hint.
   - Example rules, adjusted to the shop's real parameters: `Disallow: /*?*price=` and `Disallow: /*?*sort=`. Test patterns against sample URLs with a robots.txt parser (Google's is open source) before shipping; Search Console's old tester is gone and its robots.txt report only shows what Google fetched.
   - Filter URLs already indexed at scale: robots.txt alone leaves them indexed ("Indexed, though blocked by robots.txt"). Add `noindex` first, let Google recrawl, then block crawling if crawl volume is still a problem.
   - Filter combinations with no products should return 404, not an empty page with 200. Parameter order should be fixed (`?colour=red&size=10`, never also `?size=10&colour=red`) with no repeated filters.
   - Unfiltered pages crawled less because Googlebot is busy with filters (Crawl stats, logs): `Fix now` on large shops. A few hundred stray filter URLs on a small shop: `Leave it`.
7. **Sort, view and tracking parameters.**
   - `?sort=`, `?view=`, `?limit=`, `utm_` tags and click IDs: canonical to the clean URL, never linked internally; keep sort and view out of the crawl (step 6).
   - Internal links pointing at parameter versions of products or categories: `Fix next`; they keep feeding Google duplicates.
   - Session IDs in URLs: `Fix now`.
8. **Internal site-search pages.**
   - Results pages (`/search?q=`) should not be indexed: keep them out of the crawl with robots.txt and don't link to them. Spammers inject searches with spammy phrases to get such pages indexed under your domain; if Page indexing lists `/search` URLs, `Fix now`: serve `noindex` until they drop out, then block crawling.
   - When some searches show real demand, build a proper category or collection for them instead of indexing search results.
9. **Pagination.**
   - Each page gets its own URL (`?page=2`), a self-referencing canonical (not pointing at page 1) and a plain `<a href>` to the next page. Google no longer uses `rel=prev/next`; leaving the tags in is harmless (`Leave it`).
   - "Load more" or infinite scroll needs real paginated URLs behind it, or deep products are only discoverable through the sitemap.
   - Page 2 onwards canonicalised to page 1: `Fix next`. Products reachable only through JavaScript loading and missing from the sitemap: `Fix now`.
10. **Out-of-stock and discontinued products.**
    - Temporarily out of stock: keep the URL live at 200, set `availability` to `OutOfStock` (or `BackOrder` or `PreOrder`), and show alternatives and a back-in-stock signup. Don't noindex or remove it.
    - Seasonal or regularly restocked: keep the URL all year.
    - Discontinued with a direct successor: 301 to the successor. Discontinued but still earning links or traffic: keep a page that says so (`availability` set to `Discontinued`) and links to alternatives, or 301 to the closest category. Discontinued with neither: 404 or 410 is fine.
    - Hundreds of old products redirected to the homepage or a generic category: `Fix next` (Google usually treats them as soft 404s).
    - Drop or update discontinued items in the feed so Merchant Center stops showing them.
11. **Variants.**
    - One URL with a variant selector suits products whose variants differ only by size or colour and aren't searched for separately. The base URL is canonical; each variant still needs a preselect URL (`?colour=green`) that shows the right image, price and availability.
    - Separate URLs suit variants people search for by name (a colourway, a capacity, a model year). Each needs its own content, title and self-referencing canonical.
    - Describe the family with `ProductGroup` (`productGroupID`, `variesBy`, `hasVariant`), or have each variant point to it with `isVariantOf`.
    - Per-variant URLs identical apart from a swatch, each self-canonical: `Fix next` (duplicates). Preselect URLs that ignore the parameter and always show the default image and price: `Fix next`; Google can't match each variant to its offer.
12. **Speed on image-heavy pages.**
    - Measure field data (Search Console Core Web Vitals, PageSpeed Insights) for the category and product templates, not only the homepage. Good is LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1 at the 75th percentile.
    - Usual culprits: the main product image lazy-loaded or discovered late (load it eagerly with `fetchpriority="high"`), oversized images without `srcset`, images without width and height (layout shift), and third-party apps (reviews, chat, personalisation, upsell pop-ups) slowing interaction.
    - Grid images below the fold: `loading="lazy"`.
    - A template failing on field data with real traffic: `Fix next`. Lab-only Lighthouse scores: report as `tool` evidence and give them little weight.
13. **International pricing and currency.**
    - Each country or currency version needs its own crawlable URL (subfolder, subdomain or domain), the same currency in the page and the markup, and hreflang between versions → `hreflang-international`.
    - Currency switched or visitors redirected by IP on a single URL: Googlebot crawls mostly from US addresses, so the other versions may never be seen. `Fix now` if the shop sells in several markets this way.
    - Merchant Center: products and shipping set up for each target country, priced in that country's currency.

## What to hand back

Fill this in; every item needs a priority, evidence label, confidence and example URLs.

```markdown
## Summary
What I found: <one sentence>
What matters most: <one sentence>
What to do first: <one sentence>

## Page types
- <type>: <URL pattern> | about <count> URLs | should be indexed: <yes / no> | is: <yes / no / partly> | <evidence>

## Fix list by page type
### Sitewide (robots.txt, sitemaps, parameters)
1. [Fix now] <plain-English problem> (<term>)
   Evidence: <seen | tool | inferred>, <high | medium | low> confidence. Examples: <2 or 3 URLs>. Affected: <count or "not checked">
   Fix: <exact change and where it's made>
### Category pages
### Product pages
### Filter, sort and search URLs
### Pagination
### Out-of-stock, discontinued and variants
### Structured data and Merchant Center
### Speed
### International

## Filter decisions
- <filter>: index | crawl, don't index | don't crawl. Demand evidence: <source, or "not checked">

## What I could not check
- <item>: <why>, and what would verify it
```

## Stop and flag if

- A fix would change robots.txt, redirects, canonicals, the feed or Merchant Center settings. Draft it and get explicit permission; one wrong robots.txt pattern can drop whole categories from Google.
- The shop is mid-migration or replatforming. Run `site-migration-check` first.
- The Merchant Center account is suspended. The owner must fix the cause and request review; don't promise reinstatement.
- Markup prices don't match visible prices. Stop rich-result work until that's fixed.
- The output invents search volume for filter pages, says "index every filter", redirects discontinued products to the homepage wholesale, or lists fixes without example URLs. That output is unacceptable.

## Next step

- `schema-markup` with 3 product URLs (one with variants, one on sale, one out of stock) and the shop's shipping and returns policy.
- `internal-linking-plan` with the category tree and the filter pages chosen for indexing.
- `seo-change-monitor` to baseline the top categories and products before the fixes ship.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
