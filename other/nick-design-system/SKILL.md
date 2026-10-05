---
name: nick-design-system
description: Nick's enterprise design system. Enforces his visual standards on every web project — typography, color, layout, spacing, components, and anti-patterns. Must be referenced before any build spec is written. Produces "Enterprise Confidence with Clean Authority" — never generic AI design.
metadata:
  openclaw:
    requires: {}
---

# Nick's Design System — "Enterprise Confidence with Clean Authority"

## When to Use
Before writing ANY build spec for a web project, read this entire file and incorporate every applicable section into the Claude Code prompt. No exceptions.

## Design Philosophy
The design should feel like it belongs at the top of its industry. Not because it's flashy — because it's structured, intentional, and unapologetically polished. The design doesn't try hard. It just is.

Every element earns its place. Nothing decorative without purpose. Nothing trendy that ages in six months. Clean lines, strong brand presence, architecture that rewards exploration.

Reference sites: Accenture, Atlassian, Adobe, NVIDIA, Rocket Companies.

---

## Typography

### Font Stack
- **Primary:** Inter (headings + body) — clean, modern, enterprise-grade sans-serif
- **Alternate:** Plus Jakarta Sans or DM Sans for projects needing warmer personality
- **Monospace:** JetBrains Mono (code blocks, data displays)
- Always load via Google Fonts or next/font for performance

### Scale (Desktop)
| Element | Size | Weight | Line Height | Letter Spacing |
|---------|------|--------|-------------|----------------|
| Display/Hero | 56–72px (3.5–4.5rem) | 700–800 | 1.05–1.1 | -0.02em |
| H1 | 48px (3rem) | 700 | 1.1 | -0.02em |
| H2 | 36px (2.25rem) | 600–700 | 1.15 | -0.01em |
| H3 | 28px (1.75rem) | 600 | 1.2 | -0.01em |
| H4 | 22px (1.375rem) | 600 | 1.3 | 0 |
| Body Large | 18px (1.125rem) | 400 | 1.6 | 0 |
| Body | 16px (1rem) | 400 | 1.6 | 0 |
| Body Small | 14px (0.875rem) | 400 | 1.5 | 0 |
| Caption/Label | 12px (0.75rem) | 500 | 1.4 | 0.02em |

### Scale (Mobile)
- Hero: 36–44px
- H1: 32px
- H2: 26px
- H3: 22px
- Body: 16px (never smaller)

### Rules
- Headlines are LARGE and DECLARATIVE — short statements that hit, not paragraphs
- Headlines should read like mission statements: tell what you ARE, not what you sell
- Examples of good headlines: "Let There Be Change", "Help Everyone Home", "World Leader in AI Computing"
- Max 8–12 words per hero headline
- Subheadlines: 1–2 sentences max, Body Large size, lighter weight (400)
- Never use more than 2 font families per project

---

## Color System

### Palette Architecture
Every project gets a branded palette. No random colors. Each color earns its spot.

#### Neutral Foundation
```
--gray-50:  #FAFAFA    /* Page backgrounds */
--gray-100: #F5F5F5    /* Section alternates */
--gray-200: #E5E5E5    /* Borders, dividers */
--gray-300: #D4D4D4    /* Disabled states */
--gray-400: #A3A3A3    /* Placeholder text */
--gray-500: #737373    /* Secondary text */
--gray-600: #525252    /* Body text (light bg) */
--gray-700: #404040    /* Strong body text */
--gray-800: #262626    /* Headlines (light bg) */
--gray-900: #171717    /* Dark backgrounds */
--gray-950: #0A0A0A    /* Deepest dark */
```

#### Brand Accent Options (pick ONE primary per project)
```
/* Purple — authority, innovation (Accenture-inspired) */
--purple-500: #A100FF
--purple-600: #7B00CC
--purple-700: #5C0099

/* Green — growth, fintech, trust */
--green-500: #00C853
--green-600: #00A843
--green-700: #008533

/* Blue — reliability, enterprise (Atlassian-inspired) */
--blue-500: #0052CC
--blue-600: #0747A6
--blue-700: #003884

/* Red — energy, boldness (Adobe/Rocket-inspired) */
--red-500: #E51937
--red-600: #C7152F
--red-700: #A01128
```

#### System Colors
```
--success: #16A34A
--warning: #EAB308
--error:   #DC2626
--info:    #2563EB
```

### Color Rules
- Dark heroes with light text are strong openers — use them
- White/light section backgrounds are fine but must feel SPACIOUS and DELIBERATE, not empty
- Alternate between dark and light sections for rhythm
- Accent color used sparingly: CTAs, key highlights, hover states, brand moments
- Never use gradients as backgrounds (they look generic/AI). Solid colors or subtle texture only
- If gradient is needed, keep it very subtle (5–10% opacity shift), never rainbow
- Text contrast: minimum 4.5:1 ratio always

---

## Spacing System

### Base Unit: 4px
```
--space-1:  4px    (0.25rem)
--space-2:  8px    (0.5rem)
--space-3:  12px   (0.75rem)
--space-4:  16px   (1rem)
--space-5:  20px   (1.25rem)
--space-6:  24px   (1.5rem)
--space-8:  32px   (2rem)
--space-10: 40px   (2.5rem)
--space-12: 48px   (3rem)
--space-16: 64px   (4rem)
--space-20: 80px   (5rem)
--space-24: 96px   (6rem)
--space-32: 128px  (8rem)
```

### Section Spacing
- Between major sections: 96–128px (space-24 to space-32)
- Section internal padding: 64–96px vertical (space-16 to space-24)
- Content max-width: 1280px (80rem) with auto margins
- Generous whitespace is MANDATORY — the page must breathe
- Never stack content blocks without adequate spacing

### Container Widths
```
--container-sm: 640px    /* Narrow content, forms */
--container-md: 768px    /* Blog posts, articles */
--container-lg: 1024px   /* Standard content */
--container-xl: 1280px   /* Full layouts */
--container-2xl: 1536px  /* Wide layouts, dashboards */
```

---

## Layout Patterns

### Navigation
- **Style:** Clean horizontal nav with mega-menu capability for complex sites
- Mega-menus signal ecosystem depth — use them when there are 3+ product/service areas
- Nav should feel structured and layered — "there's a lot here" without clutter
- Sticky nav on scroll with subtle backdrop blur + shadow
- Mobile: full-screen overlay menu, not a tiny hamburger dropdown
- Nav height: 64–80px desktop, 56–64px mobile

### Hero Sections
- GO BIG. Full-viewport or near-full-viewport heroes
- Dark background with light text is the default strong opener
- One clear headline (large, declarative), one subheadline, one CTA
- Hero image/video should be cinematic or tech-forward, never generic stock
- If no custom imagery: use abstract geometric patterns, not stock photos
- Subtle entrance animations (fade up, not bounce)

### Content Sections
- Alternate light/dark backgrounds for visual rhythm
- Use CSS Grid for complex layouts, Flexbox for simpler arrangements
- Card grids: 3-column on desktop, 2 on tablet, 1 on mobile
- Cards should have consistent height within a row
- Section titles centered or left-aligned (be consistent within a project)

### Footer
- Comprehensive, multi-column footer (enterprise signal)
- Include: nav links, company info, social links, legal
- Dark background preferred
- Not an afterthought — it should feel intentional

---

## Component Standards

### Buttons
```css
/* Primary CTA */
padding: 14px 32px;
font-size: 16px;
font-weight: 600;
border-radius: 8px;
transition: all 0.2s ease;
/* Use brand accent color as background */

/* Secondary/Outline */
Same sizing, transparent bg, 2px border in brand color

/* Ghost */
No border, brand color text, subtle hover background
```
- Minimum touch target: 44x44px
- Never use rounded-full (pill) buttons — they look generic
- Hover: subtle lift (translateY -1px) + shadow, or darken bg 10%
- Active: scale(0.98) for tactile feel

### Cards
```css
background: white; /* or gray-900 on dark sections */
border-radius: 12px;
padding: 32px;
border: 1px solid var(--gray-200); /* light mode */
transition: all 0.3s ease;
```
- Hover: subtle shadow elevation + slight translateY
- No heavy borders or outlines
- Image cards: image fills top, content below with consistent padding
- Always equal height in grids

### Forms
- Large input fields (48–52px height)
- 12px border-radius on inputs
- Clear labels above inputs (never floating labels — they're confusing)
- Visible focus states with brand color ring
- Error states: red border + message below field
- Group related fields logically

### Tables/Data
- Clean horizontal lines, no vertical borders
- Alternating row backgrounds (very subtle)
- Sticky headers on long tables
- Responsive: horizontal scroll or card-stack on mobile

---

## Animation & Motion

### Principles
- Motion should feel purposeful, not decorative
- Everything is subtle — no bouncing, no spinning, no excessive parallax
- If a user wouldn't notice it consciously, it's working

### Standard Transitions
```css
/* Default */
transition: all 0.2s ease;

/* Hover effects */
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Page transitions / section reveals */
transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
```

### Scroll Animations
- Fade-up on scroll for content sections (use Framer Motion or CSS intersection observer)
- Stagger children: 50–100ms delay between items
- Never animate more than opacity + transform
- Reduce motion: respect `prefers-reduced-motion`

---

## Imagery & Media

### Rules
- NO generic stock photography. Ever.
- Acceptable: custom photography, tech-forward renders, cinematic imagery, abstract geometric patterns, brand illustrations
- If no budget for custom imagery: use abstract/geometric patterns, subtle gradient meshes, or icon-based illustrations
- Hero images should be high-quality, full-bleed or contained with purpose
- Icons: Lucide React (consistent, clean line style)
- Icon size: 20–24px inline, 32–48px for feature blocks

---

## Responsive Design

### Breakpoints (Tailwind defaults)
```
sm:  640px
md:  768px
lg:  1024px
xl:  1280px
2xl: 1536px
```

### Rules
- Mobile-first approach always
- Touch targets minimum 44x44px
- Body text never below 16px on mobile
- Test at: 375px (phone), 768px (tablet), 1280px (laptop), 1920px (desktop)
- Navigation collapses to mobile menu at `lg` breakpoint
- Images are always responsive with proper aspect ratios
- No horizontal scroll on any viewport

---

## Anti-Patterns (NEVER DO THESE)

1. **Generic AI gradients** — rainbow or purple-blue-pink gradients everywhere
2. **Cookie-cutter SaaS templates** — the Stripe clone look everyone uses
3. **Floating labels on forms** — confusing and look broken
4. **Tiny hamburger dropdowns** — use full-screen mobile menus
5. **Stock photo heroes** — smiling business people shaking hands
6. **Rounded-full pill buttons** — generic and trendy
7. **Excessive animations** — bouncing, spinning, parallax overload
8. **Low-contrast text** — gray on gray, light text on light backgrounds
9. **Cluttered layouts** — insufficient spacing, cramming content
10. **Sloppy responsive** — content overflowing, breaking at random widths
11. **Generic "SaaS purple"** — that same washed-out purple every AI tool uses
12. **Testimonial carousels with stock headshots** — if you can't get real photos, use text-only testimonials
13. **"Built with [framework]" energy** — the site should feel custom, not template-derived
14. **Decorative blobs or circles** — those amorphous SVG shapes in the background

---

## Homepage / Landing Page Minimum Standard

EVERY landing page must include AT LEAST these sections (12-15 minimum):
1. **Rich hero** — gradient bg, device mockup (CSS phone/laptop), headline, dual CTAs, trust chips
2. **Trust/press bar** — "Featured in" logos (TechCrunch, Forbes, etc.)
3. **Featured content cards** — with gradient headers, shadows, hover elevation, ratings, badges
4. **How It Works** — 3-4 steps with numbered badges and icons
5. **Feature showcase (audience 1)** — alternating text+visual layout with UI mockup
6. **Feature showcase (audience 2)** — reversed layout with dashboard/product mockup
7. **Stats section** — large numbers on dark gradient with glass-morphism cards
8. **Testimonials** — star ratings, avatar initials, quotation marks, author details
9. **Pricing** — clear card with feature checklist and CTA
10. **FAQ accordion** — 6+ questions with expand/collapse
11. **Final CTA** — dark gradient, big headline, dual buttons, app store badges
12. **Comprehensive footer** — multi-column, social icons, legal links

### Key Rules:
- NEVER ship a sparse homepage. Visual density = credibility.
- ALWAYS use static/hardcoded demo data so homepage looks rich without database dependency.
- ALWAYS build device mockups with CSS (phone frames, dashboard previews) — they prove the product exists.
- ALWAYS alternate section backgrounds (gradient, dark, gray-50, white) for visual rhythm.
- Feature sections MUST alternate layout direction (text-left/visual-right → visual-left/text-right).
- ALWAYS screenshot the competitor before building and match/exceed their visual density.
- Run visual review skill DURING development, not just after deploy.

## Pre-Build Checklist

Before passing any spec to Claude Code, verify:

- [ ] Brand accent color chosen for this project
- [ ] Typography: Inter loaded, scale applied
- [ ] Hero section: dark bg, large headline, clear CTA
- [ ] Spacing: generous, follows 4px grid
- [ ] Navigation: sticky, mega-menu if complex
- [ ] Footer: comprehensive, multi-column
- [ ] Responsive: mobile-first, all breakpoints covered
- [ ] Animations: subtle fade-up on scroll, hover states on interactive elements
- [ ] Images: no stock photos, using geometric/abstract/custom
- [ ] Anti-patterns: none of the 14 anti-patterns present
- [ ] Accessibility: contrast ratios met, focus states visible, semantic HTML
- [ ] SEO: meta tags, Open Graph, structured heading hierarchy
