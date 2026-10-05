---
name: ui-ux-pro-max
description: UI/UX design intelligence with searchable database
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ui-ux, design, style-guide, color-palette, typography, wireframe, prototype]
    triggers: [ui-ux, design-system, style-guide, color-palette, font-pairing, ux-guidelines, wireframe, mockup, prototype]
    related_skills: [sketch, pixel-art, excalidraw]
---
# ui-ux-pro-max

Comprehensive design guide for web and mobile applications. Contains 67 styles, 96 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 13 technology stacks. Searchable database with priority-based recommendations.

## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on user's OS:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## How to Use This Skill

When user requests UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Generate Design System (REQUIRED)

**Always start with `--design-system`** to get comprehensive recommendations with reasoning:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This command:
1. Searches 5 domains in parallel (product, style, color, landing, typography)
2. Applies reasoning rules from `ui-reasoning.csv` to select best matches
3. Returns complete design system: pattern, style, colors, typography, effects
4. Includes anti-patterns to avoid

**Example:**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System (Master + Overrides Pattern)

To save the design system for hierarchical retrieval across sessions, add `--persist`:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

This creates:
- `design-system/MASTER.md` — Global Source of Truth with all design rules
- `design-system/pages/` — Folder for page-specific overrides

**With page-specific override:**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

This also creates:
- `design-system/pages/dashboard.md` — Page-specific deviations from Master

**How hierarchical retrieval works:**
1. When building a specific page (e.g., "Checkout"), first check `design-system/pages/checkout.md`
2. If the page file exists, its rules **override** the Master file
3. If not, use `design-system/MASTER.md` exclusively

### Step 2c: Full Application Redesign (Next.js + Tailwind + shadcn)

When the user asks to redesign ALL pages of an existing application (not just build one new page), the single-python-command approach is insufficient. Use this multi-step orchestration pattern instead:

**Step 2c-i: Choose visual direction**
Load 1-2 templates from the `popular-web-designs` skill that match the app's domain. For dashboards: Linear, Vercel, Supabase, Sentry. For marketing pages: Stripe, Apple, Airbnb. Read the template's color palette, typography rules, component stylings, and layout principles.

**Step 2c-ii: Define design tokens directly (skip Python script)**
Write the design system into the framework's native config files, not a separate markdown file:
- `tailwind.config.ts` — extend theme with new colors (`primary`, `accent`, `muted`, `card`, `border`), box shadows (`shadow-card`, `shadow-card-hover`, `shadow-card-lg`), font families (Inter via next/font), border radii, and animations (fade-in, scale-in, slide-up)
- `app/globals.css` — HSL CSS custom properties for light and dark mode, `@layer base` with font-feature-settings and selection styling
- `app/layout.tsx` — Import Inter via `next/font/google`, apply `inter.variable` to `<html>`, set metadata and OG tags

Each of these changes the design at the framework level, making every shadcn/ui component automatically adopt the new look.

**Pitfall:** Do NOT use CSS `!important` overrides to restyle shadcn components. The CSS variable approach (hsl(--primary)) cascades correctly — shadcn's `cn()` utility resolves theme colors from CSS variables, not hardcoded classes. Overwriting component classes (like adding `rounded-lg` to every button) defeats the variable system.

**Step 2c-iii: Load design templates from popular-web-designs as context**
Before writing page code, load the chosen template(s) to extract concrete values:
- Exact hex/HSL color values for backgrounds, text, borders, accents
- Border radius scale (4px for buttons, 8px for cards, 9999px for pills)
- Shadow techniques (Vercel's shadow-as-border, Linear's luminance-stacking model)
- Typography weights and letter-spacing at different sizes
- Component patterns (glass headers, side navigation, card grids)

**Step 2c-iv: Rewrite pages in parallel using subagents**
Delegate each page rewrite to a subagent. Every subagent receives:
1. The design token reference (colors, spacing, shadows, radii)
2. The specific page's current code and what sections to preserve
3. Clear instructions to ONLY change JSX/styling, NEVER touch hooks/API/state logic
4. Exact mapping: old-class → new-class replacements (e.g. `bg-dh-cream` → `bg-background`, `rounded-none` → `rounded-lg`, `text-dh-charcoal-1` → `text-muted-foreground`)

Batch order: foundation files first (layout, globals, tailwind config), then batch 2-3 page rewrites in parallel, verify build, then batch remaining pages.

**Pitfall:** Legacy apps often have framework-wide overrides like `border-radius: 0 !important` on `button` elements in globals.css, or raw `border-slate-300` classes. These must be removed/replaced in the foundation phase, not per-page. A search for `rounded-none`, `!important`, and dh- legacy color classes across the codebase catches everything.

**Step 2c-v: Verify build after each batch**
Run `next build --no-lint` between batches to catch compilation errors early. Build failures are almost always:
- Missing imports (lucide icons renamed between versions)
- Old class references that don't exist in new tailwind config
- Mismatched string quotes from inline content updates

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**When to use detailed searches:**

| Need | Domain | Example |
|------|--------|---------|
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Alternative fonts | `typography` | `--domain typography "elegant luxury"` |
| Landing structure | `landing` | `--domain landing "hero social-proof"` |

### Step 3b: Apply Animation Patterns (when "smooth animations" or "level up" requested)

When the user asks for visual polish, smooth animations, or UI/UX refinement, load `references/web-animation-patterns.md` from this skill:

```bash
skill_view(name="ui-ux-pro-max", file_path="references/web-animation-patterns.md")
```

This reference documents 12 concrete animation patterns extracted from top-tier open-source projects (shadcn-ui, lobehub, open-webui, supabase). Each pattern includes copy-paste HTML/CSS/JS and explains when to use it:

| Pattern | Source | Best For |
|---------|--------|----------|
| Particle canvas | lobehub | Background atmosphere |
| Skeleton loading | shadcn-ui | Data-loading states |
| SVG progress rings | shadcn-ui | Confidence/rating indicators |
| Animated counting | supabase | Financial values, stats |
| Staggered entries | supabase | List reveals |
| Toast notifications | open-webui | User action feedback |
| Scroll reveal | lobehub | Below-fold sections |
| Confetti burst | custom | Milestone celebrations |
| Button micro-interactions | shadcn-ui | Click feedback |
| Card hover effects | shadcn-ui+supabase | Interactive elements |
| Live status dot | open-webui | Connection indicators |
| Gradient text | lobehub | Hero headings |

**Workflow:**
1. Load the reference file
2. Pick patterns matching the use case (data sections → skeleton + staggered; financial → animated counting; live dashboard → status dot + toast)
3. Implement each pattern following the code templates
4. Verify at 640px, 768px, and 1024px — hide canvas/motion on mobile

### Step 4: Stack Guidelines (Default: html-tailwind)

Get implementation-specific best practices. If user doesn't specify a stack, **default to `html-tailwind`**.

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | Page structure, CTA strategies | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel, pie |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | Web interface guidelines | aria, focus, keyboard, semantic, virtualize |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Available Stacks

| Stack | Focus |
|-------|-------|
| `html-tailwind` | Tailwind utilities, responsive, a11y (DEFAULT) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |
| `shadcn` | shadcn/ui components, theming, forms, patterns |
| `jetpack-compose` | Composables, Modifiers, State Hoisting, Recomposition |

---

## Example Workflow

**User request:** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp"

### Step 1: Analyze Requirements
- Product type: Beauty/Spa service
- Style keywords: elegant, professional, soft
- Industry: Beauty/Wellness
- Stack: html-tailwind (default)

### Step 2: Generate Design System (REQUIRED)

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Output:** Complete design system with pattern, style, colors, typography, effects, and anti-patterns.

### Step 3: Supplement with Detailed Searches (as needed)

```bash
# Get UX guidelines for animation and accessibility
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Get alternative typography options if needed
python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### Step 4: Stack Guidelines

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**Then:** Synthesize design system + detailed searches and implement the design.

---

## Output Formats

The `--design-system` flag supports two output formats:

```bash
# ASCII box (default) - best for terminal display
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - best for documentation
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## Tips for Better Results

1. **Be specific with keywords** - "healthcare SaaS dashboard" > "app"
2. **Search multiple times** - Different keywords reveal different insights
3. **Combine domains** - Style + Typography + Color = Complete design system
4. **Always check UX** - Search "animation", "z-index", "accessibility" for common issues
5. **Use stack flag** - Get implementation-specific best practices
6. **Iterate** - If first search doesn't match, try different keywords

---

## Common Rules for Professional UI

These are frequently overlooked issues that make UI look unprofessional:

### Icons & Visual Elements

| Rule | Do | Don't |
|------|----|----- |
| **No emoji icons** | Use SVG icons (Heroicons, Lucide, Simple Icons) | Use emojis like 🎨 🚀 ⚙️ as UI icons |
| **Stable hover states** | Use color/opacity transitions on hover | Use scale transforms that shift layout |
| **Correct brand logos** | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| **Consistent icon sizing** | Use fixed viewBox (24x24) with w-6 h-6 | Mix different icon sizes randomly |

### Interaction & Cursor

| Rule | Do | Don't |
|------|----|----- |
| **Cursor pointer** | Add `cursor-pointer` to all clickable/hoverable cards | Leave default cursor on interactive elements |
| **Hover feedback** | Provide visual feedback (color, shadow, border) | No indication element is interactive |
| **Smooth transitions** | Use `transition-colors duration-200` | Instant state changes or too slow (>500ms) |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|----|----- |
| **Glass card light mode** | Use `bg-white/80` or higher opacity | Use `bg-white/10` (too transparent) |
| **Text contrast light** | Use `#0F172A` (slate-900) for text | Use `#94A3B8` (slate-400) for body text |
| **Muted text light** | Use `#475569` (slate-600) minimum | Use gray-400 or lighter |
| **Border visibility** | Use `border-gray-200` in light mode | Use `border-white/10` (invisible) |

### Layout & Spacing

| Rule | Do | Don't |
|------|----|----- |
| **Floating navbar** | Add `top-4 left-4 right-4` spacing | Stick navbar to `top-0 left-0 right-0` |
| **Content padding** | Account for fixed navbar height | Let content hide behind fixed elements |
| **Consistent max-width** | Use same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

---

## Pre-Delivery Checklist

Before delivering UI code, verify these items:

### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Brand logos are correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] Use theme colors directly (bg-primary) not var() wrapper

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode
- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery

### Layout
- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
