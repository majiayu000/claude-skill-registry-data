---
name: animation-motion
description: CSS animations, transitions, and scroll-driven effects with accessibility (prefers-reduced-motion). Use when adding motion, hover effects, loading states, or scroll-based animations.
allowed-tools: Read, Write, Edit
---

# Animation & Motion Skill

This skill covers CSS animations and transitions with a focus on accessibility (respecting user motion preferences) and performance (avoiding jank and layout thrashing).

> **Related:** For CSS-only interactive patterns (tabs, accordions, toggles without JavaScript), see the **`progressive-enhancement`** skill.

## Philosophy

Motion should be:

1. **Purposeful** - Guides attention, shows relationships, provides feedback
2. **Respectful** - Honors `prefers-reduced-motion` preferences
3. **Performant** - Uses compositor-only properties when possible
4. **Subtle** - Enhances, doesn't distract or overwhelm

---

## Reduced Motion First

Always start with reduced motion as the default, then add motion for users who haven't opted out.

### The Pattern

```css
/* Base: no motion (reduced motion default) */
.element {
  transition: none;
}

/* Add motion only when user hasn't requested reduced motion */
@media (prefers-reduced-motion: no-preference) {
  .element {
    transition: transform 0.3s ease, opacity 0.3s ease;
  }
}
```

### Why Reduced Motion First?

| Approach | Problem |
|----------|---------|
| Motion first, then remove | Users see flash of motion before media query applies |
| Reduced first, then add | Safe default, motion is progressive enhancement |

---

## Respecting User Preferences

### The `prefers-reduced-motion` Media Query

```css
/* User prefers reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Granular Reduced Motion

Instead of removing all motion, provide alternatives:

```css
/* Full animation for users without preference */
@media (prefers-reduced-motion: no-preference) {
  .card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }
}

/* Subtle alternative for reduced motion */
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: box-shadow 0.15s ease;
  }

  .card:hover {
    box-shadow: var(--shadow-md);
  }
}
```

### JavaScript Detection

```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (prefersReducedMotion) {
  // Use instant transitions or skip animations
  element.style.transition = 'none';
} else {
  // Full animation
  element.animate(keyframes, options);
}
```

---

## Performance-Safe Properties

### Compositor-Only Properties (Fast)

These properties can be animated without triggering layout or paint:

| Property | Use For |
|----------|---------|
| `transform` | Movement, scaling, rotation |
| `opacity` | Fade in/out |
| `filter` | Blur, brightness (GPU accelerated) |

```css
/* GOOD: Compositor-only */
.card:hover {
  transform: translateY(-4px) scale(1.02);
  opacity: 0.9;
}
```

### Properties to Avoid Animating

These trigger expensive layout recalculations:

| Property | Problem |
|----------|---------|
| `width`, `height` | Layout recalc |
| `top`, `left`, `right`, `bottom` | Layout recalc |
| `margin`, `padding` | Layout recalc |
| `border-width` | Layout recalc |
| `font-size` | Layout + text reflow |

```css
/* BAD: Triggers layout */
.card:hover {
  margin-top: -4px;  /* Layout thrashing */
  height: 110%;      /* Layout thrashing */
}

/* GOOD: Use transform instead */
.card:hover {
  transform: translateY(-4px) scaleY(1.1);
}
```

### Promoting to Compositor Layer

Use `will-change` sparingly for known animations:

```css
/* Only use for elements that WILL animate */
.animated-element {
  will-change: transform, opacity;
}

/* Remove after animation completes */
.animated-element.animation-done {
  will-change: auto;
}
```

**Warning:** Don't apply `will-change` to many elements—it consumes memory.

---

## Transition Patterns

### Design Token Integration

```css
:root {
  /* Duration scale */
  --duration-instant: 0.1s;
  --duration-fast: 0.15s;
  --duration-normal: 0.3s;
  --duration-slow: 0.5s;

  /* Easing functions */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### Common Transitions

```css
/* Hover lift effect */
@media (prefers-reduced-motion: no-preference) {
  .card {
    transition:
      transform var(--duration-fast) var(--ease-out),
      box-shadow var(--duration-fast) var(--ease-out);
  }

  .card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
}

/* Focus ring */
@media (prefers-reduced-motion: no-preference) {
  button {
    transition: outline-offset var(--duration-instant) var(--ease-out);
  }

  button:focus-visible {
    outline: 2px solid var(--focus-color);
    outline-offset: 2px;
  }
}

/* Fade in */
@media (prefers-reduced-motion: no-preference) {
  .fade-in {
    animation: fadeIn var(--duration-normal) var(--ease-out);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

---

## Animation Patterns

### Keyframe Animations

```css
/* Subtle pulse for attention */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@media (prefers-reduced-motion: no-preference) {
  .notification-badge {
    animation: pulse 2s var(--ease-in-out) infinite;
  }
}

/* Reduced motion alternative: no animation */
@media (prefers-reduced-motion: reduce) {
  .notification-badge {
    animation: none;
  }
}
```

### Loading Spinners

```css
/* Spinner that respects reduced motion */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
}

@media (prefers-reduced-motion: no-preference) {
  .spinner {
    animation: spin 1s linear infinite;
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    /* Static indicator or pulsing opacity */
    animation: none;
    border-style: dotted;
  }
}
```

### Skeleton Loading

```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--surface-color) 25%,
    var(--background-alt) 50%,
    var(--surface-color) 75%
  );
  background-size: 200% 100%;
}

@media (prefers-reduced-motion: no-preference) {
  .skeleton {
    animation: shimmer 1.5s infinite;
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    background: var(--background-alt);
  }
}
```

---

## Entrance Animations

### Fade and Slide

```css
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: no-preference) {
  .animate-in {
    animation: fadeSlideUp var(--duration-normal) var(--ease-out) both;
  }

  /* Staggered children */
  .animate-in > * {
    animation: fadeSlideUp var(--duration-normal) var(--ease-out) both;
  }

  .animate-in > *:nth-child(1) { animation-delay: 0ms; }
  .animate-in > *:nth-child(2) { animation-delay: 50ms; }
  .animate-in > *:nth-child(3) { animation-delay: 100ms; }
  .animate-in > *:nth-child(4) { animation-delay: 150ms; }
}

@media (prefers-reduced-motion: reduce) {
  .animate-in,
  .animate-in > * {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

### Scale In

```css
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@media (prefers-reduced-motion: no-preference) {
  dialog[open] {
    animation: scaleIn var(--duration-fast) var(--ease-out);
  }
}
```

---

## View Transitions API

For page transitions (progressive enhancement):

```css
/* Enable view transitions */
@view-transition {
  navigation: auto;
}

/* Default crossfade */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: var(--duration-normal);
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation-duration: 0.01ms;
  }
}

/* Named transitions for specific elements */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: var(--duration-slow);
}
```

---

## Scroll-Driven Animations

Modern CSS scroll-driven animations (progressive enhancement):

```css
/* Fade in on scroll */
@keyframes fadeInOnScroll {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: no-preference) {
  .scroll-reveal {
    animation: fadeInOnScroll linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .scroll-reveal {
    opacity: 1;
    transform: none;
  }
}
```

---

## Micro-interactions

### Button Press

```css
@media (prefers-reduced-motion: no-preference) {
  button {
    transition: transform var(--duration-instant) var(--ease-out);
  }

  button:active {
    transform: scale(0.98);
  }
}
```

### Toggle Switch

```css
.toggle-track {
  width: 44px;
  height: 24px;
  background: var(--surface-color);
  border-radius: 12px;
}

.toggle-thumb {
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transform: translateX(2px);
}

@media (prefers-reduced-motion: no-preference) {
  .toggle-thumb {
    transition: transform var(--duration-fast) var(--ease-out);
  }
}

.toggle-input:checked + .toggle-track .toggle-thumb {
  transform: translateX(22px);
}
```

### Checkbox Check

```css
.checkbox-icon {
  stroke-dasharray: 24;
  stroke-dashoffset: 24;
}

@media (prefers-reduced-motion: no-preference) {
  .checkbox-icon {
    transition: stroke-dashoffset var(--duration-fast) var(--ease-out);
  }
}

.checkbox-input:checked + .checkbox-box .checkbox-icon {
  stroke-dashoffset: 0;
}
```

---

## Animation Duration Guidelines

| Animation Type | Duration | Reason |
|---------------|----------|--------|
| Micro-interaction | 100-150ms | Immediate feedback |
| Simple transition | 150-300ms | Noticeable but quick |
| Complex animation | 300-500ms | Time to follow |
| Page transition | 300-500ms | Context shift |
| Loading indicator | 1000-2000ms | One cycle visible |

### The 100ms Rule

Users perceive actions as instant if response is under 100ms. Use this for:

- Button active states
- Focus indicators
- Toggle switches

---

## Dangerous Patterns to Avoid

### Vestibular Triggers

These can cause motion sickness or seizures:

| Pattern | Problem | Alternative |
|---------|---------|-------------|
| Parallax scrolling | Vestibular issues | Static or subtle parallax |
| Auto-playing video | Unexpected motion | Play on interaction |
| Flashing (>3Hz) | Seizure risk | No flashing |
| Large zooming | Vestibular issues | Fade transitions |
| Spinning/rotating | Disorientation | Fade or slide |

```css
/* BAD: Aggressive parallax */
.parallax {
  transform: translateY(calc(var(--scroll) * 0.5));
}

/* BETTER: Subtle or disabled with reduced motion */
@media (prefers-reduced-motion: reduce) {
  .parallax {
    transform: none;
  }
}
```

### Infinite Animations

```css
/* BAD: Constant motion */
.attention-seeker {
  animation: bounce 1s infinite;
}

/* BETTER: Limited iterations */
.attention-seeker {
  animation: bounce 1s 3; /* Only 3 times */
}

/* BEST: Trigger on interaction */
.attention-seeker:hover {
  animation: bounce 0.5s;
}
```

---

## Testing Checklist

### Browser DevTools

1. **Chrome**: Rendering > Emulate CSS media feature > prefers-reduced-motion: reduce
2. **Firefox**: about:config > ui.prefersReducedMotion (0=no-preference, 1=reduce)
3. **Safari**: Develop > Experimental Features > Reduced Motion

### System Settings

- **macOS**: System Preferences > Accessibility > Display > Reduce motion
- **iOS**: Settings > Accessibility > Motion > Reduce Motion
- **Windows**: Settings > Ease of Access > Display > Show animations
- **Android**: Settings > Accessibility > Remove animations

---

## Checklist

When adding animations or transitions:

- [ ] `prefers-reduced-motion` is respected
- [ ] Reduced motion has a meaningful alternative (not just disabled)
- [ ] Only compositor properties are animated (`transform`, `opacity`)
- [ ] `will-change` is used sparingly and removed after animation
- [ ] Duration tokens are used consistently
- [ ] No flashing content (>3 flashes per second)
- [ ] Infinite animations have a purpose and can be stopped
- [ ] Parallax and large motion are optional enhancements
- [ ] Loading states work without animation
- [ ] Animation enhances rather than distracts

## Related Skills

- **css-author** - Modern CSS organization with native @import, @layer casca...
- **progressive-enhancement** - HTML-first development with CSS-only interactivity patterns
- **performance** - Write performance-friendly HTML pages
- **accessibility-checker** - Ensure WCAG2AA accessibility compliance
