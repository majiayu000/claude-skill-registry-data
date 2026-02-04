---
name: managing-seo
description: SEO maintenance for the site. Consult when adding content, modifying pages, updating metadata, or making changes that affect discoverability. Covers meta tags, structured data, OG images, sitemap, RSS, and llms.txt.
---

# Managing SEO

SEO maintenance for the site. Keep metadata accurate, content discoverable, and AI systems informed.

British English throughout—code, comments, documentation, content.

## When to Use

Consult this skill when adding blog posts, creating static pages, modifying titles or descriptions, updating site-wide configuration, or making any change that affects how the site appears to search engines, social platforms, or AI systems.

## Important

Static pages require manual sitemap entry in `src/pages/sitemap.xml.ts`. This is easy to forget when adding new pages.

## Key Principles

Keep meta content in sync with visible content. The description in meta tags must match the description visible on the page. The title in Open Graph tags must match the page heading. Drift between metadata and visible content is a bug.

Titles under 60 characters display fully in search results. Descriptions under 160 characters avoid truncation. These are soft limits—clarity matters more than hitting a number, but brevity helps.

Title format is consistent: `Page Title | Sam Folorunsho` for pages, post title alone for blog posts.

Single H1 per page. Logical heading hierarchy (H2, H3, H4) aids both accessibility and SEO. Don't skip levels.

Internal linking helps search engines understand site structure. When referencing other content on the site, link to it.

Advanced SEO concerns—Core Web Vitals, mobile-friendliness, page speed—are handled well by Astro SSR and the deployment infrastructure. Focus maintenance effort on content quality and metadata accuracy.

## Meta Tags

The SEO component (`src/components/seo/SEO.astro`) injects meta tags via the Base layout. Props flow from page to component:

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title` | string | required | Page title |
| `description` | string | SITE.description | Under 160 characters |
| `ogImage` | string | `/og/default.png` | Open Graph image path |
| `ogType` | `website` \| `article` | `website` | Use `article` for blog posts |
| `publishDate` | Date | — | Required for articles |
| `updatedDate` | Date | — | Optional, updates `article:modified_time` |
| `tags` | string[] | `[]` | Rendered as `article:tag` meta |

Generated tags include Open Graph (Facebook, LinkedIn), Twitter Cards, article metadata for blog posts, and RSS discovery.

## Structured Data

JSON-LD structured data (`src/components/seo/JSONLD.astro`) provides machine-readable context:

**WebSite schema** — Applied to all pages via Base layout. Includes site name, URL, description, author details.

**Article schema** — Applied to blog posts via Post layout. Includes headline, description, dates, author, keywords.

Both schemas follow schema.org conventions. Author information pulls from `SITE.author` in config.

## OG Image Generation

Open Graph images are generated dynamically at request time.

**Endpoint:** `src/pages/og/[...slug].png.ts`

**Library:** `src/lib/og/` using satori (JSX to SVG) and @resvg/resvg-js (SVG to PNG)

**Routes:**
- `/og/default.png` — Site default image
- `/og/blog/[slug].png` — Blog post images with title and date

**Features:**
- 1200×630px PNG output
- Theme colours selected deterministically from title hash
- Switzer Variable font loaded at runtime
- One-year cache with `immutable` directive

**Testing OG images:**

After creating or modifying content, verify OG images render correctly:

1. Local: Visit `/og/blog/[slug].png` directly in browser
2. External validators:
   - [OpenGraph.xyz](https://www.opengraph.xyz/)
   - [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
   - [Twitter Card Validator](https://cards-dev.twitter.com/validator)
   - [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

Check that title displays without truncation, colours are correct, and no rendering errors appear.

## RSS Feed

The RSS feed (`src/pages/rss.xml.ts`) auto-generates from the blog content collection.

**Maintenance level:** Automatic. No manual updates needed for new posts.

**Features:**
- Excludes draft posts
- Sorted by publish date (newest first)
- Includes tags as categories
- British English language tag (`en-gb`)
- Styled XSL for browser viewing

Only modify for structural changes to feed format.

## Sitemap

The sitemap (`src/pages/sitemap.xml.ts`) combines automatic and manual sources.

**Blog posts:** Automatic. Pulled from content collection with `lastmod` from publish/update date.

**Static pages:** Manual. Must add new pages to the `pages` array:

```typescript
const pages = [
  {url: "", changefreq: "weekly", priority: "1.0"},
  {url: "blog", changefreq: "weekly", priority: "0.9"},
  {url: "about", changefreq: "monthly", priority: "0.8"},
  {url: "uses", changefreq: "monthly", priority: "0.6"},
  // Add new static pages here
];
```

When adding a static page, always update the sitemap. This is easy to forget.

## robots.txt

Simple configuration at `public/robots.txt`:

```
User-agent: *
Allow: /

Sitemap: https://samfolorunsho.com/sitemap.xml
```

Allows all crawlers and points to sitemap. Rarely needs modification.

## llms.txt

The `llms.txt` file (`public/llms.txt`) helps AI systems understand the site. It provides context about site purpose, structure, and content—like robots.txt but for language models.

**When to update:**
- Adding new static pages
- Significant changes to site purpose or structure
- Adding new content categories

Keep it concise. The goal is orientation, not exhaustive documentation. See `public/llms.txt` for current structure.

## Canonical URLs

Generated automatically by the SEO component:

- Strips query parameters and hash
- Uses pathname only
- Falls back to configured site URL

No manual intervention needed unless creating duplicate content (rare).

## Checklists

### New Blog Post

- [ ] Title is compelling and under 60 characters
- [ ] Description is clear and under 160 characters
- [ ] Tags are relevant and consistent with existing tags
- [ ] Frontmatter is complete (title, description, publishDate, tags)
- [ ] (Automatic) RSS feed includes post
- [ ] (Automatic) Sitemap includes post with lastmod
- [ ] (Automatic) Article JSON-LD generated
- [ ] (Automatic) OG image generated from title
- [ ] Verify OG image renders correctly

### New Static Page

- [ ] SEO component receives proper title and description
- [ ] Title follows format: `Page Title | Sam Folorunsho`
- [ ] Page added to sitemap with appropriate priority
- [ ] Page added to llms.txt if significant
- [ ] Canonical URL is correct
- [ ] Heading hierarchy is logical (single H1, sequential H2-H6)

### Site-Wide Changes

- [ ] SITE config updated if name/description/author changes
- [ ] Meta descriptions stay in sync with visible content
- [ ] OG default image reflects brand accurately
- [ ] robots.txt allows appropriate crawling
- [ ] Sitemap is accessible and valid
- [ ] llms.txt reflects current site structure
- [ ] RSS feed validates correctly
