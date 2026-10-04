---
name: senternet-site-metatags
description: Add SEO meta tags, social cards, and schema markup.
---

# SEO Meta Tags Setup

Add comprehensive SEO meta tags, Open Graph, Twitter Card, schema.org structured data, and a reusable `MetaTags` React component.

## Steps

### 1. Update `index.html` with base meta tags

Add to `<head>`:

```html
<title>APPNAME - Tagline</title>

<!-- Primary Meta Tags -->
<meta name="title" content="APPNAME - Tagline" />
<meta name="description" content="One sentence description for search results." />
<meta name="keywords" content="keyword1, keyword2, keyword3" />
<meta name="author" content="APPNAME" />
<meta name="robots" content="index, follow" />

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website" />
<meta property="og:url" content="https://www.DOMAIN.com/" />
<meta property="og:title" content="APPNAME - Tagline" />
<meta property="og:description" content="One sentence description." />
<meta property="og:image" content="https://www.DOMAIN.com/preview.png" />
<meta property="og:image:secure_url" content="https://www.DOMAIN.com/preview.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:alt" content="APPNAME - short alt text" />
<meta property="og:site_name" content="APPNAME" />
<meta property="og:locale" content="en_US" />

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:url" content="https://www.DOMAIN.com/" />
<meta name="twitter:title" content="APPNAME - Tagline" />
<meta name="twitter:description" content="One sentence description." />
<meta name="twitter:image" content="https://www.DOMAIN.com/preview.png" />
<meta name="twitter:image:alt" content="APPNAME - short alt text" />
<meta name="twitter:creator" content="@HANDLE" />
<meta name="twitter:site" content="@HANDLE" />

<!-- PWA / Mobile -->
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
<meta name="apple-mobile-web-app-title" content="APPNAME" />
<meta name="mobile-web-app-capable" content="yes" />

<!-- Theme -->
<meta name="theme-color" content="#PRIMARY_COLOR" />
<meta name="msapplication-TileColor" content="#PRIMARY_COLOR" />

<!-- Canonical & misc -->
<link rel="canonical" href="https://www.DOMAIN.com/" />
<meta name="application-name" content="APPNAME" />
<meta name="format-detection" content="telephone=no" />

<!-- Favicon -->
<link rel="icon" type="image/png" href="/favicon.png" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="shortcut icon" href="/favicon.ico" />
```

If this is an iOS app, also add:
```html
<meta name="apple-itunes-app" content="app-id=APPSTORE_ID, app-argument=https://www.DOMAIN.com/" />
```

### 2. Add schema.org structured data in `index.html`

For an iOS app:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "APPNAME",
  "description": "Full description here.",
  "url": "https://www.DOMAIN.com/",
  "operatingSystem": "iOS",
  "applicationCategory": "UtilitiesApplication",
  "downloadUrl": "https://apps.apple.com/us/app/APPNAME/idXXXXXXXX",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "APPNAME",
  "url": "https://www.DOMAIN.com/"
}
</script>
```

For a general organization/service:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "APPNAME",
  "url": "https://www.DOMAIN.com/",
  "logo": "https://www.DOMAIN.com/logo.png",
  "sameAs": ["https://twitter.com/HANDLE", "https://instagram.com/HANDLE"]
}
</script>
```

### 3. Create `src/components/MetaTags.tsx`

A React component that dynamically updates all meta tags for each page (required for prerendering to capture correct per-page metadata):

```tsx
import { useEffect } from 'react';

interface MetaTagsProps {
  title?: string;
  description?: string;
  image?: string;
  url?: string;
  type?: string;
}

const getBaseUrl = () => {
  if (import.meta.env.VITE_BASE_URL) return import.meta.env.VITE_BASE_URL;
  if (typeof window !== 'undefined') return window.location.origin;
  return '';
};

export function MetaTags({
  title = 'APPNAME - Default Title',
  description = 'Default description.',
  image,
  url = typeof window !== 'undefined' ? getBaseUrl() + window.location.pathname : getBaseUrl(),
  type = 'website',
}: MetaTagsProps) {
  const baseUrl = getBaseUrl();
  const resolvedImage = image
    ? (image.startsWith('/') ? `${baseUrl}${image}` : image)
    : `${baseUrl}/preview.png`;

  useEffect(() => {
    const setMeta = (selector: string, content: string, isProperty = false) => {
      let el = document.querySelector(selector);
      if (!el) {
        el = document.createElement('meta');
        if (isProperty) el.setAttribute('property', selector.match(/property="([^"]+)"/)?.[1] ?? '');
        else el.setAttribute('name', selector.match(/name="([^"]+)"/)?.[1] ?? '');
        document.head.appendChild(el);
      }
      el.setAttribute('content', content);
    };
    const setLink = (rel: string, href: string) => {
      let el = document.querySelector(`link[rel="${rel}"]`);
      if (!el) { el = document.createElement('link'); el.setAttribute('rel', rel); document.head.appendChild(el); }
      el.setAttribute('href', href);
    };

    document.title = title;
    setMeta('meta[name="title"]', title);
    setMeta('meta[name="description"]', description);
    setMeta('meta[name="robots"]', 'index, follow');
    setMeta('meta[property="og:type"]', type, true);
    setMeta('meta[property="og:url"]', url, true);
    setMeta('meta[property="og:title"]', title, true);
    setMeta('meta[property="og:description"]', description, true);
    setMeta('meta[property="og:image"]', resolvedImage, true);
    setMeta('meta[property="og:image:secure_url"]', resolvedImage, true);
    setMeta('meta[name="twitter:card"]', 'summary_large_image');
    setMeta('meta[name="twitter:title"]', title);
    setMeta('meta[name="twitter:description"]', description);
    setMeta('meta[name="twitter:image"]', resolvedImage);
    setLink('canonical', url);

    document.dispatchEvent(new Event('app-ready'));
  }, [title, description, image, resolvedImage, url, type]);

  return null;
}
```

### 4. Use `<MetaTags>` in every page component

Every page must call `<MetaTags>` with page-specific values so prerendering captures correct metadata per route:

```tsx
export function AboutPage() {
  return (
    <>
      <MetaTags
        title="About - APPNAME"
        description="Learn more about what we do."
        image="/share/about.webp"
      />
      {/* page content */}
    </>
  );
}
```

## Notes

- The `image` path passed to `<MetaTags>` should be a root-relative path to the pre-generated share image (see `site-share-images` skill)
- OG image dimensions should be 1200x630 minimum; 1536x1024 for retina displays
- The `og:url` and `canonical` values must match exactly — search engines penalize mismatches
- Never let two pages have identical `<title>` tags

## Framework: Next.js track

On the `nextjs` track, metadata is data exported from the route, not DOM mutation performed after hydration. **Do not create `src/components/MetaTags.tsx`** — a client component that writes into `document.head` fights the Metadata API, loses on the server render, and gives crawlers the wrong tags on first paint.

### Base tags → `app/layout.tsx`

Everything step 1 puts in `index.html` becomes the layout's `metadata` export. Set `metadataBase` first: without it, every relative OG image path ships as a relative URL that crawlers cannot fetch.

```tsx
export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL ?? 'http://localhost:3000'),
  title: { default: 'APPNAME - Tagline', template: '%s | APPNAME' },
  description: 'One sentence description for search results.',
  applicationName: 'APPNAME',
  authors: [{ name: 'APPNAME' }],
  robots: { index: true, follow: true },
  openGraph: {
    type: 'website',
    siteName: 'APPNAME',
    locale: 'en_US',
    url: '/',
    images: [{ url: '/share/home.png', width: 1200, height: 630, alt: 'APPNAME - short alt text' }],
  },
  twitter: { card: 'summary_large_image', creator: '@HANDLE', site: '@HANDLE' },
  appleWebApp: { capable: true, title: 'APPNAME', statusBarStyle: 'black-translucent' },
  formatDetection: { telephone: false },
  alternates: { canonical: '/' },
};

export const viewport: Viewport = { themeColor: '#PRIMARY_COLOR' };
```

For an iOS app, `appleWebApp` plus `itunes: { appId: 'APPSTORE_ID' }` replaces the hand-written `apple-itunes-app` tag.

### Per-page tags → `export const metadata` in each `page.tsx`

```tsx
export const metadata: Metadata = {
  title: 'About',                       // becomes "About | APPNAME" via the layout template
  description: 'Learn more about what we do.',
  alternates: { canonical: '/about' },
  openGraph: { url: '/about', images: [{ url: '/share/about.png', width: 1200, height: 630 }] },
};
```

For routes whose content is dynamic (blog posts, comparison pages), export `generateMetadata({ params })` instead and derive the title, description, canonical, and image from the same data the page renders.

For a `noindex` page, set `robots: { index: false, follow: true }` — and mark it `indexable: false` in `config/routes.mjs` in the same change so it leaves the sitemap too.

### Structured data

JSON-LD has no metadata-object equivalent. Render it as a script tag in the layout (site-wide `Organization`/`WebSite`) or in the page (per-page `MobileApplication`, `Article`, `Product`):

```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
/>
```

Keep it in a server component so it lands in the HTML rather than being injected after hydration.

### Favicon

Delete the hand-written `<link rel="icon">` tags. `app/icon.png`, `app/apple-icon.png`, and `app/favicon.ico` are file conventions that emit those tags automatically; hand-written ones duplicate them.

### Verification

`npm run build && npm start`, then `curl -s localhost:$PORT/<route> | grep -E 'og:|canonical|<title>'` for every route. The tags must be in the HTML response itself, not added later by script.

See `/senternet-site-framework` for the full convention map.
