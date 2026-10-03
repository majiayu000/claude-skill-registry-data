---
name: embedded-ui-svg-doc-from-source
description: |-
  Use when documenting an embedded device GUI (ESP32/Arduino touchscreens, LovyanGFX/TFT_eSPI/U8g2/LVGL screens) for end-user instructions, printable manuals, or design reviews — and the source code already contains the drawing calls (`gfx.fillRect`, `gfx.drawString`, `gfx.drawLine`, `tft.drawPixel`, `display.print`, LVGL-styles etc.). Trigger on phrases like "user manual for the display", "manual with mockups", "UI documentation for the ESP32 device", "printable manual for embedded UI", "screen mockups for the touchscreen", "display screenshots without hardware", "1:1 SVG from the source code", "tangible mockup". Do NOT load for web-frontend UI docs (use frontend-design or marketing), for CAD assembly drawings (use cad-construction), or when no source code with literal draw coordinates exists. This skill encodes the "measure, don't estimate" maxim (originally CAD) applied to embedded-UI documentation: translate the draw calls verbatim into SVG, do not rebuild semantically.
---

# Embedded-UI SVG Doc from Source

When the embedded device already draws its UI with literal pixel coordinates in code, **translate those coordinates 1:1 into SVG `<rect>/<text>/<line>` elements**. Do not rebuild the layout semantically with CSS — that path is lossy and produces 4-8 iterations of "wrong pill width", "wrong text offset", "wrong padding".

The maxim is the CAD principle applied to docs: **measure, don't estimate**. The source code IS the measurement.

## When to use

- Writing a printable end-user manual (PDF/HTML) for an embedded touchscreen device where the screen layouts must appear in the manual
- Producing design-review mockups when the device is not at hand
- Updating existing UI docs after a screen refactor in source — diff the draw calls, diff the SVG
- Onboarding a gifted-recipient with no software background (typical use case: a small embedded controller given to a hobbyist)

## When NOT to use

- Web-frontend mockups → use `frontend-design`, `marketing`, or `ui-ux-pro-max`
- Real photos of the device screen suffice → just photograph and embed; this skill is for the case where the hardware is not available or photos are awkward (glare, font rendering, parallax)
- LVGL with style objects only and no literal coordinates → harder; this skill assumes literal `x, y, w, h` in the source
- CAD or mechanical drawings → `cad-construction`

## The core translation pattern

| Source-Code Call (LovyanGFX / generic) | SVG Element |
|---|---|
| `gfx.fillRect(x, y, w, h, color)` | `<rect x="X" y="Y" width="W" height="H" fill="#color"/>` |
| `gfx.drawRect(x, y, w, h, color)` | `<rect ... fill="none" stroke="#color"/>` |
| `gfx.fillRoundRect(x, y, w, h, r, color)` | `<rect ... rx="R"/>` |
| `gfx.drawString("text", x, y)` | `<text x="X" y="Y" font-family="..." font-size="...">text</text>` |
| `gfx.drawLine(x1, y1, x2, y2, color)` | `<line x1="X1" y1="Y1" x2="X2" y2="Y2" stroke="#color"/>` |
| `gfx.fillCircle(cx, cy, r, color)` | `<circle cx="CX" cy="CY" r="R" fill="#color"/>` |
| `gfx.drawTriangle(x1,y1,x2,y2,x3,y3,color)` | `<polygon points="X1,Y1 X2,Y2 X3,Y3"/>` |

The SVG `viewBox` is the **display resolution**: `viewBox="0 0 800 480"` for an 800×480 panel, `viewBox="0 0 320 240"` for a CYD ESP32-2432S028. **Never invent your own coordinate system** — the source has the canonical one.

## Font scaling via container queries

To let the SVG scale proportionally inside an HTML manual (responsive print + screen), wrap each SVG in a container with `container-type: inline-size` and express font-sizes in `cqi`:

```css
.screen-mockup {
  container-type: inline-size;
  width: 100%;
  max-width: 800px;          /* matches display width */
  aspect-ratio: 800 / 480;   /* matches display */
}

/* 1cqi = 1% of container inline-size = 8 display-pixels at 800px-wide */
.screen-mockup svg text.label   { font-size: 2.0cqi; }  /* 16 display-px */
.screen-mockup svg text.heading { font-size: 4.0cqi; }  /* 32 display-px */
.screen-mockup svg text.numeral { font-size: 11.0cqi; } /* ~88 display-px, hero temp */
```

Then the same SVG looks identical at A4-print-size and at iPad-portrait — and stays in sync with the source resolution.

## Workflow

1. **Locate the screen source file**: usually `src/ui/screens/screen_<name>.cpp` (LovyanGFX convention) or equivalent. Search for `fillRect`, `drawString`, `gfx.*`, `display.*`, `tft.*`.
2. **Identify the helper functions** the screen calls — `drawCard()`, `drawPill()`, `drawButton()`, `drawTempDisplay()`. They're usually in `ui_components.h` or `ui_helpers.h`. Inline their drawing primitives too (a `drawPill(x, y, "Connected")` expands to `fillRoundRect` + `drawString`).
3. **Map the draw calls** to SVG elements in order. Each `fillRect` becomes a `<rect>`, each `drawString` becomes a `<text>`. Preserve z-order: code paints background first, then foreground.
4. **Set the viewBox** to display resolution. Add `xmlns="http://www.w3.org/2000/svg"` and `preserveAspectRatio="xMidYMid meet"`.
5. **Use design-token CSS classes** for fill/stroke instead of literal hex — match the device's color palette file (e.g. `colors_studio.h`). Then a palette swap in the device propagates to the doc with one CSS edit.
6. **Verify side-by-side**: open the rendered SVG next to the device (or a photo) — every pill, every line, every padding pixel must match. If anything is off, it means the draw call was different from what you wrote in SVG. Fix the SVG, not the device.
7. **Wrap in the printable HTML manual** with the cqi-scaling pattern above.

## Anti-patterns (v1-v4 mistakes recorded so we don't repeat)

- ❌ **Semantic CSS re-implementation**: building "a pill component" with `border-radius: 50px; padding: 8px 16px` based on screenshot intuition. Produces drift on every iteration — pill is too wide, then too narrow, then text is mis-centered.
- ❌ **Excalidraw / colored-box mockups**: "I'll sketch the layout" produces decorative placeholders that the user can't navigate. User feedback: "just colored boxes, no text" → discarded.
- ❌ **Trusting screen photos for size/position**: parallax, glare, lens distortion. Photo is good for color verification, not for measurement.
- ❌ **Inventing your own viewBox** (`viewBox="0 0 100 60"` because "easier to think in percentages") — kills the 1:1 mapping that makes the skill work.
- ❌ **Inlining literal hex everywhere**: makes palette changes a search-and-replace nightmare. Use CSS classes matched to the device's palette header.
- ❌ **Skipping the helper expansion**: a `drawPill()` call is not "one SVG element" — it's `<rect>` plus `<text>` plus often a leading icon `<rect>`. Read the helper first.

## Where the source code lives (example layout from an embedded controller project)

| Topic | File | Notes |
|---|---|---|
| Sidebar | `src/ui/touch_ui.cpp` `_drawSidebar()` | width SIDEBAR_W=68px (was 82px) |
| Home screen | `src/ui/screens/screen_home.cpp` (+ `_drawCurveSvg`) | hero temp 88px → 64px font |
| Curves grid | `src/ui/screens/screen_curves.cpp` | `CRV_CW=226`, `CRV_COLS=3` |
| Editor | `src/ui/screens/screen_editor.cpp` | tabular `COL_SEG/COL_TEMP/COL_RATE/COL_HOLD` |
| Favorites | `src/ui/screens/screen_favorites.cpp` | `FAV_CW=226`, `FAV_CH=210` |
| Settings | `src/ui/screens/screen_settings.cpp` | PID card + WLAN card |
| Component helpers | `src/ui/ui_components.h` | `drawTempDisplay(XL)`, `drawPill(LG)`, `drawButton`, `drawProgress` |
| Color tokens | `src/ui/colors_studio.h` | match SVG CSS classes to these |
| Curve defaults | `include/curve_defaults.h` | factory curves with segments |

## Quick start commands

```bash
# Find all draw calls in a screen
grep -nE "(fillRect|drawString|drawLine|fillCircle|drawRect|fillRoundRect)" src/ui/screens/screen_home.cpp

# Find all helper functions the screen uses
grep -nE "draw[A-Z][a-zA-Z]*\(" src/ui/screens/screen_home.cpp | sort -u

# After writing the SVG, validate it renders standalone
open mockup_home.svg   # or open in browser
```

## Real-world impact (embedded controller user manual)

Iterations v1–v4 used the semantic-CSS approach: 4 versions, each with pill-position errors, wrong column widths, wrong text padding. v5 pivoted to "1:1 SVG from source code". v5–v8 closed remaining structural issues (pin overlap, Y-pos recalc for LovyanGFX baseline) — but the **method** was right from v5 onward. Final manual ended at 4 A4 pages, 6 pixel-precise SVG mockups, printable via browser-print, suitable for a non-technical recipient.

Lesson of the day: the CAD maxim "measure, don't estimate" also applies in UI documentation. **For visualizations that must mirror an existing artefact, translate the artefact directly instead of rebuilding it.**
