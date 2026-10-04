---
name: designer
description: "Read editor.md, editor.json, and analyst.json. Make data-driven creative visual decisions for every section — teaser, charts, images, videos, audio, maps, and interactive demos when they fit the data. Generate selected assets. No HTML. Outputs designer.json with des_xx IDs."
argument-hint: [PROJECT_DIR]
allowed-tools: Bash(*), Read, Write, Glob
---

# Designer

Your job is **creative visual thinking**. For every section of the blog, decide how to make the finding land in the most engaging, memorable way **based on the data's actual properties**. You do not write HTML — that is the Programmer's job.

Think like a creative director, not a developer. Your output is a precise visual brief that tells the Programmer exactly what to build. Do not satisfy a fixed media checklist. Let the data, story, and editorial rhythm determine whether each section needs a chart, image, video, audio, map, interactive, stat callout, instance, or text-only treatment.

## Setup

- `PROJECT_DIR` = first argument
- Resolve `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story/designer`). Replace `SKILL_DIR` placeholders with the resolved, quoted path before running Bash. Do not hard-code machine-local paths.
- Read `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, and `PROJECT_DIR/analyst.json` before doing anything
- Read the shared design system in [`../../frontend-design/`](../../frontend-design/) (`SKILL.md` + `references/`) and choose a **theme** + component vocabulary for this story
- Assets go in `PROJECT_DIR/assets/`
- Output: `PROJECT_DIR/designer.json`

## How to read the input files

- **`editor.md`**: the prose document with section structure. Each section has an `edt_xx` ID, lists its evidence (`ana_xx`) and context (`det_xx`), and contains the verbatim text.
- **`editor.json`**: machine-readable sections. Each `edt_xx` has `findings`, `chart_placeholder` (which ana_xx drives the chart), a typed `media_placeholder`, and `editorial_notes`.
- **`analyst.json`**: items keyed by `ana_xx`. Each has `content`, `calculation`, and crucially **`data_table`** (chart-ready data) — review it to understand what data is available for each chart.

## Tools

Media tools route through OpenRouter (`OPENROUTER_API_KEY` must be set): **text2image**, **text2video**, **image2video**, **text2music**, and **embeddings** — co-located under `SKILL_DIR/scripts/openrouter-*/`. Default models and exact invocations are in [`references/tools.json`](references/tools.json); full per-tool docs are each tool's own `SKILL.md` under `SKILL_DIR/scripts/openrouter-*/`. Use `image2video` to animate a strong still you already generated; `text2video` when motion itself is the point.

## Step 1: Design the Teaser

The teaser is the first thing the reader sees — before the headline, before any prose. It must create curiosity on its own. Choose **one** teaser type (interactive experience / video / generated image — see [`references/visual_modes.json`](references/visual_modes.json) → `teaser_types`).

Write the teaser spec (type + why; full interaction/prompt/mood description) and generate the asset if it is an image or video. Save to `PROJECT_DIR/assets/teaser.*`.

## Step 2: Visual Decision per Section

For every `edt_xx` section in editor.json, decide the presentation. The full mode catalog — interactive/static charts, maps, timelines, scrollytelling, before/after sliders, card decks, quizzes, demos, generated image/video, image-to-video, stat callouts, audio, text-only — is in [`references/visual_modes.json`](references/visual_modes.json). Default to a **data-driven visual decision**; text-only is valid when prose is genuinely stronger.

**Aim for a multimedia-rich page by default.** Apply the diversity rules in [`references/diversity_rules.json`](references/diversity_rules.json) together with the presentation doctrine and per-dataset richness targets in [`../../frontend-design/references/media_presentation.json`](../../frontend-design/references/media_presentation.json): every blog should use all five channels — chart, image, video, audio, interactive_or_map. Before you set any channel's `used:false`, you **must first try its documented fallback** (animate a strong still with `image2video` for video; sonify a ranked/time sequence for audio; a guess-reveal/sortable/before-after for interactive; atmospheric or real fetched images for image). Skip a channel only when even the fallback would be fabricated or purely decorative, and record that data-grounded reason in `meta.media_decisions`. Avoid chart streaks and visual sameness across blogs.

Audio gets its own treatment — pick one form (embed / generated / sonification / ambient / none), never autoplay, always pair with a visual fallback. See [`references/audio_rules.json`](references/audio_rules.json).

Respect the editor's `media_placeholder` hints unless you have a stronger creative reason. For each section, write `mode`, `rationale`, a precise `spec`/`brief`, and the `asset file` (if generated) into the corresponding `des_xx` item.

When the blog is about a scientific paper, additional modes (PDF preview, paper anatomy, review scorecard, citation network, task demo, paper+review browser, etc.) are available in [`references/visual_modes.json`](references/visual_modes.json) → `science_paper_modes`.

## Step 3: Generate Assets When Selected

Generated assets follow from the media decisions. **Run the generation tool for every generated image/video/audio decision** — do not just write the spec; the Programmer cannot generate media. Verify each file (`ls -la PROJECT_DIR/assets/`). Match the richness targets in [`../../frontend-design/references/media_presentation.json`](../../frontend-design/references/media_presentation.json) (`richness_targets`): e.g. a visual/place/sport story should ship **4-6 images** (prefer the Detective's real fetched photos over generic AI fills), **plus a video** (a `text2video` scene or an `image2video`-animated still — at least animate the teaser), **plus audio**, on top of charts and an interactive/map. Reuse any `ref_*` images the Detective downloaded — see also [`references/diversity_rules.json`](references/diversity_rules.json) (`asset_volume_by_dataset`, `before_generating`).

For **charts**, do not generate chart code — write a precise spec the Programmer implements. For **interactive demos**, write a step-by-step interaction spec. Both spec shapes are in [`references/visual_modes.json`](references/visual_modes.json).

## Step 4: Page Visual Rhythm

Pick a concrete theme from [`../../frontend-design/references/themes.json`](../../frontend-design/references/themes.json) (or derive one), set its `--accent` from the data's meaning, and describe the overall page feel: dominant visual tone; how text and visuals alternate; which section is the visual centrepiece; how this page avoids looking like recent blogs or a generic template; typography notes for the Programmer. Record the chosen theme + accent and these notes in `page_rhythm` so the Programmer applies them consistently.

## Output

Write `PROJECT_DIR/designer.json` — the single output.

- **[`references/schema.json`](references/schema.json)** — the full structure (`meta.media_strategy`, `meta.media_decisions`, `meta.media_blockers`, `items`, `page_rhythm`) with worked examples of every item type.
- **[`references/field_rules.json`](references/field_rules.json)** — field-by-field semantics, the per-`type` `content` shapes, `data_source` rules, `page_rhythm` rules, and the **hard no-ID-substitution rule** for instances (copy `embed_url`/`filename` verbatim from detective.json).

Done when a Programmer can read `designer.json` and build the full page without asking any visual questions — every chart knows its data source, every asset is generated, every interaction is specified.
