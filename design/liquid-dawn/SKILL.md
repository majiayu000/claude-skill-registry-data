---
name: liquid-dawn
description: |
  Build or restyle anything in Liquid Dawn, the calm daylight sibling of Liquid Midnight. The look: warm paper grounds
  (Dawn, primary) and a sea-slate Dusk mode; nature drawn in type (lagoon caustics, meadow breeze, cumulus, pebble
  ripples on a one-glyph lattice); glyph-tile shoals of fish, birds and islands with cast shadows; dew glass rimmed in
  pearl liquid metal; refraction drawn by the field itself under glass; light, tight type in four switchable voices
  (Manrope, Inter Tight, Geist, Instrument) with one tide-blue payoff phrase; real proportional text laid out by pretext that ripples or reflows round moving shapes; and slow motion
  where every frame is a pure function of t.
  Ships tokens (OKLCH + hex, dawn and dusk modes), materials CSS, a framework-agnostic canvas kit (fields, ASCII + lenses,
  shoals, pretext pages, render loop), a live specimen, and a render-and-look tool.
  Use for calm landing pages and heroes, composer and chat surfaces, showcase moments, living backgrounds, reels and
  posts that should feel quiet, natural and premium.
  Triggers on "liquid dawn", "light liquid glass", "calm style", "paper style with glass", "nature ascii",
  "ascii shader landing", "ascii fish", "tranquil animation", "pearl rim", "light mode liquid midnight",
  "the calm variant", "liquid midnight but light".
  NOT for the dark expressive keynote look (that is liquid-midnight) or calm matte product chrome (broomva-design).
  Do not mix their tokens on one surface.
license: MIT
metadata:
  version: "0.1.0"
primitive: null
category: design
required: false
introduced_in: "0.51.1"
---

# Liquid Dawn

The full contract is **[DESIGN.md](DESIGN.md)**: read it before you build. This file covers how to apply it.
`SKILL_DIR` is the directory that contains this file.

## 1. Decide that it fits

- **Fits:** landing pages and heroes, composers and chat surfaces, onboarding and empty states, showcase sections,
  living backgrounds, reels and posts that should feel calm and natural. Light is the default; Dusk is first-class.
- **Use liquid-midnight instead** for dark, expressive keynotes and the Agent Workspaces look.
- **Use broomva-design instead** for everyday product chrome (forms, tables, settings).
- If the target already has a design system, ask before restyling it.

## 2. Bring the assets in

The skill is self-contained: copy `assets/` into the target (keep its folder layout, since the CSS references
`../fonts/` and the kit imports `./vendor/pretext.js`).

```bash
SKILL_DIR=/path/to/skills/design/liquid-dawn   # the directory that contains this SKILL.md
mkdir -p liquid-dawn && cp -R "$SKILL_DIR/assets/." liquid-dawn/
```

Load `liquid-dawn/tokens/tokens.css`, then `liquid-dawn/css/materials.css`, and import the kit as ES modules from
`liquid-dawn/kit/index.js`. Modes: set `data-ld-mode="dawn"` or `"dusk"` on `<html>`; to follow the OS, call `followOS(document.documentElement, rebuild)` from the kit (it resolves the attribute and calls you back on every change).

## 3. Build with the grammar

Before any canvas drawing, `await fontsReady()` and call `readColors()` (again after every mode switch): the kit's
colour table `C` is empty until then, and everything below reads its colours from it.

| Need | Use |
|---|---|
| Ground | `body.ld-ground`; in a hero: `.ld-wash`, a field `<canvas class="ld-field">`, `.ld-grid`, `.ld-clearing` |
| A living field | `field(cx, { fn: (x, y) => tide(x, y, t), ramp: RAMP.water, color: C.tide, mask: (x, y) => clearing(...) })`; also `breeze` + `bladeGlyph`, `cloud`, `rippleField` |
| Glass that bends the field | DOM `.ld-lens` over the canvas **and** pass its rect as `lenses: [{x, y, w, h, r}]` to `field()`, with `fringe: [C["metal-fringe-a"], C["metal-fringe-b"]]` |
| Cards, captions | `.ld-glass` (pearl rim included); `.ld-glass-metal` for a pearl chrome bevel, `.ld-glass-prism` for a clearer cyan/sand edge |
| Nav, segmented | `.ld-capsule` with `.ld-chip` (`aria-pressed="true"` for the active one) |
| Round actions | `.ld-ring` with an inline SVG icon |
| Composer | `.ld-lens.ld-composer` with an `<input>` and a `.row` hint line |
| Life | `createShoal({ w, h, colors: C }).at(t)` and `createIslands(...)`, drawn with `tiles(cx, cells, { shadow: C.shadow })` |
| Hero background | `createHero("dawn" \| "caustic" \| "currents" \| "lagoon" \| "horizon" \| "tide", { w, h, colors: C })` over `<div class="ld-hero-bg" data-recipe=…>` + a soft and a sharp canvas; see `assets/specimen/heroes.html` |
| Film background | a `scroll-cinema` film with `sampleFrame` + `seamDissolve` + `filmType` from `kit/cinema.js`: the picture turns to type at every page break (DESIGN.md §6.6) |
| Photo as tiles | each frame: clear a scratch canvas of `cols × rows` px, `paintImage(scratch2d, img, { x, y, len, ang })` (cells), then `mosaic(cx, scratch, { cell: 14, keyLight: 0.93 })`; it returns false for a CORS-tainted photo |
| Liquid lens | `const lens = createLens(overlayCanvas, sourceCanvas, { r: 96 })` (both canvases in one CSS box); `lens.snap(x, y)` to place it (else it starts centred); `dragLens(el, lens)`; in the loop `step: lens.step(dt)`, `paint:` draw the source, then `lens.paint()`. A transparent source works over a flat page colour: under the drop the lens paints that ground (or `{ ground: [r, g, b] }`) and lays the bent source over it. Over a gradient, image or transparent page, draw the backdrop into an opaque source |
| Agent presence | `sparkOrb(cx, sparkField(900), { x, y, R: 86, t, busy })` on a dark chip |
| Pictures as print | `printInto(cx, L, { w, h, mode: "engrave" \| "dither", ...DUOTONES.cobalt })` where `L` is `imageLuma(img, w, h)` or a scene such as `coastScene(w, h, t)`. **Costly** (≈150 ms for 1440 × 360): print when its input changes, never every frame; quantise t and cache, as `specimen/paper.html` does |
| Text as a field | `layoutPage` + `lensPage` (pebble by default, well at most once per story); `flowAround` to reflow round a moving obstacle |
| Headline | `.ld-kicker`, then `.ld-hero` / `.ld-title` with the payoff in `<em>` |
| Voice | `data-ld-type="manrope" \| "inter-tight" \| "geist" \| "instrument"` on `<html>`; `await fontsReady()` before canvas text, or `await fontsReady(el)` when the theme is set on a subtree `el` |
| Motion | `createLoop({ paint(t) { … } })`; expose `window.renderAt = (t) => loop.renderAt(t)` and set `window.__ready = true` after a capture frame |

Working examples to copy (each takes `?mode=dusk` and `?t=6` for a deterministic frame):
- `assets/specimen/index.html`: ground, fields, glass, capsule, ring, composer, shoals, text as a field, motion, and
  the default hero recipe;
- `assets/specimen/heroes.html`: every hero recipe; `assets/specimen/type.html`: every voice;
- `assets/specimen/paper.html`: photo as tiles, the liquid lens, agent presence, pictures as print.
`paper.html` also includes bundled toile/sky film-to-type studies; these are ambient material options, not a continuous scroll-cinema chain. Wire a scroll background from DESIGN.md §6.6 and `kit/cinema.js`. See [the glass/orb research notes](references/glass-and-orb-studies.md) for implementation provenance and limits.

**Never ship these** (DESIGN.md §3): pure white or grey grounds; purple; editorial serif display; a field that reads
as uniform texture or rain; heavy frost; glass on glass; a frosted panel with no pearl rim; glow-orb subjects;
magenta fringes; fast motion; the `well` as a default.

## 4. Render and look

```bash
node "$SKILL_DIR/scripts/serve.mjs" liquid-dawn                      # live preview: http://127.0.0.1:4318/specimen/
node "$SKILL_DIR/scripts/render.mjs" liquid-dawn specimen/index.html --t 0,6,12 --mode dawn,dusk --out renders
```

`render.mjs` needs Playwright with Chromium (`npm i -D playwright && npx playwright install chromium`, or set
`LD_PLAYWRIGHT_DIR`). It writes a full-page PNG plus one per `[data-shot]` element. **Open every PNG and look**
against DESIGN.md §11's checklist, in both modes. Acceptance comes from the render, not from the code.

Accessibility checks on the render: text stays ink/ink2/ink3/tide; nature colours never carry text; emulate
`prefers-reduced-motion`, `prefers-reduced-transparency` and `prefers-contrast: more` and confirm the fallbacks.

## 5. Changing the style

`assets/tokens/tokens.json` is the source of truth: edit it, then `node scripts/build_tokens.mjs` (tests fail if
`tokens.css` is stale). Update DESIGN.md §4 when a colour changes; the tests re-measure contrast.
Pretext is vendored at `assets/kit/vendor/pretext.js` (v1.0.0, MIT, see `pretext.LICENSE`); re-bundle with
`bun build node_modules/@chenglou/pretext/dist/layout.js --target=browser --format=esm --minify` to update.
