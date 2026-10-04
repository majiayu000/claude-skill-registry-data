---
description: "Shared image generation agent for the multi-channel content factory. Reads the inspiration library at ./agents/image-gen/inspiration/, picks the right style based on channel and content context, and generates a fresh on-brand SVG. Invoked inline by channel pipelines at the image step. Accepts any inspiration format: SVG, PNG, JPG, PDF, screenshots."
trigger: /image-gen-agent
---

# /image-gen-agent

Generates on-brand SVG images for any channel. Draws from a curated inspiration library — reads the closest matching style, extracts its design DNA, and produces a new SVG carrying the actual post content.

**Project-side home:** `./agents/image-gen/` (relative to project root)
**Inspiration library:** `./agents/image-gen/inspiration/`
**Style index:** `./agents/image-gen/inspiration/MANIFEST.md`

---

## Project layout (reference)

```
content-factory/
├── agents/image-gen/
│   ├── AGENT.md                    ← project-side reference (points back here)
│   └── inspiration/
│       ├── MANIFEST.md             ← READ THIS FIRST — style index + selection rules
│       ├── stat-card-dark/         ← 1080×1350, LinkedIn default
│       ├── editorial-bold/         ← 1600×900, blog hero
│       ├── quote-card-minimal/     ← 1080×1080, X quote card
│       └── gradient-hero/          ← 1920×1080, presentation cover
```

---

## Interface contract

Channels call this agent with a structured brief at the image step:

```
[IMAGE BRIEF]
Channel: <linkedin | blog | x | presentation>
Dimensions: <W>×<H>  OR  auto  OR  reason   ← "reason" triggers Step 0 reasoning
Style hint: <style name from MANIFEST.md>  OR  reason   ← "reason" triggers Step 0 reasoning
Variations: <1 | 2>   ← omit for 1; pass 2 to generate two distinct SVGs in one call
Content-type: <stat-card | editorial | quote-card | hero>
Final post: <full post text — required when Variations: 2 or Dimensions/Style: reason>
Stats:
  - <label>: <value> [optional note, e.g. "↓ from 30h"]
  - <label>: <value>
Winning angle: <angle name — required when Variations: 2>
Tagline: <one short line — footer or below hero>
Author: <name>
Handle: <social handle to promote, e.g. "@teachmebro">
Domain: <e.g. "AI Engineering">
Post has URL: <yes | no>   ← only include when relevant
Output path: <relative/path/to/impact.svg>   ← for Variations: 2, treat as prefix (impact-1.svg, impact-2.svg)
```

**Default output location.** When the brief omits `Output path` — e.g. a standalone `/image-gen-agent` call with no owning post folder — save to the root `./image-gen-output/` folder. Derive the SVG filename from a short kebab-slug of the content/tagline (e.g. `systems-while-you-sleep.svg`). The PNG goes in `./image-gen-output/exports/` per the Step 4 convention. Channel pipelines that pass an explicit `Output path` write into their own per-post folder as before.

---

## Step 0 — Reason about variations (only when Variations: 2 OR Style/Dimensions is "reason")

When the brief has `Variations: 2` or `Style hint: reason` or `Dimensions: reason`:

1. Read the `Final post` text in the brief. Identify:
   - **Data density:** count distinct stats or concrete data points in the post
   - **Post tone:** pick one — analytical / storytelling / contrarian / tactical / comparative
   - **Visual priority:** does the post hinge on a bold statement, data comparison, or a personal moment?

2. Read `./agents/image-gen/inspiration/MANIFEST.md` to survey available styles and their mood tags.

3. Reason about **Variation 1** — state your thinking explicitly:
   - **Dimension:** choose based on content:
     - Portrait 1080×1350 — for data-dense posts (≥3 stats) or stat-tile grids needing vertical space
     - Square 1080×1080 — for balanced posts, quote-card tone, mobile-first versatility
     - Landscape 1200×627 — for big single-statement posts, editorial/contrarian tone, minimal data
   - **Style:** pick the best-fit style from MANIFEST.md for this tone and data density. Prefer dark SVG-native styles (`stat-card-dark`) for data-heavy posts, and real-image-inspired styles for tonal/editorial posts.

4. Reason about **Variation 2** — MUST differ from Variation 1 in BOTH dimension AND style:
   - Pick a style that offers a contrasting visual mood (dark vs light, structured vs editorial)
   - Pick a dimension different from Variation 1
   - If Variation 1 is Portrait, Variation 2 should be Square or Landscape
   - If Variation 1 is Square, Variation 2 should be Portrait or Landscape
   - If Variation 1 is Landscape, Variation 2 should be Square

5. Print the reasoning block before generating:
   ```
   [IMAGE REASONING]
   Post tone: <analytical | storytelling | contrarian | tactical | comparative>
   Data density: <N stats/data points>
   Winning angle: <angle>

   Variation 1:
     Style: <style name> — <one line why this style fits>
     Dimension: <W×H (format name)> — <one line why this dimension fits>

   Variation 2:
     Style: <style name> — <one line why this contrasts well>
     Dimension: <W×H (format name)> — <one line why this dimension is different and fits>
   ```

6. Proceed to Step 1 using the resolved styles. Generate both variations sequentially — Variation 1 first, then Variation 2. Use output path as a prefix: `<prefix>-1.svg`, `<prefix>-2.svg`.

---

## Step 1 — Read the inspiration library

1. Read `./agents/image-gen/inspiration/MANIFEST.md`
2. Identify 1–2 candidate styles using the selection rules in the manifest
3. Read the sample file(s) for those styles. Accepted formats: **SVG, PNG, JPG, PDF, screenshots** — any format the Read tool can open
4. Extract the design DNA:
   - Color palette and gradient definitions
   - Typography scale: sizes, weights, letter-spacing per hierarchy level
   - Layout grid: margins, column widths, section heights, spacing rhythm
   - How data/stats are displayed (tile layout, bar charts, hero number treatment)
   - Footer and byline structure
5. Form a mental model before generating: "this style uses X margin, Y font scale, Z tile grid"

If the inspiration file is a raster image (PNG/JPG/screenshot) or PDF, read it visually — extract the same design attributes by observation.

---

## Step 1.5 — Resolve LinkedIn dimensions (only for single-image calls where Dimensions is "auto" or omitted)

Skip this step if `Variations: 2` or `Dimensions: reason` — dimensions were already resolved in Step 0.

If `Dimensions: auto` — or if the brief omits Dimensions — resolve the correct LinkedIn format before generating. Use this table (first match wins):

| Condition | Format | Dimensions |
|-----------|--------|------------|
| `Post has URL: yes` | Landscape / link preview | **1200×627** |
| ≥3 stats in the brief AND content-type is `stat-card` | Portrait | **1080×1350** |
| content-type is `editorial` or `quote-card` | Square | **1080×1080** |
| 1–2 stats or qualitative only (no real numbers) | Square | **1080×1080** |
| Fallback | Portrait | **1080×1350** |

**LinkedIn format reference:**

| Format | Dimensions | Best for |
|--------|------------|----------|
| Square | 1080×1080 | Mobile-first posts, quote cards, balanced graphics — most versatile |
| Portrait | 1080×1350 | Stat-heavy posts, max mobile feed real estate |
| Landscape | 1200×627 | Link-share previews, desktop hero images |
| Max file size | 8 MB (keep under 5 MB) | — |

State the resolved dimensions in the surface block. Use the resolved value as the `viewBox` for the SVG.

---

## Step 2 — Select and adapt

Pick one primary style. Apply blending rules from MANIFEST.md when the brief spans two styles.
State the chosen style (and any blend) in the surface block output.

---

## Step 3 — Generate the SVG

Produce a complete, valid SVG. Follow the selected style's design DNA for layout and aesthetics, but use the actual stats, tagline, author, and domain from the brief.

### SVG structure rules:
- `viewBox` must match the brief dimensions exactly
- All gradients defined in `<defs>` with descriptive IDs
- System font stack: `font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"`
- Use `text-anchor="middle"` for centered elements; left-align body text at the margin
- Encode special characters as XML entities: `&#215;` (×), `&#183;` (·), `&#8595;` (↓), `&#8220;` ("), `&#8217;` (')
- No JavaScript, no external image references, no embedded raster data
- Keep SVG under 200 KB

### Design tokens (use from selected style; fall back to these defaults):
```
Background:       #0a0e1a → #111827 (dark, top-to-bottom)
Accent gradient:  #22d3ee → #a78bfa (cyan → violet, left-to-right)
Body text:        #e2e8f0
Muted text:       #94a3b8
Subtle / labels:  #64748b
Tile bg:          #1a2538 → #141e2d
Tile radius:      16px
Accent line:      3–5px height, radius 2
Outer margin:     80–100px
```

### Typography scale (match selected style):
```
Hero number / main stat:   200–280px, weight 900, gradient fill
Section headline:          80–120px, weight 900
Sub-label / descriptor:    34–46px, weight 300–400
Category / label caps:     22–28px, weight 700, letter-spacing 6–8
Body / byline:             18–24px, weight 400–600
```

### Content rules:
- Put every stat from the brief on the image — each gets a tile, bar, or hero position
- Tagline in footer area
- Handle (e.g. `@teachmebro`) rendered prominently in the footer — larger than the byline, styled in the accent color so it draws the eye. Place it between the tagline and the author name.
- Author + domain in byline (smaller, below the handle)
- **Never invent stats or claims not in the brief**
- **No company names, no internal tool names** unless the brief explicitly includes them
- **No emojis** unless the user explicitly asks
- Strip any private details — keep the lesson, drop the specifics

---

## Step 4 — Save and convert

1. Write the SVG to the output path from the brief.

2. Convert the SVG to PNG automatically using Bash:
   - The PNG goes into an `exports/` subfolder next to the SVG. Create it if it doesn't exist.
   - PNG filename mirrors the SVG filename: `impact-1.svg` → `exports/impact-1.png`
   - Run:
     ```bash
     # Install librsvg if missing (silent if already installed)
     which rsvg-convert > /dev/null 2>&1 || brew install librsvg -q
     mkdir -p <post-folder>/exports
     rsvg-convert -w <W> -h <H> <output.svg> -o <post-folder>/exports/<filename>.png
     ```
   - If `rsvg-convert` fails for any reason, note the error in the surface block but do not halt — the SVG is the primary output.

3. Print this surface block:

```
[IMAGE GENERATED]
Style: <style name used>
Inspired by: agents/image-gen/inspiration/<folder>/sample.<ext>
Dimensions: <W>×<H> (<format name: Portrait | Square | Landscape>)
SVG: <output path>
PNG: <post-folder>/exports/<filename>.png
Carries: <comma-separated list: stats, tagline, byline elements on the image>
```

---

## Edge cases

- **No matching style in manifest:** Pick the closest by mood tags. State the mismatch in the surface block. Suggest adding a new style to the library.
- **Stat-heavy brief, editorial channel (or vice versa):** Blend styles — note the blend in the surface block.
- **Missing brief field:** If a required field is absent (stats, tagline, author), ask before generating. Don't invent placeholder values that might end up in the published image.
- **User drops a new inspiration file without updating MANIFEST.md:** Read it anyway if pointed to directly; suggest they add it to the manifest after.

---

## Shared rules

- Never invent statistics, quotes, or claims not in the brief
- No emojis unless explicitly asked
- No company names or internal tool names in output unless the brief explicitly includes them
- Every generated SVG is saved to the output path AND surfaced in the conversation
- Authenticity over polish — a real specific detail beats a smooth generic one
