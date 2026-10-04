---
name: frontend-design
description: >
  Create distinctive, production-ready frontend interfaces with high visual quality.
  Use this skill whenever the user asks to build, design, or improve any web UI —
  including landing pages, dashboards, components, app screens, forms, or interactive
  widgets. Also trigger when the user says "make this look better", "redesign this",
  "add polish", "build a UI", "create a page", "style this", or references HTML/CSS/JS,
  React, Vue, Svelte, or any frontend framework. If the request involves any visible
  output rendered in a browser, use this skill — even if the user hasn't explicitly
  said "design." This skill produces intentional, memorable interfaces that avoid
  generic AI patterns.
---

# Frontend Design Skill

Build distinctive, production-grade frontend interfaces. Avoid generic "AI slop" aesthetics.
Deliver code that is functional, accessible, responsive, and visually intentional.

---

## Step 0 — Gather Context Before Writing Code

Infer or confirm before starting:

| Input | What to look for |
|---|---|
| Product purpose | What it does, who uses it |
| Tone | Serious / playful / premium / technical / warm |
| Framework | HTML+CSS+JS, React, Vue, Svelte, etc. |
| Device priority | Mobile-first, desktop-first, or both |
| Existing brand | Colors, fonts, tokens to preserve |
| Required content | Sections, forms, tables, media |

If the user wants speed, make reasonable assumptions and state them in one line.
If the user has provided a brief, start immediately — do not re-ask what they gave you.

---

## Step 1 — Choose a Visual Direction

Pick **one clear concept** and commit to it. Write a 2-line concept statement:
- Who it is for
- What it should feel like and what makes it stand out

**Example concepts:**
- Editorial minimal — quiet grid, strong typographic hierarchy, intentional white space
- Neo-brutalist — thick borders, raw contrast, uneven layouts, deliberate tension
- Soft organic — rounded shapes, warm tones, friendly motion, natural metaphors
- Industrial technical — monospaced type, data-dense, muted palette with precise accents
- Retro-futurist — bold geometry, gradient depth, vintage + modern collision

Do not default to "clean modern SaaS." That is not a direction — it is the absence of one.

---

## Step 2 — Define a Design System

Set all tokens before writing component code. Use CSS custom properties or framework equivalents.

### Typography
```css
/* Pair a display/heading font with a body font — contrast in personality */
--font-display: 'Your Display Font', serif;
--font-body: 'Your Body Font', sans-serif;
--font-mono: 'Your Mono Font', monospace;

/* Scale — use a consistent ratio (1.25, 1.333, or 1.5) */
--text-xs: 0.75rem;
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-xl: 1.25rem;
--text-2xl: 1.5rem;
--text-3xl: 2rem;
--text-4xl: 2.75rem;
```

### Color
```css
/* Dominant neutral + intentional accent + semantic states */
--color-bg: #...;
--color-surface: #...;
--color-border: #...;
--color-text-primary: #...;
--color-text-secondary: #...;
--color-accent: #...;
--color-accent-hover: #...;
--color-success: #...;
--color-error: #...;
```

### Spacing, Radius, Shadow
```css
/* Spacing on a consistent scale */
--space-1: 0.25rem;  --space-2: 0.5rem;
--space-3: 0.75rem;  --space-4: 1rem;
--space-6: 1.5rem;   --space-8: 2rem;
--space-12: 3rem;    --space-16: 4rem;

/* Radius — pick a personality and hold it */
--radius-sm: 4px;  --radius-md: 8px;  --radius-lg: 16px;  --radius-full: 9999px;

/* Shadows — use sparingly for real depth */
--shadow-sm: 0 1px 2px rgba(0,0,0,0.06);
--shadow-md: 0 4px 12px rgba(0,0,0,0.10);
--shadow-lg: 0 8px 24px rgba(0,0,0,0.14);
```

### Motion
```css
--duration-fast: 120ms;
--duration-base: 200ms;
--duration-slow: 350ms;
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}
```

---

## Step 3 — Plan Layout and Hierarchy

Before writing markup, sketch the content flow:

- **Primary action** — most visual weight, highest contrast
- **Supporting content** — clear grouping, breathing room
- **Secondary / contextual** — subdued, accessible but not competing

Layout principles to apply:
- Use asymmetry and rhythm shifts to avoid monotony
- Vary column widths, not just row heights
- Overlap elements deliberately when it creates depth
- Keep visual weight balanced — do not crowd all interest into one corner

Avoid:
- "Three equal cards, centered" as the default structure for everything
- Navigation that looks like every other site's navigation
- Full-width hero with centered H1 + paragraph + two buttons (unless brief demands it)

---

## Step 4 — Write Implementation-Quality Code

### HTML / Vanilla
- Use semantic elements: `<main>`, `<nav>`, `<section>`, `<article>`, `<aside>`, `<header>`, `<footer>`
- Add `aria-label` to interactive regions and icon-only buttons
- Use `<button>` for actions, `<a>` for navigation
- Keep CSS in `<style>` block or a dedicated file — no inline styles except dynamic values

### React
- One component per responsibility
- No hardcoded colors or sizes — use token variables
- Handle states: loading, empty, error, hover, active, disabled
- Accept `className` prop for composability when relevant

### Vue / Svelte / Other
- Same principles — tokens, semantic markup, state handling, accessibility
- Use scoped styles unless sharing tokens across components

### Responsive pattern
```css
/* Mobile-first baseline */
.container { padding: var(--space-4); }

@media (min-width: 768px) {
  .container { padding: var(--space-8); }
}

@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: 0 auto; padding: var(--space-12); }
}
```

---

## Step 5 — Add Meaningful Motion

Apply motion at these moments only — do not animate everything:

| Moment | Pattern |
|---|---|
| Page / section entrance | Fade + subtle translate-up, staggered by 60–80ms |
| Button / link hover | Color shift + slight scale or underline |
| Modal / drawer open | Slide in from edge or scale from trigger |
| Loading state | Skeleton shimmer or subtle pulse |
| Success / error | Brief color flash + icon entrance |

Keep total animation budget low. Three well-placed transitions feel premium.
Twenty micro-animations feel cheap.

---

## Step 6 — Accessibility Checklist

Run through before finalizing:

- [ ] All interactive elements reachable by keyboard (Tab order logical)
- [ ] Visible `:focus-visible` styles on all focusable elements
- [ ] Color contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text and UI components
- [ ] Images have meaningful `alt` text (or `alt=""` if decorative)
- [ ] Form inputs have associated `<label>` elements
- [ ] ARIA roles only where native semantics are insufficient
- [ ] Reduced-motion preference respected

---

## Step 7 — Quality Validation

Before delivering:

- [ ] Renders correctly at 375px (iPhone SE), 768px (tablet), 1280px (desktop)
- [ ] No content overflow or broken layout at any width
- [ ] Tokens used consistently — no one-off hardcoded values
- [ ] All interactive states exist (hover, active, focus, disabled)
- [ ] Visual concept is cohesive — nothing looks out of place
- [ ] Performance: no unnecessary large images, no blocking animations on scroll

---

## Output Format

Return work in this order:

1. **Concept direction** — 2–4 lines: target user, aesthetic intent, what makes it memorable
2. **Design system summary** — typography, color palette, spacing choices
3. **Implementation notes** — what was built, key decisions made
4. **Complete runnable code** — full file(s), no placeholders or "add your content here"
5. **Validation summary** — brief confirmation of responsiveness, accessibility, performance

---

## Common Mistakes to Avoid

| Anti-pattern | Better approach |
|---|---|
| Generic sans-serif + blue CTA | Choose a font pairing with personality; pick an accent that earns its place |
| Equal three-column card grid | Vary layout rhythm; use feature cards, split layouts, or asymmetric grids |
| Centered hero with H1 + two buttons | Give the hero a structural idea — image offset, text overlap, editorial crop |
| Shadow on every element | Use shadow only for elevation; most elements are flat |
| Animation on every hover | Reserve motion for meaningful transitions |
| Inline style overrides | All values in CSS tokens; no `style="color: red"` |
| Missing empty/error states | Every data-driven component needs these states |

---

## Framework-Specific Notes

**React**: Use `useState`/`useEffect` for interaction state. Tokens live in a shared `theme.js` or `:root` CSS vars imported globally.

**Vue 3**: Use `<script setup>` + CSS variables in `:root`. Composables for reusable interaction logic.

**Svelte**: Use CSS custom properties in `:root` via `<svelte:head>`. Stores for cross-component state.

**HTML/CSS/JS (no framework)**: Single file or clearly separated `style.css` + `main.js`. Use `data-*` attributes for JS hooks, never style-coupled class names.

**Tailwind**: Define design tokens in `tailwind.config.js`. Use `@apply` sparingly — prefer utility classes inline. Extend the theme rather than overriding with arbitrary values.