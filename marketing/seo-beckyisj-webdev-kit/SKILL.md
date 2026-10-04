---
name: seo
description: Audit and bootstrap SEO for a web project — sitemap.xml, robots.txt, llms.txt, JSON-LD structured data, and meta tags. Use when launching a site or adding SEO to an existing one.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [project-path]
---

# SEO Bootstrapper

Audit a web project's SEO setup and generate everything missing.

**Argument**: `$ARGUMENTS` is the project path. If not provided, ask.

## Process

### 1. Scan what's already there

Run these checks in parallel:

```bash
# Check for existing SEO files
ls public/sitemap.xml public/robots.txt public/llms.txt 2>/dev/null
ls src/app/sitemap.* src/app/robots.* 2>/dev/null

# Check for meta tags in HTML
grep -l "og:title" *.html public/*.html 2>/dev/null

# Check for JSON-LD
grep -rl "application/ld+json" . 2>/dev/null

# Check framework
cat package.json | grep -E "(next|vite|astro)" 2>/dev/null
```

### 2. Ask for essentials (if missing)

- **Canonical domain** (e.g., `https://mytool.app`)
- **Site name** and **tagline**
- **Description** (160 char max for meta description)
- **Content type**: marketing site, blog, web app, article, or tool?
- **Organization info**: name, logo URL, social links (for JSON-LD)

### 3. Generate missing pieces

Use the framework-appropriate approach:

#### A. sitemap.xml

**Static HTML sites** — create `public/sitemap.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://[domain]/</loc>
    <lastmod>2026-04-16</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://[domain]/articles/</loc>
    <lastmod>2026-04-16</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- Additional pages at 0.7 priority, monthly -->
</urlset>
```

**Next.js App Router** — create `src/app/sitemap.ts`:
```typescript
import type { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://[domain]',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 1.0,
    },
    // Additional URLs
  ];
}
```

**Priority guide:**
- Homepage: 1.0
- Index pages (articles, products): 0.8
- Individual content pages: 0.7
- Utility pages (about, contact): 0.5

#### B. robots.txt

**Static sites** — create `public/robots.txt`:
```
User-agent: *
Allow: /

# AI crawlers
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: CCBot
Allow: /

Sitemap: https://[domain]/sitemap.xml
```

**Next.js** — create `src/app/robots.ts`:
```typescript
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/', disallow: ['/api/'] },
      { userAgent: 'GPTBot', allow: '/' },
      { userAgent: 'ClaudeBot', allow: '/' },
      { userAgent: 'Claude-SearchBot', allow: '/' },
      { userAgent: 'PerplexityBot', allow: '/' },
    ],
    sitemap: 'https://[domain]/sitemap.xml',
  };
}
```

#### C. llms.txt

Create `public/llms.txt` (or root for Next.js):

```markdown
# [Site Name]

> [One-sentence tagline]

## What is [Site Name]?

[2-3 sentence description — what it does, who it's for]

## Key features

- **[Feature 1]**: [Description]
- **[Feature 2]**: [Description]
- **[Feature 3]**: [Description]

## Links

- Homepage: https://[domain]/
- Articles: https://[domain]/articles/
- Contact: https://[domain]/contact/

## About

[1-2 sentences about the creator/company]
```

Link it from the HTML head:
```html
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM-friendly content">
```

#### D. JSON-LD structured data

Choose the schema based on content type:

**Organization** (homepage of a product/company):
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Name]",
  "url": "https://[domain]",
  "logo": "https://[domain]/logo.png",
  "sameAs": [
    "https://x.com/[handle]",
    "https://linkedin.com/in/[handle]"
  ]
}
</script>
```

**WebApplication** (a tool or app):
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "[Tool Name]",
  "url": "https://[domain]",
  "description": "[Description]",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
```

**Article** (blog posts):
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "[Title]",
      "description": "[Description]",
      "datePublished": "2026-04-16",
      "author": { "@type": "Person", "name": "[Author]", "url": "[url]" },
      "publisher": {
        "@type": "Organization",
        "name": "[Publisher]",
        "logo": { "@type": "ImageObject", "url": "[logo url]" }
      },
      "mainEntityOfPage": "https://[domain]/article-url"
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://[domain]/" },
        { "@type": "ListItem", "position": 2, "name": "Articles", "item": "https://[domain]/articles/" }
      ]
    }
  ]
}
</script>
```

For Next.js, extract into a `<JsonLd>` component:
```typescript
// src/components/JsonLd.tsx
export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
```

#### E. Meta tags

Ensure every HTML page has:

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Specific Page Title] — [Site Name]</title>
<meta name="description" content="[160 char description]">
<meta name="robots" content="index, follow, max-image-preview:large">

<!-- OG -->
<meta property="og:title" content="[Title]">
<meta property="og:description" content="[Description]">
<meta property="og:url" content="https://[domain]/[path]">
<meta property="og:image" content="https://[domain]/og-image.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="[Site Name]">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[Title]">
<meta name="twitter:description" content="[Description]">
<meta name="twitter:image" content="https://[domain]/og-image.png">

<!-- Canonical -->
<link rel="canonical" href="https://[domain]/[path]">
```

For Next.js, use the `metadata` export in `layout.tsx`:
```typescript
export const metadata: Metadata = {
  metadataBase: new URL('https://[domain]'),
  title: { default: '[Site Name]', template: '%s — [Site Name]' },
  description: '[Description]',
  openGraph: {
    title: '[Site Name]',
    description: '[Description]',
    url: 'https://[domain]',
    siteName: '[Site Name]',
    images: ['/og-image.png'],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: '[Site Name]',
    description: '[Description]',
    images: ['/og-image.png'],
  },
  alternates: { canonical: 'https://[domain]' },
};
```

### 4. Report what was done

Format as a checklist:

```
## SEO Setup: [Project Name]

### Generated
✓ public/sitemap.xml (12 URLs)
✓ public/robots.txt (with AI crawler allowlist)
✓ public/llms.txt
✓ JSON-LD: Organization schema added to layout

### Already present
✓ OG meta tags
✓ Canonical URL
✓ Twitter cards

### Needs attention
⚠ Missing og-image.png — run /og-image to generate
⚠ Logo URL is a placeholder — update to real logo
```

### 5. Remind about verification

After deploying, verify with:
- Google Rich Results Test: https://search.google.com/test/rich-results
- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
- LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/

## Rules
- Never invent content — if description, tagline, or features are missing, ask
- Always use absolute URLs in sitemap and JSON-LD (not relative paths)
- Explicitly allow AI crawlers (GPTBot, ClaudeBot, Claude-SearchBot, PerplexityBot) — AI search is now a real traffic source, so opt in unless the user says otherwise
- For blogs/articles, use the @graph array to combine Article + BreadcrumbList
- Don't add JSON-LD for content that doesn't exist yet (e.g., don't add Article schema to a homepage)
- Match framework patterns: don't add `public/sitemap.xml` to a Next.js project, use `src/app/sitemap.ts`
- Keep llms.txt concise (under 500 words) — it's for AI skim, not humans
