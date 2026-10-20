---
name: motion-discipline
description: Enforce the calm-motion rule across every animation, transition, and micro-interaction. 200ms ease-out default, no spring, no bounce, no overshoot, respect prefers-reduced-motion. Audit Framer Motion and CSS transitions. Use when adding animation, reviewing motion, or auditing a component library.
---

# Skill: Motion Discipline

Motion is a trust signal. Bouncy, springy, overshooting animations read as "consumer app" — wrong register for regulatory work. Concept2Cure's motion budget is small on purpose.

This skill pairs with `claude-ui-design-principles` (principle 5: "Animation: Brief & Purposeful").

## Activation

This skill activates when:

- Adding any animation, transition, or micro-interaction
- Importing or using `framer-motion`, `react-spring`, `@react-spring/*`, `lottie-react`, or GSAP
- Writing `transition`, `animation`, `@keyframes`, or `animate-*` Tailwind classes
- Auditing a component library or reviewing motion behavior

## Hard Rules (NON-NEGOTIABLE)

1. **Default curve: `ease-out`**. Content arrives calmly and decelerates. Never `ease-in` for entrances (feels sluggish), never `linear` for UI (feels mechanical), never custom spring/bounce curves.
2. **Default duration: 200ms**. Smaller (120–180ms) for lightweight state changes (hover, press). Never > 300ms for routine UI. Exception: content-shaped skeleton pulses and intentional waits.
3. **No spring physics, no bounce, no overshoot**. Do NOT use Framer Motion's `type: "spring"`, stiffness/damping, or any easing that overshoots the target. Prohibited curves: `cubic-bezier(.68,-0.55,.27,1.55)`, `ease-in-out` with bounce, elastic.
4. **Respect `prefers-reduced-motion`**. Every animation > 120ms MUST have a reduced-motion path that either disables the animation or replaces it with a static cross-fade ≤ 120ms.
5. **Motion has purpose**. Every animation answers one of: "what arrived?", "what changed?", "where did it go?", "what's loading?". If it doesn't answer one of those, delete it.
6. **No chained entrance animations**. Page/panel entrances stagger at most 2 elements. No cascading ripple effects, no serial fade-ins across 10 cards.
7. **No attention-seeking idle motion**. No pulsing "Click me" buttons, no bouncing new-badge indicators, no shimmering brand marks. Idle UI is still.
8. **Skeleton pulses are allowed** but use a slow opacity shift (1000–1500ms ease-in-out on `opacity` only). No moving gradient "shimmer" bars unless already present in the design system.
9. **Transform + opacity only**. Animate `transform` and `opacity`. Do NOT animate `width`, `height`, `top`, `left`, `margin` — they trigger layout. Use `scale`, `translate`, or a governed layout primitive.
10. **No parallax, no 3D tilt, no magnetic cursor effects**. Not our register.

## Canonical Values

```ts
// tokens (target values — extend Tailwind config if missing)
const motion = {
  duration: {
    instant: 0,       // prefers-reduced-motion
    micro:   120,     // hover, press
    default: 200,     // state changes, reveals
    deliberate: 300,  // page transitions (max)
  },
  easing: {
    out: 'cubic-bezier(0.16, 1, 0.3, 1)',  // ease-out, calm
    inOut: 'cubic-bezier(0.4, 0, 0.2, 1)', // for crossfades
    // spring, bounce, elastic are NOT defined on purpose
  },
};
```

```tsx
// React pattern — Framer Motion
<motion.div
  initial={{ opacity: 0, y: 4 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: 4 }}
  transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
>
```

```css
/* CSS pattern */
.panel {
  transition: opacity 200ms cubic-bezier(0.16, 1, 0.3, 1),
              transform 200ms cubic-bezier(0.16, 1, 0.3, 1);
}

@media (prefers-reduced-motion: reduce) {
  .panel {
    transition-duration: 0ms;
  }
}
```

## Before Shipping Motion, Verify

- Is the duration ≤ 200ms (or ≤ 300ms for a page-level transition)?
- Is the easing `ease-out` (or a calm `ease-in-out` for crossfades)?
- Does it respect `prefers-reduced-motion`?
- Does the animation answer one of: arrival, change, exit, loading?
- Is only `transform` and `opacity` animated (no layout properties)?
- Is the motion still on idle (no attention-seeking pulses)?

## Forbidden Patterns

| Forbidden | Use Instead |
| --- | --- |
| `type: "spring"` in Framer Motion | `transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}` |
| `cubic-bezier(.68,-0.55,.27,1.55)` (bounce) | `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out) |
| Animating `width`, `height`, `top`, `left` | Animate `scale`, `translate`; or no animation |
| 500ms+ transitions on routine UI | 200ms default |
| `animate-bounce`, `animate-ping`, `animate-spin` on idle elements | Remove; use a content-shaped skeleton if loading |
| No `prefers-reduced-motion` branch | `@media (prefers-reduced-motion: reduce) { transition: none; }` |
| Staggered entrance on 10+ elements | At most 2-element stagger, or single group fade |
| Lottie animations in regulated views | Static illustration or none |
| Parallax / 3D tilt / magnetic cursor | Delete |
| `transition-all` | Specific property list |

## Tooling

- **Grep audit**: search for `type: "spring"`, `cubic-bezier`, `animate-bounce`, `animate-ping`, `transition-all`, `@keyframes` — review each hit against the rules above.
- **Reduced-motion pass**: toggle OS setting (macOS: System Settings → Accessibility → Display → Reduce motion) and re-walk the primary flows.
- **Frame-rate check**: if any animation drops below 60fps on a mid-tier laptop, shorten or cut it.

## Completion Gate

Motion is NOT done until:

- Every animation passes the 6-question check above
- No spring / bounce / overshoot in the diff
- Every animation > 120ms has a reduced-motion path
- No layout-triggering properties animated
- No idle attention-seeking motion

When in doubt, cut the animation. A still UI is always better than a chirpy one.
