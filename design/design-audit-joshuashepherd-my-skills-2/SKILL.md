---
name: design-audit
description: Audit a page or component against the Digital Curator design spec (DESIGN.md) and movemental project conventions. Use to check visual quality, accessibility, token compliance, and consistency before shipping.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Audit the specified file(s) against movemental design quality standards.

Target: $ARGUMENTS

## Before Starting

1. Read `docs/design/DESIGN.md` — the canonical design spec ("The Digital Curator").
2. Read `src/app/globals.css` — token inventory (`@theme inline`, `:root`, `@layer base`).
3. Read `src/components/primitives/index.ts` — available primitive components.

## Audit Checklist

Read the target file(s) and evaluate across all dimensions:

### 1. PATTERN & LAYOUT
- [ ] Clear visual hierarchy (Eyebrow → Display → Prose → CTA)
- [ ] Uses primitives: `Section`, `Container`, `Display`, `Eyebrow`, `Prose`, `SurfaceCard`, `FeatureSplit`
- [ ] Consistent spacing using layout tokens (`--section-y-sm: 80px`, `--section-y-lg: 120px`, `--container-max: 1200px`)
- [ ] Responsive: works at mobile (375px), tablet (768px), desktop (1280px)
- [ ] No horizontal scroll on any breakpoint
- [ ] Content sections use `<Section variant=...>` for tonal stacking — never borders

### 2. TONAL STACKING (DESIGN.md §3.1)
- [ ] Sections alternate `variant="default"` / `variant="section"` / `variant="elevated"` / `variant="midnight"`
- [ ] **No 1px solid borders for sectioning** — depth comes from tonal shifts (bg-card on bg-section = Ghost Lift)
- [ ] Border allowed ONLY for form-field accessibility (`border-border`)
- [ ] **No decorative drop shadows** — use `shadow-ambient` or tonal stacking only
- [ ] SurfaceCard `tone` matches parent Section (`on-background`, `on-section`, `midnight`)

### 3. COLOR & TOKENS
- [ ] **NO hardcoded colors** (no `bg-blue-600`, no hex values, no rgb() outside globals.css)
- [ ] All colors use semantic tokens: `bg-background`, `bg-section`, `bg-card`, `bg-elevated`, `bg-inverse-surface`, `bg-primary`, `text-foreground`, `text-muted-foreground`, `text-inverse-foreground`, `text-primary`
- [ ] **No `bg-white`, `bg-black`, `text-white`, `text-black`** (use `bg-card`/`bg-inverse-surface`/`text-foreground`/`text-inverse-foreground`)
- [ ] `text-inverse-foreground` used inside `variant="midnight"` sections (not `text-white`)
- [ ] Primary (`#0053db`) used for actions and high-priority focus ONLY — not as large backgrounds
- [ ] **Never pure black** — use `text-foreground` (#2a3439) or `bg-inverse-surface` (#101820)
- [ ] WCAG AA contrast compliance (4.5:1 normal text, 3:1 large text)

### 4. TYPOGRAPHY (DESIGN.md §5)
- [ ] **Inter font only** — loaded via `next/font/google`
- [ ] Display headings get `tracking-[-0.02em]` (tight tracking)
- [ ] Eyebrow labels: uppercase, `tracking-[0.05em]`, `text-[0.75rem]`
- [ ] Body text minimum 16px on mobile
- [ ] Line length capped at `--prose-max: 680px` for readability
- [ ] No orphaned headings (heading always followed by content)
- [ ] No more than 5 font size variations in a single view

### 5. COMPONENT USAGE
- [ ] Uses shadcn/ui primitives (Button, Card, Input) — not raw HTML with custom styles
- [ ] **Never hand-edit `src/components/ui/*`** — extend via primitives or token overrides
- [ ] Uses `<Button>` from shadcn, not raw `<button>` for styled buttons
- [ ] Uses `next/image` for all images with explicit `width`/`height` or `fill`
- [ ] Icons from `lucide-react` with `aria-hidden` for decorative icons

### 6. SERVER COMPONENTS & NEXT.JS
- [ ] **No `"use client"` in layout.tsx or page.tsx** — push to leaf components
- [ ] Data fetching in server components or via hooks — not mixed
- [ ] Middleware is `proxy.ts` at repo root (not `middleware.ts`)
- [ ] Params via props in server components, `useParams()` only in client leaves

### 7. ACCESSIBILITY
- [ ] All images have meaningful alt text
- [ ] No color-only information conveyance
- [ ] Keyboard navigation works (no traps)
- [ ] Tap targets are minimum 44x44px
- [ ] ARIA labels on icon-only buttons
- [ ] Heading order is sequential (h1 → h2 → h3)

## Output Format

```
## Design Audit: [filename]

### Score: X/7 dimensions passing

### Issues Found
1. [DIMENSION] — [severity: CRITICAL/HIGH/MEDIUM/LOW] — description — file:line
   Fix: specific suggestion

### Passing
- [DIMENSION] — what's working well
```

## Rules

- This is a **light-primary** site. There is NO global dark mode. Midnight sections are regional via `<Section variant="midnight">`.
- Always reference DESIGN.md as the authority for any design decisions.
- The Stitch project `2208910962065880866` is the visual source of truth — components should trace back to it.
- Present the full audit report before recommending any changes.
