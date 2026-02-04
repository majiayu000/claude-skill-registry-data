---
name: frontend-style-guide
description: Enforce Cookmate frontend style. Use for any UI/UX work to keep brand colors/typography, AppShell patterns, and professional interaction states. Covers desktop + mobile.
---
# Cookmate Frontend Style Guide (pragmatic)

Use this whenever you add/change UI. Keep it concise; prefer existing patterns.

## Brand essentials
- Palette (from BRANDING.md): bg #F8F1E9, surface #FFFFFF, primary #C6502B, secondary #5F7A57, accent #F0B04C, text #221B16, text-muted #6E6258, border #E6D7C7, focus #F0B04C.
- States: primary hover #B54827, pressed #9E3F23; secondary hover #526B4C, pressed #485E43; accent hover #DFA347, pressed #C99341.
- Status: success #5F7A57, warning #F0B04C, danger #C6502B.
- Typography: headings Barlow Semi Condensed; body UI Barlow. Desktop scale: Display 40/48, H1 32/40, H2 24/32, H3 20/28, body 16/24, label/meta 12-14/16-20. Mobile: drop one step (e.g., H1 ~28/36, body ~15/22). Use font-display where present.

## Layout patterns
- Wrap pages in `AppShell` (Topbar desktop, BottomNav mobile) and keep radial accent background already in AppShell.
- Navigation: use `navigation.ts` helpers (`isNavActive`, `useSelectedLayoutSegments`, ignore `(group)` segments).
- Spacing: keep sections within max-w ~6xl and horizontal padding (`px-4`, `py-10` seen in Recipes).
- Cards: rounded-3xl, border border/70, bg-card/95, shadow-sm (see RecipesView empty/loading states).

## Components & interactions
- Buttons: shadcn (Tailwind) variants; primary uses accent/primary colors; hover/pressed per palette; keep rounded-xl/2xl consistent with Topbar/BottomNav.
- Inputs/forms: shadcn inputs/selects; respect focus ring `focus-visible:ring-[accent]`, border color #E6D7C7, text #221B16.
- Empty/error/loading states: concise copy, muted foreground, reuse Card pattern.
- Mobile: BottomNav present; avoid fixed elements clashing with safe-area; add bottom padding `pb-[calc(4rem+env(safe-area-inset-bottom))]` when needed.

## Tone & content
- Copy: clear, concise, avoid “AI slop”; use sentence case; summaries and labels match nav items (Recipes, Planner, Groceries, Discover).
- Icons: Lucide set already used; align sizes (h-4/5/6) with nav patterns.

## UI guardrails
- Icons: no emojis; use Lucide/Heroicons; correct logos (Simple Icons); consistent sizing (24px viewBox, h-4/5/6).
- Hover/focus: always visible feedback; transitions 150-300ms; no layout shift; `cursor-pointer` on interactive elements; focus rings keyboard-friendly.
- Contrast: light mode primary; text contrast ≥ 4.5:1; borders visible; glass elements opaque enough in light.
- Layout: fixed navs must not cover content; account for Topbar/BottomNav padding; avoid horizontal scroll; test 320/768/1024/1440.
- Motion: respect `prefers-reduced-motion`; limit decorative animations; use transform/opacity.

## Pre-delivery checklist
- [ ] Uses AppShell/nav patterns; spacing consistent (max-w, px-4, py-10).
- [ ] Colors/typography match brand; shadcn/Tailwind tokens used.
- [ ] Icons from Lucide/Heroicons; no emojis; hover/focus visible; cursor-pointer set.
- [ ] Responsive at 320/768/1024/1440; no overlap with Topbar/BottomNav; no horizontal scroll.
- [ ] Accessibility: alt text, labels, focus ring, color not sole indicator, respects reduced motion.
- [ ] Loading/empty/error states present; no silent failures.

## References
- data/stack-nextjs.csv: Next.js UI guardrails and patterns.
- data/ux-guidelines.csv: general UX checklist.
- data/tailwind.csv: Tailwind/shadcn best practices (spacing, responsive, a11y).

## How to apply
1) Start with `AppShell` + page section spacing.
2) Use existing cards/buttons patterns and colors above; avoid inventing new styles unless necessary.
3) Check responsiveness: desktop Topbar + mobile BottomNav; grid/cards collapse gracefully.
4) Keep code lean: reuse utilities (`cn`), existing primitives in `shared/ui`.
