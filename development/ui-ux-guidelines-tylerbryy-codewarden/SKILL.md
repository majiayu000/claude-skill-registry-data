---
name: ui-ux-guidelines
description: Enforce comprehensive UI/UX best practices for accessible, performant, and delightful interfaces. Use when building components, reviewing UI code, or evaluating user experiences.
allowed-tools: Read, Grep, Glob, Edit
---

# UI/UX Guidelines for Accessible, Fast, Delightful Interfaces

## Purpose

This skill enforces industry best practices for building accessible, performant, and user-friendly interfaces. Use MUST/SHOULD/NEVER rules to guide decisions across interactions, animation, layout, content, performance, and design.

## When to Use This Skill

Activate when:
- Building new UI components
- Reviewing existing component implementations
- Implementing forms or interactive elements
- Optimizing for accessibility or performance
- Designing animations or transitions
- Creating responsive layouts
- Evaluating user experience patterns

---

## Interactions

### Keyboard Navigation

- **MUST**: Full keyboard support per [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/patterns/)
- **MUST**: Visible focus rings (`:focus-visible`; group with `:focus-within`)
- **MUST**: Manage focus (trap, move, and return) per APG patterns

### Targets & Input

- **MUST**: Hit target ≥24px (mobile ≥44px). If visual <24px, expand hit area
- **MUST**: Mobile `<input>` font-size ≥16px or set:
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
  ```
- **NEVER**: Disable browser zoom
- **MUST**: `touch-action: manipulation` to prevent double-tap zoom; set `-webkit-tap-highlight-color` to match design

### Inputs & Forms (Behavior)

- **MUST**: Hydration-safe inputs (no lost focus/value)
- **NEVER**: Block paste in `<input>`/`<textarea>`
- **MUST**: Loading buttons show spinner and keep original label
- **MUST**: Enter submits focused text input. In `<textarea>`, ⌘/Ctrl+Enter submits; Enter adds newline
- **MUST**: Keep submit enabled until request starts; then disable, show spinner, use idempotency key
- **MUST**: Don't block typing; accept free text and validate after
- **MUST**: Allow submitting incomplete forms to surface validation
- **MUST**: Errors inline next to fields; on submit, focus first error
- **MUST**: `autocomplete` + meaningful `name`; correct `type` and `inputmode`
- **SHOULD**: Disable spellcheck for emails/codes/usernames
- **SHOULD**: Placeholders end with ellipsis and show example pattern (e.g., `+1 (123) 456-7890`, `sk-012345…`)
- **MUST**: Warn on unsaved changes before navigation
- **MUST**: Compatible with password managers & 2FA; allow pasting one-time codes
- **MUST**: Avoid `autocomplete="off"` unless security-critical; don't trigger password managers for non-auth fields
- **MUST**: Trim values to handle text expansion trailing spaces
- **MUST**: No dead zones on checkboxes/radios; label+control share one generous hit target

### State & Navigation

- **MUST**: URL reflects state (deep-link filters/tabs/pagination/expanded panels). Prefer libs like [nuqs](https://nuqs.dev)
- **MUST**: Back/Forward restores scroll
- **MUST**: Links are links—use `<a>`/`<Link>` for navigation (support Cmd/Ctrl/middle-click)

### Feedback

- **SHOULD**: Optimistic UI; reconcile on response; on failure show error and rollback or offer Undo
- **MUST**: Confirm destructive actions or provide Undo window
- **MUST**: Use polite `aria-live` for toasts/inline validation
- **SHOULD**: Ellipsis (`…`) for options that open follow-ups (e.g., "Rename…") and loading states (e.g., "Loading…", "Saving…", "Generating…")

### Touch/Drag/Scroll

- **MUST**: Design forgiving interactions (generous targets, clear affordances; avoid finickiness)
- **MUST**: Delay first tooltip in a group; subsequent peers no delay
- **MUST**: Intentional `overscroll-behavior: contain` in modals/drawers
- **MUST**: During drag, disable text selection and set `inert` on dragged element/containers
- **MUST**: No "dead-looking" interactive zones—if it looks clickable, it is

### Autofocus

- **SHOULD**: Autofocus on desktop when there's a single primary input; rarely on mobile (to avoid layout shift)

---

## Animation

- **MUST**: Honor `prefers-reduced-motion` (provide reduced variant)
- **SHOULD**: Prefer CSS > Web Animations API > JS libraries
- **MUST**: Animate compositor-friendly props (`transform`, `opacity`); avoid layout/repaint props (`top`/`left`/`width`/`height`)
- **NEVER**: Use `transition: all` (explicitly list properties to avoid unintended animations)
- **SHOULD**: Animate only to clarify cause/effect or add deliberate delight
- **SHOULD**: Choose easing to match the change (size/distance/trigger)
- **MUST**: Animations are interruptible and input-driven (avoid autoplay)
- **MUST**: Correct `transform-origin` (motion starts where it "physically" should)

### Cross-Browser Compatibility

- **MUST**: Apply CSS transforms to SVG children (`<g>`), not parent `<svg>` (Safari/Firefox rendering bugs)
- **MUST**: Set `transform-box: fill-box` and `transform-origin: center` on SVG elements when animating
- **SHOULD**: Use `translateZ(0)` or `will-change: transform` if text anti-aliasing artifacts appear during transforms

---

## Layout

- **SHOULD**: Optical alignment; adjust by ±1px when perception beats geometry
- **MUST**: Deliberate alignment to grid/baseline/edges/optical centers—no accidental placement
- **SHOULD**: Balance icon/text lockups (stroke/weight/size/spacing/color)
- **MUST**: Verify mobile, laptop, ultra-wide (simulate ultra-wide at 50% zoom)
- **MUST**: Respect safe areas (use `env(safe-area-inset-*)`)
- **MUST**: Avoid unwanted scrollbars; fix overflows

---

## Content & Accessibility

- **SHOULD**: Inline help first; tooltips last resort
- **MUST**: Skeletons mirror final content to avoid layout shift
- **MUST**: `<title>` matches current context
- **MUST**: No dead ends; always offer next step/recovery
- **MUST**: Design empty/sparse/dense/error states
- **SHOULD**: Curly quotes (" "); avoid widows/orphans
- **MUST**: Tabular numbers for comparisons (`font-variant-numeric: tabular-nums` or a mono like Geist Mono)
- **MUST**: Redundant status cues (not color-only); icons have text labels
- **MUST**: Don't ship the schema—visuals may omit labels but accessible names still exist
- **MUST**: Use the ellipsis character `…` (not `...`)
- **MUST**: `scroll-margin-top` on headings for anchored links; include a "Skip to content" link; hierarchical `<h1–h6>`
- **MUST**: Resilient to user-generated content (short/avg/very long)
- **MUST**: Locale-aware dates/times/numbers/currency
- **MUST**: Accurate names (`aria-label`), decorative elements `aria-hidden`, verify in the Accessibility Tree
- **MUST**: Icon-only buttons have descriptive `aria-label`
- **MUST**: Prefer native semantics (`button`, `a`, `label`, `table`) before ARIA
- **SHOULD**: Right-clicking the nav logo surfaces brand assets
- **MUST**: Use non-breaking spaces to glue terms: `10&nbsp;MB`, `⌘&nbsp;+&nbsp;K`, `Vercel&nbsp;SDK`; use `&#x2060;` for zero-width
- **MUST**: Detect language via `Accept-Language` header and `navigator.languages`, NOT IP geolocation

---

## Performance

- **SHOULD**: Test iOS Low Power Mode and macOS Safari
- **MUST**: Measure reliably (disable extensions that skew runtime)
- **MUST**: Track and minimize re-renders (React DevTools/React Scan)
- **MUST**: Profile with CPU/network throttling
- **MUST**: Batch layout reads/writes; avoid unnecessary reflows/repaints
- **MUST**: Mutations (`POST`/`PATCH`/`DELETE`) complete in <500 ms
- **SHOULD**: Prefer uncontrolled inputs; make controlled loops cheap (keystroke cost)
- **MUST**: Virtualize large lists (e.g., `virtua`) or use `content-visibility: auto`
- **MUST**: Preload only above-the-fold images; lazy-load the rest
- **MUST**: Prevent CLS from images (explicit dimensions or reserved space)
- **SHOULD**: Use `<link rel="preconnect">` for asset/CDN domains (with `crossorigin` when needed)
- **SHOULD**: Preload critical fonts to avoid FOUT and layout shift
- **SHOULD**: Subset fonts to only used characters/scripts via `unicode-range`
- **SHOULD**: Move expensive work to Web Workers to avoid blocking main thread

---

## Design

- **SHOULD**: Layered shadows (ambient + direct)
- **SHOULD**: Crisp edges via semi-transparent borders + shadows
- **SHOULD**: Nested radii: child ≤ parent; concentric
- **SHOULD**: Hue consistency: tint borders/shadows/text toward bg hue
- **MUST**: Accessible charts (color-blind-friendly palettes)
- **MUST**: Meet contrast—prefer [APCA](https://apcacontrast.com/) over WCAG 2
- **MUST**: Increase contrast on `:hover`/`:active`/`:focus`
- **SHOULD**: Set `<meta name="theme-color">` to match page background
- **MUST**: Set `color-scheme: dark` on `<html>` in dark themes (ensures proper scrollbar/device UI contrast)
- **MUST**: On Windows, set explicit `background-color` and `color` on `<select>` to avoid dark mode contrast bugs
- **SHOULD**: Avoid gradient banding (use masks when needed)

---

## Copywriting Guidelines

> **Note**: These guidelines reflect Vercel's style guide and are provided as a reference. Adapt these principles to match your brand voice and design system.

- **SHOULD**: Active voice for actions ("Deploy your project" vs "Your project can be deployed")
- **SHOULD**: Title Case for main headings (Chicago style), sentence case for body text
- **SHOULD**: Use numerals for all numbers ("3 items" not "three items")
- **SHOULD**: Prefer `&` over "and" in UI text
- **SHOULD**: Action-oriented language ("Install the CLI" vs "You will need the CLI")
- **SHOULD**: Keep nouns consistent; introduce as few unique terms as possible
- **SHOULD**: Write in second person; avoid first person
- **SHOULD**: Use consistent placeholders (`YOUR_API_TOKEN_HERE` for strings, `0123456789` for numbers)
- **SHOULD**: Separate numbers & units with non-breaking space (`10&nbsp;MB`)
- **MUST**: Default to positive language; frame errors as problems to solve, not failures
- **MUST**: Error messages guide recovery (tell how to fix, not just what went wrong)
- **MUST**: Avoid ambiguity in button labels; be specific ("Save API Key" vs generic "Continue")
- **SHOULD**: Use ellipsis character `…` (not `...`)
- **SHOULD**: Use curly quotes (" ") over straight quotes (" ")

---

## How to Use This Skill

When reviewing or building UI:

1. **Scan the component**
   - Identify interactive elements (buttons, inputs, links)
   - Check for keyboard navigation support
   - Verify accessibility attributes

2. **Check for violations**
   - Search for blocked paste handlers
   - Look for missing `aria-label` on icon buttons
   - Verify form validation patterns
   - Check for animations without `prefers-reduced-motion`

3. **Verify patterns**
   - Forms have proper validation and error handling
   - Loading states preserve button labels
   - URLs reflect application state
   - Focus management follows APG patterns

4. **Test responsiveness**
   - Mobile hit targets ≥44px
   - Input font sizes ≥16px on mobile
   - Safe area insets respected
   - Ultra-wide layouts verified

5. **Performance checks**
   - Images have dimensions
   - Animations use compositor-friendly properties
   - Large lists are virtualized
   - Re-renders are minimized

## Integration with React Skill

This skill works alongside `react-next-modern`:
- React skill handles **architectural patterns** (Server Components, async data)
- This skill handles **UI/UX implementation** (accessibility, interactions, design)

Both skills should be active when building or reviewing frontend code.

---

## Common Violations to Watch For

### ❌ Bad: Blocking paste
```tsx
<input onPaste={(e) => e.preventDefault()} />
```

### ✅ Good: Allow paste
```tsx
<input type="email" autoComplete="email" />
```

---

### ❌ Bad: No keyboard support
```tsx
<div onClick={handleClick}>Click me</div>
```

### ✅ Good: Proper button
```tsx
<button onClick={handleClick}>Click me</button>
```

---

### ❌ Bad: Icon button without label
```tsx
<button><TrashIcon /></button>
```

### ✅ Good: Descriptive label
```tsx
<button aria-label="Delete item"><TrashIcon /></button>
```

---

### ❌ Bad: Animation without reduced motion
```css
.element {
  animation: slide 300ms ease-out;
}
```

### ✅ Good: Respects user preference
```css
.element {
  animation: slide 300ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .element {
    animation: none;
  }
}
```

---

### ❌ Bad: Small mobile hit target
```tsx
<button className="w-4 h-4">×</button>
```

### ✅ Good: Generous hit area
```tsx
<button className="w-4 h-4 p-4">×</button>
```

---

### ❌ Bad: Color-only status
```tsx
<div className="text-red-500">Error occurred</div>
```

### ✅ Good: Icon + text
```tsx
<div className="text-red-500">
  <AlertIcon aria-hidden="true" />
  <span>Error occurred</span>
</div>
```

---

### ❌ Bad: Using transition: all
```css
.button {
  transition: all 300ms ease;
}
```

### ✅ Good: Explicit properties
```css
.button {
  transition: background-color 300ms ease, transform 300ms ease;
}
```

---

### ❌ Bad: Blocking password managers
```tsx
<input type="password" autoComplete="off" />
```

### ✅ Good: Allow password managers
```tsx
<input type="password" autoComplete="current-password" />
```

---

### ❌ Bad: Vague error message
```tsx
<div>Your deployment failed.</div>
<button>Continue</button>
```

### ✅ Good: Clear, actionable guidance
```tsx
<div>
  Your API key is incorrect or expired.
  <a href="/settings">Generate a new key</a> in settings.
</div>
<button>Save API Key</button>
```

---

### ❌ Bad: Windows select with default styles
```tsx
<select>
  <option>Option 1</option>
</select>
```

### ✅ Good: Explicit colors for Windows
```tsx
<select className="bg-white dark:bg-gray-900 text-black dark:text-white">
  <option>Option 1</option>
</select>
```

---

## References

- [WAI-ARIA APG Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [APCA Contrast Calculator](https://apcacontrast.com/)
- [nuqs - URL State Management](https://nuqs.dev)
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [virtua - List Virtualization](https://github.com/inokawa/virtua)

---

## Summary

Use these guidelines to build interfaces that are:
- **Accessible**: Keyboard navigation, screen readers, WCAG compliance
- **Fast**: Optimized animations, virtualized lists, minimal re-renders
- **Delightful**: Thoughtful interactions, clear feedback, forgiving UX
- **Resilient**: Handle edge cases, provide recovery paths, test thoroughly
