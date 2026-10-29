---
name: uiux-pro-max
description: >
  Premium UI/UX design intelligence for building professional, production-grade interfaces. Use this skill whenever the user wants design system recommendations, color palette advice, typography pairings, style guidance, component library suggestions, or UI layout patterns — especially for SaaS, insurance, finance, e-commerce, or any industry-specific product. Trigger this skill when the user mentions building a landing page, dashboard, comparison page, lead gen form, or any web interface and wants it to look polished and professional. Also trigger when the user asks about design styles (glassmorphism, brutalism, minimalism, etc.), accessibility compliance (WCAG), or wants to avoid common design anti-patterns. Use even if the user just says "make this look good" or "what colors should I use" — this skill covers it all.
---

# UI/UX Pro Max — Premium Design Intelligence

Provides design system generation, style recommendations, component library guidance, and UI/UX best practices for building professional interfaces across all platforms and industries.

---

## Style Library (67 Styles — Select by Vibe)

| Category | Styles |
|---|---|
| **Modern** | Glassmorphism, Neumorphism, Claymorphism, Soft UI, Bento Grid |
| **Bold** | Brutalism, Neubrutalism, Memphis Design, Cyberpunk |
| **Refined** | Minimalism, Swiss Modernism, Editorial Grid, Accessible Design |
| **Trending** | AI-Native UI, Spatial UI, Liquid Glass, Aurora UI, Tactile Digital |

---

## Industry Design Rules

### Financial / Insurance Sites — Trust & Authority Pattern

**Page Structure (in order):**
1. Hero — clear value prop, above the fold
2. Trust indicators — ratings, certifications, licenses
3. Service comparison — transparent, no hidden pricing
4. Social proof — testimonials, reviews
5. Detail section — how it works, FAQ accordion
6. Strong CTA — above fold + repeated at bottom

**Style:** Soft UI Evolution + Accessible Design
- Clean, professional, calming
- Soft shadows, subtle depth
- WCAG AA minimum at all times

**Colors:**
- Primary: Navy `#1E3A8A`, Forest Green `#065F46`, Charcoal `#2D3748`
- Accent: Teal `#0D9488`, Blue `#3B82F6`, Sage `#10B981`
- Backgrounds: `#F9FAFB`, `#F3F4F6` (warm whites, light grays)
- ❌ Avoid: Bright reds, neons, flashy gradients

**Typography:**
- Headings: Inter, Poppins, Montserrat, DM Sans
- Body: Inter, Helvetica, Open Sans, Source Sans (≥16px mobile, ≥14px desktop)
- ❌ Avoid: Script fonts, playful fonts, condensed fonts

**Effects:**
- Transitions: 200–300ms smooth
- Hover: scale(1.02–1.05), no harsh drops
- Shadows: soft only
- Disclosure: accordions, tabs for dense info

---

## Anti-Patterns — NEVER Use These

### For Financial/Insurance:
- ❌ AI purple/pink gradients (kills trust)
- ❌ Bright neon colors (unprofessional)
- ❌ Dark mode as primary theme
- ❌ Playful/bouncy animations
- ❌ Comic Sans or novelty fonts
- ❌ Autoplay video
- ❌ Pop-ups before user engagement
- ❌ Stock photos of people pointing at laptops

### Universal Design Mistakes:
- ❌ Cluttered layouts
- ❌ Body text under 14px
- ❌ Low contrast text (WCAG fail)
- ❌ Forms without validation feedback
- ❌ No loading indicators
- ❌ Hidden pricing

---

## Component Library Recommendations

| Library | Best For |
|---|---|
| **shadcn/ui** (Tailwind + Radix) | Modern, accessible, customizable — default pick |
| **Headless UI** (Tailwind Labs) | Full brand control, excellent a11y |
| **Radix UI** (primitives) | Low-level, keyboard + screen reader tested |

### Animation Libraries:
- **Framer Motion** — smooth, professional (React)
- **GSAP** — complex scroll-based animations
- **Lenis** — smooth scroll
- **AutoAnimate** — automatic list/transition animations

---

## Pre-Delivery Checklist

### Accessibility (Critical)
- [ ] Text contrast ≥ 4.5:1 (WCAG AA)
- [ ] Visible focus states for keyboard nav
- [ ] All interactive elements have `cursor-pointer`
- [ ] Form fields have labels + error states
- [ ] Alt text on all images
- [ ] `prefers-reduced-motion` respected

### Performance
- [ ] CLS < 0.1 (no layout shift)
- [ ] INP < 200ms
- [ ] Animations at 60fps
- [ ] Images: WebP, lazy loaded

### Visual Polish
- [ ] 8px grid system for spacing
- [ ] Consistent typography hierarchy
- [ ] Smooth transitions (200–300ms)
- [ ] No harsh shadows
- [ ] Proper focus states

### Mobile
- [ ] Works at 320px minimum width
- [ ] Touch targets ≥ 44×44px
- [ ] Text ≥ 16px on mobile
- [ ] No horizontal scroll
- [ ] Load time < 3s

---

## Quick Reference Examples

### Insurance Comparison Page
```
Pattern: Trust & Authority
Style: Soft UI + Accessible Design
Colors: Navy #1E3A8A + Teal #0D9488
Type: Inter headings / Helvetica body
Effects: Soft shadows, gentle hover, 200ms transitions

Structure:
1. Hero (value prop)
2. Trust badges (BBB, licenses)
3. 3-card comparison grid
4. Testimonials carousel
5. FAQ accordion
6. CTA: "Get Quote Now"
```

### Financial Dashboard
```
Pattern: Data-First Dashboard
Style: Minimalism + Data Visualization
Colors: Charcoal #2D3748 + Blue accents #3B82F6
Type: DM Sans headings / Inter body
Libraries: Chart.js + shadcn/ui + Framer Motion
```

---

## Implementation Phases

| Phase | Focus |
|---|---|
| **Week 1** | Design system (colors, type, spacing) + core components |
| **Week 2** | Hero, trust indicators, comparison, testimonials |
| **Week 3** | Animations, micro-interactions, a11y audit, performance |
| **Ongoing** | Film grain, illustrations, progressive enhancements |

---

> **Core principle:** Solid fundamentals first. Premium polish added incrementally. Trust and clarity always beat flashy effects.
