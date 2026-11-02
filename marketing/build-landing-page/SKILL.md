---
name: build-landing-page
description: Use when building or restructuring a landing, marketing, or other public conversion page — checks it against a section grammar, one conversion goal, a semantic skeleton, and a hero LCP/CLS budget. Works on built HTML from any stack.
---

# Build Landing Page

A landing page has one job. This skill names it, audits which sections serve it, adds
only what's missing, and holds the hero to a performance budget — because on a public
page LCP and CLS are ranking and revenue, not polish.

## 1. Gate — is this a public page?

Run the gate from `../_shared/page-types.md`: must this page be findable and readable
without JS? If it's an authenticated app surface, stop — this skill doesn't apply; the
`skills/frontend/` catalogue owns app screens.

## 2. Audit current state

Work from the built/served HTML (a URL or a file from `dist/`/`build/`/`out/`):

```bash
curl -s "$URL" -o /tmp/page.html        # or cp the built file
grep -ci "<h1" /tmp/page.html                                  # exactly 1?
grep -oE "<(header|main|section|footer|nav)\b" /tmp/page.html | sort | uniq -c   # landmarks
grep -oiE "<(img|picture|video)[^>]*" /tmp/page.html | head -5                   # hero media + attrs
```

Read the page and list: which grammar sections exist, what the `h1` claims, how many
competing CTAs there are. **Prerequisite check:** if the main content isn't in the HTML
(view-source test, `../_shared/page-types.md`), fix crawlability first —
`../set-up-seo/SKILL.md`.

## 3. Name the one job

Every landing page converts toward exactly one action: sign up, buy, book, subscribe,
download. Name it in one sentence ("this page exists to get a demo booked"). If nobody
can, that is the first finding — no section work matters until the job is named. Every
primary CTA on the page is *that* action; anything else is subordinate (footer, text
links).

## 4. Decide what to do

- No page yet → compose from the grammar (step 5), required sections first.
- Page exists, sections missing for its goal → add only those.
- All sections present → tighten against the grammar's must-haves (step 5) and the
  budget (step 7). Re-running on a conforming page changes nothing.

## 5. Section grammar

Walk top to bottom; details and anti-patterns in `./section-grammar.md`.

| Section | Its job | Must contain | Skip when |
|---|---|---|---|
| Hero | state value + action | `h1` = outcome (not product name); one primary CTA above the fold; LCP visual on budget | never |
| Social proof | borrow trust | real logos / named quotes / specific numbers | nothing real yet — omit, don't fake |
| Problem → solution | mirror the pain | the problem in the visitor's words, then the turn | product self-evident (waitlist) |
| Features as benefits | capability → outcome | each item leads with what the visitor gets | single-feature page |
| Pricing | remove the price question | real numbers or honest "from …"; one recommended tier | no self-serve price |
| FAQ | answer created objections | 4–8 real questions, direct answers (visible text first; schema is optional, see `../set-up-seo/structured-data.md`) | nothing left open |
| Final CTA | catch the convinced scroller | one line of value + the same primary action; no new links | single-screen page |

## 6. Semantic skeleton

Landmarks and heading order are accessibility and machine-readability at once:

```html
<header><!-- logo, minimal nav --></header>
<main>
  <section aria-labelledby="hero-h">
    <h1 id="hero-h">Outcome the visitor gets</h1>
    <p>One supporting line — the mechanism.</p>
    <a class="cta" href="#signup">The one action</a>
  </section>
  <section aria-labelledby="proof-h"><h2 id="proof-h">…</h2>…</section>
  <!-- further sections: h2 each, h3 inside, no skipped levels -->
</main>
<footer><!-- legal links: imprint/privacy — required, not optional chrome --></footer>
```

Exactly one `h1`. Every section gets a real heading — screen readers and answer engines
navigate by them.

## 7. Hero performance budget

The hero owns LCP and most CLS risk. Core Web Vitals "good" thresholds, judged at the
75th percentile of real page loads (mobile and desktop separately): **LCP ≤ 2.5 s,
CLS ≤ 0.1, INP ≤ 200 ms** (web.dev/articles/vitals, verified 2026-10-09). A public page
with near-zero JS rarely fails INP; LCP and CLS are where it is won or lost.

```html
<!-- the LCP image: dimensions reserve space (CLS), priority wins the network race -->
<img src="/hero.avif" alt="What the image shows" width="1200" height="800"
     fetchpriority="high" decoding="async">
<!-- a hero font: preload + swap so text is never invisible -->
<link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin>
```

```css
@font-face { font-family: Heading; src: url(/fonts/heading.woff2) format('woff2');
             font-display: swap; }
```

- Modern format (AVIF/WebP), sized for its largest rendered width — not the original.
  Bare AVIF accepts a small no-support tail; wrap in `<picture>` with WebP/JPEG
  `<source>` fallbacks when the audience skews to older browsers.
- `width`/`height` (or CSS `aspect-ratio`) on **every** image so nothing shifts.
- No carousel, no autoplay video, no JS-gated rendering in the hero — each delays the LCP
  element or shifts layout. Scripts use `defer` (or
  `type="module"`) and sit below the fold; a public page's JS budget starts at zero
  (`../_shared/page-types.md`).

## 8. Verify

```bash
curl -s "$URL" | grep -ci "<h1"          # 1
curl -s "$URL" | grep -ci "fetchpriority"   # ≥1 (the hero image)
```

View the page with JS disabled: full content, readable order. Run Lighthouse (mobile
profile) on the deployed URL: LCP ≤ 2.5 s, CLS ≤ 0.1. Lighthouse is a lab run on one
device; the pass/fail Google uses is field data (CrUX, or RUM via `configure-analytics`),
which a new page only has after about four weeks of traffic.

## References
- ./section-grammar.md — per-section rules, anti-examples, when to deviate.
- ./stack-pointers.md — where hero/meta wiring lives in Next, Astro, Nuxt, Vite SPA.
- ../set-up-seo/SKILL.md — crawlability, metadata, structured data for this page.
- ../set-up-lead-capture/SKILL.md — when the one action is a form.
- ../../frontend/optimize-performance/SKILL.md — app-side CWV work (the other side of the priority inversion).
