---
name: logo-design
description: |
  Creates SVG logos with scalable geometry, color theory, and variant generation. Use when designing logos, icons, or brand marks, generating favicons or social avatars, or reviewing a logo for scalability, color, or variant coverage.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-logo-design
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: design
---

# Logo Design

## Intro

A good logo is simple, memorable, timeless, versatile, and
appropriate to its audience. Build it as clean SVG geometry, limit
color to 2-3 hues, and ship the full set of variants (full, mark,
favicon, monochrome, reversed) before calling it done.

## Overview

### Design principles

- **Simplicity:** recognizable at 16x16 (favicon size).
- **Memorability:** one distinctive element anchors recognition.
- **Timelessness:** avoid trendy gradients and shadows that date
  quickly.
- **Versatility:** must work in color, monochrome, reversed, and at
  every size.
- **Appropriateness:** style matches the brand personality and
  audience.

### SVG construction

Build logos from clean geometric shapes (`<circle>`, `<rect>`,
`<path>`). Define the design space with `viewBox` (e.g. `viewBox="0 0
100 100"`) and omit `width` and `height` for fluid scaling. Optimize
paths by minimizing control points and trimming unnecessary
precision. Use `<g>` groups with meaningful IDs such as `id="mark"`
and `id="wordmark"`. Center the design in the viewBox with breathing
room at the edges.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <g id="mark">
    <!-- Logo mark paths -->
  </g>
  <g id="wordmark">
    <!-- Text elements (convert to paths for distribution) -->
  </g>
</svg>
```

### Color theory

| Scheme | Description | Use Case |
|---|---|---|
| **Monochromatic** | Shades of one hue | Elegant, cohesive |
| **Complementary** | Opposite on color wheel | High contrast, energetic |
| **Analogous** | Adjacent hues | Harmonious, natural |
| **Triadic** | Three equally spaced hues | Vibrant, balanced |
| **Split-complementary** | Base + two adjacent to complement | Contrast with less tension |

Limit a logo to 2-3 colors, ensure 4.5:1 contrast against both white
and dark backgrounds, choose colors that reproduce well in CMYK
(print) and RGB (screen), and test for colorblind safety (avoid
red/green as the only differentiator).

### Typography in logos

Pick fonts that reflect brand personality (geometric feels modern,
serif feels traditional). Modify letterforms for uniqueness via
custom ligatures and adjusted spacing. Convert text to paths for
distribution so the logo does not depend on font files. Maintain
consistent optical (visual, not mathematical) kerning. Ensure
readability at small sizes — avoid thin strokes and tight spacing.

### Variants to generate

Every logo ships as a set of variants:

| Variant | Size/Format | Use Case |
|---|---|---|
| **Full logo** | SVG, any size | Website header, documents |
| **Icon/mark only** | SVG, square | App icon, social avatar |
| **Favicon** | 32x32, 16x16 | Browser tab |
| **Monochrome** | SVG, single color | Printing, watermarks |
| **Reversed** | SVG, light on dark | Dark backgrounds |
| **Social banner** | 1200x630 | Open Graph / social sharing |

### Testing and validation

- Render at 16px, 32px, 180px, and 512px — verify recognizability at
  every size.
- Test on white, black, and colored backgrounds.
- Convert to grayscale and check the mark remains distinct.
- Simulate deuteranopia and protanopia for colorblind safety.
- Print a black-and-white test page to check single-color
  reproduction.
- Compare side-by-side with competitors to confirm distinctiveness.

### Common mistakes

- Too many details that disappear at small sizes.
- Text not converted to paths (font dependency).
- Colors that clash with common UI backgrounds.
- Overly complex paths that bloat file size.
- No monochrome variant (needed for single-color printing).
- Raster effects (drop shadows, blur) embedded in SVG.
- Trendy gradients or shadows that date the logo quickly.
- Missing reversed (light-on-dark) variant for dark mode.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Leaving text as `<text>` elements in the distribution SVG.** Text elements depend on the font being installed on the viewer's system. If the font is not available, the wordmark renders in a fallback typeface and breaks the intended design. Always convert text to paths before delivering a logo SVG.
- **Delivering only the color variant.** A logo used on dark backgrounds, in single-color print, or as a browser favicon requires dedicated variants. The minimum set is: full color, monochrome, reversed, and favicon. Delivering one variant forces the client to improvise — usually badly.
- **Embedding raster effects (drop shadows, blur) in the SVG.** SVG filters are renderer-dependent and often look different across browsers; they also fail to scale and print cleanly. Logos must be built from clean vector geometry only.
- **Not verifying legibility at favicon scale.** A logo that reads well at 512px may become an indistinct blob at 16×16px. Test at 16px, 32px, and 512px before delivering. Simplify until the mark is distinct at the smallest size.
- **Including `width` and `height` attributes on the root SVG element.** Fixed pixel dimensions prevent the logo from scaling to its container. Set only `viewBox` on the root element; omit `width` and `height` so the logo scales fluidly.
- **Choosing colors for RGB screens without verifying CMYK reproduction.** Brand colors selected purely for screen display may shift significantly when converted to CMYK for print. For any logo intended for print, verify that the chosen colors have acceptable CMYK equivalents before finalizing.
- **Using red and green as the only differentiators.** Approximately 8% of men cannot distinguish red from green. A mark whose meaning depends on this distinction is invisible to a significant share of the audience. Always verify colorblind safety before finalizing a palette.

## Full reference

### The five principles expanded

**Simple:**

- Can be described in one sentence.
- Uses 2-3 colors maximum.
- Relies on basic geometric forms.
- Recognizable at a glance (under 2 seconds).
- Test: can you draw it from memory?

**Memorable:**

- One distinctive element that anchors recognition.
- Avoid generic symbols (globes, swooshes, abstract circles).
- Negative-space tricks create lasting impressions (FedEx arrow, NBC
  peacock).
- Unique enough to avoid confusion with competitors.

**Timeless:**

- Avoid trends: flat design today is the dated look of tomorrow.
- Classic logos survive decades (Apple, Nike, Mercedes).
- If you must follow a trend, isolate it so it can be updated
  without redesigning.
- Test: would this look dated in 10 years?

**Versatile** — must work without modification in:

- Large format: billboards, banners.
- Small format: favicon (16x16), app icon (1024x1024).
- Color: full color on white, on dark, on colored backgrounds.
- Monochrome: single color (black, white, or any brand color).
- Print: CMYK, embossing, engraving, single-color printing.

**Appropriate:**

- Style matches audience expectations (playful vs. professional).
- Color psychology aligns with brand values.
- Does not unintentionally resemble other brands or inappropriate
  imagery.
- Works across cultures if the brand is international.

### Color psychology quick reference

| Color | Associations | Industries |
|---|---|---|
| Blue | Trust, stability, technology | Finance, tech, healthcare |
| Red | Energy, urgency, passion | Food, entertainment, sports |
| Green | Growth, nature, health | Organic, finance, environment |
| Yellow | Optimism, warmth, caution | Retail, food, children |
| Purple | Luxury, creativity, wisdom | Beauty, education, luxury goods |
| Orange | Friendliness, confidence | Tech, food, youth brands |
| Black | Sophistication, power | Luxury, fashion, tech |
| White | Clean, minimal, pure | Tech, healthcare, luxury |

### SVG optimization checklist

1. Remove editor metadata (Inkscape, Illustrator comments).
2. Minimize decimal precision (2 decimal places usually enough).
3. Use relative path commands where shorter (`l` vs `L`).
4. Combine overlapping shapes where possible.
5. Remove hidden elements and unused definitions.
6. Optimize with SVGO: `svgo --multipass input.svg -o output.svg`.
7. Verify rendering after optimization.

### Favicon generation sizes

| Size | Purpose |
|---|---|
| 16x16 | Browser tab (legacy) |
| 32x32 | Browser tab (standard) |
| 48x48 | Windows taskbar |
| 180x180 | Apple Touch Icon |
| 192x192 | Android Chrome |
| 512x512 | Android Chrome splash |

Prefer a single SVG favicon where supported:

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
```

### Responsive logo system

A complete system includes multiple lockups for different contexts:

| Lockup | Description | Where Used |
|---|---|---|
| **Primary** | Full mark + wordmark | Website header, letterhead |
| **Horizontal** | Mark left, text right | Navigation bars, email signatures |
| **Stacked** | Mark above text | Social media, documents |
| **Icon only** | Mark without text | App icon, favicons, small spaces |
| **Wordmark only** | Text without mark | When the mark is already visible |

Design the mark and wordmark as independent `<g>` groups in a single
SVG, then extract each lockup as a separate file.

### File deliverables

| Format | Purpose |
|---|---|
| SVG | Web, scalable, primary format |
| PNG (transparent) | Presentations, documents |
| PNG (with background) | Social media profiles |
| ICO | Windows favicon |
| PDF | Print-ready vector |

### References

- `references/design-principles.md` — source for the five principles,
  color psychology, optimization checklist, favicon sizes, lockup
  system, and deliverables table.
