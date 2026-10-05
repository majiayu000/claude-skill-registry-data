---
name: interactive-page-repost-publisher
description: >-
  Ingest JS-heavy external pages into StaticFlow as standalone local
  interactive mirrors backed by LanceDB assets, with bilingual article
  write-back and localized interactive locales.
---

# Interactive Page Repost Publisher

Use this skill when the source page is not a normal Markdown/article import:
- custom elements, canvas/SVG demos, sliders, inline scripts
- page-local JS bundle is required to understand the content
- the user wants both article searchability and preserved interaction
- the interactive page itself must support Chinese/English switching

## Companion Skills
- Required: `../staticflow-cli-publisher/SKILL.md`
- Required for article translation and summary quality: `../article-bilingual-translation-publisher/SKILL.md`
- Optional for mixed-source normalization: `../external-blog-repost-publisher/SKILL.md`

## Non-Negotiable Rules

### Rule 1: Interactive view is a standalone local page
- Do not forward the user to the origin URL.
- Do not rely on remote JS/CSS/image assets at runtime.
- Serve the mirror from StaticFlow backend route:
  - `/interactive-pages/<page_id>?lang=zh`
  - `/interactive-pages/<page_id>?lang=en`

### Rule 2: Do not inject the interactive page into normal article HTML
- The article page is for search, SEO, summary, and the “open interactive” CTA.
- The interactive experience lives in its own HTML page.
- Avoid trying to run source page scripts inside the normal SPA article body.

### Rule 3: All mirror assets go into LanceDB
- Mirror assets belong in:
  - `interactive_pages`
  - `interactive_assets`
  - `interactive_page_locales`
- Do not keep the production mirror only on disk.

### Rule 4: Publish in two tracks
- Track A: `articles`
  - Chinese translated body in `content`
  - normalized English source body in `content_en`
  - bilingual `detailed_summary.zh/en`
- Track B: interactive mirror
  - base locale from the captured source page
  - localized locale variants via `interactive add-locale`

### Rule 5: Localized interaction is part of the deliverable
- It is not enough to translate only the article body.
- The interactive UI itself must have localized assets if the user asks for Chinese/English switching.
- After adding a non-source locale, `interactive_pages.translation_scope` should become `article_and_interactive`.

### Rule 6: Localized interactive pages must preserve source fidelity
- Localized pages should remain as close to the source DOM structure as practical.
- Do not flatten or regenerate source code blocks if that would drop syntax-highlighting classes or visual styling hooks.
- Preserve original visual behavior, code highlighting, component structure, and interaction wiring unless a change is required for localization.
- Translation quality target is a faithful full-text translation, not a shortened rewrite.

### Rule 7: Raw localized entries must remain single-locale
- `/interactive-pages/<page_id>/entry?lang=zh` must read as a Chinese-first page and must not embed a full English article body.
- `/interactive-pages/<page_id>/entry?lang=en` must read as an English-first page and must not embed a full Chinese article body.
- Do not stack two full-language article bodies inside one raw entry.
- Do not treat “English source page + appended Chinese translation block” as acceptable localization.

### Rule 8: Bilingual comparison belongs to the article track
- Bilingual comparison is allowed in `articles.content` / `articles.content_en` or article detail UI.
- Raw interactive entries must not implement bilingual comparison by appending a second full-language article below the first.
- `/interactive-pages/<page_id>/entry?lang=<locale>` is a localized mirror, not a side-by-side bilingual view.

### Rule 9: Translation source must be clean
- If the currently published LanceDB article body is malformed, do not reuse it as translation source material.
- Rebuild bilingual article artifacts from source HTML, clean source Markdown, or another verified clean extraction.
- Existing broken reposts require a rebuild from clean source, not patch stacking on top of corrupted Markdown.

### Rule 10: Provide direct access to the raw localized entry page
- The standalone wrapper is useful, but it is not the only entry.
- The user should be able to open the current-language raw render directly:
  - `/interactive-pages/<page_id>/entry?lang=zh`
  - `/interactive-pages/<page_id>/entry?lang=en`
- If a wrapper shell exists, include a visible CTA that opens the current-language raw render.

### Rule 11: Verify routes, DB rows, and real interaction after write
- Query the DB rows after publish.
- Open the local mirror route and confirm it renders.
- Verify core interaction still works after localization.
- Verify localized copy on real rendered frames, not only the landing screen.

### Rule 12: Article date should default to the import date
- Unless the user explicitly asks to preserve the source publication date in `articles.date`, use the actual import date.
- If the source article has its own original publication date, mention it in the article body or attribution instead of reusing it as the StaticFlow article date by default.

### Rule 13: Do not capture the executed DOM as the entry HTML
- For JS-heavy pages, the entry HTML should come from the original fetched response HTML whenever practical.
- Do not serialize `document.documentElement.outerHTML` after the page has already executed and mutated the DOM unless the task specifically requires a post-init snapshot.
- Otherwise replay can duplicate runtime-generated nodes, causing overlapping titles, SVGs, or other animated content on reload.

## Default DB
- Unless the user says otherwise, use:
  - `/mnt/wsl/data4tb/static-flow-data/lancedb`

## Naming and Storage Conventions
- `articles.id`: stable article id, e.g. `bloom-filters`
- `interactive_pages.id`: `ipg-<article_id>`, e.g. `ipg-bloom-filters`
- localized interactive assets should usually live under:
  - `localized/zh/...`
  - `localized/en/...`

## Workflow

### Step 1: Confirm this page needs the interactive pipeline
Use this skill instead of normal repost when:
- the page depends on page-specific JS to make sense
- the page uses custom elements or heavy DOM initialization
- screenshots or plain Markdown would lose the core teaching value

### Step 2: Prepare bilingual article artifacts
Create under `/tmp/interactive_repost/<article_id>/`:
- `content_zh.md`
- `content_en.md`
- `summary_zh.md`
- `summary_en.md`

Requirements:
- `content_en` must be a normalized English source article, not a recap
- `content` must be a polished Chinese translation
- both should include attribution and source URL

### Step 3: Capture and ingest the base interactive mirror
Use `sf-cli interactive ingest-page`.

Canonical command:

```bash
cargo run -q -p sf-cli -- interactive \
  --db-path /mnt/wsl/data4tb/static-flow-data/lancedb \
  ingest-page \
  --url "<source_url>" \
  --article-id "<article_id>" \
  --file /tmp/interactive_repost/<article_id>/content_zh.md \
  --summary "<short_summary>" \
  --tags "tag-a,tag-b" \
  --category "<category>" \
  --category-description "<category_description>" \
  --content-en-file /tmp/interactive_repost/<article_id>/content_en.md \
  --summary-zh-file /tmp/interactive_repost/<article_id>/summary_zh.md \
  --summary-en-file /tmp/interactive_repost/<article_id>/summary_en.md \
  --author ackingliu \
  --allow-host "<expected_host>"
```

Notes:
- `--capture-script` defaults to `scripts/capture_interactive_page.mjs`
- `--capture-manifest` can be used to skip a fresh Playwright capture
- Prefer passing `--date <import-date>` explicitly so the stored article date matches the ingest date.
- base ingest creates:
  - `articles.article_kind = interactive_repost`
  - `articles.source_url`
  - `articles.interactive_page_id = ipg-<article_id>`
  - `interactive_pages`
  - `interactive_assets`

Capture guidance:
- Rewrite asset URLs against the source response HTML, then store that rewritten source HTML as the entry page.
- Remove or neutralize source `<base>` tags when mirroring so local asset routing stays stable.
- If runtime URL patching is used, make it skip already-local `/api/interactive-pages/...` asset paths to avoid double rewrite and 404s.

### Step 4: Build localized interactive assets
If the user needs Chinese/English switching inside the interactive page:
1. create localized HTML/JS/CSS assets
2. generate a capture-manifest style JSON for that locale
3. add the locale with `sf-cli interactive add-locale`

Canonical command:

```bash
cargo run -q -p sf-cli -- interactive \
  --db-path /mnt/wsl/data4tb/static-flow-data/lancedb \
  add-locale \
  --page-id "ipg-<article_id>" \
  --locale zh \
  --title "<localized_title>" \
  --manifest /tmp/interactive_repost/<article_id>/locale-zh-manifest.json
```

Expectations:
- localized assets are written into `interactive_assets`
- locale metadata is written into `interactive_page_locales`
- old assets under `localized/<locale>/` are replaced
- localized HTML should preserve original classes/markup needed for syntax highlighting and page styling
- translated interactive content should cover the source text as completely as practical

Locale QA requirements before `add-locale`:
- Audit the localized HTML/JS assets for leftover user-visible English sentences, especially frame scripts that update subtitles over time.
- Do not stop at the first frame; inspect later frames such as election, replication, partition recovery, conclusion, and any direct-entry hash routes.
- If you manually patch localized asset files after generating the locale manifest, refresh the manifest `sha256` values before publishing.
- Confirm the localized raw entry is single-locale, not a bilingual stacked page.
- Confirm there is no malformed Jekyll macro residue, broken table markdown, or raw template marker carried over from a previous repost.
- If the existing LanceDB article content is malformed, regenerate bilingual article artifacts from clean source before publishing the locale.

### Step 5: Frontend entry policy
- Article detail should open the local mirror directly.
- Preferred user-facing entry:
  - `/interactive-pages/ipg-<article_id>?lang=zh`
- Old SPA helper routes may exist, but the final experience should land on the standalone mirror page.
- If a shell/wrapper page is used, it should also expose a direct CTA to:
  - `/interactive-pages/ipg-<article_id>/entry?lang=<locale>`

### Step 6: Verify after write
DB verification:

```bash
cargo run -q -p sf-cli -- db --db-path /mnt/wsl/data4tb/static-flow-data/lancedb \
  query-rows articles --where "id = '<article_id>'" --limit 1

cargo run -q -p sf-cli -- db --db-path /mnt/wsl/data4tb/static-flow-data/lancedb \
  query-rows interactive_pages --where "id = 'ipg-<article_id>'" --limit 1

cargo run -q -p sf-cli -- db --db-path /mnt/wsl/data4tb/static-flow-data/lancedb \
  query-rows interactive_page_locales --where "page_id = 'ipg-<article_id>'" --limit 10
```

Route verification:

```bash
curl -I "http://127.0.0.1:39123/interactive-pages/ipg-<article_id>?lang=zh"
curl -I "http://127.0.0.1:39123/interactive-pages/ipg-<article_id>/entry?lang=zh"
```

Behavior verification:
- open the mirror page in a browser
- switch `中文 / English`
- open the current-language raw entry page directly
- confirm the key buttons/sliders/graphs still work
- click through multiple steps in later frames, not just the first `Continue`
- confirm syntax highlighting and original visual styling still render correctly
- confirm there are no duplicated runtime-generated elements after reload such as overlapping titles, subtitles, or SVG scenes
- confirm requests are served from `/api/interactive-pages/<page_id>/assets/...`
- confirm there are no obvious leftover English sentences in the localized locale except intentional protocol names / proper nouns
- confirm `/entry?lang=<locale>` does not embed a full second-language article body below the localized one

## Deliverable Checklist
- `articles` row exists and is queryable from frontend
- `interactive_pages.status = ready`
- `interactive_pages.translation_scope`
  - `article_only` for source-only mirror
  - `article_and_interactive` after localized interactive locale is added
- localized interactive route opens and is readable
- current-language raw entry route opens directly and remains readable
- article detail contains a strong CTA to open the interactive page
- wrapper shell contains a visible CTA to open the raw current-language render
- no runtime dependence on the original host for mirrored assets

## Failure Handling
- If the source host is not on the allowed list, stop before mirroring or use an explicit override.
- If the page only renders a shell, retry with Playwright capture before giving up.
- If localized assets break interaction, keep the original locale intact and fix the locale manifest/assets before re-running `add-locale`.
- If localization looks partly translated, inspect the localized frame scripts and other runtime text sources before blaming routing.
- If the article is already published, preserve unrelated fields unless the user explicitly asks for overwrite.

## Working Example
- `https://samwho.dev/bloom-filters/`
- article id: `bloom-filters`
- page id: `ipg-bloom-filters`
- expected frontend entry:
  - `/interactive-pages/ipg-bloom-filters?lang=zh`
