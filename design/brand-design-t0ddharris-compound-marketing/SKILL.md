---
name: brand-design
version: 2.0.0
description: "When the user wants to create visual creative assets — LinkedIn ads, carousel images, social graphics, banners, display ads, presentation slides, or any visual marketing content. Also use when the user mentions 'design,' 'creative,' 'ad image,' 'carousel,' 'banner,' 'social graphic,' 'slide,' 'visual asset,' 'LinkedIn ad,' or 'display ad.' This skill ensures all visual output follows the brand system."
---

# Brand Design

You are an expert brand designer creating on-brand visual assets for the company. Every asset you produce must follow the brand system defined in `/brain/brand-guide/brand-guide.md`.

**Scope boundary — use `web-design` instead when:** the task is live interactive web UI — framework landing pages, HubSpot landing pages, hover/focus/responsive states, motion, accessibility, page audits, or polishing shipped web pages. This skill covers *static* creative assets only (ads, carousels, banners, slide graphics, whitepaper PDFs). If someone asks to "build," "audit," "critique," or "polish" a shipped web page, stop and load `web-design`.

## Before Designing

**Always read the brand guide first:**
Read `/brain/brand-guide/brand-guide.md` to load the full color palette, typography, gradients, spacing, and component patterns. **Every color, font, radius, and spacing value in this skill comes from that file** — this skill defines production patterns, the brand guide supplies the values. If the brand guide is missing or still has `[FILL IN]` placeholders, stop and suggest running `/design-extract` (from a website) or filling it manually before producing assets.

**Check approved design references if the brand guide lists any:**
If the brand guide records a Figma reference file or an approved-designs folder (e.g., `marketing/assets/`), pull current approved designs before creating new assets so your work extends the existing system rather than inventing a parallel one. Skip anything marked archived.

**If the asset includes product claims or copy:**
Read `/brain/truth.md` and `/brain/positioning-and-messaging.md` to ensure accuracy. Never invent product facts.

Gather this context (ask if not provided):

### 1. Asset Type
- What are you creating? (LinkedIn ad, carousel, banner, social graphic, presentation slide, other)
- What are the dimensions / format requirements?

### 2. Purpose & Platform
- Where will this be used? (LinkedIn feed, LinkedIn ad, Twitter/X, blog header, website, presentation)
- What is the goal? (awareness, clicks, engagement, lead gen)

### 3. Content
- What is the primary message or headline?
- Any supporting text, data points, or proof points?
- Should it include a CTA? What action?
- Any specific imagery, icons, or illustrations needed?

### 4. Variations
- How many variations or sizes needed?
- A/B testing versions?

---

## Brand System Reference

**Do not redefine brand system values here.** Colors, typography, gradients, buttons, tags, cards, and spacing live in `/brain/brand-guide/brand-guide.md` and that file is authoritative.

When building assets, load the brand guide's values into CSS custom properties so the patterns below stay reusable:

```css
:root {
  --canvas: /* primary background from brand guide */;
  --surface: /* card/surface color from brand guide */;
  --border: /* default border color from brand guide */;
  --text-primary: /* primary text color from brand guide */;
  --text-secondary: /* supporting text color from brand guide */;
  --text-muted: /* tertiary/meta text color from brand guide */;
  --accent: /* primary accent color from brand guide */;
  --accent-2: /* secondary accent, if the brand has one */;
  --gradient: /* signature gradient, if the brand has one */;
  --font: /* brand font stack from brand guide */;
}
```

The non-negotiables, whatever the brand's values are:

- **One canvas.** Use the brand's primary background consistently. Don't drift between near-matches across assets.
- **One accent leads.** The brand guide defines the primary accent and any approved alternates (and when to use which). Don't promote a secondary color to primary because it looks nice on one asset.
- **Gradients (if the brand has them) are used by purpose.** The brand guide defines where each gradient variant is allowed (text effects vs. decorative surfaces). Never invent new gradient stops or apply a text-only gradient to borders and backgrounds.
- **The brand font, at the brand's weights.** Load it properly (Google Fonts import or local files per the brand guide). No substitutions in final assets.
- **Component patterns come from the brand guide.** Tags, buttons, and cards each have defined variants — use those, don't design new ones per asset.

### Production patterns (generic, brand-agnostic)

These patterns are specific to creative asset production and work with any brand's values:

**Card-internal labels (plain text).** When labeling items inside a card (e.g., pillar names, feature names), use plain bold uppercase text in the accent color — not pills or tags. This maintains hierarchy: tags = section level, plain text = card level.

```css
.card-label {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent);
}
```

**Short accent bars (diagram / small-card indicator).** For diagrammatic cards (smaller radius than the brand's standard card), use a short accent bar (3px × 24px) on the left edge via `::before`, not a full-height left border.

```css
.diagram-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 24px;
  position: relative;
}

.diagram-card::before {
  content: '';
  position: absolute;
  top: 16px;
  left: 0;
  width: 3px;
  height: 24px;
  border-radius: 0 2px 2px 0;
  background: var(--accent); /* or --accent-2 for semantic variation */
}
```

Use the brand guide's standard card spec for any card that represents a real product/feature; reserve the diagram card for small schematic elements.

**Flow elements (connected strip).** For sequential flows (A → B → C), use a single card container with items and arrows inside — no individual borders between items.

```css
.flow {
  display: flex;
  align-items: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
}

.flow-item {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
  padding: 12px 24px;
}

.flow-arrow {
  font-size: 14px;
  color: var(--accent);
  padding: 12px 14px;
}
```

**Gradient or accent text (headline emphasis).** If the brand guide defines a text-effect gradient, apply it to emphasis words in headlines via `background-clip: text` — and only where the brand guide allows. If the brand has no gradient, use the accent color for emphasis words instead.

```css
.tagline strong {
  font-weight: 700;
  background: var(--gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

**Blockquote / capstone lines.** For italic summary lines or pull quotes, use a subtle left border.

```css
.capstone {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  font-style: italic;
  line-height: 155%;
  padding-left: 16px;
  border-left: 2px solid var(--border);
}
```

---

## Design Principles

### Contrast & Hierarchy
Use contrast against the canvas to guide the eye:
1. Accent/gradient or highest-contrast text — highest priority (headline)
2. Primary text — main information
3. Secondary text — supporting information
4. Muted text — tertiary/meta information

### Restraint
Accents are powerful because they're used sparingly. A single accented headline against a clean canvas is more impactful than accent everywhere.

### Breathing Room
Use generous spacing. Don't crowd elements. Negative space reads as premium, not empty.

### Consistency Over Novelty
Match the brand's existing patterns (website, approved assets). Don't introduce new visual ideas that diverge from the established system. The goal is brand coherence, not creative exploration.

---

## Asset Type Guidelines

### LinkedIn Ads (Single Image)
- **Recommended sizes:** 1200x627px (landscape), 1080x1080px (square)
- Keep headline to 5-8 words max
- One clear CTA
- Logo in corner (use the logo variant that contrasts with your canvas — the brand guide lists available logo files)
- High contrast — these compete in a busy feed

### LinkedIn Carousel
- **Size:** 1080x1080px (square, recommended) or 1080x1350px (portrait) per slide
- **Slide 1 (Hook):** Bold headline with accent treatment, minimal copy
- **Middle slides:** One idea per slide, consistent layout
- **Final slide:** CTA slide with clear next step
- Maintain consistent header/footer elements across slides
- Use slide numbers or progress indicator
- Keep text concise — short statements and key points, not paragraphs
- **Safe zone:** Keep text away from edges (minimum 48px padding) to prevent mobile crop

**LinkedIn Carousel Font Size Minimums (1080x1080):**

| Element | Minimum Size | Recommended Range | Weight |
|---------|-------------|-------------------|--------|
| Headlines / Titles | 48px | 48–72px | 600 |
| Body text | 36px | 36–48px | 400 |
| Supporting text / descriptions | 28px | 28–36px | 400 |
| Captions / footnotes / labels | 27px | 27–32px | 400–500 |
| Buttons / CTAs | 28px | 28–36px | 500 |
| Meta info (slide numbers, tags) | 24px | 24–28px | 500 |

**Hard rule:** Never go below 24px for any text on a 1080x1080 carousel slide. These are viewed on mobile phones — small text becomes unreadable. When in doubt, go larger and cut words instead.

### Social Graphics (LinkedIn/Twitter Posts)
- **Size:** 1200x627px (LinkedIn), 1200x675px (Twitter)
- Support the post copy — don't duplicate it
- Data visualizations, diagrams, or key stat callouts work well
- Brand the image but don't over-logo it

### Event Social Cards (Speaker / Sponsorship Promos)

A proven pattern for promoting company presence at industry events. Store finished cards in `marketing/assets/social-cards/[event-name]/` so future events can extend the set.

**Size:** 1200x627px (landscape, works on both LinkedIn and X)

**Layout (two-column, ~65/35 split):**

```
┌──────────────────────────────────────────────────────────┐
│  [Event Logo]                    [Company Logo]          │
│                                  SPONSOR TIER            │
│                                                          │
│  Catch our Keynote Session - [Date] @ [Time]             │
│                                                          │
│  Session Title:                    ┌─────────┐           │
│  Subtitle in Italic                │  Photo  │           │
│  Across Multiple Lines             └─────────┘           │
│                                   Speaker Name           │
│  EVENT NAME (uppercase, muted)    Title                  │
│  Date · Location                  SPEAKER ROLE           │
└──────────────────────────────────────────────────────────┘
```

**Background:** Use a branded background from `brain/brand-guide/` or an approved background asset if one exists. Good variants range from vibrant (gradient + ghosted brand mark) to restrained (dark/solid with a subtle accent glow). Match the energy to the message.

**Top band (co-branding):**
- Event logo (official event branding, not just text) — top left
- Company logo — top right
- Sponsor tier (e.g., "GOLD SPONSOR"), if applicable, in the accent color, uppercase, small, directly below the company logo

**Session intro line:**
- Conversational tone: "Catch our **Keynote Session** - [Date] @ [Time]"
- The session type in bold primary text; the rest in regular weight secondary text
- This line bridges the logos above and the session title below

**Session title (visual hero):**
- Main title in bold (weight 700), primary text color
- Subtitle/description in *italic* (weight 400 italic) — the italic differentiates title from description without a second color
- Largest text on the card, ~36-42px equivalent at 1200px width

**Event details (muted):**
- Event name in uppercase, muted text color, weight 600
- Date + location below in lighter weight, separated by a center dot (·)

**Speaker section (right column):**
- Circular headshot crop with a solid accent border ring (2-3px)
- Vignette/blend the headshot edges into the card background if the original photo has a clashing background
- Speaker name in primary text, weight 600, ~18-20px
- Title (e.g., "Co-founder & CTO") in secondary text, weight 400, ~13-14px
- Role label (e.g., "KEYNOTE SPEAKER") in the accent color, uppercase, weight 600, letter-spacing, ~10-11px

**Typography notes for event cards:**
- Brand font throughout
- Session title is the dominant text element; logos and speaker name are secondary
- Generous line spacing on the session title (1.15-1.2 line-height)

### Display / Banner Ads
- Follow IAB standard sizes as requested
- Extreme economy of words — 3-5 words headline max
- Logo, headline, CTA — that's it
- Ensure the brand accent is visible even at small sizes

### Blog / Content Headers
- **Size:** 1200x630px (standard OG image size)
- Topic-relevant but on-brand
- Title overlay should be legible
- Consistent treatment across the blog for series recognition

### Presentation Slides
- **Size:** 1920x1080px (16:9)
- **Background:** the slide background from the brand guide (brands often use a slightly different value than the web canvas — check)
- High-contrast headline treatment per the brand guide
- One idea per slide
- Use the brand's card pattern for content blocks
- Data and diagrams should use brand accent colors

---

## Output Format

**Output location:** `marketing/design/[asset-slug]/` — confirm the project slug with the user before creating files.

### For Each Asset, Provide:

**1. HTML/CSS Implementation**
Generate production-quality HTML/CSS that can be:
- Screenshotted directly for use
- Rendered in a browser at exact dimensions
- Easily modified for variations

Use inline styles or a `<style>` block. Include:
- Exact dimensions with `width` and `height`
- The brand font loaded properly (import or local files per the brand guide)
- All brand colors by their exact values from the brand guide (no approximations)
- The brand's signature accent/gradient where appropriate

**2. Design Rationale**
Brief notes on:
- Why you made key layout/emphasis choices
- Which brand elements you applied and why
- Any trade-offs or alternatives considered

**3. Variations (if requested)**
- A/B headline variations
- Different emphasis treatments
- Size adaptations

### Code Quality Standards

- Use semantic HTML
- All text must be real text (not images of text) for easy editing
- Load the brand font via `@import` or `@font-face`
- Set `box-sizing: border-box` globally
- Use flexbox/grid for layout
- Add comments marking editable sections (headlines, body copy, CTA text)

---

## Checklist Before Delivering

- [ ] Read `/brain/brand-guide/brand-guide.md`
- [ ] Canvas color matches the brand guide exactly
- [ ] Brand font loaded and applied at the brand's weights
- [ ] Colors match brand palette exactly (no approximations)
- [ ] Gradients/accents used only where the brand guide allows them
- [ ] Spacing follows the brand scale
- [ ] Border radius matches brand patterns
- [ ] Text hierarchy is clear (accent/primary → secondary → muted)
- [ ] Any product claims verified against `/brain/truth.md`
- [ ] Asset dimensions match the target platform
- [ ] Logo included where appropriate (correct variant for the background)
- [ ] Readable at actual display size (especially mobile)
- [ ] Font sizes meet platform minimums (e.g., no text below 24px on carousel slides)
- [ ] No AI slop patterns in any copy (see CLAUDE.md)
- [ ] **Visual QA passed** — ran spatial checks via `agent-browser eval` (centering, alignment, even spacing, connector endpoints)

---

## MCP Tools: Figma & agent-browser

### Figma MCP (Design Input)

When the user provides a Figma URL or references a Figma design (and the Figma MCP server is connected):

1. **Pull design context** — Use `mcp__figma-remote-mcp__get_design_context` to extract layout, colors, typography, and spacing from the Figma node. Use this to match the design exactly when building HTML/CSS.
2. **Take a screenshot** — Use `mcp__figma-remote-mcp__get_screenshot` to see the visual design before translating it to code.
3. **Get design variables** — Use `mcp__figma-remote-mcp__get_variable_defs` to pull color tokens, spacing values, and other design variables defined in the Figma file.
4. **Generate design system rules** — Use `mcp__figma-remote-mcp__create_design_system_rules` to produce a design system reference for the repo.
5. **Get metadata** — Use `mcp__figma-remote-mcp__get_metadata` to get an overview of the node structure (layer names, sizes, positions) before pulling full design context.

**When to use:** Whenever the user shares a Figma link, says "match this design," or wants to translate a Figma mockup into HTML/CSS creative assets. If the brand guide records a canonical Figma reference file, check it for approved styles before designing from scratch.

### agent-browser (Visual Validation)

After generating HTML/CSS assets, use agent-browser to validate rendering:

1. **Open the asset** — Run `agent-browser open <file-or-url>` to open the HTML file or a local server URL.
2. **Take a screenshot** — Run `agent-browser screenshot` to capture the rendered asset at exact dimensions. Compare against the reference design if one exists.
3. **Test at different sizes** — Run `agent-browser set viewport <width> <height>` to test the asset at different viewport sizes (e.g., 1080x1080 for carousel, 1200x627 for LinkedIn ad, 1920x1080 for presentation).
4. **Accessibility snapshot** — Run `agent-browser snapshot -i` to check text contrast and element structure.

**When to use:** After building any HTML/CSS creative asset — validate before delivering. Especially useful for carousel slides (check each slide), responsive assets, and ads that need to hit exact pixel dimensions.

### Visual QA (Layout Precision)

After taking a screenshot, run a **spatial quality check** using `agent-browser eval` to programmatically measure element positions. This catches alignment and spacing issues that are hard to spot visually but obvious when measured.

**What to check:**

1. **Centering** — Elements that should be centered within their parent must be within 2px of true center (both horizontal and vertical).
2. **Horizontal alignment** — Elements in the same visual row should share the same `top` value (within 2px tolerance).
3. **Vertical alignment** — Elements in the same visual column should share the same `left` value (within 2px tolerance).
4. **Even spacing** — Repeated elements (e.g., logo rows, badge groups, card grids) should have equal gaps between them. Measure the gap between each consecutive pair and flag if any gap differs from the others by more than 4px.
5. **Connector endpoint clearance** — Arrow/line endpoints must NOT overlap or touch the element boxes they connect. SVG marker arrowheads extend beyond the line endpoint by ~8px in the arrow direction. If a line endpoint sits exactly on an element's edge, the arrowhead will visually bleed into the box. **Fix:** Pull each endpoint at least 8px away from the nearest element edge (measure along the arrow direction). Use `getBoundingClientRect()` on both the element and the SVG coordinate mapping to verify. Convert SVG viewBox coordinates to screen coordinates using `svgRect.width / viewBoxWidth` scaling.
6. **Label proximity to its arrow/element** — Arrow labels must be positioned close to and clearly associated with the arrow or element they describe. A label more than 20px from its associated arrow line, or more than 40px from its associated element, is misplaced. For diagram arrow labels, verify the label sits within 20px of the arrow's path (not floating in empty space above/below). If a label is closer to a different arrow or element than its intended one, it is misplaced.
7. **Container boundary breathing room** — Elements inside a dashed or solid container (namespace, zone, group box) must have at least 20px of clear space from the container's inner edges on all sides. An element flush against a container border looks cramped and sloppy. Measure each element's distance from its container's top, right, bottom, and left inner edges. Flag any gap under 20px.
8. **Symmetry** — If the layout is visually symmetric (e.g., two boxes flanking a center), verify their distances from center are equal within 4px.
9. **Text vs ALL lines (critical)** — Text labels must never overlap or touch ANY line in the diagram — this includes structural borders (zone dividers, container edges), SVG arrow paths (horizontal, vertical, and diagonal), and dashed connector lines. For every text label, check its bounding box against:
   - **Structural lines:** zone dividers, namespace/container borders (dashed or solid), host borders. Use the known Y (or X) position of each line.
   - **SVG arrow paths:** For horizontal arrows, check if the label's X range overlaps the arrow's X range AND the label's Y range is within 8px of the arrow's Y. For vertical arrows, check if the label's Y range overlaps the arrow's Y range AND the label's X range is within 8px of the arrow's X. For diagonal arrows, compute the arrow's Y at the label's X position (linear interpolation) and check if the label's Y range is within 8px.
   - **Minimum clearance: 8px** between any edge of a text label and any line. If closer, move the label clearly away (12px+ preferred).
   - This is the single most common visual defect in diagram work — always check it.
10. **Mirror-distance labels** — When two labels flank a divider or boundary line (one above, one below), they must be equidistant from that line. Measure the gap from each label's nearest edge to the line. If the gaps differ by more than 4px, flag it and adjust so both gaps match. This applies to any pair of labels that mirror each other across a horizontal or vertical rule (e.g., "loads" above a zone divider and "sends" below it).
11. **Zone label consistency** — When a layout has multiple zones separated by dividers or borders (e.g., "Userspace" / "Kernel"), each zone label must have the same distance from its nearest boundary (top border, divider, or bottom border). Measure each zone label's gap from the edge it "belongs to" — if they differ by more than 4px, flag it. For example, if one zone label is 16px below the divider, the other zone's label must be ~16px below the top border of its container.

**How to run the check:**

Use `agent-browser eval` with a script that:
1. Queries all key elements by class or data attribute
2. Calls `getBoundingClientRect()` on each
3. Computes center points, gaps, and alignment offsets
4. Returns a report of any violations

Example — text-vs-lines check (adapt selectors and line coordinates to your diagram):
```js
() => {
  const issues = [];
  const host = document.querySelector('.host');
  const hr = host.getBoundingClientRect();

  // 1. Define ALL lines in the diagram (structural + SVG arrows)
  const structLines = [
    { name: 'zone-divider', y: 430 },       // horizontal structural line
    { name: 'namespace-bottom', y: 415 },    // dashed container border
  ];
  const arrowLines = [
    { name: 'service-a→queue', y: 500, x1: 590, x2: 660 },   // horizontal SVG arrow
    { name: 'agent→collector', y: 344, x1: 680, x2: 790 },
  ];

  // 2. Check every text label against every line
  document.querySelectorAll('.arrow-label').forEach(el => {
    const r = el.getBoundingClientRect();
    const name = el.textContent.trim();
    const top = Math.round(r.top - hr.top);
    const bottom = Math.round(r.bottom - hr.top);
    const left = Math.round(r.left - hr.left);
    const right = Math.round(r.right - hr.left);

    // Check vs structural lines (full-width)
    for (const line of structLines) {
      const crosses = (top < line.y && bottom > line.y);
      const minDist = Math.min(Math.abs(top - line.y), Math.abs(bottom - line.y));
      if (crosses || minDist < 8)
        issues.push(`"${name}" ${crosses ? 'CROSSES' : minDist+'px from'} ${line.name}`);
    }
    // Check vs horizontal SVG arrows (only if X ranges overlap)
    for (const arrow of arrowLines) {
      if (right > arrow.x1 && left < arrow.x2) {
        const crosses = (top < arrow.y && bottom > arrow.y);
        const minDist = Math.min(Math.abs(top - arrow.y), Math.abs(bottom - arrow.y));
        if (crosses || minDist < 8)
          issues.push(`"${name}" ${crosses ? 'CROSSES' : minDist+'px from'} ${arrow.name}`);
      }
    }
  });
  return issues.length ? issues : 'All labels clear of lines';
}
```

**When to run:** After every design asset is rendered in the browser — before taking the final screenshot and before delivering to the user. Fix any issues found before declaring the asset done.

**Tolerance thresholds:**
| Check | Tolerance |
|-------|-----------|
| Centering | 2px |
| Alignment (shared edge) | 2px |
| Even spacing | 4px |
| Connector endpoint clearance | Arrowhead must be ≥ 8px clear of element edge (never overlap boxes) |
| Label-to-arrow proximity | Label must be ≤ 20px from its arrow path |
| Label-to-element proximity | Max 40px from associated element |
| Container breathing room | Elements must be ≥ 20px from container inner edges |
| Text vs lines (structural + SVG arrows) | Labels must be 8px+ clear of ALL lines (borders, dividers, arrow paths) |
| Mirror-distance labels | Gap difference ≤ 4px from shared divider |
| Zone label consistency | Gap difference ≤ 4px between matching zone labels |

---

## Post-Processing: Background Color Enforcement

AI image generators (Gemini, etc.) often add subtle gradients, glow, or vignettes to backgrounds even when instructed not to. When an asset requires an **exact background color** (e.g., your brand's slide or web canvas), use this PIL script to force every near-background pixel to the target color after generation.

**When to use:** After any AI-generated image that must sit on a specific brand background. Also useful for compositing generated illustrations onto slide decks or web pages where color mismatch would be visible.

The script below targets dark canvases (the threshold catches near-black pixels). For light canvases, invert the comparison (`r > threshold and g > threshold and b > threshold` with a threshold around 200).

```python
from PIL import Image

def enforce_background_color(input_path, output_path, target_rgb, threshold=60):
    """
    Replace all near-dark pixels with an exact background color.

    Args:
        input_path: Path to the source image
        output_path: Path to save the processed image
        target_rgb: The exact background color as (R, G, B) — use your brand
                    guide's canvas value, e.g. (18, 18, 18) for #121212
        threshold: Pixels where R, G, and B are ALL below this value get replaced.
                   Default 60 catches dark backgrounds without touching colored elements.
                   Lower (e.g., 40) for tighter replacement; higher (e.g., 80) for more aggressive.
    """
    img = Image.open(input_path).convert("RGB")
    pixels = img.load()
    w, h = img.size
    replaced = 0
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            if r < threshold and g < threshold and b < threshold:
                pixels[x, y] = target_rgb
                replaced += 1
    img.save(output_path)
    print(f"Replaced {replaced:,} pixels → rgb{target_rgb} in {output_path}")

# Usage: pass your brand guide's exact canvas values
# enforce_background_color("input.png", "output.png", target_rgb=(18, 18, 18))
# enforce_background_color("input.png", "output.png", target_rgb=(18, 18, 18), threshold=40)  # tighter match
```

Look up the exact RGB values for your web canvas, slide background, and card surfaces in `/brain/brand-guide/brand-guide.md` before running.

---

## Icons: Use Libraries First, Custom Second

**Never hand-draw SVG icons when an open-source icon library has what you need.** Check these libraries first — they have thousands of professionally designed, consistent icons:

1. **Lucide Icons** (ISC license) — https://lucide.dev/icons/ — Preferred. Clean thin-line style.
2. **Tabler Icons** (MIT) — https://tabler.io/icons — 5000+ icons.
3. **Phosphor Icons** (MIT) — https://phosphoricons.com — Has a "thin" weight.

**Workflow:**
- Search the library for the concept you need
- Fetch the SVG from unpkg: `https://unpkg.com/lucide-static@latest/icons/{name}.svg`
- Adapt to brand colors (accent-color stroke) and scale to fit the target viewBox
- Only create custom SVG icons when no library icon fits the concept

**To embed a Lucide icon in a 120x120 viewBox:**
```svg
<g transform="translate(10, 10) scale(4.2)" stroke="var(--accent)" stroke-width="0.36" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <!-- paste Lucide path data here -->
</g>
```
(Replace `var(--accent)` with the literal accent hex when the SVG is used standalone outside a page with the custom property defined.)

---

## Multi-Page Document Design (Whitepapers, Datasheets)

When asked to design a whitepaper, datasheet, or other multi-page branded document:

### Workflow: HTML First, Figma Second

1. **Build as HTML/CSS** — Design the full document as a multi-page HTML file with brand styling. Use all the brand system rules from the brand guide (canvas, typography, accents, card patterns, spacing scale). Structure the HTML with explicit page breaks via `page-break-after: always` or separate page divs.

2. **Export to PDF** — Use the `html-to-pdf` skill to export a print-quality vector PDF via Playwright. This gives selectable text, exact colors, and crisp rendering at any zoom.

3. **Push to Figma for editing (optional)** — If the Figma MCP server is connected, use `mcp__figma-remote-mcp__generate_figma_design` to capture the HTML page into Figma. This imports the design as a visual reference that the team can annotate, adjust, or polish in Figma's editor.

### Why Not Build Directly in Figma?

Figma plugin APIs can create objects programmatically, but multi-page documents with complex typography, diagrams, pull quotes, and brand styling require hundreds of lines of JS per page. The results are functional but not designer-polished. HTML/CSS gives us:
- Full control over typography, spacing, and layout
- Reusable brand CSS patterns
- Print-quality PDF export (vector, selectable text)
- A source file we can version-control and iterate on

Figma's strength is collaborative visual editing, not document authoring. Use it as the refinement layer, not the production layer.

### Document Design Standards

- **Page size:** Match the target output (e.g., 8.5"x11" letter, A4). Set HTML body dimensions to the DPI-scaled equivalent.
- **Margins:** Generous margins (minimum 0.75" on all sides for print safety).
- **Headers/footers:** Consistent placement with the company logo, page numbers, and document title.
- **Section breaks:** Use the brand accent as a subtle section divider (thin line or text accent), not a full bar.
- **Pull quotes:** Use the capstone/blockquote pattern from the brand system.
- **Diagrams:** Build inline as SVG or styled HTML, not as image embeds. This keeps them vector-sharp in PDF.
- **Cover page:** Full-bleed brand canvas with an accented headline, subtitle, date, and company logo.

---

## Related Skills

- **copywriting**: For the copy/messaging that goes into the asset
- **social-content**: For social media post copy that accompanies the visual
- **paid-ads**: For ad campaign strategy and targeting context
- **copy-editing**: For reviewing copy within the asset
- **html-to-pdf**: For exporting HTML documents to print-quality vector PDFs
- **long-form**: For whitepaper and datasheet content drafting (Phase 1)

## Learnings

<!-- Updated by /reflect in your instance. Promote stable patterns to the main skill body. Ships empty. -->
