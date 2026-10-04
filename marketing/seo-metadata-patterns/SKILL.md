---
name: seo-metadata-patterns
description: Complete SEO patterns for Next.js — Metadata API, Open Graph, Twitter cards, JSON-LD structured data, sitemap, and robots.txt. Use when shipping any public-facing page.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# SEO & Metadata Patterns

## Purpose
Ensure every public-facing page has proper SEO metadata, social sharing cards, and structured data. These patterns work with Next.js App Router's Metadata API.

## When to Use This Skill
- Shipping any page that will be publicly accessible
- Setting up social sharing (OG images, Twitter cards)
- Adding structured data for rich search results
- Generating sitemaps and robots.txt

## Output Format / Delivery
Provide highly optimized, crawlable, and fully compliant SEO metadata, Open Graph configs, sitemap generators, and JSON-LD structured schemas.

## Behavior Rules
1. **Never use generic or duplicate metadata descriptions** across distinct routes — always tail-cut descriptions to 120-160 characters.
2. **Always define metadataBase in layout.tsx** before exporting dynamic relative URLs.
3. **Never allow indexable staging or admin environments** — always exclude them in `robots.ts` or with `noindex` headers.

## Maintenance Notes
This skill is locked for standard Next.js App Router metadata features. Update if Next.js introduces new Metadata API abstractions.

---

## Phase 1: Metadata API (Next.js)

### Static Metadata (Most Pages)
```tsx
// app/page.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Product Name — Clear Value Proposition",
  description: "A compelling description (120-160 chars) that accurately describes the page content and includes primary keywords naturally.",
  keywords: ["saas", "product", "solution"],

  openGraph: {
    title: "Product Name — Clear Value Proposition",
    description: "OG description for social sharing. Can differ from meta description.",
    url: "https://product.com",
    siteName: "Product Name",
    locale: "en_US",
    type: "website",
    images: [{
      url: "https://product.com/og-image.png",
      width: 1200,
      height: 630,
      alt: "Product Name — descriptive alt text",
    }],
  },

  twitter: {
    card: "summary_large_image",
    title: "Product Name — Clear Value Proposition",
    description: "Twitter card description.",
    images: ["https://product.com/og-image.png"],
    creator: "@handle",
  },

  robots: { index: true, follow: true },

  alternates: {
    canonical: "https://product.com",
  },
};
```

### Root Layout Metadata (Global Defaults)
```tsx
// app/layout.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  metadataBase: new URL("https://product.com"),
  title: {
    template: "%s — Product Name",  // Dynamic: page title replaces %s
    default: "Product Name",         // Fallback
  },
  description: "Default description for pages without their own.",
};
```

### Page-Level Title Override
```tsx
// app/pricing/page.tsx
export const metadata = {
  title: "Pricing",  // Renders as "Pricing — Product Name" via template
};
```

---

## Phase 2: Dynamic Metadata (Blog Posts, Products)

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from "next";

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);

  if (!post) return { title: "Not Found" };

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: "article",
      publishedTime: post.publishedAt,
      authors: [post.author.name],
      images: [{
        url: post.coverImage,
        width: 1200,
        height: 630,
        alt: post.title,
      }],
    },
  };
}
```

---

## Phase 3: JSON-LD Structured Data

### Organization Schema (Root Layout)
```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Product Name",
    url: "https://product.com",
    logo: "https://product.com/logo.png",
    sameAs: [
      "https://twitter.com/product",
      "https://github.com/product",
    ],
  };

  return (
    <html lang="en">
      <body>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        {children}
      </body>
    </html>
  );
}
```

### Product Schema (Pricing Page)
```tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Product Name",
  applicationCategory: "BusinessApplication",
  offers: {
    "@type": "AggregateOffer",
    lowPrice: "29",
    highPrice: "199",
    priceCurrency: "USD",
    offerCount: "3",
  },
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: "4.8",
    reviewCount: "2847",
  },
};
```

### Article Schema (Blog Posts)
```tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "Article",
  headline: post.title,
  description: post.excerpt,
  image: post.coverImage,
  datePublished: post.publishedAt,
  dateModified: post.updatedAt,
  author: {
    "@type": "Person",
    name: post.author.name,
  },
  publisher: {
    "@type": "Organization",
    name: "Product Name",
    logo: { "@type": "ImageObject", url: "https://product.com/logo.png" },
  },
};
```

---

## Phase 4: Sitemap Generation

```tsx
// app/sitemap.ts
import type { MetadataRoute } from "next";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts();

  const staticRoutes: MetadataRoute.Sitemap = [
    { url: "https://product.com", lastModified: new Date(), changeFrequency: "weekly", priority: 1 },
    { url: "https://product.com/pricing", lastModified: new Date(), changeFrequency: "monthly", priority: 0.8 },
    { url: "https://product.com/about", lastModified: new Date(), changeFrequency: "monthly", priority: 0.5 },
  ];

  const blogRoutes: MetadataRoute.Sitemap = posts.map((post) => ({
    url: `https://product.com/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: "weekly" as const,
    priority: 0.6,
  }));

  return [...staticRoutes, ...blogRoutes];
}
```

---

## Phase 5: Robots.txt

```tsx
// app/robots.ts
import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/", "/dashboard/", "/_next/"],
      },
    ],
    sitemap: "https://product.com/sitemap.xml",
  };
}
```

---

## Phase 6: SEO Checklist

### Per-Page Requirements
- [ ] `<title>` is unique, descriptive, 50-60 characters
- [ ] `<meta description>` is unique, compelling, 120-160 characters
- [ ] One `<h1>` per page, matches the page topic
- [ ] Heading hierarchy is logical (h1 → h2 → h3, no skips)
- [ ] Images have descriptive `alt` text
- [ ] Internal links use meaningful anchor text (not "click here")
- [ ] `canonical` URL is set to prevent duplicate content
- [ ] OG image is 1200×630px with readable text at small sizes

### Site-Wide Requirements
- [ ] `sitemap.xml` is generated and includes all public routes
- [ ] `robots.txt` exists and allows crawling of public pages
- [ ] JSON-LD Organization schema on root layout
- [ ] All pages have unique titles (no duplicates)
- [ ] No orphan pages (every page is linked from at least one other page)
- [ ] Page load time < 3s on mobile (LCP)
