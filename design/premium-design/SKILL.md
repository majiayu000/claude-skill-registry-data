---
name: premium-design
description: Enforces anti-AI-slop design system for all UI work
---

# Premium Design System — RJ Business Solutions

## Before Writing ANY UI Code:
1. Define the design direction (editorial, brutalist, neo-corporate, etc.)
2. Select font pairing from approved list (NEVER Inter/Roboto/Arial)
3. Define color palette with CSS variables (light + dark mode)
4. Plan layout with asymmetric grid compositions
5. Select icon strategy (Phosphor primary, Lucide secondary)

## Typography Rules:
- Headings: Clash Display, Cabinet Grotesk, or Satoshi (via next/font)
- Body: Plus Jakarta Sans, General Sans, or Space Grotesk (via next/font)
- Data/Code: JetBrains Mono or Space Mono (via next/font)
- NEVER use system fonts as primary display fonts

## Color Rules:
- Define 5-color palette minimum with semantic names
- Use CSS custom properties: --color-primary, --color-accent, etc.
- WCAG AA contrast ratios mandatory (≥4.5:1 body, ≥3:1 large)
- Dark mode: NEVER just invert. Design intentionally.

## Animation Rules (Framer Motion 12+):
- Page transitions: smooth, purposeful (200-400ms)
- Scroll-triggered reveals: staggeredChildren with delayChildren
- Hover states: scale(1.02-1.05), shadow elevation, color shift
- Loading: skeleton screens with shimmer, NEVER empty white space
- CLS < 0.1. Animations at ≥60fps.

## Component Quality Checklist:
- [ ] Loading state (skeleton with shimmer)
- [ ] Error state (branded, helpful message, retry button)
- [ ] Empty state (illustration, CTA to populate)
- [ ] Populated state (real data, not placeholder)
- [ ] Hover/focus/active states
- [ ] Mobile responsive (375px minimum)
- [ ] Keyboard accessible
- [ ] Screen reader friendly (aria-labels)

## Image Rules:
- ALWAYS next/image (NEVER raw <img>)
- Real photos from Unsplash/Pexels (NEVER placeholder.com)
- blurDataURL for loading placeholders
- Proper width/height/alt on every image
- WebP format preferred
