---
name: saas-landing
mode: prototype
preview: html
inputs:
  - name: companyName
    type: string
    label: Company Name
  - name: tagline
    type: string
    label: Tagline
  - name: primaryColor
    type: string
    label: Primary Color
parameters:
  - name: hue
    type: hue
    label: Accent Hue
  - name: density
    type: spacing
    label: Content Density
outputs:
  primary: index.html
---

# SaaS Landing Page Skill

Generate a modern, conversion-focused SaaS landing page.

## Rules
- Single-page layout with sticky navigation
- Hero section with gradient background (NO purple/cyan gradients)
- Feature grid with 3-4 features (NO 3-column equal cards)
- Social proof section with real company logos or placeholder blocks
- Pricing table with 3 tiers
- Footer with newsletter signup
- Use the provided company name and tagline
- Respect the primary color for accents (max 2 uses per screen)
- Inter font is FORBIDDEN. Use Geist, Satoshi, or Cabinet Grotesk

## Structure
1. Navigation (sticky, blur backdrop)
2. Hero (left text + right visual/metric)
3. Social proof (logo bar)
4. Features (alternating layout)
5. Testimonials (1 highlighted + grid)
6. Pricing (3 tiers, middle emphasized)
7. CTA banner
8. Footer

## Technical
- Single-file HTML with inline CSS
- Responsive: mobile-first breakpoints
- CSS custom properties for theming
- Smooth scroll behavior
