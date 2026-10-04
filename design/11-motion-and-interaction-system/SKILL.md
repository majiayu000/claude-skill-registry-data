---
name: "motion-and-interaction-system"
description: "Meaning-first animation with 3-tier hierarchy. CSS scroll-driven (animation-timeline: scroll()), View Transitions API, @starting-style DOM-insert, container scroll-state queries, prefers-reduced-motion mandatory on all animations."
metadata:
  version: "2.1.0"
  updated: "2026-05-03"
  effort: "medium"
  model: "sonnet"
license: "Rutgers"
compatibility:
  claude-code: ">=2.0.0"
  agentskills: ">=1.0.0"
submodules:
  - build-breaking-rules.md
priority: 3
pack: "design"
stage: beta
triggers:
  - "motion"
  - "animation"
  - "transition"
paths:
  - "org:website_build"
---

# 11 — Motion and Interaction System

Apply meaning-first CSS animations (scroll-driven, View Transitions, `@starting-style`) with mandatory `prefers-reduced-motion` on every animated surface.

## Motion serves one of three purposes

1. **Feedback** — confirm user action (button press, form submit, save)
2. **Continuity** — preserve spatial context across state changes (page transition, modal open)
3. **Delight** — express brand personality (hero parallax, signature reveal)

Anything else = AI slop. Cut it.

## 3-Tier Hierarchy

- **Tier 1 — Functional** — feedback on every interaction (hover, focus, active, tap). Duration 100–200ms. Transform/opacity only.
- **Tier 2 — Choreographic** — page transitions, modal entrance, section reveal. Duration 300–500ms. View Transitions or `@starting-style`.
- **Tier 3 — Cinematic** — hero parallax, signature reveal, scroll-driven storytelling. Duration ≥600ms. Scroll-timeline.

Never stack 3 tiers on same surface. One cinematic per page.

## Mandatory `prefers-reduced-motion`

EVERY animation MUST honor `prefers-reduced-motion: reduce` — snap to final state, never hide content.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## View Transitions API

- Same-document SPA: `document.startViewTransition(() => updateDOM())`
- Cross-document MPA: `@view-transition { navigation: auto; }` in CSS
- Per-element: `view-transition-name: hero-image;` on persistent elements
- Chrome 126+, Safari 18+, Firefox 144 (Oct 2025)

```css
::view-transition-old(root), ::view-transition-new(root) {
  animation-duration: 0.3s;
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
```

## Scroll-Driven Animations

- `animation-timeline: scroll()` (root scroller) or `view()` (element-in-viewport)
- Off-main-thread on Chrome stable + Safari 26 (2025)
- Firefox unsupported — pair with `prefers-reduced-motion` AND `duration:1ms` fallback

```css
@keyframes fade-up { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.reveal { animation: fade-up linear; animation-timeline: view(); animation-range: entry 0% cover 30%; }
```

## `@starting-style` (DOM-insert animation)

Baseline 2026 — animates from explicit starting state to default state when element enters DOM.

```css
.toast { opacity: 1; transform: translateY(0); transition: opacity 0.3s, transform 0.3s; }
@starting-style { .toast { opacity: 0; transform: translateY(-10px); } }
```

## Container Scroll-State Queries (Baseline 2026)

`@container scroll-state(stuck: top)` — replaces JS scroll-listener-based sticky styling.

```css
.nav { container-type: scroll-state; }
@container scroll-state(stuck: top) { .nav { box-shadow: 0 4px 12px rgba(0,0,0,0.4); } }
```

## Micro-Interactions (Tier 1 patterns)

- **Button press** — `transform: scale(0.98)` on `:active`, 100ms
- **Hover** — `transform: translateY(-1px)` + color shift, 200ms
- **Focus-visible** — 3px brand-accent ring, 2px offset, 0ms (instant)
- **Tap** — haptic feedback via `navigator.vibrate(10)` if supported
- **Toggle** — animated check/cross morph via `<svg>` path interpolation
- **Loading** — pulse 1.2s ease-in-out infinite

## Stagger sequences (no JS needed)

```css
.list-item { animation: fade-up 0.4s ease-out backwards; }
/* OR use sibling-index() (Baseline 2026) */
.list-item { transition-delay: calc((sibling-index() - 1) * 80ms); }
```

## Performance constraints

- Animate `transform` + `opacity` ONLY on hot paths
- `will-change` sparingly (transform, opacity only when actually animated)
- Drop GPU layers after animation completes
- INP target ≤100ms per `_kernel/standards.md#cwv` — animations must not block input

## Interaction polish (every interactive element)

Per `10-experience-and-design-system` § 4-state distinction:

- Default → neutral
- Hover → underline-sweep + color shift + `translateY(-1px)`
- Focus-visible → 3px brand-accent ring 2px offset (distinct from hover)
- Active → `scale(0.98)` + immediate color confirm

Audit gate: Playwright cycles each interactive through 4 states → diff ≥3px pixel-difference or fail.

## Banned motion

- ❌ Uniform fade-in on every element (AI slop tell)
- ❌ Parallax on every section (one cinematic per page)
- ❌ Spinning loaders that don't progress
- ❌ Auto-playing video with sound
- ❌ Carousel auto-rotate (manual swipe only — accessibility)
- ❌ Scroll-jacking that breaks browser back button
- ❌ Animations that block input (INP >100ms)
- ❌ Easter eggs on critical conversion paths

## See submodules: view-transitions.md, scroll-driven.md, micro-interactions.md, reduced-motion.md, build-breaking-rules.md.
