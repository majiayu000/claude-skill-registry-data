---
name: optimize
description: 'Full SEO optimization — audit, fix, and enhance SEO across Next.js and Directus Arguments: [--skip-directus] [--skip-build] [--report-only].'
---

# SEO Optimize

End-to-end SEO optimization for a Directus + Next.js project. Audits the current state, implements all fixes, extends Directus schema with SEO fields, and produces a final report.

## Arguments

- `--skip-directus` (optional) — Skip Directus schema changes and field population
- `--skip-build` (optional) — Skip the final `pnpm build` verification
- `--report-only` (optional) — Audit only, do not make changes. Show what needs fixing

## Skills Used

This command orchestrates all seo-dev skills plus Directus MCP tools:

| Skill | Used In |
|-------|---------|
| `seo-dev:setup` | Phase 1: Audit foundations |
| `seo-dev:meta-tags` | Phase 2: Metadata & OG |
| `seo-dev:structured-data` | Phase 3: JSON-LD |
| `seo-dev:sitemap-robots` | Phase 4: Sitemap & Robots |
| `seo-dev:performance` | Phase 5: Core Web Vitals |
| `seo-dev:technical-seo` | Phase 6: Technical SEO |
| `seo-dev:content-seo` | Phase 7: Content optimization |
| `seo-dev:audit` | Phase 1 & Phase 8: Audit & Report |
| `directus-dev:schema-design` | Phase 1g: Schema audit |
| `directus-dev:mcp-tools` | Phase 3D: Field creation & item population |
| `stack-directus-nextjs:directus-to-nextjs` | Phase 3D-4: Data fetching updates |

## Process

### Phase 1: SEO Audit (read-only)

Scan the entire project to understand the current SEO state. Do NOT make changes yet — collect findings first.

#### 1a. Project Structure Discovery

```bash
# Find the app directory
ls -d src/app 2>/dev/null || ls -d app 2>/dev/null

# Identify all page routes
find src/app -name "page.tsx" -o -name "page.ts" 2>/dev/null || find app -name "page.tsx" -o -name "page.ts" 2>/dev/null

# Find root layout
find src/app -name "layout.tsx" -maxdepth 1 2>/dev/null || find app -name "layout.tsx" -maxdepth 1 2>/dev/null
```

#### 1b. Metadata Audit

Check every page and layout for metadata:

```bash
# Pages with metadata
grep -rl "export const metadata\|export async function generateMetadata" src/app --include="*.tsx" --include="*.ts"

# Pages WITHOUT metadata (these need fixing)
find src/app -name "page.tsx" | while read f; do
  grep -qE "metadata|generateMetadata" "$f" || echo "MISSING: $f"
done

# Check metadataBase
grep -r "metadataBase" src/app/layout.tsx

# Check title template
grep -r "template:" src/app/layout.tsx

# Check NEXT_PUBLIC_SITE_URL
grep "NEXT_PUBLIC_SITE_URL" .env .env.local 2>/dev/null
```

#### 1c. Sitemap & Robots Audit

```bash
ls src/app/sitemap.ts src/app/robots.ts 2>/dev/null
```

#### 1d. Structured Data Audit

```bash
# Check for existing JSON-LD
grep -rl "application/ld+json" src/ --include="*.tsx" --include="*.ts"

# Check for schema-dts
grep "schema-dts" package.json

# Check for JsonLd component
grep -rl "JsonLd" src/components/ --include="*.tsx" 2>/dev/null
```

#### 1e. Images Audit

```bash
# Images without alt text
grep -rn "<Image\|<img" src/ --include="*.tsx" | grep -v "alt=" | head -30

# Images without sizes prop
grep -rn "<Image" src/ --include="*.tsx" | grep -v "sizes=" | head -20

# Images marked as high priority (should be only LCP images).
# Next.js 16 replaced the `priority` prop with `preload`; the docs recommend loading="eager" / fetchPriority="high". Search for all of them
grep -rnE "priority|preload|fetchPriority|loading=\"eager\"" src/ --include="*.tsx" | grep "<Image\|Image " | head -10

# Check next.config for image formats
grep -A5 "images:" next.config.ts 2>/dev/null || grep -A5 "images:" next.config.js 2>/dev/null
```

#### 1f. Heading Hierarchy Audit

```bash
# Count H1 tags per page
find src/app -name "page.tsx" | while read f; do
  count=$(grep -c "<h1\|<H1" "$f" 2>/dev/null || echo "0")
  [ "$count" != "1" ] && echo "H1 count=$count: $f"
done
```

#### 1g. Directus Schema Audit (skip if --skip-directus)

Use Directus MCP tools to discover content collections and check for SEO fields.

**Step 1: Discover all collections**

Call the `schema` tool with no parameters to get the full collection list:

```
Tool: schema
Input: {}
```

**Step 2: Identify content collections**

From the schema response, identify content collections — those that have a `slug` or `name`/`title` field and represent public-facing content (e.g., `components`, `posts`, `pages`, `products`). Skip system collections and junction tables.

**Step 3: Get detailed schema for each content collection**

```
Tool: schema
Input: { "keys": ["components", "posts"] }
```

**Step 4: Check for SEO fields**

For each content collection, check if these fields exist:
- `meta_title` (string) — SEO title override
- `meta_description` (text) — SEO description override
- `og_image_url` (string) — Open Graph image URL
- `canonical_url` (string) — Custom canonical URL

Record which collections need SEO fields added vs. which already have them.

#### 1h. Compile Audit Report

Present findings in this format before proceeding:

```
## SEO Audit Results

### Foundations
- [ ] metadataBase: [present/missing]
- [ ] Title template: [present/missing]
- [ ] NEXT_PUBLIC_SITE_URL: [present/missing]
- [ ] sitemap.ts: [present/missing]
- [ ] robots.ts: [present/missing]
- [ ] schema-dts: [installed/missing]

### Pages (X total)
- Pages with metadata: X/Y
- Pages without metadata: [list]
- Pages missing canonical: [list]

### Structured Data
- JSON-LD present: [yes/no]
- Organization schema: [yes/no]
- WebSite schema (home page): [yes/no]
- Page-specific schemas: [list]

### Images
- Images without alt: X
- Images without sizes: X
- LCP images without `fetchPriority="high"` / `loading="eager"` (or `priority` / `preload`): X

### Headings
- Pages with wrong H1 count: [list]

### Directus SEO Fields
- Content collections found: [list]
- Collections with all 4 SEO fields (meta_title, meta_description, og_image_url, canonical_url): [list]
- Collections missing SEO fields: [list with which fields are missing]
- Items with empty meta_title: X/Y total

### Estimated changes: X files to create/modify
```

**If --report-only**: stop here, show the report, and exit.

Ask the user to confirm before proceeding with changes.

### Phase 2: SEO Foundations

Apply `seo-dev:setup` patterns.

#### 2a. Install schema-dts

```bash
pnpm add -D schema-dts
```

#### 2b. Set NEXT_PUBLIC_SITE_URL

If missing from `.env` / `.env.local`, add it:
```
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
```

Ask the user for their production domain if not already set.

#### 2c. Configure Root Layout Metadata

Read the current root layout. Add or update:

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'),
  title: {
    template: '%s | Site Name',
    default: 'Site Name',
  },
  description: 'Site description',
  openGraph: {
    type: 'website',
    siteName: 'Site Name',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
  },
}
```

Preserve any existing metadata fields. Merge, do not replace.

#### 2d. Create robots.ts (if missing)

Apply `seo-dev:sitemap-robots` pattern with environment-aware blocking and AI crawler rules. Never disallow `/_next/` — Google needs those JS/CSS/image files to render pages.

#### 2e. Create sitemap.ts (if missing)

Apply `seo-dev:sitemap-robots` dynamic pattern. Fetch pages from Directus:

```tsx
import type { MetadataRoute } from 'next'
import directus from '@/lib/directus'
import { readItems } from '@directus/sdk'

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://yourdomain.com'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    { url: BASE_URL, lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
  ]

  // Dynamic pages from Directus
  // Adapt collection names and slugs to the actual project
  try {
    const posts = await directus.request(
      readItems('posts', {
        fields: ['slug', 'date_updated'],
        filter: { status: { _eq: 'published' } },
      })
    )

    const postEntries: MetadataRoute.Sitemap = posts.map((post) => ({
      url: `${BASE_URL}/blog/${post.slug}`,
      lastModified: post.date_updated ? new Date(post.date_updated) : new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.7,
    }))

    return [...staticPages, ...postEntries]
  } catch {
    return staticPages
  }
}
```

Adapt collection names (`posts`, `pages`, `products`) to match the actual project schema discovered in Phase 1.

### Phase 3: Structured Data

Apply `seo-dev:structured-data` patterns.

#### 3a. Create JsonLd Component

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

#### 3b. Create Schema Factory Functions

Create `lib/schema.ts` with factory functions from the `seo-dev:structured-data` skill:
- `createOrganization`
- `createWebSite`
- `createBreadcrumbList`
- `createArticle` (if blog/news exists)
- `createProduct` (if e-commerce exists)

#### 3c. Add Sitewide Schemas

Add `<JsonLd>` for Organization to the root layout `<body>`, and `<JsonLd>` for WebSite (`name` / `alternateName`, used for the site name) to the home page `app/page.tsx` — Google reads WebSite only on the home page. Do not add `SearchAction` or FAQPage/HowTo markup for search appearance: Google no longer shows those features.

#### 3d. Add Page-Specific Schemas

For each content page type discovered in Phase 1:
- Blog posts → Article schema
- Product pages → Product schema
- All inner pages → BreadcrumbList schema

### Phase 3D: Directus SEO Fields (skip if --skip-directus)

**This phase is MANDATORY unless `--skip-directus` is passed.** It creates SEO fields in Directus content collections via MCP tools and auto-populates existing records. Do NOT skip this or defer it to a separate request.

#### 3D-1. Create SEO fields via MCP

For each content collection identified in Phase 1g that lacks SEO fields, call the `fields` tool to create all four fields in a single batch.

**IMPORTANT**: The `data` parameter must always be an **array** of field objects, even for a single field. Each field object must include `field`, `type`, `meta`, and `schema`.

```
Tool: fields
Input: {
  "action": "create",
  "collection": "<collection_name>",
  "data": [
    {
      "field": "meta_title",
      "type": "string",
      "meta": {
        "interface": "input",
        "display": "raw",
        "note": "SEO title for search engines (50-60 chars). Falls back to main title if empty.",
        "options": { "trim": true, "placeholder": "Override page title for search results..." },
        "width": "half",
        "sort": 100
      },
      "schema": {
        "data_type": "varchar",
        "max_length": 70,
        "is_nullable": true
      }
    },
    {
      "field": "meta_description",
      "type": "text",
      "meta": {
        "interface": "input-multiline",
        "display": "raw",
        "note": "SEO description (150-160 chars). Falls back to main description if empty.",
        "options": { "trim": true, "placeholder": "Override description for search results..." },
        "width": "full",
        "sort": 101
      },
      "schema": {
        "data_type": "text",
        "is_nullable": true
      }
    },
    {
      "field": "og_image_url",
      "type": "string",
      "meta": {
        "interface": "input",
        "display": "raw",
        "note": "Open Graph image URL (1200x630 recommended). Used for social media previews.",
        "options": { "trim": true, "placeholder": "https://..." },
        "width": "half",
        "sort": 102
      },
      "schema": {
        "data_type": "varchar",
        "max_length": 500,
        "is_nullable": true
      }
    },
    {
      "field": "canonical_url",
      "type": "string",
      "meta": {
        "interface": "input",
        "display": "raw",
        "note": "Custom canonical URL. Leave empty to use the default page URL.",
        "options": { "trim": true, "placeholder": "https://..." },
        "width": "half",
        "sort": 103
      },
      "schema": {
        "data_type": "varchar",
        "max_length": 500,
        "is_nullable": true
      }
    }
  ]
}
```

**Rules:**
- Only create fields that do not already exist (check Phase 1g results)
- Process ALL content collections, not just one
- If a collection already has some SEO fields (e.g., `meta_title` exists but `og_image_url` doesn't), only add the missing ones
- Log every field created: `Created <field> on <collection>`

#### 3D-2. Auto-populate SEO fields from existing data

For each content collection that received new SEO fields, read all items that have empty SEO fields and derive values from existing content.

**Step 1: Read items with empty meta_title**

```
Tool: items
Input: {
  "action": "read",
  "collection": "<collection_name>",
  "query": {
    "fields": ["id", "name", "description"],
    "filter": {
      "meta_title": { "_null": true }
    },
    "limit": -1
  }
}
```

Adapt field names to the collection's actual schema — the "title" field may be called `name`, `title`, `heading`, etc. The "description" field may be `description`, `excerpt`, `content`, `body`, etc. Use the schema from Phase 1g to determine correct field names.

**Step 2: Batch update items with derived SEO values**

```
Tool: items
Input: {
  "action": "update",
  "collection": "<collection_name>",
  "keys": [1, 2, 3],
  "data": {
    "meta_title": null
  }
}
```

Since batch update applies the same data to all keys, process items **individually** or in groups with identical derived values:

```
Tool: items
Input: {
  "action": "update",
  "collection": "<collection_name>",
  "keys": [<item_id>],
  "data": {
    "meta_title": "<derived from name/title, truncated to 60 chars>",
    "meta_description": "<derived from description, truncated to 160 chars>"
  }
}
```

**Derivation rules:**
- `meta_title`: Take the item's primary title/name field. Truncate to 60 chars. If > 57 chars, truncate at the last word boundary and append "..."
- `meta_description`: Take the item's description/content/excerpt field. Strip HTML/markdown if present. Truncate to 160 chars at word boundary.
- `og_image_url`: Use the item's `image_url` field if one exists. Otherwise leave null.
- `canonical_url`: Leave null (auto-derived from slug in Next.js)
- For **10+ items**, process in batches of 10 to avoid timeouts. Log progress: `Updated X/Y items in <collection>`

#### 3D-3. Update TypeScript types

Add SEO fields to the relevant TypeScript interface in the project's types file:

```tsx
export interface DirectusComponent {
  // ... existing fields ...
  meta_title: string | null
  meta_description: string | null
  og_image_url: string | null
  canonical_url: string | null
}
```

#### 3D-4. Update data fetching functions

Add SEO fields to all `readItems` calls that fetch content for pages with `generateMetadata`:

```tsx
const item = await directus.request(
  readItems('components', {
    fields: [
      // ... existing fields ...
      'meta_title', 'meta_description', 'og_image_url', 'canonical_url',
    ],
    filter: { slug: { _eq: slug } },
    limit: 1,
  })
)
```

#### 3D-5. Update generateMetadata to use Directus SEO fields

On every dynamic page with `generateMetadata`, use Directus SEO fields with fallback to existing data:

```tsx
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const item = await getComponentBySlug(slug)
  if (!item) return { title: 'Not Found' }

  const title = item.meta_title || item.name
  const description = item.meta_description || item.description || ''

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      images: item.og_image_url
        ? [{ url: item.og_image_url, width: 1200, height: 630 }]
        : undefined,
    },
    alternates: {
      canonical: item.canonical_url || `/catalog/${slug}`,
    },
  }
}
```

#### 3D-6. Verify Directus changes

After all fields are created and items populated:

1. Call `schema` tool with `keys: ["<collection>"]` to confirm fields exist
2. Call `items` tool to read a sample item and verify SEO fields are populated
3. Log summary: `Directus SEO fields: X collections updated, Y fields created, Z items auto-populated`

### Phase 4: Meta Tags & OG Images

Apply `seo-dev:meta-tags` patterns.

For every page discovered in Phase 1 that lacks metadata:

1. **Static pages** (about, contact, etc.) — Add `export const metadata: Metadata` with title, description, OG tags, canonical
2. **Dynamic pages** (blog/[slug], products/[slug]) — Add `generateMetadata` function using Directus SEO fields
3. **Add OG image defaults** — Either static images or `opengraph-image.tsx` for dynamic generation

### Phase 5: Content Optimization

Apply `seo-dev:content-seo` patterns.

1. **Fix heading hierarchy** — Ensure single H1 per page, logical H2-H6 nesting
2. **Fix image alt texts** — Add descriptive alt text to all `<Image>` components missing it
3. **Add sizes prop** — Add responsive `sizes` attribute to all `<Image>` components
4. **Mark LCP images** — Add `loading="eager"` and `fetchPriority="high"` to above-the-fold hero/banner images (one per page max; if the LCP image differs between mobile and desktop, use `fetchPriority="high"` alone, because `loading="eager"` would download both). Next.js 16 deprecated the `priority` prop in favor of `preload`; on Next.js 15 and earlier `priority` still works
5. **Create Breadcrumbs component** — If inner pages lack breadcrumbs, create a reusable component with BreadcrumbList schema

### Phase 6: Performance & Technical SEO

Apply `seo-dev:performance` and `seo-dev:technical-seo` patterns.

#### 6a. next.config.ts Updates

Add security headers and image format optimization:

```ts
// Add to next.config.ts
const nextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],
    // Keep existing remotePatterns
  },
  async headers() {
    return [{
      source: '/(.*)',
      headers: [
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      ],
    }]
  },
}
```

Merge with existing config — do not overwrite. Do not add `X-XSS-Protection` (deprecated, non-standard); a `Content-Security-Policy` is the modern control.

#### 6b. Verify next/font Usage

Check that `next/font` is used in root layout (not external font links). If using Google Fonts via `<link>`, migrate to `next/font/google`.

#### 6c. Check Lazy Loading

Verify non-critical components use `dynamic()` imports where appropriate.

### Phase 7: Build Verification (skip if --skip-build)

```bash
pnpm build
```

Check for:
- Metadata-related build errors
- TypeScript errors in new/modified files
- Sitemap/robots generation warnings

If build fails, fix the errors and retry.

### Phase 8: Final Report

Present the complete report:

```
## SEO Optimization Report

### Before → After Summary

| Category | Before | After |
|----------|--------|-------|
| Pages with metadata | X/Y | Y/Y |
| Pages with canonical | X/Y | Y/Y |
| Structured data schemas | X | Y |
| Images with alt text | X/Y | Y/Y |
| Images with sizes | X/Y | Y/Y |
| sitemap.ts | missing/present | present |
| robots.ts | missing/present | present |
| schema-dts | missing/installed | installed |
| metadataBase | missing/set | set |
| Security headers | missing/set | set |
| AVIF/WebP | disabled/enabled | enabled |
| Directus SEO fields | X/Y collections | Y/Y collections |
| Items with meta_title | 0/X | X/X |

### Files Created
- [list of new files]

### Files Modified
- [list of modified files with brief description of changes]

### Directus Changes (if applied)
- Collections updated: [list]
- SEO fields created: [X fields across Y collections]
  - Per collection: `<collection>`: meta_title, meta_description, og_image_url, canonical_url
- Items auto-populated: X/Y items received derived meta_title + meta_description
- Verification: [PASS/FAIL — schema confirmed, sample item checked]

### Remaining Manual Tasks
- [ ] Set NEXT_PUBLIC_SITE_URL to production domain
- [ ] Submit sitemap in Google Search Console
- [ ] Add Google Search Console verification code
- [ ] Create custom OG images for key pages
- [ ] Review auto-generated meta_title/meta_description values in Directus Admin
- [ ] Add og_image_url for key items via Directus Admin
- [ ] Test with Google Rich Results Test after deployment

### Build Status
- [PASS/FAIL] — pnpm build

### Next Steps
1. Deploy and test with PageSpeed Insights
2. Submit sitemap to Google Search Console
3. Verify rich results after 2-4 weeks
4. Run /seo-dev:optimize again after adding new content
```

## Example

Input: `/seo-dev:optimize`

Output: Runs full audit → shows report → asks for confirmation → implements all changes → shows final report.

Input: `/seo-dev:optimize --report-only`

Output: Runs full audit → shows report → exits without changes.

Input: `/seo-dev:optimize --skip-directus`

Output: Runs full optimization on Next.js side only, does not touch Directus schema or content.