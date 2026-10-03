---
name: seo-optimization
description: Optimize web applications for search engines. Implement technical SEO, structured data, and performance optimizations for better rankings.
triggers:
- /seo
- /search optimize
---

# Search Engine Optimization (SEO)

This skill covers technical SEO implementation to improve search engine visibility, rankings, and organic traffic for web applications.

## When to use this skill

Use this skill when you need to:
- Optimize website for search engines
- Implement technical SEO requirements
- Add structured data markup
- Improve Core Web Vitals for SEO
- Set up proper indexing and crawling

## Prerequisites

- Access to website source code
- Google Search Console access
- Understanding of HTML semantics
- Knowledge of JavaScript frameworks (if applicable)

## Guidelines

### Technical SEO Fundamentals

**Semantic HTML**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Page Title | Brand Name</title>
  <meta name="description" content="Compelling meta description under 160 characters">
  <link rel="canonical" href="https://example.com/page">
</head>
<body>
  <header>
    <nav aria-label="Main navigation">
      <!-- Navigation -->
    </nav>
  </header>
  
  <main>
    <article>
      <h1>Primary Heading</h1>
      <h2>Subheading</h2>
      <!-- Content -->
    </article>
  </main>
  
  <footer>
    <!-- Footer content -->
  </footer>
</body>
</html>
```

**URL Structure**
- Use descriptive, keyword-rich URLs
- Keep URLs short and readable
- Use hyphens to separate words
- Avoid query parameters when possible

```
✅ https://example.com/products/wireless-headphones
❌ https://example.com/p?id=12345&cat=audio
```

**Heading Hierarchy**
```html
<!-- ✅ Correct heading structure -->
<h1>Main Page Title</h1>
  <h2>Section One</h2>
    <h3>Subsection</h3>
  <h2>Section Two</h2>
    <h3>Subsection</h3>
      <h4>Detail</h4>

<!-- ❌ Avoid: Skipping levels or multiple H1s -->
<h1>Title</h1>
<h3>Skipped H2</h3>
```

### Meta Tags

**Essential Meta Tags**
```html
<!-- Character encoding -->
<meta charset="UTF-8">

<!-- Viewport for mobile -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Page description (160 chars max) -->
<meta name="description" content="Learn SEO best practices for web development with practical examples and guidelines.">

<!-- Robots directive -->
<meta name="robots" content="index, follow">

<!-- Canonical URL -->
<link rel="canonical" href="https://example.com/original-page">

<!-- Open Graph (social sharing) -->
<meta property="og:title" content="SEO Best Practices">
<meta property="og:description" content="Complete guide to technical SEO">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="article">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="SEO Best Practices">
<meta name="twitter:description" content="Complete guide to technical SEO">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### Structured Data

**JSON-LD Implementation**
```html
<!-- Article markup -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "SEO Best Practices Guide",
  "description": "Complete guide to technical SEO implementation",
  "author": {
    "@type": "Person",
    "name": "Jane Developer"
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20",
  "image": "https://example.com/article-image.jpg"
}
</script>

<!-- Organization markup -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/name"
  ]
}
</script>

<!-- Product markup -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Wireless Headphones",
  "image": "https://example.com/headphones.jpg",
  "description": "High-quality wireless headphones",
  "brand": {
    "@type": "Brand",
    "name": "AudioTech"
  },
  "offers": {
    "@type": "Offer",
    "price": "99.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

### SPA SEO (React, Vue, Angular)

**Server-Side Rendering (SSR)**
```javascript
// Next.js example with metadata
import Head from 'next/head';

export default function ProductPage({ product }) {
  return (
    <>
      <Head>
        <title>{product.name} | Store</title>
        <meta name="description" content={product.description} />
        <link rel="canonical" href={`https://example.com/products/${product.slug}`} />
      </Head>
      <ProductDetails product={product} />
    </>
  );
}

export async function getServerSideProps({ params }) {
  const product = await fetchProduct(params.slug);
  return { props: { product } };
}
```

**Dynamic Sitemap**
```javascript
// pages/sitemap.xml.js (Next.js)
export async function getServerSideProps({ res }) {
  const pages = await fetchAllPages();
  
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      ${pages.map(page => `
        <url>
          <loc>https://example.com${page.path}</loc>
          <lastmod>${page.updatedAt}</lastmod>
          <changefreq>${page.changeFreq}</changefreq>
          <priority>${page.priority}</priority>
        </url>
      `).join('')}
    </urlset>`;

  res.setHeader('Content-Type', 'text/xml');
  res.write(sitemap);
  res.end();
  
  return { props: {} };
}
```

### Performance for SEO

**Core Web Vitals Impact**
- LCP < 2.5s (Good), < 4s (Needs Improvement)
- FID < 100ms (Good), < 300ms (Needs Improvement)
- CLS < 0.1 (Good), < 0.25 (Needs Improvement)

**Image Optimization**
```html
<!-- Responsive images with lazy loading -->
<img 
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  alt="Descriptive image text"
  loading="lazy"
  width="800"
  height="600"
>
```

**Resource Hints**
```html
<!-- Preconnect to required origins -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://cdn.example.com">

<!-- Preload critical resources -->
<link rel="preload" href="/critical.css" as="style">
<link rel="preload" href="/hero-image.jpg" as="image">
```

### Crawlability

**Robots.txt**
```
User-agent: *
Allow: /

# Disallow admin and private areas
Disallow: /admin/
Disallow: /private/
Disallow: /api/

# Allow specific file types
Allow: /*.js$
Allow: /*.css$

# Sitemap location
Sitemap: https://example.com/sitemap.xml
```

**Internal Linking**
- Use descriptive anchor text
- Maintain shallow site architecture (3 clicks max)
- Implement breadcrumb navigation
- Add pagination with rel="next"/"prev"

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Headphones</li>
  </ol>
</nav>
```

### Mobile Optimization

**Mobile-First Indexing**
- Ensure mobile and desktop content match
- Test with Google Mobile-Friendly Test
- Use responsive design (avoid separate mobile URLs)
- Optimize for touch interactions

### Monitoring

**Google Search Console**
- Submit sitemaps
- Monitor indexing status
- Review Core Web Vitals report
- Check mobile usability
- Analyze search performance

**Key Metrics**
- Organic traffic
- Click-through rate (CTR)
- Average position
- Indexed pages
- Crawl errors

## Examples

See the `examples/` directory for:
- `structured-data/` - JSON-LD examples by type
- `meta-tags/` - Complete meta tag templates
- `spa-seo/` - Framework-specific SEO implementations
- `robots-txt/` - Robots.txt examples

## References

- [Google Search Central](https://developers.google.com/search/docs)
- [Schema.org](https://schema.org/)
- [Moz SEO Learning Center](https://moz.com/learn/seo)
- [Web.dev SEO](https://web.dev/seo/)
- [Next.js SEO](https://nextjs.org/docs/app/building-your-application/optimizing/metadata)
