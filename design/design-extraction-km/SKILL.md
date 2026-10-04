---
name: design-extraction_KM
description: >
  Extract design tokens, components, layout, and motion specs from screenshots and screen-recording
  videos, then pair them with curated visual-theme guidance for implementation. Use this skill whenever
  the user wants to reverse-engineer a UI, extract a design system from screenshots or video, pull
  colors or typography or spacing from visuals, build a structured design spec, transform tokens to
  CSS or Tailwind or SwiftUI or Compose, or choose a cohesive visual theme for the resulting system.
  Supersedes `ui-spec-extractor` and `design-theme-library`.
---
<!-- Merged from: ui-spec-extractor, design-theme-library (2026-04-05) -->

# Design Extraction

Screenshot or video -> DTCG 2025.10 design tokens + components + layout + motion specs, with a merged visual-theme library for turning extracted structure into a coherent design system.

Hybrid vision + computational pipeline with confidence-driven iteration.

## What This Skill Owns

- Visual reverse engineering from screenshots and screen recordings
- Design-token extraction and validation
- Token transforms for code-facing outputs
- Theme selection, palette direction, typography systems, and motion philosophy

For curated theme packs and research-backed visual-system references, load the preserved material under `merged/design-theme-library/`.

## Feedback Loop

**Read `FEEDBACK.md` first** every time you use this skill. It contains accumulated learnings,
calibration fixes, and known issues discovered through real-world usage.

Cycle: detect issue → search FEEDBACK.md → scope fix → draft & ask user → write on approval → compact at 75 entries.

## Routing Table

| User says | Action |
|-----------|--------|
| "extract design tokens from this screenshot" | [Static pipeline](#static-pipeline) |
| "analyze this UI / design" | [Static pipeline](#static-pipeline) |
| "what colors / fonts / spacing are in this" | [Static pipeline](#static-pipeline) |
| "extract motion / animation from this video" | [Video pipeline](#video-pipeline) |
| "convert tokens to CSS / Tailwind / SwiftUI" | [Token transforms](#token-transforms) |
| "validate this design spec" | Run `scripts/validate_static.py <spec.json>` |
| "what colors are in this screenshot" | Run `scripts/static/palette_extract.py <image>` |

---

## Static Pipeline

Five-pass screenshot → design-spec extraction. Read `references/static-pipeline.md` for the full walkthrough with examples and edge-case guidance.

### Quick Start

1. **Pass 0 — Inventory.** Feed screenshot to vision with `references/prompts-static/pass0_inventory.md`. Get element inventory + platform detection.

2. **Run computational tools in parallel** (all output JSON to stdout):
   ```bash
   python scripts/static/palette_extract.py <image>   # K-means color clustering
   python scripts/static/ocr_extract.py <image>        # Text + font estimation
   python scripts/static/segment_ui.py <image>         # Element segmentation
   python scripts/static/grid_detect.py <image>         # Grid + spacing scale
   python scripts/static/corner_detect.py <image>       # Border radius
   python scripts/static/gradient_fit.py <image>        # Gradient detection
   ```

3. **Pass 1 — Tokens.** Use `references/prompts-static/pass1_tokens.md`. Feed inventory + tool outputs → DTCG tokens.

4. **Pass 2 — Components.** Use `references/prompts-static/pass2_components.md`. Group elements into components with tokenRefs.

5. **Pass 3 — Layout.** Use `references/prompts-static/pass3_layout.md`. Build hierarchy tree + grid analysis.

6. **Pass 4 — Validation.** Use `references/prompts-static/pass4_validation.md`. Cross-check, score confidence, decide: finalize / iterate / human_review.

7. **Output**: JSON matching `references/schemas/design-spec.schema.json`.

### Confidence Convergence

After pass 4, check the decision:
- `overallScore >= 0.85` → **finalize**
- `overallScore >= 0.65` and passes < 4 → **iterate** on lowest-scoring items using failure actions from `assets/config/static_confidence.json`
- `overallScore < 0.65` → **flag for human review** with specific open questions

Stop iterating if score doesn't improve by ≥ 0.02 between passes, or after 4 total passes (max 8 vision calls).

### Confidence Tiers

| Source | Range | When |
|--------|-------|------|
| Figma MCP / DevTools ground truth | 0.95–1.0 | Ground-truth available |
| Computational tool + vision agree | 0.75–0.90 | Hybrid pipeline |
| Vision model alone | 0.50–0.80 | No tool corroboration |
| Screenshot-only shadow/gradient | 0.35–0.60 | Hard-to-measure properties |

---

## Video Pipeline

Screen-recording video → motion tokens + orchestration + easing curves. Read `references/video-pipeline.md` for the full walkthrough.

### Quick Start

1. **Ingest.** `python scripts/video/ingest.py <video>` — FFprobe metadata, normalization.
2. **Segment detection.** `python scripts/video/segment_detect.py <frames_dir>` — Frame-diff energy, motion windows.
3. **Pass 0 — Inventory.** Use `references/prompts-video/pass0_inventory.md` with keyframes.
4. **Pass 1 — Semantic.** Use `references/prompts-video/pass1_segment_semantic.md` for motion token extraction.
5. **Element tracking.** `python scripts/video/track_element.py <frames_dir> <bbox>` — Template matching + optical flow.
6. **Easing fit.** `python scripts/video/easing_fit.py <trajectory.json>` — Cubic-bezier + spring fitting.
7. **Pass 2 — Implementation.** Use `references/prompts-video/pass2_implementation_map.md` for framework code mapping.

Output: motion spec JSON matching `references/schemas/example_motion_spec.json`. TypeScript types in `references/schemas/motion_tokens.ts`.

For scroll/parallax analysis, also read `references/prompts-video/pass1b_scroll_analysis.md`.

Validate motion tokens: `python scripts/validate_motion.py <spec.json> assets/config/motion_confidence.json`

---

## Token Transforms

Convert extracted DTCG tokens to platform-specific code via Style Dictionary v4.

```bash
# Extract tokens from a full design spec into standalone files
python scripts/dtcg_to_sd.py output.json --output tokens/ --split

# Build all platforms (CSS, Tailwind, SwiftUI, Compose, SCSS)
node scripts/sd_build.mjs

# Build single platform
node scripts/sd_build.mjs --platform css
```

The SD v4 config lives at `assets/sd-config.mjs`. Read `references/style-dictionary.md` for integration details and SD v4 vs v3 migration notes.

**Dependencies**: `npm install style-dictionary@^4` (optional: `@tokens-studio/sd-transforms@^1` for enhanced DTCG transforms — use v1.x, NOT v2.x which targets SD v5).

---

## DTCG Token Format

All tokens use DTCG 2025.10: `$value`, `$type`, `$description`. Never mix with legacy `value`/`type`.

```json
{
  "color": {
    "brand": {
      "primary": {
        "$type": "color",
        "$value": "#2563EB",
        "$description": "Primary brand color"
      }
    }
  }
}
```

Confidence and evidence live in a **separate `tokenMeta` block**, not inside `$value`. This keeps tokens clean for Style Dictionary transforms.

Supported types: `color`, `dimension`, `fontFamily`, `fontWeight`, `fontSize`, `lineHeight`, `letterSpacing`, `shadow`, `gradient`, `duration`, `cubicBezier`, `border`, `typography` (composite).

---

## Architecture

```
INPUT
  Screenshot (PNG/JPG) │ Video (MP4/MOV) │ URL
          │                     │
  ┌───────▼────────┐    ┌──────▼───────┐
  │ Pass 0:         │    │ Video        │
  │ Platform +      │    │ Ingest +     │
  │ Inventory       │    │ Segments     │
  └───────┬────────┘    └──────┬───────┘
          │                     │
  ┌───────▼─────────────────────▼──────┐
  │  Computational Tools (parallel)     │
  │  palette│OCR│segment│grid│corners  │
  │  gradients│flow│tracking│easing    │
  └───────┬─────────────────────┬──────┘
          │                     │
  ┌───────▼────────┐    ┌──────▼───────┐
  │ Pass 1-3:       │    │ Video        │
  │ Tokens →        │    │ Tracking +   │
  │ Components →    │    │ Easing Fit   │
  │ Layout          │    │              │
  └───────┬────────┘    └──────┬───────┘
          │                     │
  ┌───────▼─────────────────────▼──────┐
  │ Pass 4: Validation + Confidence     │
  │ Cross-check tools vs vision         │
  │ Score → finalize / iterate / flag   │
  └───────┬────────────────────────────┘
          │
  ┌───────▼──────────────────────┐
  │  Output: design-spec.json     │
  │  + motion-spec.json (video)   │
  │  + Style Dictionary build     │
  └──────────────────────────────┘
```

---

## Key Design Principles

**Vision + Computational Hybrid**: Vision model handles semantics (what is this element?). Computational tools handle measurement (what exact hex/px value?). When they disagree, lower confidence and iterate.

**DTCG 2025.10 First**: Token schemas use `$value`/`$type`/`$description`. Confidence metadata stays separate so SD transforms work cleanly.

**Confidence-Driven Iteration**: Every extraction has per-field confidence. Low confidence triggers the failure action from config. Max 4 passes to prevent infinite loops.

**Platform-Agnostic Tokens**: Extract canonical values (hex, px), then transform via Style Dictionary to platform-specific code.

**Extraction Tiers**: Ground truth (Figma/DevTools, 0.95+) > Hybrid (vision + tools, 0.70–0.90) > Screenshot-only (0.40–0.70).

---

## Known Confidence Ceilings

| Property | Confidence | Why |
|----------|-----------|-----|
| Color hex | 0.85–0.95 | K-means is reliable |
| Font family | 0.40–0.60 | Unreliable from screenshots; use platform priors |
| Font size/weight | 0.70–0.85 | Measurable from bbox + stroke width |
| Spacing | 0.75–0.90 | Grid detection is solid |
| Border radius | 0.65–0.85 | Anti-aliasing adds ±1-2px |
| Box shadow | 0.35–0.55 | Extremely hard from screenshots |
| Gradients | 0.55–0.75 | 2-stop OK; complex gradients unreliable |
| Motion easing | 0.70–0.90 | Spring/bezier fitting works well with clean video |

---

## File Map

``` 
design-extraction/
├── SKILL.md                          ← You are here
├── FEEDBACK.md                       ← Accumulated learnings (read first!)
├── scripts/
│   ├── static/
│   │   ├── palette_extract.py        ← K-means color clustering
│   │   ├── ocr_extract.py            ← Tesseract OCR + font estimation
│   │   ├── segment_ui.py             ← Edge detection + element segmentation
│   │   ├── grid_detect.py            ← Projection profiles + spacing scale
│   │   ├── corner_detect.py          ← Harris corners + radius fitting
│   │   ├── gradient_fit.py           ← Linear/radial gradient fitting
│   │   └── visual_diff.py            ← SSIM comparison for validation
│   ├── video/
│   │   ├── ingest.py                 ← FFprobe metadata + normalization
│   │   ├── segment_detect.py         ← Frame diff energy + motion windows
│   │   ├── track_element.py          ← Template matching + optical flow
│   │   ├── easing_fit.py             ← Cubic-bezier + spring fitting
│   │   └── flow_analysis.py          ← Dense optical flow + parallax
│   ├── validate_static.py            ← Token/component/layout validation
│   ├── validate_motion.py            ← Motion token validation
│   ├── dtcg_to_sd.py                 ← DTCG → SD token converter
│   └── sd_build.mjs                  ← Style Dictionary build runner
├── references/
│   ├── static-pipeline.md            ← Detailed walkthrough + edge cases
│   ├── video-pipeline.md             ← Video motion pipeline guide
│   ├── tool-reference.md             ← Computational tool accuracy + params
│   ├── style-dictionary.md           ← SD v4 integration + migration
│   ├── troubleshooting.md            ← Common issues + fixes
│   ├── motion-output-transforms.md   ← Motion → framework code examples
│   ├── prompts-static/               ← Vision prompts for passes 0-4
│   ├── prompts-video/                ← Vision prompts for video passes
│   └── schemas/                      ← JSON Schema, examples, TS types
└── assets/
    ├── config/
    │   ├── static_confidence.json    ← Thresholds + failure actions
    │   └── motion_confidence.json    ← Motion thresholds
    └── sd-config.mjs                 ← Style Dictionary v4 platform config
```

---

## Dependencies

**Python** (all scripts): `numpy`, `Pillow`

**Optional Python**: `pytesseract` + Tesseract binary (OCR), `scikit-image` (SSIM), `scipy` (easing fit)

**Node.js** (transforms): `style-dictionary@^4`, optionally `@tokens-studio/sd-transforms@^1`

**Video pipeline**: `ffmpeg` / `ffprobe`

---

## Reference Loading Guide

Read these files when you need deeper information. Don't load everything up front.

| Need | Read |
|------|------|
| Full static extraction walkthrough | `references/static-pipeline.md` |
| Full video extraction walkthrough | `references/video-pipeline.md` |
| Tool accuracy, params, limitations | `references/tool-reference.md` |
| Style Dictionary v4 setup, SD v3→v4 migration | `references/style-dictionary.md` |
| Something isn't working | `references/troubleshooting.md` |
| Writing motion → framework code | `references/motion-output-transforms.md` |
| Output JSON structure | `references/schemas/design-spec.schema.json` |
| Example output | `references/schemas/example_design_spec.json` |
| Confidence thresholds & failure routing | `assets/config/static_confidence.json` |
