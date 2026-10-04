---
name: seo-landing
description: "Generates fast, SEO-optimized static HTML landing pages targeting 100/100 PageSpeed (LCP < 2.5s, INP < 100ms, CLS < 0.1), full schema.org JSON-LD, AVIF images, critical CSS, zero external dependencies. Use when: user asks to create/build/generate a landing page, one-pager, or static site with focus on SEO, speed, or PageSpeed; asks for an SEO-friendly page from a brief/ТЗ; or asks to audit/fix a landing against a performance checklist."
metadata:
  argument-hint: "[topic/domain or brief]"
---

# SEO Landing Generator

Builds a static single-page HTML landing optimized for 100/100 PageSpeed and maximum SEO: critical CSS, AVIF images, full JSON-LD structured data, native-only interactivity, zero third-party requests on first load.

## When to Use
- User asks for a landing page / one-pager focused on speed and SEO → **generate** mode.
- User provides a brief (ТЗ) and wants a production-ready static page → **generate** mode.
- User asks to audit an existing landing against the checklist without changes → **audit-only** mode (§0b, read-only, no project files).
- User asks to fix/improve an existing landing → **fix-existing** mode (§0c).

## Procedure

### 0. Route the request to a mode first
The skill serves three modes — pick one from the request (ask if ambiguous), because each mode collects different inputs and produces different output:

- **generate** — build a new landing page from a brief ("build/create/generate a landing…"). Runs the full procedure below.
- **audit-only** — read-only inspection of an existing page ("audit/check/review this landing against the checklist…", no changes requested). Runs §0b. Never writes project files.
- **fix-existing** — apply targeted fixes to an existing page ("fix/improve/optimize this page…"). Runs §0c.

Representative routing:
- "Build a landing for a dental clinic from this brief" → **generate**.
- "Audit https://example.com/ against the performance checklist and report what's wrong" → **audit-only**.
- "This landing's hero image shifts on load — fix it" → **fix-existing**.

Generation-only brief fields (target keywords, business type, CTA, media facts) are collected ONLY for generate and rebuild work. An audit or a targeted fix must not be blocked or delayed by missing generation inputs, and audit-only mode must not create or modify any project files.

### 0a. Collect the brief (generate mode; ask if missing)
Required before generating anything:
- Domain / final URL — for canonical, og:url, absolute paths, JSON-LD `@id`.
- Site identity (for `WebSite` markup, only when the page is the domain/subdomain home page): preferred site name, optional alternate names, and the canonical home URL — collected separately from the landing URL.
- Breadcrumb trail (for `BreadcrumbList` markup, only when a real site hierarchy exists): the visible breadcrumb trail and canonical parent URLs.
- Page language, base direction, and Open Graph locale — three separate inputs, never one value copied across formats: a BCP-47 language tag for `<html lang>` (e.g. `en-US`, `ar-SA`), the base direction (`ltr`/`rtl` — RTL documents get `dir="rtl"` on `<html>`, and `lang` alone does not set directionality), and the Open Graph locale in `language_TERRITORY` format for `og:locale` (e.g. `en_GB`). Ask when direction is unknown for an RTL-capable language (tech-spec §2).
- Topic + 1–3 target keywords — for H1, title, description.
- Business type: Organization or LocalBusiness. For LocalBusiness collect the verified public/legal business name and the complete structured postal address (street, locality, region, postal code, country), plus phone and geo coordinates. Also collect the verified schema.org subtype(s) based on the actual business (e.g. `Restaurant`, `Dentist`, `HardwareStore`) — never chosen from target keywords. Never invent missing identity facts: fall back to `Organization` markup or omit entity markup until the facts are provided.
- CTA and contacts (phone, form, messengers). When a form is requested, also collect its submission destination and method (a first-party endpoint or a documented form service — never invented), the consent/privacy text required for the collected personal data, and where submissions are stored and who owns them; with no destination, the form is omitted or explicitly stubbed (tech-spec §10 form submission contract).
- A brand-approved favicon or explicit permission to create one — never invent a brand mark silently.
- Approved source material and a claim owner for objective marketing facts (numbers, prices, qualifications, guarantees, comparisons, case studies) — without them such claims are omitted, never invented.
- Whether images are provided; whether FAQ / reviews / video blocks are needed. For a video block collect source-backed facts: video URL/ID, title, description, accurate first-publication date/time with timezone, and a unique crawlable thumbnail (plus `contentUrl` when applicable). Never invent missing media facts. Also collect the video mode with its trade-off stated: click-only facade (default — privacy/performance; the page will not satisfy Google's video discovery requirements and no video-search benefit is claimed) or SEO-discoverable (self-hosted `<video>` or a documented direct embed — required when video search traffic matters) (tech-spec §9).

If domain or keywords are missing — ask first, do not invent them.

### 0b. Audit-only mode (read-only)
Audit an existing page without generating a replacement. No project files are created or modified in this mode — the deliverable is a report.

1. Identify the target: a deployed URL (preferred — lets every check run against reality) or local HTML files. If neither is supplied, ask; never guess the target.
2. Run the applicable checks from §5 against the target as-is: W3C validity, local asset existence (for local files), JSON-LD via a schema.org validator, Lighthouse against the served/deployed URL, crawlability contract (robots.txt + sitemap.xml at the deployed host), and the manual accessibility checks in tech-spec §8.
3. Report evidence per check: pass/fail with the measured value or observed markup, and the exact command/tool used. Where a check cannot run (no deployed URL for Lighthouse, no robots.txt on the host), report a blocker for that check — do not estimate, extrapolate, or omit it silently.
4. Distinguish syntax validity from Google feature eligibility (FAQPage, VideoObject, rich results): valid markup is reported as valid markup, never as an achieved search feature.
5. Optionally end with a prioritized fix list. Applying fixes is a separate **fix-existing** request — do not start editing without it.

### 0c. Fix-existing mode
Apply targeted fixes to an existing page without a full rebuild.

1. Identify the page/files and the specific problems to fix; collect only the inputs those fixes need (never the full generation brief).
2. Apply each fix per the relevant tech-spec section, preserving unrelated markup and content.
3. STOP POINT (§4) applies: show the changed page before validation. If fixes change what the user approved earlier, obtain renewed approval before reporting.
4. Validate the changed page (§5) and report measured evidence only.

## Generation workflow (generate mode)

### 1. Create the project folder
Every project lives in its own folder inside the workspace — **never write to the workspace root**. The output is a multi-file project: every local resource referenced by the HTML must exist as a real file.

```
<workspace>/<project-slug>/
  index.html        # the generated landing page
  styles.css        # only when below-the-fold CSS is deferred (§1); absent when all CSS is inlined
  script.js         # only when the page uses JS (§10); single file, defer
  images/           # every image variant referenced in src/srcset/preload/OG tags (AVIF/WebP/JPEG, all breakpoints)
  favicon.png       # stable square brand icon, ≥48×48
  ASSETS.md         # rights & provenance record for every asset
  robots.txt
  sitemap.xml
  SERVER-SETUP.md   # hosting instructions
```

Image branch:
- Images provided in the brief → produce all required variants (AVIF/WebP/JPEG at every breakpoint named in `srcset`) from them.
- No images available → request them from the user or omit the image/block. Never emit a successful-looking asset URL without producing the file or explicitly asking for it — a referenced-but-missing file is a generation failure, not a placeholder.

### 2. Generate the page
Build `index.html` strictly following [references/tech-spec.md](./references/tech-spec.md) — 13 requirement sections (performance, HTML structure, SEO, security, CSS/fonts, forbidden list, testing, accessibility, embedded video, typical blocks, deferred widgets, content truthfulness & provenance, input sanitization & output encoding).

Treat every brief value as untrusted: encode it for its exact output context (HTML text, attribute, URL, JSON-LD), allow-list URL schemes (reject `javascript:`/unexpected `data:`), escape `<` in serialized JSON-LD, and validate structured IDs (e.g. YouTube `^[A-Za-z0-9_-]{11}$`) before they reach any URL (tech-spec §13).

For embedded YouTube video use the facade pattern by default; the SEO-discoverable mode (self-hosted `<video>` or a documented direct embed) is an explicit brief choice with a disclosed trade-off, never a silent switch — rules and the Google discovery requirements in tech-spec §9, facade reference implementation in [references/video-facade.md](./references/video-facade.md). Maps follow the facade rule only (tech-spec §10): a local screenshot in the initial DOM, the iframe inserted only on explicit activation — never a native `loading="lazy"` map iframe. Reference: [references/map-facade.md](./references/map-facade.md).

### 3. Generate companion files
- `robots.txt` at the site root with a fully qualified `Sitemap:` line, never blocking the canonical page or required media.
- `sitemap.xml` with XML-escaped absolute canonical `<loc>` URLs matching the HTML canonical; `lastmod` only from a verifiable significant-content-change timestamp (omit when unknown — never use generation time blindly).
- Hosting instructions from [references/server-config.md](./references/server-config.md): caching, Brotli/gzip, security headers.

### 4. STOP POINT — user approval
Show the generated page to the user and ask explicitly whether the HTML version is OK. **Do not proceed to validation and the final report until the user confirms.** If there are remarks — fix and ask again.

### 5. Validate
Run the executable validation contract from tech-spec §7 — pinned commands against the served page, measured results only, explicit BLOCKER when a gate cannot run:
- W3C HTML validity (Nu validator, JSON output; zero errors).
- Local asset/link existence: extract every local URL referenced by the output (img `src`/`srcset`, `<source>` `srcset`, preload `href`/`imagesrcset`, favicon, OG/Twitter images, CSS `url()`, script `src`) and verify each file exists in the project folder. Any missing referenced local resource is a hard failure — produce the file or remove the reference; never ship HTML pointing at files that were never created.
- JSON-LD syntax (JSON parse) — separate from Google rich-result eligibility, which is checked with Rich Results Test on the deployed page.
- Responsive screenshots at 320/768/1280/1920px, inspected for overflow and reflow.
- Lighthouse: pinned version/profile, 3 runs, median per category, threshold ≥ 90, artifacts kept in the project's `reports/` — lab evidence only, never field Core Web Vitals and never WCAG certification.
- Manual accessibility checks (tech-spec §8) — no automated tool alone determines WCAG conformance: keyboard navigation, focus order/visibility, dialog focus flow, zoom/reflow, reduced motion, semantic name-role-value, alternative-text quality, and all interactive visual states. Record pass/fail evidence per applicable WCAG 2.1 AA criterion; report unresolved items instead of silently certifying them.
- Crawlability contract: parse `sitemap.xml`, compare every `<loc>` with the HTML canonical, check the `Sitemap:` URL in `robots.txt`, and request both deployed files successfully (HTTP 200).

Fix any violations found before reporting. Disclose evidence honestly: every reported number comes with the exact command and artifact path that produced it; a gate that could not run is reported as `BLOCKER: <reason>` instead of a number. Never output a PageSpeed/LCP score that was not actually measured.

### 6. Final report
Briefly list:
- LCP parameters
- PageSpeed score
- schema.org types used in the code

## Main pitfalls
- Never use external JS/CSS libraries, external fonts, or SVG images (tech-spec §6).
- Never reference a local asset that was never created: every `src`/`srcset`/preload/OG URL must resolve to a real file in the project folder; missing source images are requested from the user, not invented (OUTPUT contract).
- Never emit a raw brief value into markup: context-encode everything, reject `javascript:`/unexpected `data:` URLs, and self-test generation with hostile values (quotes, `</script>`, event-handler payloads) (tech-spec §13).
- Never load YouTube iframes, maps, chats, subscription popups, or cookie banners on first load (tech-spec §9, §10, §11) — the single documented exception is a brief-chosen SEO-discoverable video mode with a direct embed recorded as a first-load dependency (tech-spec §9 Mode S).
- All content must exist in raw HTML — nothing rendered only by JS.
- Absolute URLs in JSON-LD, canonical, and OG tags.
- Total JS budget ≤ 15 KB, one file, `defer` before `</body>`.
