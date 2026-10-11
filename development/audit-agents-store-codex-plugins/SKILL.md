---
name: audit
description: SEO audit checklist and automated testing for Next.js sites. This skill should be used when the user asks to "audit SEO", "check SEO", "SEO checklist", "Lighthouse SEO", "SEO test", "automated SEO testing", "SEO report", or wants to systematically evaluate their site's SEO health and identify issues.
---

# SEO Audit

Systematic checklist and automated testing patterns for evaluating a Next.js site's SEO health.

## Quick Audit Commands

Run these to get an instant snapshot of SEO status:

```bash
# Check all pages have metadata exports
grep -r "export const metadata\|export async function generateMetadata" src/app --include="*.tsx" --include="*.ts" -l

# Find pages WITHOUT metadata
find src/app -name "page.tsx" | while read f; do
  grep -qE "metadata|generateMetadata" "$f" || echo "MISSING metadata: $f"
done

# Check for sitemap and robots
ls src/app/sitemap.ts src/app/robots.ts 2>/dev/null || echo "Missing sitemap.ts or robots.ts"

# Check metadataBase
grep -r "metadataBase" src/app/layout.tsx || echo "NO metadataBase set"

# Find images without alt text
grep -rn "<img\|<Image" src/ --include="*.tsx" | grep -v "alt=" | head -20

# Check for H1 tags in pages
find src/app -name "page.tsx" | while read f; do
  grep -qE "<h1|<H1" "$f" || echo "NO H1: $f"
done

# Check structured data
grep -r "application/ld+json" src/ --include="*.tsx" -l
```

## Full SEO Audit Checklist

### 1. Crawlability & Indexability

| Check | How to Verify | Priority |
|-------|---------------|----------|
| `robots.ts` exists and is correct | Visit `/robots.txt` | Critical |
| `sitemap.ts` exists with all pages | Visit `/sitemap.xml`, count URLs | Critical |
| Sitemap submitted to Google Search Console | GSC → Sitemaps | Critical |
| No broken internal links (404s) | Run crawler or Lighthouse | High |
| No redirect chains (A→B→C) | Check `next.config.ts` redirects | High |
| No orphan pages | Verify every page has inbound links | Medium |
| Clean URL structure (lowercase, hyphens) | Review route structure | Medium |
| Staging blocked from indexing | Check `robots.ts` non-production rules | Critical |
| `robots.ts` does not disallow `/_next/` | Read `robots.ts` — blocked JS/CSS stops Google rendering pages | Critical |
| Generated sitemaps (`generateSitemaps`) are all discoverable | Next.js builds no sitemap index; check `robots.ts` lists them or a route handler serves an index | High |

### 2. Metadata & Social

| Check | How to Verify | Priority |
|-------|---------------|----------|
| `metadataBase` set in root layout | Grep for `metadataBase` | Critical |
| Title template configured | Check root layout `title.template` | Critical |
| Every page has unique `title` | Grep for metadata exports | Critical |
| Every page has unique `description` | Check metadata exports | Critical |
| `description` length 150-160 chars | Measure each page | High |
| `title` length 50-60 chars | Measure each page | High |
| Canonical URL on every page | Check `alternates.canonical` | Critical |
| Open Graph tags present | `curl -sA "facebookexternalhit/1.1" <url> \| grep -i og:` (bots get `<head>` metadata; on request-time rendered pages browsers and Googlebot get streamed metadata, while prerendered pages keep it in the initial `<head>`) | High |
| OG image configured (1200x630) | Test with Facebook Debugger | High |
| Twitter Card configured | Check `twitter:card` tags; preview in the X post composer (the Card Validator was retired) | Medium |

### 3. Structured Data

| Check | How to Verify | Priority |
|-------|---------------|----------|
| Organization schema on root layout | Check for JSON-LD in layout | High |
| BreadcrumbList on inner pages | Check for breadcrumb JSON-LD | Medium |
| Article schema on blog posts | Check blog page JSON-LD | High (if blog) |
| Product schema on product pages | Check product page JSON-LD | High (if e-commerce) |
| Search appearance not planned around FAQPage or HowTo | Grep for FAQPage / HowTo: both rich results are removed from Google Search; existing markup is harmless, but do not count it as SEO work | Low |
| WebSite markup on the home page with `name` / `alternateName` | Check home page JSON-LD | Medium |
| Structured data matches visible page content | Compare JSON-LD with the rendered page | High |
| Schema validates (Rich Results Test for types Google renders; Schema.org Validator for the rest) | Test live URLs | Critical |
| `schema-dts` installed for type safety | Check `package.json` | Medium |

### 4. Performance

| Check | How to Verify | Priority |
|-------|---------------|----------|
| LCP < 2.5s | PageSpeed Insights | Critical |
| INP < 200ms | PageSpeed Insights (field data) | Critical |
| CLS < 0.1 | PageSpeed Insights | Critical |
| LCP image has `loading="eager"` + `fetchPriority="high"` (`preload` in Next.js 16 only if one LCP image for all viewports; if the LCP image differs per viewport, `fetchPriority="high"` only — no `loading="eager"` or `preload`) | Check hero/banner Image component | High |
| All images have `sizes` prop | Grep for `<Image` without sizes | High |
| All images have `width`/`height` or `fill` | Grep for missing dimensions | High |
| `next/font` used (no external font requests) | Check network tab, layout.tsx | High |
| AVIF/WebP enabled | Check `next.config.ts` images.formats | Medium |
| No render-blocking third-party scripts | Check `<Script>` strategy props | Medium |

### 5. Content

| Check | How to Verify | Priority |
|-------|---------------|----------|
| Single H1 per page | Grep for `<h1` in pages | Critical |
| Logical heading hierarchy (no skips) | Audit heading levels per page | High |
| All images have alt text | Grep for `<Image` without `alt` | Critical |
| Alt text is descriptive (not "image") | Manual review | High |
| Descriptive internal link text | No "click here" anchors | Medium |
| Breadcrumb navigation present | Check inner pages | Medium |

### 6. Security & Mobile

| Check | How to Verify | Priority |
|-------|---------------|----------|
| HTTPS everywhere | Check production URL | Critical |
| Security headers configured | Check response headers | Medium |
| Mobile responsive | Test with Chrome DevTools | Critical |
| Touch targets >= 48px | Lighthouse accessibility audit | High |
| No horizontal scroll on mobile | Manual check | High |
| Viewport meta tag present | Inspect `<head>` in DevTools; customize via `export const viewport` | Critical |
| HTML document well under 2 MB uncompressed (Googlebot crawls the first 2 MB) | Check document size; keep metadata and JSON-LD near the top | Medium |

## Automated Testing with Playwright

Create an SEO test file that validates critical SEO elements:

```tsx
// tests/seo.spec.ts
import { test, expect } from '@playwright/test'

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'

test.describe('SEO Fundamentals', () => {
  test('homepage has correct meta tags', async ({ page }) => {
    // Playwright reads the rendered DOM, so streamed metadata (request-time rendered pages) is found here too.
    // For HTML-limited social bots, also run: curl -sA "facebookexternalhit/1.1" <url>
    await page.goto(BASE_URL)

    // Title
    const title = await page.title()
    expect(title).toBeTruthy()
    expect(title.length).toBeLessThanOrEqual(60)

    // Meta description
    const description = page.locator('meta[name="description"]')
    await expect(description).toHaveAttribute('content', /.{50,160}/)

    // Canonical
    const canonical = page.locator('link[rel="canonical"]')
    await expect(canonical).toHaveAttribute('href', /https?:\/\//)

    // OG tags
    await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', /.+/)
    await expect(page.locator('meta[property="og:description"]')).toHaveAttribute('content', /.+/)
    await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', /https?:\/\//)
  })

  test('all pages have single H1', async ({ page }) => {
    const pages = ['/', '/about', '/blog']
    for (const path of pages) {
      await page.goto(`${BASE_URL}${path}`)
      const h1Count = await page.locator('h1').count()
      expect(h1Count, `${path} should have exactly 1 H1`).toBe(1)
    }
  })

  test('all images have alt text', async ({ page }) => {
    await page.goto(BASE_URL)
    const images = page.locator('img')
    const count = await images.count()
    for (let i = 0; i < count; i++) {
      const alt = await images.nth(i).getAttribute('alt')
      // alt can be empty string (decorative) but must exist
      expect(alt, `Image ${i} missing alt attribute`).not.toBeNull()
    }
  })

  test('sitemap.xml is valid', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/sitemap.xml`)
    expect(response.status()).toBe(200)
    const body = await response.text()
    expect(body).toContain('<urlset')
    expect(body).toContain('<url>')
    expect(body).toContain('<loc>')
  })

  test('robots.txt is valid', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/robots.txt`)
    expect(response.status()).toBe(200)
    const body = await response.text()
    expect(body).toContain('User-agent')
    expect(body).toContain('Sitemap')
  })

  test('structured data is valid JSON', async ({ page }) => {
    await page.goto(BASE_URL)
    const scripts = page.locator('script[type="application/ld+json"]')
    const count = await scripts.count()
    expect(count).toBeGreaterThan(0)

    for (let i = 0; i < count; i++) {
      const content = await scripts.nth(i).textContent()
      expect(() => JSON.parse(content!), `JSON-LD block ${i} is invalid JSON`).not.toThrow()
      const parsed = JSON.parse(content!)
      expect(parsed['@context']).toBe('https://schema.org')
    }
  })
})
```

## Lighthouse CI Integration

Add Lighthouse CI to your GitHub Actions:

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with: { node-version: '22' }
      - run: npm ci && npm run build
      - uses: treosh/lighthouse-ci-action@v12
        with:
          urls: |
            http://localhost:3000/
            http://localhost:3000/blog
          budgetPath: ./lighthouse-budget.json
          uploadArtifacts: true
```

Lighthouse budget file:
```json
[{
  "path": "/*",
  "timings": [
    { "metric": "largest-contentful-paint", "budget": 2500 },
    { "metric": "cumulative-layout-shift", "budget": 0.1 },
    { "metric": "total-blocking-time", "budget": 200 }
  ],
  "resourceCounts": [
    { "resourceType": "script", "budget": 10 },
    { "resourceType": "total", "budget": 50 }
  ]
}]
```

## Full-Site Scan with Unlighthouse

For scanning every page on your site at once:

```bash
npx unlighthouse --site https://yourdomain.com
```

Unlighthouse crawls your entire site and runs Lighthouse on each page, producing a dashboard with aggregated results.

## Audit Report Template

After running the audit, present results in this format:

```
## SEO Audit Report — [Site Name] — [Date]

### Critical Issues (fix immediately)
- [ ] Issue description — affected pages — recommended fix

### High Priority (fix this sprint)
- [ ] Issue description — affected pages — recommended fix

### Medium Priority (plan for next sprint)
- [ ] Issue description — affected pages — recommended fix

### Passing
- [x] Item that passed verification
```