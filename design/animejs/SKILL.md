---
name: animejs
description: >
  anime.js v4 usage patterns — imperative JS animation timelines, SVG line drawing, stagger
  grids, and text effects (scrambleText, splitText). Use when a request needs anime.js,
  animejs, timeline animation, stagger, SVG line draw, scramble text, or a lightweight
  Framer Motion alternative outside React or under bundle-size pressure. Not the default —
  Framer Motion remains ui-engineer's React-declarative default; reach for this skill only
  for imperative timelines, SVG draw, stagger grids, text-scramble/reveal effects, or
  non-React contexts. For CSS-only micro-interactions use motion-and-transitions instead.
allowed-tools: Read, Glob, Grep
---


# anime.js (v4)

anime.js is a small (~10-24 kB), MIT-licensed, imperative JavaScript animation engine. It is
NOT a replacement for Framer Motion — it is an opt-in alternative for the class of work Framer
Motion handles poorly: imperative timelines, SVG path drawing, stagger grids, and text effects
(scramble/split), and it works outside React (vanilla JS, non-React frameworks).

## Decision table — which motion tool

| Need | Use |
|---|---|
| CSS-only micro-interaction (hover, open/close, modal, badge) | `motion-and-transitions` |
| React-declarative animation (the ui-engineer default) | Framer Motion |
| Imperative JS timeline, SVG line draw, stagger grid, text scramble/reveal | **anime.js** (this skill) |
| Non-React context, or bundle-size-sensitive (vanilla JS, static HTML, explainer pages) | **anime.js** (this skill) |

If none of the last two rows apply, you almost certainly want Framer Motion or
`motion-and-transitions` instead — do not reach for a second animation library by default.

## Reuse search (recon 2026-07-12)

`rg -il "anime|scramble"` across `rules/ commands/ skills/ agents/ scripts/ docs/` before
authoring this skill found no existing corpus surface owning anime.js usage: `motion-core.md`
documents GSAP-Club recipes only, `wayfinder/references/libraries.md` pins anime.js
**v3.2.2** (no text module — see `references/text-effects.md` for the v3-vs-v4 API rewrite),
and `frontend-design`'s `references/aceternity/` owns React text-effect components on Framer
Motion. Full recon:
`docs/recon/animejs-text-scrambletext.md`.

## Core v4 API

```javascript
import { animate, createTimeline, stagger } from 'animejs';

// Single animation
animate('.box', {
  translateX: 250,
  rotate: '1turn',
  duration: 800,
  ease: 'inOut(3)', // named easing, or a custom cubic-bezier string
});

// Timeline — sequence + stagger
createTimeline({ defaults: { duration: 650, ease: 'inOut(3)' } })
  .add('.item', { opacity: [0, 1], y: [20, 0] }, stagger(80));
```

- `animate(target, params)` — the core tween function. `target` is a CSS selector, DOM node,
  NodeList, or array of any of those.
- `createTimeline(params)` — sequences multiple `animate` calls; `.add(target, params, position)`
  chains steps. `position` accepts an offset (`'+=100'`) or a `stagger(...)` value.
- `stagger(value, opts?)` — distributes a delay across a target set (grid stagger, list
  stagger). Composes with both `animate` and timeline `.add`.
- `ease` — named presets (`'inOut(3)'`, `'outExpo'`, etc.) or a custom bezier/spring string.
  v4 is a full API rewrite vs v3's global `anime()` function — do not copy v3 snippets
  (`anime({...})`) into v4 code.

## React integration pattern

```tsx
import { useEffect, useRef } from 'react';
import { animate } from 'animejs';

function Box() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    const anim = animate(ref.current, { translateX: 250, duration: 800 });
    return () => anim.pause(); // cleanup — prevents a tween firing into an unmounted node
  }, []);

  return <div ref={ref} />;
}
```

Always clean up in the effect's return (pause or revert the animation) — an anime.js instance
has no automatic unmount awareness, unlike Framer Motion's component lifecycle integration.

## Mandatory: `prefers-reduced-motion` guard

Every anime.js animation MUST check the media query before running, same convention as
`motion-and-transitions` and `wayfinder`:

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  animate('.box', { translateX: 250, duration: 800 });
} else {
  // set the end state directly, no animation
}
```

## NEVER

- **NEVER** mix v3's global `anime({...})` call style with v4 named imports — they are
  different APIs on different major versions; a copy-pasted v3 snippet silently fails against
  the v4 package (no shared global to call).
- **NEVER** target `scrambleText()` at `textContent` — it MUST drive `innerHTML`. Targeting
  `textContent` compiles fine and silently no-ops (no scramble, no error, no console warning) —
  see `references/text-effects.md` for the full footgun.
- **NEVER** skip the effect cleanup in a React `useEffect` return — unlike Framer Motion,
  anime.js has no component-lifecycle awareness; an animation left running past unmount keeps
  ticking against a detached node.
- **NEVER** ship an anime.js animation without the `prefers-reduced-motion` guard above — this
  is a hard requirement, not a nice-to-have, matching `motion-and-transitions` and
  `wayfinder` convention.
- **NEVER** reach for anime.js as a second general-purpose animation library "just in case" —
  it is scoped to imperative timelines / SVG draw / stagger grids / text effects / non-React
  contexts. A request that doesn't need one of those almost always wants Framer Motion instead.

## Text effects (scrambleText, splitText)

**MANDATORY**: read `references/text-effects.md` before writing any `scrambleText`/`splitText`
call — the full parameter table, the `innerHTML`-not-`textContent` footgun, `seed` for
deterministic replay, and `splitText`'s `accessible` setting all live there. Do not guess
parameter names from the snippets in this file alone.

## Related skills

- `motion-and-transitions` — CSS-only micro-interactions (default for hover/open/close/modal).
- `frontend-design` § `references/motion-core.md` — GSAP-based React component recipes, plus
  the free-path (anime.js) alternative to the 4 GSAP-Club-gated text components.
- `wayfinder` § `references/libraries.md` — anime.js v3.2.2 CDN pin for explainer HTML
  pages, plus the additive v4 text-scramble subsection.
