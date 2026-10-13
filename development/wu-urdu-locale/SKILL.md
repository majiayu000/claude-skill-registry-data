---
name: wu-urdu-locale
description: Orchestrate the WriteUrdu crawlable Urdu locale initiative. Build /urdu/ as a language-prefixed static locale from the existing product, preserve English canonical owners, reuse one codebase, and execute WU-I18N-001 slices in order. Never use /pk/, geo redirects, duplicate product logic, or JS-only SEO localization.
---

# WriteUrdu crawlable Urdu locale orchestrator

Use this skill for any implementation, review or continuation request related to `/urdu/` localization.

## Read first

1. `specs/WU-I18N-001-crawlable-urdu-locale.md`
2. `specs/WU-I18N-001A-locale-routing-static-generation.md`
3. `specs/WU-I18N-001B-urdu-seo-hreflang-sitemaps.md`
4. `specs/WU-I18N-001C-phase1-urdu-content-qa-measurement.md`
5. `specs/WU-GROWTH-001-search-adsense-growth-system.md`
6. `seo.config.js`
7. `docs/WU-PUBLIC-PAGE-REGISTRY.csv`
8. `js/site-header-core.js`
9. `js/content-locale.js`
10. `site-header.js`

## Core decision

The locale model is:

```text
English/default: /
Urdu:            /urdu/
```

Use language code `ur` for the general Urdu locale.

Do not implement `/pk/` as a substitute. Do not auto-redirect by IP/browser/country.

## Architecture invariants

### One product

There is one WriteUrdu product implementation.

Urdu pages reuse:

- the same editor logic;
- the same keyboard logic;
- the same Card Studio logic;
- the same exports;
- the same account/document APIs;
- the same telemetry contracts;
- the same AdSense page-type rules.

Do not fork product JS for Urdu.

### Static-first crawlability

Urdu search pages must return meaningful Urdu in initial HTML.

A language toggle that changes the DOM after load is not sufficient for this initiative.

Preferred implementation:

```text
source HTML + locale catalogue + generator -> checked-in /urdu/*.html
```

Do not introduce a framework or always-on Worker merely for normal locale rendering.

### URL owns language

```text
/urdu/... => ur
anything else => en
```

Do not let `localStorage` override the language of the current canonical URL after load.

### English owners are protected

Do not move or redirect established English canonical routes.

The only normal English-page SEO change required by localization is reciprocal alternate/hreflang metadata and locale discovery links.

## Slice routing

### Slice A — foundation

Use `.claude/skills/wu-urdu-locale-build/SKILL.md`.

Scope:

- locale route registry/helper;
- normalized product paths;
- asset/path safety;
- PWA/service-worker safety;
- deterministic Urdu generation;
- language counterpart navigation;
- local dev/test resolution.

Do not implement broad content or sitemap launch before Slice A gates are green.

### Slice B/C — SEO + launch

Use `.claude/skills/wu-urdu-locale-seo-launch/SKILL.md`.

Scope:

- localized metadata;
- self canonicals;
- reciprocal hreflang;
- sitemap generation;
- structured data language/URL;
- eight-page Urdu content review;
- RTL/accessibility QA;
- Search Console/revenue measurement contract.

## Phase 1 corpus

Exactly these eight indexable Urdu routes are the first launch corpus unless the owning spec is updated:

```text
/urdu/
/urdu/urdu-keyboard
/urdu/urdu-editor
/urdu/tools/urdu-voice-typing
/urdu/urdu-alphabet
/urdu/urdu-faq
/urdu/urdu-card-studio
/urdu/how-to-write-urdu-on-photo
```

Do not bulk-enable every `seo.config.js` route in the first implementation slice.

## Route-normalization rule

Never add locale duplication such as:

```js
path === '/urdu-editor' || path === '/urdu/urdu-editor'
```

Introduce/use the shared helper so feature modules compare normalized product paths.

Locale prefix belongs to routing, not product identity.

## Asset rule

Audit all relative local assets before considering `/urdu/` safe.

Particularly reject accidental requests to:

```text
/urdu/js/*
/urdu/css/*
/urdu/image/*
/urdu/sw.js
/urdu/manifest.webmanifest
```

unless such a locale-specific resource was explicitly designed.

Shared resources should normally be root-absolute.

## Translation rule

Prefer natural task language over technical literal translation.

Good examples:

```text
انگریزی حروف میں اردو لکھیں
آن لائن اردو لکھیں
اردو کی بورڈ
بولیں اور اردو میں لکھیں
تصویر پر اردو لکھیں
```

Do not optimize visible copy around the words `transliteration` or `Roman` when normal users can understand a simpler task description.

Never translate user-authored content.

## SEO rule

For every launched pair:

```text
English canonical -> English
Urdu canonical    -> Urdu
hreflang en       -> English
hreflang ur       -> Urdu
x-default         -> English/default
```

Pairs must be reciprocal in initial HTML.

Urdu canonical must never point to English.

## AdSense rule

Locale inherits the page type.

Do not create new ad density or placements solely because an Urdu route exists.

Respect `WU-GROWTH-001` and existing protected workspaces.

## Database rule

This initiative needs no new database.

Do not create D1/KV/R2 state for static localization.

## Execution discipline

Before editing:

1. identify the exact slice;
2. inspect current route/path behavior;
3. inspect existing localization strings relevant to that slice;
4. identify affected tests;
5. preserve unrelated active feature work.

During implementation:

- make the smallest architecture-complete change;
- avoid page-by-page hacks;
- use registry-driven behavior;
- keep generator output deterministic;
- never edit generated Urdu files as the primary source.

After implementation:

- regenerate derived locale/SEO artifacts;
- run focused tests first;
- run the full required suite;
- inspect generated HTML directly, not only the hydrated browser DOM;
- document any production/Search Console steps still required.

## Required verification

Baseline:

```text
npm run locale:generate
npm run locale:check
npm run seo:generate
npm run seo:check
npm run governance:check
npm test
npm run test:browser
```

If commands do not exist yet, Slice A owns adding them.

## Stop conditions

Stop and report rather than invent behavior if:

- the locale generator would require duplicating live editor implementation;
- the proposed URL would canonicalize back to English;
- a Phase 1 Urdu page has only metadata translated while body content remains substantially English;
- service worker/asset behavior under the locale prefix is unresolved;
- tests would be weakened to allow incorrect canonical/hreflang output;
- implementation requires a new backend without a separate approved reason.

## Completion behavior

A slice is complete only when its owning acceptance checklist is satisfied.

Do not mark the whole `WU-I18N-001` implemented after Slice A or B. Phase 1 closes only after Slice C production/search launch gates are complete. Phase 2 full-corpus expansion remains follow-up work.