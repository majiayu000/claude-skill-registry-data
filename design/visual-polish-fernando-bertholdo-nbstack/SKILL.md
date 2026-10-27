---
name: visual-polish
description: Use when refining interface details (text wrapping, spacing, animations, shadows, alignment) to compound small visual improvements into polished, responsive experiences following Jakub Krehel's principles.
---

# UI Visual Polish

## Overview

Great interfaces rarely come from a single thing—it's usually a collection of small, thoughtful details that compound into a cohesive, polished experience. This skill documents techniques for visual refinement: text wrapping strategies, balanced border radius hierarchies, contextual animations, optical alignment, and shadow composition. Each detail is intentional and measurable.

## When to Use / When NOT to Use

### Use When:
- Refining typography presentation (headings, body text, dynamic numbers)
- Designing nested UI components with multiple layers
- Adding entrance/exit animations to modals, tooltips, or lists
- Replacing solid borders with depth-aware shadows
- Aligning buttons with icons or misaligned visual elements
- Optimizing animations for user interruption (mid-toggle, mid-drag)
- Adding micro-interactions (copy-to-clipboard, status toggles)
- Ensuring consistent visual hierarchy across the interface

### Do NOT Use When:
- Building motion-heavy animations (use dedicated motion library docs)
- Solving structural layout issues (use CSS Grid/Flexbox guides)
- Implementing accessibility requirements (separate A11y guide)
- Addressing performance bottlenecks (use optimization guide)
- Creating brand identity from scratch (use design system docs)

---

## Core Techniques

### Surfaces & Layout

#### 1. Text Wrapping Strategy

Balance text distribution and reading flow with CSS `text-wrap`:

- **`text-wrap: balance`** — For headings
  - Distributes text evenly across lines
  - Prevents orphaned words at line ends
  - Use once per heading (computed once at render)
  - Best for titles, hero text, short high-impact copy

- **`text-wrap: pretty`** — For body text
  - Similar to `balance` but slower algorithm
  - Better for longer paragraphs
  - Reduces hyphenation and ugly breaks
  - May slightly reflow on resizes

**Implementation:**
```css
h1, h2, h3 {
  text-wrap: balance;
}

p {
  text-wrap: pretty;
}
```

#### 2. Concentric Border Radius

Create visual hierarchy in nested elements by proportional radius scaling.

**Formula:** `outer_radius = inner_radius + padding`

**Example:**
- Inner element: `border-radius: 12px`
- Padding: `8px`
- Outer container: `border-radius: 20px` (12 + 8)

This creates balanced visual nesting and guides the eye through component hierarchy without explicit borders.

```css
.card {
  border-radius: 20px;
  padding: 8px;
}

.card-inner {
  border-radius: 12px;
  padding: 8px;
}

.card-content {
  border-radius: 4px;
}
```

#### 3. Shadows Over Borders

Replace flat `border` declarations with layered shadows for depth and background flexibility.

**Three-Layer Shadow Composition:**
```css
box-shadow:
  0px 0px 0px 1px rgba(0, 0, 0, 0.06),           /* Outline */
  0px 1px 2px -1px rgba(0, 0, 0, 0.06),          /* Soft inner shadow */
  0px 2px 4px 0px rgba(0, 0, 0, 0.04);           /* Ambient shadow */

/* Dark mode: use white with opacity */
box-shadow:
  0px 0px 0px 1px rgba(255, 255, 255, 0.1),
  0px 1px 2px -1px rgba(255, 255, 255, 0.06),
  0px 2px 4px 0px rgba(255, 255, 255, 0.04);

/* Hover state: increase opacity */
transition: box-shadow 200ms cubic-bezier(0.4, 0, 0.2, 1);
```

**Why:** Shadows adapt to any background; solid borders limit color palette and feel flat.

#### 4. Image Outlines

Apply subtle outlines to images for visual containment and depth.

```css
img {
  outline: 1px solid rgba(0, 0, 0, 0.1);
  outline-offset: -1px;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  img {
    outline-color: rgba(255, 255, 255, 0.1);
  }
}
```

Creates consistent visual framing without relying on parent backgrounds.

---

### Typography

#### 5. Font Smoothing (macOS)

macOS applies subpixel antialiasing by default, making text appear heavier than intended on light backgrounds.

**Solution:** Apply `-webkit-font-smoothing: antialiased` (or Tailwind's `antialiased` class) at layout root.

```css
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

**Effect:** Produces thinner, crisper rendering of light text on macOS; no effect on other OS.

#### 6. Tabular Numbers

Prevent number shifting when values update by using fixed-width numerals.

```css
.counter, .price, .metric {
  font-variant-numeric: tabular-nums;
  /* or Tailwind: class="tabular-nums" */
}
```

**When to use:**
- Dashboards with live-updating metrics
- Price displays with dynamic values
- Counters and timers
- Financial tables

**Caveat:** Some fonts (e.g., Inter) alter numeral appearance with `tabular-nums`. Test in your font.

---

### Animation Details

#### 7. Contextual Icon Animations

Animate icon transitions (copy→check, eye→eye-off) with opacity, scale, and blur.

**Technique:**
- **Opacity:** 0 → 1 (fade in)
- **Scale:** 0.25 → 1 (grow from center)
- **Blur:** 4px → 0px (sharpen as it enters)
- **Duration:** 300ms–400ms

**Why motion library preferred:** CSS transitions alone lack spring easing for natural deceleration.

**Example (Framer Motion syntax):**
```jsx
<AnimatePresence mode="wait">
  {isCopied ? (
    <motion.div
      key="check"
      initial={{ opacity: 0, scale: 0.25, filter: "blur(4px)" }}
      animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
      exit={{ opacity: 0, scale: 0.75 }}
      transition={{ type: "spring", stiffness: 200, damping: 10 }}
    >
      <CheckIcon />
    </motion.div>
  ) : (
    <motion.div
      key="copy"
      initial={{ opacity: 0, scale: 0.25, filter: "blur(4px)" }}
      animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
      exit={{ opacity: 0, scale: 0.75 }}
      transition={{ type: "spring", stiffness: 200, damping: 10 }}
    >
      <CopyIcon />
    </motion.div>
  )}
</AnimatePresence>
```

#### 8. Interruptible vs Fixed Animations

**CSS Transitions** (for interactions):
- Interpolate toward latest state
- Support interruption (user changes intent mid-animation)
- Best for: toggles, hovers, drag interactions
- User interrupts frequently; animations must retarget

**Keyframe Animations** (for sequences):
- Run fixed, predetermined timelines
- Do not retarget mid-sequence
- Best for: page-load sequences, one-time reveals
- Non-interruptible animations feel broken

**Decision Rule:** Use transitions for user interactions; keyframes for deterministic sequences.

```css
/* ✅ Transition: interruptible */
.toggle {
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1);
}
.toggle:hover {
  transform: scale(1.05);
}

/* ✅ Keyframe: deterministic */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.slide-in {
  animation: slideIn 800ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

#### 9. Enter Animations with Stagger

Combine opacity, blur, and vertical translation for smooth entrances.

**Single Block (headings, descriptions):**
```css
@keyframes enterBlock {
  from {
    opacity: 0;
    filter: blur(5px);
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    filter: blur(0);
    transform: translateY(0);
  }
}

.enter-block {
  animation: enterBlock 800ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

**Staggered (buttons, list items):**
- Sectional stagger: ~100ms delays between groups
- Word-level stagger: ~80ms delays between individual items

```jsx
{buttons.map((btn, i) => (
  <motion.button
    key={i}
    initial={{ opacity: 0, filter: "blur(5px)", y: 8 }}
    animate={{ opacity: 1, filter: "blur(0px)", y: 0 }}
    transition={{
      duration: 0.8,
      delay: i * 0.1, // Stagger by 100ms
      ease: "easeOut"
    }}
  >
    {btn.label}
  </motion.button>
))}
```

#### 10. Exit Animations (Subtle)

Exits should be less prominent than entrances—they're farewell states.

**Options:**
- **Full exit:** `calc(-100% - 4px)` (slide out past container edge + padding)
- **Subtle exit:** Fixed `-12px` offset (gentle departure)

Combine with opacity fade and maintain directional motion:

```css
@keyframes exitSubtle {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-12px);
  }
}

.exit-subtle {
  animation: exitSubtle 400ms ease-in forwards;
}
```

---

### Interaction Details

#### 11. Scale-on-Press Feedback

Provide tactile feedback when buttons are pressed.

**Rule:** Scale exactly `0.96` (never below 0.95).

```css
button {
  transition: transform 100ms cubic-bezier(0.4, 0, 0.2, 1);
}

button:active {
  transform: scale(0.96);
}
```

Values below 0.95 feel exaggerated; 0.96 is subtle and satisfying.

#### 12. Optical vs Geometric Alignment

Geometric alignment doesn't always look correct visually. Adjust spacing for optical correctness.

**Common case:** Buttons with text + icon
- Icon is lighter visually, needs less padding
- Text carries weight, needs more padding

```css
.button-with-icon {
  display: flex;
  align-items: center;
  padding-left: 12px;  /* Icon side: less padding */
  padding-right: 16px; /* Text side: more padding */
}
```

**Best practice:** Fix alignment in the SVG itself to avoid container adjustments.

#### 13. Minimum Interactive Hit Area

Ensure all interactive elements are at least **40×40 pixels** (mobile accessibility standard).

```css
button, a, input[type="checkbox"] {
  min-width: 40px;
  min-height: 40px;
}
```

---

### Performance & Best Practices

#### 14. Skip Page-Load Animations

Avoid jarring animations on first paint.

```jsx
<AnimatePresence initial={false}>
  {/* Animations only on state changes, not mount */}
</AnimatePresence>
```

#### 15. Transition Property Specificity

Never use `transition: all`—specify exact properties.

```css
/* ❌ Avoid */
.element {
  transition: all 200ms ease;
}

/* ✅ Specific */
.element {
  transition: background-color 200ms ease, transform 200ms ease;
}
```

Reduces unnecessary repaints and makes intent clearer.

#### 16. `will-change` Usage

Reserve `will-change` for GPU-compositable properties only:
- `transform`
- `opacity`
- `filter`

```css
.animated-element {
  will-change: transform, opacity;
}
```

Do NOT use on `box-shadow`, `background-color`, or layout properties—they cannot be GPU-accelerated.

---

## Quick Reference Table

| Technique | Property/Value | Use Case | Duration |
|-----------|----------------|----------|----------|
| Text Balance | `text-wrap: balance` | Headings | N/A (layout) |
| Text Pretty | `text-wrap: pretty` | Body paragraphs | N/A (layout) |
| Border Radius | `outer = inner + padding` | Nested components | N/A (layout) |
| Shadow Depth | 3-layer composition | Borders, cards | N/A (static) |
| Font Smoothing | `-webkit-font-smoothing: antialiased` | macOS rendering | N/A (static) |
| Tabular Nums | `font-variant-numeric: tabular-nums` | Counters, prices | N/A (static) |
| Icon Animate | Opacity 0→1, Scale 0.25→1, Blur 4→0px | Toggle icons | 300–400ms |
| Enter Animation | `translateY(8px), blur(5px), opacity(0)` | Staggered reveals | 800ms + stagger |
| Exit Animation | `translateY(-12px), opacity(0)` | Dismissals | 400ms |
| Scale Press | `scale(0.96)` | Button press feedback | 100ms |
| Hit Area | Min 40×40px | All interactive | N/A (layout) |

---

## Review Checklist

Before shipping a refined UI component, validate:

- [ ] **Typography**
  - [ ] Headings use `text-wrap: balance`
  - [ ] Body text uses `text-wrap: pretty`
  - [ ] Font smoothing applied at layout root (`-webkit-font-smoothing: antialiased`)
  - [ ] Dynamic numbers use `tabular-nums` if value changes

- [ ] **Spacing & Hierarchy**
  - [ ] Concentric border radius follows formula (`outer = inner + padding`)
  - [ ] Shadows replace flat borders (3-layer composition)
  - [ ] Image outlines applied consistently (`outline: 1px solid rgba(0, 0, 0, 0.1)`)
  - [ ] Optical alignment verified (text + icon buttons checked)

- [ ] **Animation**
  - [ ] Enter animations use stagger (button delays ~100ms)
  - [ ] Exit animations are subtle and directional
  - [ ] Icon toggles animate: opacity, scale, blur
  - [ ] Animations are interruptible (CSS transitions for interactions)
  - [ ] `initial={false}` on AnimatePresence (skip page-load)

- [ ] **Interaction**
  - [ ] Buttons scale to exactly `0.96` on press
  - [ ] All interactive elements ≥40×40px
  - [ ] `transition` property is specific (not `all`)
  - [ ] `will-change` used only for `transform`, `opacity`, `filter`

- [ ] **Accessibility & Performance**
  - [ ] Color contrast meets WCAG AA
  - [ ] Motion respects `prefers-reduced-motion`
  - [ ] Animations don't block critical rendering path
  - [ ] No jank on 60fps target devices

---

## Common Mistakes

### ❌ Flat Borders Instead of Shadows
```css
/* ❌ Feels flat, limits backgrounds */
border: 1px solid #ccc;

/* ✅ Depth-aware, adapts to any background */
box-shadow:
  0px 0px 0px 1px rgba(0, 0, 0, 0.06),
  0px 1px 2px -1px rgba(0, 0, 0, 0.06),
  0px 2px 4px 0px rgba(0, 0, 0, 0.04);
```

### ❌ Animation Without Interruption
```jsx
/* ❌ Feels broken if user changes intent mid-animation */
animation: spin 2s linear infinite;

/* ✅ Retargets on toggle; smooth interruption */
transition: transform 200ms ease;
```

### ❌ Over-Scaled Press Feedback
```css
/* ❌ Feels exaggerated */
button:active { transform: scale(0.90); }

/* ✅ Subtle and satisfying */
button:active { transform: scale(0.96); }
```

### ❌ Text Clipping Due to Missing Wrapping
```css
/* ❌ Creates orphans and awkward breaks */
h1 { /* no text-wrap */ }

/* ✅ Balanced distribution */
h1 { text-wrap: balance; }
```

### ❌ Hardcoded Icon Padding
```css
/* ❌ Looks misaligned */
button { padding: 12px 12px 12px 12px; }

/* ✅ Optically correct */
button { padding-left: 10px; padding-right: 14px; }
```

### ❌ No Stagger on List Reveals
```jsx
/* ❌ All items enter at once; feels abrupt */
{items.map(item => <Item />)}

/* ✅ Staggered entrance; feels intentional */
{items.map((item, i) => (
  <Item delay={i * 0.08} />
))}
```

### ❌ Numbers Shifting in Tables
```css
/* ❌ Metrics jump as values update */
.metric { font-family: "Inter"; }

/* ✅ Numbers stay aligned */
.metric { font-variant-numeric: tabular-nums; }
```

---

## References & Inspiration

- **Jakub Krehel's "Details that make interfaces feel better"** — Core philosophy
- Framer Motion docs for spring easing and AnimatePresence patterns
- WCAG accessibility guidelines for color contrast and motion preferences
- CSS spec: `text-wrap`, `box-shadow`, `font-variant-numeric`

---

**Version:** 1.0.0
**Last Updated:** 2026-03-30
**Status:** Active
