---
name: pptx-generate-slide-skill
description: >-
  Fill a PowerPoint template with structured JSON via python-pptx Slide Master
  layouts. Not for presentations from scratch.
license: Apache-2.0
compatibility: opencode
category: Presentation
---

## What I do

**Pipeline contract: fill user-supplied templates — never build a deck from scratch.** I render a JSON `slide_data_list` into a `.pptx` via `scripts/ppt_builder.py`; I am the only approved method for generating presentations from structured data.

- Validate every deck against JSON schemas (two-layer LLM-JSON repair) before rendering
- Resolve resource placeholders into real assets before rendering; embed **native editable charts** and **native embedded pictures** (never linked, never chart-as-image)
- Introspect ANY `.pptx`, match layouts by placeholder-composition fingerprint
- Write speaker notes (user's prompt language) to each slide's Notes pane

**NOT for:** decks with no template, raw OOXML editing, thumbnails/visual analysis.

## Template contract

| File | Role |
|------|------|
| `template/default.pptx` | bundled default — used when no `template_path` given |
| `template/default.config.json` | optional layout-name pins (`<slide_type>_layout`) |
| `template/default.pptx.contract.json` | auto-generated introspection contract (mtime-cached, gitignored) |

- **User-supplied template = path pass-through:** `--template /path/to/user.pptx`; never overwrite the default. The engine introspects it before every render.
- **Severe template problems abort (TemplateError):** corrupt / not a PPTX / no slide master / zero layouts / serves none of the 8 slide types. Minor issues (missing fonts, no header/footer, small content area) stay non-fatal warnings.
- **Capability check before authoring:** `servable_slide_types(get_render_contract(tpl))` — author only slide types the template actually serves; downshift density to `concise` when a content area is `< ~30 in²`.

### Layout resolution — the gotchas that bite

Layouts resolve **by placeholder-composition fingerprint, NOT by index** — reordering layouts in the master must never break a deck. **Layout names are only a tie-breaker/fallback**, never the primary key (user templates rename layouts freely). Precedence:

1. `default.config.json` pin — explicit layout name, highest precedence
2. Fingerprint match — composition-closest layout (the template-agnostic path)
3. Name-based fallback (`_LAYOUT_NAME_MAP`) — backward-compat safety net
4. Degradation — skip slide + clear warning (never silent)

Among compatible layouts: name affinity → fewest surplus placeholders → largest `content_area_in2` → index.

## Slide data format

**Language: multilingual (relaxed).** Slide content and notes MAY be in any language — match the user's prompt language; do NOT force-translate. Notes MUST preserve the original user message verbatim and append a suggested transition.

8 slide types: `title_slide`, `content_slide`, `section_header_slide`, `two_content_slide`, `comparison_slide`, `content_image_slide`, `chart_slide`, `closing_slide`.

| Field | Req | Applies to | Notes |
|-------|-----|-----------|-------|
| `slide_type`, `title` | yes | all | — |
| `subtitle` | no | title/closing | **omit on `closing_slide`** — the `End` layout's built-in sign-off shows by default |
| `body` | no | content/content_image | `\n` = new paragraph; format `**Title** — Description` |
| `body_left` / `body_right` | no | two_content/comparison | same body format |
| `chart_type`, `categories`, `series` | yes | chart | 9 chart types — table in reference.md |
| `chart_options` | no | chart | styling overrides — table in reference.md |
| `image_path` | no | any slide | embeds a native picture; PICTURE placeholder filled when present |
| `image_position` | no | with `image_path` | `full` (default `below-title`), `half-left`, `half-right` |
| `image_size` | no | with `image_path` | `{"width": in, "height": in}` override |
| `data_query` (+ `data_hint`) | no | chart | resource placeholder — resolver fills `categories`/`series` |
| `notes` | yes | all | full presenter script ~120–180 words (style guide below) |
| `presenter_name` / `presenter_email` | no | closing | omit on first generation; set only when user picks "Add sign-off" in Stage-5 refinement |

Body parsing: each line splits at the first ` — `, ` - `, or `: ` into a bold title run + description run; `**` stripped automatically; no card-slot limit.

Full field reference, chart-type/chart-options/theme tables, and example JSON: [`reference.md`](reference.md).

## Resource resolution pipeline

```
agent emits placeholders -> resolve_slide_data_list() -> schema validation -> generate_ppt_from_data()
```

- Emit **placeholders, never fabricated URLs or chart numbers** — the agent never touches real URLs
- **`data_query` contract:** the resolver makes NO network calls; real numbers come from the agent's `webfetch` pre-flight written as concrete `categories`/`series`. **Fabricating chart numbers to pass validation is forbidden** — every value must trace to a fetched source (citation lands in notes)
- Concrete values always win — resolver never overwrites an existing `image_path`/`series`
- Non-fatal: unconfigured provider or failed fetch → warning, slide renders without the asset
- Config: copy `scripts/resolver.config.example.json` → `scripts/resolver.config.json` (gitignored)

## Schema validation

`validate_slide_data_list(data, strict=True, density_mode=…)` — structured errors (slide index + field path + reason) so the agent can self-correct.

- **Strict mode:** missing `notes` and schema violations block rendering (agent pre-flight gate)
- **Density mode** (`'standard'|'concise'|'text-heavy'`|None): per-slide word-budget check → warnings only, never blocks, never promoted by strict
- **Default mode:** degrade gracefully (skip unknown slide types, default bad `chart_type` to `bar`, skip dataless charts); abort only on unrecoverable breakage (e.g. not an array) with a clear `ValidationError`
- **Two-layer retry:** `parse_and_validate(raw_text)` repairs common LLM-JSON mistakes (code fences, trailing commas, single quotes, variable assignments) before validating

Invocation snippets: [`reference.md`](reference.md).

## Density modes

Deck-wide per-slide visible-text budget — the primary lever against text overflow.

| Mode | Words/slide | Use when |
|------|-------------|----------|
| `concise` | 0–10 | image-only/keynote/hero decks; small content areas |
| `standard` ⭐ default | 30–50 | balanced reporting decks |
| `text-heavy` | 75–150 | dense self-study/handout decks |

Counts visible text only (`title`+`subtitle`+`body`+`body_left`+`body_right`; emphasis markers and ` — `/` - `/`: ` delimiters stripped; each CJK char = 1 word). Not counted: `notes`, chart `categories`/`series`. Underflow on title/section/closing slides is expected and harmless; out-of-budget = warning, never error. Default `standard` for first generation (auto-downshifted `concise` for small content areas; a user-stated density intent wins); adjustable post-generation in Stage 5.

## Generation workflow

1. **Outline → self-critique → detail+JSON**, schema-validated at each JSON stage. The primary agent does NOT pause after the outline — first generation is autonomous (self-critique, no pre-generation prompt); refinements are offered after the file is returned. Subagents skip the refinement prompt too. Details: `docs/DESIGN-multi-stage-generation.md`.
2. **Slide-count convention:** "N pages" = TOTAL deck including cover and closing (N ≥ 3 → 1 cover + N−2 content + 1 closing; N = 2 → cover + 1 content; N = 1 → cover only). Closing defaults to `"Thank You"` title, no `subtitle` authored.
3. **Temp cleanup:** outline artifacts (namespaced system temp dir) cleared automatically after every successful render (`cleanup_temp=True`) — nothing pollutes the repo.
4. **Post-generation (primary agent only):** one multi-select refinement question (density ±, slides ±, add sign-off, change ratio, no adjustment) — never a second prompt.

## Render

```bash
# default template
python ppt_builder.py --output report.pptx --data slides.json
# user template (path pass-through) · optional aspect ratio
python ppt_builder.py --template ~/my_company_template.pptx --output report.pptx --data slides.json --target-size 4:3
```

**Multi-aspect-ratio output (US-4.6):** `target_size` accepts a preset (`"16:9"`, `"4:3"`, `"1:1"`) or `{"width_in": W, "height_in": H}`; every element scales proportionally. No-op when the target ratio equals native. **Hidden-JSON-schema embed rule:** the output's embedded schema `slide_dimensions` is rewritten to the target size — the deck is self-describing and re-usable as a target-sized template; a stale input-embedded schema is never laundered in. The `<output>.render.json` sidecar records `aspect_ratio` + scale factors.

**Verification before handoff:** check servable slide types up front (capability check above); after rendering, read 2–3 notes from the newest `output/*.pptx` to confirm house style (bundled default has 0 slides — snippets in reference.md).

Output path: `<project_root>/output/`, function returns the absolute `.pptx` path.

## Error handling — rule of thumb

Fatal (clear exception): non-array input, strict-mode schema violations, missing template, `TemplateError`. Everything else degrades with a logged warning — unknown slide type, missing placeholder, failed slide, unknown `chart_type` (→ `bar`), missing chart data, bad `image_path`, unknown `image_position` (→ `below-title`), resolver failure. Full table: [`reference.md`](reference.md).

## Speaker notes style — four-part structure

Every `notes` field = a full presenter script (~120–180 words), NOT bullet summaries:

1. **KEY MESSAGE** — one crisp declarative takeaway
2. **Verbatim dialogue + stage directions** — quoted speakable sentences tied to the slide's real numbers/names, interspersed imperatives (`Pause. Let the number land.`); cover/closing open with `[morning/afternoon]` and `[Name]`; 2–4 quote blocks
3. **TRANSITION** — one quoted line bridging to the next slide
4. **COACHING** — MUST include (a) tone/pacing note AND (b) an anticipated Q&A ("be ready for…")

GOOD example block: [`reference.md`](reference.md).

## Self-critique rubric

Revise the outline against these before writing JSON: consistency (one coherent story) · flow (each slide sets up the next) · coverage gaps · redundancy · length (right count for the ask) · template fit (small content area → `concise` budget; only servable slide types).

> Removed 2026-09: chart-type/options/theme tables, placement-preset details, example interaction transcripts, end-to-end deck examples, execution/introspection code dumps, and the error-handling table — moved to reference.md or deleted.
