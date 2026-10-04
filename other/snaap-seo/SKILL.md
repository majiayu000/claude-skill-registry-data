---
name: snaap-seo
description: >
  Use for meta tags, structured data, sitemap, robots, landing pages and any indexing work on
  Snaap Connections. Provides the JSON-LD templates, title/description patterns and the curl
  verification commands.
---
# Snaap SEO

**Verify with curl against raw HTML, not DevTools.** For example:

```
curl -s https://www.snaapconnections.co.ke/products | grep -c 'href="/products/'      # expect >= 12
curl -s -o /dev/null -w '%{http_code}\n' https://www.snaapconnections.co.ke/sitemap.xml  # expect 200
```

**Store schema:** `"@type": "MobilePhoneStore"` (case-sensitive; `mobilephoneStore` is discarded
by Google). Complete it from `src/constants/business`: name, url, image, telephone, address
(streetAddress / addressLocality / addressRegion / addressCountry), openingHoursSpecification
(Mon–Sun 08:00–19:00), sameAs (Facebook / TikTok / Instagram), areaServed = the five counties.
**Omit `geo`** until the owner supplies the verified Google Business Profile pin.

**Product / Offer:** `priceCurrency: "KES"`, availability, sku, itemCondition, priceValidUntil,
hasMerchantReturnPolicy, a BreadcrumbList matching the visible breadcrumb, and shippingDetails as
two `OfferShippingDetails` (KES 300 same-day coast; KES 500–1,500 24h upcountry). **Never** add
`aggregateRating` without real approved reviews.

**Titles / descriptions:** unique per route. Generate product meta from live fields
(name / price / specs); use the hand-written blurb only as a suffix — descriptions feed the
JSON-LD, so drift misprices us to Google.

**Filtered listings:** self-referencing canonical; validate `?brand=` / `?category=` server-side
against the real lists; unknown value → 404; `noindex` any zero-result combination.

Validate every schema with Google's Rich Results Test before merge. A schema that fails validation
is worse than none.
