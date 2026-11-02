---
name: set-up-seo
description: Use when a public page must be found by search and answer engines — crawlability gate (content in served HTML), metadata, JSON-LD by page type, sitemap, robots.txt incl. AI crawlers, answer-ready structure. Audits built HTML from any stack.
---

# Set Up SEO

Discoverability as a checked property, not a vibe. Audit the *served* HTML, fix in
order: crawlability → metadata → structured data → sitemap/robots → answerability.

## 1. Gate — is this a public page?

Run the gate from `../_shared/page-types.md`. App surfaces behind auth: stop, wrong
catalogue. For this skill the gate doubles as the first audit: if the main content fails
the view-source test, **that is finding #1** and everything else waits —
see `./crawlability.md`.

## 2. Audit current state

```bash
curl -s "$URL" -o /tmp/page.html
grep -oiE "<title>[^<]*</title>" /tmp/page.html
grep -ciE "<meta name=\"description\"" /tmp/page.html
grep -ciE "rel=\"canonical\"" /tmp/page.html
grep -ciE "property=\"og:(title|description|image)\"" /tmp/page.html
grep -ciE "application/ld\+json" /tmp/page.html
curl -s "$ORIGIN/robots.txt"; curl -sI "$ORIGIN/sitemap.xml" | head -1
```

Audit each *template* (home, article, product), not just one URL. Apply only what's
missing; a conforming page is a no-op.
(The `-c` counters count matching *lines*, not tags — minified heads collapse to 1 — and
the patterns assume double-quoted attributes; treat them as presence checks, not totals.)

## 3. Metadata per page

- **`<title>`** — unique per page, the page's promise, brand last ("Outcome the visitor
  gets — Brand"). ~60 chars is a display heuristic: Google truncates by pixel width and
  may rewrite the title; it is not a rule.
- **`<meta name="description">`** — the snippet pitch containing the page's one job.
  Google often substitutes its own snippet; write it for the click, not for a length.
- **`<link rel="canonical">`** — absolute URL, on every public page (self-referencing is
  correct); one canonical per duplicate-reachable content.
- **Open Graph / Twitter** — `og:title`, `og:description`, `og:image` (1200×630),
  `twitter:card` — this is what the link looks like when shared.
- All of it must be in the **served** HTML (step 1), not injected client-side.

## 4. Structured data (JSON-LD)

Pick types from the table in `./structured-data.md`; the hard rule is **schema mirrors
visible content, never invents it**. Example for an article page:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Exactly the visible h1",
  "description": "Matches the meta description",
  "datePublished": "2026-05-01",
  "dateModified": "2026-06-10",
  "author": { "@type": "Person", "name": "The visible byline" }
}
</script>
```

`FAQPage` only for real, visible FAQ sections — Google stopped showing FAQ rich results
on 2026-05-07 for all sites, so the markup earns no SERP feature; it is optional
(`./structured-data.md`). No `HowTo` markup: that rich result went away in 2023.

## 5. sitemap.xml + robots.txt

```
# robots.txt — at the origin root
User-agent: *
Allow: /
Sitemap: https://example.com/sitemap.xml
```

- Sitemap: every *canonical, public* URL — no redirects, no noindexed pages, no params.
  Generate at build; `lastmod` only if it's real.
- Submit once via Search Console (the old ping endpoints are retired); after that the
  `Sitemap:` line is discovery enough.
- **`Disallow` is not `noindex`** — to de-index, serve `<meta name="robots"
  content="noindex">` on a crawlable page (`./crawlability.md`).
- **AI crawlers are a policy decision, not a default.** Training bots and search/answer
  bots are separate user agents — allow or block each on purpose (`./crawlability.md`).
  Landing pages that want to be cited keep the search bots allowed.

## 6. Answer-engine readability

Answer engines quote pages that answer cleanly. The moves are content structure, not
tags:

- A section heading phrased as the question users ask, followed **immediately** by a
  direct answer in 2–3 sentences — elaboration after, never before.
- Visible **author**, **published/updated dates**, and (for health/finance/legal topics)
  a named reviewer — trust signals machines and humans share.
- Enumerable facts as lists or tables — extractable beats prose.
- One idea per paragraph; the page answers its `<title>`'s promise.

This is the generic core of GEO/AEO; project-specific scoring belongs in a rubric
(`../audit-content-quality/SKILL.md`). No special tag, file, or schema is known to make
answer engines cite a page — `llms.txt` included (`./crawlability.md`). Clear, visible,
crawlable content is the whole lever.

## 7. Verify

```bash
curl -s "$URL" | grep -c "ld+json"        # ≥1
curl -s "$ORIGIN/robots.txt" | grep -ci "^Sitemap:"   # 1
```

Paste the URL into `validator.schema.org` (0 errors) and, for Product/Article/Breadcrumb,
the Rich Results Test. Fetch
with JS disabled: title, description, content all present. Share the URL in a chat
client: the OG preview renders.

## References
- ./crawlability.md — the view-source test, the empty-shell symptom, Disallow vs noindex, remediation pointers.
- ./structured-data.md — type table, the mirror rule, the FAQ caveat, validation.
- ../_shared/page-types.md — the gate and the priority inversion.
- ../audit-content-quality/SKILL.md — rubric-driven scoring on top of this baseline.
- ../../frontend/set-up-document-head/SKILL.md — in-app (SPA) head management; it handles tabs and a11y, not crawlability.
