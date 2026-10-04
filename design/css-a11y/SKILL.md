---
name: css-a11y
description: >-
  CSS accessibility audit and fixes. Checks focus-visible styles, reduced motion
  support, contrast preferences, forced-colors mode, visually-hidden patterns,
  touch target sizes, color contrast ratios, color-only indicators, skip links,
  and reading order. Use when auditing accessibility, fixing a11y issues, adding
  focus styles, supporting reduced motion, improving contrast, or making CSS
  accessible.
disable-model-invocation: true
license: MIT
---

# css-a11y — CSS Accessibility Audit & Fixes

You are a CSS accessibility specialist. Your job is to audit stylesheets for accessibility failures and provide fixes using modern CSS. Every interactive element must be keyboard-accessible, every preference media query must be respected, and contrast must meet WCAG 2.2 AA minimums.

For anti-patterns that cause accessibility failures, see the css-expert skill's [anti-patterns.md](../css-expert/references/anti-patterns.md). For browser support on `:focus-visible`, `prefers-contrast`, `forced-colors`, and related features, see [browser-compat.md](../css-expert/references/browser-compat.md).

## Workflow

```
Accessibility Audit Progress:
- [ ] Step 1: Scan for focus style issues
- [ ] Step 2: Check prefers-reduced-motion support
- [ ] Step 3: Check prefers-contrast support
- [ ] Step 4: Check forced-colors mode support
- [ ] Step 5: Verify touch target sizes
- [ ] Step 6: Audit color contrast ratios
- [ ] Step 7: Check for color-only indicators
- [ ] Step 8: Verify visually-hidden pattern
- [ ] Step 9: Check skip links
- [ ] Step 10: Verify logical reading order
- [ ] Step 11: Generate report
```

## Step 1: Focus Styles

### What to Find

Search for these violations:

- `outline: none` or `outline: 0` without a replacement
- `:focus` styles without `:focus-visible`
- Interactive elements (`a`, `button`, `input`, `select`, `textarea`, `[tabindex]`) with no focus styles at all
- Focus styles that rely on color change alone (fail for colorblind users)

### Required Pattern

Every interactive element must have a visible `:focus-visible` style:

```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

### Acceptable Variations

```css
/* Custom focus ring */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: var(--radius-s);
}

/* Inner focus ring for contained elements */
.button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: -2px;
}

/* High-contrast focus ring (visible on any background) */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px var(--color-surface);
}
```

### Never

- `*:focus { outline: none; }` — this breaks keyboard navigation
- `:focus` without `:focus-visible` — shows rings on mouse clicks
- Focus styles that use only `box-shadow` — invisible in forced-colors mode

## Step 2: prefers-reduced-motion

### What to Find

- Any `animation` or `transition` without a `prefers-reduced-motion` counterpart
- `@keyframes` definitions used without a reduced-motion media query
- Scroll-driven animations without opt-out

### Required Pattern

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

This global reset is the minimum. For finer control, address per-component:

```css
.hero {
  animation: slide-in 600ms ease;
}

@media (prefers-reduced-motion: reduce) {
  .hero {
    animation: none;
  }
}
```

### Essential vs Non-Essential Motion

- **Essential** (keep): loading spinners, progress indicators, form validation feedback
- **Non-essential** (reduce/remove): decorative transitions, parallax, entrance animations, hover effects, auto-playing carousels

For essential motion, reduce but don't remove:

```css
@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation-duration: 1.5s;
    /* slower but still functional */
  }
}
```

## Step 3: prefers-contrast

### What to Find

- No `prefers-contrast` media query in the codebase
- Low-contrast borders (e.g., light gray on white)
- Muted/subtle text that becomes unreadable at higher contrast

### Required Pattern

```css
@media (prefers-contrast: more) {
  :root {
    --color-text: light-dark(oklch(5% 0 0), oklch(98% 0 0));
    --color-text-muted: light-dark(oklch(25% 0 0), oklch(85% 0 0));
    --color-border: light-dark(oklch(30% 0 0), oklch(80% 0 0));
  }

  .card {
    border-width: 2px;
    border-color: var(--color-border);
  }

  .button[data-variant="ghost"] {
    border: 2px solid currentColor;
  }
}
```

Key actions in `prefers-contrast: more`:
- Darken body text toward black/white
- Make muted text visible (bump contrast)
- Increase border widths
- Add borders to elements that rely on background-only differentiation
- Increase font weight for thin text

## Step 4: forced-colors Mode

### What to Find

- Elements that rely solely on `background-color` for meaning
- Custom SVG icons with hardcoded fills
- Decorative borders that carry semantic meaning
- Focus indicators using only `box-shadow` (invisible in forced-colors)

### Required Pattern

```css
@media (forced-colors: active) {
  .button {
    border: 1px solid ButtonText;
  }

  .badge {
    border: 1px solid;
    forced-color-adjust: none; /* only if you need to preserve a specific color */
  }

  .icon {
    fill: currentColor;
    stroke: currentColor;
  }

  .card {
    border: 1px solid CanvasText;
  }

  :focus-visible {
    outline: 2px solid Highlight;
    outline-offset: 2px;
  }
}
```

System color keywords to use: `Canvas`, `CanvasText`, `LinkText`, `ButtonFace`, `ButtonText`, `Highlight`, `HighlightText`, `GrayText`, `Mark`, `MarkText`.

## Step 5: Touch Target Sizes

### What to Find

- Buttons, links, or interactive elements smaller than 44x44px
- Icon buttons with no padding
- Inline links in dense text with no vertical padding

### Required Minimum

```css
.interactive {
  min-width: 44px;
  min-height: 44px;
}
```

### Techniques for Small Visual Elements

```css
/* Visually small, functionally large */
.icon-button {
  position: relative;
  /* visual size */
  width: 24px;
  height: 24px;

  &::after {
    content: "";
    position: absolute;
    inset: -10px;
    /* actual touch area: 44x44 */
  }
}
```

For inline links, ensure adequate line-height and padding:

```css
.prose a {
  padding-block: 0.125em;
}
```

## Step 6: Color Contrast Ratios

### WCAG 2.2 AA Minimums

| Element | Minimum Ratio |
|---------|---------------|
| Normal text (< 24px / < 18.66px bold) | 4.5:1 |
| Large text (>= 24px / >= 18.66px bold) | 3:1 |
| UI components and graphical objects | 3:1 |
| Decorative/disabled elements | No requirement |

### What to Find

- Light gray text on white backgrounds
- Placeholder text with insufficient contrast
- Disabled states that are unreadable (though not required, still best practice)
- Text over images or gradients without a backdrop

### Fix Patterns

```css
/* Ensure text-on-image readability */
.hero-text {
  text-shadow: 0 1px 3px oklch(0% 0 0 / 0.5);
  /* or use a backdrop */
  background: oklch(0% 0 0 / 0.6);
  padding: var(--space-s) var(--space-m);
}

/* Placeholder contrast */
::placeholder {
  color: var(--color-text-muted);
  opacity: 1;
}
```

When recommending colors, verify the contrast ratio. If you can't compute it precisely, err on the side of higher contrast.

## Step 7: Color-Only Indicators

### What to Find

- Form validation using only red/green border colors
- Status indicators using only colored dots
- Links distinguishable from body text only by color
- Charts/graphs using only color for data series

### Required Pattern

Always pair color with a secondary indicator — shape, icon, text, pattern, or border treatment:

```css
/* Form validation — color + icon + border */
.field[aria-invalid="true"] {
  border-color: var(--color-error);
  border-inline-start-width: 3px;
}

.field[aria-invalid="true"] + .error-message::before {
  content: "\26A0\FE0F "; /* warning sign */
}

/* Links — color + underline */
.prose a {
  color: var(--color-primary);
  text-decoration: underline;
  text-underline-offset: 0.15em;
}
```

## Step 8: Visually-Hidden Pattern

Ensure a proper `.visually-hidden` / `.sr-only` utility exists:

```css
.visually-hidden {
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
```

### Common Uses

- Skip link text
- Icon button labels
- Form field descriptions
- Section headings for screen readers
- Table captions

### Anti-Pattern

```css
/* BAD — content removed from accessibility tree */
.hide { display: none; }
.hide { visibility: hidden; }

/* BAD — incomplete hiding, may cause layout shifts */
.hide { font-size: 0; }
.hide { text-indent: -9999px; }
```

## Step 9: Skip Links

Verify a skip link exists as the first focusable element:

```css
.skip-link {
  position: absolute;
  inset-inline-start: 0;
  inset-block-start: 0;
  padding: var(--space-s) var(--space-m);
  background: var(--color-surface);
  color: var(--color-text);
  transform: translateY(-100%);
  transition: transform 150ms ease;
  z-index: 9999;

  &:focus-visible {
    transform: translateY(0);
  }
}
```

It should link to `#main-content` or the primary content landmark.

## Step 10: Logical Reading Order

### What to Find

- CSS `order` property that makes visual order differ from DOM order
- `flex-direction: row-reverse` or `column-reverse` breaking tab order
- Grid placement that rearranges content away from source order
- `position: absolute` pulling content out of flow in a way that breaks logical order

### Rule

Visual order should match DOM order for keyboard navigation. If `order` or visual reordering is used, ensure `tabindex` or ARIA attributes compensate. Flag any case where CSS reordering creates a mismatch.

```css
/* WARNING: This changes visual order but not tab order */
.nav { display: flex; flex-direction: row-reverse; }

/* If needed, use reading-flow (emerging) or restructure the DOM */
```

## Step 11: Generate Report

Produce a structured audit report:

```
CSS Accessibility Audit Report
==============================

CRITICAL (must fix):
- [FOCUS] outline: none found in reset.css:12 — no replacement provided
- [MOTION] 6 animations have no prefers-reduced-motion fallback
- [CONTRAST] .text-muted has 2.8:1 ratio (needs 4.5:1)

WARNINGS (should fix):
- [TOUCH] .icon-btn is 32x32px (needs 44x44px minimum)
- [COLOR] .status-dot uses color only — add shape/text indicator
- [ORDER] .nav uses flex-direction: row-reverse — verify tab order

PASSING:
- [FOCUS-VISIBLE] ✓ Global :focus-visible styles present
- [SKIP-LINK] ✓ Skip link found
- [VISUALLY-HIDDEN] ✓ Utility class present
- [FORCED-COLORS] ✓ forced-colors media query present

FILES REVIEWED: 8
ISSUES FOUND: 9 critical, 3 warnings
```

## Rules

- Never suggest `outline: none` without a visible replacement
- `prefers-reduced-motion` is non-negotiable — every animation needs it
- Focus styles must work in forced-colors mode (use `outline`, not just `box-shadow`)
- Don't use `display: none` for visually-hidden content — it removes from a11y tree
- Touch targets: 44x44px minimum, no exceptions for interactive elements
- Always verify color contrast when recommending color changes
