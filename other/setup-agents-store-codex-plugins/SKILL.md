---
name: setup
description: SEO setup and initial audit for Next.js projects. This skill should be used when the user asks to "set up SEO", "add SEO to my project", "audit SEO", "check SEO setup", "initialize SEO", "configure metadata", or wants to verify their Next.js project has proper SEO foundations in place.
---

# SEO Setup & Initial Audit

Verify and establish SEO foundations for a Next.js App Router project. Run this before implementing specific SEO features.

## Step 1: Audit Current State

Check the project for existing SEO infrastructure:

```bash
# Check for metadata in root layout
grep -r "metadata" src/app/layout.tsx || echo "NO metadata export found"

# Check for sitemap
ls src/app/sitemap.ts 2>/dev/null || ls app/sitemap.ts 2>/dev/null || echo "NO sitemap.ts found"

# Check for robots
ls src/app/robots.ts 2>/dev/null || ls app/robots.ts 2>/dev/null || echo "NO robots.ts found"

# Check for existing SEO packages
grep -E "next-seo|next-sitemap|schema-dts" package.json || echo "No SEO packages installed"

# Check metadataBase
grep -r "metadataBase" src/app/layout.tsx || echo "NO metadataBase set"
```

Report which items are missing before proceeding.

## Step 2: Install Dependencies

Only one package is needed — `schema-dts` provides TypeScript types for Schema.org structured data (zero bundle impact, types only):

```bash
pnpm add -D schema-dts
```

`next-seo` is not needed. Meta tags (`<title>`, description, Open Graph, canonical) come from the built-in Next.js Metadata API — do not use the Pages Router `NextSeo` / `DefaultSeo` components in an App Router project. `next-seo` v7 (7.3.0, July 2026) is actively maintained, but it is now a library of JSON-LD components (`ArticleJsonLd`, `ProductJsonLd`, ...). It is an optional alternative to the hand-written `JsonLd` component + `schema-dts` types taught in the `structured-data` skill; if the project already uses it, keep it rather than rewriting. Do NOT install `next-sitemap` unless the project has complex dynamic sitemap requirements that exceed built-in `sitemap.ts` capabilities.

## Step 3: Set metadataBase in Root Layout

The root layout MUST set `metadataBase` — all relative OG image URLs resolve against it:

```tsx
// app/layout.tsx (or src/app/layout.tsx)
import type { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'
  ),
  title: {
    template: '%s | Site Name',
    default: 'Site Name',
  },
  description: 'Site description for search engines',
}
```

Add `NEXT_PUBLIC_SITE_URL` to `.env`:
```
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
```

## Step 4: Create robots.ts

```tsx
// app/robots.ts
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://yourdomain.com'
  const isProduction = process.env.NODE_ENV === 'production'

  if (!isProduction) {
    return { rules: { userAgent: '*', disallow: ['/'] } }
  }

  return {
    rules: [
      { userAgent: '*', allow: '/', disallow: ['/api/', '/admin/'] },
      { userAgent: 'GPTBot', disallow: ['/'] },
      { userAgent: 'CCBot', disallow: ['/'] },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  }
}
```

Block AI training crawlers (GPTBot, CCBot) by default — most sites do not want their content used for AI training. Remove these rules if the site explicitly opts in.

## Step 5: Create sitemap.ts

```tsx
// app/sitemap.ts
import type { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://yourdomain.com'

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    { url: baseUrl, lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
    { url: `${baseUrl}/about`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
  ]

  // Dynamic pages — fetch from your CMS/database
  // const posts = await getAllPosts()
  // const dynamicPages = posts.map(post => ({
  //   url: `${baseUrl}/blog/${post.slug}`,
  //   lastModified: new Date(post.updatedAt),
  //   changeFrequency: 'weekly' as const,
  //   priority: 0.7,
  // }))

  return [...staticPages]
}
```

## Step 6: Google Search Console Verification

Add the verification tag to root layout metadata:

```tsx
export const metadata: Metadata = {
  // ... other metadata
  verification: {
    google: 'your-google-verification-code',
    // yandex: 'yandex-code',
  },
}
```

## Step 7: Verify Setup

After setup, confirm all pieces are in place:

1. Run `pnpm build` — no metadata errors
2. Visit `http://localhost:3000/sitemap.xml` — valid XML
3. Visit `http://localhost:3000/robots.txt` — correct rules
4. Inspect the rendered page (DevTools Elements, Search Console URL Inspection, or Playwright) — `<title>`, `<meta name="description">`, and resolved absolute `og:image` URLs present. on request-time rendered pages Next.js 15.2+ streams `generateMetadata` output into `<body>` for JavaScript-capable crawlers (prerendered pages with a non-dynamic `generateMetadata` keep it in the initial `<head>`); `curl` shows streamed metadata in `<head>` only for HTML-limited bots (see the `meta-tags` skill)
5. Check `<link rel="canonical">` on each page

## SEO Setup Checklist

| Item | Status | Priority |
|------|--------|----------|
| `metadataBase` in root layout | Required | Critical |
| Title template in root layout | Required | Critical |
| Default description in root layout | Required | Critical |
| `robots.ts` created | Required | Critical |
| `sitemap.ts` created | Required | Critical |
| `schema-dts` installed | Recommended | High |
| Google Search Console verification | Recommended | High |
| `NEXT_PUBLIC_SITE_URL` env var | Required | Critical |
| Canonical URLs on all pages | Required | High |
| OG images configured | Recommended | Medium |

## What This Skill Does NOT Cover

- Specific metadata patterns for individual pages — see `meta-tags` skill
- Structured data (JSON-LD) implementation — see `structured-data` skill
- Performance optimization — see `performance` skill
- Content optimization — see `content-seo` skill