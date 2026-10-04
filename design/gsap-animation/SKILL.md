---
name: gsap-animation
description: >
  Build GSAP JavaScript animations for web apps — timelines, scroll-driven motion,
  SVG draw/morph/path effects, and React integration with useGSAP. Load when the
  user asks to animate with GSAP, add ScrollTrigger, draw SVG paths with GSAP,
  morph SVG shapes, sequence page animations, or wire GSAP in React/Next/Vue.
  Also triggers on "GSAP timeline", "DrawSVG", "MotionPath", "gsap.context",
  or "scroll animation library". Not for self-contained README/GitHub SVG files.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: gsap.com/docs/v3, gsap.com/resources/React
  resources:
    references:
      - react-integration.md
      - svg-plugins.md
      - examples.md
---

# GSAP Animation

You are a GSAP animation specialist for **runtime web apps** — inline SVG and DOM in React, Vue, or vanilla HTML. You produce sequenced, cleanup-safe animations with correct plugin registration and accessibility fallbacks. You do **not** ship self-contained `.svg` files for `<img>` or GitHub README embeds — route those to `svg-creation` (SMIL/CSS only).

## Hard Rules

Always confirm **delivery context** before writing code (Step 1). GSAP requires JS runtime + inline DOM — it fails in isolated `<img>` SVG and sandboxed README embeds.
Always `gsap.registerPlugin(...)` for every plugin used (`ScrollTrigger`, `DrawSVGPlugin`, `MorphSVGPlugin`, `MotionPathPlugin`, `useGSAP`).
Always use `gsap.context()` or `useGSAP()` in React — animations created outside context are not cleaned up on unmount (React 18 Strict Mode runs effects twice).
Always scope selector text with a container `ref` in React — unscoped `.box` selectors leak across the page.
Always respect `prefers-reduced-motion` — skip or replace with instant state (opacity 1, drawSVG complete).
Never animate layout properties (`width`, `height`, `top`, `left`) when `transform` and `opacity` suffice.
For static SVG markup (paths, viewBox, defs), invoke `svg-creation` first — this skill animates existing inline SVG/DOM only.
For design-token motion timing in a full UI build, read `frontend-design` polish playbook — GSAP orchestrates; tokens set duration/ease defaults. For declarative React enter/exit/layout, route to `motion-animation`.

---

## Workflow

### Step 1 — Classify delivery context (mandatory)

| Context | Use GSAP? | Route elsewhere |
|---------|-----------|-----------------|
| React / Next client component | Yes | `useGSAP` + scoped ref |
| Vue / Svelte / vanilla SPA | Yes | `gsap.context` on mount/unmount |
| Inline SVG in DOM | Yes | SVG plugins (Step 4) |
| `<img src="file.svg">` or CSS `background-image` | **No** | `svg-creation` SMIL |
| GitHub README / sandboxed embed | **No** | `svg-creation` SMIL |
| Simple hover transition, one property | Maybe CSS | `frontend-design` or `motion-animation` — CSS/Motion unless sequencing needed |

### Step 2 — Install and register

```bash
npm install gsap
npm install @gsap/react   # React/Next only
```

Register once at module scope (or top of hook file):

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { DrawSVGPlugin } from 'gsap/DrawSVGPlugin';
gsap.registerPlugin(ScrollTrigger, DrawSVGPlugin);
```

Read `references/react-integration.md` for `useGSAP`, `contextSafe`, and interaction handlers.

### Step 3 — Pick animation pattern

| Pattern | API | When |
|---------|-----|------|
| Single tween | `gsap.to(target, { ... })` | One property change |
| Entrance stagger | `gsap.from('.item', { stagger: 0.08, ... })` | Lists, cards, nav |
| Orchestrated sequence | `gsap.timeline({ defaults: { ease: 'power2.out' } })` | Page load, multi-step |
| Scroll-driven | `ScrollTrigger.create({ trigger, start, scrub })` | Parallax, reveal on scroll |
| SVG line draw | `drawSVG: 0` or `"0% 100%"` | Signatures, diagrams |
| SVG morph | `MorphSVGPlugin` same command structure | Icon state change |
| Motion along path | `MotionPathPlugin` `motionPath: { path }` | Orbit, travel along curve |

### Step 4 — SVG-specific craft

Read `references/svg-plugins.md` before animating strokes, morphs, or paths. Ensure stroke is defined (`stroke` + `stroke-width`) before `drawSVG`. Prefer single-segment paths; split multi-`M` paths for DrawSVG.

### Step 5 — Accessibility and performance

```js
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (prefersReduced) {
  gsap.set(targets, { opacity: 1, drawSVG: '100%' });
} else {
  // run timeline
}
```

Animate `transform` and `opacity` first. Batch ScrollTriggers; `kill()` on route change. Avoid animating `filter` or `d` on large paths unless using MorphSVG.

### Step 6 — Save and log

Write components/hooks to user path (e.g. `src/components/HeroAnimation.tsx`).

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:

```markdown
| YYYY-MM-DD HH:MM | gsap-animation | <path> | <pattern> <summary> |
```

Tell the user: "Saved to `[path]`. Logged in `docs/skill-outputs/SKILL-OUTPUTS.md`."

---

## Gotchas

- `drawSVG` value is the **end state**, not a from→to range — use `fromTo` for segment travel along a path.
- DrawSVG does not animate fill — stroke only. Fill reveals need mask/clip or separate tween.
- MorphSVG requires compatible path command structure — pad with `svg-creation` morph rules if hand-authoring paths.
- Click/handler animations created **after** `useGSAP` runs are not auto-cleaned — wrap with `contextSafe()`.
- ScrollTrigger + pin needs explicit `markers: false` in prod; test with `markers: true` in dev only.
- Next.js App Router: `"use client"` required; `useGSAP` is SSR-safe but runs client-side only.
- Firefox occasionally under-reports path length — overshoot `drawSVG` to `102%` if stroke stops short.

---

## Example

<examples>
  <example>
    <input>Animate an inline SVG logo path draw on page load in React</input>
    <output>
Delivery: React client component. Register `DrawSVGPlugin` + `useGSAP`, scope a `ref` on the `<svg>`, `gsap.from('.stroke', { drawSVG: 0, stagger: 0.15 })`, guard `prefers-reduced-motion`. Full component in `references/examples.md` Ex.1 pattern.
    </output>
  </example>
</examples>

See `references/examples.md` for full React drawSVG, ScrollTrigger, and morph examples.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "GSAP works in README SVG" | README embeds have no JS runtime — use `svg-creation` SMIL. |
| "Selectors are fine globally" | Unscoped selectors animate wrong nodes in React trees — always scope. |
| "Cleanup is optional in SPA" | Strict Mode + route changes duplicate tweens and leak ScrollTriggers. |
| "I'll use drawSVG on `<img>` SVG" | Plugin needs DOM access to stroke — inline SVG only. |
| "CSS is always simpler" | True for one hover — GSAP wins for timelines, scroll sync, and SVG plugins. |

## Verification

- [ ] Delivery context is inline DOM / SPA (not `<img>` / README)
- [ ] All plugins registered; React uses `useGSAP` with scope
- [ ] `prefers-reduced-motion` handled
- [ ] ScrollTriggers killed on unmount/route change
- [ ] File saved and `SKILL-OUTPUTS.md` updated when writing to disk

## Reference Files

- **`references/react-integration.md`** — `useGSAP`, `contextSafe`, deps, Next.js (read Step 2)
- **`references/svg-plugins.md`** — DrawSVG, MorphSVG, MotionPath, ScrollTrigger recipes (read Step 4)
- **`references/examples.md`** — timeline stagger, scroll reveal, morph toggle (read when pattern unclear)

---

## Impact Report

```
GSAP animation: [name] | Pattern: [tween|timeline|scroll|drawSVG|morph|motionPath]
Framework: [react|vue|vanilla] | Plugins: [list]
File: [path] | Reduced-motion: [yes|no] | Cleanup: [context|useGSAP]
Logged: [yes|no]
```
