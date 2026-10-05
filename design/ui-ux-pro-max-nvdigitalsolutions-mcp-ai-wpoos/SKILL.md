---
type: Skill
name: ui-ux-pro-max
description: AI-powered design intelligence with 67 UI styles, 161 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 15+ tech stacks. Generates complete design systems for any product type with industry-specific reasoning rules.
source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
license: MIT — see THIRD_PARTY_NOTICES.md
---

# UI/UX Pro Max — Design Intelligence Skill

This skill activates AI-powered design intelligence for producing polished, production-ready UI/UX work. It embeds 67 UI styles, 99 UX guidelines, pre-delivery checklists, and a structured design system workflow so the AI can generate complete, coherent design systems without any external tooling.

## When to Use This Skill

Activate this skill whenever the user asks to:
- **Build** a UI, screen, component, page, or application
- **Design** a layout, design system, style guide, or visual identity
- **Create** mockups, wireframes, prototypes, or production-ready code
- **Implement** a frontend, dashboard, landing page, or mobile screen
- **Review** an existing UI for quality, consistency, or accessibility issues
- **Fix** design problems: poor contrast, broken layouts, inconsistent spacing
- **Improve** an existing interface's visual quality or usability

---

## Design System Generation Workflow

### Step 1 — Analyze Requirements

Before selecting any style or color, extract the following from the user's request:

1. **Product type** — What is being built? (SaaS dashboard, e-commerce store, mobile app, landing page, etc.)
2. **Industry** — Which industry category applies? (See Industry Categories table below.)
3. **Target audience** — Who are the end users? (age, technical level, accessibility needs)
4. **Tech stack** — Which framework or platform? (See Supported Tech Stacks below.)
5. **Tone/brand** — Any stated brand personality, color preferences, or aesthetic direction?
6. **Constraints** — Dark mode required? Accessibility level (AA/AAA)? Performance budget?

### Step 2 — Select Style, Color & Typography

Using the analysis from Step 1:

1. **Choose a UI style** from the 67 UI Styles table that best matches the product type and industry.
2. **Select a color palette** appropriate to the industry (use the Industry Categories table to guide palette mood).
3. **Choose a font pairing** — a display/heading font + a body font that match the chosen style's personality.
4. **Define semantic color tokens**: `primary`, `secondary`, `surface`, `error`, `success`, `warning`, `text`, `text-muted`, `border`.
5. **Define a spacing scale** using 4pt/8dp increments: `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96`.
6. **Define a type scale**: `12 / 14 / 16 / 18 / 24 / 32 / 48`.

### Step 3 — Implement

Apply the design system to the requested output:

- Use the chosen style's visual language consistently across all components.
- Apply the spacing scale — never use arbitrary pixel values.
- Apply the type scale — never use arbitrary font sizes.
- Implement all 10 rule categories from the Quick Reference (§1–§10) as hard constraints.
- Validate against the Pre-Delivery Checklist before finalizing output.

### Step 4 — Validate

Before presenting the final output, run through the Pre-Delivery Checklist (see below). Fix any failing items. Only present output that passes all checklist items.

---

## Rule Categories — Priority Table

| Priority | Category | Level | Description |
|----------|----------|-------|-------------|
| 1 | Accessibility | **CRITICAL** | Color contrast, focus states, ARIA, keyboard nav, screen reader support |
| 2 | Touch & Interaction | **CRITICAL** | Touch target sizes, tap feedback, safe areas, loading states |
| 3 | Performance | **HIGH** | Image optimization, lazy loading, bundle splitting, list virtualization |
| 4 | Style Selection | **HIGH** | Style-product match, consistency, icon sets, dark mode pairing |
| 5 | Layout & Responsive | **HIGH** | Mobile-first, breakpoints, no horizontal scroll, spacing scale |
| 6 | Typography & Color | **MEDIUM** | Line height, line length, font pairing, semantic color tokens |
| 7 | Animation | **MEDIUM** | Duration/easing, transform-only, reduced-motion, interruptibility |
| 8 | Forms & Feedback | **MEDIUM** | Labels, error placement, submit feedback, inline validation |
| 9 | Navigation Patterns | **HIGH** | Bottom nav limits, back behavior, deep linking, adaptive nav |
| 10 | Charts & Data | **LOW** | Chart type matching, accessible palettes, responsive charts |

---

## Quick Reference — 99 UX Guidelines

### §1 Accessibility (CRITICAL)

| Rule | Guideline |
|------|-----------|
| `color-contrast` | Minimum 4.5:1 ratio for normal text (large text 3:1) |
| `focus-states` | Visible focus rings on interactive elements (2–4px) |
| `alt-text` | Descriptive alt text for meaningful images |
| `aria-labels` | `aria-label` for icon-only buttons |
| `keyboard-nav` | Tab order matches visual order; full keyboard support |
| `form-labels` | Use `<label>` with `for` attribute |
| `skip-links` | Skip to main content for keyboard users |
| `heading-hierarchy` | Sequential h1→h6, no level skip |
| `color-not-only` | Don't convey info by color alone (add icon/text) |
| `dynamic-type` | Support system text scaling; avoid truncation as text grows |
| `reduced-motion` | Respect `prefers-reduced-motion`; reduce/disable animations when requested |
| `voiceover-sr` | Meaningful `accessibilityLabel`/`accessibilityHint`; logical reading order |

### §2 Touch & Interaction (CRITICAL)

| Rule | Guideline |
|------|-----------|
| `touch-target-size` | Min 44×44pt (Apple) / 48×48dp (Material) |
| `touch-spacing` | Minimum 8px/8dp gap between touch targets |
| `hover-vs-tap` | Use click/tap for primary interactions; don't rely on hover alone |
| `loading-buttons` | Disable button during async operations; show spinner or progress |
| `error-feedback` | Clear error messages near problem |
| `cursor-pointer` | Add `cursor-pointer` to clickable elements (Web) |
| `tap-delay` | Use `touch-action: manipulation` to reduce 300ms delay (Web) |
| `press-feedback` | Visual feedback on press (ripple/highlight) |
| `safe-area-awareness` | Keep primary touch targets away from notch, Dynamic Island, gesture bar |

### §3 Performance (HIGH)

| Rule | Guideline |
|------|-----------|
| `image-optimization` | Use WebP/AVIF, responsive images (`srcset`/`sizes`), lazy load non-critical assets |
| `image-dimension` | Declare `width`/`height` or use `aspect-ratio` to prevent layout shift (CLS) |
| `font-loading` | Use `font-display: swap/optional` to avoid invisible text (FOIT) |
| `critical-css` | Prioritize above-the-fold CSS |
| `lazy-loading` | Lazy load non-hero components via dynamic import / route-level splitting |
| `bundle-splitting` | Split code by route/feature to reduce initial load and TTI |
| `reduce-reflows` | Avoid frequent layout reads/writes; batch DOM reads then writes |
| `virtualize-lists` | Virtualize lists with 50+ items |
| `main-thread-budget` | Keep per-frame work under ~16ms for 60fps |
| `debounce-throttle` | Use debounce/throttle for high-frequency events |

### §4 Style Selection (HIGH)

| Rule | Guideline |
|------|-----------|
| `style-match` | Match style to product type |
| `consistency` | Use same style across all pages |
| `no-emoji-icons` | Use SVG icons (Heroicons, Lucide), not emojis |
| `color-palette-from-product` | Choose palette from product/industry |
| `effects-match-style` | Shadows, blur, radius aligned with chosen style |
| `platform-adaptive` | Respect platform idioms (iOS HIG vs Material) |
| `state-clarity` | Make hover/pressed/disabled states visually distinct |
| `dark-mode-pairing` | Design light/dark variants together |
| `icon-style-consistent` | Use one icon set/visual language across the product |
| `primary-action` | Each screen should have only one primary CTA |

### §5 Layout & Responsive (HIGH)

| Rule | Guideline |
|------|-----------|
| `viewport-meta` | `width=device-width initial-scale=1` (never disable zoom) |
| `mobile-first` | Design mobile-first, then scale up |
| `breakpoint-consistency` | Use systematic breakpoints (375 / 768 / 1024 / 1440) |
| `readable-font-size` | Minimum 16px body text on mobile |
| `line-length-control` | Mobile 35–60 chars per line; desktop 60–75 chars |
| `horizontal-scroll` | No horizontal scroll on mobile |
| `spacing-scale` | Use 4pt/8dp incremental spacing system |
| `container-width` | Consistent max-width on desktop (`max-w-6xl` / `7xl`) |
| `z-index-management` | Define layered z-index scale |
| `fixed-element-offset` | Fixed navbar/bottom bar must reserve safe padding |
| `viewport-units` | Prefer `min-h-dvh` over `100vh` on mobile |

### §6 Typography & Color (MEDIUM)

| Rule | Guideline |
|------|-----------|
| `line-height` | Use 1.5–1.75 for body text |
| `line-length` | Limit to 65–75 characters per line |
| `font-pairing` | Match heading/body font personalities |
| `font-scale` | Consistent type scale (e.g. 12 14 16 18 24 32) |
| `contrast-readability` | Darker text on light backgrounds |
| `color-semantic` | Define semantic color tokens (primary, secondary, error, surface) |
| `color-dark-mode` | Dark mode uses desaturated / lighter tonal variants, not inverted colors |
| `color-accessible-pairs` | Foreground/background pairs must meet 4.5:1 (AA) or 7:1 (AAA) |
| `truncation-strategy` | Prefer wrapping over truncation |
| `whitespace-balance` | Use whitespace intentionally to group related items |

### §7 Animation (MEDIUM)

| Rule | Guideline |
|------|-----------|
| `duration-timing` | Use 150–300ms for micro-interactions; complex transitions ≤400ms |
| `transform-performance` | Use `transform`/`opacity` only; avoid animating `width`/`height`/`top`/`left` |
| `loading-states` | Show skeleton or progress indicator when loading exceeds 300ms |
| `easing` | Use `ease-out` for entering, `ease-in` for exiting |
| `motion-meaning` | Every animation must express a cause-effect relationship |
| `spring-physics` | Prefer spring/physics-based curves for natural feel |
| `exit-faster-than-enter` | Exit animations shorter than enter (~60–70% of enter duration) |
| `interruptible` | Animations must be interruptible by user tap/gesture |
| `no-blocking-animation` | Never block user input during an animation |

### §8 Forms & Feedback (MEDIUM)

| Rule | Guideline |
|------|-----------|
| `input-labels` | Visible label per input (not placeholder-only) |
| `error-placement` | Show error below the related field |
| `submit-feedback` | Loading then success/error state on submit |
| `required-indicators` | Mark required fields (e.g. asterisk) |
| `empty-states` | Helpful message and action when no content |
| `toast-dismiss` | Auto-dismiss toasts in 3–5s |
| `confirmation-dialogs` | Confirm before destructive actions |
| `inline-validation` | Validate on blur (not keystroke) |
| `input-type-keyboard` | Use semantic input types (`email`, `tel`, `number`) |
| `focus-management` | After submit error, auto-focus the first invalid field |

### §9 Navigation Patterns (HIGH)

| Rule | Guideline |
|------|-----------|
| `bottom-nav-limit` | Bottom navigation max 5 items; use labels with icons |
| `back-behavior` | Back navigation must be predictable and consistent |
| `deep-linking` | All key screens must be reachable via deep link / URL |
| `nav-label-icon` | Navigation items must have both icon and text label |
| `nav-state-active` | Current location must be visually highlighted |
| `modal-escape` | Modals and sheets must offer a clear close/dismiss affordance |
| `state-preservation` | Navigating back must restore previous scroll position, filter state |
| `adaptive-navigation` | Large screens (≥1024px) prefer sidebar; small screens use bottom/top nav |
| `navigation-consistency` | Navigation placement must stay the same across all pages |

### §10 Charts & Data (LOW)

| Rule | Guideline |
|------|-----------|
| `chart-type` | Match chart type to data type (trend → line, comparison → bar, proportion → pie/donut) |
| `color-guidance` | Use accessible color palettes; avoid red/green only pairs |
| `data-table` | Provide table alternative for accessibility |
| `legend-visible` | Always show legend; position near the chart |
| `tooltip-on-interact` | Provide tooltips/data labels on hover or tap |
| `axis-labels` | Label axes with units and readable scale |
| `responsive-chart` | Charts must reflow or simplify on small screens |
| `empty-data-state` | Show meaningful empty state when no data exists |
| `animation-optional` | Chart entrance animations must respect `prefers-reduced-motion` |

---

## 67 UI Styles Reference

### General Styles (49)

| # | Style Name | Best For |
|---|-----------|----------|
| 1 | Minimalism & Swiss Style | Enterprise apps, dashboards, documentation |
| 2 | Neumorphism | Health/wellness apps, meditation platforms |
| 3 | Glassmorphism | Modern SaaS, financial dashboards |
| 4 | Brutalism | Design portfolios, artistic projects |
| 5 | 3D & Hyperrealism | Gaming, product showcase, immersive |
| 6 | Vibrant & Block-based | Startups, creative agencies, gaming |
| 7 | Dark Mode (OLED) | Night-mode apps, coding platforms |
| 8 | Accessible & Ethical | Government, healthcare, education |
| 9 | Claymorphism | Educational apps, children's apps, SaaS |
| 10 | Aurora UI | Modern SaaS, creative agencies |
| 11 | Retro-Futurism | Gaming, entertainment, music platforms |
| 12 | Flat Design | Web apps, mobile apps, startup MVPs |
| 13 | Skeuomorphism | Legacy apps, gaming, premium products |
| 14 | Liquid Glass | Premium SaaS, high-end e-commerce |
| 15 | Motion-Driven | Portfolio sites, storytelling platforms |
| 16 | Micro-interactions | Mobile apps, touchscreen UIs |
| 17 | Inclusive Design | Public services, education, healthcare |
| 18 | Zero Interface | Voice assistants, AI platforms |
| 19 | Soft UI Evolution | Modern enterprise apps, SaaS |
| 20 | Neubrutalism | Gen Z brands, startups, Figma-style |
| 21 | Bento Box Grid | Dashboards, product pages, portfolios |
| 22 | Y2K Aesthetic | Fashion brands, music, Gen Z |
| 23 | Cyberpunk UI | Gaming, tech products, crypto apps |
| 24 | Organic Biophilic | Wellness apps, sustainability brands |
| 25 | AI-Native UI | AI products, chatbots, copilots |
| 26 | Memphis Design | Creative agencies, music, youth brands |
| 27 | Vaporwave | Music platforms, gaming, portfolios |
| 28 | Dimensional Layering | Dashboards, card layouts, modals |
| 29 | Exaggerated Minimalism | Fashion, architecture, portfolios |
| 30 | Kinetic Typography | Hero sections, marketing sites |
| 31 | Parallax Storytelling | Brand storytelling, product launches |
| 32 | Swiss Modernism 2.0 | Corporate sites, architecture, editorial |
| 33 | HUD / Sci-Fi FUI | Sci-fi games, space tech, cybersecurity |
| 34 | Pixel Art | Indie games, retro tools, creative |
| 35 | Bento Grids | Product features, dashboards, personal |
| 36 | Spatial UI (VisionOS) | Spatial computing apps, VR/AR |
| 37 | E-Ink / Paper | Reading apps, digital newspapers |
| 38 | Gen Z Chaos / Maximalism | Gen Z lifestyle, music artists |
| 39 | Biomimetic / Organic 2.0 | Sustainability tech, biotech, health |
| 40 | Anti-Polish / Raw Aesthetic | Creative portfolios, artist sites |
| 41 | Tactile Digital / Deformable UI | Modern mobile apps, playful brands |
| 42 | Nature Distilled | Wellness brands, sustainable products |
| 43 | Interactive Cursor Design | Creative portfolios, interactive |
| 44 | Voice-First Multimodal | Voice assistants, accessibility apps |
| 45 | 3D Product Preview | E-commerce, furniture, fashion |
| 46 | Gradient Mesh / Aurora Evolved | Hero sections, backgrounds, creative |
| 47 | Editorial Grid / Magazine | News sites, blogs, magazines |
| 48 | Chromatic Aberration / RGB Split | Music platforms, gaming, tech |
| 49 | Vintage Analog / Retro Film | Photography, music/vinyl brands |

### Landing Page Styles (8)

| # | Style Name | Best For |
|---|-----------|----------|
| 1 | Hero-Centric Design | Products with strong visual identity |
| 2 | Conversion-Optimized | Lead generation, sales pages |
| 3 | Feature-Rich Showcase | SaaS, complex products |
| 4 | Minimal & Direct | Simple products, apps |
| 5 | Social Proof-Focused | Services, B2C products |
| 6 | Interactive Product Demo | Software, tools |
| 7 | Trust & Authority | B2B, enterprise, consulting |
| 8 | Storytelling-Driven | Brands, agencies, nonprofits |

### BI/Analytics Dashboard Styles (10)

| # | Style Name | Best For |
|---|-----------|----------|
| 1 | Data-Dense Dashboard | Complex data analysis |
| 2 | Heat Map & Heatmap Style | Geographic/behavior data |
| 3 | Executive Dashboard | C-suite summaries |
| 4 | Real-Time Monitoring | Operations, DevOps |
| 5 | Drill-Down Analytics | Detailed exploration |
| 6 | Comparative Analysis Dashboard | Side-by-side comparisons |
| 7 | Predictive Analytics | Forecasting, ML insights |
| 8 | User Behavior Analytics | UX research, product analytics |
| 9 | Financial Dashboard | Finance, accounting |
| 10 | Sales Intelligence Dashboard | Sales teams, CRM |

---

## Industry Categories — Design System Reasoning

Use this table to guide style selection, color palette mood, and typography tone for each industry.

| Sector | Product Types |
|--------|--------------|
| **Tech & SaaS** | SaaS, Micro SaaS, B2B Service, Developer Tool, AI/Chatbot Platform, Cybersecurity |
| **Finance** | Fintech/Crypto, Banking, Insurance, Personal Finance Tracker, Invoice & Billing |
| **Healthcare** | Medical Clinic, Pharmacy, Dental, Veterinary, Mental Health |
| **E-commerce** | General, Luxury, Marketplace (P2P), Subscription Box, Food Delivery |
| **Services** | Beauty/Spa, Restaurant, Hotel, Legal, Home Services, Booking & Appointment |
| **Creative** | Portfolio, Agency, Photography, Gaming, Music Streaming |
| **Lifestyle** | Habit Tracker, Recipe & Cooking, Meditation, Weather, Diary, Mood Tracker |

**Industry → Style guidance:**
- **Tech & SaaS**: Prefer Minimalism, Glassmorphism, AI-Native UI, Bento Box Grid, or Soft UI Evolution.
- **Finance**: Prefer Minimalism, Accessible & Ethical, Dimensional Layering, or Glassmorphism. Avoid playful/chaotic styles.
- **Healthcare**: Prefer Accessible & Ethical, Inclusive Design, Flat Design, or Soft UI Evolution. Accessibility rules are non-negotiable.
- **E-commerce (General)**: Prefer Flat Design, Vibrant & Block-based, or Conversion-Optimized landing styles.
- **E-commerce (Luxury)**: Prefer Exaggerated Minimalism, Liquid Glass, or Vintage Analog.
- **Creative/Portfolio**: Prefer Brutalism, Neubrutalism, Anti-Polish, Kinetic Typography, or Parallax Storytelling.
- **Gaming**: Prefer Cyberpunk UI, HUD/Sci-Fi FUI, Retro-Futurism, Pixel Art, or 3D & Hyperrealism.
- **Wellness/Lifestyle**: Prefer Neumorphism, Organic Biophilic, Nature Distilled, or Claymorphism.
- **Dashboards/Analytics**: Prefer Data-Dense Dashboard, Executive Dashboard, or Bento Box Grid.

---

## Supported Tech Stacks

This skill generates design system output for the following tech stacks. Always adapt component syntax, class names, and patterns to the target stack:

| Category | Stacks |
|----------|--------|
| **Web (React ecosystem)** | React, Next.js, Astro |
| **Web (Vue ecosystem)** | Vue, Nuxt.js, Nuxt UI |
| **Web (Other)** | Svelte, Angular, HTML + Tailwind CSS |
| **Component libraries** | shadcn/ui, Nuxt UI |
| **Mobile (iOS)** | SwiftUI |
| **Mobile (Cross-platform)** | React Native, Flutter |
| **Mobile (Android)** | Jetpack Compose |
| **Backend-driven** | Laravel (Blade + Alpine.js / Livewire) |

**Stack-specific notes:**
- **shadcn/ui**: Use CSS variables for theming; follow the `cn()` utility pattern; use Radix UI primitives for accessibility.
- **Flutter**: Use `ThemeData` for design tokens; prefer `Material 3` color scheme; use `MediaQuery` for responsive breakpoints.
- **SwiftUI**: Follow iOS HIG; use `@Environment(\.colorScheme)` for dark mode; use `safeAreaInsets` for safe areas.
- **Tailwind CSS**: Define custom tokens in `tailwind.config.js`; use `@layer components` for reusable patterns.

---

## Pre-Delivery Checklist

Run this checklist before presenting any UI output. Every item must pass.

### Icons & Visual Language
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons come from a consistent icon family and style

### Interactivity
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150–300ms)
- [ ] All tappable elements provide clear pressed feedback

### Accessibility
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard nav
- [ ] `prefers-reduced-motion` respected
- [ ] Screen reader focus order matches visual order

### Responsive Layout
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile
- [ ] Safe areas respected (notch, gesture bar)
- [ ] Viewport meta tag present and correct

### Touch & Mobile
- [ ] Touch targets ≥44×44pt (iOS) / 48×48dp (Android)
- [ ] Safe areas respected (notch, gesture bar)

### Dark Mode
- [ ] Both light and dark mode tested (if dark mode is in scope)

---

## Design System Output Template

When generating a design system, structure the output as follows:

```
## Design System: [Product Name]

### Style
- **UI Style**: [chosen style from the 67 styles]
- **Rationale**: [1–2 sentences explaining why this style fits the product]

### Color Tokens
- `--color-primary`: #...
- `--color-secondary`: #...
- `--color-surface`: #...
- `--color-surface-elevated`: #...
- `--color-error`: #...
- `--color-success`: #...
- `--color-warning`: #...
- `--color-text`: #...
- `--color-text-muted`: #...
- `--color-border`: #...

### Typography
- **Heading font**: [font name] — [weight range]
- **Body font**: [font name] — [weight range]
- **Type scale**: 12 / 14 / 16 / 18 / 24 / 32 / 48px

### Spacing Scale
4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96px

### Border Radius
- Small: 4px (inputs, tags)
- Medium: 8px (cards, buttons)
- Large: 16px (modals, sheets)
- Full: 9999px (pills, avatars)

### Shadows
- Subtle: 0 1px 3px rgba(0,0,0,0.08)
- Card: 0 4px 12px rgba(0,0,0,0.10)
- Elevated: 0 8px 24px rgba(0,0,0,0.14)

### Component Notes
[Key component patterns for the chosen stack]
```

---

## Full Python-Powered Version

This bundled skill is a self-contained distillation of the upstream **UI UX Pro Max** skill. The full version includes:

- **161 color palettes** with industry-specific recommendations (CSV data)
- **57 font pairings** with personality tags (CSV data)
- **25 chart types** with data-type matching rules (CSV data)
- **Python-powered design system generator** (`search.py`) that queries the CSV data to produce tailored recommendations
- **Automated style matching** based on product type + industry + audience inputs

The full Python-powered version is available at:
**https://github.com/nextlevelbuilder/ui-ux-pro-max-skill** (v2.5.0, MIT License, by NextLevelBuilder)

To use the full version, clone that repository and follow its setup instructions. The bundled skill above covers the core design intelligence and all 99 UX guidelines without requiring Python or CSV data files.
