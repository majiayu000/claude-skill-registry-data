---
name: animation-motion
description: Use when designing or reviewing UI animations, transitions, and motion interactions. Triggers for animation decisions, performance optimization, accessibility compliance, and gesture handling.
---

# UI Animation & Motion — Emil Kowalski Design Philosophy

## Overview

Taste is trained, not innate. Animation excellence compounds through study and practice—most users never consciously notice individual polish, yet the collection creates stunning results. Beauty is leverage: aesthetic excellence is competitive advantage. This skill applies Emil Kowalski's battle-tested animation decision framework to ship production-grade motion.

---

## When to Use This Skill

**Use when:**
- Designing animations for UI components (buttons, modals, dropdowns, popovers, tooltips)
- Reviewing animation implementations for performance and accessibility
- Deciding whether/how/how-fast to animate interactions
- Building gesture-driven interfaces (drag, swipe, hold)
- Optimizing motion for accessibility (prefers-reduced-motion)
- Creating staggered or spring-based animations
- Debugging animation timing, easing, or transform issues

**Do NOT use for:**
- Animation frameworks/libraries selection (use dedicated framework skills)
- Keyframe animation software (Figma, After Effects)
- SVG animation exclusively (this covers CSS/WAAPI)

---

## The Animation Decision Framework

### Question 1: Should This Animate at All?

**Frequency is the primary gate:**

| Frequency | Example | Decision |
|-----------|---------|----------|
| **100+ times/day** | Keyboard shortcuts, frequently toggled UI | ❌ Never animate |
| **Tens of times/day** | Hover effects, toggle states | ⚠️ Remove or drastically reduce |
| **Occasional (few per session)** | Modals, toasts, notifications | ✅ Standard animation acceptable |
| **Rare** | Onboarding, celebrations, first-run | ✅ Can add delight |
| **Keyboard-initiated** | Any action from keyboard (return, space, etc.) | ❌ Never animate |

**Golden rule:** If users interact with it frequently, *every millisecond of animation compounds into frustration.*

### Question 2: What Is the Purpose?

**Valid animation purposes:**
1. **Spatial consistency** — clarify origin/destination (modal from center, popover from trigger)
2. **State indication** — show what changed (button pressed, checkbox checked)
3. **Explanation** — guide attention or teach (scroll hint, tooltip entrance)
4. **Feedback** — confirm action received (keystroke feedback, form validation)
5. **Preventing jarring changes** — smooth transitions between states

**Invalid reasons:**
- "Looks cool" (unless rare, intentional delight)
- Eye candy for frequently-used UI (animation debt)
- Mimicking competitors without purpose

### Question 3: What Easing Curve Should It Use?

**Default easing selection:**

| Scenario | Easing | Rationale |
|----------|--------|-----------|
| **Element entering/exiting** | ease-out | Fast start = responsive; slows to natural stop |
| **Moving/morphing on screen** | ease-in-out | Symmetric motion feels balanced |
| **Hover/color change** | ease | General purpose, smooth |
| **Constant motion** | linear | Clock-like consistency |

**CRITICAL:** Use **custom easing curves**, not CSS defaults:

```css
:root {
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
}
```

**Never use `ease-in` for UI animations** — delays initial movement, feels sluggish and unresponsive.

### Question 4: How Fast Should It Be?

**Duration guidelines:**

| Component | Duration Range | Rationale |
|-----------|-----------------|-----------|
| **Button press feedback** | 100–160ms | Instant perceived feedback |
| **Tooltips/small popovers** | 125–200ms | Quick appearance |
| **Dropdowns/selects** | 150–250ms | Slightly longer for scope change |
| **Modals/drawers** | 200–500ms | Larger movement space |
| **Marketing/explanatory** | Flexible | Can extend for teaching |

**Rule of thumb:** UI animations under 300ms. Anything longer *feels* like loading.

---

## Spring Animations — Alive Motion

Springs simulate physics naturally. Duration emerges from physics parameters, not fixed time. **Use for:**
- Drag interactions (user expects momentum)
- "Alive" elements that feel responsive
- Interruptible gestures (springs maintain velocity when interrupted)
- Decorative mouse-tracking effects

**Apple-style config:**
```javascript
{
  type: "spring",
  duration: 0.5,
  bounce: 0.2  // 0.1-0.3 recommended; keep subtle
}
```

**Traditional config (Framer Motion):**
```javascript
{
  type: "spring",
  mass: 1,
  stiffness: 100,
  damping: 10
}
```

**Key insight:** Springs maintain velocity when interrupted. CSS animations restart from zero (rigid).

---

## Component Animation Patterns

### Buttons
```css
/* Base */
button {
  transition: transform 160ms var(--ease-out);
}

/* Active state — subtle press feedback */
button:active {
  transform: scale(0.97);
}
```

**Why 0.97, not 0.95?** Subtle feedback feels refined; aggressive scale looks cheap.

### Never Animate From scale(0)
```css
/* ❌ BAD — jarring entrance, feels cheap */
@keyframes popIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

/* ✅ GOOD — smooth, natural entrance */
@keyframes popIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
```

### Popovers — Origin-Aware
```css
/* Popover respects where it originated from */
[data-radix-popover-content] {
  transform-origin: var(--radix-popover-content-transform-origin);
  animation: popoverEnter 200ms var(--ease-out);
}

@keyframes popoverEnter {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

**Modals keep center origin** — always `transform-origin: center center`.

### Tooltips — Smart Delays
```css
/* First appearance: delay to confirm intent */
[role="tooltip"] {
  transition: opacity 200ms var(--ease-out);
  transition-delay: 300ms;
}

/* Subsequent hovers: instant (user already hovering element) */
[role="tooltip"][data-instant] {
  transition-delay: 0ms;
}
```

### CSS Transitions vs. Keyframes
- **Use CSS transitions** for interruptible UI (user can stop mid-animation)
- **Use keyframes** for deterministic, looping effects (loading spinners, constant motion)
- **Transitions are superior** for most UI because they handle interruption gracefully.

### Blur for Masking Imperfect Transitions
```css
/* During fade transitions, slight blur hides interpolation artifacts */
[data-transitioning] {
  filter: blur(2px);
  transition: filter 200ms var(--ease-out);
}

[data-transitioning][data-done] {
  filter: blur(0px);
}
```

Keep blur under 20px; large blur reads as visual glitch.

### @starting-style for Entry Animations (CSS-only)
```css
/* Define "before" state without JavaScript */
dialog {
  opacity: 1;
  translate: 0 0;
  animation: dialogEnter 300ms var(--ease-out);
}

@starting-style {
  dialog {
    opacity: 0;
    translate: 0 -20px;
  }
}
```

---

## CSS Transform Mastery

### translateY with Percentages
```css
/* Percentage relative to ELEMENT SIZE, not viewport */
[data-drawer] {
  transform: translateY(100%);  /* Moves down by element's own height */
  transition: transform 300ms var(--ease-drawer);
}

[data-drawer][data-open] {
  transform: translateY(0);
}
```

### scale() Propagates to Children
```css
/* Parent scale affects children proportionally */
.parent {
  transform: scale(0.95);  /* All descendants scale 0.95x */
}
```

### 3D Transforms with Preserve-3D
```css
.card {
  transform-style: preserve-3d;
  transform: rotateX(15deg) rotateY(-10deg);
}

.card-face {
  transform: translateZ(20px);  /* Lifts face forward in 3D space */
}
```

---

## clip-path for Advanced Animation

**Use for rectangular masks:**

```css
/* Reveal from top down */
.reveal {
  clip-path: inset(0 0 100% 0);
  animation: revealDown 400ms var(--ease-out) forwards;
}

@keyframes revealDown {
  to { clip-path: inset(0 0 0 0); }
}
```

**Use cases:**
- Tab color transitions (reveal new color under existing)
- Hold-to-delete progress indicators
- Image reveals on scroll
- Comparison sliders (before/after)

---

## Gesture and Drag Interactions

### Momentum-Based Dismissal
```javascript
// User swipes dismissible element
element.addEventListener('pointerup', (event) => {
  const velocity = calculateVelocity(event);

  if (Math.abs(velocity) > DISMISS_THRESHOLD) {
    // Use spring to carry momentum
    element.animate([
      { transform: 'translateY(0)' },
      { transform: 'translateY(100%)' }
    ], {
      duration: 300,
      easing: 'cubic-bezier(0.32, 0.72, 0, 1)'
    });
  }
});
```

### Boundary Friction (Not Hard Stops)
```javascript
// Damping at boundaries instead of walls
let velocity = getVelocity();
if (element.y > MAX_Y) {
  velocity *= 0.95;  // Friction dampens momentum
}
```

### setPointerCapture() for Cross-Document Tracking
```javascript
element.addEventListener('pointerdown', (event) => {
  element.setPointerCapture(event.pointerId);
  // All subsequent pointer events target this element, even off-screen
});

element.addEventListener('pointermove', (event) => {
  if (event.isPrimary) {
    // Only respond to primary pointer (not secondary touch)
    updateDrag(event.clientX, event.clientY);
  }
});
```

---

## Performance Rules

### Only Animate transform and opacity
```css
/* ✅ GOOD — GPU accelerated, no repaints */
.button {
  transition: transform 160ms var(--ease-out), opacity 160ms var(--ease-out);
}

/* ❌ BAD — triggers reflow on every frame */
.button {
  transition: width 160ms, height 160ms, padding 160ms;
}
```

### CSS Variables for Coordinated Animations
```css
:root {
  --animation-duration: 300ms;
  --animation-easing: var(--ease-out);
}

.modal {
  animation: modalEnter var(--animation-duration) var(--animation-easing);
}

.modal-overlay {
  animation: overlayFade var(--animation-duration) var(--animation-easing);
}
```

### CSS Animations Beat JavaScript Under Load
- Use CSS transitions/animations for UI
- Use JavaScript (Web Animation API) for complex, programmatic effects
- Profile on real devices (mobile especially)

### WAAPI (Web Animation API) for Programmatic CSS
```javascript
element.animate([
  { transform: 'translateY(-100px)', opacity: 0 },
  { transform: 'translateY(0)', opacity: 1 }
], {
  duration: 300,
  easing: 'cubic-bezier(0.23, 1, 0.32, 1)',
  fill: 'forwards'
});
```

**Verify on real devices, always.** Desktop Chrome may hide jank that's visible on iPhone.

---

## Accessibility — Non-Negotiable

### Always Respect prefers-reduced-motion
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Not optional.** Users with vestibular disorders experience nausea from motion.

### Use @media (hover: hover) for Hover-Only Effects
```css
/* Only show hover effects on devices that support hover */
@media (hover: hover) {
  button:hover {
    opacity: 0.8;
  }
}
```

Prevents ghost states on touch devices.

---

## Stagger Animations — Visual Rhythm

Animate multiple elements in sequence, not simultaneously:

```css
.item {
  opacity: 0;
  animation: itemEnter 300ms var(--ease-out) forwards;
}

.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
```

**Effect:** Creates visual rhythm, guides attention, feels intentional.

---

## Sonner Principles — Polish Compounding

1. **Cohesion:** Every detail works together. No random animations.
2. **Opacity + Height:** Sophisticated reveals use combined opacity and height shifts, not just fade.
3. **Fresh eyes review:** Review animations the next day. What felt good at 3 AM looks different at noon.
4. **Asymmetric enter/exit timing:** Fast entrance (100-150ms), slower exit (200-300ms). Feels snappier.

---

## Debugging Animations

### Slow Motion Testing in DevTools
1. Open DevTools (F12)
2. Animations panel → **Slow down playback (10x)**
3. Frame-by-frame inspection reveals micro-timing issues

### Debug Checklist
- Does animation respond immediately to user input?
- Does easing curve feel natural (not robotic)?
- Does animation maintain 60fps on mobile? (DevTools Performance tab)
- Is motion purpose clear (spatial, feedback, state)?

---

## Quick Reference Table

| Aspect | Rule |
|--------|------|
| **Button press** | 100-160ms, scale(0.97), ease-out |
| **Modal entrance** | 200-500ms, origin-aware, ease-out |
| **Dropdown open** | 150-250ms, ease-out |
| **Hover state** | Remove or keep <100ms; avoid on keyboard shortcuts |
| **Easing default** | Custom cubic-bezier, never CSS `ease-in` |
| **Performance** | transform + opacity only |
| **Accessibility** | Always respect prefers-reduced-motion |
| **Spring bounce** | 0.1-0.3, keep subtle |
| **Scale entrance** | Never scale(0), use scale(0.95) + opacity |
| **Popover origin** | Use transform-origin: var(--radix-popover-content-transform-origin) |

---

## Review Checklist

When reviewing UI code with animations, verify:

- [ ] **Clear purpose** — Animation serves spatial, feedback, state, or explanation purpose (not "just cool")
- [ ] **Frequency-appropriate** — Not animating keyboard shortcuts or 100x/day interactions
- [ ] **Custom easing curves** — Not using CSS `ease`, `ease-in`, or `ease-out` defaults
- [ ] **Duration under 300ms** — UI animations, not marketing videos
- [ ] **Buttons have :active feedback** — Press feedback present
- [ ] **No scale(0) animations** — Using scale(0.95) + opacity for entrances
- [ ] **Popovers origin-aware** — Using transform-origin for popover content
- [ ] **Respects prefers-reduced-motion** — Media query in place, verified
- [ ] **Only animates transform and opacity** — No reflow-triggering properties
- [ ] **Tested on real devices** — Not just Chrome desktop
- [ ] **Asymmetric timing** — Faster entrance, slower exit
- [ ] **No spring jank** — Springs don't overshoot on fast interactions

---

## Review Format

Use this markdown table when presenting before/after animation changes:

| Before | After | Why |
|--------|-------|-----|
| Button grows on hover | Button darkens on hover | Hover is >10x/day; animation removed |
| Modal scale(0) entrance | Modal scale(0.95) entrance | Smoother, less jarring visual |
| 500ms dropdown open | 200ms dropdown open | Felt laggy; 200ms is perceptually instant |

---

## Common Mistakes

### 1. Animating Frequently-Used Interactions
```javascript
// ❌ BAD — submitted 100x/day, animation compounds to ~3 min/day lost
buttonSubmit.addEventListener('click', () => {
  showLoadingSpinner();  // 300ms animation
});

// ✅ GOOD — instant feedback, no animation
buttonSubmit.disabled = true;
buttonSubmit.textContent = 'Loading...';
```

### 2. Using ease-in for UI
```css
/* ❌ BAD — delays initial movement, feels unresponsive */
.modal {
  transition: opacity 300ms ease-in;
}

/* ✅ GOOD — fast start, natural deceleration */
.modal {
  transition: opacity 300ms cubic-bezier(0.23, 1, 0.32, 1);
}
```

### 3. Hardcoded Timing (No Coordination)
```css
/* ❌ BAD — impossible to adjust globally */
.modal { animation: modalEnter 350ms ease-out; }
.overlay { animation: overlayFade 300ms ease-out; }
.button { animation: buttonSlide 250ms ease-out; }

/* ✅ GOOD — adjust once, applies everywhere */
:root {
  --duration-modal: 300ms;
  --duration-feedback: 150ms;
}

.modal { animation: modalEnter var(--duration-modal) var(--ease-out); }
```

### 4. Forgetting prefers-reduced-motion
```css
/* ❌ BAD — ignores accessibility preference */
.animation { animation: spin 1s linear infinite; }

/* ✅ GOOD — respects user preference */
.animation { animation: spin 1s linear infinite; }
@media (prefers-reduced-motion: reduce) {
  .animation { animation: none; }
}
```

### 5. Scale From Zero
```javascript
// ❌ BAD
element.style.transform = 'scale(0)';
setTimeout(() => {
  element.style.transform = 'scale(1)';
}, 0);

// ✅ GOOD
element.style.transform = 'scale(0.95)';
element.style.opacity = '0';
setTimeout(() => {
  element.style.transform = 'scale(1)';
  element.style.opacity = '1';
}, 0);
```

---

## Final Principle

**Taste is trained.** Study animations in Apple Mail, Linear, Stripe, Arc Browser. Screenshot the good ones. Copy the feeling (not the code). Practice writing micro-interactions. Review with fresh eyes. Ship, measure, iterate.

Every 100ms compounded across millions of interactions shapes user perception. Excellence is leverage.
