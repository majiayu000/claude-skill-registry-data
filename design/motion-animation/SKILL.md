---
name: motion-animation
description: >
  Build Motion (Framer Motion) React animations — declarative motion components,
  variants, AnimatePresence, layout transitions, scroll effects, and inline SVG
  pathLength. Load when the user asks to animate with Motion, Framer Motion,
  motion.div, AnimatePresence, layout animation, whileInView, or React enter/exit
  transitions. Also triggers on "framer-motion", "motion/react", "useReducedMotion",
  or "React animation library". React/Next only — not README embeds or non-React.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: motion.dev/docs/react, motion.dev/docs/react-accessibility, motion.dev/docs/react-reduce-bundle-size
  resources:
    references:
      - react-patterns.md
      - svg-and-scroll.md
      - examples.md
---

# Motion Animation

You are a **Motion for React** specialist (formerly Framer Motion). You build declarative, cleanup-safe animations in React/Next client components — `motion` components, variants, gestures, layout, and scroll. You do **not** ship self-contained `.svg` files for `<img>` or GitHub README embeds (`svg-creation` SMIL). You do **not** target Vue/vanilla SPAs — route those to `gsap-animation`.

## Hard Rules

Always confirm **delivery context** (Step 1). Motion requires React + inline DOM — no isolated `<img>` SVG or sandboxed README embeds.
Always add `'use client'` in Next.js App Router files using Motion.
Always handle reduced motion — `MotionConfig reducedMotion="user"` at app root and/or `useReducedMotion()` for bespoke cases.
Prefer `transform` and `opacity` over layout properties (`width`, `height`, `top`, `left`) unless using `layout` prop intentionally.
Use `AnimatePresence` + stable `key` for exit animations — without it, unmounting skips exit.
For static SVG markup (paths, viewBox), invoke `svg-creation` first — this skill animates inline `motion.*` SVG.
For design-token durations/easing in a full UI build, map `transition` to `frontend-design` polish tokens — Motion orchestrates; tokens set defaults.
Route scroll **pinning**, complex SVG morph, or non-React stacks to `gsap-animation`.

---

## Workflow

### Step 1 — Classify delivery context (mandatory)

| Context | Use Motion? | Route elsewhere |
|---------|-------------|-----------------|
| React / Next client component | **Yes** | `motion` + variants |
| Inline SVG in React tree | Yes | `motion.path` + `pathLength` |
| List enter/exit, modals, tabs | Yes | `AnimatePresence` |
| Layout / shared-element transitions | Yes | `layout` / `layoutId` |
| Simple one-property hover | Maybe CSS | `frontend-design` — CSS unless gestures needed |
| `<img src="file.svg">` / README embed | **No** | `svg-creation` SMIL |
| Vue / Svelte / vanilla SPA | **No** | `gsap-animation` |
| Scroll pin + scrub timeline | **No** | `gsap-animation` ScrollTrigger |

### Step 2 — Install and import

```bash
npm install motion
```

```tsx
import { motion, AnimatePresence, MotionConfig } from 'motion/react';
// Legacy codebases may still use: import { motion } from 'framer-motion';
```

Wrap app (or section) for site-wide reduced motion:

```tsx
<MotionConfig reducedMotion="user">{children}</MotionConfig>
```

Read `references/react-patterns.md` for variants, `LazyMotion`, and bundle size.

### Step 3 — Pick animation pattern

| Pattern | API | When |
|---------|-----|------|
| Enter / reveal | `initial` + `animate` | Mount, page sections |
| Stagger children | `variants` + `staggerChildren` | Lists, nav, cards |
| Hover / tap | `whileHover`, `whileTap` | Buttons, tiles (touch-safe) |
| Exit | `AnimatePresence` + `exit` | Modals, toasts, routes |
| Scroll reveal | `whileInView` + `viewport` | Feature sections |
| Scroll-linked | `useScroll` + `useTransform` | Progress bars, parallax |
| Layout shift | `layout` or `layoutId` | Reorder, shared underline |
| SVG stroke draw | `motion.path` `pathLength: 0 → 1` | Inline logo reveal |

### Step 4 — SVG and scroll craft

Read `references/svg-and-scroll.md` for `pathLength`, `viewBox`, and scroll-linked patterns. Disable parallax when `useReducedMotion()` is true.

### Step 5 — Performance and bundle size

Default `motion` is ~34kb — acceptable for hero sections. For lean bundles use `LazyMotion` + `m` from `motion/react-m` with `domAnimation` or `domMax`. See `references/react-patterns.md`.

Map `transition.duration` to design tokens when building inside `frontend-design` (quick 0.1–0.14s, base 0.16–0.24s, emphasized 0.28–0.42s).

### Step 6 — Save and log

Write components to user path (e.g. `src/components/HeroReveal.tsx`).

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:

```markdown
| YYYY-MM-DD HH:MM | motion-animation | <path> | <pattern> <summary> |
```

Tell the user: "Saved to `[path]`. Logged in `docs/skill-outputs/SKILL-OUTPUTS.md`."

---

## Gotchas

- `AnimatePresence` must wrap the conditional; child needs unique `key` or exit never runs.
- `layout` animates position/size — disable or simplify when `useReducedMotion()` is true on large surfaces.
- `pathLength` animates stroke only — fill reveals need opacity or clipPath.
- Import from `motion/react` (v11+); `framer-motion` package is the legacy path — do not mix import paths in one file.
- `whileInView` fires once by default — set `viewport={{ once: false }}` only when repeat is intended.
- `LazyMotion strict` throws if `motion` (not `m`) is used inside — breaks tree-shaking benefits.
- Spring is default for `x`/`y`/`scale` — override with `transition={{ type: 'tween', duration: 0.2 }}` for token-aligned UI motion.

---

## Example

<examples>
  <example>
    <input>Stagger feature cards into view on scroll in a Next.js landing page</input>
    <output>
Delivery: React client component. Container `motion.div` with `variants` (`hidden`/`show`, `staggerChildren: 0.08`), children `motion.article` with `whileInView="show"` + `viewport={{ once: true, margin: '-80px' }}`, `MotionConfig reducedMotion="user"` at layout. Full code in `references/examples.md` Ex.2.
    </output>
  </example>
</examples>

See `references/examples.md` for AnimatePresence modal, SVG pathLength, and layoutId.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Motion works in README SVG" | No JS runtime in embeds — use `svg-creation` SMIL. |
| "Skip AnimatePresence for modals" | Without it, close animation never runs — jarring UX. |
| "Framer Motion import is fine everywhere" | New projects use `motion/react`; legacy may use `framer-motion` — pick one per repo. |
| "GSAP and Motion interchangeably" | Motion = declarative React; GSAP = timelines, scroll pin, Vue/vanilla. Match stack. |
| "layout on everything" | Layout animations are expensive — reserve for meaningful reorder/shared elements. |

## Verification

- [ ] Delivery context is React inline DOM (not `<img>` / README / Vue)
- [ ] `'use client'` present in Next.js App Router files
- [ ] Reduced motion handled (`MotionConfig` and/or `useReducedMotion`)
- [ ] Exit animations use `AnimatePresence` + `key`
- [ ] File saved and `SKILL-OUTPUTS.md` updated when writing to disk

## Reference Files

- **`references/react-patterns.md`** — variants, AnimatePresence, LazyMotion, gestures (read Step 2–3)
- **`references/svg-and-scroll.md`** — pathLength, useScroll, whileInView, reduced-motion parallax (read Step 4)
- **`references/examples.md`** — stagger reveal, modal exit, SVG draw, layoutId (read when pattern unclear)

---

## Impact Report

```
Motion animation: [name] | Pattern: [enter|stagger|exit|layout|scroll|pathLength]
Framework: react | Import: [motion/react|framer-motion]
File: [path] | Reduced-motion: [MotionConfig|useReducedMotion|both]
Logged: [yes|no]
```
