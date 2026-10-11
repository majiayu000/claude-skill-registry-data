---
name: meta-tags
description: Meta tags, Open Graph, Twitter Cards, and Next.js Metadata API patterns. This skill should be used when the user asks about "meta tags", "Open Graph", "og:image", "Twitter Card", "social sharing preview", "generateMetadata", "metadata API", "canonical URL", "OG image generation", "opengraph-image.tsx", or needs to configure page-level metadata for SEO and social sharing.
---

# Meta Tags & Social Sharing

Next.js App Router provides a first-class Metadata API that replaces the `<Head>`-style helpers of older SEO packages (the `NextSeo` / `DefaultSeo` components of `next-seo` v6 were built for the Pages Router). Export a `metadata` object or `generateMetadata` function from any `layout.tsx` or `page.tsx`.

## Static Metadata

Use for pages with fixed content (home, about, contact):

```tsx
// app/about/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us',        // Becomes "About Us | Site Name" via template
  description: 'Learn about our team and mission. We build tools for developers.',
  openGraph: {
    title: 'About Us',
    description: 'Learn about our team and mission.',
    url: '/about',
    type: 'website',
    images: [{ url: '/og/about.png', width: 1200, height: 630, alt: 'About Us' }],
  },
  twitter: {
    card: 'summary_large_image',
  },
  alternates: {
    canonical: '/about',
  },
}
```

## Dynamic Metadata (generateMetadata)

Use for pages with dynamic content (blog posts, products, profiles):

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'

interface Props {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)
  if (!post) return {}

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      url: `/blog/${slug}`,
      type: 'article',
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      authors: [post.author.name],
      images: [{ url: post.image, width: 1200, height: 630, alt: post.title }],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
    alternates: {
      canonical: `/blog/${slug}`,
    },
  }
}
```

The fetch inside `generateMetadata` is automatically memoized with the page component — no duplicate requests.

## Title Template

Set in the root layout. Child pages only provide the page-specific part:

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    template: '%s | Acme',    // "About | Acme", "Blog | Acme"
    default: 'Acme',          // Used when child doesn't set title
  },
}

// app/about/page.tsx
export const metadata: Metadata = {
  title: 'About',  // Renders as "About | Acme"
}
```

Nested layouts can override the template for their section:
```tsx
// app/blog/layout.tsx
export const metadata: Metadata = {
  title: {
    template: '%s | Acme Blog',
    default: 'Acme Blog',
  },
}
```

## Open Graph Tags

### Required Properties

| Property | Description | Length |
|----------|-------------|-------|
| `og:title` | Page title for social sharing | 40-60 chars |
| `og:description` | Summary for social cards | 150-200 chars |
| `og:image` | Preview image URL (must be absolute) | - |
| `og:url` | Canonical page URL | - |
| `og:type` | Content type: `website`, `article`, `product` | - |
| `og:site_name` | Your site name | - |

### Image Specifications

| Platform | Size | Ratio | Format |
|----------|------|-------|--------|
| Universal | 1200 x 630 px | 1.91:1 | PNG or JPG |
| Twitter/X large | 1200 x 675 px | 16:9 | PNG or JPG |
| Minimum | 600 x 315 px | 1.91:1 | PNG or JPG |

Use **1200 x 630** for universal compatibility. Keep file size under 300KB (max 8MB). URL must be absolute HTTPS.

## Twitter Cards

```tsx
twitter: {
  card: 'summary_large_image',   // Large image preview
  // card: 'summary',            // Small square thumbnail
  title: 'Page Title',
  description: 'Page description',
  images: ['https://example.com/og.png'],
  creator: '@username',           // Optional: tweet author
  site: '@sitename',              // Optional: site account
}
```

If `twitter` fields are omitted, Next.js falls back to `openGraph` values automatically.

## Dynamic OG Image Generation

Generate OG images on-the-fly with `opengraph-image.tsx`. No external service needed:

```tsx
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'

export const alt = 'Blog post preview'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)

  return new ImageResponse(
    (
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: '#0a0a0a',
          color: '#ffffff',
          padding: 60,
        }}
      >
        <div style={{ fontSize: 56, fontWeight: 700 }}>{post.title}</div>
        <div style={{ fontSize: 28, color: '#888', marginTop: 20 }}>
          {post.excerpt}
        </div>
      </div>
    ),
    { ...size }
  )
}
```

The image is auto-linked in the page's `<head>` — no manual `openGraph.images` needed when using file-based convention.

### Custom Fonts in OG Images

```tsx
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'

export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const font = await readFile(join(process.cwd(), 'assets/Inter-Bold.ttf'))

  return new ImageResponse(
    (<div style={{ fontSize: 48, fontFamily: 'Inter' }}>Title</div>),
    {
      ...size,
      fonts: [{ name: 'Inter', data: font, style: 'normal', weight: 700 }],
    }
  )
}
```

## Twitter Image Convention

Similarly, create `twitter-image.tsx` for a Twitter-specific card image:

```tsx
// app/twitter-image.tsx
import { ImageResponse } from 'next/og'

export const alt = 'Site Name'
export const size = { width: 1200, height: 675 }
export const contentType = 'image/png'

export default function Image() {
  return new ImageResponse(
    (<div style={{ /* ... */ }}>Site Name</div>),
    { ...size }
  )
}
```

## Canonical URLs

Set canonical on every page to prevent duplicate content:

```tsx
alternates: {
  canonical: '/blog/my-post',       // Relative to metadataBase
  // canonical: 'https://example.com/blog/my-post',  // Or absolute
}
```

For paginated content:
```tsx
alternates: {
  canonical: '/blog',
  // No rel=prev/next needed — Google ignores them since 2019
}
```

## Validation Checklist

After implementing metadata, verify:

1. **Rendered DOM** — check `<title>`, `<meta name="description">`, OG tags in the rendered page. Since Next.js 15.2 `generateMetadata` output can be streamed: on request-time rendered pages, crawlers that execute JavaScript (Googlebot) get the tags appended to `<body>` after the first UI, so "View source" may not show them where you expect. Prerendered pages whose `generateMetadata` adds no dynamic behavior keep their metadata in the initial `<head>`. Use Google Search Console URL Inspection (rendered HTML), DevTools Elements, or Playwright `page.title()` / `page.locator('meta[...]')`.
2. **Social crawlers get `<head>` metadata** — HTML-limited bots that cannot run JavaScript (`facebookexternalhit`, `Twitterbot`, `LinkedInBot`, `Slackbot`, `Bingbot`, `DuckDuckBot` and the other bots on Next.js's default list; Googlebot is not on it) receive blocking metadata inside `<head>`. Check the raw HTML as they see it:
   ```bash
   curl -sA "facebookexternalhit/1.1" https://example.com/blog/my-post | grep -iE "<title|og:|twitter:"
   curl -sA "Twitterbot/1.0" https://example.com/blog/my-post | grep -iE "twitter:|og:"
   ```
3. **Facebook Sharing Debugger** — test OG preview (developers.facebook.com/tools/debug/)
4. **X card preview** — the standalone Twitter Card Validator was retired in 2022 and its old URL no longer shows a validator. Paste the URL into the X post composer to see the card preview, or use a third-party OG/Twitter-card checker. The `twitter:card` and `og:*` tags are still read.
5. **LinkedIn Post Inspector** — test LinkedIn preview
6. **Google Rich Results Test** — check structured data (separate from meta tags)

### Streaming metadata and `htmlLimitedBots`

Next.js detects HTML-limited bots by User-Agent and keeps blocking `<head>` metadata for them. If a social or SEO crawler that you depend on is missing from the default list, add it with `htmlLimitedBots` in `next.config.ts`:

```ts
// next.config.ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  // ABBREVIATED sample. A custom value REPLACES the default User-Agent list, it does not extend it:
  // start from the full default regex in html-bots.ts (packages/next/src/shared/lib/router/utils/
  // in the Next.js repo) and append your own crawler.
  htmlLimitedBots: /facebookexternalhit|Twitterbot|LinkedInBot|Slackbot|Bingbot|MyCustomBot/i,
}

export default config
```

Because the sample above drops every default bot it does not list (Google's `*-Google` / `Google-*` tools, DuckDuckBot, Discordbot, WhatsApp, Applebot and more), a copy-pasted abbreviated regex would silently stream metadata to those bots. Copy the full default first.

`htmlLimitedBots: /.*/` turns streaming metadata off for every visitor (metadata always in `<head>`), at the cost of slower responses. The default is right for most sites. Under Cache Components, a `generateMetadata` that depends on external data but not on request data should use `'use cache'` so metadata stays part of the static shell; `metadataBase` must then be returned as a string (`url.toString()`), because `URL` instances are not serializable.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `metadataBase` | Set in root layout — OG images need absolute URLs |
| Exporting both `metadata` and `generateMetadata` | Use only one per file — both cause a build error |
| Relative `og:image` without `metadataBase` | Always set `metadataBase` or use absolute URLs |
| Description too long (>160 chars) | Keep 150-160 chars — Google truncates longer text |
| Title too long (>60 chars) | Keep 50-60 chars — search engines truncate |
| Same title/description on all pages | Each page needs unique metadata |