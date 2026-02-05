---
name: nextjs-metadata
description: Next.js Metadata API for SEO, OpenGraph tags, structured data, and social sharing. Use when implementing metadata, SEO, or social media previews.
---

# Next.js Metadata

Expert guidance for implementing effective metadata in Next.js.

## Quick Reference

| Concern | Solution | Example |
|---------|----------|---------|
| Page title | metadata object | `export const metadata = { title: '...' }` |
| Dynamic metadata | generateMetadata function | `export async function generateMetadata({ params })` |
| OpenGraph images | metadata.images | `openGraph: { images: ['/og.jpg'] }` |
| Structured data | Script component | `<Script type="application/ld+json">` |
| Canonical URLs | metadata.alternates | `canonical: 'https://...'` |
| Twitter cards | metadata.twitter | `twitter: { card: 'summary_large_image' }` |

## What Do You Need?

1. **Static metadata** - metadata object for fixed values
2. **Dynamic metadata** - generateMetadata for dynamic values
3. **OpenGraph** - Social sharing images and descriptions
4. **Structured data** - JSON-LD for rich results
5. **Canonical URLs** - Preventing duplicate content

Specify a number or describe your metadata scenario.

## Routing

| Response | Reference to Read |
|----------|-------------------|
| 1, "static", "metadata", "object" | [static-metadata.md](./references/static-metadata.md) |
| 2, "dynamic", "generatemetadata", "params" | [dynamic-metadata.md](./references/dynamic-metadata.md) |
| 3, "opengraph", "social", "sharing" | [opengraph.md](./references/opengraph.md) |
| 4, "structured", "json-ld", "schema" | [structured-data.md](./references/structured-data.md) |
| 5, "canonical", "seo", "duplicate" | [seo.md](./references/seo.md) |

## Essential Principles

**Every page needs metadata**: Title, description, OpenGraph image minimum.

**Static for static pages**: Use metadata object when values don't change.

**Dynamic for dynamic routes**: Use generateMetadata when data comes from params or fetch.

**OpenGraph for sharing**: Ensure pages look good when shared on social media.

**Structured data for rich results**: Use JSON-LD for articles, products, organizations.

## Code Patterns

### Static Metadata
```typescript
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My App',
  description: 'Description for search engines',
  openGraph: {
    title: 'My App',
    description: 'Description for social sharing',
    images: ['/og-image.jpg'],
  },
}

export default function Page() {
  return <div>...</div>
}
```

### Dynamic Metadata
```typescript
// app/blog/[slug]/page.tsx
import { Metadata } from 'next'

export async function generateMetadata(
  { params }: { params: { slug: string } }
): Promise<Metadata> {
  const post = await fetchPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      images: [post.ogImage],
    },
  }
}

export default function BlogPost({ params }: { params: { slug: string } }) {
  // ...
}
```

### Structured Data
```typescript
import Script from 'next/script'

export default function ArticlePage({ post }: { post: Post }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    datePublished: post.publishedAt,
    author: { '@type': 'Person', name: post.author.name },
  }

  return (
    <>
      <Script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <article>{post.content}</article>
    </>
  )
}
```

## Metadata Checklist

| Element | Required | Format |
|---------|----------|--------|
| title | Yes | string or Metadata.title |
| description | Yes | string (~160 chars) |
| openGraph:title | Yes | string |
| openGraph:description | Yes | string |
| openGraph:image | Yes | string or array (1200x630px min) |
| twitter:card | Recommended | 'summary_large_image' |
| canonical | Recommended | string |
| alternates:languages | Optional | Record<locale, string> |

## Common Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| Missing page title | High | Add metadata.title |
| No OpenGraph image | Medium | Add openGraph.images |
| No description | Medium | Add metadata.description |
| Dynamic not using generateMetadata | High | Change to async function |
| Duplicate content (no canonical) | Medium | Add metadata.canonical |
| Small OG image (< 1200x630) | Low | Use larger image |

## Reference Index

| File | Topics |
|------|--------|
| [static-metadata.md](./references/static-metadata.md) | metadata object, all options |
| [dynamic-metadata.md](./references/dynamic-metadata.md) | generateMetadata, params, fetch |
| [opengraph.md](./references/opengraph.md) | OG tags, Twitter cards, images |
| [structured-data.md](./references/structured-data.md) | JSON-LD, Script component, schemas |
| [seo.md](./references/seo.md) | Canonical, hreflang, robots, sitemap |

## Success Criteria

Metadata is complete when:
- Every page has title and description
- OpenGraph tags present (title, description, image)
- OG image is 1200x630px minimum
- Dynamic routes use generateMetadata
- Canonical URLs set for duplicate content
- Structured data for content types (articles, products)
