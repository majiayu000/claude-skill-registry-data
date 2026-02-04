---
name: seo-2025-patterns
description: 2025 SEO best practices for Next.js including Core Web Vitals (INP replaces FID), E-E-A-T signals, Schema markup, AI content guidelines, and technical SEO. Use when optimizing pages for search engines, implementing metadata, adding structured data, or improving page speed.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# SEO 2025 Patterns

**Purpose:** Implement 2025 SEO best practices for Next.js applications to maximize search visibility and organic traffic.

**Activation Triggers:**
- Optimizing pages for search engines
- Implementing metadata and Open Graph
- Adding Schema.org structured data
- Improving Core Web Vitals
- E-E-A-T signal implementation
- Sitemap and robots.txt setup
- Meta description optimization

**Key Resources:**
- `scripts/seo-audit.sh` - Comprehensive SEO audit script
- `scripts/validate-schema.sh` - Validate JSON-LD structured data
- `templates/metadata-patterns.tsx` - Next.js Metadata API patterns
- `templates/schema-components.tsx` - JSON-LD schema components
- `examples/complete-seo-setup.md` - Full SEO implementation example

## 2025 SEO Landscape

### Key Changes from 2024

1. **INP Replaces FID** - Interaction to Next Paint is now a Core Web Vital
2. **AI Content Guidelines** - Google rewards helpful AI content with human oversight
3. **E-E-A-T Enhanced** - "Experience" added as first factor
4. **Passage Ranking** - Google indexes specific passages
5. **Video SEO** - Video snippets dominate SERPs
6. **Zero-Click Optimization** - Featured snippets and AI Overviews

### Core Web Vitals Targets (2025)

| Metric | Target | What It Measures |
|--------|--------|------------------|
| LCP | < 2.5s | Largest Contentful Paint |
| INP | < 200ms | Interaction to Next Paint |
| CLS | < 0.1 | Cumulative Layout Shift |

## Next.js Metadata API

### Basic Metadata Configuration

```typescript
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: {
    default: 'Site Name - Main Tagline',
    template: '%s | Site Name',
  },
  description: 'Your site description for search engines (150-160 characters)',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  authors: [{ name: 'Author Name', url: 'https://author.com' }],
  creator: 'Creator Name',
  publisher: 'Publisher Name',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
}
```

### Open Graph Configuration

```typescript
export const metadata: Metadata = {
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://example.com',
    siteName: 'Site Name',
    title: 'Page Title for Social Sharing',
    description: 'Description for social media (150-200 chars)',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'OG Image Alt Text',
      },
    ],
  },
}
```

### Twitter Card Configuration

```typescript
export const metadata: Metadata = {
  twitter: {
    card: 'summary_large_image',
    site: '@sitehandle',
    creator: '@creatorhandle',
    title: 'Title for Twitter',
    description: 'Description for Twitter (150-200 chars)',
    images: ['/twitter-image.png'],
  },
}
```

### Robots Configuration

```typescript
export const metadata: Metadata = {
  robots: {
    index: true,
    follow: true,
    nocache: false,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}
```

### Dynamic Metadata

```typescript
// app/blog/[slug]/page.tsx
import type { Metadata, ResolvingMetadata } from 'next'

type Props = {
  params: { slug: string }
}

export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const post = await getPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      authors: [post.author.name],
      images: [
        {
          url: post.coverImage,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
  }
}
```

## Dynamic Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/pricing`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.9,
    },
  ]

  // Dynamic pages from database
  const posts = await getAllPosts()
  const postPages: MetadataRoute.Sitemap = posts.map((post) => ({
    url: `${baseUrl}/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }))

  return [...staticPages, ...postPages]
}
```

## Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://example.com'

  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/admin/', '/_next/', '/private/'],
      },
      {
        userAgent: 'GPTBot',
        disallow: '/', // Block AI training crawlers if desired
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  }
}
```

## Schema.org Structured Data

### Organization Schema

```typescript
// components/seo/OrganizationSchema.tsx
export function OrganizationSchema() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Company Name',
    url: 'https://example.com',
    logo: 'https://example.com/logo.png',
    sameAs: [
      'https://twitter.com/company',
      'https://linkedin.com/company/company',
      'https://github.com/company',
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+1-555-555-5555',
      contactType: 'customer service',
      availableLanguage: ['English'],
    },
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}
```

### Article Schema

```typescript
// components/seo/ArticleSchema.tsx
interface ArticleSchemaProps {
  title: string
  description: string
  image: string
  author: { name: string; url: string }
  publishedAt: string
  updatedAt: string
  url: string
}

export function ArticleSchema(props: ArticleSchemaProps) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: props.title,
    description: props.description,
    image: props.image,
    author: {
      '@type': 'Person',
      name: props.author.name,
      url: props.author.url,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Company Name',
      logo: {
        '@type': 'ImageObject',
        url: 'https://example.com/logo.png',
      },
    },
    datePublished: props.publishedAt,
    dateModified: props.updatedAt,
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': props.url,
    },
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}
```

### FAQ Schema

```typescript
// components/seo/FAQSchema.tsx
interface FAQItem {
  question: string
  answer: string
}

export function FAQSchema({ items }: { items: FAQItem[] }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}
```

### Breadcrumb Schema

```typescript
// components/seo/BreadcrumbSchema.tsx
interface BreadcrumbItem {
  name: string
  url: string
}

export function BreadcrumbSchema({ items }: { items: BreadcrumbItem[] }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  )
}
```

## Core Web Vitals Optimization

### LCP Optimization

```typescript
// Prioritize above-fold images
import Image from 'next/image'

// Hero image with priority
<Image
  src="/hero.jpg"
  alt="Hero description"
  width={1200}
  height={600}
  priority  // Preloads image for LCP
  sizes="(max-width: 768px) 100vw, 1200px"
/>
```

### Font Optimization

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Prevents CLS
  preload: true,
  variable: '--font-inter',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  )
}
```

### Script Optimization

```typescript
import Script from 'next/script'

// Defer non-critical scripts
<Script
  src="https://analytics.example.com/script.js"
  strategy="lazyOnload"  // Load after page is interactive
/>

// Load immediately for critical scripts
<Script
  src="https://critical.example.com/script.js"
  strategy="afterInteractive"
/>
```

## E-E-A-T Signals

### Author Information

```typescript
// components/AuthorBio.tsx
export function AuthorBio({ author }) {
  return (
    <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
      <Image
        src={author.avatar}
        alt={author.name}
        width={64}
        height={64}
        className="rounded-full"
      />
      <div>
        <h3 className="font-semibold">{author.name}</h3>
        <p className="text-sm text-muted-foreground">{author.title}</p>
        <p className="text-sm">{author.bio}</p>
        <div className="flex gap-2 mt-2">
          <a href={author.twitter}>Twitter</a>
          <a href={author.linkedin}>LinkedIn</a>
        </div>
      </div>
    </div>
  )
}
```

### Trust Signals

- Clear contact information
- Privacy policy and terms of service
- About page with company information
- Author pages with credentials
- Published and updated dates
- HTTPS everywhere

## SEO Audit Checklist

```bash
# Run comprehensive SEO audit
./scripts/seo-audit.sh

# Checks:
# ✓ All pages have unique titles
# ✓ All pages have meta descriptions
# ✓ Open Graph tags present
# ✓ Twitter cards configured
# ✓ Sitemap.xml exists and valid
# ✓ Robots.txt configured
# ✓ Schema markup valid
# ✓ Images have alt text
# ✓ Heading hierarchy correct
# ✓ Internal linking structure
```

## Testing Tools

- **Google Search Console** - Monitor indexing and search performance
- **PageSpeed Insights** - Core Web Vitals measurement
- **Rich Results Test** - Validate structured data
- **Mobile-Friendly Test** - Mobile compatibility
- **Schema.org Validator** - Validate JSON-LD
