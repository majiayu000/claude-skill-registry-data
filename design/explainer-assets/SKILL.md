---
name: explainer-assets
description: 'Generate crafted SVG/CSS components, props, characters, and environments for animated explainer videos — the build order, light rules, factory patterns, and engineering contracts that make assets read as illustrated objects AND survive choreography. Use when creating or upgrading any visual asset: a prop, mascot, component system, or background world.'
user-invocable: true
---

# Explainer assets — generating components and source art properly

Every asset in an explainer is either a **component** (chips, bars, cards, stamps — styled DOM), a **prop** (vessels, pages, cabinets, gauges — inline SVG), a **character** (host mascot, population minions — SVG factories), or an **environment layer** (parallax worlds — data-URI or inline SVG). Each has its own build discipline. The difference between "styled div" and "crafted object" is a fixed sequence of cheap moves — never skill, always order.

## The universal build order (any prop, every time)

1. **Silhouette first.** Flat single-fill shape at the FINAL footprint (left/top/width/height and viewBox locked before any detail). Get the read at thumbnail size — if the silhouette doesn't say "bucket," no amount of detail will.
2. **One light source, top-left, film-wide.** Then: 2-tone via `linear-gradient(180deg, lighter, base)` on the body, top gloss (`inset 0 2px 0 rgba(255,255,255,.3-.5)` or a highlight path), bottom shade (`inset 0 -3px 0 rgba(0,0,0,.1)`).
3. **Depth cues — the 3 that sell 3D:** a DARKER inner-opening ellipse for any mouth/rim (this single ellipse is what makes an opening read as 3D); a soft base-contact shadow ellipse; inter-unit shadow lines between stacked parts (drawers, sheets).
4. **Detail pass — 3 to 5 accents max:** bands/hoops with a 1px white highlight edge, label plates, grain lines, corner ticks, a specular curve. Stop before it gets busy; Kurzgesagt props are simple shapes with perfect light.
5. **Motion hooks LAST, planned not patched:** the class the timeline will target, a wrapper `<g>` for any transform the animation will own, and the pivot decided NOW (see svgOrigin below). An asset built without motion hooks gets rebuilt.

## Component systems before one-offs

Never style one chip. Build the SYSTEM in CSS once — every variant inherits:
- **The sticker recipe:** hard down-right ink drop (`3px 3px 0 var(--ink)`) + top gloss inset + bottom shade inset + `inset 0 0 0 1-2px rgba(255,255,255,.14)` die-cut rim. Translucent insets ride ANY background color, light or dark — one rule elevates every variant.
- One radius scale (sm 10 / base 13 / lg 16), one shadow angle, one light direction.
- **Text-safe rule:** on components carrying animated text (SplitText chars), gloss must be inset box-shadows (paint UNDER text) — never a positioned `::before` overlay (paints OVER the glyphs and dims them).
- Stamps get ink-bleed: same-hue soft `text-shadow` (glyphs) or shared `drop-shadow` filter (SVG marks).
- Drawn line-art (arrows, boxes): ONE selector — `filter: drop-shadow(0 1.5px .5px rgba(0,0,0,.17))` on all `.drw` strokes gives every arrow a 2-tone underside and reveals WITH DrawSVG (filters are independent of dashoffset).

## Character factories

Characters are **JS functions returning SVG strings**, not static markup — one edit upgrades every instance.
- **Singleton host** (one instance, e.g. the flying mascot): MAY carry `uid`-suffixed `<defs>` gradients (`'bwg'+uid`) for iridescent wings, radial antenna balls, body sheen. Expose a **faces API** (`host('aha'|'sad'|'happy', size)`) — swap eyes/brows/mouth blocks, keep everything else.
- **Multi-instance minions** (inlined 10-50×): must be **id-FREE** — plain fills only (wing vein stroke, top highlight ellipse, stripe highlight lines, cheek dot) or gradient ids duplicate across the document and break rendering.
- **Class-hook contract:** wrapper classes the CSS animates (`hwrap` bob, `hwl/hwr` wing flutter, `heyes` blink) are API — never rename during an asset pass without updating CSS + JS + docs together. New decorative transforms go on INNER wrapper `<g>`s so they compose with (never fight) the CSS animation on the outer hook.
- Ground-contact shadow under every character; badges/accessories as optional factory args.
- **Props characters hold get full prop treatment** (the pencil: gradient hex body + facet lines + specular, crimped ferrule, eraser cap with darker rim, wood taper with grain, graphite cone — same anchor/axis as the arm rotation expects).

## Environments (parallax worlds)

- Three layers with fixed roles: **far** (sky gradient, sun/moon, haze band, 2-tone volumetric clouds = tinted base ellipse + 3 white circles + bright top ellipse, far hills), **mid** (hero landmarks — hive/buildings with real detail, layered-petal flowers), **near** (blurred foreground foliage, CORNERS ONLY so it never covers captions, leaf midribs + side veins).
- Every layer needs a variant per scene mood (warm/paper/cold/dark) — same shapes, recolored; dark gets moon + fireflies.
- Ambient characters (drifting minions, dust motes) live in **margins and the top strip only** — their full drift path must never cross a text band.

## SVG engineering contracts (each one has broken production)

- **Pivot planning:** a px `transformOrigin` on an SVG group is BBOX-relative — rebuilding the group's geometry silently moves the pivot (a gauge needle swung off-stage for a full scene this way). For fixed pivots in SVG user-space always use GSAP's `svgOrigin:'x y'`, decided when the asset is built.
- **Selector inventory before touching anything:** grep the script for every class/positional selector; `.bkt3 path` means the FIRST `<path>` must remain the tweened body — lead with `<ellipse>` shadows, never a decorative path.
- **Footprint freeze:** re-crafting keeps left/top/width/height/viewBox identical; `overflow:visible` lets back-sheets/stacks peek without moving the box. Placement changes are a separate, deliberate pass.
- **Decorate timeline-driven props with pseudo-elements** (`::before` ruled lines, tape, cracks, meniscus) — they ride the transform with zero new choreography. Track which pseudos are "taken" per class; collisions are silent.
- **Hide with autoAlpha** (visibility:hidden), not bare opacity/scale — invisible elements must not leave phantom boxes that fool overlap audits.
- Files need `<meta charset="utf-8">`; HTML entities in DOM text, `\u` escapes in JS strings.

## Quality gates for any new/changed asset

1. Reads correctly at 100% AND at thumbnail scale (the silhouette test).
2. One light direction across the whole frame — a new prop lit differently is a defect.
3. No flat fills on anything bigger than an accent.
4. `node --check` the script block + full selector-survival checklist after any DOM surgery.
5. Overlap audit (0.5s steps) after placing it — an asset isn't done until it coexists with everything else on stage.
