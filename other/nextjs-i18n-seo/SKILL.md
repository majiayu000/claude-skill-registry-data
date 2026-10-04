---
name: nextjs-i18n-seo
description: Audit/fix Next.js i18n SEO for the App Router — crawlability, 307→301 redirects, locale URLs, sitemap, hreflang. Use when diagnosing lost PageRank or i18n redirect bugs in middleware.
user-invocable: true
argument-hint: "[site URL or project path]"
metadata:
  version: "1.0.0"
---

# Next.js i18n SEO Fix

Multilingual Next.js sites commonly ship with a crawlability-killing bug: locale redirects that use **307 Temporary** instead of **301 Permanent**. This means Googlebot never transfers PageRank to the actual indexed URL. Fix this first — it's a one-line change with immediate impact.

## The Core Problem

When a user (or Googlebot) hits `/hexagrams/14`, Next.js middleware redirects to `/en/hexagrams/14`. The default `NextResponse.redirect(url)` issues a **307 Temporary Redirect**. Google does not transfer PageRank on 307s. Result: any backlink to the clean URL is wasted.

**Pages Router** doesn't have this problem because `getStaticPaths` generates pages at their final URL with no redirect hop.

---

## Phase 1: Audit the Site

### 1. Check the redirect status code
```bash
curl -I https://example.com/some-page
# Look for: Location: and HTTP/2 301 vs 307
```

### 2. Check robots.txt
```
https://example.com/robots.txt
```
- All paths should be allowed (or only `/api/` blocked)
- Sitemap URL must be listed

### 3. Check the sitemap
```
https://example.com/sitemap.xml
```
- Are all pages listed with their final (locale-prefixed) URL?
- Are `alternates.languages` hreflang entries present?

### 4. Inspect the middleware
Look for `NextResponse.redirect(url)` — if no status code is passed, it's a 307.

---

## Phase 2: Fix the 307 → 301 Bug

**File: `src/middleware.ts`** (or `middleware.ts` at root)

```ts
// ❌ BEFORE — issues 307 Temporary Redirect
const response = NextResponse.redirect(newUrl);

// ✅ AFTER — issues 301 Permanent Redirect (passes PageRank)
const response = NextResponse.redirect(newUrl, 301);
```

Also fix any locale alias redirects (e.g. `zh-hans` → `zh-CN`) the same way — they should already be 301 if added later, but verify.

**Commit message:**
```
fix: change locale redirect from 307 to 301 for SEO PageRank transfer
```

---

## Phase 3 (Optional but Recommended): No-Prefix Default Locale

The locale prefix (`/en/hexagrams/14`) adds an extra path segment vs. `/hexagrams/14`. For English-first sites, removing the prefix from the default locale gives cleaner URLs and eliminates the redirect entirely for the primary language.

### Middleware changes

```ts
const defaultLocale = 'en';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const pathnameHasLocale = nonDefaultLocales.some(
    (l) => pathname.startsWith(`/${l}/`) || pathname === `/${l}`
  );

  // Already has a non-default locale — pass through
  if (pathnameHasLocale) return NextResponse.next();

  // Has explicit /en/ prefix — strip it (301 to clean URL)
  if (pathname.startsWith('/en/') || pathname === '/en') {
    const url = request.nextUrl.clone();
    url.pathname = pathname.replace(/^\/en/, '') || '/';
    return NextResponse.redirect(url, 301);
  }

  // No locale prefix — serve as default (English) directly, no redirect
  return NextResponse.next();
}
```

### generateStaticParams changes

```ts
// Layout and page components: include '' (no prefix) for English
export async function generateStaticParams() {
  return [
    { locale: '' },      // English — served at root paths
    { locale: 'zh-CN' },
    { locale: 'zh-TW' },
  ];
}
```

### Sitemap changes

```ts
// English URLs use no prefix
const enUrl = `${baseUrl}/hexagrams/${h.id}`;
// Other locales keep prefix
const zhCNUrl = `${baseUrl}/zh-CN/hexagrams/${h.id}`;
```

### Hreflang

```html
<link rel="alternate" hreflang="en" href="https://example.com/hexagrams/14" />
<link rel="alternate" hreflang="zh-CN" href="https://example.com/zh-CN/hexagrams/14" />
<link rel="alternate" hreflang="x-default" href="https://example.com/hexagrams/14" />
```

---

## Checklist

```
[ ] curl -I site.com/some-page → confirm 301 (not 307)
[ ] curl -I site.com/en/some-page → confirm 301 to /some-page (if no-prefix)
[ ] sitemap.xml lists final URLs (no redirect hops)
[ ] hreflang present on all pages with x-default
[ ] robots.txt allows all content paths, blocks /api/
[ ] generateStaticParams covers all locale variants
[ ] No cookie-only locale detection (Googlebot ignores cookies)
```

---

## Why Pages Router Appeared Better

Pages Router with `getStaticPaths` serves pages at their exact URL with **zero redirect hops**. App Router with locale middleware adds a redirect layer. The framework itself isn't the problem — the redirect type (307 vs 301) and the locale URL strategy are what matter. App Router with 301 redirects and/or no-prefix default locale matches or exceeds Pages Router crawlability.

---

## Real-World Comparison

| | sixlines.online (App Router) | bookofchanges.academy (Pages Router) |
|---|---|---|
| Hexagram URL | `/en/hexagrams/14` | `/hexagrams/14` |
| Redirect on clean URL | 307 → locale URL ❌ | none ✅ |
| Sitemap entries | 192 (64 × 3 locales) | 64 |
| Middleware on every req | yes | no |
| Fix | Change to 301 + consider no-prefix | — |
