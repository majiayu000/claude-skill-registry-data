---
name: senternet-site-sitemap
description: Generate sitemap.xml from site routes and keep it wired into build and deploy workflows.
---

# Sitemap Generation

Generate a `sitemap.xml` from a route list, with optional multilingual `hreflang` support, and wire it into the build pipeline.

## Steps

### 1. Create `scripts/generate-sitemap.mjs`

```js
#!/usr/bin/env node
import { writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const SITE_URL = 'https://www.DOMAIN.com'; // replace with actual domain
const LASTMOD = process.env.SITEMAP_LASTMOD || new Date().toISOString().slice(0, 10);

// Define all routes with their SEO priority.
// NEVER list a `noindex` route here (see "Never include noindex routes").
// Legal pages like /privacy and /terms are typically noindex, so they are
// deliberately absent from this example.
const ROUTES = [
  { path: '/',        changefreq: 'weekly',  priority: '1.0' },
  { path: '/about',   changefreq: 'monthly', priority: '0.8' },
  // Add landing pages, blog posts, compare pages, etc.
];

// For multilingual sites, define locales. Remove/empty this array for English-only sites.
const LOCALES = [
  { language: 'en', prefix: '' },
  // { language: 'es', prefix: '/es' },
];

function localizedPath(routePath, prefix) {
  if (routePath === '/') return prefix || '/';
  return `${prefix}${routePath}`;
}

function escapeXml(val) {
  return val.replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll("'", '&apos;')
            .replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

const urls = [];
for (const route of ROUTES) {
  for (const locale of LOCALES) {
    const loc = `${SITE_URL}${localizedPath(route.path, locale.prefix)}`;

    // Build hreflang alternates (only needed for multilingual sites)
    const alternates = LOCALES.length > 1
      ? [
          ...LOCALES.map(alt => ({
            hreflang: alt.language,
            href: `${SITE_URL}${localizedPath(route.path, alt.prefix)}`,
          })),
          { hreflang: 'x-default', href: `${SITE_URL}${localizedPath(route.path, '')}` },
        ]
      : [];

    urls.push({ loc, alternates, ...route });
  }
}

const xml = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' +
    (LOCALES.length > 1 ? ' xmlns:xhtml="http://www.w3.org/1999/xhtml"' : '') + '>',
  ...urls.map(entry => {
    const altLines = entry.alternates
      .map(a => `    <xhtml:link rel="alternate" hreflang="${escapeXml(a.hreflang)}" href="${escapeXml(a.href)}" />`)
      .join('\n');
    return [
      '  <url>',
      `    <loc>${escapeXml(entry.loc)}</loc>`,
      altLines,
      `    <lastmod>${LASTMOD}</lastmod>`,
      `    <changefreq>${entry.changefreq}</changefreq>`,
      `    <priority>${entry.priority}</priority>`,
      '  </url>',
    ].join('\n');
  }),
  '</urlset>',
  '',
].join('\n');

writeFileSync(join(__dirname, '../public/sitemap.xml'), xml);
console.log(`Generated sitemap with ${urls.length} URL(s).`);
```

### 2. Add the script to `package.json`

```json
{
  "scripts": {
    "generate:sitemap": "node scripts/generate-sitemap.mjs",
    "build:prod": "npm run generate:sitemap && tsc -b && vite build --mode production && node scripts/prerender.mjs"
  }
}
```

### 3. Reference the sitemap in `robots.txt`

```
User-agent: *
Allow: /

Sitemap: https://www.DOMAIN.com/sitemap.xml
```

### 4. Keep routes in sync

The routes array in `generate-sitemap.mjs` must stay in sync with:
- `src/App.tsx` (React Router routes)
- `scripts/prerender.mjs` (prerender ROUTES array)

When you add a new page, update all three files at the same time.

### 5. Never include noindex routes

A sitemap tells search engines "these are my canonical, indexable pages." A
route that renders `<meta name="robots" content="noindex, ...">` says the
opposite. Listing a noindex route in the sitemap is a direct contradiction that
Google Search Console flags as a coverage error ("Submitted URL marked
noindex"), so it must never happen.

**Rule: a route belongs in `ROUTES` only if it is indexable. If a page is
noindex, leave it out of the sitemap entirely.**

Legal / boilerplate pages (`/privacy`, `/terms`, and often `/ai-disclosure`)
are the usual noindex candidates: they carry no search value and can dilute or
duplicate signals. When a page is set to noindex (via the site's `MetaTags`
`noindex` prop or an equivalent `<meta name="robots">`), remove it from:

- `scripts/generate-sitemap.mjs` (`ROUTES`)
- `scripts/prerender.mjs` — keep prerendering it (crawlers still fetch direct
  links to it), it just must not be advertised in the sitemap
- Leave the React `<Route>` in `src/App.tsx`

Leave a short comment where the route would otherwise sit, so the omission
reads as deliberate rather than a missed sync. Conversely, before marking a
route noindex, delete it from `ROUTES` in the same change.

### 6. Priority guidelines

Only indexable routes appear in the sitemap (see the rule above), so this table
covers indexable page types.

| Page type | Priority | Changefreq |
|-----------|----------|------------|
| Home | 1.0 | weekly |
| Primary landing pages | 0.9 | weekly |
| Features, about | 0.8 | monthly |
| Blog/insight posts | 0.7–0.8 | monthly |
| Compare / alternative pages | 0.7 | monthly |
| Secondary content | 0.5 | monthly |

### 7. For high-volume programmatic pages (100+ pages)

Use a sitemap index instead of a single sitemap:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.DOMAIN.com/sitemap-main.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.DOMAIN.com/sitemap-blog.xml</loc>
  </sitemap>
</sitemapindex>
```

## Verification

After generating:
- Open `public/sitemap.xml` and verify route count
- Submit to Google Search Console: Sitemaps → Add sitemap
- The IndexNow script reads from this file automatically — no extra steps needed

## Framework: Next.js track

On the `nextjs` track there is no generator script and no committed `public/sitemap.xml`. The sitemap is a route: `app/sitemap.ts`, served at `/sitemap.xml`. Everything above about priorities, changefreq, and never listing `noindex` routes still applies — only the mechanism changes.

Use the route manifest at `config/routes.mjs` (created by `/senternet-site-nextjs-setup`) as the single source of truth, so the sitemap, `app/robots.ts`, and `scripts/indexnow.mjs` cannot disagree:

```ts
// app/sitemap.ts
import type { MetadataRoute } from 'next';
import { indexableRoutes } from '@/config/routes.mjs';

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? 'http://localhost:3000';

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return indexableRoutes().map(route => ({
    url: `${baseUrl}${route.path === '/' ? '' : route.path}`,
    lastModified,
    changeFrequency: route.changefreq,
    priority: route.priority,
  }));
}
```

Differences to hold on to:

- **The noindex rule is enforced by data, not by memory.** A route marked `indexable: false` in `config/routes.mjs` is filtered out here automatically. Set that flag in the same change that sets `robots: { index: false }` in the page's `metadata`.
- **Dynamic routes** (blog posts, comparison pages) come from the same list that feeds their `generateStaticParams`. Import that list into `sitemap.ts` and concatenate rather than hand-maintaining a second copy.
- **Multilingual** `hreflang` alternates go in the `alternates.languages` field of each sitemap entry, and must match `alternates.languages` in the page's `metadata`.
- **Nothing is wired into `build:prod`** — there is no generate step. Verify with `npm start && curl -s localhost:$PORT/sitemap.xml`.
- **Do not also ship `public/sitemap.xml`.** Two sources for the same path is a silent conflict where the static file wins and quietly goes stale.
- For 100+ programmatic pages, `app/sitemap.ts` can export `generateSitemaps()` to emit a sitemap index instead of one large file.

See `/senternet-site-framework` for the full convention map.
