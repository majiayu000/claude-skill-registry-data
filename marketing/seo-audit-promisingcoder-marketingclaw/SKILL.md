---
name: seo-audit
description: "Running a no-API on-page SEO audit of a URL or set of pages — title/meta tags, headings, schema.org structured data, internal links, image alts, canonicals, and Core Web Vitals pointers — using existing fetch/browser tools."
metadata: { "marketingclaw": { "emoji": "🔍" } }
---

# SEO Audit Skill

An on-page SEO audit playbook that needs no API keys — it works entirely off fetching the page
HTML (via the web-fetch tool, the browser-requests skill, or `curl`) and reading it against the
checklist in `references/checklist.md`.

## When to use

Triggered by requests like "audit this page for SEO", "why isn't this page ranking", "check our
on-page SEO", or as a step inside `marketing-report`'s monthly SEO section.

## Workflow

1. **Fetch the page.** Prefer the browser-requests skill or a web-fetch tool if the page is
   JS-rendered (client-side routed content won't show up in raw HTML); otherwise
   `curl -sL "$URL"` is enough for server-rendered pages. Fetch the rendered DOM, not just the
   initial HTML, when the site is a JS framework (Next.js, Astro islands, React SPA) so you see
   what search engines actually see after rendering (or check if the site pre-renders/SSRs).
2. **Walk the checklist** in `references/checklist.md` section by section: title/meta,
   headings, structured data, internal linking, images, canonical/indexability, and Core Web
   Vitals pointers.
3. **Score each item** pass/warn/fail with the specific text found (e.g. the actual `<title>`
   content and its character count) — don't just say "title tag missing", show what's there.
4. **Prioritize fixes.** Rank findings by estimated impact: missing/duplicate title or meta
   description and non-canonical/noindex mistakes first (these block ranking entirely), then
   heading structure and internal links, then image alts and minor schema gaps last.
5. **Report top 3-5 actions**, not an exhaustive dump — this is meant to be actionable, not a
   250-line checklist regurgitated back at the user.

## Multi-page audits

For a whole site/section, fetch the sitemap first (`/sitemap.xml`, or ask the `gsc` skill's
sitemaps endpoint) to get the URL list, sample a representative set (homepage, a top landing
page, a blog post, a product/pricing page) rather than crawling everything, and look for
cross-page patterns (e.g. every product page missing a meta description) rather than treating
each page in isolation.

## Core Web Vitals

This skill does not call PageSpeed Insights or CrUX APIs (no API key required by design). Instead:

- Flag obvious causes visible in the HTML/network trace: unoptimized/oversized images without
  `width`/`height` (CLS risk), render-blocking synchronous `<script>` tags in `<head>` (LCP/FID
  risk), missing `font-display` on `@font-face` (CLS/FOIT risk), and excessive third-party
  scripts.
- Point the user to `https://pagespeed.web.dev/analysis?url=<page-url>` for the actual measured
  Core Web Vitals numbers (field + lab data) rather than guessing at scores.

## Notes

- No environment variables or API keys required — this skill is intentionally free-first.
- Pair with the `gsc` skill (if configured) to check whether a page is actually indexed and to
  see real click/impression/position data alongside the on-page findings — a perfect on-page
  score with zero impressions usually means an indexing or internal-linking problem, not a
  content problem.
- Pair with `keyword-research` when the ask is "what should this page target" rather than "audit
  what's already here."
