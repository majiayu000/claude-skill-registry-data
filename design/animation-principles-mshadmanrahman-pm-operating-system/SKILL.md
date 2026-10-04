---
name: animation-principles
description: "Disney's 12 animation principles applied to web and mobile UI. Use when implementing CSS animations, JS transitions, micro-interactions, page transitions, loading states, hover effects, or motion design. Covers timing, easing, accessibility (prefers-reduced-motion), and framework patterns (Framer Motion, CSS native, GSAP). Triggers: animate, transition, motion, hover effect, loading animation, page transition, micro-interaction, easing, spring physics."
---

# Animation Principles for UI

Disney's 12 animation principles adapted for web and mobile interfaces. Based on [dylantarre/animation-principles](https://github.com/dylantarre/animation-principles).

## The 12 Principles: Web Implementation

| # | Principle | Web Implementation | When to Use |
|---|-----------|-------------------|-------------|
| 1 | **Squash & Stretch** | `transform: scale()` on interaction states | Button press, toggle bounce, badge update |
| 2 | **Anticipation** | Slight reverse movement before action | Dropdown opens, drag start, navigation |
| 3 | **Staging** | Focus attention via motion hierarchy | Modal focus, form field activation |
| 4 | **Straight Ahead / Pose to Pose** | JS frame-by-frame vs CSS keyframes | Progress (straight) vs state snaps (pose) |
| 5 | **Follow Through / Overlapping** | Staggered child animations, elastic easing | Menu items, list entries, content settle |
| 6 | **Slow In / Slow Out** | `ease-in-out`, cubic-bezier curves | Every UI transition (never use `linear`) |
| 7 | **Arc** | `motion-path` or bezier translate transforms | Toggle switches, circular menus |
| 8 | **Secondary Action** | Shadows, glows responding to primary motion | Button shadow on hover, icon color shift |
| 9 | **Timing** | Duration ranges per interaction type | See timing table below |
| 10 | **Exaggeration** | Scale beyond 1.0, overshoot animations | Emphasis moments, error shakes |
| 11 | **Solid Drawing** | Consistent transform-origin, 3D perspective | All transforms need correct origin |
| 12 | **Appeal** | Smooth 60fps, purposeful motion | Every animation must have a reason |

## Principle Details

**Squash & Stretch**: Apply `scaleY` compression on button press, `scaleX` stretch on hover. Keep volume constant: if you compress Y, expand X slightly. Keep subtle in UI; this is interfaces, not cartoons.

**Anticipation**: Before expanding a dropdown, shrink it 2-3% first. Before sliding content left, move it 5px right. Hover states prepare for click. Draggable items elevate on grab start.

**Staging**: Dim background elements during modal focus. Use motion to direct eye flow: animate important elements first. Active form fields are clearly distinguished. One interaction feedback at a time.

**Straight Ahead vs Pose to Pose**: Use CSS `@keyframes` for predictable, repeatable animations (pose to pose). Use JavaScript/GSAP for dynamic, physics-based motion (straight ahead). Progress indicators = straight ahead. Checkboxes = pose to pose.

**Follow Through & Overlapping**: Child elements complete movement after parent stops. Use `animation-delay` with decreasing values for natural stagger (30-50ms per item). Ripple effects expand past tap point. Toggle switches overshoot then settle.

**Slow In / Slow Out**: Never use `linear` for UI motion. Standard: `cubic-bezier(0.4, 0, 0.2, 1)`. Enter: `cubic-bezier(0, 0, 0.2, 1)` (ease-out). Exit: `cubic-bezier(0.4, 0, 1, 1)` (ease-in). Exit animations shorter than enter (~60-70% of enter duration).

**Arc**: Elements in nature move in arcs, not straight lines. Use `offset-path` or combine X/Y transforms with different easings. Toggle switches travel in slight arc. Circular action buttons expand radially.

**Secondary Action**: Button shadow grows/blurs on hover. Icon inside button rotates while button scales. Background particles respond to primary element. Shadow responds to elevation changes.

**Timing**: See the complete timing reference table below. Micro-interactions: 100-200ms. Standard transitions: 200-400ms. Complex sequences: 400-700ms.

**Exaggeration**: Hover states scale to 1.05-1.1, not 1.01. Error shakes move 10-20px, not 2px. Make motion noticeable but not jarring. Save theatrics for key moments (onboarding, achievement).

**Solid Drawing**: Maintain consistent `transform-origin`. Use `perspective` for 3D depth. Avoid conflicting transforms. Buttons scale from center, tooltips from pointer.

**Appeal**: Target 60fps using `transform` and `opacity` only. Add personality through custom easing curves. Motion should feel intentional: if you can't explain why something animates, remove it.

## Timing Reference

### By Interaction Type

| Interaction | Duration | Easing |
|-------------|----------|--------|
| Hover | 100ms | ease-out |
| Click/tap feedback | 100ms | ease-out |
| Toggle switch | 150-200ms | spring/elastic |
| Checkbox | 150ms | ease-out |
| Focus ring | 100ms | ease-out |
| Tooltip show | 150ms | ease-out |
| Tooltip hide | 100ms | ease-in |
| Badge update | 200ms | elastic |
| Form error | 200ms | ease-out |
| Dropdown open | 200-300ms | ease-out |
| Modal open | 250-350ms | ease-out |
| Modal close | 200-300ms | ease-in |
| Page slide forward | 300-400ms | ease-out |
| Page slide back | 250-350ms | ease-out |
| Tab switch | 150-200ms | ease-out |
| Shared element | 300-400ms | ease-in-out |

### By Time Scale

| Scale | Duration | Use For | Easing |
|-------|----------|---------|--------|
| Instant | 0-100ms | Hover, focus, tap feedback, ripples | `ease-out` or step |
| Micro | 100-200ms | Toggles, checkboxes, tooltips, badges | `ease-out`, `cubic-bezier(0.2, 0, 0, 1)` |
| Small | 200-300ms | Dropdowns, accordions, slides, fades | `ease-out`, spring |
| Medium | 300-500ms | Page transitions, modals, drawers | `ease-in-out`, `cubic-bezier(0.4, 0, 0.2, 1)` |
| Large | 500-800ms | Complex sequences, onboarding reveals | `cubic-bezier(0.16, 1, 0.3, 1)` |

## Code Patterns

### Micro-interactions

```css
/* Button with squash/stretch */
.button {
  transition: transform 100ms ease-out, box-shadow 100ms ease-out;
}
.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.button:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

/* Toggle switch with overshoot */
.toggle-thumb {
  transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toggle-thumb.active {
  transform: translateX(20px);
}

/* Checkbox draw effect */
.checkmark {
  stroke-dasharray: 20;
  stroke-dashoffset: 20;
  transition: stroke-dashoffset 200ms ease-out 50ms;
}
.checkbox:checked + .checkmark {
  stroke-dashoffset: 0;
}

/* Dropdown with anticipation */
.dropdown-enter {
  animation: dropdown-open 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes dropdown-open {
  0% { transform: scaleY(0.98); opacity: 0; }
  100% { transform: scaleY(1); opacity: 1; }
}
```

### Page Transitions

```css
/* Crossfade (default) */
.page-exit-active {
  opacity: 0;
  transition: opacity 200ms ease-in;
}
.page-enter {
  opacity: 0;
}
.page-enter-active {
  opacity: 1;
  transition: opacity 200ms ease-out;
}

/* Slide (hierarchical navigation) */
.page-enter {
  transform: translateX(100%);
}
.page-enter-active {
  transform: translateX(0);
  transition: transform 300ms ease-out;
}
.page-exit-active {
  transform: translateX(-30%);
  transition: transform 300ms ease-in;
}

/* Shared element (View Transitions API) */
.hero-image {
  view-transition-name: hero;
}
::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: 300ms;
}
```

### Stagger Pattern

```css
/* List items entering with stagger */
.list-item {
  opacity: 0;
  transform: translateY(10px);
  animation: stagger-in 300ms ease-out forwards;
}
.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 40ms; }
.list-item:nth-child(3) { animation-delay: 80ms; }
.list-item:nth-child(4) { animation-delay: 120ms; }

@keyframes stagger-in {
  to { opacity: 1; transform: translateY(0); }
}
```

### Framer Motion (React)

```tsx
/* Spring-based animation */
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -10 }}
  transition={{ type: "spring", stiffness: 300, damping: 24 }}
/>

/* Stagger children */
<motion.ul variants={{
  show: { transition: { staggerChildren: 0.05 } }
}}>
  <motion.li variants={{
    hidden: { opacity: 0, y: 10 },
    show: { opacity: 1, y: 0 }
  }} />
</motion.ul>

/* Layout animation (shared element) */
<motion.div layoutId="hero-card" />

/* Reduced motion */
const prefersReducedMotion = useReducedMotion();
<motion.div
  animate={{ x: 100 }}
  transition={prefersReducedMotion ? { duration: 0 } : { type: "spring" }}
/>
```

## Easing Reference

| Name | CSS Value | Use |
|------|-----------|-----|
| Standard | `cubic-bezier(0.4, 0, 0.2, 1)` | General purpose |
| Enter (decelerate) | `cubic-bezier(0, 0, 0.2, 1)` | Elements appearing |
| Exit (accelerate) | `cubic-bezier(0.4, 0, 1, 1)` | Elements leaving |
| Sharp | `cubic-bezier(0.4, 0, 0.6, 1)` | Quick, snappy |
| Overshoot | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful, bouncy |
| Smooth out | `cubic-bezier(0.16, 1, 0.3, 1)` | Elegant settle |
| Spring (CSS approx) | `cubic-bezier(0.175, 0.885, 0.32, 1.275)` | Natural feel |

## Navigation Direction Model

| Pattern | Transition | Direction |
|---------|------------|-----------|
| Drill-down (list to detail) | Slide left / shared element | Right = forward |
| Tab bar | Fade / horizontal slide | Follows tab position |
| Bottom sheet | Slide up from bottom | Vertical |
| Modal | Scale + fade from trigger | Z-axis |
| Back button | Reverse of forward | Left = back |
| Forward navigation | Animate left/up | Deeper into hierarchy |
| Backward navigation | Animate right/down | Toward home |

## Accessibility: Reduced Motion

### CSS Implementation

```css
/* Default: full animation */
.element {
  transition: transform 300ms ease-out;
}

/* Reduced motion: replace with opacity or instant */
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: opacity 200ms ease-out;
    /* Or: transition: none; */
  }

  /* Kill all animations globally */
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Safe vs Harmful Motion

| Safe | Potentially Harmful | Always Avoid |
|------|-------------------|--------------|
| Opacity fades | Parallax scrolling | Auto-playing video backgrounds |
| Color transitions | Background movement | Infinite looping animations |
| Small scale (<5%) | Zoom animations | Flashing (seizure risk) |
| Very slow movement (500ms+) | Spinning/rotating | Rapid zoom in/out |
| Non-repeating animations | Fast repeated animations | >3 flashes per second |
| | Large moving areas (>1/4 viewport) | Vestibular-triggering patterns |

### WCAG Compliance

- **2.3.3**: Motion from interactions can be disabled unless essential
- **2.2.2**: Moving content >5 seconds must be pausable
- **2.3.1**: No content flashes >3 times per second

## Performance Rules

1. Animate only `transform` and `opacity` for GPU acceleration
2. Use `will-change` sparingly; remove after animation completes
3. Prefer CSS over JavaScript when animation is predictable
4. Keep per-frame work under ~16ms for 60fps
5. Test on low-powered devices
6. Debounce scroll/resize-triggered animations
7. Use `requestAnimationFrame` for JS animations
8. Virtualize animated lists with 50+ items

## Pre-Delivery Checklist

- [ ] `prefers-reduced-motion` respected globally
- [ ] All animations have reduced/no-motion alternative
- [ ] No auto-playing motion over 5 seconds
- [ ] Every interactive element has feedback (hover, active, focus)
- [ ] Disabled states have no animation, reduced opacity
- [ ] Exit animations are shorter than enter (~60-70%)
- [ ] No `linear` easing on UI transitions
- [ ] Only `transform` and `opacity` animated (no width/height/top/left)
- [ ] Stagger delay is 30-50ms per item (not simultaneous)
- [ ] No animation blocks user input
- [ ] Animations are interruptible (user gesture cancels in-progress motion)
- [ ] Motion direction is consistent with navigation model
