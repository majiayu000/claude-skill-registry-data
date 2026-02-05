---
name: figma-design-analyzer
description: Extract and analyze Figma designs to create structured design specifications. Use this skill when you need to analyze Figma nodes, extract design properties (layout, spacing, typography), classify components using Atomic Design principles, and generate design specification documents that can be used for implementation.
---

# Figma Design Analyzer

## Overview

Systematically analyze Figma designs and extract structured design specifications. This skill focuses on understanding design intent, extracting accurate properties, and creating comprehensive design specification documents that serve as blueprints for implementation.

**Use this skill when:**
- Analyzing Figma designs to understand structure and properties
- Extracting design tokens and component specifications
- Classifying components according to Atomic Design principles
- Creating design specification documents for developers
- Comparing existing implementations with Figma designs

## Core Workflow

### Step 1: Extract Figma Design Information

When given a Figma URL or node ID, use Figma MCP tools to extract design data:

1. **Parse the Figma URL to extract node ID:**
   ```
   URL: https://figma.com/design/fileKey/fileName?node-id=1-2
   Node ID: 1:2 (replace - with :)
   ```

2. **Extract node design context:**
   ```
   mcp__figma-dev__get_design_context(
     nodeId: "1:2",
     dirForAssetWrites: "/absolute/path/to/project/public/assets",
     clientLanguages: "typescript",
     clientFrameworks: "react,nextjs"
   )
   ```
   This returns the design code, including HTML structure and CSS properties.

3. **Get component metadata for structure overview:**
   ```
   mcp__figma-dev__get_metadata(
     nodeId: "1:2",
     clientLanguages: "typescript",
     clientFrameworks: "react,nextjs"
   )
   ```
   Use this to understand the component hierarchy before detailed analysis.

4. **Check for Figma variables (design tokens):**
   ```
   mcp__figma-dev__get_variable_defs(
     nodeId: "1:2",
     clientLanguages: "typescript",
     clientFrameworks: "react,nextjs"
   )
   ```
   Extract design system tokens for colors, typography, spacing, etc.

5. **Verify Code Connect mappings:**
   ```
   mcp__figma-dev__get_code_connect_map(
     nodeId: "1:2",
     clientLanguages: "typescript",
     clientFrameworks: "react,nextjs"
   )
   ```
   Check if the component is already mapped to existing code.

### Step 2: Handle Component Instances and Variants

**Important:** When the node is a component instance:

1. **Identify if it's an instance:**
   - Check metadata for "component instance" type
   - Note the main component ID

2. **Get the main component:**
   - Use `get_design_context` on the main component node
   - Extract the base structure and properties

3. **Extract instance-specific properties:**
   - Get the instance's specific size, device, and variant settings
   - Note any overrides (text, images, colors, etc.)

4. **Handle variants:**
   - If the main component uses variants, identify the variant mode
   - Extract the correct variant values for the instance
   - Document variant properties for props mapping

### Step 3: Classify the Component

Use Atomic Design principles to classify the component:

1. **Read the classification guide:**
   ```
   Read references/atomic-design-classification.md
   ```

2. **Apply the decision tree:**
   - **Atom**: Indivisible, single purpose (button, input, icon, text label)
   - **Molecule**: 2-5 atoms, simple combination (search bar, form field)
   - **Organism**: Complex, multiple molecules/atoms (header, card, form)

3. **Determine the component category:**
   - Document: `atomicCategory: Atom | Molecule | Organism`

### Step 4: Analyze Layout and Spacing

Extract accurate layout information:

1. **Read layout analysis guide:**
   ```
   Read references/layout-analysis-guide.md
   ```

2. **Determine layout method:**
   - **Auto Layout** → Flexbox
     - Check: direction (row/column), justify-content, align-items
   - **Grid structure** → CSS Grid
     - Check: grid-template-columns, grid-template-rows, gap
   - **Overlapping elements** → Absolute positioning
     - Check: position, top, left, z-index

3. **Extract spacing values:**
   ```
   Read references/spacing-extraction-guide.md
   ```
   - **Padding**: Internal spacing (px, py, pt, pr, pb, pl)
   - **Gap**: Spacing between flex/grid items
   - **Margin**: External spacing (rarely used, prefer gap)

4. **Map to Tailwind classes:**
   - Use standard Tailwind scale when possible (p-4, gap-6, etc.)
   - Use arbitrary values `[value]` for custom sizes (p-[18px])

5. **Document in specification:**
   ```markdown
   ## Layout
   - Method: Flexbox
   - Direction: row
   - Justify: center
   - Align: center

   ## Spacing
   - Padding: px-6 py-3
   - Gap: gap-2
   - Border Radius: rounded-lg
   ```

### Step 5: Extract Typography

Extract accurate text styling:

1. **Read typography guide:**
   ```
   Read references/typography-extraction-guide.md
   ```

2. **Extract font properties:**
   - Font family (font-sans, font-serif, custom)
   - Font size (text-sm, text-base, text-lg, etc.)
   - Font weight (font-normal, font-semibold, font-bold)
   - Line height (leading-tight, leading-normal, etc.)
   - Letter spacing (tracking-tight, tracking-wide, etc.)
   - Text color (text-gray-900, text-white, etc.)
   - Text alignment (text-left, text-center, text-right)
   - Text decoration (underline, line-through)
   - Text transform (uppercase, lowercase, capitalize)

3. **Map to Tailwind classes:**
   - Use standard Tailwind typography classes
   - Check for design tokens in Figma variables
   - Use arbitrary values for custom sizes

4. **Document in specification:**
   ```markdown
   ## Typography
   - Font: text-base font-semibold
   - Color: text-white
   - Line Height: leading-normal
   - Alignment: text-center
   ```

### Step 6: Choose Semantic HTML

Select appropriate HTML elements:

1. **Read semantic HTML guide:**
   ```
   Read references/semantic-html-guide.md
   ```

2. **Apply semantic rules:**
   - **Sections**: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`
   - **Headings**: `<h1>` to `<h6>` (respect hierarchy)
   - **Interactive**: `<button>` for actions, `<a>` for navigation
   - **Content**: `<article>`, `<section>` for grouping
   - **Forms**: `<form>`, `<input>`, `<label>`, `<select>`, `<textarea>`
   - **Lists**: `<ul>`, `<ol>`, `<li>` for lists
   - **Media**: `<img>`, `<video>`, `<audio>`, `<figure>`, `<figcaption>`

3. **Consider accessibility:**
   - Add ARIA attributes when semantic HTML is insufficient
   - Ensure keyboard accessibility
   - Verify color contrast ratios

4. **Document in specification:**
   ```markdown
   ## Semantic HTML
   - Root Element: button
   - ARIA: role="button" aria-label="Submit"
   ```

### Step 7: Extract Colors and Visual Properties

Extract color and visual styling:

1. **Extract color properties:**
   - Background color (bg-blue-500, bg-gradient-to-r, etc.)
   - Text color (text-white, text-gray-900, etc.)
   - Border color (border-gray-300, etc.)

2. **Extract visual properties:**
   - Border radius (rounded, rounded-lg, rounded-full, etc.)
   - Border width (border, border-2, etc.)
   - Box shadow (shadow, shadow-md, shadow-lg, etc.)
   - Opacity (opacity-50, opacity-100, etc.)

3. **Check Figma variables:**
   - Look for design token mappings
   - Use semantic color names when available

4. **Document in specification:**
   ```markdown
   ## Colors
   - Background: bg-blue-500
   - Hover: hover:bg-blue-600
   - Text: text-white
   - Border: border-transparent

   ## Visual Properties
   - Border Radius: rounded-lg
   - Shadow: shadow-md
   ```

### Step 8: Handle Responsive Designs

When multiple Figma nodes represent different device sizes:

1. **Extract all node IDs** from provided URLs
   - Desktop node
   - Tablet node
   - Mobile node

2. **Analyze each node:**
   - Layout changes (grid columns, flex direction)
   - Spacing changes
   - Typography changes (font size, line height)
   - Hidden/shown elements

3. **Document responsive variations:**
   ```markdown
   ## Responsive Behavior
   - Mobile (default): flex-col gap-4 text-sm
   - Tablet (md): md:flex-row md:gap-6 md:text-base
   - Desktop (lg): lg:gap-8 lg:text-lg
   ```

### Step 9: Generate Design Specification Document

Create a comprehensive design specification:

1. **Use Markdown format with front matter:**
   ```markdown
   ---
   componentName: Button
   atomicCategory: Atom
   semanticElement: button
   figmaNodeId: "123:456"
   figmaUrl: "https://figma.com/design/..."
   ---

   # Button Component Specification

   ## Overview
   A primary action button component.

   ## Atomic Design Classification
   - Category: Atom
   - Reason: Single, indivisible interactive element

   ## Layout
   - Method: Flexbox
   - Direction: row
   - Justify: center
   - Align: center

   ## Spacing
   - Padding: px-6 py-3
   - Gap: gap-2
   - Border Radius: rounded-lg

   ## Typography
   - Font: text-base font-semibold
   - Color: text-white
   - Line Height: leading-normal
   - Alignment: text-center

   ## Colors
   - Background: bg-blue-500
   - Hover: hover:bg-blue-600
   - Active: active:bg-blue-700
   - Disabled: disabled:bg-gray-300

   ## Visual Properties
   - Border: border-transparent
   - Shadow: shadow-md
   - Transition: transition-colors duration-200

   ## Semantic HTML
   - Root Element: button
   - ARIA: aria-label when no text content

   ## Variants
   - variant: primary | secondary | tertiary
     - primary: bg-blue-500 text-white
     - secondary: bg-white text-blue-500 border-blue-500
     - tertiary: bg-transparent text-blue-500
   - size: small | medium | large
     - small: px-4 py-2 text-sm
     - medium: px-6 py-3 text-base
     - large: px-8 py-4 text-lg

   ## States
   - Default: As specified above
   - Hover: Darker background
   - Active: Even darker background
   - Disabled: Gray background, reduced opacity
   - Focus: Ring outline for keyboard navigation

   ## Responsive Behavior
   - Mobile: Full width, smaller padding
   - Tablet: Inline, medium padding
   - Desktop: Inline, larger padding

   ## Accessibility
   - Keyboard: Focusable, Enter/Space to activate
   - Screen Reader: Announced as "button"
   - Color Contrast: WCAG AA compliant

   ## Assets
   - Icons: /public/assets/icon-arrow.svg (if any)
   - Images: None

   ## Notes
   - Always use semantic <button> element
   - Avoid using <a> styled as button
   - Include loading state if used for async actions
   ```

2. **Save the specification:**
   - Filename: `{ComponentName}.design.md`
   - Location: `/design-specs/` or project-specific location

## Special Workflows

### Comparing Design with Implementation

When asked to compare an existing component with Figma:

1. **Read the existing component code**
2. **Extract Figma design properties** using MCP tools
3. **Compare systematically:**
   - Layout method (Flexbox, Grid, etc.)
   - Spacing values (padding, gap, margin)
   - Typography (font size, weight, line height, color)
   - Colors and backgrounds
   - Border radius, shadows, etc.
4. **Generate a diff report:**
   ```markdown
   ## Design Differences Report

   ### Component: Button

   #### Spacing
   - Design: px-6 py-3 gap-2
   - Implementation: px-4 py-2 gap-3
   - Status: ❌ Mismatch
   - Impact: Button appears smaller and less comfortable

   #### Typography
   - Design: text-base font-semibold
   - Implementation: text-base font-semibold
   - Status: ✅ Match

   #### Colors
   - Design: bg-blue-500 hover:bg-blue-600
   - Implementation: bg-blue-600 hover:bg-blue-700
   - Status: ❌ Mismatch
   - Impact: Button is darker than intended

   ### Recommendations
   1. Update padding to px-6 py-3
   2. Update gap to gap-2
   3. Update background colors to match design
   ```
5. **Document required changes** in the specification

### Breaking Down a Full Page

When given a full page Figma node:

1. **Get page metadata** to understand structure
2. **Identify major sections:**
   - Header
   - Hero
   - Content sections
   - Footer

3. **For each section:**
   - Classify as Organism
   - Identify child Molecules and Atoms
   - Extract design properties
   - Create individual specifications

4. **Create component tree:**
   ```
   Page (Template)
   ├─ Header (Organism)
   │  ├─ Logo (Atom)
   │  ├─ Navigation (Molecule)
   │  └─ UserMenu (Molecule)
   ├─ Hero (Organism)
   │  ├─ Heading (Atom)
   │  ├─ Paragraph (Atom)
   │  └─ CTAButton (Atom)
   ├─ Features (Organism)
   │  └─ FeatureCard (Molecule) × 3
   │     ├─ Icon (Atom)
   │     ├─ Title (Atom)
   │     └─ Description (Atom)
   └─ Footer (Organism)
      ├─ Logo (Atom)
      └─ Links (Molecule)
   ```

5. **Generate specifications from bottom-up:**
   - Create Atom specifications first
   - Build Molecule specifications
   - Assemble Organism specifications
   - Compose Page specification with assembly instructions

## Best Practices

1. **Always read guides before starting:**
   - Layout analysis guide for layout decisions
   - Spacing guide for accurate spacing extraction
   - Typography guide for text styling
   - Atomic Design guide for classification
   - Semantic HTML guide for element selection

2. **Prioritize pixel-perfect accuracy:**
   - Use exact spacing values from Figma
   - Match typography precisely
   - Verify colors match design tokens

3. **Document thoroughly:**
   - Include all variants and states
   - Document responsive behavior
   - Note accessibility considerations
   - Include designer notes if available

4. **Consider implementation:**
   - Map to Tailwind classes for easy implementation
   - Document component hierarchy
   - Note any complex interactions

5. **Maintain consistency:**
   - Use consistent naming conventions
   - Follow project-specific patterns
   - Align with design system when available

## Resources

This skill includes comprehensive guides:

### references/

- **layout-analysis-guide.md**: Criteria for choosing Flexbox, Grid, absolute positioning
- **spacing-extraction-guide.md**: Methods for extracting padding, gap, margin values
- **typography-extraction-guide.md**: Guide for extracting font properties
- **atomic-design-classification.md**: Classification criteria for Atoms, Molecules, Organisms
- **semantic-html-guide.md**: Recommendations for choosing appropriate HTML elements

**Usage:** Always read relevant guides before starting analysis to ensure accuracy.

## Common Pitfalls

1. **Not handling component instances properly:**
   - Always get the main component when working with instances
   - Extract instance-specific properties separately

2. **Ignoring variants:**
   - Check for variant properties in Figma
   - Document all variant options

3. **Using wrong layout method:**
   - Read the layout guide
   - Don't default to Flexbox for everything

4. **Skipping semantic HTML:**
   - Don't use `<div>` for everything
   - Consider accessibility and SEO

5. **Forgetting responsive behavior:**
   - Check for responsive variants in Figma
   - Document breakpoint changes

6. **Not checking existing code:**
   - Always check Code Connect mappings
   - Avoid duplicating existing specifications

## Output Format

The final output should be a Markdown document with:

1. **Front matter** with metadata
2. **Overview** section
3. **Design properties** organized by category
4. **Variants and states** documentation
5. **Responsive behavior** notes
6. **Accessibility** considerations
7. **Assets** references
8. **Implementation notes**

This specification document will be used by the `nextjs-react-implementation` skill to generate actual code.

---

**This skill systematically analyzes Figma designs and creates structured specifications for accurate implementation.**
