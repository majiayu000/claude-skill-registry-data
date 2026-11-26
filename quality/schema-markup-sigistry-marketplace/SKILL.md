---
name: schema-markup
description: Detect, validate and write JSON-LD structured data. Pick schema types by page type, fill Google's required properties, link entities in one @graph, and drop retired rich results. Use for "add schema to my site", "check my structured data", "fix Rich Results Test errors", "product schema", "missing field shippingDetails".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/schema-markup
---

# Schema markup

Find the structured data a page or template already outputs, check whether it is valid, eligible and true to the page, then write the JSON-LD it should have: types chosen by what the page actually is, Google's required properties filled from real data, entities linked in one `@graph`. You hand back ready-to-paste JSON-LD per template and a validation checklist.

> **Romeo's rule:** Markup describes what is on the page; it is not a letter to Google asking for stars.

## Use this when

- Someone asks to "add schema", "check structured data" or "get rich results" for a site or a new page template.
- The Rich Results Test or a Search Console enhancement report shows errors or warnings, such as `Missing field "shippingDetails"` or `Either "offers", "review", or "aggregateRating" should be specified`.
- A shop's product pages need merchant listing markup with price, availability, shipping and returns.
- Rich results (stars, prices, video thumbnails, breadcrumbs) disappeared after a theme, plugin or platform change.
- The business wants its organisation, authors and profiles described consistently for search engines and AI systems (`Organization`, `Person`, `sameAs`).

## Don't use this for

- Merchant Center feeds, product data quality and faceted navigation across a shop → `ecommerce-seo-audit`.
- Google Business Profile, reviews and map-pack visibility → `local-seo-audit`.
- Pages Google can't crawl, render or index, so the markup is never seen → `technical-seo-audit`.
- Author bios, sourcing and trust signals beyond the markup itself → `eeat-trust-review`.

## What you need

### Required

- The URL or HTML of one representative page per template (home, article, product, category, location, event, job, author page).
- What each template is for, in a sentence, and the facts the markup will state: legal and trading name, logo URL, official social and directory profiles, address and phone for local businesses, prices, currencies, shipping and return terms for shops.

### Helpful

- Search Console → Enhancements and Shopping reports (Merchant listings, Product snippets, Breadcrumbs, Videos and so on), with example URLs for each error.
- The CMS and any SEO plugin or app producing markup (Yoast, Rank Math, Shopify theme, a reviews app), because each outputs its own graph and duplicates are common.
- Whether a Merchant Center account exists: its shipping and returns settings override on-page markup.
- A Wikidata item or Wikipedia page for the organisation, if one exists.

### No tools?

View the page source and search for `application/ld+json` (JSON-LD), `itemscope` / `itemprop` (Microdata) and `vocab=` / `typeof=` (RDFa). Paste each JSON-LD block into any JSON linter to catch syntax errors. Run Google's Rich Results Test with the URL (it renders JavaScript and tests as Googlebot smartphone by default), then the Schema Markup Validator at validator.schema.org. Search Console's enhancement reports are free if the site is verified.

## Ground rules

- Markup must match visible content. Every price, rating, author, date, address and availability in the JSON-LD appears on the page with the same value. Marking up hidden or invented content can earn a manual action that removes rich result eligibility.
- Valid markup makes a page eligible for a rich result. It never guarantees one, and it is not a ranking boost on its own.
- Two validators answer two questions. The Rich Results Test asks "is this eligible for a Google feature, and does Google see it after rendering?"; it only reports types Google uses. The Schema Markup Validator asks "is this valid schema.org?"; it checks every type and property but says nothing about Google eligibility. Use both. A clean SMV result with an RRT error still means no rich result.
- Required properties missing = error = not eligible. Recommended properties missing = warning, still eligible. Add recommended properties only when the true value exists; never invent a value to clear a warning.
- One graph per page. One `<script type="application/ld+json">` holding an `@graph`, entities joined by `@id`. Two plugins each emitting an `Organization` or `Product` is a defect, not redundancy.
- Stable `@id`s: `https://example.com/#organization` and `https://example.com/#website` on every page; `<page URL>#article`, `#product`, `#person` for page entities. Same entity, same `@id`, everywhere.
- No self-serving review stars. `LocalBusiness` and `Organization` pages aren't eligible for review stars when the business controls the reviews about itself, including reviews pulled in by an embedded third-party widget. Product ratings must come from genuine reviews shown on the page.
- Use the most specific true type (`Dentist` over `LocalBusiness`, `BlogPosting` over `CreativeWork`), never a type that's merely flattering.
- Put JSON-LD in the server-rendered HTML where you can. Google processes JavaScript-injected markup, but its docs warn that JS-generated Product markup can make Shopping crawls less frequent and less reliable, and many non-Google crawlers don't run JavaScript.

## Steps

1. **Inventory what's there.** For each template, record every structured data block in the raw HTML and the rendered HTML (URL Inspection or the Rich Results Test "View tested page" → HTML).
   - Format (JSON-LD, Microdata, RDFa), source (theme, plugin, tag manager, app, hand-coded), the types and `@id`s present.
   - Duplicates: the same entity output twice, or in two formats. Conflicting values (two prices, two logos) = `Fix now` on money pages, otherwise `Fix next`.
   - Microdata or RDFa that validates is fine. Convert to JSON-LD only when you're already rewriting that template.
2. **Check against what Google still supports.** Google's search gallery is the source of truth; check it before promising any feature. Known retirements and limits:
   - HowTo rich results: removed in 2023.
   - FAQ rich results: limited to well-known government and health sites from August 2023; Google's documentation changelog says the feature stopped appearing in Search on 7 May 2026 and its documentation was removed in June 2026. Don't add FAQPage for Google. Existing FAQPage markup is harmless: `Leave it` (other consumers may still read it).
   - Phased out after Google's June 2025 announcement: Book Actions, Course Info, Claim Review (fact check), Estimated Salary, Learning Video, Special Announcement and Vehicle Listing. Six of them left the Rich Results Test and Search Console reports on 9 September 2025; Google later noted Book Actions markup is still used by a feature, so check its current status.
   - Practice problems: deprecated November 2025, no longer shown from January 2026.
   - Sitelinks search box: removed November 2024, so `WebSite` `potentialAction` `SearchAction` does nothing in Google (`Leave it` if present).
   - Breadcrumb paths: not shown in mobile results since January 2025, still shown on desktop. Still worth adding; it's cheap.
   - Dataset markup feeds Dataset Search, not Google Search results. Events must have a physical location; online-only events aren't supported.
3. **Pick types by page type.** Required properties are Google's for its feature; everything after "rec." is recommended.
   - Home: `Organization` (no required; rec. `name`, `url`, `logo` at least 112×112 px, `sameAs`, `legalName`, `address`, `contactPoint`, identifiers such as `vatID` or `duns`) or a specific `LocalBusiness` / `OnlineStore` subtype, plus `WebSite` (`name`, `url`, `alternateName`) on the home page to tell Google the site name to show in results.
   - Article, blog post, news: `Article` / `BlogPosting` / `NewsArticle` (no required; rec. `headline`, `image` at 16:9, 4:3 and 1:1 and at least 50,000 pixels, `datePublished`, `dateModified`, `author` with `name` and `url`). One `author` entry per person; names only, job titles go in `jobTitle`.
   - Breadcrumbs: `BreadcrumbList` with `ListItem` `position`, `name`, `item` (`item` optional on the last crumb), matching the visible trail.
   - Product you sell (merchant listing): `Product` with `name`, `image`, `offers`; `Offer` with `price` and `priceCurrency`; rec. `availability`, `itemCondition`, `shippingDetails`, `hasMerchantReturnPolicy`, `gtin`, `mpn`, `sku`, `brand`, genuine `aggregateRating` / `review`. Variants: `ProductGroup` with `hasVariant`, `variesBy`, `productGroupID`. One main product per page; not for category listings.
   - Product you review but don't sell (product snippet): `Product` with `name` plus one of `review`, `aggregateRating` or `offers`. Editorial reviews can add pros and cons via `positiveNotes` / `negativeNotes` (at least two statements).
   - Local business location: most specific `LocalBusiness` subtype with `name` and `address` (`PostalAddress`); rec. `geo`, `telephone`, `url`, `openingHoursSpecification`, `priceRange`. One location per page.
   - Event: `Event` with `name`, `startDate` (ISO 8601 with timezone) and `location` (`Place` with `address`); rec. `endDate`, `eventStatus`, `offers`, `organizer`, `performer`, `image`.
   - Job ad: `JobPosting` with `title`, `description` (HTML), `datePosted`, `hiringOrganization`, `jobLocation` (or `applicantLocationRequirements` with `jobLocationType: "TELECOMMUTE"` for remote); rec. `validThrough`, `baseSalary`, `employmentType`, `directApply`, `identifier`. Remove or expire it when the job is filled.
   - Video watch page: `VideoObject` with `name`, `thumbnailUrl`, `uploadDate`; rec. `contentUrl` (preferred) or `embedUrl`, `description`, `duration`, `creator`, and `Clip` (`hasPart`) or `SeekToAction` for key moments.
   - Software or SaaS: `SoftwareApplication` (or `WebApplication`, `MobileApplication`) with `name`, `offers.price` (0 if free) and `aggregateRating` or `review`; rec. `applicationCategory`, `operatingSystem`. Without genuine ratings there's no rich result; the markup still describes the product.
   - Author or profile page: `ProfilePage` with `mainEntity` (`Person` or `Organization` with `name`); rec. `sameAs`, `image`, `description`, `dateCreated`, `dateModified`.
   - Forum thread: `DiscussionForumPosting` with `author.name`, `datePublished` and `text`, `image` or `video`. Mostly question-and-answer threads → `QAPage`.
   - Recipe: `Recipe` with `name`, `image`; rec. `recipeIngredient`, `recipeInstructions` (`HowToStep`), `totalTime`, `recipeYield`, `nutrition.calories`, `author`, `aggregateRating`, `video`.
   - Anything else (course list, vacation rental, movie, paywalled content, image licence metadata): read that feature's page in Google's search gallery before writing it.
4. **Shop-wide policies.** A store can state default returns once on the `Organization` (`hasMerchantReturnPolicy`) and default shipping via `hasShippingService` (`ShippingService`, which needs `shippingConditions`). Product-level markup overrides organisation-level markup, and Merchant Center or Search Console settings override both. If those settings exist, make the markup agree with them.
5. **Validate the existing markup.** Rich Results Test on the live URL (smartphone), Schema Markup Validator, then Search Console's enhancement reports for trends and example URLs. Common defects:
   - `"price": "$19.99"` (currency symbol in price), prices with thousands separators, `priceCurrency` not ISO 4217.
   - Dates not ISO 8601, or no timezone. `availability` as "In stock" instead of `https://schema.org/InStock`.
   - Relative or robots-blocked image URLs. Logo that's a wide banner or tiny favicon.
   - `aggregateRating` with zero reviews, or ratings not shown on the page. Self-serving review stars on the home page.
   - `author.name` containing "By", a job title or several people. `dateModified` that changes on every page load.
   - Markup describing items not on the page, or several competing `Product` entities on one product page.
6. **Write the JSON-LD.** One script, `"@context": "https://schema.org"`, an `@graph` array, absolute URLs, ISO 8601 dates with timezone, values pulled from CMS fields rather than hard-coded so price, stock and dates stay true. `sameAs` lists only official profiles the organisation or person controls (LinkedIn, GitHub, Crunchbase, Wikidata, Wikipedia, social accounts), never review sites or competitors. Pattern for an article page:

   ```html
   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@graph": [
       { "@type": "Organization", "@id": "https://example.com/#organization",
         "name": "Example Ltd", "url": "https://example.com/",
         "logo": { "@type": "ImageObject", "url": "https://example.com/logo-512.png" },
         "sameAs": ["https://www.linkedin.com/company/example", "https://github.com/example"] },
       { "@type": "WebSite", "@id": "https://example.com/#website",
         "url": "https://example.com/", "name": "Example",
         "publisher": { "@id": "https://example.com/#organization" } },
       { "@type": "Person", "@id": "https://example.com/authors/sam-lee/#person",
         "name": "Sam Lee", "jobTitle": "Head of Support",
         "url": "https://example.com/authors/sam-lee/",
         "sameAs": ["https://www.linkedin.com/in/example-sam-lee"] },
       { "@type": "BlogPosting", "@id": "https://example.com/blog/fix-crawl-errors/#article",
         "mainEntityOfPage": "https://example.com/blog/fix-crawl-errors/",
         "headline": "How to fix crawl errors in Search Console",
         "image": ["https://example.com/img/crawl-errors-16x9.jpg",
                   "https://example.com/img/crawl-errors-4x3.jpg",
                   "https://example.com/img/crawl-errors-1x1.jpg"],
         "datePublished": "2026-09-14T09:00:00+01:00",
         "dateModified": "2026-10-30T16:20:00+00:00",
         "author": { "@id": "https://example.com/authors/sam-lee/#person" },
         "publisher": { "@id": "https://example.com/#organization" },
         "isPartOf": { "@id": "https://example.com/#website" } },
       { "@type": "BreadcrumbList", "itemListElement": [
         { "@type": "ListItem", "position": 1, "name": "Blog", "item": "https://example.com/blog/" },
         { "@type": "ListItem", "position": 2, "name": "How to fix crawl errors" } ] }
     ]
   }
   </script>
   ```

   The `Offer` for a product page you sell, with shipping and returns (add `gtin`, `sku` and `brand` on the `Product` when you have them):

   ```json
   "offers": {
     "@type": "Offer",
     "url": "https://shop.example/p/merino-throw-grey/",
     "price": 89.00, "priceCurrency": "GBP",
     "availability": "https://schema.org/InStock",
     "itemCondition": "https://schema.org/NewCondition",
     "shippingDetails": {
       "@type": "OfferShippingDetails",
       "shippingRate": { "@type": "MonetaryAmount", "value": 0, "currency": "GBP" },
       "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "GB" },
       "deliveryTime": { "@type": "ShippingDeliveryTime",
         "handlingTime": { "@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY" },
         "transitTime": { "@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY" } } },
     "hasMerchantReturnPolicy": {
       "@type": "MerchantReturnPolicy",
       "applicableCountry": "GB",
       "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
       "merchantReturnDays": 30,
       "returnMethod": "https://schema.org/ReturnByMail",
       "returnFees": "https://schema.org/FreeReturn" }
   }
   ```

7. **Re-test before handing back.** Paste the final JSON-LD into the Rich Results Test (code mode) and the Schema Markup Validator. After deployment, re-run the Rich Results Test against the URL and confirm the script appears in URL Inspection's crawled HTML.

## What to hand back

One section per template, worst problems first, with JSON-LD ready to paste.

```markdown
# Structured data review: <site> (<date>)

**What I found:** <one plain-English sentence>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

## Findings
### 1. <Template, e.g. Product pages> · `Fix now`
- Problem: <plain English first, then the term in brackets>
- Evidence: <example URL, validator message or snippet> · seen / tool / inferred · confidence: high / medium / low
- Fix: <what changes and where: theme file, plugin setting, CMS field>

## JSON-LD to paste
### <Template> (<example URL>)
<one complete <script type="application/ld+json"> block with @graph>
- Values taken from: <CMS field or page element for each dynamic value>
- Placeholders to fill: <[confirm: ...] items, or "none">
- Remove: <duplicate blocks or plugin output to switch off>

## Leave it
- <e.g. old FAQPage markup>: <why it's harmless>

## Validation checklist
- [ ] JSON parses (straight quotes, no trailing commas)
- [ ] Rich Results Test on the live URL (smartphone): expected items detected, zero errors
- [ ] Schema Markup Validator: zero errors for every type
- [ ] Every marked-up value is visible on the page and identical
- [ ] One entity per @id; no duplicate Organization or Product from plugins or apps
- [ ] Image URLs are absolute, crawlable and not blocked by robots.txt
- [ ] Values come from the template, so price, stock and dates update themselves
- [ ] URL Inspection shows the script in the crawled HTML after deploy
- [ ] Search Console enhancement reports rechecked 1 to 2 weeks after deploy

## What I could not check
- <item>: <what would verify it>
```

## Stop and flag if

- The markup would state facts you don't have (price, rating, GTIN, address, return window). Use `[confirm: ...]` placeholders and name who must supply them; never invent values or reviews.
- The user wants review stars for their own business on its own site, or markup for content that isn't visible. Explain the policy and don't write it.
- The user expects a retired feature (FAQ, HowTo, fact check, sitelinks search box). Say so before writing anything.
- Pages are blocked, noindexed or not rendering, so no markup would be read. Route to `technical-seo-audit` first.
- Fixing it means editing a live theme, plugin setting or tag manager container. Draft the change; apply nothing without explicit permission for that change.
- Output without both validators run (or a clear "not run, because..."), or with conflicting duplicate entities left in place, is not acceptable.

## Next step

- Shops → `ecommerce-seo-audit` with the merchant listing findings, to align markup with feeds and Merchant Center.
- Article and author markup in place → `eeat-trust-review` to check the author pages and bios the `Person` entities point to.
- After deploy → `seo-change-monitor` to snapshot the markup and catch a theme update that removes it.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
