---
name: website-qa
description: >
  The pre-launch QA gate for a new site: run the basic tests (a11y light+dark +
  seo + navigation + anchors + orphans + images + tone + positioning + placeholders + email + links), fix to green, then handle technical SEO /
  performance — ask the user to run a
  Lighthouse / PageSpeed Insights test and act on First Contentful Paint (FCP)
  and Largest Contentful Paint (LCP). Use before launch (steps 7–8 of the
  new-website pipeline) and after any code/copy change. Delegates Core Web
  Vitals / crawl depth to seo-audit. Trigger phrases: "run the tests", "QA the
  site", "is the site launch ready", "a11y check", "accessibility test",
  "Lighthouse", "PageSpeed", "FCP", "LCP", "page speed", "Core Web Vitals",
  "performance check", "are the tests green".
---

# Website QA

The gate every page passes before launch, and the check re-run after any edit.
Two parts: the **automated basic tests**, then the **performance handoff**.

## 1. Basic tests (fix to green)

`npm test` runs the Playwright suite from the `new-website` skill's
`templates/astro/` overlay against a production build (`astro build && astro
preview` — the static output Cloudflare serves). Test the contract, not the
cosmetics; red → green → commit.

- `a11y.spec.ts` — axe WCAG 2 A/AA + best-practice on every page, **light AND
  dark**; zero violations.
- `seo.spec.ts` — title ≤60 / description 120–160 (hard floor AND cap); og/twitter
  mirror title/description; canonical == og:url == absolute URL; one `<h1>`; JSON-LD
  parses; the sitemap matches `PAGES` exactly (drift alarm: a route missing from
  `PAGES` fails here — the `website-seo-geo` contract).
- `navigation.spec.ts` — every `PAGES` route returns 200; internal links resolve
  with no redirect hop (absolute URLs on the production host count as internal).
- `anchors.spec.ts` — the other half of internal-link integrity: every in-site
  `#fragment` (same-page `#x`, cross-page `/page#x`, relative `about#x`, or `/?q#x`)
  points at a real element id on its target page — links and shipped-page target ids
  are read from the live DOM. Catches the dead-anchor bug navigation.spec can't see — a link
  that 200s but scrolls nowhere because the id doesn't exist. Offline.
- `orphans.spec.ts` — the inverse of navigation.spec: every `PAGES` route must be
  **reachable from the home page** by following internal links. A page can be in the
  sitemap and pass every other spec yet be linked from nowhere (orphaned — crawlers
  find it late, humans never do). Crawls the in-site link graph from `/` and fails
  listing any unreachable page. Deliberately-unlinked pages opt out via `ORPHAN_EXEMPT`.
  Offline. The judgment-side report (inbound count, thin pages, where to add links) is
  the `internal-link-audit` skill.
- `middleware.spec.ts` — `functions/_middleware.ts`, which `astro preview` never runs,
  called directly: previews noindexed, live-domain responses unchanged, and the project alias
  `<project>.pages.dev` 301ing to the live domain only once `CANONICAL_URL` is set. Offline.
- `analytics-server.spec.ts` — analytics server mode, the middleware and
  `functions/go/email.ts` called directly with a stand-in for Plausible: one page view per
  page a visitor opens and none for assets, prefetches, scripts or previews; an email tap
  counted and answered with the mailto: link; crawlers and links from other sites given the
  "[at]" hint, never the address. Offline.
- `images.spec.ts` — every `<img>` has `alt` + `width`/`height` + an explicit
  `loading` (`lazy`, or `eager` for the LCP image); raster sources are WebP/AVIF
  in src, srcset and `<picture>` (the `website-design-system` rules).
- `tone.spec.ts` — no em dashes / contractions / buzzwords in copy or metadata.
  Language-aware: the contraction/buzzword rules apply only to `<html lang>` en*
  pages; the em-dash ban is universal (the `website-content-guide` rules).
- `positioning.spec.ts` — each page in the `POSITIONING` map carries its positioning
  term (case-insensitive) in `<title>`, `<meta description>` and its `<h1>` or intro
  paragraph; declared `body` phrases (market category + core positioning phrase) appear
  in the body. Hermetic string containment, not a density check (the `website-positioning`
  spine). Empty map = green from commit 1. Also **warns (without failing)** when a `PAGES`
  route has no entry and isn't in `POSITIONING_EXEMPT` — an un-positioned content page is a
  lost opportunity, surfaced rather than silent. This is a mechanical string check, not a
  judgment read — for "does the offer actually read clearly", see `website-positioning-check`.
- `placeholders.spec.ts` — leftovers a visitor could read. Reads each page's rendered
  copy, `<head>` metadata, alt texts, aria-labels and JSON-LD, plus the web manifest,
  for an unfilled `[SLOT]` (the `"[MISSING: …]"` content token and the starter's
  `[BRACKET]` slots alike), filler text, an author note (`TODO`), an unrendered
  template expression or a dummy name. The CI grep for `[MISSING:` is the fast
  source-side half; this is the half that reads what a page serves. The starter's
  privacy page, imprint and manifest sit in `UNFILLED_UNTIL_LAUNCH` and are
  **reported, not failed**, until filled; a filled target fails until its entry is
  deleted, so the list empties itself and must be empty at launch (`new-website` §4).
  A `"[MISSING: …]"` on a page only warns on your own machine, so a draft branch can
  be pushed, and fails in CI. Not read: the 404 page, `llms.txt`, and the starter's
  example values (the name `Example`, `hello@example.com`); those stay a
  launch-checklist item.
- `privacy-host.spec.ts` — the host the privacy page tells visitors to block (the text
  marked `data-analytics-host`) is the host in `ANALYTICS.scriptHost`. A `[BRACKET]` slot
  there passes (`placeholders.spec.ts` reports it), and so does a page without the mark.
- `email.spec.ts` — no plaintext (harvestable) email address in the served HTML
  (addresses go through `<EmailLink>`, which obfuscates; the `website-design-system` rule).
- `links.spec.ts` — offline outgoing-link guard: no `STALE_DOMAINS` (domains you've
  retired) reappear in an anchor href. Hermetic — makes no network calls. The
  *liveness* of the links you keep is the network-dependent `outgoing-link-audit`
  skill (pre-launch / monthly, **not** in CI).

First fill `tests/_helpers.ts` `PAGES` with the real routes. A failure is a real
defect — fix the page, do not loosen the test (Rule 12: never silently skip). For
diagnosing a specific failure, `test-failure-triage`; for intermittent ones,
`flaky-test-debugger`.

## 1b. TDD — what NEW tests to write for a feature

The specs in §1 are the always-on baseline. When you add a *feature*, write its test
**first** (red → green → commit): state what "correct" means before building it, then
implement until green. Test the **contract/behaviour, not the cosmetics** (assert "the form
shows a success state", not "the heading is 32px") — a test that can't fail when the logic
breaks is worthless (Rule 9).

When a new route is added, the only change needed for the baseline to cover it is adding its
path to `tests/_helpers.ts` `PAGES` — a11y, SEO, navigation and image checks then
apply automatically.

Feature → the high-value test to add:
| Feature | Write a test that… |
|---|---|
| New page/route | add it to `PAGES`; baseline a11y+SEO+links now assert it (returns 200, one `<h1>`, title/desc in range). Then **link it from a related page** — `orphans.spec.ts` fails if it's reachable from no internal link. |
| Contact / lead form | valid input → success state; invalid → error; the endpoint/`mailto` is invoked. The mail-app contact form: install `website-contact-form`, whose `tests/mail-form.spec.ts` covers exactly this (set its `PAGE` and `TO`). The skill is bundled with a site only when it was scaffolded with a form; otherwise it comes from the toolkit the site was built with. |
| Theme toggle / dark mode | toggling persists across reload; run a11y in **both** themes (`THEMES=['light','dark']`). A toggle that stores the choice is storage the privacy page must disclose (section 3). |
| Site search | a known query returns the expected result; empty query handled. |
| Redirects (`_redirects`) | each legacy URL 301s to the new clean URL. |
| Images / new media | every `<img>` has `alt` + `width`/`height`; raster sources are WebP/AVIF; LCP image not lazy (see `website-design-system`). |
| Nav / CTA change | the expected links render and resolve; the CTA lands on the right page. |
| Copy/brand rules | extend the tone rules in `tests/_helpers.ts` to ban the new off-brand phrasing (`tone.spec.ts` holds the pages to them). |
| New/changed positioning | add the page's term to the `POSITIONING` map in `positioning.spec.ts`; the page must carry it in `<title>`/`<meta description>`/`<h1>` (see `website-positioning`). |
| Public scorecard (`website-scorecard`) | install the skill by its §2 (three files and the package script; the spec needs the script, so never copy it alone), then set `PAGE` in `tests/scorecard.spec.ts`: the page must show the numbers in `scorecard.json`, and the file must add up. |
| Colours or a logo from `website-brand-kit` | nothing to copy: its intake runs this suite itself after it writes, and puts every file back if the suite goes red. After a run with a logo, the seven icon files the pages and the manifest link exist under `public/` (`favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `images/logo.png`). |
| Story-led home page (`website-story`) | copy that skill's `templates/story.spec.ts` into `tests/` and fill its `CONFIG` from the values listed at the end of `STORY.md` (the rest have defaults); `positioning.spec.ts` stays untouched. |
| Tagline under the logo (`website-tagline`) | copy that skill's `templates/tagline.spec.ts` into `tests/` and set `CONFIG.selector` to the element that shows the line: the page must show `SITE.tagline` word for word, in a `<p>`, no other file under `src/` may hold the line, and the line must keep to that skill's limits (eight words, 50 characters). |
| Exposed email/phone | it's rendered via `EmailLink` — assert the built HTML has **no plaintext `mailto:` or literal `@`-address** (crawler/spam protection; see `website-design-system`). |

Keep it thin: a marketing site needs a high-value harness, not 1000 unit tests. Don't test a
cosmetic you'll change next week; do pin every contract a third party could silently break.

## 1c. Enforce the gate on push (the pre-push hook)

The baseline only protects the site if it actually runs before a deploy. The scaffold ships
a **`pre-push` git hook** (`scripts/hooks/pre-push`) that runs `scripts/verify.mjs` (the same
as `npm run verify`: `npm ci` only on its first run or when `package.json` or `package-lock.json` changed, `npm run check`, then
`npm test`, which builds once; short output) and `check_seo.py` (if present), and **refuses the
push if anything is red** — so a broken build never reaches the deploy branch. A site without
`scripts/verify.mjs` gets the older `npm run build` + `npm test`. It's wired automatically: the `prepare` script in
`package.json` (`node scripts/wire-hooks.mjs`, a line with no shell syntax) points
`core.hooksPath` at `scripts/hooks` on `npm install` — when the site is the root of its git
repo. In a subfolder of a bigger repo it leaves that repo's hooks alone, so the gate is not
wired there; say so rather than assume it runs.

This is the local complement to CI: Cloudflare Pages builds on push **independently of CI**,
so without this hook a red test would still deploy. The hook is what makes "fails → does not
ship" literally true on a direct-push-to-`main` workflow, without forcing a slower PR flow.

**Offer it as a choice — never silently impose or remove it (Rule 1/Rule 12).** When setting
up or handing off a site, surface both directions:
- **Relax for one push:** `git push --no-verify` (skips the hook for that push only).
- **Disable entirely:** `git config --unset core.hooksPath` (re-enable with
  `npm install`, or `git config core.hooksPath scripts/hooks`).
- **Tune what it runs:** edit `scripts/hooks/pre-push` (e.g. leave out a slow step; CI still
  runs everything).

A team that wants the speed of direct pushes and the safety of the gate keeps it on; a solo
builder mid-experiment may want it off. Make the call explicit with the user; don't decide for
them. (Requires the per-machine `npx playwright install chromium` from SETUP.md, or the test
step errors — a fail-loud, fixable by setup, not a reason to drop the hook.)

## 2. Performance — Lighthouse / PageSpeed (FCP & LCP)

Performance numbers need a real run; this is a **handoff to the user** (the agent
cannot run Lighthouse against a deployed URL reliably). Ask the user to run one:

> Please run a **PageSpeed Insights** test ( https://pagespeed.web.dev/ ) on the
> page URL — or Chrome DevTools → Lighthouse — and paste the **First Contentful
> Paint (FCP)** and **Largest Contentful Paint (LCP)** for mobile and desktop.

Targets (Core Web Vitals "good"): **FCP ≤ 1.8s**, **LCP ≤ 2.5s** (mobile, field
data preferred). Then act on what the report flags. Common fixes already baked
into the starters / `website-design-system`:
- LCP image: eager-load + `fetchpriority="high"`, correct format/size, no lazy.
- Render-blocking CSS: Astro inlines it (`inlineStylesheets: 'always'`).
- Fonts: self-hosted woff2, `font-display: swap`, preload only above-the-fold.
- Layout shift (CLS): explicit `width`/`height` on media.
- Defer non-critical JS (analytics is `async` plus a short inline stub, production-only; none
  in analytics server mode).

For deeper technical SEO (crawl, indexability, Core Web Vitals strategy), run the
existing **`seo-audit`** skill — do not duplicate it here.

## Done means

All basic tests green; FCP/LCP within target on the user's PageSpeed run (or the
remaining gaps explicitly listed, not hidden); launch checklist in `new-website`
§4 satisfied.
