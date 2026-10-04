---
name: saas
description: Modern SaaS aesthetic — blue/indigo, clean cards, dashboard-ready, built for trust and conversion.
---
# SaaS
## Mission
Build trust at a glance. Clean layouts, professional blue-indigo palette, and card-based organization that makes complex products feel simple and reliable.
## Brand
### 🎨 Colors
- `#2563EB` — Blue (primary)
- `#4338CA` — Indigo (secondary)
- `#F8FAFC` — Light background
- `#FFFFFF` — Card surface
- `#10B981` — Success green (accent)
- `#0F172A` — Dark text
### 🔤 Typography
- Heading font: Inter (Google Fonts)
- Body font: Inter (Google Fonts)
- Type scale: `0.75rem` / `0.875rem` / `1rem` / `1.125rem` / `1.25rem` / `1.5rem` / `2.25rem`
### 📐 Spacing
- Grid system: 12-column CSS Grid, `1.5rem` gutter
- Section padding: `6rem` vertical, `2rem` horizontal (max-width `1280px` centered)
- Card gaps: `1.5rem`
### 🧩 Components
- Buttons: Rounded (`0.375rem`), blue fill for primary, indigo outline for secondary, `font-weight: 500`
- Cards: White with `1px` subtle border (`#E2E8F0`), `0.5rem` border-radius, `box-shadow` on hover
- Nav: Sticky, white background with bottom border, logo left, links center/right, "Sign In" + "Get Started" CTAs
- Hero: Centered h1 + subheadline + CTA button + dashboard/product screenshot with subtle shadow
- Footer: 4-column link grid on light gray (`#F1F5F9`) background, copyright bar
### ♿ Accessibility
- Contrast: `#0F172A` on white = 15.5:1 (AAA); blue links on white = 5.9:1 (AA)
- Focus states: `2px` blue ring with `2px` offset, never remove outline
- Reduced motion: disable hover lifts and carousel animations
- Font size minimums: `0.875rem` for body, `1rem` for inputs
### ✍️ Writing Tone
- Clear, confident, benefit-driven — not hype
- Second person ("You'll get..."), active voice
- Labels: "Get Started," "View Pricing," "Start Free Trial," "Book a Demo"
## Do / Don't
### ✅ Do
- Center content with `max-width: 1280px` and auto margins
- Use generous whitespace — breathing room signals quality
- Add a subtle gradient to the hero background (white to `#F1F5F9`)
- Include trust signals: logos row, testimonial cards, case study stats
- Progressive disclosure — show the simple version first, details on click
### ❌ Don't
- Use more than two accent colors beyond blue/indigo
- Overcrowd cards — max 3 pieces of information per card
- Use hover effects that shift layout — stick to shadow/color transitions
- Hide pricing — SaaS must show pricing above the fold or one scroll away
- Let the dashboard screenshot look fake — use real data or realistic placeholders
## Quality Gates
- [ ] Page loads under 2s on 3G (Lighthouse performance score ≥ 90)
- [ ] Hero CTA passes 4.5:1 contrast; all text passes AA minimum
- [ ] Responsive: cards collapse from 3-up to 2-up to 1-up cleanly
- [ ] Keyboard navigation works through nav, cards, and footer links
- [ ] No layout shift during font load (`font-display: swap` + size-adjust)
- [ ] Trust signals (logos, testimonials, stats) are visible without scrolling