---
name: clone-design
description: High-fidelity website/app clone design pipeline. Use when asked to clone, replicate, copy, or recreate any existing website or app screen. Captures real assets (images, SVGs, fonts, colors), extracts exact design tokens, generates the clone in Stitch, composites real assets into the output, then runs section-by-section visual comparison against the reference. Produces 90%+ accurate clones by combining Stitch generation with real asset injection.
---

# Clone Design Pipeline

9-phase pipeline for high-fidelity website/app clones.

## Prerequisites

- Playwright: `NODE_PATH=/data/.npm-global/lib/node_modules`
- Stitch MCP via mcporter: `MCPORTER_CALL_TIMEOUT=180000`
- Noto Color Emoji font installed (for emoji rendering)
- Scripts in: `skills/clone-design/scripts/`

## Pipeline

### Phase 1: CAPTURE — Reference Screenshots

Screenshot the target at mobile (390×844) viewport, full-page + per-viewport-section.

```bash
NODE_PATH=/data/.npm-global/lib/node_modules node skills/clone-design/scripts/extract-assets.js <url> <output-dir>
```

This produces:
- `screenshots/full-page.png` + `screenshots/section-N.png` per viewport
- `screenshots/viewport.png` (above-fold only)
- `assets/images/`, `assets/svgs/`, `assets/fonts/`
- `design-tokens.json` (structured extraction)
- `extraction-report.md` (human-readable summary)
- `source.html` (raw page HTML)

### Phase 2: ANALYZE — Extract Design Tokens

Read `extraction-report.md` and `design-tokens.json`. Extract:
- **Color palette** — every hex used, grouped by role (background, text, accent, border)
- **Typography** — font families, sizes, weights per element type
- **Spacing** — section gaps, card padding, element margins
- **Components** — identify cards, buttons, navs, hero sections, footers
- **Layout** — section order, background color per section, full-page height

### Phase 3: VISUAL STUDY — Section-by-Section Analysis

Use the `image` tool to analyze each `screenshots/section-N.png`:
- Describe every element, its position, colors, typography
- Note exact content (text, labels, CTAs)
- Identify images, illustrations, icons that need compositing
- Map section boundaries and background transitions

### Phase 4: GENERATE — Stitch Per Section (Multi-Pass)

For long pages, generate in **2-3 Stitch calls** max (Stitch handles long prompts well). Group sections logically:
- Pass 1: Hero + above-fold sections
- Pass 2: Mid-page content sections
- Pass 3: Footer + city grid + final sections

Each prompt must include:
- Exact hex colors from extraction
- Exact font families and sizes
- Exact content text (copy from source.html or visual analysis)
- Exact layout structure and spacing
- References to extracted image positions ("170px tall image placeholder at position X")
- `deviceType="MOBILE"` for mobile clones

Use `edit_screens` for refinement passes rather than regenerating from scratch.

### Phase 5: PULL — Get Generated Code

```bash
MCPORTER_CALL_TIMEOUT=60000 mcporter call stitch.get_screen \
  name="projects/{pid}/screens/{sid}" projectId="{pid}" screenId="{sid}" --output json
```

Download the HTML code via the `downloadUrl`. Save to `stitch-pulls/<project>/`.

### Phase 6: COMPOSITE — Inject Real Assets

```bash
NODE_PATH=/data/.npm-global/lib/node_modules node skills/clone-design/scripts/compose-assets.js \
  <generated.html> <extract-dir> <output.html>
```

This script:
- Replaces placeholder/stock images with extracted real images
- Injects @font-face declarations for downloaded fonts
- Preserves inline SVGs from extraction

After auto-compositing, manually review and fix:
- Image ordering (script matches sequentially — may need reordering)
- SVG icons that need injection at specific positions
- Font family names in CSS that don't match extracted names
- Any remaining placeholder content

### Phase 7: RENDER — Screenshot the Clone

```bash
NODE_PATH=/data/.npm-global/lib/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844, deviceScaleFactor: 2 } });
  await page.goto('file:///path/to/composed.html');
  await page.waitForTimeout(4000);
  await page.screenshot({ path: '/path/to/output.png', fullPage: true });
  await browser.close();
})();
"
```

### Phase 8: COMPARE — Visual Diff

```bash
NODE_PATH=/data/.npm-global/lib/node_modules node skills/clone-design/scripts/visual-diff.js \
  <extract-dir> <composed.html> <diff-output-dir>
```

Then use the `image` tool to compare each section pair:
- Reference `screenshots/section-N.png` vs Clone `clone-section-N.png`
- Score each section on: layout, colors, typography, content, assets
- Identify specific pixel-level differences

### Phase 9: ITERATE — Fix and Re-render

Based on comparison findings:
1. Edit the HTML directly for small fixes (colors, spacing, text)
2. Use `edit_screens` in Stitch for structural changes
3. Re-composite assets if images shifted
4. Re-render and re-compare

**Max 3 iterations.** After 3, assess if the approach needs rethinking.

## Quality Targets

| Metric | Target |
|---|---|
| Layout structure | 95%+ section ordering and sizing match |
| Color accuracy | Exact hex match on primary palette |
| Typography | Same font family, ±1px on sizes |
| Content | 100% text match (copied from source) |
| Images/assets | Real assets from source, correctly positioned |
| Overall fidelity | 90%+ visual match |

## File Organization

```
stitch-pulls/<project>/
├── extract/                  # Phase 1 output
│   ├── screenshots/          # Reference screenshots
│   ├── assets/               # Downloaded images, SVGs, fonts
│   ├── design-tokens.json    # Structured tokens
│   ├── extraction-report.md  # Human-readable summary
│   └── source.html           # Raw source
├── generated.html            # Phase 5 Stitch output
├── composed.html             # Phase 6 with real assets
├── final-rendered.png        # Phase 7 screenshot
└── diff/                     # Phase 8 comparison
    ├── clone-section-N.png
    └── diff-report.md
```

## Generating Original Designs (Non-Clone)

When designing original screens (not cloning an existing site), skip Phases 1-3 and 6. Instead:
1. Use brand tokens from SOUL.md / brand-systems skill
2. Craft a detailed Stitch prompt with exact specs (Phase 4)
3. Pull and render (Phases 5, 7)
4. Run the standard 10-point design review (from design-review-protocol skill)
5. Iterate on code directly for precise fixes
6. Max 3 iterations before reassessing approach

## Tips

- Always set `MCPORTER_CALL_TIMEOUT=180000` for Stitch generation calls
- Use `modelId="GEMINI_3_1_PRO"` for highest quality generation
- Copy exact text content from `source.html` — never paraphrase
- For emoji rendering, ensure `fonts-noto-color-emoji` is installed
- For dark themes, extract colors carefully — `rgba(0,0,0,0)` is transparent, not black
- Long pages (>3000px) should be generated in 2-3 passes for better fidelity
