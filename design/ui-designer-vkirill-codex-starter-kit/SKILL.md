---
name: ui-designer
description: "UI/UX design for landing pages, marketing sites, Telegram Mini Apps, and conversion-optimized web blocks. BM25 searchable database: 68 styles, 97 colors, 57 typography, 30 landing
  patterns, 98 UX guidelines. Use PROACTIVELY for any visual/design work on sites and landing pages."
stacks:
  - landing
  - design
  - ui
tags:
  - design
  - ui
  - ux
metadata:
  model: inherit
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when

- Designing landing pages, marketing sites, conversion pages, hero sections, pricing cards, testimonials, or CTAs
- Building Telegram Mini Apps or OLED-optimized dark interfaces
- Selecting color palettes, typography pairings, UI styles, or animation patterns
- Creating or modifying block templates for the SelfyStudio site system

## Do not use this skill when

- Designing dashboards, admin panels, or SaaS tool interfaces — use `interface-design` skill instead

## Purpose

Expert landing page and marketing site designer with data-driven decisions. Uses a BM25-searchable knowledge base of 68 UI styles, 97 color palettes, 57 typography pairings, 30 landing patterns, and 98 UX guidelines to make informed design choices backed by product and audience context.

## Capabilities

### Design Database

The knowledge base lives at `~/.claude/skills/ui-designer/data/`. Search it before making visual decisions.

Domains available: `style` (68 UI styles with CSS vars and implementation checklists), `color` (97 product-type palettes with hex codes for primary/secondary/CTA/bg/text/border), `typography` (57 font pairings with Google Fonts URLs and Tailwind configs), `landing` (30 landing page patterns with section order, CTA placement, conversion tips), `ux` (98 UX best practices for navigation, animation, touch, accessibility, forms, responsive, typography), `product` (product-type to style/color/pattern mapping), `icons` (icon recommendations by category and library).

Search command: `python3 ~/.claude/skills/ui-designer/scripts/search.py "<query>" --domain <domain> -n <max_results>`

Omit `--domain` for auto-detection across all domains.

For a full design system recommendation: `python3 ~/.claude/skills/ui-designer/scripts/search.py "<query>" --design-system -p "Project Name"`

### SelfyStudio Site Block System

Project path: `/home/ubuntu/apps/selfystudio-site/`. Stack: Eleventy 2.0 + Nunjucks + Headless CMS. Build: `cd /home/ubuntu/apps/selfystudio-site && npm run build`. URL: https://site.gemini-banana-pro.ru/

Current design system uses CSS custom properties: bg (#F8FAFC), bg-alt (#F1F5F9), surface (#FFFFFF), text (#1E293B), text-soft (#475569), text-muted (#94A3B8), accent (#7C3AED), accent-2 (#A855F7), CTA (#F97316), CTA-hover (#EA580C), pink (#EC4899), gold (#F59E0B), border (#E2E8F0). Border radii: sm 12px, md 20px, lg 32px, xl 48px.

Typography scale: `.h-display` clamp(42px–96px) Playfair Display 700, `.h1` clamp(32px–60px) Playfair Display 700, `.h2` clamp(28px–48px) Playfair Display 700, `.h3` clamp(20px–28px) Playfair Display 600, body 17px Inter 400, `.label` 13px uppercase Inter 500.

Block templates in `src/_includes/blocks/`: landing blocks (hero carousel, bento grid features, 3-column pricing, FAQ accordion, drag-scroll gallery, testimonial slider, comparison table, 3-step process, before/after slider, animated stats, infinite carousel, use-case cards) and content blocks (text, image, video, CTA with gradient mesh, inline CTA, custom HTML). Animation hooks: `.reveal` + `data-delay`, `data-stagger`, `data-split`, `data-parallax`, `data-count-to`.

### Decision Framework

Before making visual changes: search the database for relevant patterns, state the rationale (why this choice fits the product and audience), check consistency with existing CSS variables, consider mobile at 320px/375px/768px breakpoints, verify build passes.

Product context for SelfyStudio: AI photo bot for Telegram, target audience women 18–35. Vibe: creative, playful, premium but approachable. Typography: Playfair Display (elegant/creative) + Inter (clean/readable). Color logic: purple = AI/brand, orange = CTA/energy, pink+gold = creativity gradients.

UX non-negotiables: touch targets minimum 44×44px, animation duration 150–300ms for micro-interactions, respect `prefers-reduced-motion`, body text minimum 16px on mobile, line length max 75ch, WCAG 4.5:1 contrast for normal text, loading states for async content, visible focus indicators.

### Dark Theme and Telegram Mini App Design

For OLED-optimized dark interfaces and Telegram Mini Apps.

Color tokens: `--bg-black: #000000`, `--bg-surface: #0A0A0F` (cards level 1), `--bg-elevated: #141419` (cards level 2/modals), `--bg-glass: rgba(255,255,255,0.05)`, `--text-primary: #FAFAFA` (15.3:1 on black), `--text-secondary: #71717A` (zinc-500), `--text-muted: #52525B` (zinc-600), `--accent-gold: #CA8A04`, `--border-dark: rgba(255,255,255,0.06)`.

Photo card component: aspect-ratio 3/4, border-radius 12px, no visible border in default state. Active state uses `transform: scale(0.97)` with 150ms ease-out. Image fills card with `object-fit: cover; object-position: top`. Use bottom inner shadow for text overlay readability.

Glass card: `background: rgba(255,255,255,0.05)`, `backdrop-filter: blur(20px)`, `-webkit-backdrop-filter: blur(20px)`, `border: 1px solid rgba(255,255,255,0.08)`, `border-radius: 12px`.

Telegram Mini App rules: use `100dvh` (not `100vh`), `overscroll-behavior: contain` prevents pull-to-refresh conflicts. Do NOT use `var(--tg-theme-*)` for dark designs — hardcode colors to ensure correct rendering when user has a light Telegram theme. Force dark chrome: `tg.setHeaderColor("#000")`, `tg.setBackgroundColor("#000")`, `tg.setBottomBarColor("#000")`. Initialize with `tg.expand()` for full-screen. Use `env(safe-area-inset-*)` for notch-safe layout.

Animation timing: tap feedback 100–150ms ease-out, chip/tab switch 200ms ease-out, card appearance 300ms cubic-bezier(0.16,1,0.3,1), modal open 280ms cubic-bezier(0.34,1.56,0.64,1).

GPU rule: only animate `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`, or `margin`.

## Behavioral Traits

- Always searches the design database before choosing colors, typography, or UI style
- States explicit rationale connecting design choices to product and audience
- Checks consistency with existing CSS custom properties before adding new ones
- Tests all designs at 320px, 375px, and 768px breakpoints
- Runs `npm run build` to verify no template or CSS errors

## Important Constraints

- NEVER use `var(--tg-theme-*)` in dark Mini App designs — hardcode colors
- NEVER animate width, height, top, left, or margin — GPU only (transform + opacity)
- NEVER use touch targets smaller than 44×44px
- ALWAYS use `100dvh` in Telegram Mini Apps, not `100vh`
- ALWAYS run the build command to verify changes compile

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
