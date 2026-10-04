---
name: react-styling
description: React styling, design tokens, responsive layout, and motion — Tailwind, CSS Modules, CSS-in-JS, design tokens (CSS custom properties), breakpoints, container queries, CSS animations, Framer Motion, dark mode. Use when styling React components, implementing responsive design, building from Figma, adding animations, or setting up a design token system. Triggers on "Tailwind", "CSS", "styling", "responsive", "animation", "motion", "design tokens", "dark mode".
---

# react-styling

How a Senior UX Engineer styles React: design-token-driven, responsive by default, motion that respects users, and zero magic numbers.

## The "no magic numbers" rule

The fastest senior-vs-mid signal in any review:
```tsx
// Mid
<div className="mt-[17px] text-[#3a3a3a]">…</div>

// Senior
<div className="mt-4 text-neutral-800">…</div>
```

Every spacing, color, type-size, border-radius, and shadow value should be a token. If you find yourself typing `17px` or `#3a3a3a`, stop. Either there's an existing token close enough, or there's a missing token you should add.

## Design tokens via CSS custom properties

This works in any stack (Next, Vite, Astro). Define once, use everywhere:

```css
/* tokens.css */
:root {
  /* Color — semantic, not literal */
  --color-bg: hsl(0 0% 100%);
  --color-fg: hsl(0 0% 10%);
  --color-fg-muted: hsl(0 0% 40%);
  --color-brand: hsl(173 80% 40%);
  --color-brand-hover: hsl(173 80% 35%);
  --color-border: hsl(0 0% 90%);
  --color-danger: hsl(0 70% 50%);

  /* Space scale (8px-based) */
  --space-1: 0.25rem;  /* 4 */
  --space-2: 0.5rem;   /* 8 */
  --space-3: 0.75rem;  /* 12 */
  --space-4: 1rem;     /* 16 */
  --space-6: 1.5rem;   /* 24 */
  --space-8: 2rem;     /* 32 */
  --space-12: 3rem;    /* 48 */
  --space-16: 4rem;    /* 64 */

  /* Type scale */
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.5rem;
  --font-size-2xl: 2rem;
  --font-size-3xl: 3rem;

  /* Radii */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px hsl(0 0% 0% / 0.06);
  --shadow-md: 0 4px 12px hsl(0 0% 0% / 0.08);
  --shadow-lg: 0 12px 32px hsl(0 0% 0% / 0.12);

  /* Motion */
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  --duration-fast: 150ms;
  --duration-base: 250ms;
  --duration-slow: 400ms;
}

[data-theme="dark"] {
  --color-bg: hsl(0 0% 7%);
  --color-fg: hsl(0 0% 96%);
  --color-fg-muted: hsl(0 0% 65%);
  --color-border: hsl(0 0% 18%);
}
```

**Why CSS custom properties beat JS-only tokens**: they cascade, they animate, they switch theme without re-rendering React, and they work in `<style>` attributes.

## Tailwind: the senior playbook

### Configure tokens in `tailwind.config.ts`
```ts
import type { Config } from 'tailwindcss';

export default {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: 'hsl(var(--color-bg) / <alpha-value>)',
        fg: 'hsl(var(--color-fg) / <alpha-value>)',
        brand: {
          DEFAULT: 'hsl(var(--color-brand) / <alpha-value>)',
          hover: 'hsl(var(--color-brand-hover) / <alpha-value>)',
        },
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
      },
    },
  },
} satisfies Config;
```

This pattern (Tailwind classes → CSS variables → tokens) is what Radix UI, shadcn/ui, and every modern design system uses. Theme switching is just changing the variable values.

### Tailwind patterns to use

- **`cn` helper** for conditional classes:
  ```ts
  import { clsx, type ClassValue } from 'clsx';
  import { twMerge } from 'tailwind-merge';
  export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
  }
  ```
  ```tsx
  <button className={cn('btn', variant === 'primary' && 'btn-primary', className)} />
  ```

- **`cva` (class-variance-authority)** for variant components:
  ```ts
  import { cva } from 'class-variance-authority';
  const button = cva('inline-flex items-center justify-center font-medium rounded-md transition', {
    variants: {
      variant: {
        primary: 'bg-brand text-white hover:bg-brand-hover',
        ghost: 'bg-transparent text-fg hover:bg-fg/5',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-base',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  });
  ```

- **Arbitrary values sparingly** — if you need `mt-[17px]`, you probably need a missing token. Use `mt-[var(--specific-thing)]` if it's a one-off architectural decision.

### Tailwind smells

- Long, unreadable class strings → extract a component or use `cva`
- Inline conditional with `?` chains → use `cn` helper
- `!important` (`!`) for anything outside of utility overrides → fix specificity instead
- Inline arbitrary colors → add a token

## CSS Modules (alternative when Tailwind isn't on the table)

```css
/* Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  padding: var(--space-2) var(--space-4);
  background: var(--color-brand);
  color: white;
  border-radius: var(--radius-md);
  transition: background var(--duration-fast) var(--ease);
}
.button:hover { background: var(--color-brand-hover); }
.button:focus-visible {
  outline: 2px solid var(--color-brand);
  outline-offset: 2px;
}

.ghost {
  background: transparent;
  color: var(--color-fg);
}
.ghost:hover { background: hsl(var(--color-fg) / 0.06); }
```

```tsx
import s from './Button.module.css';
import { cn } from '@/lib/cn';

<button className={cn(s.button, variant === 'ghost' && s.ghost)} />
```

## Responsive: mobile-first by default

```tsx
// Tailwind — mobile-first, breakpoint utilities only ADD constraints upward
<div className="
  grid
  grid-cols-1 gap-4 p-4
  md:grid-cols-2 md:gap-6 md:p-8
  lg:grid-cols-3
">
```

```css
/* Plain CSS — mobile first */
.grid { display: grid; grid-template-columns: 1fr; gap: var(--space-4); }
@media (min-width: 768px) {
  .grid { grid-template-columns: repeat(2, 1fr); gap: var(--space-6); }
}
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
```

Common breakpoints (Tailwind defaults are sensible):
- `sm` 640px — phone landscape
- `md` 768px — tablet
- `lg` 1024px — small laptop
- `xl` 1280px — desktop
- `2xl` 1536px — large desktop

**Test at 320px wide.** If it breaks there, it's not responsive.

### Container queries (use when the layout depends on the container, not the viewport)

```css
.card-container { container-type: inline-size; }
.card { display: grid; grid-template-columns: 1fr; }
@container (min-width: 400px) {
  .card { grid-template-columns: 1fr 2fr; }
}
```

```tsx
// Tailwind v4 / with @tailwindcss/container-queries plugin
<div className="@container">
  <div className="grid grid-cols-1 @md:grid-cols-2">…</div>
</div>
```

Container queries are a strong senior signal because most candidates still use viewport queries everywhere. Use them when a card looks different in a sidebar vs. a full-width grid.

## Layout: flex vs. grid

- **Grid**: 2D layouts, page-level layouts, anything aligned in both rows and columns
- **Flex**: 1D layouts — a row of buttons, a vertical stack, "push items to the ends"

```tsx
{/* Common: nav with logo left, items right */}
<nav className="flex items-center justify-between">
  <Logo />
  <div className="flex items-center gap-4">…</div>
</nav>

{/* Common: card grid, auto-fit */}
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6">
```

`grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` is one of the most useful patterns: cards reflow without media queries.

## Animation — the senior playbook

### Animate the cheap properties only
GPU-accelerated, no layout: `transform`, `opacity`, `filter`.
Expensive (cause layout/paint): `width`, `height`, `top`, `left`, `margin`.

```css
/* Bad — causes layout on every frame */
.menu-enter { left: -300px; transition: left 0.3s; }
.menu-enter-active { left: 0; }

/* Good — composite-only */
.menu-enter { transform: translateX(-100%); transition: transform 0.3s var(--ease); }
.menu-enter-active { transform: translateX(0); }
```

### Always respect prefers-reduced-motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### CSS transitions for state, keyframes for ongoing motion

```css
/* State change — transition */
.btn { transform: scale(1); transition: transform var(--duration-fast) var(--ease); }
.btn:active { transform: scale(0.98); }

/* Ongoing motion — keyframes */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.skeleton { animation: pulse 1.5s ease-in-out infinite; }
```

### Framer Motion (use sparingly, only when CSS can't)

```tsx
import { motion, AnimatePresence } from 'framer-motion';

<AnimatePresence>
  {open && (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 8 }}
      transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}
    >
      …
    </motion.div>
  )}
</AnimatePresence>
```

Use Framer when:
- You need exit animations (CSS-only can't animate elements leaving the DOM cleanly)
- You need orchestration (stagger, sequence)
- You need gestures (drag, swipe)

Otherwise CSS wins on bundle size and perf.

### Scroll-triggered animation
Use `IntersectionObserver`, not scroll listeners:
```tsx
function FadeInOnScroll({ children }: { children: ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setVisible(true),
      { rootMargin: '0px 0px -10% 0px' }
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return (
    <div
      ref={ref}
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(12px)',
        transition: 'opacity 400ms var(--ease), transform 400ms var(--ease)',
      }}
    >
      {children}
    </div>
  );
}
```

For Tailwind, `animation-delay` utilities + the new `@starting-style` or libraries like `react-intersection-observer` work too.

## Dark mode

Three approaches, ranked:

1. **`class` strategy + CSS variables** (recommended): toggle a class on `<html>`, all tokens flip via cascade.
   ```html
   <html class="dark">
   ```
   ```css
   :root { --color-bg: white; }
   .dark { --color-bg: black; }
   ```
   In Tailwind: configure `darkMode: 'class'`.

2. **`prefers-color-scheme`** only: respects system, no toggle.
   ```css
   @media (prefers-color-scheme: dark) { :root { --color-bg: black; } }
   ```

3. **Hybrid**: default to system, allow override via class.

Always test:
- Contrast in both modes
- Initial render — prevent flash of wrong theme (FOUC) by setting class on `<html>` synchronously before React hydrates (Next.js: a small inline script in `<head>`)

## Modern CSS — the platform features worth knowing

These ship in evergreen browsers and let you delete React/JS in many cases. Most candidates still write 2018-era CSS while these newer features solve the same problems with less code.

### `:has()` — parent selector

```css
/* Card with featured badge → tinted background */
.card:has(.badge--featured) {
  background: hsl(173 80% 95%);
}

/* Form with any invalid field → show submit warning */
form:has(:user-invalid) .submit-warning {
  display: block;
}

/* Article with an image → adjust padding */
article:has(figure) {
  padding-block: 2rem;
}
```

Removes the need for state-driven className toggles in many cases.

### `:focus-within`

```css
.field:focus-within {
  outline: 2px solid var(--color-brand);
  outline-offset: 2px;
}

.field:focus-within .hint {
  opacity: 1;
}
```

Highlights a container when any descendant has focus — common for form fields, dropdowns, cards.

### `:user-valid` and `:user-invalid`

```css
input:user-invalid {
  border-color: var(--color-danger);
}
input:user-valid {
  border-color: var(--color-success);
}
```

Matches **after** the user has interacted. Unlike `:invalid`, which matches on blank required fields before the user even tries.

### `light-dark()` and `color-scheme`

```css
:root {
  color-scheme: light dark;
  --color-bg: light-dark(white, hsl(0 0% 7%));
  --color-fg: light-dark(hsl(0 0% 10%), hsl(0 0% 96%));
}
```

Theme switching without `@media (prefers-color-scheme)` blocks. `color-scheme` also tells the browser to use light/dark form controls + scrollbars.

### `color-mix()` — derive colors at the CSS layer

```css
:root {
  --color-brand: hsl(173 80% 40%);
  --color-brand-hover: color-mix(in oklch, var(--color-brand), black 10%);
  --color-brand-tint:  color-mix(in oklch, var(--color-brand), white 90%);
}
```

Define one brand color, derive hover/tint/shade without a build step. `in oklch` keeps the mix perceptually uniform.

### `@layer` — order cascade explicitly

```css
@layer reset, base, components, utilities;

@layer base {
  h1 { font-size: 2rem; }
}

@layer components {
  .card { padding: 1rem; }
}

@layer utilities {
  .text-center { text-align: center; }
}
```

Layers listed later win, regardless of specificity. Predictable cascade without specificity wars or `!important`.

### `@scope` — scope styles without naming hacks

```css
@scope (.card) {
  h2 { font-size: 1.5rem; }   /* only h2 inside .card */
}
```

CSS-Modules-like scoping without the build step. Chromium 118+, Safari/Firefox behind flag — keep as progressive enhancement.

### `text-wrap: balance` and `text-wrap: pretty`

```css
h1, h2, h3 { text-wrap: balance; }   /* even line lengths for headings */
p          { text-wrap: pretty; }     /* avoid widow words */
```

Tiny additions, huge typographic upgrade.

### `interpolate-size: allow-keywords`

```css
details {
  interpolate-size: allow-keywords;
}

details::details-content {
  block-size: 0;
  transition: block-size 0.3s ease;
}

details[open]::details-content {
  block-size: auto;
}
```

Finally enables smooth transition to/from `auto` — accordion open/close without JS measurement. Chromium 131+ only as of mid-2026.

### `scrollbar-gutter: stable`

```css
html {
  scrollbar-gutter: stable;
}
```

Reserves scrollbar space even when not visible. Prevents layout jumps when content height changes (e.g., modal opens → scrollbar disappears → page jumps).

### Anchor positioning (cross-reference)

For positioning popovers/tooltips relative to triggers without JS — see `react-html-platform` for the full pattern.

### Browser support cheat (mid-2026)

- `:has()` — universal
- `:focus-within` — universal
- `:user-valid` / `:user-invalid` — universal
- `light-dark()` — universal
- `color-mix()` — universal
- `@layer` — universal
- `@scope` — Chromium 118+, others behind flag
- `text-wrap: balance` — universal
- `text-wrap: pretty` — Chromium 117+, others catching up
- `interpolate-size: allow-keywords` — Chromium 131+ only
- `scrollbar-gutter` — universal
- Anchor positioning — Chromium 125+, others behind flag

For not-yet-universal features, fallback is usually "no animation" or "default positioning" — degrades gracefully.

## Common styling mistakes (interviewer-visible)

| Mistake | Fix |
|---|---|
| `style={{ color: '#3a3a3a' }}` | Use a token |
| `transform: scale(0.95)` on click but no transition | Add `transition: transform 150ms ease` |
| Hover-only states (no `focus-visible`) | Always pair hover with focus |
| `outline: none` without replacement | Use `:focus-visible { outline: 2px solid var(--color-brand); }` |
| Fixed `width: 320px` | Use `max-width: 320px; width: 100%` |
| `100vh` on mobile breaks (browser chrome) | Use `100dvh` or `100svh` |
| Animating `width` for a sliding menu | Animate `transform: translateX` |
| Setting `font-size: 14px` everywhere | Use a type scale, set base on `<html>` and rem elsewhere |
| `position: absolute` without `position: relative` parent | Always pair |
| Forgetting hover/focus/active/disabled | Run through all 4 states for every interactive |

## Narration phrases

- "I'm using CSS custom properties for tokens so theme switching is a single class toggle on `<html>` — no React re-render needed."
- "All animation is on `transform` and `opacity` — those run on the compositor and don't trigger layout."
- "I added `prefers-reduced-motion` because the hero animation isn't essential to the content."
- "I'm using container queries here because this card lives in both a 3-column grid and a sidebar — viewport breakpoints would lie."
- "The breakpoints are mobile-first; the only place I had to override down was the sticky nav at < 480px."
