---
name: create-design-md
description: Create a new DESIGN.md file for any website, app, or custom design system. Use when the user wants to document a design system in DESIGN.md format, extract design tokens from a URL or existing CSS, create a custom design system from scratch, author a DESIGN.md for their own project, or contribute a new design to the awesome-design-md collection. Also trigger when user mentions "design system documentation", wants to formalize their app's visual language, or asks to create or generate a DESIGN.md file.
---

# Create a DESIGN.md File

Author a complete DESIGN.md file — the plain-text design system format that AI agents read to generate consistent UI. This skill guides through creating all 9 required sections with proper structure, ensuring the output matches the quality of the 58 existing files in the collection.

## What is DESIGN.md?

DESIGN.md is a concept from Google Stitch — a markdown design system document optimized for LLM comprehension. It captures the complete visual DNA of a website or app: colors, typography, components, spacing, shadows, and design philosophy. Drop it in a project root and any AI coding agent instantly understands how the UI should look.

## The 9-section format

Every DESIGN.md follows this structure. All 9 sections are required for a complete file.

### Section 1: Visual Theme & Atmosphere
The opening narrative. Describe the design philosophy, visual mood, density, and key characteristics. This is prose, not specs — it tells the reader what the design *feels* like and why it works.

Include:
- Overall mood and philosophy (e.g., "cinematic reductionism", "warm editorial minimalism")
- Typography personality and approach
- Color story and emotional tone
- Key visual characteristics as bullet points (8-10 items with specific values)

### Section 2: Color Palette & Roles
Every color with its hex value, CSS variable name (if known), and functional role. Group by purpose:

- **Primary**: Brand colors, main backgrounds, key text colors
- **Interactive**: Link colors, CTA backgrounds, hover states, focus rings
- **Text hierarchy**: Heading, body, secondary, muted, disabled
- **Surface & borders**: Card backgrounds, dividers, border colors
- **Shadows**: Shadow colors with rgba values
- **Status colors**: Success, warning, error (if present)

Format: `**Color Name** (\`#hex\`): Description of when and how to use it.`

### Section 3: Typography Rules
Font families with fallback stacks, then a complete hierarchy table:

| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|------|--------|-------------|----------------|-------|
| Display Hero | ... | ...px | ... | ... | ... | When to use |
| Section Heading | ... | ... | ... | ... | ... | ... |
| Body | ... | ... | ... | ... | ... | ... |
| Caption | ... | ... | ... | ... | ... | ... |

Include at least: Display, Heading, Sub-heading, Body, Button, Caption, Micro. Add notes about OpenType features, variable font axes, or font-display strategy if relevant.

### Section 4: Component Stylings
Detailed specs for each component with all states:

- **Buttons**: Primary, secondary, ghost/outline variants. Each with: background, text color, border, padding, radius, and states (hover, active, disabled, focus)
- **Cards/Containers**: Border treatment, shadow, radius, padding, background
- **Inputs/Forms**: Border style, focus ring, padding, placeholder color, error state
- **Navigation**: Layout, active state, hover state, mobile behavior
- **Distinctive components**: Anything unique to this design (e.g., pill badges, gradient borders)

### Section 5: Layout Principles
- Spacing system: base unit and scale (e.g., 4px base with 4/8/12/16/24/32/48/64)
- Grid: columns, container max-width, gutters
- Whitespace philosophy (generous vs compact)
- Border-radius scale

### Section 6: Depth & Elevation
- Shadow definitions for each level (low, medium, high elevation)
- Surface hierarchy (how surfaces layer)
- Any special depth effects (glassmorphism, gradients, overlays)

### Section 7: Do's and Don'ts
Design guardrails:
- **Do**: 5-8 rules to always follow
- **Don't**: 5-8 anti-patterns to avoid
These are the brand differentiators — the rules that make the design feel intentional.

### Section 8: Responsive Behavior
- Breakpoints with pixel values
- Touch target sizes for mobile
- Collapsing strategy (how complex layouts simplify)
- Font size adjustments per breakpoint

### Section 9: Agent Prompt Guide
Quick-reference summary for fast component generation:
- Quick color reference (5-6 key colors)
- Ready-to-use component prompts (3-4 examples showing how to instruct an agent)
- Iteration guidance (common adjustments and refinements)

## Workflow

### 1. Determine the source

Ask the user where the design data comes from:

**From a live website**: The user provides a URL. Extract design tokens by analyzing the site's CSS, computed styles, and visual patterns. Note: you may need web access to fetch the site.

**From existing CSS/code**: The user has CSS files, Tailwind config, theme objects, or design token files. Extract and restructure into DESIGN.md format.

**From scratch**: The user describes the design they want. Generate a complete, internally consistent design system based on their description.

**From visual reference**: The user describes a mood or references existing brands. Create an original design system inspired by (but not copying) the reference.

### 2. Load a format reference

Read an existing DESIGN.md to calibrate the expected quality and format. Good references:
- `design-md/stripe/DESIGN.md` — comprehensive, well-structured, rich detail
- `design-md/apple/DESIGN.md` — excellent typography documentation
- `design-md/claude/DESIGN.md` — warm, editorial tone

Read one of these before writing to match the quality bar.

### 3. Draft all 9 sections

Write each section following the format above. For each section:
- Use specific values (hex codes, pixel sizes, weights) — never vague descriptions
- Include CSS variable names where known
- Write prose sections (1, 7) with personality — these aren't just data dumps
- The typography table must be complete with all columns filled

### 4. Validate completeness

Check the draft against this checklist:
- [ ] Section 1 has clear key characteristics bullet points
- [ ] Section 2 has all colors with hex values and functional roles
- [ ] Section 3 has font families with fallbacks AND a complete hierarchy table
- [ ] Section 4 has buttons with states, cards, inputs, and navigation
- [ ] Section 5 has a spacing scale with specific values
- [ ] Section 6 has shadow definitions with exact values
- [ ] Section 7 has at least 5 Do's and 5 Don'ts
- [ ] Section 8 has breakpoints with pixel values
- [ ] Section 9 has quick color reference and example prompts

### 5. Output the file

Write to `DESIGN.md` in the location the user specifies (default: project root).

The first line should be: `# Design System Inspiration of {Brand Name}`

### 6. Contributing to the collection

If the user wants to add this to the awesome-design-md repo:
1. Create a new directory under `design-md/{lowercase-name}/`
2. Place the `DESIGN.md` file there
3. Create a `README.md` with a brief description
4. Update `design-md/_index.md` with the new entry
5. Open a PR following the CONTRIBUTING.md guidelines
