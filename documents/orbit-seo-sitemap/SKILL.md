---
name: orbit-seo-sitemap
description: Audit XML sitemap output — well-formed XML, sitemap-index for large sites (50K URL chunks), priority + changefreq usage, image / video / news sitemaps, robots.txt linkage, coexistence with Yoast / RankMath / WP core sitemaps. Use when the user says "sitemap", "XML sitemap", "search console sitemap", "Yoast sitemap conflict".
---

# 🪐 orbit-seo-sitemap — Sitemap audit

Sitemaps tell search engines what to crawl. Broken sitemaps = invisible content.

---

## What this skill checks

### 1. Sitemap is well-formed XML
```bash
curl -s https://my-site.com/sitemap.xml | xmllint --noout -
```

Should exit 0. Any error = malformed → search engines reject silently.

### 2. WP 5.5+ ships sitemaps natively at `/wp-sitemap.xml`
**Whitepaper intent:** Plugins shouldn't ship their own sitemap unless they have a clear reason — WP core sitemap is good enough for most. If you do ship one, opt-out of WP core's:

```php
add_filter( 'wp_sitemaps_enabled', '__return_false' );
```

### 3. Sitemap-index for large sites
A single sitemap.xml is limited to 50,000 URLs OR 50MB. Bigger sites need a sitemap index pointing to chunked sub-sitemaps.

```xml
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://my-site.com/sitemap-posts-1.xml</loc>
    <lastmod>2026-04-29</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://my-site.com/sitemap-products.xml</loc>
  </sitemap>
</sitemapindex>
```

### 4. priority / changefreq — Google ignores these
**Whitepaper intent:** `<priority>` and `<changefreq>` are part of the spec but Google has publicly said it ignores them. Bing still uses changefreq (loosely). Don't over-engineer these.

### 5. robots.txt links to sitemap
```
User-agent: *
Allow: /

Sitemap: https://my-site.com/sitemap.xml
```

WP doesn't write robots.txt by default — plugin / customer must.

### 6. Image sitemap (if plugin generates image-heavy content)
```xml
<url>
  <loc>https://my-site.com/post/</loc>
  <image:image>
    <image:loc>https://my-site.com/post-cover.jpg</image:loc>
  </image:image>
</url>
```

### 7. Video / News sitemap (specific use cases)
- News sitemap — only if you produce news (specific tags, time-window 2 days)
- Video sitemap — for video-heavy sites

### 8. Coexistence with SEO plugins
- Yoast: `/sitemap_index.xml` (theirs)
- RankMath: `/sitemap_index.xml` (theirs)
- WP core: `/wp-sitemap.xml` (default)

If your plugin generates a 4th — robots.txt + Search Console submission gets confusing. Pick one + hook into it.

---

## Output

```markdown
# Sitemap Audit — my-plugin

## Sitemap URL
- /sitemap.xml — your plugin's
- /sitemap_index.xml — Yoast also active
- /wp-sitemap.xml — WP core (still on)

⚠ Three sitemaps for same site — Google may submit / verify any. Recommendation:
1. Disable WP core via `wp_sitemaps_enabled = false`
2. Hook into Yoast's via `wpseo_sitemap_index`
3. Drop your standalone

## Validation
- ✓ XML well-formed
- ✓ < 50,000 URLs (no chunking needed)
- ⚠ priority + changefreq present — Google ignores; can drop to slim XML

## robots.txt
- ❌ robots.txt doesn't reference any sitemap
- Recommendation: add `Sitemap: https://my-site.com/sitemap_index.xml`

## Image sitemap
- ⚠ Plugin produces image-heavy posts but no <image:image> tags in sitemap
   → Add for richer image-search indexing
```

---

## Pair with

- `/orbit-seo-schema` — schema-side
- `/orbit-compat-yoast` / `/orbit-compat-rankmath` — coexistence

---

## Sources & Evergreen References

### Canonical docs
- [sitemaps.org](https://www.sitemaps.org/) — protocol spec
- [Google Sitemaps docs](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview) — submission + best practices
- [WP wp_sitemaps](https://developer.wordpress.org/reference/classes/wp_sitemaps/) — WP core API
- [Yoast wpseo_sitemap_index filter](https://developer.yoast.com/customization/yoast-seo/filters/sitemaps/) — extend Yoast

### Last reviewed
- 2026-04-29
