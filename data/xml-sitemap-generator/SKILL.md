---
name: xml-sitemap-generator
description: Generate valid XML sitemap files for websites with proper URL entries, priorities, change frequencies, and optional image/video extensions. Triggers on "create sitemap", "generate sitemap.xml", "XML sitemap for", "SEO sitemap".
---

# XML Sitemap Generator

Generate valid XML sitemaps compliant with the Sitemaps Protocol for search engine optimization.

## Output Requirements

**File Output:** `sitemap.xml`, `sitemap-index.xml`, or `sitemap-{section}.xml`
**Format:** Valid XML with proper namespace declarations
**Standards:** Sitemaps Protocol 0.9

## When Invoked

Immediately generate a complete, valid XML sitemap. Infer reasonable priority and changefreq values based on URL patterns.

## Sitemap Protocol Specifications

### Required Elements
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
  </url>
</urlset>
```

### Optional Elements
- `<lastmod>` - Last modification date (W3C Datetime format)
- `<changefreq>` - Expected change frequency
- `<priority>` - Relative priority (0.0 to 1.0)

### Limits
- Maximum 50,000 URLs per sitemap file
- Maximum 50MB file size (uncompressed)
- Use sitemap index for larger sites

## Template Types

### Basic Website Sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Homepage -->
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- Main Navigation Pages -->
  <url>
    <loc>https://example.com/about</loc>
    <lastmod>2024-01-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>

  <url>
    <loc>https://example.com/services</loc>
    <lastmod>2024-01-12</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

  <url>
    <loc>https://example.com/contact</loc>
    <lastmod>2024-01-05</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.6</priority>
  </url>

  <!-- Blog Section -->
  <url>
    <loc>https://example.com/blog</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>

  <url>
    <loc>https://example.com/blog/post-title-one</loc>
    <lastmod>2024-01-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>

  <url>
    <loc>https://example.com/blog/post-title-two</loc>
    <lastmod>2024-01-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>
```

### E-commerce Sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Homepage -->
  <url>
    <loc>https://store.example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- Category Pages -->
  <url>
    <loc>https://store.example.com/category/electronics</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>

  <url>
    <loc>https://store.example.com/category/electronics/laptops</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>

  <!-- Product Pages -->
  <url>
    <loc>https://store.example.com/product/laptop-pro-15</loc>
    <lastmod>2024-01-14</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>

  <url>
    <loc>https://store.example.com/product/wireless-mouse</loc>
    <lastmod>2024-01-13</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>

  <!-- Static Pages -->
  <url>
    <loc>https://store.example.com/shipping</loc>
    <lastmod>2024-01-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>

  <url>
    <loc>https://store.example.com/returns</loc>
    <lastmod>2024-01-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Sitemap Index (For Large Sites)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2024-01-15</lastmod>
  </sitemap>

  <sitemap>
    <loc>https://example.com/sitemap-blog.xml</loc>
    <lastmod>2024-01-15</lastmod>
  </sitemap>

  <sitemap>
    <loc>https://example.com/sitemap-products-1.xml</loc>
    <lastmod>2024-01-15</lastmod>
  </sitemap>

  <sitemap>
    <loc>https://example.com/sitemap-products-2.xml</loc>
    <lastmod>2024-01-14</lastmod>
  </sitemap>
</sitemapindex>
```

### Sitemap with Images Extension
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://example.com/products/widget</loc>
    <image:image>
      <image:loc>https://example.com/images/widget-front.jpg</image:loc>
      <image:title>Widget Front View</image:title>
      <image:caption>High-quality widget shown from the front</image:caption>
    </image:image>
    <image:image>
      <image:loc>https://example.com/images/widget-side.jpg</image:loc>
      <image:title>Widget Side View</image:title>
    </image:image>
  </url>
</urlset>
```

### Sitemap with Video Extension
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>https://example.com/videos/tutorial</loc>
    <video:video>
      <video:thumbnail_loc>https://example.com/thumbs/tutorial.jpg</video:thumbnail_loc>
      <video:title>Getting Started Tutorial</video:title>
      <video:description>Learn how to use our product in 5 minutes</video:description>
      <video:content_loc>https://example.com/videos/tutorial.mp4</video:content_loc>
      <video:duration>300</video:duration>
      <video:publication_date>2024-01-15T08:00:00+00:00</video:publication_date>
    </video:video>
  </url>
</urlset>
```

### News Sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://news.example.com/article/breaking-news</loc>
    <news:news>
      <news:publication>
        <news:name>Example News</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>2024-01-15T12:00:00+00:00</news:publication_date>
      <news:title>Breaking: Major Event Unfolds</news:title>
    </news:news>
  </url>
</urlset>
```

## Priority and Changefreq Guidelines

### Priority Values
| Page Type | Priority |
|-----------|----------|
| Homepage | 1.0 |
| Main category/section pages | 0.8-0.9 |
| Product/service pages | 0.7-0.8 |
| Blog/article index | 0.7 |
| Individual blog posts | 0.5-0.6 |
| Policy pages (privacy, terms) | 0.3-0.5 |
| Utility pages (login, cart) | 0.3 |

### Changefreq Values
| Value | Use For |
|-------|---------|
| always | Real-time pages, live data |
| hourly | News, frequently updated content |
| daily | Blog index, homepage |
| weekly | Product pages, regular content |
| monthly | About pages, documentation |
| yearly | Policy pages, archives |
| never | Dated archives, old content |

## Date Formats

### W3C Datetime (Required)
```
YYYY-MM-DD
YYYY-MM-DDThh:mmTZD
YYYY-MM-DDThh:mm:ssTZD
YYYY-MM-DDThh:mm:ss.sTZD
```

Examples:
- `2024-01-15`
- `2024-01-15T09:30:00+00:00`
- `2024-01-15T09:30:00Z`

## Validation Checklist

Before outputting, verify:
- [ ] Valid XML declaration with UTF-8 encoding
- [ ] Correct namespace declarations
- [ ] All URLs are absolute (include protocol and domain)
- [ ] URLs are properly escaped (& becomes &amp;)
- [ ] lastmod dates are W3C Datetime format
- [ ] priority values are between 0.0 and 1.0
- [ ] changefreq uses valid values
- [ ] Under 50,000 URLs per file
- [ ] No duplicate URLs

## URL Escaping

Escape these characters:
| Character | Escape |
|-----------|--------|
| & | `&amp;` |
| ' | `&apos;` |
| " | `&quot;` |
| > | `&gt;` |
| < | `&lt;` |

## Example Invocations

**Prompt:** "Create sitemap.xml for a SaaS marketing website"
**Output:** Complete `sitemap.xml` with homepage, features, pricing, blog, and static pages.

**Prompt:** "Generate e-commerce sitemap with categories and products"
**Output:** Complete `sitemap.xml` with category hierarchy, product pages, and static pages.

**Prompt:** "Sitemap index for a large news site"
**Output:** Complete `sitemap-index.xml` plus individual `sitemap-{section}.xml` files.
