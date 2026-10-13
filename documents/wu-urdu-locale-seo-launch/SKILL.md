---
name: wu-urdu-locale-seo-launch
description: Implement WU-I18N-001B and WU-I18N-001C after locale foundation is green. Own Urdu metadata, reciprocal hreflang, canonicals, sitemap generation, structured data language, natural Urdu Phase 1 copy, RTL/accessibility QA, production smoke, and privacy-safe search/revenue measurement.
---

# WU-I18N-001B/C implementation skill

Read:

1. `specs/WU-I18N-001B-urdu-seo-hreflang-sitemaps.md`
2. `specs/WU-I18N-001C-phase1-urdu-content-qa-measurement.md`
3. parent `specs/WU-I18N-001-crawlable-urdu-locale.md`
4. `specs/WU-GROWTH-001-search-adsense-growth-system.md`
5. `seo.config.js`
6. locale registry/catalogue created by Slice A
7. `scripts/generate-seo-files.js`
8. `scripts/check-seo.js`
9. `scripts/sync-static-search-metadata.js`
10. `docs/WU-PUBLIC-PAGE-REGISTRY.csv`

Do not use this skill until Slice A route/asset/generation gates are green.

## Mission

Turn the generated Urdu pages into correct search documents and credible Urdu product experiences.

The release unit is eight Phase 1 routes, not the full site.

## SEO invariants

For each pair:

```text
English canonical = English URL
Urdu canonical    = Urdu URL
hreflang en       = English URL
hreflang ur       = Urdu URL
x-default         = English URL
```

All alternates are reciprocal in initial source HTML.

Never canonicalize Urdu back to English.

## Metadata workflow

For each Phase 1 route:

1. inspect current English search owner and intent;
2. write natural Urdu title;
3. write concise Urdu description;
4. write/confirm Urdu H1 and lede;
5. record metadata in the shared locale registry;
6. regenerate HTML;
7. validate source, not only hydrated DOM.

Do not mechanically translate the English title word-for-word.

Do not introduce new keyword ownership that conflicts with established English pages.

## Natural Urdu rule

Primary UI/search copy should describe the task simply.

Prefer:

```text
انگریزی حروف میں اردو لکھیں
آن لائن اردو لکھیں
اردو کی بورڈ
بولیں اور اردو میں لکھیں
تصویر پر اردو لکھیں
```

Avoid technical jargon as headline copy when a normal phrase exists.

Do not keyword-stuff the Urdu query watchlist.

## Sitemap rule

Generate locale sitemap data from registries.

Never manually add `/urdu/` URLs to XML without generator coverage.

Expected Phase 1 Urdu indexable set: eight URLs.

No account, feedback, search, public UGC share or other noindex utility route enters the Urdu sitemap.

## Schema rule

Keep the underlying schema type.

For Urdu versions ensure:

- canonical URL is Urdu;
- human-readable name/headline/description matches visible Urdu page;
- `inLanguage: ur` where valid;
- FAQ schema contains only questions/answers visible on that Urdu page;
- publisher identity stays the same Write Urdu entity.

## English protection rule

Do not rewrite proven English search metadata while implementing Urdu alternates.

The homepage English title/description experiment is protected.

English pages may gain reciprocal hreflang only.

## Content completeness workflow

For each of the eight pages create a route checklist covering:

```text
metadata
H1/lede
primary CTA/actions
help/instructions
error/loading/empty states
navigation/footer
next steps
aria labels
mixed-language fragments
```

Do not mark a route complete if only metadata/hero is Urdu and the primary task remains critically English-only.

## RTL QA rule

Test desktop + Pixel 5/mobile.

Fix layout with logical CSS where practical rather than creating a large `.locale-urdu` override layer.

Check:

- action order;
- icon spacing;
- menus/dropdowns;
- tables;
- cards;
- form labels;
- modals/toasts;
- focus order;
- mixed English tokens like PDF/QR/WhatsApp;
- ad boundaries.

## Product behavior rule

Localization cannot change functional contracts.

Retest:

- homepage typing/transliteration wiring;
- Keyboard direct input;
- Editor controls/export entry points;
- Voice support/permission/error flow;
- Alphabet → Keyboard journey;
- Photo Guide → Card Studio journey;
- locale counterpart switching.

Never translate user text/template content.

## AdSense rule

Use normalized product path/page type.

Urdu locale does not receive extra ad units.

Verify:

```text
Write pages -> workspace protection preserved
Learn pages -> existing Learn placement rules
Create pages -> Create protected areas preserved
```

## Measurement rule

Reuse existing telemetry and `WU-GROWTH-001`.

If locale is added to events, use bounded enum only:

```text
en
ur
```

Never send typed Urdu, transcript, draft or filename content.

After production, record the manual Search Console tasks still needed.

Do not fabricate indexing/revenue results in implementation notes.

## Tests to add/extend

### SEO static tests

Validate:

- exact self canonical;
- `en`, `ur`, `x-default` links;
- reciprocity;
- `lang=ur dir=rtl`;
- localized title/description/H1;
- OG URL/title/description;
- schema URL/language;
- sitemap membership;
- no accidental noindex;
- English owner unchanged.

### Browser tests

Representative flows:

```text
/urdu/ -> writer works
/urdu/urdu-keyboard -> keyboard action works
/urdu/tools/urdu-voice-typing -> status/error UI is Urdu
/urdu/urdu-alphabet -> /urdu/urdu-keyboard
/urdu/how-to-write-urdu-on-photo -> /urdu/urdu-card-studio
Urdu page -> exact English counterpart
```

## Release verification

Run:

```text
npm run locale:generate
npm run locale:check
npm run seo:generate
npm run seo:check
npm run governance:check
npm test
npm run test:browser
```

Then perform/record production checks for all eight routes.

## Search launch tasks to report, not fake

Once deployed:

- submit/refresh sitemap(s);
- URL Inspect `/urdu/` and representative nested pages;
- verify Google-selected canonical;
- request indexing for the Phase 1 set in a measured way;
- monitor Search Console filtered by `/urdu/`;
- capture emerging Urdu-script queries;
- compare English owner performance for cannibalization/regression;
- capture AdSense/page-group contribution when enough data exists.

These are external/manual observations. Code completion does not imply Google indexing.

## Stop conditions

Do not expand beyond Phase 1 if:

- English/Urdu canonical pairs are wrong;
- hreflang reciprocity fails;
- generated body copy is substantially English;
- Urdu route breaks a primary action;
- route prefix causes product or ad classification errors;
- English ranking-owner metadata is being rewritten without evidence;
- implementation proposes thin Urdu pages merely to increase URL count.

## Completion

Update spec checklists only with actual evidence.

Mark Phase 1 complete only after production smoke plus technical search launch gates are done. Leave full-corpus Phase 2 as follow-up until explicitly started.