---
name: responsive-audit
description: Audit and fix responsiveness issues for movemental — breakpoint coverage, layout collapse, touch targets, typography scaling, overflow, and navigation. Enforces mobile-first design for Next.js 16 + Tailwind v4.
disable-model-invocation: true
---

Audit and fix responsiveness across the specified section or page(s).

Target: $ARGUMENTS

If no target is provided, audit the homepage and its constituent sections.

## Before Starting

1. Read `docs/design/DESIGN.md` — layout tokens: `--container-max: 1200px`, `--prose-max: 680px`, `--section-y-sm: 80px`, `--section-y-lg: 120px`. Breathing Layout rule.
2. Read `src/app/globals.css` — verify layout tokens exist.
3. Read `src/components/primitives/container.tsx` — Container responsive padding.
4. Read `src/components/primitives/section.tsx` — Section spacing tokens.

## Breakpoints

Movemental uses Tailwind's mobile-first breakpoints:
- **Mobile:** 0-639px (default styles)
- **sm:** 640px+
- **md:** 768px+
- **lg:** 1024px+
- **xl:** 1280px+

## Audit Checklist

### 1. LAYOUT INTEGRITY
- [ ] No horizontal overflow at any breakpoint (check for `overflow-x` issues)
- [ ] `Container` component used consistently (`max-w-[var(--container-max)]` + responsive padding)
- [ ] Grid layouts collapse gracefully: `sm:grid-cols-2`, `lg:grid-cols-3`, etc.
- [ ] No fixed widths that break below `375px` mobile
- [ ] `FeatureSplit` stacks at `<lg` breakpoint
- [ ] Images scale properly with `fill` + responsive `sizes` attribute

### 2. TYPOGRAPHY SCALING
- [ ] Body text minimum 16px at all breakpoints
- [ ] Display headings use responsive fluid sizing (via `clamp()` or breakpoint variants)
- [ ] Line length capped at `--prose-max` (680px) for readability
- [ ] No text truncation that hides meaningful content

### 3. TOUCH & INTERACTION
- [ ] All tap targets minimum 44x44px on mobile
- [ ] Buttons have adequate padding (at least `py-3 px-6` on mobile)
- [ ] Links have sufficient spacing to avoid mis-taps
- [ ] Navigation accessible on mobile (hamburger menu, sheet/drawer)

### 4. SECTION SPACING
- [ ] `Section` component uses `spacing="sm"` (80px) or `spacing="lg"` (120px)
- [ ] No sections with custom padding that breaks the rhythm
- [ ] Hero sections have adequate top padding accounting for fixed nav (`pt-[calc(4rem+...)]`)

### 5. IMAGES & MEDIA
- [ ] All images use `next/image` with `fill` or explicit responsive dimensions
- [ ] `sizes` attribute is meaningful (not just `100vw` on all images)
- [ ] Aspect ratios maintained across breakpoints
- [ ] No images that stretch or crop unattractively at different widths

### 6. NAVIGATION
- [ ] Desktop nav works at `md+` with proper link spacing
- [ ] Mobile nav activates below `md` with hamburger trigger
- [ ] Fixed nav doesn't overlap content
- [ ] Footer responsive layout (stacks on mobile, grid on desktop)

## Output Format

```
## Responsive Audit: [target]

### Breakpoint Pass/Fail Matrix
| Component | 375px | 640px | 768px | 1024px | 1280px |
|-----------|-------|-------|-------|--------|--------|

### Issues Found
1. [SEVERITY] — [breakpoint] — description — file:line
   Fix: specific Tailwind change

### Fixes Applied
- file.tsx:line — [before] → [after]
```

## Rules

- Test at all 5 breakpoints minimum: 375px, 640px, 768px, 1024px, 1280px.
- Mobile-first: ensure default (no prefix) styles work at 375px. Add `sm:`, `md:`, `lg:` for wider.
- If Chrome DevTools MCP is available, take screenshots at each breakpoint for visual verification.
- The `Container` primitive handles responsive padding — don't add custom `px-*` around it.
- Breathing Layout rule (DESIGN.md): if a component feels crowded, increase padding — never shrink type to fit.
