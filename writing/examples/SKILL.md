---
name: examples
description: Complete SEO recipes and implementation examples for Next.js App Router. This skill should be used when the user asks for "SEO example", "blog SEO setup", "e-commerce SEO", "landing page SEO", "SaaS SEO", "full SEO implementation", "SEO recipe", "SEO template", or needs a complete, copy-paste ready SEO implementation for a specific page type.
---

# SEO Examples & Recipes

Complete, production-ready SEO implementations for common page types. Each recipe includes metadata, structured data, and component patterns.

## Recipe 1: Blog with Article Schema

### Root Layout (Sitewide SEO)

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { JsonLd } from '@/components/json-ld'
import { createOrganization } from '@/lib/schema'

const inter = Inter({ subsets: ['latin'], display: 'swap', variable: '--font-sans' })

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://yourblog.com'

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { template: '%s | Your Blog', default: 'Your Blog' },
  description: 'Insights on web development, SEO, and modern tooling.',
  openGraph: {
    type: 'website',
    siteName: 'Your Blog',
    locale: 'en_US',
  },
  twitter: { card: 'summary_large_image' },
  alternates: { types: { 'application/rss+xml': '/feed.xml' } },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <JsonLd data={createOrganization({
          name: 'Your Blog', logo: `${SITE_URL}/logo.png`, url: SITE_URL,
          sameAs: ['https://twitter.com/yourblog', 'https://github.com/yourblog'],
        })} />
        {children}
      </body>
    </html>
  )
}
```

### Home Page (Site Name)

Google reads `WebSite` markup (the site name) from the home page only, so it lives in `app/page.tsx`, not in the root layout:

```tsx
// app/page.tsx
import { JsonLd } from '@/components/json-ld'
import { createWebSite } from '@/lib/schema'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://yourblog.com'

export default function HomePage() {
  return (
    <>
      <JsonLd data={createWebSite(SITE_URL, 'Your Blog')} />
      {/* post list */}
    </>
  )
}
```

### Blog Post Page

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'
import Image from 'next/image'
import { JsonLd } from '@/components/json-ld'
import { createArticle, createBreadcrumbList } from '@/lib/schema'
import { Breadcrumbs } from '@/components/breadcrumbs'
import sanitizeHtml from 'sanitize-html' // npm i sanitize-html @types/sanitize-html

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL!

interface Props { params: Promise<{ slug: string }> }

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
    alternates: { canonical: `/blog/${slug}` },
  }
}

export async function generateStaticParams() {
  const posts = await getAllPostSlugs()
  return posts.map((slug) => ({ slug }))
}

export default async function BlogPost({ params }: Props) {
  const { slug } = await params
  const post = await getPost(slug)

  return (
    <>
      <JsonLd data={createArticle({
        headline: post.title,
        description: post.excerpt,
        image: post.image,
        datePublished: post.publishedAt,
        dateModified: post.updatedAt,
        author: { name: post.author.name, url: `${SITE_URL}/authors/${post.author.slug}` },
        url: `${SITE_URL}/blog/${slug}`,
      })} />
      <JsonLd data={createBreadcrumbList([
        { name: 'Home', url: SITE_URL },
        { name: 'Blog', url: `${SITE_URL}/blog` },
        { name: post.title, url: `${SITE_URL}/blog/${slug}` },
      ])} />

      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Blog', href: '/blog' },
        { name: post.title, href: `/blog/${slug}` },
      ]} />

      <article>
        <h1>{post.title}</h1>
        <time dateTime={post.publishedAt}>
          {new Date(post.publishedAt).toLocaleDateString()}
        </time>
        <Image
          src={post.image} alt={post.title}
          width={1200} height={630} loading="eager" fetchPriority="high"
          sizes="(max-width: 768px) 100vw, 800px"
        />
        {/* CMS HTML is untrusted input (one compromised editor account is enough for stored XSS):
            sanitize it on the server before it reaches dangerouslySetInnerHTML */}
        <div dangerouslySetInnerHTML={{ __html: sanitizeHtml(post.content, {
          allowedTags: [...sanitizeHtml.defaults.allowedTags, 'img', 'h1', 'h2'],
          allowedAttributes: { ...sanitizeHtml.defaults.allowedAttributes, img: ['src', 'alt', 'width', 'height'] },
          allowedSchemes: ['https', 'http', 'mailto'],
        }) }} />
      </article>
    </>
  )
}
```

`sanitizeHtml` drops `<script>`, `<iframe>`, event-handler attributes (`onerror`) and `javascript:` links, and keeps the headings, links and images a post needs. Storing Markdown in the CMS and rendering it with a renderer that escapes raw HTML is the alternative; `JsonLd` below escapes `<` instead because its payload is JSON, not HTML.

### Blog Sitemap

```tsx
// app/blog/sitemap.ts
import type { MetadataRoute } from 'next'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL!

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts()

  return posts.map((post) => ({
    url: `${SITE_URL}/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'weekly',
    priority: 0.7,
  }))
}
```

## Recipe 2: E-commerce Product Page

```tsx
// app/products/[slug]/page.tsx
import type { Metadata } from 'next'
import Image from 'next/image'
import { JsonLd } from '@/components/json-ld'
import { createProduct, createBreadcrumbList } from '@/lib/schema'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL!

interface Props { params: Promise<{ slug: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const product = await getProduct(slug)
  if (!product) return {}

  return {
    title: `${product.name} — ${product.brand}`,
    description: `${product.name} by ${product.brand}. ${product.shortDescription}. $${product.price}.`,
    openGraph: {
      title: product.name,
      description: product.shortDescription,
      url: `/products/${slug}`,
      type: 'website',
      images: product.images.map((img) => ({
        url: img, width: 1200, height: 630, alt: product.name,
      })),
    },
    alternates: { canonical: `/products/${slug}` },
  }
}

export default async function ProductPage({ params }: Props) {
  const { slug } = await params
  const product = await getProduct(slug)

  return (
    <>
      <JsonLd data={createProduct({
        name: product.name,
        description: product.shortDescription,
        image: product.images[0],
        price: product.price.toString(),
        currency: 'USD',
        availability: product.inStock ? 'InStock' : 'OutOfStock',
        sku: product.sku,
        brand: product.brand,
        ratingValue: product.rating?.toString(),
        reviewCount: product.reviewCount,
        url: `${SITE_URL}/products/${slug}`,
      })} />
      <JsonLd data={createBreadcrumbList([
        { name: 'Home', url: SITE_URL },
        { name: product.category, url: `${SITE_URL}/products?category=${product.categorySlug}` },
        { name: product.name, url: `${SITE_URL}/products/${slug}` },
      ])} />

      <h1>{product.name}</h1>
      <Image
        src={product.images[0]} alt={`${product.name} — ${product.brand}`}
        width={800} height={800} loading="eager" fetchPriority="high"
        sizes="(max-width: 768px) 100vw, 50vw"
      />
      <p className="text-2xl font-bold">${product.price}</p>
      <p>{product.description}</p>
    </>
  )
}
```

## Recipe 3: Landing Page

```tsx
// app/page.tsx
import type { Metadata } from 'next'
import Image from 'next/image'

export const metadata: Metadata = {
  title: 'Your Product — Tagline in 60 chars',
  description: 'Clear value proposition in 150-160 characters. Explain what the product does and who it is for.',
  openGraph: {
    title: 'Your Product — Tagline',
    description: 'Clear value proposition for social sharing.',
    url: '/',
    type: 'website',
    images: [{ url: '/og/home.png', width: 1200, height: 630, alt: 'Your Product' }],
  },
  alternates: { canonical: '/' },
}

export default function Home() {
  return (
    <>
      <section>
        <h1>Your Product Headline</h1>
        <p>Value proposition paragraph explaining the core benefit.</p>
        <Image
          src="/hero.jpg" alt="Product in action"
          width={1200} height={630} loading="eager" fetchPriority="high" sizes="100vw"
        />
      </section>

      <section>
        <h2>Features</h2>
        {/* Feature blocks with H3 subheadings */}
      </section>

      <section>
        <h2>How It Works</h2>
        {/* Step-by-step with numbered items */}
      </section>
    </>
  )
}
```

## Recipe 4: SaaS Pricing Page

```tsx
// app/pricing/page.tsx
import type { Metadata } from 'next'
import type { SoftwareApplication, WithContext } from 'schema-dts'
import { JsonLd } from '@/components/json-ld'

export const metadata: Metadata = {
  title: 'Pricing',
  description: 'Simple, transparent pricing. Free tier available. Pro from $29/mo. Enterprise custom.',
  openGraph: {
    title: 'Pricing — Your Product',
    description: 'Simple, transparent pricing for teams of all sizes.',
    url: '/pricing',
    type: 'website',
  },
  alternates: { canonical: '/pricing' },
}

export default function PricingPage() {
  const softwareSchema: WithContext<SoftwareApplication> = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'Your Product',
    operatingSystem: 'Web',
    applicationCategory: 'BusinessApplication',
    offers: [
      {
        '@type': 'Offer',
        name: 'Free',
        price: '0',
        priceCurrency: 'USD',
      },
      {
        '@type': 'Offer',
        name: 'Pro',
        price: '29',
        priceCurrency: 'USD',
        billingIncrement: 'P1M',
      },
    ],
  }

  return (
    <>
      <JsonLd data={softwareSchema} />
      <h1>Simple Pricing for Every Team</h1>
      {/* Pricing cards */}
    </>
  )
}
```

## Recipe 5: Dynamic OG Image for Any Page

```tsx
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'

export const alt = 'Blog post preview'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug)
  const font = await readFile(join(process.cwd(), 'public/fonts/Inter-Bold.ttf'))

  return new ImageResponse(
    (
      <div style={{
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
        width: '100%', height: '100%', background: '#0a0a0a', color: '#fff', padding: 60,
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={{ fontSize: 52, fontWeight: 700, lineHeight: 1.2 }}>{post.title}</div>
          <div style={{ fontSize: 24, color: '#888' }}>{post.excerpt}</div>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 20, color: '#666' }}>
          <span>{post.author.name}</span>
          <span>{new Date(post.publishedAt).toLocaleDateString()}</span>
        </div>
      </div>
    ),
    { ...size, fonts: [{ name: 'Inter', data: font, style: 'normal', weight: 700 }] }
  )
}
```

## Common Utility: schema.ts

See the `structured-data` skill for the complete `lib/schema.ts` factory functions. All recipes above import from this shared file.

## Common Utility: json-ld.tsx

```tsx
// components/json-ld.tsx
import type { Thing, WithContext } from 'schema-dts'

export function JsonLd<T extends Thing>({ data }: { data: WithContext<T> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(data).replace(/</g, '\\u003c'),
      }}
    />
  )
}
```