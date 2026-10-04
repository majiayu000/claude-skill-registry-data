---
name: orbit-seo-schema
description: Audit Schema.org structured data output (JSON-LD) — required-vs-optional fields per type, Google Rich Results eligibility, validation against schema.org spec, coexistence with Yoast / RankMath. Use when the user says "schema markup", "structured data", "JSON-LD", "rich results", "schema.org".
---

# 🪐 orbit-seo-schema — Structured data audit

Schema.org markup unlocks Google rich results. Wrong markup = penalty risk. Right markup = stars / reviews / FAQs in SERP.

---

## What this skill checks

### 1. JSON-LD format (preferred over microdata / RDFa)
**Whitepaper intent:** Google explicitly recommends JSON-LD. Microdata + RDFa still work but are harder to maintain and easier to misnest.

```php
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "<?php echo esc_js( get_the_title() ); ?>",
  "datePublished": "<?php echo esc_js( get_the_date('c') ); ?>",
  "author": { "@type": "Person", "name": "<?php echo esc_js( get_the_author() ); ?>" }
}
</script>
```

Note: use `esc_js` AND `wp_json_encode` — `esc_js` alone breaks JSON.

```php
// ✅ Better
$schema = [
  '@context' => 'https://schema.org',
  '@type' => 'Article',
  'headline' => get_the_title(),
  'datePublished' => get_the_date( 'c' ),
];
echo '<script type="application/ld+json">' . wp_json_encode( $schema ) . '</script>';
```

### 2. Required vs recommended fields (per type)

Per Google Rich Results docs:
| Type | Required | Recommended |
|---|---|---|
| Article | headline, datePublished, image | author, dateModified |
| Product | name, image, offers (price/availability) | brand, description, aggregateRating, review |
| Recipe | name, image, recipeIngredient, recipeInstructions | author, prepTime, cookTime, recipeYield |
| Event | name, location, startDate | description, image, performer, offers |
| Organization | name, url | logo, sameAs |
| LocalBusiness | name, address, telephone | openingHours, image, priceRange |

Missing required = ineligible for rich results.

### 3. Validate via Google Rich Results Test
```bash
curl -X POST 'https://searchconsole.googleapis.com/v1/urlTestingTools/richResults:run' \
  -H 'Content-Type: application/json' \
  -d '{ "url": "https://my-site.com/post/" }'
```

(Auth required — Google Cloud OAuth)

Or just paste the JSON-LD into [Schema Markup Validator](https://validator.schema.org/) for a quick check.

### 4. Coexistence with SEO plugins
**Whitepaper intent:** Yoast / RankMath both output schema. Your plugin's schema duplicates → Google may pick wrong instance, or flag both as broken.

Solution:
```php
if ( defined( 'WPSEO_VERSION' ) ) {
  // Hook into Yoast schema graph instead of outputting separately
  add_filter( 'wpseo_schema_graph', 'my_plugin_extend_yoast_schema' );
} elseif ( defined( 'RANK_MATH_VERSION' ) ) {
  add_filter( 'rank_math/schema/snippet', 'my_plugin_extend_rm_schema' );
} else {
  // No SEO plugin — output our schema directly
}
```

### 5. Don't fabricate data
```json
"aggregateRating": { "@type": "AggregateRating", "ratingValue": 5, "reviewCount": 1000 }
```

If you don't actually have 1000 reviews, you'll get a Google manual action. Schema must be real.

### 6. Image dimensions
Google wants images at least 1200×630 (or 16:9) for Article schema. Smaller = ineligible.

---

## Output

```markdown
# Schema Audit — my-plugin

## Output mode
✓ JSON-LD (preferred)
⚠ Some pages also have microdata (`itemtype` attributes) — pick one

## Article schema
- ✓ headline, datePublished, image present
- ❌ image dimension < 1200×630 in 14 posts — ineligible for rich results
- ✓ author Person present

## Product schema (Woo integration)
- ✓ All required fields
- ⚠ aggregateRating output even when reviewCount = 0 — drop the field if no reviews

## Coexistence
- ❌ Both Yoast AND your plugin output Article schema for posts
   → Hook into Yoast's wpseo_schema_graph

## Validation
Run: https://validator.schema.org/?url=<your-url>
```

---

## Pair with

- `/orbit-compat-yoast` / `/orbit-compat-rankmath` — coexistence
- `/orbit-seo-sitemap` — sitemap-side
- `/orbit-seo-meta-tags` — OG, Twitter cards

---

## Sources & Evergreen References

### Canonical docs
- [Schema.org](https://schema.org/) — root spec
- [Google — Search Gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) — types Google supports
- [Rich Results Test](https://search.google.com/test/rich-results) — validation tool
- [Schema Markup Validator](https://validator.schema.org/) — independent validator
- [Yoast Schema docs](https://developer.yoast.com/customization/yoast-seo/adapting-schema/) — extend Yoast
- [RankMath Schema](https://rankmath.com/kb/customize-schema/) — extend RM

### Last reviewed
- 2026-04-29 — Google updates required-fields list every quarter
