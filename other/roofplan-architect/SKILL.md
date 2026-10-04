---
name: roofplan-architect
description: >
  ISO 128/129/3098 drawing quality skill for the Panelin 2D roof plan, 3D
  realistic preview, and print/PDF pipeline. Provides a 100-point scoring
  rubric across 7 domains, implementation patterns, and verification workflow.
---

# RoofPlan Architect — Skill

## When to use

- "audit drawing quality", "ISO score", "improve plan annotations"
- "add scale bar / orientation mark / datum mark"
- "fix dimension collisions", "adjust line weights"
- "print theme", "capture SVG for PDF", "3D snapshot"
- "encounter colors in 3D"
- Any work on the files listed in the agent's Source of Truth table

## 8-Domain Checklist

Before shipping any drawing change, verify:

1. **Dimensioning (ISO 129)** — extension lines have gap+overshoot, 45° ticks,
   chain dims stacked correctly, envelope dim present for multi-zone.
2. **Visual hierarchy (ISO 128)** — 5-tier LINE_WEIGHTS applied, poché hatch
   visible on all zones, encounter edges distinguishable from zone borders.
3. **Typography (ISO 3098)** — 3 font tiers used consistently, Share Tech Mono
   loaded, fontWeight 500 on dimensions.
4. **Symbols** — ScaleBar auto-selects unit, OrientationMark at top-left,
   DatumMark at bottom-left of envelope.
5. **Collision avoidance** — dim text labels don't overlap encounter labels
   (AABB check via `roofPlanCotaObstacles.js`).
6. **Print/PDF** — PRINT_THEME applied, SVG captured via
   `captureRoofPlanSvgToDataUrl`, 3D via `capture3dCanvasToDataUrl`.
7. **3D preview** — dimension overlays visible, encounter edges color-coded
   by mode (continuo/pretil/cumbrera/desnivel).
8. **Organization** — all new SVG groups tagged with `data-bmc-layer`.

## Scoring Rubric (summary)

| Domain | Max | Items |
|--------|-----|-------|
| Dimensioning (ISO 129) | 25 | gap+overshoot, ticks, chain stacking, envelope, arch dims |
| Visual Hierarchy (ISO 128) | 20 | LINE_WEIGHTS, poché hatch, collision avoidance |
| Typography (ISO 3098) | 15 | 3 tiers, font family, weight, cross-device legibility |
| Symbols & Annotation | 10 | ScaleBar, OrientationMark, DatumMark, 3D overlays |
| Organization (layers) | 10 | data-bmc-layer tags, envelope layer present |
| Quality / Traceability | 10 | PDF 2D plan, 3D snapshot, collision-free labels |
| Color / Presentation | 10 | print theme, 3D encounter colors, overall consistency |
| **TOTAL** | **100** | |

Full per-item scoring matrix: see `reference.md` in this skill folder.

## Key Constants

```js
// roofPlanDrawingTheme.js
LINE_WEIGHTS = { zoneBorder: 0.072, encounter: 0.055, dimMain: 0.032, panelJoint: 0.024, hatch: 0.012 }
PRINT_THEME  = { dimStroke: '#000', zoneFill: '#f5f5f5', zoneBorder: '#1a1a1a', encounterStroke: '#333', panelJoint: '#666', hatchStroke: '#999', textColor: '#000', fontFamily: "'Share Tech Mono', 'DIN Alternate', 'Courier New', monospace" }

// RoofPanelRealisticScene.jsx
ENCOUNTER_COLORS = { continuo: '#22c55e', pretil: '#f97316', cumbrera: '#3b82f6', desnivel: '#ef4444' }

// roofPlanSvgTypography.js
dimFontPrimary   = dimFont          // 1×
dimFontSecondary = dimFont * 0.82   // chain dims, arch dims
dimFontTertiary  = dimFont * 0.72   // encounter labels, scale bar, datum
```

## Implementation Patterns

### Adding a new annotation layer

1. Create component in `src/components/roofPlan/`.
2. Accept `(x, y, svgTy, ...)` props — coordinates in meters.
3. Add `data-bmc-layer="your-layer-name"` to the root `<g>`.
4. Mount in `RoofPreview.jsx` before `</svg>`, after existing annotations.
5. Adjust `padB` / `padL` in the `svgViewBox` useMemo if needed.

### Modifying line weights

1. Add/edit the key in `LINE_WEIGHTS` in `roofPlanDrawingTheme.js`.
2. Reference via `import { LINE_WEIGHTS } from "..."`.
3. Apply as `strokeWidth={LINE_WEIGHTS.yourKey}` on SVG elements.

### Capturing SVG or 3D for PDF

1. Tag the target element: `data-bmc-capture="your-id"`.
2. Query at capture time: `document.querySelector('[data-bmc-capture="your-id"]')`.
3. Pass to the appropriate capture function in `captureDomToPng.js`.
4. Add a `row()` call in `buildSnapshotSectionHtml()` in `quotationViews.js`.

## Verification Workflow

1. `npm run lint` — after any edit in `src/`.
2. `npm test` — after logic changes.
3. Browser: paso 7 (Estructura) with 1-zone, 2-zone, and 3-zone configs.
4. PDF: paso 13, generate enriched PDF, verify 2D plan + 3D snapshot pages.
5. Final: `npm run gate:local:full` (lint → test → build).

## References

- Agent definition: `.cursor/agents/roofplan-architect.md`
- ISO scoring matrix: `.cursor/skills/roofplan-architect/reference.md`
- Knowledge base: `docs/team/knowledge/RoofPlanArchitect.md`
- 2D viewer specialist (non-ISO): `.cursor/agents/bmc-roof-2d-viewer-specialist.md`
