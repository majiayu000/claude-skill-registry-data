---
name: seo-optimizer
description: SEO Engineer — Fintech Platform — Institutional capability and runbook for seo-optimizer.
---

# SKILL: SEO Engineer — Fintech Platform
## Domain: Technical SEO, Meta Tags, Structured Data, Core Web Vitals

**Activation triggers:** meta tags, Open Graph, sitemap, robots.txt, structured
data, page title, canonical URL, Core Web Vitals, SSR, landing page SEO,
search ranking, social sharing.

---

## Module SEO Strategy

```
Public pages (need SEO):
  /                          ← landing page (highest priority)
  /features                  ← product features
  /pricing                   ← pricing plans
  /academy                   ← course listings (Google discovery)
  /academy/<course-slug>     ← individual course pages
  /blog/<slug>               ← editorial content
  /providers                 ← copy trading provider directory

Authenticated app pages (NO indexing — add noindex):
  /expert/*                  ← trading terminal
  /auth/*                    ← login/register
  /settings/*                ← user settings
```

---

## React Helmet / Meta Management

```typescript
// app/src/shared/seo/SEOHead.tsx
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title: string;
  description: string;
  canonical?: string;
  ogImage?: string;
  noIndex?: boolean;
  structuredData?: Record<string, unknown>;
}

export function SEOHead({
  title,
  description,
  canonical,
  ogImage = 'https://integralmarket.com/og-default.png',
  noIndex = false,
  structuredData,
}: SEOProps) {
  const fullTitle = `${title} | Integral Market`;

  return (
    <Helmet>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      {noIndex && <meta name="robots" content="noindex, nofollow" />}
      {canonical && <link rel="canonical" href={canonical} />}

      {/* Open Graph */}
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={ogImage} />
      <meta property="og:type" content="website" />
      <meta property="og:site_name" content="Integral Market" />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImage} />

      {/* Structured Data */}
      {structuredData && (
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      )}
    </Helmet>
  );
}
```

---

## Page-Level SEO Usage

```typescript
// Landing page
<SEOHead
  title="AI-Powered Trading Platform"
  description="Integral Market gives traders professional-grade analytics, copy trading, and MT5 integration in one unified platform."
  canonical="https://integralmarket.com/"
  structuredData={{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Integral Market",
    "applicationCategory": "FinanceApplication",
    "description": "AI-powered trading platform with copy trading, analytics, and broker integration.",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD",
      "description": "Free tier available"
    }
  }}
/>

// Course page
<SEOHead
  title={course.title}
  description={course.description.slice(0, 155)}
  canonical={`https://integralmarket.com/academy/${course.slug}`}
  ogImage={course.thumbnail_url}
  structuredData={{
    "@context": "https://schema.org",
    "@type": "Course",
    "name": course.title,
    "description": course.description,
    "provider": { "@type": "Organization", "name": "Integral Market" },
    "hasCourseInstance": {
      "@type": "CourseInstance",
      "courseMode": "online"
    }
  }}
/>

// Authenticated pages — always noindex
<SEOHead
  title="Trading Terminal"
  description="Integral Market Expert"
  noIndex={true}
/>
```

---

## Sitemap Generation (FastAPI)

```python
# integral-market-backend/app/api/v1/endpoints/sitemap.py
from fastapi import APIRouter
from fastapi.responses import Response
from lxml import etree

router = APIRouter()

STATIC_URLS = [
    ("/", "1.0", "daily"),
    ("/features", "0.9", "weekly"),
    ("/pricing", "0.9", "weekly"),
    ("/academy", "0.8", "daily"),
]

@router.get("/sitemap.xml", include_in_schema=False)
async def sitemap(db: AsyncSession = Depends(get_async_db)):
    base = "https://integralmarket.com"
    urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Static pages
    for path, priority, changefreq in STATIC_URLS:
        url = etree.SubElement(urlset, "url")
        etree.SubElement(url, "loc").text = f"{base}{path}"
        etree.SubElement(url, "priority").text = priority
        etree.SubElement(url, "changefreq").text = changefreq

    # Dynamic course pages
    courses = await db.execute(select(Course).where(Course.is_published.is_(True)))
    for course in courses.scalars():
        url = etree.SubElement(urlset, "url")
        etree.SubElement(url, "loc").text = f"{base}/academy/{course.slug}"
        etree.SubElement(url, "lastmod").text = course.updated_at.strftime("%Y-%m-%d")
        etree.SubElement(url, "priority").text = "0.7"
        etree.SubElement(url, "changefreq").text = "monthly"

    xml = etree.tostring(urlset, xml_declaration=True, encoding="utf-8", pretty_print=True)
    return Response(content=xml, media_type="application/xml")

@router.get("/robots.txt", include_in_schema=False)
async def robots():
    content = """User-agent: *
Allow: /
Allow: /academy/
Allow: /features
Allow: /pricing
Allow: /blog/
Disallow: /expert/
Disallow: /auth/
Disallow: /settings/
Disallow: /api/

Sitemap: https://integralmarket.com/sitemap.xml
"""
    return Response(content=content, media_type="text/plain")
```

---

## Core Web Vitals Optimization

```typescript
// 1. LCP — preload above-the-fold images
// In index.html:
// <link rel="preload" as="image" href="/hero-image.webp">

// 2. CLS — always reserve space for dynamic content
// WRONG:
<img src={url} alt="Chart" />

// CORRECT (aspect-ratio reserves space before image loads):
<div className="relative aspect-video w-full overflow-hidden rounded-xl">
  <img src={url} alt="Chart" className="absolute inset-0 h-full w-full object-cover" />
</div>

// 3. INP — defer non-critical JS
// In vite.config.ts:
// build.rollupOptions.output.manualChunks
const manualChunks = (id: string) => {
  if (id.includes('tradingview')) return 'charting';
  if (id.includes('@tanstack')) return 'query';
  if (id.includes('framer-motion')) return 'animation';
  if (id.includes('node_modules')) return 'vendor';
};
```

---

## SEO Content Rules for Academy

```
Course Title Format:
  "[Level] [Topic]: [Outcome]"
  Example: "Beginner Forex Trading: Master Risk Management in 30 Days"

Course Description Format (155 chars max for meta):
  "[Action verb] [skill] with [unique approach] — [key benefit]. [Social proof if available]."
  Example: "Master forex trading psychology with AI-driven feedback loops — used by 5,000+ traders."

Course Slug Format:
  kebab-case, no stop words, max 5 words
  Example: /academy/forex-risk-management-beginners

URL Strategy:
  - Permanent slugs (never change after publish)
  - 301 redirect if slug must change
  - No query params in canonical URLs
```

---

## Anti-Patterns

```
✗ Same meta description on every page (duplicate content penalty)
✗ Missing canonical URL on paginated pages (Google penalizes duplicates)
✗ Indexing authenticated app pages (/expert/, /auth/) — security + noise
✗ OG image missing or wrong dimensions (must be 1200×630px)
✗ Title > 60 chars (truncated in SERPs)
✗ Description > 155 chars (truncated in SERPs)
✗ Missing alt text on images (accessibility + SEO)
✗ JavaScript-only content for crawlers (dynamic content needs SSR or prerendering)
✗ Missing robots.txt (search engines crawl /api/ and /auth/ freely)
✗ Blocking CSS/JS in robots.txt (Google can't render the page)
```
