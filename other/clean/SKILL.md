---
name: clean
description: Minimal white space, airy grid-based layouts with zero decoration.
---
# Clean
## Mission
Disappear completely — let content stand alone through generous white space, rigorous grid alignment, and the total absence of decorative elements.
## Brand
### 🎨 Colors
- `#ffffff` — White background
- `#f8f9fa` — Subtle gray surface
- `#212529` — Text primary (near-black)
- `#6c757d` — Text secondary (gray)
- `#0d6efd` — Accent blue (sparing use)
- `#dee2e6` — Subtle border
### 🔤 Typography
- Headings: Inter (Google Fonts)
- Body: Inter (Google Fonts)
- Scale: xs 0.75rem, sm 0.875rem, base 1rem, lg 1.125rem, xl 1.5rem, 2xl 2rem, 3xl 2.5rem
### 📐 Spacing
- Grid: 12-column, 24px gutters, max-width 1200px centered
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 1.5rem
### 🧩 Components
- Buttons: Clean — 6px radius, solid fill for primary, 1px border for secondary, 12px-20px horizontal padding, 44px height
- Cards: 8px radius, white fill, 1px `#dee2e6` border, 24px internal padding, hover adds subtle 2px shadow
- Nav: Simple — white background, logo left, links right, 1px bottom border, 64px height
- Hero: Centered, generous padding (100px+ vertical), large headline, supportive subhead, one CTA, optional clean illustration
- Footer: Light gray `#f8f9fa`, clean column layout, small text, no decoration
### ♿ Accessibility
- Minimum contrast ratio 4.5:1 for all body text
- Focus states: 2px blue ring with 2px offset on all interactive elements
- Reduced motion: Instant transitions, no hover animations
- Minimum font size 0.75rem (12px), recommended 1rem for body
### ✍️ Writing Tone
- Voice: Clear, direct, helpful — like good documentation
- Labels: Sentence case, action-oriented
- No marketing hyperbole; let the product speak for itself
## Do / Don't
### ✅ Do
- Use white space as the primary layout tool — more space, not more borders
- Keep the color palette to grayscale plus one accent color
- Align everything to the 12-column grid with consistent 24px gutters
- Use a single font family with weight variations for hierarchy
- Remove elements until nothing further can be removed without breaking function
### ❌ Don't
- Add decorative elements — icons, dividers, gradients, illustrations, patterns
- Use more than 1 accent color anywhere on a page
- Overlap elements — everything sits in its own grid cell
- Use shadows darker than `rgba(0,0,0,0.06)`
- Add animation beyond subtle opacity fades (200ms max)
## Quality Gates
- [ ] All elements align to the 12-column grid
- [ ] No decorative elements present — every pixel serves function
- [ ] Only 1 accent color in use on any page
- [ ] Body text is minimum 1rem on all viewports
- [ ] Focus states visible on all interactive elements
- [ ] Page works with CSS grid disabled (content order is logical)