---
name: build-ui
description: Build new UI components, pages, layouts, or full apps using real-world design systems. Use this skill whenever the user wants to create UI inspired by a specific brand or website (Apple, Stripe, Airbnb, Linear, Vercel, Tesla, Figma, Notion, Spotify, and 49 more), asks to "make it look like [brand]", wants a landing page, dashboard, or component in a particular style, or mentions DESIGN.md files. Also trigger when the user wants pixel-perfect UI matching a known brand's visual language, wants to build "in the style of" a company, or references any design system from the awesome-design-md collection — even if they don't explicitly mention design systems.
---

# Build UI from Design System

Generate new UI components, pages, or full layouts that precisely match a real-world brand's design system. This skill reads curated DESIGN.md files containing exact color palettes, typography hierarchies, component specs, shadow systems, and layout rules extracted from 58 production websites.

## Why this matters

DESIGN.md files capture the complete visual DNA of a brand — not just colors and fonts, but the philosophy, spacing rhythm, shadow approach, and guardrails that make a design system feel cohesive. Using these specs produces UI that looks intentionally designed rather than generically themed.

## Available Designs

Read the catalog at `design-md/_index.md` to see all 58 available design systems with their category, theme, accent color, and key characteristics. Use this to help the user choose a design if they haven't specified one, or to confirm you're loading the right one.

## Workflow

### 1. Identify the target design

If the user named a brand (e.g., "build me a Stripe-style pricing page"), match it against the catalog. If they described a vibe instead (e.g., "dark, minimal, developer-focused"), read the catalog and suggest 2-3 matching designs with their key characteristics.

If the user wants to use a `DESIGN.md` already in their project root, read that file directly instead of the catalog.

### 2. Load the design system

Read `design-md/{directory}/DESIGN.md` where `{directory}` matches the catalog entry. This file contains all 9 sections you need:

| Section | What you extract |
|---------|-----------------|
| 1. Visual Theme & Atmosphere | Overall mood, density, design philosophy — sets the tone for everything |
| 2. Color Palette & Roles | Exact hex values with semantic roles (primary, accent, surface, text hierarchy) |
| 3. Typography Rules | Font families, complete size/weight/line-height/letter-spacing hierarchy table |
| 4. Component Stylings | Button variants with states, cards, inputs, nav — with exact specs |
| 5. Layout Principles | Spacing scale, grid system, container widths, whitespace philosophy |
| 6. Depth & Elevation | Shadow definitions, surface hierarchy levels, elevation approach |
| 7. Do's and Don'ts | Guardrails — things to always do and things to never do |
| 8. Responsive Behavior | Breakpoints, touch targets, collapsing strategy |
| 9. Agent Prompt Guide | Quick color reference and ready-to-use component prompts |

### 3. Confirm scope with the user

Ask what to build if not already clear:
- **Page types**: Landing page, pricing page, dashboard, settings page, docs page, blog, portfolio
- **Components**: Navigation bar, hero section, feature grid, pricing cards, footer, form, modal, sidebar
- **Full app shell**: Complete layout with nav + content + sidebar

### 4. Determine the tech stack

Ask about the target framework if not obvious from the project context:
- **HTML + CSS**: Pure semantic HTML with vanilla CSS custom properties
- **React + Tailwind**: JSX components with Tailwind utility classes
- **React + CSS Modules**: JSX with scoped CSS
- **Vue / Svelte / Other**: Adapt to their framework's conventions
- **CSS-only**: Just the stylesheet, no markup

If the project already has a framework set up, match it. Don't ask if the answer is obvious from existing files.

### 5. Generate the UI

Apply each section of the DESIGN.md systematically. This is the critical step — don't skip any section.

**Colors** (Section 2): Use the exact hex values from the palette. Map semantic roles correctly:
- Primary backgrounds and surfaces
- Text hierarchy (heading color vs body color vs secondary text)
- Interactive states (default, hover, active, focus)
- Accent colors for CTAs and highlights

**Typography** (Section 3): Match the hierarchy table precisely:
- Use the specified font families (include proper fallback stacks)
- Match sizes, weights, line-heights, and letter-spacing for each role
- Apply the right font to the right role (display font for headlines, body font for text)

**Components** (Section 4): Build components matching the documented specs:
- Button variants with all states (default, hover, active, disabled)
- Card styles with proper border, shadow, radius, and padding
- Input styling matching the documented approach
- Navigation matching the documented pattern

**Layout** (Section 5): Follow the spacing system:
- Use the documented spacing scale (base unit and multipliers)
- Apply the grid/container approach (max-width, gutters, columns)
- Respect the whitespace philosophy (generous vs compact)

**Depth** (Section 6): Apply the shadow system:
- Use exact shadow values from the depth documentation
- Apply the right elevation level to each element
- Follow the surface hierarchy

**Responsive** (Section 8): Implement the breakpoint system:
- Use documented breakpoints
- Follow the collapsing strategy
- Apply touch target sizes for mobile

**Guardrails** (Section 7): Check your output against the Do's and Don'ts:
- Verify you're following the "always do" rules
- Verify you're not violating the "never do" rules

### 6. Quality verification

Before presenting the result, verify:

- [ ] All color hex values match the DESIGN.md exactly (no approximations)
- [ ] Typography uses correct font families, sizes, weights, line-heights, and letter-spacing
- [ ] Shadows match the documented shadow system (exact values)
- [ ] Border-radius follows the documented scale
- [ ] Spacing follows the documented scale
- [ ] Component states (hover, active, focus, disabled) are implemented
- [ ] No guardrails from Section 7 are violated
- [ ] The overall atmosphere matches Section 1's description

### 7. Present the result

Output complete, ready-to-use code. Include:
- All necessary HTML/JSX markup
- Complete styling (CSS, Tailwind classes, or styled-components)
- Comments noting which design tokens are applied where (e.g., `/* Stripe Purple #533afd */`)
- Font import statements or links where applicable
- Brief note on how to preview the result

## Tips for better results

- Start with Section 9 (Agent Prompt Guide) for a quick-reference summary before diving into other sections
- When in doubt about a value, prefer the exact documented spec over your general knowledge of the brand
- Pay special attention to letter-spacing — it's the most commonly missed detail and has a huge impact on feel
- Shadow colors are often brand-tinted (e.g., Stripe uses blue-tinted shadows) — don't default to generic black shadows
- The Do's and Don'ts section often contains the most important differentiators between "looks like the brand" and "looks generic"
