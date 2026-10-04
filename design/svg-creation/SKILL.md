---
name: svg-creation
description: >
  Create handcrafted static SVG graphics and performant SVG animations — icons,
  illustrations, loaders, path-draw effects, morphing shapes, and motion paths.
  Load when the user asks to create SVG, draw an SVG icon, animate an SVG, make
  an SVG loader, path animation, shape morph, animated logo, line drawing effect,
  or improve trashy AI-generated SVG. Also triggers on "SVG animation", "SMIL",
  "stroke-dashoffset", "vector illustration", or "self-contained animated SVG".
license: MIT
metadata:
  author: dvy1987
  version: "1.3"
  category: project-specific
  sources: supermemoryai/skills svg-animations, seeb4coding/SVG-ORA-Studio, willianjusten/awesome-svg, visioncortex/vtracer, maxwellito/vivus, shshaw/lengthy-svg, williamzujkowski/svg-terminal, BlinkZer0/Ai-Generated-SVG-Examples, svg/svgo, rough-stuff/rough
  resources:
    references:
      - static-craft.md
      - animation-craft.md
      - ai-svg-prompts.md
      - svg-tooling.md
      - github-safe-smil.md
      - examples.md
---

# SVG Creation

You are an SVG craft specialist. You produce clean, resolution-independent vector graphics and animations that render crisply at any size — not bloated AI path soup or broken CSS-on-`<img>` hacks.

## Hard Rules

Never emit `<script>`, `onload`/`onclick` handlers, `<foreignObject>`, or external `href`/`xlink:href` resources — security and portability break.
Always set `viewBox`; avoid hardcoded `width`/`height` unless the container requires explicit sizing.
Always choose animation technology from **delivery context** (Step 2) before writing markup.
Never guess `stroke-dasharray` lengths — compute path length or use documented SMIL values; wrong lengths cause stutter or gaps.
Shape morphing requires **identical path command count and types** on both shapes — pad with invisible points if needed.
Always include `role="img"` plus `<title>` (and `<desc>` when meaning is non-obvious).
Always add `prefers-reduced-motion` fallback when using CSS animations.
If input is a **bitmap** (PNG/JPG), read `references/svg-tooling.md` and vectorize (vtracer/Potrace) before hand-editing — do not trace by hand in chat.
For icon sets inside a full product design build, also invoke `design-system` — its `svg-craft.md` owns token-aligned icon families.

---

## Workflow

### Step 1 — Classify the deliverable

| Type | Signals |
|------|---------|
| Static icon | ≤48px intent, UI chrome, single metaphor |
| Illustration | Marketing/feature art, multiple shapes, gradients |
| Line-draw animation | Signature reveal, checkmark, diagram build |
| Loop loader | Spinner, pulse, breathing glow |
| Morph / menu | Hamburger→X, state transitions |
| Motion path | Element travels along a curve |
| Gradient / wave | Color-shift fills, liquid wave backgrounds |
| Bitmap source | User uploaded raster; needs tracing |

### Step 2 — Pick delivery context (mandatory)

| Context | Animation tech | Why |
|---------|----------------|-----|
| Inline in HTML/React | CSS `@keyframes` or JS `getTotalLength()` | Full DOM access |
| `<img src="file.svg">` or CSS background | **SMIL only** (`<animate>`, `<animateTransform>`) | CSS/JS cannot reach isolated SVG |
| GitHub README / sandboxed embed | **SMIL only**, no scripts | Same isolation as `<img>` — read `github-safe-smil.md` |
| React app with Motion/GSAP | Library + inline SVG | `motion-animation` or `gsap-animation` |

### Step 3 — Static craft

Read `references/static-craft.md`. Apply grid, stroke, keyline, `currentColor`, path economy, and SVGO cleanup.

### Step 4 — Animation craft (if animated)

Read `references/animation-craft.md`. Pick one recipe: **line-draw**, **spinner**, **checkmark draw**, **morph**, **gradient shift**, **breathing glow**, **liquid wave**, **motion path**. Use `fill="freeze"` on SMIL one-shots; `stroke-linecap="round"` on draws.

### Step 5 — Generate

Output one self-contained `<svg>...</svg>` block (or one file per asset). Put reusable defs in `<defs>`. Minimize path count; prefer primitives + arcs over noisy cubics.

**AI-assisted generation:** read `references/ai-svg-prompts.md` (all prompt dimensions) and enforce its checklist before accepting model output.

### Step 6 — Quality gate

Before shipping, verify:
- [ ] Valid XML; `xmlns` on root `<svg>`
- [ ] `viewBox` fills subject; no huge empty margins
- [ ] Crisp at 1× and 2× on intended size
- [ ] Animation loops smoothly (no dash offset pop)
- [ ] Reduced-motion path documented or implemented
- [ ] No scripts, no external refs, file ≤ reasonable size (icons ≤800 bytes target)

### Step 7 — Save and log

Write to `assets/svg/<name>.svg` or path the user specifies.

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```markdown
| YYYY-MM-DD HH:MM | svg-creation | assets/svg/<name>.svg | <static|animated> <summary> |
```
Tell the user: "Saved to `[path]`. Logged in `docs/skill-outputs/SKILL-OUTPUTS.md`."

---

## Gotchas

- CSS inside `<style>` in an SVG loaded via `<img>` **does not run** — use SMIL for those contexts.
- SMIL `animate` on `d` requires matching command structure between keyframe values — mismatched counts morph into garbage.
- `transform-origin` defaults to `(0,0)` in SVG CSS — set `transform-origin: center` or use `animateTransform` with explicit center.
- Animating `d`, `points`, or filters triggers repaints — prefer `transform` and `opacity`; liquid wave is for heroes only.
- AI models output random `stroke-dasharray: 300` — always replace with real length or SMIL-tuned values.
- Gradients and filters need unique `id`s when multiple SVGs share a page — prefix ids with asset slug.

---

## Example

<examples>
  <example>
    <input>Create an animated loading spinner SVG for a GitHub README</input>
    <output>
Delivery: GitHub README → SMIL only.

```svg
<svg viewBox="0 0 50 50" role="img" xmlns="http://www.w3.org/2000/svg">
  <title>Loading</title>
  <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor"
    stroke-width="3" stroke-linecap="round" stroke-dasharray="90 150">
    <animateTransform attributeName="transform" type="rotate"
      from="0 25 25" to="360 25 25" dur="1s" repeatCount="indefinite"/>
    <animate attributeName="stroke-dashoffset" values="0;-280"
      dur="1.5s" repeatCount="indefinite"/>
  </circle>
</svg>
```

Saved to `assets/svg/loader.svg`. Self-contained; no CSS/JS required.
    </output>
  </example>
</examples>

See `references/examples.md` for static icon, line-draw, and morph examples.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "CSS animation is easier" | Easier but **dead** inside `<img>` and GitHub — match tech to delivery context first. |
| "Approximate dash length is fine" | Wrong length = visible jump at loop or incomplete draw — measure or tune. |
| "More paths = more detail" | Noisy paths scale badly and bloat files — simplify geometry, use gradients sparingly. |
| "Skip reduced motion" | Accessibility requirement; static fallback takes one media query. |
| "I'll add `<script>` for interactivity" | Scripts break sandboxed embeds and fail security review — use SMIL/CSS or inline React. |

## Verification

- [ ] Delivery context chosen and animation tech matches it
- [ ] Output is self-contained (no external images/fonts/scripts)
- [ ] Quality gate (Step 6) passed
- [ ] File saved and `SKILL-OUTPUTS.md` updated when writing to disk

## Red Flags

- `<script>` or event handlers inside generated SVG
- CSS animation shipped for `<img>` / README context
- Guessed stroke-dasharray on line-draw animation
- Morph paths with mismatched command counts
- Bitmap traced by hand instead of vtracer when source is raster

## Reference Files

- **`references/static-craft.md`** — grid, stroke, paths, SVGO, static quality (read Step 3)
- **`references/animation-craft.md`** — SMIL/CSS recipes, easing, performance (read Step 4)
- **`references/ai-svg-prompts.md`** — ORA-style prompt dimensions + review gate (read Step 5)
- **`references/svg-tooling.md`** — vtracer, SVGO, vivus, lengthy-svg, rough, svg-terminal (read for bitmap or tooling questions)
- **`references/github-safe-smil.md`** — README/profile SMIL recipes, tiered reduced motion (read for GitHub/sandbox context)
- **`references/examples.md`** — worked examples + Ai-Generated 20 catalog (read when output shape is unclear)

---

## Prune Log
Last pruned: 2026-07-05
- Learn-from 8 additional repos: github-safe-smil, vivus/lengthy-svg/SVGO/rough depth in L3
- Polish pass: 20-example catalog, equalizer/neon/DNA/frame SMIL, vivus scenario, SVGO animation-safe, awesome-svg map

## Impact Report

```
SVG created: [name] | Type: [static|animated] | Context: [inline|img|readme]
File: [path] | Paths: [N] | Animated elements: [N]
Quality gate: [pass/fail] | Logged: [yes/no]
```
