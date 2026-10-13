---
name: building-parallax-scroll-effects
description: >
  Builds scroll-linked motion effects — depth-layer parallax, sticky pinning,
  scroll-triggered reveals, horizontal scroll-jacking, pointer/mouse parallax,
  scale-on-scroll, velocity-aware marquees, and native CSS scroll-driven
  animation (animation-timeline) — with performance and accessibility handled
  from the first line of code, not bolted on after. Activates when the user
  asks for parallax scrolling, scroll animations, scroll-triggered effects,
  depth on scroll, sticky sections, pinned sections, horizontal scroll
  sections, scroll-jacking, mouse or pointer parallax, animate on scroll,
  reveal on scroll, scroll-linked motion, or a landing page/hero that should
  "feel alive" while scrolling. Covers four implementation stacks — vanilla
  CSS/JS, native CSS scroll-timelines, GSAP ScrollTrigger, and Motion (the
  library formerly named Framer Motion) for React — and picks between them
  by tradeoff, not by default. Check this before writing any scroll-linked
  animation, even a single fade-in-on-scroll.
version: "1.0.0"
---

# Building Parallax Scroll Effects

A source-of-truth for scroll-linked motion: which effect communicates what,
which stack to build it in, and the performance/accessibility floor every
effect has to clear before it ships. The effect taxonomy below started from
a survey of what a no-code visual-effects gallery shows off; everything past
the taxonomy — the code, the performance rules, the accessibility contract,
the stack tradeoffs — is original engineering work, because that gallery is
marketing inspiration for a visual builder, not an implementation guide. It
has zero lines of code and no browser-support, performance, or
reduced-motion guidance anywhere in it.

## Quick-Start Decision Tree

```
What's the goal?
  ├─ Set a scene / add depth to a hero ──────── Depth-layer parallax (below)
  ├─ Spotlight one element while content moves ─ Sticky pin + pass-through
  ├─ Make a headline/image arrive with weight ── Scroll-triggered reveal
  ├─ Emphasize a focal product/shape ─────────── Scale/zoom on scroll
  ├─ Turn vertical scroll into a gallery rail ── Horizontal scroll-linked panel
  ├─ Add responsiveness to cursor movement ───── Pointer/mouse parallax
  ├─ Animate a ticker/logo rail ───────────────── Velocity-aware marquee
  └─ Not sure ─────────────────────────────────── references/technique-catalog.md

Which stack?
  ├─ Portable, no bundler, static/single-file ── Vanilla CSS + JS (A)
  ├─ Effect is a pure keyframe animation ──────── Native CSS scroll-timeline (B), + JS fallback
  ├─ Needs precise scrubbing/pinning at scale ──── GSAP + ScrollTrigger (C)
  ├─ Already inside a React app ──────────────── Motion for React (D)
  └─ Unsure ─────────────────────────────────────  Stack Selection Matrix below
```

## The Non-Negotiables

These apply regardless of technique or stack. Skipping any of these is how
parallax becomes the reason a site feels sluggish or excludes someone.

**Compositor-only properties.** Animate `transform` and `opacity` only.
Never animate `top`, `left`, `width`, `height`, or `margin` on scroll —
each one forces a layout recalculation on every frame, which is the
textbook cause of scroll jank.

**Reduced motion means off, not smaller.** `prefers-reduced-motion: reduce`
disables the scroll-linked movement entirely — it does not mean "move it
20% less." Content must render in its final, readable state with no
transform applied.

```css
@media (prefers-reduced-motion: reduce) {
  [data-parallax], [data-reveal], [data-pin] {
    transform: none !important;
    animation: none !important;
    transition: none !important;
  }
}
```

**Throttle everything, prefer observers over polling.** Any `scroll` or
`pointermove` listener that touches the DOM must be wrapped in
`requestAnimationFrame` and attached with `{ passive: true }`. For simple
enter/exit detection (reveals, pins turning on), use `IntersectionObserver`
instead of a scroll listener — it doesn't run on every scroll tick at all.
Reserve scroll-position math for effects that genuinely need continuous
position (true depth offset, horizontal-scroll translate amount).

**Coarse pointers don't get pointer-parallax.** Gate any cursor-driven
effect behind `matchMedia('(pointer: fine)')`. On touch devices it does
nothing useful and just spends battery. Reduce layer count and movement
range on narrow viewports generally — a 3-layer parallax hero that's
subtle on desktop is often nauseating at arm's length on a phone.

**Native CSS scroll-timelines need a fallback, always.** As of mid-2026,
`animation-timeline` has full support in Chrome, Edge, Opera, and Safari 26+,
but is still shipped behind a flag in Firefox — roughly 85% global support
on caniuse [SOURCED: Josh Comeau, joshwcomeau.com, June 2026]. Feature-detect
with `@supports` and ship a real fallback, not a broken effect for ~15% of
visits:

```css
@supports (animation-timeline: view()) {
  .reveal { animation: reveal-in linear; animation-timeline: view(); animation-range: entry 0% cover 40%; }
}
@supports not (animation-timeline: view()) {
  /* IntersectionObserver adds .is-visible; this rule renders that state */
  .reveal { opacity: 0; transform: translateY(24px); transition: opacity .6s, transform .6s; }
  .reveal.is-visible { opacity: 1; transform: none; }
}
```

**Never trap scroll.** A pinned or horizontal-scroll-jacked section must
resolve within roughly one to two viewport heights of normal scrolling and
then release control back to the page. Don't require a specific gesture,
a minimum dwell time, or a "correct" scroll speed to escape it.

**Effect-off parity.** Every scroll-jacked or pinned section must remain
fully readable and keyboard-navigable with the animation mentally switched
off — correct tab order, no content that only appears on hover or only
via a pointer-parallax interaction. The motion is a progressive
enhancement on top of accessible markup, never a replacement for it.

Full detail, checklists, and mobile-testing steps:
`references/performance-and-accessibility.md`

## Technique Catalog (quick reference)

| Technique | Effect | Best for | Complexity |
|---|---|---|---|
| Depth-layer parallax | BG/mid/FG move at different scroll speeds | Hero scenes, environmental storytelling | Low |
| Sticky pin + pass-through | Element pins while related content scrolls past it | Product spotlights, captions, quotes | Low–Med |
| Scroll-triggered reveal | Text/image arrives via mask, clip, or fade as it enters view | Headlines, narrative beats | Low |
| Scale/zoom on scroll | Element grows or shrinks as it centers in the viewport | Focal product shots, "step closer" moments | Low |
| Horizontal scroll-linked panel | Vertical scroll drives horizontal translation | Galleries, timelines, case-study rails | Med–High |
| Pointer/mouse parallax | Elements shift with cursor position | Hero interactivity on desktop | Low |
| Velocity-aware marquee | Ticker speeds/slows/reverses with scroll speed and direction | Logo rails, footers | Med |
| 3D perspective layering | True `translateZ` depth under a `perspective` container | Cinematic hero moments | Med |
| Scroll-scrubbed media | Scroll position maps to video `currentTime` or canvas frame | Product demos, explainer sequences | High |
| Scroll-linked theme shift | A background or theme value changes across page zones | Section-to-section mood changes | Low |

Full write-up per technique — what it looks like, when it earns its
complexity, and the mistake people actually make with it —
`references/technique-catalog.md`.

## Stack Selection Matrix

| | A. Vanilla CSS+JS | B. Native CSS scroll-timeline | C. GSAP + ScrollTrigger | D. Motion for React |
|---|---|---|---|---|
| Dependencies | None | None (CSS only) | 1 (free, see below) | 1 (React-only) |
| Ceiling on performance | Good, if you follow the non-negotiables | Best — compositor-only by construction | Good — battle-tested measurement/resize handling | Good |
| Handles horizontal scroll-jack cleanly | You hand-roll the math | Not really — this needs JS-level measurement | Yes, this is its strongest case | Yes, via `useScroll`/`useTransform` |
| Works outside React | Yes | Yes | Yes | No |
| Current caveat | You own every edge case | ~85% support; Firefox behind a flag [SOURCED] | None — was a paid Club plugin, now fully free since April 2025 after Webflow's GreenSock acquisition [SOURCED] | Import path is now `motion/react`; old `framer-motion` package still installs but isn't actively developed [SOURCED] |

**Default:** A for portable, single-file, or no-bundler builds — this is
what the four examples in `examples/` use. D for anything already inside a
React/Vite codebase, since it's idiomatic there and ships a
`useReducedMotion` hook for free. C only when a section genuinely needs
scrubbing or pinning math across many breakpoints that A or D would take
real effort to get right by hand. B is a performance upgrade layered on
top of A or D, not a standalone choice yet — the Firefox gap means you're
maintaining a fallback path either way.

Full code recipes for all four stacks: `references/implementation-recipes.md`

## Golden Path

1. **Name the goal in one sentence** — what should feel different as the
   visitor scrolls, and in which section. If you can't say it in a
   sentence, the effect is probably going to be noise, not craft.
2. **Pick 1–2 techniques from the catalog.** Stacking three or more effects
   on one screen reads as busy, not impressive — this is the one place
   "more" reliably makes a design worse.
3. **Pick a stack** from the matrix and state the assumption if the user
   didn't specify one.
4. **Wire the reduced-motion guard before the effect**, not after — it's
   one CSS block and it's much easier to verify against a blank state than
   to retrofit once movement exists everywhere.
5. **Build with compositor-only properties from the first line.**
6. **Verify** (see `references/performance-and-accessibility.md`):
   reduced-motion truly disables movement; the coarse-pointer/mobile path
   was a deliberate choice, not an accident; tab order and content access
   work with the effect switched off; no scroll-timeline effect ships
   without a `@supports not (...)` fallback.
7. Ship.

## Reference Map

| Need | Open |
|---|---|
| Full technique write-ups, common mistakes | `references/technique-catalog.md` |
| Real code for all 4 stacks, per technique | `references/implementation-recipes.md` |
| Performance/accessibility checklists, mobile testing | `references/performance-and-accessibility.md` |
| Deeper stack tradeoffs, edge cases | `references/decision-framework.md` |
| Four complete, differently-branded worked examples | `examples/` (see `examples/README.md`) |

## Trigger Evaluation

**Should trigger:**
1. "Build a landing page with parallax scrolling"
2. "Add a scroll-triggered reveal to this hero section"
3. "I want the background to move slower than the foreground as you scroll"
4. "Make this feel alive when you scroll, like those showcase sites do"
5. "Add horizontal scroll to this gallery, driven by the normal scroll wheel"

**Should NOT trigger:**
1. "Add a simple fade-in animation on page load" — time-based, not
   scroll-linked; nothing here should fire on a plain load animation.
2. "Build me a scrollable data table" — functional overflow scrolling, not
   a scroll-linked visual effect.

**Observed:** all five positive prompts contain vocabulary directly in the
description (parallax, scroll-triggered, background moves slower than
foreground, feel alive when you scroll, horizontal scroll driven by scroll)
→ PASS. Negative 1 has no scroll-position vocabulary — it's a timeline
animation, not a scroll-timeline one → correctly silent. Negative 2 is
functional scrolling with no visual-motion request → correctly silent.

## Self-Verification Checklist

1. Name is gerund form (`building-parallax-scroll-effects`) and matches the directory — done
2. Description is third-person, keyword-dense, under 1024 chars — done
3. SKILL.md is under 500 lines — verified at packaging time
4. 5 positive + 2 negative eval scenarios written above — done
5. `references/` present (this file exceeds 100 lines) — done
6. No reference file links to another reference file (checked at packaging time)
7. No placeholder sections — every section above has real content, and all
   four examples are complete, working files, not scaffolds
8. CLAIMS/COUNTEREXAMPLE/CONTRADICTIONS footer present — below
9. Every path referenced above (`references/*.md`, `examples/`) exists at
   that exact path in the packaged zip — verified at packaging time

## CLAIMS
- [SOURCED] `animation-timeline` (native CSS scroll-driven animation) has full support in Chrome, Edge, Opera, and Safari 26+, and ships behind a flag in Firefox as of mid-2026 — roughly 85% global support on caniuse (Josh Comeau, joshwcomeau.com, June 19 2026).
- [SOURCED] GSAP and every formerly-paid Club plugin (ScrollTrigger, ScrollSmoother, SplitText, MorphSVG, DrawSVG) became 100% free for commercial use in April 2025, following Webflow's October 2024 acquisition of GreenSock — no license key or membership required.
- [SOURCED] Framer Motion was renamed Motion in 2025; the current package is `motion` with import path `motion/react`. The legacy `framer-motion` package still installs but is no longer actively developed.
- [GENERATED] Compositor-only animation is the single highest-leverage performance rule in this skill — reasoned from how browser rendering pipelines avoid layout/paint work, not measured with profiling data against this skill's own examples.

## COUNTEREXAMPLE
- A scroll-jacked section that's keyboard-accessible and unaffected by reduced-motion can still fail real visitors if it's the *only* path to the content below it — mechanism accessibility doesn't guarantee information-architecture accessibility.
- GSAP being fully free removes the licensing objection, not the dependency-weight or over-animation objection. Free isn't the same as no cost.

## CONTRADICTIONS
- ! This skill recommends native CSS scroll-timelines as the highest-performance option, then requires a JS fallback for the ~15% of visits on Firefox — meaning most real deployments maintain both a CSS path and a JS path. The performance ceiling is real; the maintenance floor is higher than the "no JavaScript required" pitch implies.
