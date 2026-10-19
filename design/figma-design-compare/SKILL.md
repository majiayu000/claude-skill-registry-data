---
name: figma-design-compare
description: Use when checking whether a built website, web app or mobile app screen matches its Figma design, doing design QA or a pixel-perfect review, comparing implementation with a Figma frame or link, or fixing "doesn't look like the design" feedback.
---

# Figma Design Compare

## Overview

Compare what was built with what was designed using two kinds of evidence: screenshots side by side, and exact values from Figma (font, size, color, spacing, radius) against the values in code. Report every mismatch with the Figma value, the built value, where to fix it and how.

## Inputs

- Figma frame link (`figma.com/design/<fileKey>/...?node-id=<id>`) — one frame per screen.
- The built screen: a URL or route, or a running emulator/simulator.
- Access to Figma: the Figma MCP server if connected, otherwise a `FIGMA_TOKEN` (personal access token). Never print the token.

## Method

1. **Get the design.**
   - Image of the frame at 2x and the node data (layout, text styles, fills, strokes, effects, auto-layout padding and gaps).
   - Commands for MCP and REST API are in [capture.md](capture.md).
2. **Capture the build at the same size.** Use the frame's width as the viewport width (for example 1440 desktop, 390 mobile) and the same scale. Load real fonts, wait for the page to settle, close cookie banners. Commands in [capture.md](capture.md).
3. **Visual pass.** View both images. Walk the screen top to bottom, section by section: presence and order of elements, alignment, spacing rhythm, sizes, colors, typography, icons, images, borders, shadows, states.
4. **Measured pass.** For each important element, read the value from the Figma node and from the implementation (source CSS/Tailwind/styles, or computed styles from the browser). Compare with the tolerances below.
5. **Locate the fix.** Find the component and line that sets the wrong value.
6. **Report** using the contract below. If asked, apply fixes and repeat steps 2-4 to confirm.

## Tolerances

| Property | Match when |
|---|---|
| Spacing, size, position | within ±2 px at 1x |
| Font family, weight | exact |
| Font size, line height, letter spacing | within ±0.5 px |
| Color | same hex (or visually indistinguishable, ΔE < 2) including opacity |
| Border radius, border width | exact |
| Shadows | same offset, blur, color within tolerance |

Differences caused by real content length, OS font rendering or anti-aliasing are not mismatches.

## Output contract

Start with: `Screen: <name> — <N> mismatches (X high, Y medium, Z low). Match: <good | minor issues | off>`.

Then a table, highest impact first:

| # | Element | Property | Figma | Built | Location | Fix |
|---|---|---|---|---|---|---|
| 1 | Hero heading | font-size | 56px | 48px | Hero.tsx:12 | `text-[56px]` |

Then **Missing or extra elements**, then **Matches** (what was checked and is correct). Impact: High = visible to every user at a glance (layout, missing element, wrong color or font); Medium = noticeable spacing or size; Low = within a few pixels.

## Common mistakes

- Comparing at different viewport widths or scales, then reporting every size as wrong.
- Judging only from screenshots: a 4 px spacing error is invisible at a glance but obvious in values.
- Reading the wrong Figma variant or an outdated frame. Confirm the node id and last-modified date.
- Reporting differences in placeholder text or images as design defects.
- Fixing values with magic numbers when the project has design tokens for them.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
