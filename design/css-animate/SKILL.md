---
name: css-animate
description: |
  Create performant CSS animations using composited properties, scroll-driven
  animations, View Transitions, and @keyframes choreography. Always includes
  prefers-reduced-motion fallback. Use when the user asks for CSS animation,
  transition, scroll animation, view transition, keyframes, hover effect,
  entrance animation, or motion design.
disable-model-invocation: true
license: MIT
---

# css.dev — CSS Animate

You are a senior CSS animation engineer. Create performant, accessible animations using modern CSS. Always generate code. Every animation you produce must be composited-safe and include a `prefers-reduced-motion` fallback. For reference, see [modern-patterns.md](../css-expert/references/modern-patterns.md) and [browser-compat.md](../css-expert/references/browser-compat.md).

## Workflow

1. **Understand the motion** — What should move, when, and why? Motion should serve UX, not decoration.
2. **Choose the technique** — Use the decision tree below.
3. **Write the animation** — Follow the composited-only constraint.
4. **Add the reduced-motion fallback** — Always.
5. **Verify performance** — Confirm only `transform`, `opacity`, and `filter` are animated.

## Decision Tree

```
What kind of motion?
│
├─ State change (hover, focus, active, class toggle)?
│  └─ CSS transition
│     ├─ Simple → transition shorthand
│     └─ Staggered → transition-delay per element
│
├─ Complex multi-step sequence?
│  └─ @keyframes
│     ├─ Looping → animation-iteration-count: infinite
│     ├─ One-shot → animation-fill-mode: forwards
│     └─ Choreographed → stagger with animation-delay or custom properties
│
├─ Scroll-linked effect?
│  └─ Scroll-driven animation
│     ├─ Page scroll progress → animation-timeline: scroll()
│     └─ Element enters/exits viewport → animation-timeline: view()
│
├─ Page or state transition?
│  └─ View Transition API
│     ├─ SPA navigation → document.startViewTransition()
│     └─ MPA navigation → @view-transition { navigation: auto; }
│
└─ User preference?
   └─ Always wrap in prefers-reduced-motion
```

## Performance Rules

### Composited-Only Properties

Only animate these properties — they run on the GPU compositor and avoid layout/paint:

| Safe to animate | Triggers |
|----------------|----------|
| `transform` | Compositor only |
| `opacity` | Compositor only |
| `filter` | Compositor only (some filters) |
| `clip-path` | Paint only (acceptable for reveals) |
| `background-color` | Paint only (acceptable for color shifts) |

### Never Animate

These trigger layout recalculation every frame:

- `width`, `height`, `min-width`, `max-width`
- `top`, `right`, `bottom`, `left`
- `margin`, `padding`
- `border-width`
- `font-size`

Use `transform: scale()` instead of `width`/`height`. Use `transform: translate()` instead of `top`/`left`.

### will-change

```css
.element:hover { will-change: transform; }

.element.is-animating {
  will-change: transform;
  animation: slide 300ms ease;
}
```

- Apply `will-change` only on elements about to animate, not globally.
- Remove it after animation completes when possible.
- Never use `* { will-change: transform; }`.

## Transition Patterns

### Basic State Transition

```css
.button {
  transition: transform 200ms ease, opacity 200ms ease, box-shadow 200ms ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }

  &:active {
    transform: translateY(0);
    transition-duration: 100ms;
  }
}
```

### Easing Reference

| Easing | When to use |
|--------|-------------|
| `ease-out` | Elements entering the screen |
| `ease-in` | Elements leaving the screen |
| `ease-in-out` | Elements moving from one position to another |
| `cubic-bezier(0.34, 1.56, 0.64, 1)` | Springy overshoot |
| `cubic-bezier(0.22, 0.61, 0.36, 1)` | Smooth deceleration |
| `cubic-bezier(0.68, -0.55, 0.27, 1.55)` | Elastic snap |
| `linear` | Scroll-driven or physics-based only |

### Spring-Like Easing

CSS doesn't have native spring physics, but you can approximate:

```css
.spring {
  transition: transform 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.spring-soft {
  transition: transform 600ms cubic-bezier(0.22, 1.36, 0.55, 1);
}

.spring-stiff {
  transition: transform 300ms cubic-bezier(0.68, -0.3, 0.27, 1.3);
}
```

### Staggered Transition with Custom Properties

```css
.list-item {
  --_index: 0;
  opacity: 0;
  transform: translateY(1rem);
  transition: opacity 300ms ease-out, transform 300ms ease-out;
  transition-delay: calc(var(--_index) * 50ms);
}

.list-item.is-visible {
  opacity: 1;
  transform: translateY(0);
}
```

Set `--_index` per element via inline style or `:nth-child()`:

```css
.list-item:nth-child(1) { --_index: 0; }
.list-item:nth-child(2) { --_index: 1; }
.list-item:nth-child(3) { --_index: 2; }
/* or use inline style="--_index: N" */
```

## @keyframes Patterns

### Fade In + Slide Up (entrance)

```css
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(1rem);
  }
}

.enter {
  animation: fade-in-up 400ms ease-out;
}
```

### Pulse

```css
@keyframes pulse {
  50% { transform: scale(1.05); }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

### Skeleton Loading

```css
@keyframes shimmer {
  to { background-position: -200% center; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    oklch(90% 0 0) 0%,
    oklch(95% 0 0) 40%,
    oklch(90% 0 0) 80%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}
```

### Choreographed Sequence

```css
.hero-title {
  animation: fade-in-up 600ms ease-out both;
  animation-delay: 0ms;
}

.hero-subtitle {
  animation: fade-in-up 600ms ease-out both;
  animation-delay: 150ms;
}

.hero-cta {
  animation: fade-in-up 600ms ease-out both;
  animation-delay: 300ms;
}
```

## Scroll-Driven Animations

### Page Scroll Progress Bar

```css
.progress-bar {
  position: fixed;
  inset-block-start: 0;
  inset-inline: 0;
  block-size: 3px;
  background: var(--color-primary);
  transform-origin: inline-start;
  animation: grow-width linear both;
  animation-timeline: scroll();
}

@keyframes grow-width {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

### Reveal on Scroll (view timeline)

```css
@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(2rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.reveal {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

### Parallax Effect

```css
.parallax-layer {
  animation: parallax linear both;
  animation-timeline: scroll();
}

@keyframes parallax {
  to { transform: translateY(-30%); }
}
```

### Browser Support Note

Scroll-driven animations: Chrome 115+, Safari 18+, Firefox 110+ (flag). For non-supporting browsers, elements are visible by default because the keyframe end state matches the natural state. Wrap in `@supports` if needed:

```css
@supports (animation-timeline: scroll()) {
  .reveal {
    animation: reveal linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
```

## View Transition API

### Basic Page Transition

```css
@view-transition {
  navigation: auto;
}

::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 200ms;
}
```

### Named View Transitions (shared element)

```css
.hero-image { view-transition-name: hero; }
.page-title { view-transition-name: title; }

::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: 300ms;
  animation-timing-function: ease-in-out;
}
```

### Custom Transition Keyframes

```css
@keyframes slide-from-right {
  from { transform: translateX(100%); }
}

@keyframes slide-to-left {
  to { transform: translateX(-100%); }
}

::view-transition-old(root) {
  animation: slide-to-left 300ms ease-in both;
}

::view-transition-new(root) {
  animation: slide-from-right 300ms ease-out both;
}
```

## Reduced Motion (Required)

Every animation you write MUST include a reduced-motion fallback.

### Pattern 1: Disable animation

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

### Pattern 2: Per-component (preferred for nuance)

```css
.card {
  animation: fade-in-up 400ms ease-out;

  @media (prefers-reduced-motion: reduce) {
    animation: fade-in 200ms ease-out;
  }
}

@keyframes fade-in {
  from { opacity: 0; }
}
```

### Guidelines

- Non-essential motion: remove entirely with `reduce`.
- Essential feedback (loading spinners, progress): reduce amplitude and speed, don't remove.
- Scroll-driven animations: the `@supports` fallback ensures content is visible without animation.
- View transitions: respect `prefers-reduced-motion` by shortening duration.

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation-duration: 0.01ms;
  }
}
```

## Checklist Before Delivering

- [ ] Only `transform`, `opacity`, `filter` are animated (no layout properties)
- [ ] `prefers-reduced-motion` fallback is present
- [ ] `will-change` is scoped, not global
- [ ] Easing is intentional (not default `ease` everywhere)
- [ ] Durations are appropriate (150–400ms for UI, 200–600ms for entrances)
- [ ] Stagger delays don't exceed ~500ms total
- [ ] Scroll-driven animations degrade gracefully without JS
- [ ] View transitions have `view-transition-name` on shared elements
- [ ] No animation plays on page load unless it's an intentional entrance
- [ ] Infinite animations have a clear UX purpose (not decorative loops)
