---
name: figma-design-extraction
description: |
  Complete Figma design extraction for pixel-perfect implementation.
  Extracts design tokens, component specs, layouts, and responsive behavior systematically.

  Use when user provides Figma design:
  - Figma URL or file link provided
  - User mentions "Figma", "design file", "mockup", or "design system"
  - During /create-plan phase when design needs extraction
  - User says "extract from Figma" or references Figma link

  Extract systematically:
  - Design tokens: ALL colors (hex + usage), typography (sizes, weights, line heights),
    spacing scale, border radius, shadows, opacity values
  - Components: ALL states (default, hover, active, focus, disabled, loading, error),
    ALL variants (size/style/intent), exact dimensions, spacing, visual properties
  - Layouts: page structure, grid systems (columns, gutters), component hierarchy
  - Responsive: mobile/tablet/desktop differences explicitly documented
  - Assets: icons (names, sizes), images (dimensions, alt text), illustrations

  Goal: Extract ONCE completely during planning phase. Implementation should never
  need to re-fetch from Figma MCP. Focus on exact values only - no approximations,
  no guessing. Completeness prevents re-work and design inconsistencies.

  Critical for /create-plan workflow. Validates MCP connection before extraction.
  Documents everything in structured format for /execute-plan to implement accurately.

  Do NOT load for: Building UI without design (use theme-factory), implementing
  from already-extracted specs, responsive layout questions, or backend work.
---

# Figma Design Extraction

## Purpose
Extract complete design specifications from Figma MCP once during planning to enable accurate implementation without re-fetching.

---

## Core Principle

**Extract everything once, implement accurately forever.**

The goal is to capture ALL design information during `/create-plan` so that `/execute-plan` never needs to access Figma MCP again. Complete extraction prevents:
- Implementation guesswork
- Design inconsistencies
- Re-fetching during coding
- Context loss from incomplete specs

---

## Pre-Extraction Validation

### Check MCP Connection

**Before extraction, verify**:
1. Figma MCP server is available and responding
2. Authentication is valid
3. Can access the specific file/frame
4. User has read permissions

**If validation fails**:
- Inform user: "Figma MCP connection failed. Options: 1) Fix connection, 2) Provide design specs manually, 3) Continue without design"
- Do NOT proceed with incomplete extraction
- Do NOT assume or guess design values

### Identify Extraction Scope

**Ask user to clarify** (if not obvious):
- Which Figma file? (URL or file key)
- Which frame(s)? (specific page/frame name)
- What device sizes? (mobile/tablet/desktop frames)
- Any specific components to focus on?

**Why**: Prevents extracting irrelevant designs or missing critical frames.

---

## What to Extract

### 1. Design Tokens (Foundation)

**Colors** - Extract ALL colors used:
- Primary palette (with shades: 50, 100, 200...900)
- Secondary/accent colors
- Neutral/gray scale
- Semantic colors (success, warning, error, info)
- Text colors (heading, body, caption, disabled)
- Background colors
- Border colors

**Document format**:
```
Primary-500: #3b82f6 (Usage: buttons, links, primary actions)
Primary-600: #2563eb (Usage: button hover state)
Neutral-700: #374151 (Usage: body text)
Error-500: #ef4444 (Usage: error messages, destructive actions)
```

**Typography** - Extract ALL text styles:
- Font families (with fallbacks)
- All font sizes used
- Font weights
- Line heights
- Letter spacing (if significant)

**Document format**:
```
Heading-1: Inter, 32px, 700 (bold), 40px line-height
Body: Inter, 16px, 400 (regular), 24px line-height
Caption: Inter, 14px, 400 (regular), 20px line-height
```

**Spacing System**:
- Identify spacing scale (e.g., 4, 8, 16, 24, 32, 48, 64px)
- Note padding/margin patterns
- Document container widths

**Other Tokens**:
- Border radius values
- Shadow definitions (elevation system)
- Opacity values (if used systematically)
- Transition durations (if specified)

---

### 2. Component Specifications

**For EACH interactive component**:

**States** - Document all states:
- Default (resting state)
- Hover (mouse over)
- Active (pressed/clicked)
- Focus (keyboard navigation)
- Disabled (non-interactive)
- Loading (async operations)
- Error (validation failure)
- Success (validation pass)

**Variants** - Document all variants:
- Size variants (small, medium, large)
- Style variants (primary, secondary, outline, ghost, link)
- Intent variants (default, success, warning, error)

**Dimensions**:
- Width (fixed, min-width, max-width, or responsive)
- Height (fixed or min/max)
- Aspect ratios (for images/media)

**Spacing**:
- Padding (all sides or specific)
- Margins/gaps (between elements)
- Internal spacing (icon to text gap, etc.)

**Visual Properties**:
- Background colors (per state/variant)
- Text colors (per state/variant)
- Border (width, style, color, radius)
- Shadows (per state if different)
- Icons (names, sizes, colors)

**Example documentation**:
```
Button Component (figma-id: abc123)

States: default, hover, active, disabled, loading
Variants: primary, secondary, outline

Primary Variant - Default State:
- Dimensions: auto width (min 120px), 44px height
- Padding: 12px vertical, 24px horizontal
- Background: Primary-500 (#3b82f6)
- Text: White (#ffffff), Body-Bold (Inter 16px 600)
- Border: none
- Border radius: 8px
- Shadow: sm (0 1px 2px rgba(0,0,0,0.05))
- Icon: (if present) 20px, 8px gap to text

Primary Variant - Hover State:
- Background: Primary-600 (#2563eb)
- Shadow: md (0 4px 6px rgba(0,0,0,0.1))
- (Other props same as default)

Primary Variant - Disabled State:
- Background: Neutral-200 (#e5e7eb)
- Text: Neutral-400 (#9ca3af)
- Cursor: not-allowed
- (Other props same as default)
```

---

### 3. Layout Specifications

**Page Structure**:
- Overall layout (header, main, sidebar, footer)
- Container max-widths
- Sections and their purposes
- Navigation patterns

**Grid Systems**:
- Number of columns (e.g., 12-column grid)
- Gutters (spacing between columns)
- Container padding/margins
- Responsive behavior

**Component Hierarchy**:
- Parent-child relationships
- Nesting patterns
- Z-index layers (if critical)

---

### 4. Responsive Specifications

**Extract designs for ALL breakpoints**:

**Mobile (320-640px)**:
- Layout changes (stack vs. row)
- Typography scaling
- Component size adjustments
- Hidden/shown elements
- Touch target sizes (44x44px minimum)

**Tablet (641-1024px)**:
- Layout transitions
- Column changes (1 col → 2 col)
- Component adaptations

**Desktop (1025px+)**:
- Full layout
- Hover states (not applicable on mobile)
- Maximum widths
- Multi-column layouts

**Document differences explicitly**:
```
Header Component:
- Mobile: Logo center, hamburger menu, height 64px
- Tablet: Logo left, visible nav items, height 72px
- Desktop: Logo left, full nav + search, height 80px
```

---

### 5. Assets

**Icons**:
- List all icons used (name, source)
- Sizes (multiple sizes if responsive)
- Colors (if not inheriting from text color)
- Stroke widths (if line icons)

**Images**:
- Source URLs or file references
- Dimensions and aspect ratios
- Alt text (if specified in Figma)
- Lazy loading considerations

**Illustrations/Graphics**:
- Export formats needed (SVG, PNG, etc.)
- Color variations (if theme-aware)

---

## Extraction Quality Checklist

Before marking extraction complete, verify:

- [ ] All colors documented with hex codes and usage notes
- [ ] All typography styles captured with complete specs
- [ ] Spacing scale identified and documented
- [ ] ALL component states documented (not just default)
- [ ] ALL component variants documented
- [ ] Responsive specifications for mobile/tablet/desktop
- [ ] Dimensions include min/max where applicable
- [ ] Interactive states (hover, active, focus) specified
- [ ] Error states and loading states captured
- [ ] Icons and assets listed with sources
- [ ] Shadows and border radius values documented
- [ ] No "approximate" or "similar to" values - exact only

---

## Common Extraction Mistakes

1. **Incomplete state documentation** - Only extracting default state, missing hover/active/disabled
   → Fix: Extract ALL states for every interactive element

2. **Approximating values** - Guessing "about 16px" instead of measuring exactly
   → Fix: Use Figma inspector for exact values

3. **Missing responsive specs** - Only extracting desktop design
   → Fix: Check for mobile/tablet frames and document differences

4. **Vague color descriptions** - "blue" instead of exact hex
   → Fix: Always use hex codes with usage notes

5. **Ignoring component variants** - Only documenting primary button, missing secondary/outline
   → Fix: Systematically extract all variants

6. **Assuming spacing** - Not documenting padding/margins
   → Fix: Measure and document all spacing explicitly

7. **Forgetting disabled states** - Functional states only
   → Fix: Disabled, loading, and error states are critical

8. **No component hierarchy** - Flat list without relationships
   → Fix: Show parent-child relationships and nesting

---

## Documentation Format

**Structure in planning doc**:

```markdown
## Design Specifications (Figma)

### Reference
- File: {Name}
- Frame: {Frame name/path}
- Link: {URL}
- Extracted: {ISO date}

### Design Tokens
[Complete token documentation]

### Component Breakdown
[Each component with all states/variants]

### Layout Specifications
[Page structure and grid system]

### Responsive Specifications
[Mobile/tablet/desktop differences]

### Assets
[Icons, images, illustrations]
```

---

## Validation Before Implementation

When `/execute-plan` reads design specs:

**Check completeness**:
- Can implement without guessing any values?
- Are all states documented?
- Are responsive changes clear?
- Are color references unambiguous?

**If incomplete**:
- Do NOT guess or assume
- Flag missing specs to user
- Either: Re-extract from Figma or ask user for clarification

---

## Key Takeaway

**Completeness prevents re-work.**

Spending extra time on thorough extraction during planning saves hours during implementation. Exact specifications eliminate guesswork, reduce design inconsistencies, and enable confident implementation without accessing Figma MCP again.

Extract once, extract completely, implement accurately.
