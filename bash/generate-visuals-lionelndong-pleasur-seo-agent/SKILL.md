---
name: generate-visuals
description: Realize every typed [VISUAL:...] placeholder in the cited draft into an actual on-brand asset — deterministic charts/diagrams/tables/covers/annotations (headless browser + real logo), Playwright screenshots/action-shots of brand UI, and the gated AI infographic/concept-illustration lanes. AI image type=image is retired (dropped + logged as a manual TODO). Updates the draft to reference local image paths.
allowed-tools: Read, Write, Edit, Bash
---

> **✅ Visual generation is WIRED and ON by default (`BLOG_AGENT_VISUALS=on`, 2026-06-29).**
> The dispatcher (`scripts/generate_visuals.py`) routes every typed `[VISUAL:...]` to its on-brand
> engine, optimizes the PNG, records it in `content-pipeline/images/{slug}/manifest.json`
> (`status: captured|manual|failed`), and rewrites the draft so each captured placeholder becomes
> `![alt](images/{slug}/file.png)`. **No silent fallbacks:** a type that can't be produced loud-fails
> into the manifest as `failed` (the visuals gate then halts) — nothing is ever substituted.
> Set **`BLOG_AGENT_VISUALS=off`** to fall back to the legacy no-op (placeholders left in place, no
> assets) for a text-only dry run.

> **No AI image generation for `type=image` (Ryan-faithful rebuild, 2026-06-25):** the retired
> `type=image` placeholder is dropped — stripped from the draft and logged as a non-blocking manual
> TODO; it never calls an image model. The two *gated* AI lanes that DO run are first-class
> `type=infographic` and `type=concept-illustration` (Nano Banana via Replicate), each of which still
> owes the hard vision gate in `VISUAL-CRITIQUE-LOOP.md` before publish.

> **Every generated visual MUST pass `VISUAL-CRITIQUE-LOOP.md`** (render → deterministic check →
> vision critique → fix → re-render, max 3) before it ships. The deterministic engines give a clean
> first filter; the vision pass catches semantic/aesthetic issues. The gated AI lanes
> (infographic, concept-illustration, and the AI cover route) are the strictest.


# Generate Visuals Skill

Take every `[VISUAL:type=...;...]` placeholder in the cited draft and produce a real asset on disk for the types we can automate, plus a `manual-capture.md` to-do for the rest. Update the draft to reference the local images so subsequent stages (preview, format-for-publish) treat them as ordinary markdown images.

This is the skill that closes the gap Ryan Law called out in his content-engineering blog: "blog post images are not a solved problem, yet" — we automate the deterministic types (real screenshots, data charts/tables) and leave generative imagery to an editor, exactly as he does.

## Diagram engine (process flows / decision trees / flow charts)

A standalone premium engine for "how it works" process flows, step sequences, and simple decision
trees — **clean + structured + on-brand**, deliberately distinct from the hand-drawn infographic.
Renders headless via `scripts/render_diagram_web.py` (dagre.js auto-layout + a custom brand-card
renderer — HTML node cards over an SVG edge layer; `dagre.min.js` bundled, no runtime CDN):
`--type linear|tree|flow` or `--config spec.json`. Full usage + spec format in **`DIAGRAM-THEME.md`**.
Like the chart / infographic / annotation engines, every output MUST pass `VISUAL-CRITIQUE-LOOP.md`
before publish.

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` — the cited draft with typed placeholders (or legacy `[SCREENSHOT: ...]`)
- `brand-config.md` — product URLs and visual-generation config block
- `../../../templates/visual-types.md` — taxonomy reference

## Process

1. **Run the dispatcher.** It does everything below in one shot:

   ```bash
   doppler run -- python .claude/skills/generate-visuals/scripts/generate_visuals.py "<slug>"
   ```

   (Drop the `doppler run --` prefix if env vars are exported in the shell.)

2. **What the dispatcher does:**
   - Parses every `[VISUAL:...]` and legacy `[SCREENSHOT:...]` placeholder
   - Dispatches by `type` to the right engine (all engines run **in the container** — patchright +
     chromium + node + bundled apexcharts/dagre — invoked as subprocesses):
     - `chart` → `render_chart_web.py` (ApexCharts headless, brand theme + real logo) — **replaces** the old matplotlib `render_chart.py`
     - `diagram` (`process`/`decision-tree`/`flowchart`/`cycle`) → `render_diagram_web.py` (dagre layout + brand card)
     - `table` (`comparison`/`pricing-table`/`feature-table`) → **DROPPED — author a NATIVE `:::` component** (`:::table`/`:::feature-matrix`/`:::decision-table`/`:::proscons`/`:::pricing`), never a PNG. (`render_table_card.py` still runs inside `/format-for-publish` for the site-renderer table→card conversion, PLEAA-567 — just not as an authored visual.)
     - `cover` / `hero` → **`cover_hero_engine.js` (the APPROVED Ahrefs FLAT-VECTOR illustration on brand-blue) → `logo_stamp.py --no-logo --bg-color #2E90FA`**, 1600×900, needs the vision gate. AI (Replicate) — a deliberate operator override of the deterministic default, FOR COVERS. `render_cover.py` line-art is the FREE FALLBACK (no key / gen fails).
     - `annotation` → `annotate_screenshot.py --strict` (callout boxes/arrows; a missing target HARD-FAILS)
     - `screenshot` → `capture_screenshot.py` (patchright; uses `auth/state.json` if it exists)
     - `action-shot` → `action_shot.py` (deterministic retina capture + brand frame; **default** now, no paid cloud agent). Logged-in shots need the showcase session → else `manual` (`session_required`).
     - `external` → `capture_screenshot.py` (clips to `selector`; CF/login → `/capture-visuals` fallback breadcrumb)
     - `demo` (`animation`/`video`/`gif`) → `animate_demo.py` (looping GIF/MP4/WebP; auth scenes → `manual`)
     - `infographic` → `infographic_engine.js` (Nano Banana) **then** `composite_logo.py` (stamp real logo) — gated AI, vision gate required
     - `concept-illustration` → `concept_illustration_engine.js` (Nano Banana) + `concept_palette_check.py` (advisory) — gated AI, vision gate required
     - `image` → **dropped** (AI image generation retired): stripped from the draft + logged as a manual TODO; no image model is ever called
     - `card` → **skipped** (the blog has native stat/quote/callout components — not a generated asset)
     - `none` → skipped (no asset)
   - **No silent fallback:** any type that can't be produced (unresolved chart data, prose-only diagram, missing showcase session for an authed action-shot, engine error, Replicate failure) is recorded `failed`/`manual` with a reason — never substituted with a different visual.
   - Optimizes every captured PNG via `optimize_image.py` (Pillow lossless re-save)
   - Writes `content-pipeline/images/{slug}/manifest.json` with the typed record of every visual
   - Writes `content-pipeline/images/{slug}/manual-capture.md` with editor instructions for un-automated visuals
   - Rewrites `content-pipeline/6-drafts-cited/{slug}.md` — every `[VISUAL:...]` whose asset succeeded becomes `![alt](images/{slug}/file.png)`. Failed or manual entries keep their typed placeholder (so the gate catches them).

3. **Tell the user** the manifest path, how many visuals were captured vs. flagged manual, and any failures.

## Output

Under `content-pipeline/images/{slug}/`:
- `chart-{n}-{slug}.png` · `diagram-{n}-{slug}.png` · `table-{n}-{slug}.png` · `cover-{n}-{slug}.png` · `annotation-{n}-{slug}.png` — deterministic engine renders
- `screenshot-{n}-{slug}.png` · `action-{n}-{slug}.png` · `external-{n}-{slug}.png` — patchright captures
- `demo-{n}-{slug}.gif` (+ `.mp4`/`.webp`) — animated demos
- `infographic-{n}-{slug}.png` · `concept-{n}-{slug}.png` — gated AI lanes (logo-stamped for infographics)
- `manifest.json` — typed record per visual: `{type, status: captured|manual|failed, path?, engine?, reason?, alt, ...}`
- `manual-capture.md` — editor instructions for manual/failed entries (auth-gated action-shots, blocked externals, failed renders)

Plus an updated `content-pipeline/6-drafts-cited/{slug}.md` with image markdown substituted in.

## Auth setup (one-time)

For Pleasur.AI app pages that require login, run once:

```bash
python .claude/skills/generate-visuals/scripts/setup_auth.py
```

This launches a non-headless browser. Log in to `pleasur.ai`. The script saves cookies + storage state to `.claude/skills/generate-visuals/auth/state.json` (gitignored). Future captures replay that session.

If `state.json` is missing, screenshot captures of authenticated pages will fail and be flagged in `manual-capture.md`.

## Quality checklist

- [ ] Every typed visual placeholder either produced a PNG/GIF or appears in `manual-capture.md`
- [ ] No naked `[VISUAL:...]` or `[SCREENSHOT:...]` left in the cited draft for types that should have been captured
- [ ] All captured PNGs are at least 1200px wide (covers exactly 1600×900)
- [ ] manifest.json records `status` per visual (captured/manual/failed) with a `reason` for non-captured
- [ ] Filenames in `images/{slug}/` are predictable (type-N-slug.png) and referenced from the draft
- [ ] Every captured visual passed `VISUAL-CRITIQUE-LOOP.md` (deterministic check + vision critique) before publish

## Backwards compatibility

Legacy `[SCREENSHOT: description]` placeholders are still recognized and treated as `[VISUAL:type=screenshot;what=description]`. Generated assets are saved with the same naming scheme.

## Failure modes (loud — no silent substitution)

Every failure becomes a `failed`/`manual` manifest entry with a `reason`; the placeholder is kept in
the draft so the visuals gate catches it. Nothing is ever swapped for a different visual.

- **`type=image` placeholder**: dropped and logged as a manual TODO (AI image generation retired) — the placeholder is stripped; the article ships without it.
- **Chart/diagram with unusable data**: free-text or unresolved `data=` → `failed` (`chart_data_unresolved` / `diagram_requires_structured_data` / `diagram_data_unresolved`). Fix by adding the numbers/nodes to `content-pipeline/1-research/<slug>-data.json` under the referenced key, or a `config=` file.
- **Table with no spec**: no `columns=`, no resolvable `data=`, no `config=`/`spec=` → `failed` (`table_no_spec_columns_or_data`).
- **Annotation target missing/overlapping**: `--strict` → `failed` (`annotation_strict_failed`, with `missing`/`overlaps` in the entry). Fix the `selector`.
- **Action-shot needs login**: an authed shot without the showcase session → `manual` (`session_required`) with the `setup_auth.py` fix hint (not a hard fail — it's an operator follow-up).
- **External blocked**: Cloudflare / login wall → `failed` with a `fallback.method=claude_in_chrome` breadcrumb; `/capture-visuals` retries via a real Chrome session.
- **Gated AI lane**: missing `REPLICATE_API_KEY` or a Nano-Banana error → `failed` (`infographic_generate_failed` / `concept_illustration_generate_failed`). No fallback by design.
- **Engine timeout / missing executable**: `failed` (`engine_timeout_*s` / `executable_not_found`); the rest of the stage continues.
- **Playwright auth missing (screenshot)**: `capture_screenshot.py` captures without auth (public pages render; authed pages show login) and flags a short/blank capture for editor review.

## Auto-capture coverage by type

Deterministic, free, on-brand engines (the common path — white card on `#F7F8FA`, IBM Plex + Geist,
brand palette, the real composited Pleasur.ai logo):

- **`chart`** — `render_chart_web.py` (ApexCharts headless; brand theme + real logo baked in). `style=`/`chart_type=` picks `bar|bar_h|area|line|donut`; `data=` is `research.<key>` (resolved from `content-pipeline/1-research/<slug>-data.json`), `path:KEY`, or a full `config=` ApexCharts options file. **Replaces** the old matplotlib `render_chart.py`. See `CHART-THEME.md`.
- **`diagram`** (`process`/`decision-tree`/`flowchart`/`cycle`) — `render_diagram_web.py` (dagre auto-layout + brand-card renderer). `style=`/`diagram_type=` picks `linear|tree|flow|cycle`; needs **structured** input: `data=research.<key>` or `config=<path to a {direction,nodes,edges} spec>`. A diagram described only in prose loud-fails (`diagram_requires_structured_data`). See `DIAGRAM-THEME.md`.
- **`table`** (`comparison`/`pricing-table`/`feature-table`) — `render_table_card.py` (brand table card; `comparison`/`pricing`/`grid`/`table` modes). Spec from `columns=A,B,C` + rows in `data=`, an inline/`research.<key>` spec object, or a `config=`/`spec=` file. See `COMPARISON-TABLE.md`.
- **`cover`** / `hero` — `render_cover.py` (deterministic line-art hero, **1600×900**, free). `title=` (or `what=`) required; `theme=light|dark|bold|aurora`, `accent=`, `eyebrow=`/`subtitle=`, `icon=`, `motif=` map to flags; `content=<cover JSON>` wins. The auto-pipeline uses **only** this free route — the AI cover lane (`cover_hero_engine.js`) stays a manual operator choice. See `COVER-RECIPE.md`.
- **`annotation`** — `annotate_screenshot.py --strict` (numbered callout boxes/arrows on a brand-URL shot). `url=` (or `target=`); `targets=<JSON array of {selector,kind,label}>` or a single `selector=`/`annotate=`; `dismiss=` clicks an age/cookie gate; `color=` sets the highlight. **Always `--strict`** — a missing target HARD-FAILS into the manifest (mandate: no silent skip).

Stateful / capture engines:

- **`screenshot`** — `capture_screenshot.py` (patchright headless; uses `auth/state.json` if present).
- **`action-shot`** — `action_shot.py` (deterministic patchright retina capture + brand frame; presets in `action_shot_presets.json`, polish in `frame_shot.py`). **Default now** (no paid cloud agent; the old `BROWSER_USE_ENABLED` gate is gone — opt into Browser Use only by editing the engine). Public presets (pricing) work now; **chat/call/gallery need the showcase session** from `setup_auth.py` (Standard+ for calls) → else surfaced as `manual` (`session_required`). See `ACTION-SHOT-RECIPE.md`. (Editor fallback `/capture-visuals` remains for one-off interactive grabs.)
- **`external`** — **auto-captured (PLEAA-417, 2026-05-06).** patchright opens the URL, clips to `selector`, padded crop. Cloudflare / login walls fall back to `/capture-visuals` (Claude-in-Chrome, real session). ToS bypasses out of scope — both paths fail ⇒ entry stays `failed`, gate halts.
- **`demo`** (`animation`/`video`/`gif`) — `animate_demo.py` (looping GIF + MP4 + WebP, on-brand frame). Public scenes (`pricing-toggle`, `pricing-scroll`) run now; **auth scenes** (`chat-typing`, `image-generating`, `call`) come back `manual` (`blocked_on_auth`) until the showcase session lands. Draft references the GIF; MP4/WebP sit alongside (`alt_formats`). See `ANIMATED-DEMO.md`.

Gated AI lanes (Replicate / Nano Banana; **mandatory `REPLICATE_API_KEY`, loud-fail, no fallback**; every output owes the hard vision gate in `VISUAL-CRITIQUE-LOOP.md`):

- **`infographic`** — `infographic_engine.js` (hand-drawn-edu) **then** `composite_logo.py` (stamp the real logo). Needs `content=<JSON {title,subtitle,takeaway,items[]}>` or inline `data=`. See `INFOGRAPHIC-RECIPE.md`.
- **`concept-illustration`** (`concept`) — `concept_illustration_engine.js` for a truly abstract concept (rare ~6% slot), then `concept_palette_check.py` (advisory `WARN` attached to the manifest, not decisive). Needs `content=<JSON {concept,metaphor,...}>` or inline `data=`. Logo OFF for in-body. See `CONCEPT-ILLUSTRATION-RECIPE.md`.

Retired / non-asset:

- **`image`** — **retired** (dropped to a manual TODO; no AI image generation). Use `screenshot`/`chart`/`table`/`diagram`/`infographic`/`concept-illustration` instead.
- **`card`** — **skipped**: the blog has native stat/quote/callout components (`render_card_web.py` exists for one-off use, but the auto-pipeline does not generate card assets — see `CARD-STANDARD.md`).
- **`none`** — skipped (argue with prose, not a picture).

## Failure → fallback dispatch (PLEAA-417)

When `external` capture fails for one of the bot-block reasons (`cloudflare_challenge_unresolved`, `redirected_to_login`, `navigation_failed`, `image_dimensions_too_small`), the manifest entry stays `status: "failed"` (so `pipeline_gate.py` halts as PLEAA-392 requires) but carries a `fallback` block:

```json
{
  "fallback": {
    "method": "claude_in_chrome",
    "skill": "/capture-visuals",
    "url": "...", "selector": "...", "what": "...", "sub": "..."
  }
}
```

The orchestrator (or an autonomous heartbeat) reads the failed entries, runs `/capture-visuals {slug}` to dispatch the Chrome MCP fallback, and re-runs the gate. If the Chrome path also fails, the entry stays `failed` and the editor handles it manually — we never bypass site protections.
