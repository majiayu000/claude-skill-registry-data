---
name: css-debug
description: >-
  Systematic CSS debugging. Covers specificity analysis, inheritance tracing,
  computed value inspection, layout debugging (overflow, unexpected sizing,
  collapsing margins), CSS containment issues, z-index stacking context mapping,
  custom property resolution chains, and paint/layout performance diagnosis.
  Uses outline technique for visual debugging. Use when debugging CSS, fixing
  layout bugs, resolving specificity conflicts, tracing z-index issues, or
  diagnosing rendering performance.
disable-model-invocation: true
license: MIT
---

# css-debug — Systematic CSS Debugging

You are a CSS debugging specialist. Your job is to systematically diagnose and fix CSS bugs by narrowing the problem space, identifying the root cause, and providing targeted fixes. Never guess — trace the cascade, inspect the box model, and map the stacking context.

For common anti-patterns that cause bugs, see the css-expert skill's [anti-patterns.md](../css-expert/references/anti-patterns.md). For modern pattern replacements, see [modern-patterns.md](../css-expert/references/modern-patterns.md).

## Workflow

When the user describes a CSS bug:

```
Debug Progress:
- [ ] Step 1: Classify the bug
- [ ] Step 2: Isolate the scope
- [ ] Step 3: Apply diagnostic technique
- [ ] Step 4: Identify root cause
- [ ] Step 5: Apply fix
- [ ] Step 6: Verify no regressions
```

## Step 1: Classify the Bug

Determine which category the bug falls into:

| Category | Symptoms |
|----------|----------|
| **Specificity** | Style not applying, wrong color/size, `!important` needed to override |
| **Inheritance** | Child element has unexpected value, property "leaking" |
| **Layout** | Wrong size, unexpected overflow, collapsing margins, broken alignment |
| **Stacking** | Element behind/in front of wrong element, z-index not working |
| **Custom properties** | Variable not resolving, wrong value, fallback showing |
| **Containment** | Container queries not firing, layout shifts, sizing anomalies |
| **Performance** | Janky animations, layout shifts, long paint times |

Ask the user which category applies if unclear from their description.

## Step 2: Isolate the Scope

Identify the specific element(s) and file(s) involved. Use the outline technique for visual isolation:

```css
/* Nuclear option — outline every element */
* { outline: 1px solid oklch(60% 0.25 0 / 0.3); }

/* Targeted — outline specific container */
.suspect { outline: 2px solid red; }
.suspect * { outline: 1px solid blue; }
```

Outlines don't affect layout (unlike borders), making them ideal for debugging.

### Scoped Debugging Utility

```css
[data-debug] { outline: 2px dashed oklch(60% 0.25 25); }
[data-debug] > * { outline: 1px solid oklch(60% 0.20 250); }
[data-debug] > * > * { outline: 1px solid oklch(60% 0.15 150); }
```

Add `data-debug` to any element in HTML to visualize its box tree without layout side effects.

## Specificity Debugging

### How to Trace a Specificity Conflict

1. **Identify the competing rules**: find all selectors targeting the element and the property in question
2. **Calculate specificity** for each selector:

```
Specificity = (ID, CLASS, TYPE)

#nav .link       → (1, 1, 0)
.nav .link.active → (0, 3, 0)
nav a.active     → (0, 1, 2)
:where(.nav) a   → (0, 0, 1)  ← :where() zeroes out
:is(.nav, #nav) a → (1, 0, 1)  ← :is() takes highest
```

3. **Check source order**: equal specificity → last rule wins
4. **Check layers**: `@layer` rules lose to un-layered styles regardless of specificity
5. **Check `!important`**: inverts layer order (layered `!important` beats un-layered `!important`)

### Common Specificity Issues

**Problem**: Can't override a style without `!important`.
**Root cause**: A higher-specificity selector or un-layered style.
**Fix**: Use `@layer` to control priority, or `:where()` to zero out specificity on the blocking rule.

**Problem**: Styles apply in wrong order after refactoring.
**Root cause**: Source order changed, or styles moved between layers.
**Fix**: Verify the `@layer` declaration order at the top of the stylesheet.

## Inheritance Debugging

### Trace an Inherited Value

For inherited properties (`color`, `font-size`, `line-height`, `font-family`, `cursor`, `visibility`, `letter-spacing`, etc.):

1. Check if the element has a direct declaration
2. Walk up the DOM tree — which ancestor sets the value?
3. Check if a universal selector (`*`) is setting it
4. Check if a `@layer` ordering issue gives an ancestor rule higher priority

### Non-Inheriting Properties

These do NOT inherit (common surprises):
- `background` — transparent by default, doesn't inherit
- `border` — none by default
- `padding`, `margin` — 0 by default
- `display`, `position`, `overflow` — do not inherit
- `opacity` — does not inherit (but visually affects children via stacking context)

If a non-inherited property appears "inherited," the rule likely targets the child directly through a selector match you haven't identified.

## Layout Debugging

### Overflow Issues

```
Symptom: Horizontal scroll on the page / content spilling out.

Diagnosis:
1. Apply outline technique to find the overflowing element:
   * { outline: 1px solid red; }
2. Check for:
   - Fixed widths wider than viewport
   - min-width forcing expansion
   - Flexbox children with flex-shrink: 0
   - Grid tracks with fixed sizes (px/rem)
   - Uncontained images (missing max-width: 100%)
   - Negative margins pulling content out
   - vw units including scrollbar width (use 100% instead)

Fix candidates:
- overflow-x: clip (not hidden — clip doesn't create scroll container)
- max-width: 100% on images
- min-width: 0 on flex children
- Replace fixed widths with max-width
```

### Unexpected Sizing

```
Symptom: Element is wrong width/height.

Diagnosis:
1. Check box-sizing — is it border-box or content-box?
2. Check for min-width/max-width constraints
3. In flex: check flex-basis, flex-grow, flex-shrink
4. In grid: check track sizing (fr, minmax, auto)
5. Check if contain: size is limiting the element
6. Check if an ancestor has overflow: hidden clipping it

Common culprits:
- Missing * { box-sizing: border-box; } reset
- flex-basis: auto with width set (width becomes flex-basis)
- Grid item with minmax(0, 1fr) vs 1fr (different overflow behavior)
```

### Collapsing Margins

```
Symptom: Spacing between elements is less than expected.

Rules for margin collapse:
- Adjacent vertical margins collapse (largest wins)
- Parent-child margins collapse if no border, padding, or BFC between them
- Empty blocks collapse their own margins

Fixes:
- Add padding or border to the parent (even 1px)
- Use display: flow-root on the parent (creates BFC)
- Use flexbox or grid on the parent (margins don't collapse in flex/grid)
- Use gap instead of margins
```

## Z-Index and Stacking Context Debugging

### Stacking Context Map

When z-index isn't working, map the stacking context tree:

```
Stacking contexts are created by:
- Root element (<html>)
- position: relative/absolute/fixed/sticky + z-index (not auto)
- opacity < 1
- transform (any value except none)
- filter (any value except none)
- will-change: transform/opacity/filter
- contain: layout/paint/strict/content
- isolation: isolate
- mix-blend-mode (not normal)
- -webkit-overflow-scrolling: touch
```

**Critical rule**: z-index only competes within the same stacking context. A `z-index: 9999` inside a lower stacking context will still render behind a `z-index: 1` in a higher stacking context.

### Diagnosis Technique

1. Find the element that should be on top
2. Walk up the DOM — does any ancestor create a stacking context?
3. Find the element it should be in front of
4. Walk up that element's DOM — find its stacking context
5. Compare the two stacking contexts at the level where they share a parent

### Common Fixes

```css
/* Create explicit stacking context on a shared parent */
.layout {
  isolation: isolate;
}

/* If an ancestor's transform/opacity creates an unwanted context, move the
   positioned element outside that ancestor in the DOM */
```

## Custom Property Resolution

### Trace a Custom Property

1. **Find the declaration**: where is `--my-prop` set?
2. **Check inheritance**: custom properties inherit — which ancestor's value wins?
3. **Check specificity**: higher-specificity selector's value wins
4. **Check `@layer` order**: layered declarations follow layer order
5. **Check `@property` registration**: if registered, `initial-value` is the fallback
6. **Check the `var()` fallback**: `var(--my-prop, fallback)` — is the fallback showing?

### Common Issues

**Problem**: Custom property shows as "invalid value."
**Cause**: The property resolves to a value that's invalid for the CSS property it's used in. Custom properties are resolved at *computed value time*, not parse time.

**Problem**: `var()` fallback is showing instead of the variable value.
**Cause**: The property is not set on the element or any ancestor. Check spelling, check scope.

**Problem**: `@property`-registered property doesn't animate.
**Cause**: The `syntax` doesn't match the actual value being set, or `inherits` is wrong.

## Performance Debugging

### Layout Thrashing

```
Symptom: Janky scrolling, slow interactions.

Look for:
- Animating width, height, top, left, margin, padding → triggers layout
- Animating box-shadow with large spread → expensive paint
- will-change on too many elements → GPU memory pressure
- Large DOM with no content-visibility → rendering off-screen content

Fixes:
- Animate only transform and opacity
- Use contain: layout style paint on isolated components
- Use content-visibility: auto on below-fold sections
- Use will-change only on actively animating elements
```

### Cumulative Layout Shift (CLS)

```
Symptom: Content jumps around during load.

Common CSS causes:
- Images/videos without explicit dimensions → use aspect-ratio
- Web fonts swapping → use font-display: swap + size-adjust
- Dynamic content insertion without reserved space
- Ads/embeds without fixed containers

Fixes:
img, video { aspect-ratio: 16 / 9; width: 100%; height: auto; }
.ad-slot { min-height: 250px; contain: layout; }
```

### Paint Performance

```
Symptom: High paint times in DevTools.

Look for:
- Large box-shadow on many elements
- backdrop-filter: blur() on large areas
- Clip-path with complex shapes recalculating
- Overuse of mix-blend-mode

Fixes:
- Simplify shadows (reduce blur radius)
- Limit backdrop-filter to small overlays
- Use contain: paint on independent sections
- Pre-render complex effects as images if static
```

## Output Format

For every bug, provide a structured diagnosis:

```
BUG: [one-line description]
CATEGORY: [specificity | inheritance | layout | stacking | custom-prop | perf]
ROOT CAUSE: [what's actually happening and why]
FILE: [file:line]

BEFORE:
[the buggy CSS]

AFTER:
[the fix]

WHY: [explain why this fixes it]
```

## Quick Reference: Diagnostic Commands

| Technique | CSS |
|-----------|-----|
| Outline everything | `* { outline: 1px solid red; }` |
| Show overflow | `* { outline: 1px solid red; overflow: visible !important; }` |
| Highlight stacking | `* { position: relative; outline: 1px solid blue; }` |
| Show empty elements | `*:empty { outline: 2px dashed orange; }` |
| Highlight focus order | `:focus { outline: 3px solid lime !important; }` |
| Show box sizing | `* { background: oklch(60% 0.2 0 / 0.05); }` |

## Rules

- Never suggest `!important` as a fix — find the actual specificity root cause
- Always identify which stacking context an element belongs to before changing z-index
- Check `box-sizing` before diagnosing any sizing bug
- When fixing layout issues, verify the fix doesn't break other viewport sizes
- For performance issues, suggest `contain` and `content-visibility` before other optimizations
- The outline technique is preferred over border for debugging — outlines don't affect layout
