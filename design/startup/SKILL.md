---
name: startup
description: Fresh gradient-heavy startup aesthetic — bold hero, modern sans, investor-pitch energy, built to convert.
---
# Startup
## Mission
Sell the vision before the product. Bold gradients, confident typography, high-contrast hero sections, and the kinetic energy of a pitch deck — every pixel should say "this is going to be huge."
## Brand
### 🎨 Colors
- `#7C3AED` — Vibrant purple (primary gradient start)
- `#3B82F6` — Electric blue (primary gradient end)
- `#F97316` — Energetic orange (accent)
- `#0F172A` — Dark slate (text)
- `#FFFFFF` — White (background)
- `#F8FAFC` — Light gray surface
### 🔤 Typography
- Heading font: DM Sans (Google Fonts)
- Body font: DM Sans (Google Fonts)
- Type scale: `0.75rem` / `0.875rem` / `1rem` / `1.125rem` / `1.25rem` / `1.75rem` / `3rem`
### 📐 Spacing
- Grid system: 12-column CSS Grid, `1.5rem` gutter, `max-width: 1200px`
- Section padding: `6rem` vertical, `2rem` horizontal
- Card gaps: `1.5rem`
### 🧩 Components
- Buttons: Large (`1rem` padding), bold gradient fill (purple→blue), `0.5rem` border-radius, `font-weight: 600`, hover glow
- Cards: White with subtle border, `0.75rem` radius, bold stat numbers, gradient accent bar on top edge
- Nav: Sticky, white/transparent, logo left, "Get Early Access" CTA right, smooth background transition on scroll
- Hero: Full-viewport gradient background (animated purple→blue→orange shift), massive h1, rotating value-prop carousel, social proof below
- Footer: Dark slate background, 4-column link grid, gradient newsletter signup bar, "Made with 🚀"
### ♿ Accessibility
- Contrast: `#0F172A` on white = 15.5:1 (AAA); gradient button text must be white on dark enough gradient midpoint
- Focus states: `3px` gradient ring (purple→blue) with `2px` offset
- Reduced motion: disable gradient animation, hover lifts, and carousel rotation
- Font size minimums: `1rem` for body, `3rem` mobile hero heading minimum
### ✍️ Writing Tone
- Bold, ambitious, urgent but not desperate — "the future doesn't wait"
- Use social proof language: "Join 10,000+ teams," "Backed by YC," "As seen in"
- Labels: "Get Early Access," "Join the Waitlist," "See the Demo," "Start Building"
## Do / Don't
### ✅ Do
- Lead with a bold gradient hero — purple-to-blue is the startup standard
- Include social proof above the fold (investor logos, user count, press mentions)
- Use large stat numbers (72px+) in cards to sell traction
- Add a waitlist or early-access CTA as the primary conversion goal
- Animate the hero gradient subtly — it signals "alive and moving fast"
### ❌ Don't
- Use muted or pastel colors — startup is high-energy, high-saturation
- Hide the product — show a screenshot, mockup, or demo video above the fold
- Write passive or modest copy — "We're building..." → "The fastest way to..."
- Overuse orange — it's the accent, not the primary; one orange element per viewport
- Let the gradient overwhelm text — always check contrast at gradient midpoints
## Quality Gates
- [ ] Hero CTA button text passes 4.5:1 contrast at the gradient midpoint
- [ ] Gradient animation respects `prefers-reduced-motion: reduce`
- [ ] Social proof (logos/stats) visible without scrolling on desktop
- [ ] Page loads under 2.5s on 3G (gradients can be heavy — optimize)
- [ ] Responsive: hero text scales down to `2rem` minimum on mobile
- [ ] All links and buttons have visible focus indicators