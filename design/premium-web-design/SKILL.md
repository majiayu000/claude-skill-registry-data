---
name: Premium Web Design
description: Comprehensive luxury web design skill with reusable animation/interaction patterns, reference site analyses, and tool guides for building stunning React+TS+Tailwind websites
recall_keywords: [premium design, luxury website, animation, scroll animation, parallax, hero section, hover effect, page transition, clinic website, GSAP, framer motion, lenis, smooth scroll, reveal animation, staggered, magnetic button, cursor follower, before after slider, booking form, whatsapp button, review carousel, premium ui, stunning website, beautiful design, luxury ui, elegant, interactive]
---

# Premium Web Design Skill

Build stunning, award-winning websites with production-ready animation and interaction patterns. Designed for luxury brands, medical aesthetics clinics, and premium digital experiences.

## Quick Start — "I Need X" Pattern Index

| I need... | Use pattern | File |
|---|---|---|
| Elements appearing on scroll | Fade-In on Scroll, Staggered Reveal | patterns/scroll-animations.md |
| Depth/layers while scrolling | Parallax Background | patterns/scroll-animations.md |
| Horizontal scrolling section | Horizontal Scroll Section | patterns/scroll-animations.md |
| Reading progress indicator | Scroll Progress Bar | patterns/scroll-animations.md |
| Dramatic text entrance | Text Reveal Word-by-Word | patterns/scroll-animations.md |
| Content changing in sticky area | Sticky Section with Scroll-Driven Content | patterns/scroll-animations.md |
| Dramatic landing area | Full-Screen Text Reveal, Video Background | patterns/hero-sections.md |
| Layered depth on hero | Parallax Image Layers | patterns/hero-sections.md |
| Animated color background | Animated Gradient Background | patterns/hero-sections.md |
| Image + text side by side | Split-Screen Hero | patterns/hero-sections.md |
| Navbar changes on scroll | Transparent-to-Solid | patterns/navigation.md |
| Mobile hamburger menu | Full-Screen Hamburger Overlay | patterns/navigation.md |
| Animated link hover | Animated Underline Links | patterns/navigation.md |
| Bilingual language toggle | Bilingual Language Switcher | patterns/navigation.md |
| Button that pulls to cursor | Magnetic Button Effect | patterns/hover-cursor.md |
| Image color on hover | Grayscale-to-Color | patterns/hover-cursor.md |
| Card perspective effect | 3D Card Tilt | patterns/hover-cursor.md |
| Custom cursor that follows mouse | Custom Cursor Follower | patterns/hover-cursor.md |
| Route transitions | Fade, Clip-Path, Shared Layout | patterns/page-transitions.md |
| Animated card grid | Staggered Card Grid | patterns/content-elements.md |
| Numbers counting up | Counter Animation | patterns/content-elements.md |
| Before/after comparison | Image Comparison Slider | patterns/content-elements.md |
| Testimonial display | Testimonial Carousel | patterns/content-elements.md |
| Collapsible sections | Accordion with Smooth Height | patterns/content-elements.md |
| Progressive image loading | Blur-to-Sharp Lazy Load | patterns/content-elements.md |
| Service listing cards | Service Card | patterns/medical-spa.md |
| Doctor profiles | Doctor Profile Card | patterns/medical-spa.md |
| Treatment results display | Before/After Slider | patterns/medical-spa.md |
| Appointment booking | Multi-Step Booking Form | patterns/medical-spa.md |
| WhatsApp contact | WhatsApp Floating Button | patterns/medical-spa.md |
| Client reviews | Review Carousel with Stars | patterns/medical-spa.md |

## Design Principles — Premium vs Generic

### What Makes a Site Feel Premium
1. **Restraint over excess** — One hero animation, not five competing effects
2. **Intentional whitespace** — Let elements breathe; crowded = cheap
3. **Subtle motion** — 0.3-0.6s transitions, ease-out curves, never bounce
4. **Typography hierarchy** — Serif for headlines, sans for body, generous line-height
5. **Color discipline** — 2-3 colors max for luxury brands
6. **Reveal, don't display** — Elements should feel discovered, not dumped on screen
7. **Consistent timing** — Same easing and duration across all animations
8. **Photography-led** — Large, high-quality images with subtle treatments

### Anti-Patterns (What Makes Sites Look AI-Generated)
1. Generic gradient backgrounds with no brand connection
2. Every element animated — scroll fatigue kills engagement
3. Stock photo grids with identical aspect ratios
4. Overly complex animations that distract from content
5. Inconsistent animation timing and easing
6. Too many font families (max 2-3)
7. Animations that block content access or cause layout shift
8. Parallax on mobile (kills performance, feels gimmicky)
9. Auto-playing video without user context
10. Symmetric layouts everywhere — asymmetry creates visual interest

## Animation Timing Guide

| Context | Duration | Easing |
|---|---|---|
| Micro-interaction (hover, focus) | 150-250ms | ease-out |
| Element reveal on scroll | 400-600ms | ease-out or power2.out |
| Page transition | 300-500ms | ease-in-out |
| Stagger between items | 50-100ms | — |
| Background parallax | Continuous | linear |
| Number counter | 1500-2500ms | power3.out |
| Menu open/close | 300-400ms | ease-in-out |
| Modal/overlay | 200-300ms | ease-out |

## Color Palette Examples (pick one, or build your own)

### Classic Luxury
- Primary: `#0D1B3E` (deep navy) — Text, headers
- Accent: `#C9A035` (gold) — CTAs, accent borders
- Neutral: `#FFFFFF` (white) — Backgrounds
- Off-white: `#FAFBFC` — Section backgrounds
- Beige: `#F5F3F0` — Subtle dividers

### Rose Gold
- Primary: `#B76E79` | Dark: `#2C2C2C` | Light: `#F7F3F0`

### Emerald Spa
- Primary: `#1B4332` | Accent: `#D4AF37` | Neutral: `#F8F6F2`

### Modern Minimal
- Primary: `#111111` | Neutral: `#E8E4DF` | Light: `#FFFFFF`

### Pearl & Champagne
- Primary: `#E6D5B8` | Text: `#4A4A4A` | Light: `#FEFDFB`

> **Customize**: Define your brand palette once in your project's Tailwind config + a design token file. Reference everywhere by semantic name (`bg-brand-primary`), not hex.

## Typography Recommendations

| Role | Font | Weight | Size (desktop) |
|---|---|---|---|
| Hero headline | Georgia, Playfair Display | 300-400 | 48-72px |
| Section headline | Georgia, Cormorant Garamond | 400 | 32-40px |
| Body text | Inter, DM Sans | 400 | 16-18px |
| Button/CTA | Inter, DM Sans | 500-600 | 14-16px |
| Caption/meta | Inter, DM Sans | 400 | 12-14px |
| Arabic headlines | Noto Kufi Arabic | 400-500 | 32-48px |
| Arabic body | Noto Sans Arabic | 400 | 16-18px |

## File Index

```
premium-web-design/
  SKILL.md                          <- This file
  patterns/
    scroll-animations.md            <- 8 scroll patterns
    hero-sections.md                <- 5 hero patterns
    navigation.md                   <- 4 nav patterns
    hover-cursor.md                 <- 4 hover/cursor patterns
    page-transitions.md             <- 3 transition patterns
    content-elements.md             <- 6 content patterns
    medical-spa.md                  <- 6 medical spa patterns
  references/
    [domain].md                     <- Analyzed reference sites
  tools/
    ANIMATION-TOOLS.md              <- GSAP, Framer Motion, Lenis reference
```

## Dependencies (npm install)

```bash
npm install gsap @gsap/react motion lenis
```

> **Note:** `motion` is the successor to `framer-motion` (rebranded mid-2025). Import from `motion/react` instead of `framer-motion`.

## Component Sources

| Source | What It Offers | When to Use |
|---|---|---|
| **21st.dev Magic** (MCP) | Generate React+TS+Tailwind components from natural language | Before hand-coding standard UI components |
| **Origin UI** (coss.com/ui) | 400+ free copy-paste React+Tailwind components (MIT) | Browse for ready-made cards, forms, navbars, inputs |
| **shadcn/ui** | Accessible, composable React components | Base primitives that you customize |
| **Radix UI** | Unstyled accessible primitives | When you need total visual control |

## RTL / Bilingual Checklist

- [ ] All horizontal animations reverse for `dir="rtl"`
- [ ] Text alignment follows logical properties (`text-start` not `text-left`)
- [ ] Padding/margin use logical properties (`ps-4` not `pl-4`)
- [ ] Icons that indicate direction (arrows, chevrons) flip for RTL
- [ ] Language switcher stores preference in localStorage
- [ ] Font family switches to the RTL typeface for RTL content
- [ ] Floating CTAs (WhatsApp, chat) move to bottom-left in RTL

## Design Inspiration Philosophy

**Core thesis**: In the AI era, the differentiator is interactivity and intentional design. Scroll-stopping websites beat generic AI output. Designs conceived in Figma; implemented in code with React + GSAP + Framer Motion + Lenis.

**Signature techniques to replicate**:
- Oversized serif headlines overlapping product imagery (`mix-blend-mode` + `z-index`)
- Scroll-driven product reveals (GSAP `ScrollTrigger` with `scrub`)
- Cinematic section transitions (Framer Motion `AnimatePresence`)
- Grain/noise texture overlays for tactile depth
- Dark-to-light section rhythm for visual contrast

See `references/` for full analyses of specific sites you want to learn from.

## Related Skills — Use Together, Not Instead

This skill is an UPGRADE LAYER. It works alongside existing skills, never replacing them.

| Skill | What It Does | When to Use It WITH premium-web-design |
|---|---|---|
| **21st-dev-magic** | Generates base components from natural language via MCP | START here for standard components (cards, navs, forms), then apply premium-web-design animation patterns on top |
| **frontend-design** (Anthropic plugin) | Full frontend development workflow, component scaffolding | Use for project structure, build pipeline, component organization. premium-web-design adds the animation/interaction polish |
| **impeccable** | Design polish, micro-interactions, pixel-perfect refinement | Apply AFTER premium-web-design patterns are in place — impeccable is the final coat of paint |
| **tailwind-patterns** | Tailwind-specific utilities, responsive patterns, design tokens | Use for Tailwind class strategy |
| **ui-ux-pro-max** | UX strategy, user flows, information architecture | Use BEFORE premium-web-design — decide WHAT to build and WHY |
| **react-patterns** | React component architecture, hooks, state management | Use for component structure decisions |
| **i18n-localization** | Full i18n setup, RTL support, translation workflow | Use alongside — every premium-web-design pattern has RTL notes |
| **instagram-access** | Download Instagram assets (photos, reels, stories) | Use to pull real brand imagery and social proof content |

## MCP Servers for Website Development

| MCP Server | What It Does | When to Use |
|---|---|---|
| **@21st-dev/magic** | Generate React+TS+Tailwind components from natural language | Before hand-coding — check if a ready-made component exists |
| **context7** | Look up live library documentation | Before writing GSAP/Framer Motion/React code — get latest API syntax |
| **playwright** | Browser automation, visual testing, screenshots | Preview and test components in real browser |
| **github** | PRs, issues, repo management | Commit, push, review workflow |
| **exa-web-search** | Deep web research | Research design inspiration, competitor analysis |

## Design Reference Libraries

- **awesome-design-md** (`~/.claude/references/awesome-design-md/`) — DESIGN.md files from Airbnb, Apple, Linear, Spotify, Stripe. Use for design system principles from world-class teams.
- **premium-web-design references** (`references/` subfolder) — Analyzed websites. Use for specific animation techniques and luxury design patterns.
