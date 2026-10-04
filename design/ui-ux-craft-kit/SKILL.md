---
name: ui-ux-craft-kit
description: "UI/UX design intelligence for web and mobile. Includes 50+ styles, 161 color palettes, 57 font pairings, 161 product types, 99 UX guidelines, and 25 chart types across 10 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, and HTML/CSS). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, and check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, and mobile app. Elements: button, modal, navbar, sidebar, card, table, form, and chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, and flat design. Topics: color systems, accessibility, animation, layout, typography, font pairing, spacing, interaction states, shadow, and gradient."
---

# UI/UX CraftKit — Design Intelligence

Comprehensive design guide for web and mobile applications. Contains 50+ styles, 161 color palettes, 57 font pairings, 161 product types with reasoning rules, 99 UX guidelines, and 25 chart types across 10 technology stacks. Searchable database with priority-based recommendations.

Open source on GitHub: [github.com/hardikamal/ui-ux-craft-kit](https://github.com/hardikamal/ui-ux-craft-kit)

## Search Command

```bash
python3 <skill_dir>/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

Replace `<skill_dir>` with the absolute path to this skill directory.

**Domains:**
- `product` — Product type recommendations (SaaS, e-commerce, portfolio)
- `style` — UI styles (glassmorphism, minimalism, brutalism) + AI prompts
- `typography` — Font pairings with Google Fonts imports
- `color` — Color palettes by product type
- `landing` — Page structure and CTA strategies
- `chart` — Chart types and library recommendations
- `ux` — Best practices and anti-patterns
- `icons` — Icon library recommendations
- `react` — React/Next.js performance guidelines
- `web` — Web accessibility and interface patterns
- `google-fonts` — Google Fonts search

**Stack-specific search:**
```bash
python3 <skill_dir>/scripts/search.py "<query>" --stack react-native
```

**Design system generation:**
```bash
python3 <skill_dir>/scripts/search.py "<query>" --design-system [-p "Project Name"]
```

## When to Apply

Use this skill when the task involves **UI structure, visual design decisions, interaction patterns, or user experience quality control**.

### Must Use

- Designing new pages (Landing Page, Dashboard, Admin, SaaS, Mobile App)
- Creating or refactoring UI components (buttons, modals, forms, tables, charts)
- Choosing color schemes, typography systems, spacing standards, or layout systems
- Reviewing UI code for accessibility or visual consistency
- Implementing navigation structures, animations, or responsive behavior
- Making product-level design decisions (style, information hierarchy, brand)
- Improving perceived quality, clarity, or usability of interfaces

### Skip

- Pure backend logic development
- API or database design only
- Performance optimization unrelated to the interface
- Infrastructure or DevOps work

**Rule**: If the task changes how a feature **looks, feels, moves, or is interacted with** → use this skill.

## How to Use (Step by Step)

### Step 1: Identify the Task Domain
Run a search to get relevant design context before generating UI code:

```bash
# Get style recommendations for a product type
python3 <skill_dir>/scripts/search.py "SaaS dashboard" --domain product

# Get color palette
python3 <skill_dir>/scripts/search.py "fintech app" --domain color

# Get font pairing
python3 <skill_dir>/scripts/search.py "modern minimal" --domain typography

# Generate a full design system
python3 <skill_dir>/scripts/search.py "fitness tracking app" --design-system -p "FitTrack"
```

### Step 2: Apply Results
Use the search results to inform your design decisions. The search returns prioritized, ranked results from the database.

### Step 3: Quality Check Against Priority Rules

| Priority | Category | Key Checks |
|----------|----------|------------|
| 1 | Accessibility | Contrast 4.5:1, Alt text, Keyboard nav, Aria-labels |
| 2 | Touch & Interaction | Min 44×44px targets, Loading feedback |
| 3 | Performance | WebP/AVIF, Lazy loading, CLS < 0.1 |
| 4 | Style Selection | Match product type, Consistency, SVG icons |
| 5 | Layout & Responsive | Mobile-first, No horizontal scroll |
| 6 | Typography & Color | Base 16px, Line-height 1.5, Semantic tokens |
| 7 | Animation | 150–300ms duration, transform/opacity only |
| 8 | Forms & Feedback | Visible labels, Error near field |
| 9 | Navigation | Predictable back, Bottom nav ≤5 items |
| 10 | Charts & Data | Legends, Tooltips, Accessible colors |

## Quick Reference

### Accessibility (CRITICAL)
- Minimum 4.5:1 contrast ratio for normal text
- Visible focus rings on all interactive elements
- Descriptive alt text for meaningful images
- aria-labels for icon-only buttons
- Tab order matches visual order
- Support `prefers-reduced-motion`

### Touch & Interaction (CRITICAL)
- Min 44×44pt (Apple) / 48×48dp (Material) touch targets
- Minimum 8px gap between touch targets
- Use click/tap for primary interactions, not hover-only
- Disable button + show spinner during async operations
- Add `cursor-pointer` to clickable elements

### Performance (HIGH)
- Use WebP/AVIF + responsive `srcset`
- Declare `width`/`height` to prevent CLS
- `font-display: swap` to avoid FOIT
- Lazy load below-fold images
- Virtualize lists with 50+ items

### Style Selection (HIGH)
- Match style to product type (run `--domain product`)
- Use SVG icons (Heroicons, Lucide) — never emoji as icons
- One icon set/visual language across the product
- Each screen has only one primary CTA

### Layout & Responsive (HIGH)
- `width=device-width, initial-scale=1` viewport meta
- Design mobile-first: 375 → 768 → 1024 → 1440
- No horizontal scroll on mobile
- Use 4pt/8dp spacing scale
- `min-h-dvh` instead of `100vh` on mobile

### Typography & Color (MEDIUM)
- Minimum 16px body text (avoids iOS auto-zoom)
- Line height 1.5–1.75 for body text
- 65–75 chars per line on desktop
- Use semantic color tokens, not raw hex in components
- Bold headings (600–700), Regular body (400), Medium labels (500)

### Animation (MEDIUM)
- 150–300ms for micro-interactions
- Use `transform`/`opacity` only — never animate `width`/`height`
- Respect `prefers-reduced-motion`
- Exit animations 60–70% of enter duration
- Every animation must convey meaning, not just decoration

### Forms & Feedback (MEDIUM)
- Visible label per input (not placeholder-only)
- Show error below the related field
- Validate on blur, not keystroke
- Confirm before destructive actions
- Auto-dismiss toasts in 3–5s

### Navigation (HIGH)
- Bottom nav max 5 items with labels
- Back navigation must be predictable
- All key screens reachable via deep link
- State preservation when navigating back

### Charts & Data (LOW)
- Match chart type to data type (trend → line, comparison → bar)
- Always show legend near chart
- Provide tooltips on hover/tap
- Use accessible color palettes (not red/green only)
