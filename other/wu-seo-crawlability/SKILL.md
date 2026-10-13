---
name: wu-seo-crawlability
description: Implement or review WU-SEO-CRAWL-001 one slice at a time. Covers public-language cleanup, static internal-link shell, static SEO/schema generation and crawlable collection content while preserving mature-domain URLs and current query ownership.
---

# WriteUrdu SEO Crawlability — implementation skill

Use this skill for implementation/review work under `WU-SEO-CRAWL-001`.

## 1. Mandatory read order

Always read current `main`, then:

1. `specs/WU-SEO-CRAWL-001-public-copy-static-crawlability.md`
2. `specs/BACKLOG.md`
3. `specs/README.md`
4. `seo.config.js`
5. `js/seo.js`
6. `js/v2-shell.js`
7. `js/site-header-core.js`
8. `scripts/generate-seo-files.js`
9. `scripts/generate-urdu-locale.js`
10. relevant current SEO/static regression tests

Then read the exact slice:

```text
CRAWL-A → specs/WU-SEO-CRAWL-001A-public-language-cleanup.md
CRAWL-B → specs/WU-SEO-CRAWL-001B-static-internal-link-shell.md
CRAWL-C → specs/WU-SEO-CRAWL-001C-static-seo-graph.md
CRAWL-D → specs/WU-SEO-CRAWL-001D-static-collection-content.md
```

Do not implement later slices opportunistically while working on an earlier one unless a tiny compatibility change is unavoidable and explicitly documented.

## 2. Core invariants

### Preserve mature-domain ownership

Do not change without explicit evidence/approval:

- canonical URLs;
- homepage English-to-Urdu typing H1/title/search description;
- `/urdu-keyboard` direct-keyboard ownership;
- `/roman-urdu-transliteration` specialist guide ownership;
- Card Studio/photo-guide ownership;
- current hreflang relationships;
- Search/Feedback `noindex,follow` behavior.

### Static-first does not mean JavaScript-free

Keep JavaScript for:

- editors;
- canvas/rendering;
- local state;
- filtering/sorting;
- favorites/recents;
- runtime locale switching;
- interactive menus;
- personalized user output.

Move only crawl-critical public information to source/build HTML.

### Product language, not architecture language

Do not expose:

- SEO keyword/page strategy;
- internal route-consolidation rationale;
- telemetry/data-model vocabulary;
- internal config/version IDs;
- CDN/runtime/vendor mechanics unless disclosure is materially required;
- implementation boundaries such as whether one workspace embeds another.

Do not mechanically remove legitimate user-domain terms such as `Unicode`, `InPage`, `Nastaliq`, `Naskh`, `OCR`, `PDF`, `QR`.

## 3. Slice A workflow

1. Fetch all affected current files from `main`.
2. Identify exact strings from the parent audit before editing.
3. Rewrite only the smallest public-copy spans necessary.
4. Keep title/meta/canonical/H1 unchanged unless the slice explicitly says otherwise.
5. Add a narrow regression test for leaked phrases/internal identifiers.
6. Run SEO + static tests.
7. Review diff for accidental privacy/legal meaning loss.

Do not make a broad style rewrite of every page.

## 4. Slice B workflow

1. Inventory existing source-visible navigation/footer markup by page family.
2. Identify the current canonical navigation/link registry owner.
3. Choose build/source generation over per-page hand duplication where practical.
4. Emit meaningful semantic links in initial HTML.
5. Make `v2-shell.js` enhance existing markup rather than being the sole source of links.
6. Test with raw source parsing and browser runtime.
7. Verify Urdu locale routing and visual behavior.

## 5. Slice C workflow

1. Treat `seo.config.js` as the route/schema declaration source.
2. Reuse/generalize the existing Urdu static generation pattern.
3. Create one shared schema construction path where feasible.
4. Emit schema into source/build HTML.
5. Keep runtime locale/meta restoration behavior that is still necessary.
6. Prevent duplicate schema after JS execution.
7. Validate source JSON parsing and representative schema types.

FAQ schema moves as part of this slice; do not create separate FAQ-rich-result work.

## 6. Slice D workflow

1. Identify the real catalogue data source for each collection.
2. Generate semantic static catalogue HTML from that same source.
3. Progressively enhance the generated items.
4. Never serialize local/user-entered text into build artifacts.
5. Do not ship a hidden static duplicate plus a second dynamic catalogue.
6. Keep HTML bounded and useful.
7. Verify source item presence and runtime interactions.

## 7. Test expectations

Every slice should add focused source-level tests. Browser-rendered tests alone are insufficient for this epic.

Key categories:

```text
source metadata
source links
source schema
source catalogue content
no duplicate runtime schema/navigation
canonical/hreflang invariants
noindex utility invariants
locale regressions
interactive behavior regressions
```

Run the repository's current full/focused test commands rather than assuming filenames in the spec are complete.

## 8. Diff review checklist

Before proposing a PR:

- no canonical URL changed;
- no redirect changed unless explicitly required;
- no homepage query-owner metadata changed;
- no legal/privacy statement weakened accidentally;
- no user text added to telemetry/schema/build artifacts;
- no duplicate nav/footer/schema/catalogue after runtime;
- no Urdu locale regression;
- no new thin SEO pages;
- no new ad placement/density.

## 9. PR discipline

One slice per PR after the parent epic is merged.

Preferred titles:

```text
WU-SEO-CRAWL-001A: clean public product language
WU-SEO-CRAWL-001B: make internal links static-first
WU-SEO-CRAWL-001C: pre-render SEO structured data
WU-SEO-CRAWL-001D: pre-render collection content
```

In each PR body state:

- exact routes/files changed;
- what remains intentionally runtime-driven;
- search/canonical invariants checked;
- tests run;
- any production source-view follow-up still required.