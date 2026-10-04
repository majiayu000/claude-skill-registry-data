---
name: advanced-responsive-patterns
description: Systematic responsive implementation with 5 breakpoints, container queries, fluid spacing, responsive component patterns, and touch targets. Use when building layouts that must work across all devices.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# Advanced Responsive Patterns

## Purpose
Replace "test at 375px and 1280px" with a comprehensive responsive system. Every pattern includes exact breakpoint values, Tailwind prefixes, and implementation code.

## When to Use This Skill
Use when:
- Building any layout that must work on mobile, tablet, and desktop
- Implementing responsive navigation, grids, or typography
- Testing responsive behavior across breakpoints

Do NOT use when:
- The layout is non-responsive or trivial.

## Phase 1: Responsive Layout Strategy
## 1. Breakpoint System

Use Tailwind's mobile-first breakpoints: base (375px), `md:` (768px), `lg:` (1024px), `xl:` (1280px), `2xl:` (1536px).

**RULE**: Never write `max-width` media queries. Always build mobile-first with `min-width` breakpoints.

---

## 2. Container Queries

For components that adapt to their container width, not the viewport.

```css
/* Parent declares itself as a container */
.card-grid {
  container-type: inline-size;
  container-name: card-grid;
}

/* Children respond to container width */
@container card-grid (min-width: 600px) {
  .card { flex-direction: row; }
}

@container card-grid (min-width: 900px) {
  .card-grid-inner { grid-template-columns: repeat(3, 1fr); }
}
```

Tailwind v3.4+ equivalent:
```html
<div class="@container">
  <div class="flex flex-col @md:flex-row @lg:grid @lg:grid-cols-3">
    ...
  </div>
</div>
```

**Use container queries when**: A component is used in multiple layout contexts (sidebar vs main content vs modal) and needs to adapt to available space, not viewport width.

---

## 3. Fluid Spacing

### clamp() for Smooth Scaling
```css
/* Margin/padding that scales smoothly between breakpoints */
.section {
  padding-block: clamp(2rem, 5vw, 6rem);    /* 32px → 96px smoothly */
  padding-inline: clamp(1rem, 3vw, 3rem);   /* 16px → 48px smoothly */
}

/* Section gaps */
.section-gap {
  margin-top: clamp(3rem, 8vw, 8rem);       /* 48px → 128px */
}

/* Hero headline */
.hero-title {
  font-size: clamp(2rem, 5vw + 1rem, 4.5rem); /* 32px → 72px */
}
```

### Fluid Spacing Scale
| Token | Min (mobile) | Preferred | Max (desktop) |
|-------|-------------|-----------|---------------|
| `--space-sm` | 0.5rem | 1vw | 1rem |
| `--space-md` | 1rem | 2vw | 2rem |
| `--space-lg` | 2rem | 5vw | 4rem |
| `--space-xl` | 3rem | 8vw | 6rem |
| `--space-2xl` | 4rem | 10vw | 8rem |

---

## 4. Responsive Component Patterns

### Table: Card View on Mobile

The most non-obvious responsive pattern. Standard grids and flex stacked→row are trivially known.

```tsx
// Desktop: standard table
// Mobile: card stack

export function ResponsiveTable({ data }: { data: Row[] }) {
  return (
    <>
      {/* Desktop table */}
      <table className="hidden md:table w-full">
        <thead>
          <tr>
            <th className="text-left">Name</th>
            <th className="text-right">Amount</th>
            <th className="text-left">Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id}>
              <td>{row.name}</td>
              <td className="text-right font-mono tabular-nums">{row.amount}</td>
              <td>{row.status}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Mobile card stack */}
      <div className="md:hidden space-y-3">
        {data.map((row) => (
          <div key={row.id} className="p-4 rounded-lg border border-zinc-200">
            <div className="font-medium">{row.name}</div>
            <div className="text-sm text-zinc-500 mt-1">{row.status}</div>
            <div className="font-mono tabular-nums mt-2">{row.amount}</div>
          </div>
        ))}
      </div>
    </>
  );
}
```

---

## 5. Touch Targets

| Element | Minimum Size | Recommended |
|---------|-------------|-------------|
| Buttons | 44 × 44px | 48 × 48px |
| Links (inline text) | 44px height (via padding) | — |
| Icon buttons | 44 × 44px | 48 × 48px |
| Form inputs | 44px height | 48px height |
| Spacing between targets | 8px | 12px |

```html
<!-- Even small icons need large touch targets -->
<button class="p-3 -m-3" aria-label="Close">
  <svg class="w-4 h-4">...</svg>
</button>
<!-- p-3 = 12px padding on each side → icon is 16px + 24px padding = 40px
     -m-3 = negative margin prevents the padding from pushing layout -->
```

---

## 6. Responsive Typography

```css
/* Fluid heading scale */
h1 { font-size: clamp(2rem, 5vw + 0.5rem, 4rem); }
h2 { font-size: clamp(1.5rem, 3vw + 0.5rem, 2.5rem); }
h3 { font-size: clamp(1.25rem, 2vw + 0.5rem, 1.75rem); }

/* Body text: FIXED, not fluid */
body { font-size: 1rem; }  /* 16px always */

/* Reading width constraint */
.prose { max-width: 65ch; }
```

**RULE**: Body text and UI text use fixed `rem` sizes. Only display headings use fluid `clamp()` values. Fluid body text is disorienting and breaks accessibility zoom.

---

## 7. Breakpoint Testing Checklist

| Breakpoint | Width | Test |
|-----------|-------|------|
| Small mobile | 375px | All content visible? No horizontal overflow? Touch targets ≥ 44px? |
| Large mobile | 428px | Same checks. Text doesn't feel cramped? |
| Tablet portrait | 768px | Grid transitions correct? Nav switches from hamburger? |
| Tablet landscape | 1024px | Split layouts activate? Sidebar visible (if app)? |
| Desktop | 1280px | Full layout. Max-width containers prevent ultra-wide stretching? |
| Ultra-wide | 1920px | Content centered with max-width? No empty side gutters > 200px? |

### How to Test in Chrome DevTools
1. Open DevTools → Toggle Device Toolbar (Ctrl+Shift+M)
2. Set responsive viewport
3. Test at each width in the table above
4. Check: no horizontal scroll, no text overflow, no overlapping elements
5. Use "Throttling: Mid-tier mobile" to test performance at each size

## Output Format / Delivery
- Mobile-first responsive CSS and components.
- Verified breakpoint layouts and touch-target sizes.

## Behavior Rules
- Always build mobile-first; do not write max-width overrides.
- Ensure all touch targets are at least 44x44px.

## Maintenance Notes
- Updated to match structural guidelines in June 2026.
