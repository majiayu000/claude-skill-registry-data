---
name: modern
description: Current web standard — clean sans-serif typography, grid layouts, subtle shadows, and polished utility.
---
# Modern
## Mission
Deliver a polished, trustworthy web experience using familiar patterns: clear hierarchy, responsive grids, and tasteful depth.
## Brand
### 🎨 Colors
- `#2563EB` — Primary (blue-600)
- `#7C3AED` — Secondary (violet-600)
- `#10B981` — Accent (emerald-500)
- `#FFFFFF` — Background (white)
- `#111827` — Text (gray-900)
- `#6B7280` — Muted text (gray-500)
### 🔤 Typography
- Heading: **Plus Jakarta Sans** (Google Fonts) — modern geometric sans
- Body: **Inter** (Google Fonts) — workhorse sans-serif
- Scale: xs 0.75rem | sm 0.875rem | base 1rem | lg 1.125rem | xl 1.25rem | 2xl 1.5rem | 3xl 2rem
### 📐 Spacing
- Grid: 12-column responsive, 20px gutter, max-width 1280px container
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 1.5rem in auto-fit CSS Grid
### 🧩 Components
- Buttons: filled primary (8px radius), outline secondary, 0.5rem 1.5rem padding, 150ms transition on hover/active
- Cards: white background, 8px radius, subtle box-shadow (0 1px 3px rgba(0,0,0,0.1)), 1.5rem padding
- Nav: sticky top, white background, subtle bottom border, logo left + links center/right, hamburger at mobile
- Hero: 2-column grid (text left, illustration right), gradient accent blob behind headline
- Footer: 4-column link grid, muted background (#F9FAFB), subtle top border
### ♿ Accessibility
- Contrast minimum 4.5:1 for all text
- Focus states: 2px solid primary ring with 2px offset
- Respect `prefers-reduced-motion` — reduce transitions to instant
- Minimum body font size 16px (1rem)
### ✍️ Writing Tone
- Clear, helpful, confident. Active voice. Benefit-led but not hyperbolic.
- Labels use sentence case. CTAs start with verbs. One space after periods.
## Do / Don't
### ✅ Do
- Use a consistent 8px spacing scale throughout
- Apply subtle box-shadows for depth layers (sm, md, lg token scale)
- Limit max-width to 1280px with auto margins for content containment
- Use CSS Grid for card layouts with auto-fit and minmax
- Style all interactive states: hover, focus, active, disabled
### ❌ Don't
- Use more than 2 typefaces across the entire site
- Apply box-shadow blur values larger than 15px — subtle is modern
- Nest cards inside cards — one depth layer per component
- Use colored backgrounds for content areas — keep it white/off-white
- Add decorative elements that don't serve a function
## Quality Gates
- [ ] Responsive at 320px, 768px, 1024px, and 1440px widths
- [ ] All interactive elements have hover, focus, active, and disabled states
- [ ] Spacing follows an 8px scale — no value breaks the scale
- [ ] No more than 2 font families in use
- [ ] Max-width container (1280px) enforces content boundaries
- [ ] Color contrast passes WCAG AA (4.5:1) for all text