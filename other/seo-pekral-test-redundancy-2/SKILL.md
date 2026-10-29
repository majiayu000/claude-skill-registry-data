---
name: seo
description: "Use when auditing, planning, or implementing SEO in a Laravel app — crawlability, indexability, JSON-LD structured data in Blade, Core Web Vitals, on-page tags, keyword mapping, competitor gap analysis, E-E-A-T content quality, and measurement."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/laravel/laravel.md` for routing, Blade, and asset conventions.
- Apply `@rules/security/frontend.md` — never inject unsanitized user content into JSON-LD, meta tags, or `<head>`; escape every dynamic value.
- Fix technical blockers before content optimization.
- One page maps to one clear primary search intent.
- Every recommendation must be page-specific and implementable. No generic "improve SEO" output.
- Mobile-first: indexing is mobile-first, so audit the mobile render.
- White-hat only: recommend nothing that violates search-engine guidelines (no cloaking, paid links, doorway pages, or scaled spam content).

## Modes

This skill runs in one of two modes, selected by the caller via `MODE` (default `optimize`):

- **`optimize` (default)** — full SEO work: write `<head>` tags, canonical links, and JSON-LD into Blade layouts, edit `robots.txt` and the sitemap, restructure internal linking, and change what a page loads. Every section below behaves as written unless it is explicitly flagged for `MODE=cr`.
- **`cr` (read-only lens — invoked by `@skills/code-review/SKILL.md`, `code-review-github`, `code-review-jira`, and `code-review-bugsnag` when the diff touches a public crawl or indexing surface)** — **never modify a Blade view, a route, `robots.txt`, a sitemap, or any other project file, never author a test, never stage / commit / push, never run fixers or checkers, and never chain a follow-up review.** Scope the analysis to the lines added or modified by the PR diff and return the findings as markdown only, carrying the reproducer fields the CR folds into its standard Critical / Moderate buckets.
Every instruction below that would touch a file — add, set, rewrite, redirect, canonicalize, or any other such verb — is emitted as a written proposal carrying a concrete Blade or configuration snippet, never applied to the project.

> **What this lens owns in a CR:** the crawler-facing contract of the surface the diff changes — what `robots.txt` allows and blocks, what the sitemap lists, whether the canonical is self-consistent and non-looping, whether a page is unintentionally `noindex`, the title / meta-description / heading structure of the changed page, whether a JSON-LD block is valid and matches content actually present, and what the changed `<head>` asks the browser to fetch first for LCP.
> It **defers the markup a view renders** — component composition, state placement, accessibility semantics, and design tokens — to the three frontend lenses (`@skills/frontend-patterns/SKILL.md`, `@skills/frontend-a11y/SKILL.md`, `@skills/design-system/SKILL.md`), and **defers which bundle that view loads** — the entrypoint, the `@vite` directive that pulls it in, the manifest behind it, and how it splits — to `@skills/vite-patterns/SKILL.md`. It never raises a finding one of those four owns.
> Those boundaries divide the *dimensions* of a `<head>` change, never its lines: one `@vite` line inside a layout carries a bundle finding from the build lens and, when the same change also drops the preload the largest contentful element needs, an LCP finding from this lens, because those are two different defects.
> An **unescaped dynamic value** rendered into a meta tag, a canonical `href`, or a JSON-LD payload is not this lens's either: `@rules/security/frontend.md` and `@skills/security-review/SKILL.md` own it, and a security finding is never moved out of a security owner.
> The lens judges the surface the project publishes. **Never raise a finding whose only fix is to index a surface the project deliberately keeps out of the index** — an admin, staging, or authenticated layout carrying `noindex` is the correct answer, not a defect on the diff.

## Use when
- Auditing crawlability, indexability, canonicals, or redirects.
- Improving title tags, meta descriptions, or heading structure.
- Adding or validating structured data (JSON-LD).
- Improving Core Web Vitals (LCP, INP, CLS).
- Doing keyword research and mapping keywords to URLs.
- Planning internal linking, sitemap, or robots changes.
- Comparing against competitors to find content or keyword gaps.
- Assessing content quality and E-E-A-T signals.
- Defining what to measure after changes ship.

## Technical SEO

### Crawlability
- `robots.txt` allows important pages and blocks low-value surfaces (e.g. `/admin`, filtered listing permutations). In Laravel, serve a static `public/robots.txt` or a route that renders one per environment (block everything on staging).
- No important page is unintentionally `noindex`.
- Important pages are reachable within a shallow click depth (3 clicks from the homepage).
- Avoid redirect chains longer than two hops. Audit Laravel `Redirect::` rules and web-server rewrites for stacked redirects.
- Canonical tags are self-consistent and non-looping.

### Indexability
- Preferred URL format is consistent (trailing slash, casing, `www` vs apex). Enforce with a single canonical host and HTTPS redirect.
- Generate canonical URLs from named routes, not hand-built strings, so they stay consistent: `route('post.show', $post)`.
- Multilingual pages need correct `hreflang` when locales exist.
- Sitemaps reflect the intended public surface only. Build a sitemap from Laravel routes/models, or use the optional `spatie/laravel-sitemap` package to crawl and emit `sitemap.xml`.
- No duplicate URLs compete without canonical control (e.g. pagination, query-string facets).

### Site-health audit checklist
Walk these every audit; each item maps to a concrete file, route, or response to inspect — never report a category without naming where it occurs.

| Check | What to look for | Where in Laravel |
| --- | --- | --- |
| Crawl errors | 4xx/5xx on linked URLs | server logs, route list, `php artisan route:list` |
| Broken links | dead internal/outbound `href`s | Blade views, content models, a crawl pass |
| Redirect chains | 2+ stacked hops | `Redirect::` rules, web-server rewrites |
| Mixed content | `http://` assets on an HTTPS page | Blade asset refs; force `asset()`/`secure_url()` |
| Duplicate content | same intent on multiple URLs | facets, pagination, casing/slash variants |
| Thin content | low-value near-empty pages | auto-generated tag/archive pages |
| Orphan pages | published but unlinked internally | compare sitemap/routes against internal links |

- Orphan detection: a page in the sitemap or route list with no internal `href` pointing at it cannot be discovered by crawlers following links — surface it and add an internal link or drop it from the sitemap.
- Mixed content: an HTTPS page that loads any `http://` asset is downgraded and may be blocked by the browser. Derive asset URLs from `asset()` / `secure_url()` so they inherit the request scheme.

### Canonical + meta in a Blade layout
```blade
{{-- resources/views/layouts/app.blade.php (inside <head>) --}}
<title>@yield('title', config('app.name'))</title>
<meta name="description" content="@yield('meta_description', '')">
<link rel="canonical" href="{{ $canonical ?? url()->current() }}">
@hasSection('noindex')
    <meta name="robots" content="noindex,nofollow">
@endif
@stack('schema')
```

```blade
{{-- a page view --}}
@section('title', $post->title . ' | ' . config('app.name'))
@section('meta_description', Str::limit(strip_tags($post->excerpt), 155))
@php($canonical = route('post.show', $post))
```

## Core Web Vitals
Targets: LCP < 2.5s, INP < 200ms, CLS < 0.1.

- LCP: preload the hero image and critical fonts; ship hashed assets through Vite (`@vite`) so they cache long-term. Use `loading="eager"` and `fetchpriority="high"` on the LCP image; `loading="lazy"` on below-the-fold images.
- INP: trim heavy JS. Keep Alpine.js components small and defer non-critical Livewire polling. Avoid long synchronous work in event handlers.
- CLS: reserve layout space — set explicit `width`/`height` on images, and avoid injecting content above existing content. Tailwind `aspect-*` utilities help reserve space.
- Reduce render-blocking work: let Vite split CSS/JS, defer non-critical scripts, and self-host fonts with `font-display: swap`.

## Structured data (JSON-LD)
Emit JSON-LD in the layout via a pushed stack so each page contributes its own schema. Match schema to content that is actually present.

- Homepage: `Organization` or local business schema where appropriate.
- Editorial pages: `Article` / `BlogPosting`.
- Product pages: `Product` and `Offer`.
- Interior pages: `BreadcrumbList`.
- Q&A sections: `FAQPage` only when the content truly matches.

```blade
{{-- a page view --}}
@push('schema')
<script type="application/ld+json">
{!! json_encode([
    '@context' => 'https://schema.org',
    '@type'    => 'Article',
    'headline' => $post->title,
    'author'   => ['@type' => 'Person', 'name' => $post->author->name],
    'publisher'=> ['@type' => 'Organization', 'name' => config('app.name')],
    'datePublished' => $post->published_at->toIso8601String(),
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) !!}
</script>
@endpush
```

Build the array with `json_encode` (never string-concatenate user input) so values are escaped and the document stays valid. Validate the emitted markup with Google's Rich Results Test before relying on it.

## On-page rules

### Title tags
- Aim for roughly 50–60 characters.
- Put the primary keyword or concept near the front.
- Write for humans, not stuffed for bots.

### Meta descriptions
- Aim for roughly 120–160 characters.
- Describe the page honestly and include the main topic naturally.

### Headings
- Exactly one `H1` per page.
- `H2`/`H3` reflect real content hierarchy; do not pick heading levels for visual styling.

### Formulas
```text
Title:  Primary Topic - Specific Modifier | Brand
Meta:   Action + topic + value proposition + one supporting detail
```

## Competitor gap analysis
Use competitors to find concrete, page-level opportunities — never to copy.

- **Keyword gaps:** queries competitors rank for that the site does not. Map each gap to a new or existing URL, not a generic "write more content" note.
- **Content gaps:** topics or intents covered by competitors but missing from the site's coverage map.
- **SERP-feature gaps:** rich results competitors win (breadcrumb, product, review snippets) that the site's schema does not yet support. Confirm that Google still offers the result type for this kind of site before recommending it.
- **Site-structure gaps:** shallower paths or clearer internal linking that make competitor pages easier to crawl.
- Output each gap as `[gap type] target query/topic → owning URL → concrete change`, so it slots straight into the audit output below.

## Content quality and E-E-A-T
Search engines reward Experience, Expertise, Authoritativeness, and Trustworthiness. Tie each signal to something on the page.

- **Experience / expertise:** show a real, attributed author (`Article.author` in JSON-LD plus a visible byline) and first-hand detail, not paraphrased generalities.
- **Authoritativeness:** cite primary sources and earn relevant links naturally; do not buy or exchange links.
- **Trust:** keep content accurate and current, show a clear publish/updated date, and make contact / ownership discoverable.
- **Helpful-content first:** write for the person with the query. Consolidate or differentiate thin near-duplicate pages instead of keeping them for keyword coverage.

## Measurement and reporting
Every recommendation needs a measurable outcome; pick the metrics that match the change and capture a baseline before shipping.

- **Visibility:** organic traffic, impressions, average position, keyword rankings.
- **Engagement / conversion:** click-through rate, conversions, assisted conversions.
- **Technical health:** Core Web Vitals (field data), index coverage, crawl errors.
- Source field data from Search Console and Analytics, not lab numbers alone.
- State the metric, its baseline, and the expected direction with each finding so the change is verifiable after release.

## Tooling
Validate audits and findings with real tools rather than asserting them:

- **Search Console** — index coverage, queries, impressions/CTR, Core Web Vitals field data.
- **PageSpeed Insights / Lighthouse** — Core Web Vitals diagnostics and lab traces.
- **Rich Results Test** — confirm JSON-LD is valid and eligible before relying on it.
- **A crawler** (e.g. Screaming Frog) — broken links, redirect chains, orphan pages, duplicate titles.
- Prefer Laravel-native checks where they suffice: `php artisan route:list` for the public surface, a sitemap build for the intended index set.

## Audit output shape
```text
[HIGH] Duplicate title tags on product pages
Location: resources/views/products/show.blade.php
Issue: @section('title') falls back to the app name for every product, weakening relevance and creating duplicate signals.
Fix: Render a unique title from the product name and primary category.
Measure: distinct title coverage in Search Console; expect duplicate-title warnings to drop.
```

## Anti-patterns

| Anti-pattern | Fix |
| --- | --- |
| keyword stuffing | write for users first |
| thin near-duplicate pages | consolidate or differentiate them |
| schema for content that is not present | match schema to reality |
| advice without checking the actual page | read the real Blade view first |
| generic "improve SEO" output | tie every recommendation to a page or asset |
| hand-built canonical URLs | derive from named routes |
| buying or exchanging links | earn links through useful content |
| recommendation with no metric | state the metric and baseline to verify it |

## Done when
- robots.txt, canonicals, and redirects are correct with no unintended `noindex`.
- The site-health checklist passes: no crawl errors, broken links, mixed content, redirect chains, orphan pages, or thin/duplicate content go unsurfaced.
- Sitemap reflects the public surface and important pages are shallow-depth.
- Each audited page has one H1, a 50–60 char title, and a 120–160 char meta description.
- Valid JSON-LD matches the page's real content and passes the Rich Results Test.
- LCP/INP/CLS targets are met or have a concrete remediation plan.
- Competitor and content gaps are captured as page-level, actionable findings.
- Every finding cites a specific file or URL, a concrete fix, and a metric to verify it.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
