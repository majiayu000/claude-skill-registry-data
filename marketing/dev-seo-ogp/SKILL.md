---
name: dev-seo-ogp
description: "Add Open Graph (OGP) and Twitter Card meta tags for social media link previews. Use when: (1) User says 'add OGP', 'og tags', 'social preview', 'link preview', (2) Setting up SEO meta tags for a new site, (3) User wants og:image or Twitter cards, (4) User mentions 'OGP', 'Open Graph', 'twitter:card', 'social sharing'."
user-invocable: true
argument-hint: "[project path or URL]"
---

# SEO: Open Graph & Twitter Card Meta Tags

Add proper OGP and Twitter Card meta tags so links display rich previews on social media, chat apps, and search results.

## OG Image

### Recommended Size

- **1200 x 630 pixels** — universal standard for Facebook, Twitter/X, LinkedIn, Discord, Slack
- Aspect ratio: **1.91:1**
- Format: **PNG** or **JPG** (PNG for logos/graphics, JPG for photos)
- File size: under **5 MB** (ideally under 300 KB for fast loading)
- Place in the `public/` directory (static assets)

### Creating the OG Image

If the user provides a screenshot or design:

```bash
# Resize to OGP dimensions using sharp-cli
npx --yes sharp-cli -i source.png -o public/img/ogp.png resize 1200 630 --fit cover
```

If no image tool is available, use the screenshot as-is if it's close to 1200x630.

## Required Meta Tags

These are the minimum tags every page needs:

```html
<!-- Open Graph -->
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Page description" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://example.com/page/" />
<meta property="og:image" content="https://example.com/img/ogp.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Description of the image" />
<meta property="og:site_name" content="Site Name" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Page Title" />
<meta name="twitter:description" content="Page description" />
<meta name="twitter:image" content="https://example.com/img/ogp.png" />
```

### Tag Details

| Tag | Required | Notes |
| --- | --- | --- |
| `og:title` | Yes | Page title, 60-70 chars max for best display |
| `og:description` | Yes | 155-200 chars. Falls back to `<meta name="description">` on some platforms |
| `og:type` | Yes | `website` for homepage, `article` for content pages |
| `og:url` | Yes | Canonical URL of the page. Must be absolute |
| `og:image` | Yes | **Must be absolute URL** (https://...). Relative paths fail on most platforms |
| `og:image:width` | Recommended | Helps platforms render without re-fetching the image |
| `og:image:height` | Recommended | Same as above |
| `og:image:alt` | Recommended | Accessibility. Required if og:image is set |
| `og:site_name` | Optional | Brand name shown above the title on some platforms |
| `og:locale` | Optional | e.g., `en_US`, `ja_JP` |
| `twitter:card` | Yes | `summary_large_image` for full-width preview, `summary` for small square |
| `twitter:title` | Optional | Falls back to og:title |
| `twitter:description` | Optional | Falls back to og:description |
| `twitter:image` | Optional | Falls back to og:image |
| `twitter:site` | Optional | @username of the site's Twitter account |

## Implementation by Framework

### Astro

Edit the main layout file (usually `src/layouts/*.astro`). Add tags in `<head>`:

```astro
---
// In the frontmatter, construct the OG image URL
const ogImageUrl = new URL(withBase("/img/ogp.png"), Astro.site || Astro.url).href;
const canonicalUrl = new URL(Astro.url.pathname, Astro.site || Astro.url).href;
---
<head>
  <!-- existing tags -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content={canonicalUrl} />
  <meta property="og:image" content={ogImageUrl} />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content={description || siteName} />
  <meta property="og:site_name" content={siteName} />
  <meta name="twitter:card" content="summary_large_image" />
</head>
```

For Astro, set `site` in `astro.config.mjs` to enable `Astro.site`:

```js
export default defineConfig({
  site: "https://example.com",
});
```

If `site` is not set, fall back to `Astro.url` (works for relative but OG image needs absolute).

### Next.js (App Router)

Use the `metadata` export or `generateMetadata()`:

```tsx
export const metadata: Metadata = {
  openGraph: {
    title: "Page Title",
    description: "Description",
    url: "https://example.com",
    siteName: "Site Name",
    images: [{ url: "/img/ogp.png", width: 1200, height: 630, alt: "Description" }],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Page Title",
    description: "Description",
    images: ["/img/ogp.png"],
  },
};
```

### Docusaurus

Use `themeConfig.metadata` in `docusaurus.config.js` for site-wide defaults:

```js
themeConfig: {
  metadata: [
    { property: "og:image", content: "https://example.com/img/ogp.png" },
    { property: "og:image:width", content: "1200" },
    { property: "og:image:height", content: "630" },
    { name: "twitter:card", content: "summary_large_image" },
  ],
}
```

## Same OG Image for All Pages

When using one OG image site-wide:

- Place it at `public/img/ogp.png`
- Reference it with an absolute URL in meta tags
- `og:title` and `og:description` should still be per-page

## Validation & Testing

After adding tags, validate with:

- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
- [opengraph.xyz](https://www.opengraph.xyz/) — preview across platforms

## Common Mistakes

- **Relative image URLs** — og:image must be absolute (https://...). Relative paths silently fail.
- **Missing image dimensions** — Without width/height, platforms re-fetch the image to detect size, causing slow or broken previews.
- **Image too large** — Keep under 5 MB. Platforms may timeout on large files.
- **og:url mismatch** — Must match the canonical URL. Mismatches cause duplicate content issues.
- **Missing twitter:card** — Without this, Twitter shows a plain link instead of a rich preview.
