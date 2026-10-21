---
name: website-seo-geo
description: >
  The on-page SEO + GEO contract for a new site: exact metadata limits (title
  50–60 chars, meta description 140–160 with a 120 floor), og:title/og:description == title/desc,
  twitter inherits OG, clean canonical == og:url, required JSON-LD schema, and
  llms.txt for AI answer engines. Use when building or reviewing a page's head
  / metadata (step 6 of the new-website pipeline), or when a title/description is
  too long or tags are out of sync. Enforced by the seo.spec.ts check in the
  new-website test suite. Delegates depth to ai-seo (GEO) and schema-markup.
  Trigger phrases: "SEO metadata", "title too long", "meta description length",
  "og tags", "twitter card", "canonical", "is my SEO set up", "llms.txt", "GEO",
  "head tags", "structured data on this page".
---

# Website SEO & GEO

The metadata contract every page must satisfy. This skill owns the **exact
limits and consistency rules**; it hands depth off to the existing global skills:
`ai-seo` (AI answer-engine / GEO strategy), `schema-markup` (rich JSON-LD),
`seo-audit` (technical SEO / crawl / Core Web Vitals — see also `website-qa`).

## The limit table (enforced)

| Tag | Ideal | Hard cap | Why |
|---|---|---|---|
| `<title>` | 50–60 chars | ~60 | Google truncates ~580–600px; >60 risks a cut, >70 almost always cut |
| `<meta description>` | 140–160 chars | ~160 | Truncates ~920px; >160 cut; <120 wastes space / keyword room |
| `og:title` / `og:description` | = `<title>` / = description | — | Test fails on any divergence |
| `twitter:title` / `twitter:description` | inherit OG (same strings) | — | `twitter:card = summary_large_image` |

The test counts characters (em-dash, en-dash, curly apostrophe each = 1 char but
render wider — stay clear of the cap). `<meta name="description">` is **separate
from** `og:description`; one does not replace the other — ship both, in sync.

### German (and other compounding languages) eat the budget faster

The limits above are pixel-render caps, not word counts — they don't change per
language, and the numbers in the table stay exactly as specified. But German
compound nouns (`Suchmaschinenoptimierung`, `Barrierefreiheit`,
`Barrierefreiheitsprüfung`) pack far more meaning per character into a single
unbroken word than English does, so the same 50–60 / 140–160 char cap holds
noticeably less content once translated. Write for it deliberately:

- **Front-load the key term.** German syntax tends to push the important noun
  toward the end of a compound or clause; if you translate an English title
  1:1 the keyword can land past where truncation cuts. Put the primary
  keyword/term first, then qualify it, rather than burying it in a trailing
  compound.
- **When one natural compound blows the budget, don't force it — restructure.**
  If `Barrierefreiheitsprüfung` (24 chars alone) doesn't leave room for
  anything else, reach for a shorter near-synonym or split brand/category from
  descriptor with a colon or dash: `Website-Builder: barrierefrei &
  SEO-optimiert` reads better and fits, where one giant compound noun forces
  an awkward truncation or abbreviation.
- **Budget for ~10–15% fewer effective words of meaning** than an English
  title/description of the same character count. Plan the German copy's
  content around that from the start — don't write the English version, translate
  it, and then trim words until the character count fits; that's how you end
  up with a mangled abbreviation instead of a deliberate, readable title.

- **Target the LOWER half of the title range (~50–55 chars) for German.**
  Google truncates by pixel width (~580px), not characters — German capitalizes
  every noun, and capitals plus umlauts render wide, so a passing 60-char
  German title can still be cut in the SERP. The 60-char cap is a ceiling,
  not a safe harbor.

This is a **writing tactic**, not a test change: `seo.spec.ts` enforces the same
character counts regardless of language, and it should — the fix here is how you
write within that budget, not the budget itself.

## Consistency rules

- One pair of inputs `(title, description)` drives `<title>`, OG, Twitter,
  canonical and the WebPage schema — wired once in the new-website skill's
  `templates/astro/src/layouts/Base.astro`, so pages only pass `title`/`description`
  and the tags can never drift.
- **Canonical** is clean (no `.html`), absolute, and equals `og:url` and the
  page's `sitemap.xml` `<loc>`.
- **No trailing slash (convention):** URLs are `/about`, not `/about/` (home stays `/`).
  The starter sets `trailingSlash: 'never'` + `build.format: 'file'`; write internal links
  without a trailing slash. `navigation.spec.ts` flags any `/about/` link (404/redirect hop)
  and `seo.spec.ts` pins `canonical == SITE.url + path`, so the whole site stays consistent.
- Exactly one `<h1>` per page (its text MAY differ from the keyword-tuned title).
- **ASCII slugs only:** transliterate German umlauts/ß to digraphs (`/ueber-uns`,
  not `/über-uns`) — machine-serialized URLs (canonical, sitemap) percent-encode
  non-ASCII while hand-written strings (PAGES, llms.txt, authored links) stay
  raw, a mismatch factory (site-architecture has the full rule).
- **og:locale derives from `<html lang>`** (de → de_DE; regioned tags → base+region;
  one shared `ogLocaleFor()` in `src/config.ts`, emitted by Base.astro, asserted
  by `seo.spec.ts` whenever a value derives — mapped bases and all regioned
  tags) — a German page silently carrying `og:locale en_US` is exactly the
  drift this row exists to stop.

## Schema (JSON-LD) — minimum per page

- Every page: `WebSite` + `Organization` (once, site-wide) and a `WebPage` node.
- Add page-type schema via `schema-markup`: `BreadcrumbList` on nested pages,
  `FAQPage` on FAQs, `Article`/`TechArticle` with author `@id` + dates on posts,
  `Service`/`Product` as relevant. Author/Organization `@id`s and `sameAs` feed
  EEAT (see `website-content-guide`); keep `sameAs` URLs that actually resolve.
- **`FAQPage` describes the Q&A to machines, not a Google rich result.** Since August
  2023 Google shows FAQ rich results only for well-known, authoritative government
  and health sites ([Google](https://developers.google.com/search/blog/2023/08/howto-faq-changes)); most sites get none. Don't promise one.
- **Datetimes in JSON-LD carry an explicit timezone.** `VideoObject.uploadDate`,
  `Event.startDate/endDate`, `Offer.validFrom`, `Article` dates etc. must be full
  ISO-8601 with an offset (`2026-03-11T00:00:00+00:00`, not a bare `2026-03-11`).
  Google's video parser rejects a date-only `uploadDate` as "missing a timezone" /
  "invalid datetime value" — a GSC error that only surfaces weeks after launch.
- Validate with Google Rich Results Test / schema.org validator before launch.

## GEO (generative engine optimization)

- Ship `/llms.txt` (template in the starters): a curated, accurate index of key
  pages + facts for AI answer engines. **Write it in the site's primary content
  language** (German site → German descriptions; multilingual site → each
  entry's description in that page's language) — same precedent as the
  privacy page: an answer engine quoting your English blurb to a German
  searcher is the wrong-language failure again. Keep it in sync with the site — route
  *coverage* is enforced both ways in the new-website starter suite:
  `tests/llms-coverage.spec.ts` fails if any `PAGES` route is missing from it,
  or if a same-site entry goes stale (page removed/renamed). Add the page's
  `- [Title](URL): description` line in the same commit as the page;
  deliberately-hidden pages (paid-ad landers) go in its `LLMS_EXEMPT` with a
  reason. On a site that predates the guard, copy the spec in from the starter
  before relying on it.
- For deeper GEO/AEO (being cited by ChatGPT/Perplexity/AI Overviews, answer
  formatting, entity coverage), run **`ai-seo`** — do not duplicate it here.

## PDFs you host (the doc-title IS the search-result title)

A PDF has no `<title>` — Google and **Bing** print its embedded **doc-title** as
the search-result title. Authoring tools ship a placeholder
("PowerPoint-Präsentation", "Microsoft Word - report.docx") or a working-filename
slug, which Bing flags as *"page title too short"* (seen in production on a real
site built with this kit, 2026-06-19). So any PDF you put in `public/` needs a
descriptive doc-title set **before** it ships:

- **Title convention:** the same human title the page uses for that document —
  e.g. `Talk Title — Speaker | Brand`. ≥15 chars, never the authoring placeholder.
- **Set it in BOTH places crawlers read** — the Info dict `/Title` **and** the XMP
  `dc:title`. Fixing only one leaves the stale title visible. Use the helper:
  ```bash
  python3 scripts/set_pdf_title.py public/<file>.pdf "Descriptive Title | Brand" --author "Author"
  ```
  (needs `pip install pypdf`; local authoring tool only — the test below is dep-free.)
- **Enforced by `seo.spec.ts`:** the PDF guard scans `public/**/*.pdf` and fails the
  build on a placeholder, a title under 15 chars, or no doc-title at all. No-op for
  sites that host no PDFs.
- After fixing a live PDF, **re-submit its URL in Bing/Google** so it recrawls.

## Done means

`npm test` green — specifically `seo.spec.ts`: every title/description within
limits, og/twitter/canonical in sync, JSON-LD parses, a sitemap exists, and every
hosted PDF carries a descriptive doc-title (not an authoring placeholder).

## Judgment pass (what the tests cannot check)

`seo.spec.ts` proves the metadata is *well-formed*; it cannot tell you it is *good*.
Once it is green, do a one-page judgment read — this is a model call (Rule 5: use the
model only where code can't answer):
- **Title matches search intent**, not just ≤60 chars — would a searcher click it
  over its SERP neighbours?
- **Description earns the click** — answers the query, not keyword-stuffed.
- **Schema is semantically right** — correct `@type` and real relationships, not
  merely valid JSON (a valid-but-wrong `@type` still passes the test).
- **`llms.txt` is accurate vs the live site** — facts and wording current, no
  drift (route *coverage* is the mechanical half, pinned by
  `tests/llms-coverage.spec.ts`; this read is about the wording half).
- **EEAT signals resolve** — `sameAs` / author URLs actually load and corroborate.

Intent and semantics only. Structural correctness is the test's job; cross-file
route/URL/config/SEO consistency is the `website-review` (Double-Knuth) skill's job.
