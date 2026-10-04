---
name: templateclaw-landing
description: "Generate a modern landing page with 2026 design trends. Supports SaaS, portfolio, product, startup, and app styles. Includes glassmorphism, gradient animations, responsive layout, and dark mode."
allowed-tools: Read, Write, Edit
argument-hint: "[style: saas|portfolio|product|startup|app]"
---

# TemplateClaw — Landing Page Generator

Generate a production-ready landing page with cutting-edge 2026 design.

## When Invoked

1. If argument provided (e.g., `/templateclaw-landing saas`), generate that style directly
2. If no argument, ask: "What type of landing page? (saas / portfolio / product / startup / app)"

## Landing Page Styles

### SaaS Landing Page
- Hero with gradient mesh background + animated orbs
- Feature grid (3 columns) with glassmorphism cards
- Pricing table (3 tiers) with popular tier highlighted
- Social proof section (logos + testimonials)
- CTA sections with gradient buttons
- FAQ accordion

### Portfolio Landing Page
- Full-screen hero with name + title + animated gradient text
- Project showcase grid with hover overlays
- Skills section with animated progress bars
- Experience timeline
- Contact form with glassmorphism style

### Product Launch Landing Page
- Product hero with 3D-style mockup placeholder
- Feature highlights with icons
- How-it-works steps (numbered)
- Testimonials carousel
- Early access signup form

### Startup Pitch Landing Page
- Bold statement hero with counter animations
- Problem → Solution narrative sections
- Team grid
- Investor logos / backed-by section
- Waitlist CTA

### Mobile App Landing Page
- Phone mockup hero (CSS-only device frame)
- App screenshots carousel
- Feature list with device-specific icons
- Download badges (App Store / Play Store)
- Reviews section

## Design System (All Styles)

```css
/* Colors */
--bg-primary: #0A0E1A;
--bg-card: rgba(255,255,255,0.05);
--accent-violet: #7C3AED;
--accent-pink: #EC4899;
--accent-blue: #3B82F6;
--text-primary: #F8FAFC;
--text-secondary: #94A3B8;

/* Effects */
backdrop-filter: blur(20px);
border: 1px solid rgba(255,255,255,0.1);
background: linear-gradient(135deg, var(--accent-violet), var(--accent-pink));

/* Typography */
font-family: 'Inter', system-ui, sans-serif;
code: 'JetBrains Mono', monospace;
```

## Output Requirements

- Single HTML file with embedded CSS and JS
- Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`)
- Google Fonts (Inter + JetBrains Mono) via CDN
- Fully responsive (mobile-first breakpoints: sm, md, lg, xl)
- Dark mode by default, optional light toggle
- Smooth scroll behavior
- Intersection Observer for scroll animations
- All images use placeholder gradients (no external images)
- Accessible: semantic HTML, ARIA labels, focus states
- Under 500 lines for single page, well-commented

## Customization Points

Mark these with HTML comments for easy customization:
```html
<!-- CUSTOMIZE: Brand name -->
<!-- CUSTOMIZE: Hero headline -->
<!-- CUSTOMIZE: Feature list -->
<!-- CUSTOMIZE: Pricing tiers -->
<!-- CUSTOMIZE: Contact info -->
```
